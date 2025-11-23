from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, List
import uuid

from models.schemas import (
    ScenarioRequest, Scenario, Play, TrackingRequest,
    TrackedScenario, NewsArticle, Alert, AssetClass
)
from services.gemini_service import GeminiService
from services.news_service import NewsService

app = FastAPI(
    title="Hedge Fund Agent API",
    description="AI-powered trading guidance and scenario analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
gemini_service = GeminiService()
news_service = NewsService()

# In-memory storage (in production, use a database)
scenarios_db: Dict[str, Scenario] = {}
tracked_scenarios_db: Dict[str, TrackedScenario] = {}


@app.get("/")
async def root():
    return {
        "message": "Hedge Fund Agent API",
        "version": "1.0.0",
        "endpoints": {
            "scenarios": "/scenarios",
            "tracking": "/tracking",
            "docs": "/docs"
        }
    }


@app.post("/scenarios", response_model=Scenario)
async def create_scenario(request: ScenarioRequest):
    """
    Create a new scenario and get AI-generated investment plays
    """
    try:
        # Use Gemini to analyze the scenario
        analysis = await gemini_service.analyze_scenario(request.description)
        
        # Generate unique IDs
        scenario_id = str(uuid.uuid4())
        
        # Create Play objects
        plays = []
        for play_data in analysis["plays"]:
            play = Play(
                id=str(uuid.uuid4()),
                asset_class=AssetClass(play_data["asset_class"]),
                title=play_data["title"],
                description=play_data["description"],
                action=play_data["action"],
                instruments=play_data["instruments"],
                rationale=play_data["rationale"],
                risk_level=play_data["risk_level"],
                time_horizon=play_data["time_horizon"],
                confidence_score=play_data["confidence_score"]
            )
            plays.append(play)
        
        # Create Scenario object
        scenario = Scenario(
            id=scenario_id,
            description=request.description,
            interpreted_scenario=analysis["interpreted_scenario"],
            plays=plays,
            created_at=datetime.now(),
            is_tracking=False
        )
        
        # Store in database
        scenarios_db[scenario_id] = scenario
        
        return scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing scenario: {str(e)}")


@app.get("/scenarios", response_model=List[Scenario])
async def list_scenarios():
    """
    Get all created scenarios
    """
    return list(scenarios_db.values())


@app.get("/scenarios/{scenario_id}", response_model=Scenario)
async def get_scenario(scenario_id: str):
    """
    Get a specific scenario by ID
    """
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return scenarios_db[scenario_id]


@app.post("/tracking/start", response_model=TrackedScenario)
async def start_tracking(request: TrackingRequest):
    """
    Start tracking a specific scenario and play
    """
    # Validate scenario exists
    if request.scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario = scenarios_db[request.scenario_id]
    
    # Find the play
    play = None
    for p in scenario.plays:
        if p.id == request.play_id:
            play = p
            break
    
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    
    # Fetch initial news
    try:
        news_articles_data = await news_service.fetch_news_for_scenario(
            scenario.description,
            play.instruments
        )
        
        news_articles = [
            NewsArticle(**article) for article in news_articles_data
        ]
        
        # Generate initial alerts
        alerts_data = await gemini_service.generate_alerts(
            scenario.interpreted_scenario,
            play.dict(),
            news_articles_data
        )
        
        alerts = [
            Alert(
                id=str(uuid.uuid4()),
                scenario_id=scenario.id,
                play_id=play.id,
                message=alert["message"],
                severity=alert["severity"],
                created_at=datetime.now()
            )
            for alert in alerts_data
        ]
        
        # Create tracked scenario
        tracked_scenario = TrackedScenario(
            scenario=scenario,
            play=play,
            news_articles=news_articles,
            alerts=alerts,
            last_updated=datetime.now(),
            play_updates=[]
        )
        
        # Store in database
        tracking_key = f"{request.scenario_id}_{request.play_id}"
        tracked_scenarios_db[tracking_key] = tracked_scenario
        
        # Mark scenario as tracking
        scenario.is_tracking = True
        
        return tracked_scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting tracking: {str(e)}")


@app.get("/tracking", response_model=List[TrackedScenario])
async def list_tracked_scenarios():
    """
    Get all tracked scenarios
    """
    return list(tracked_scenarios_db.values())


@app.get("/tracking/{scenario_id}/{play_id}", response_model=TrackedScenario)
async def get_tracked_scenario(scenario_id: str, play_id: str):
    """
    Get a specific tracked scenario
    """
    tracking_key = f"{scenario_id}_{play_id}"
    
    if tracking_key not in tracked_scenarios_db:
        raise HTTPException(status_code=404, detail="Tracked scenario not found")
    
    return tracked_scenarios_db[tracking_key]


@app.post("/tracking/{scenario_id}/{play_id}/refresh", response_model=TrackedScenario)
async def refresh_tracked_scenario(scenario_id: str, play_id: str):
    """
    Refresh a tracked scenario with latest news and updates
    """
    tracking_key = f"{scenario_id}_{play_id}"
    
    if tracking_key not in tracked_scenarios_db:
        raise HTTPException(status_code=404, detail="Tracked scenario not found")
    
    tracked = tracked_scenarios_db[tracking_key]
    
    try:
        # Fetch latest news
        news_articles_data = await news_service.fetch_news_for_scenario(
            tracked.scenario.description,
            tracked.play.instruments
        )
        
        news_articles = [
            NewsArticle(**article) for article in news_articles_data
        ]
        
        # Check for play updates
        play_update = await gemini_service.update_play_with_news(
            tracked.play.dict(),
            news_articles_data
        )
        
        # Generate new alerts
        alerts_data = await gemini_service.generate_alerts(
            tracked.scenario.interpreted_scenario,
            tracked.play.dict(),
            news_articles_data
        )
        
        new_alerts = [
            Alert(
                id=str(uuid.uuid4()),
                scenario_id=scenario_id,
                play_id=play_id,
                message=alert["message"],
                severity=alert["severity"],
                created_at=datetime.now()
            )
            for alert in alerts_data
        ]
        
        # Update the tracked scenario
        tracked.news_articles = news_articles
        tracked.alerts.extend(new_alerts)
        tracked.last_updated = datetime.now()
        
        # Add play updates if any
        if play_update.get("should_modify") and play_update.get("modifications"):
            tracked.play_updates.append(
                f"[{datetime.now().isoformat()}] {play_update['modifications']}"
            )
            # Update confidence score
            tracked.play.confidence_score = play_update.get("updated_confidence_score", tracked.play.confidence_score)
        
        return tracked
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing tracked scenario: {str(e)}")


@app.delete("/tracking/{scenario_id}/{play_id}")
async def stop_tracking(scenario_id: str, play_id: str):
    """
    Stop tracking a scenario
    """
    tracking_key = f"{scenario_id}_{play_id}"
    
    if tracking_key not in tracked_scenarios_db:
        raise HTTPException(status_code=404, detail="Tracked scenario not found")
    
    # Remove from tracking
    del tracked_scenarios_db[tracking_key]
    
    # Update scenario tracking status
    if scenario_id in scenarios_db:
        scenarios_db[scenario_id].is_tracking = False
    
    return {"message": "Tracking stopped successfully"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scenarios_count": len(scenarios_db),
        "tracked_scenarios_count": len(tracked_scenarios_db)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
