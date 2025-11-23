from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class AssetClass(str, Enum):
    EQUITY = "equity"
    COMMODITY = "commodity"
    FIXED_INCOME = "fixed_income"


class ScenarioRequest(BaseModel):
    description: str = Field(..., description="Natural language description of the market scenario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "S&P 500 down 5% over the next month"
            }
        }


class Play(BaseModel):
    id: str
    asset_class: AssetClass
    title: str
    description: str
    action: str  # e.g., "Buy", "Sell", "Short"
    instruments: List[str]  # e.g., ["SPY", "QQQ"]
    rationale: str
    risk_level: str  # e.g., "Low", "Medium", "High"
    time_horizon: str  # e.g., "Short-term", "Medium-term", "Long-term"
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class Scenario(BaseModel):
    id: str
    description: str
    interpreted_scenario: str
    plays: List[Play]
    created_at: datetime
    is_tracking: bool = False


class TrackingRequest(BaseModel):
    scenario_id: str
    play_id: str


class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    summary: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)


class Alert(BaseModel):
    id: str
    scenario_id: str
    play_id: str
    message: str
    severity: str  # "info", "warning", "critical"
    created_at: datetime


class TrackedScenario(BaseModel):
    scenario: Scenario
    play: Play
    news_articles: List[NewsArticle]
    alerts: List[Alert]
    last_updated: datetime
    play_updates: List[str]  # List of modifications to the play


class PlayUpdate(BaseModel):
    play_id: str
    updates: str
    updated_at: datetime
