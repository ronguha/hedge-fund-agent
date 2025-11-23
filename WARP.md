# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Hedge Fund Agent is an AI-powered trading guidance tool that helps users analyze market scenarios and get investment recommendations across equities, commodities, and fixed income. The system uses Google Gemini AI to analyze market scenarios, generate investment plays, and provide real-time tracking with news updates.

## Architecture

### High-Level Structure

The project follows a **client-server architecture** with clear separation of concerns:

- **Backend (FastAPI)**: RESTful API server that orchestrates AI analysis, news fetching, and scenario management
- **Frontend (Next.js)**: React-based UI with client-side state management and API integration

### Key Architectural Patterns

**Backend Services Layer**:
- `GeminiService`: Handles all AI interactions including scenario analysis, play updates, and alert generation
- `NewsService`: Manages news fetching from NewsAPI and RSS feeds with relevance scoring
- All services are instantiated at app startup and shared across requests

**Data Flow**:
1. User submits scenario description → Backend analyzes with Gemini → Returns 3 investment plays (equity, commodity, fixed income)
2. User tracks a play → Backend fetches news, generates alerts → Creates TrackedScenario
3. Refresh tracked scenario → Backend re-fetches news, checks for play modifications, generates new alerts

**In-Memory Storage**: 
- The backend uses dictionaries (`scenarios_db`, `tracked_scenarios_db`) for storage
- This is intentionally temporary; in production, replace with a database
- Data is lost on server restart

**State Management**:
- Frontend uses React state hooks to manage scenarios, plays, and tracking state
- No global state management library (Redux/Zustand) currently used
- API client (`frontend/src/lib/api.ts`) provides typed interfaces for all backend interactions

## Development Commands

### Backend

**Setup and run**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Required environment variables** (create `backend/.env`):
```
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_news_api_key_here  # Optional
```

**Start development server**:
```bash
cd backend
uvicorn main:app --reload
```

**View API documentation**:
- Interactive docs: http://localhost:8000/docs
- Alternative: http://localhost:8000/redoc

**Run backend directly**:
```bash
cd backend
python main.py
```

### Frontend

**Setup and run**:
```bash
cd frontend
npm install
```

**Required environment variables** (create `frontend/.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Start development server**:
```bash
cd frontend
npm run dev
```

**Build for production**:
```bash
cd frontend
npm run build
npm start
```

**Lint**:
```bash
cd frontend
npm run lint
```

## Key Files and Components

### Backend Core Files

- `backend/main.py`: FastAPI application with all API endpoints (scenarios, tracking, health)
- `backend/models/schemas.py`: Pydantic models defining data structures (Scenario, Play, Alert, etc.)
- `backend/services/gemini_service.py`: AI service for scenario analysis and play generation
- `backend/services/news_service.py`: News aggregation from NewsAPI and RSS feeds

### Frontend Core Files

- `frontend/src/lib/api.ts`: API client with typed interfaces matching backend schemas
- `frontend/src/app/page.tsx`: Main application with view state management (create/plays/tracking)
- `frontend/src/components/ScenarioInput.tsx`: Input form for market scenarios
- `frontend/src/components/PlayCard.tsx`: Display individual investment plays
- `frontend/src/components/TrackingDashboard.tsx`: Real-time tracking interface

## Important Implementation Details

### Gemini AI Integration

The `GeminiService` uses prompt engineering to extract structured JSON responses from Gemini:
- Prompts specify exact JSON schema in the prompt text
- Response parsing handles markdown code blocks (```json)
- Falls back to direct JSON parsing if no code blocks present

**Key methods**:
- `analyze_scenario()`: Returns interpreted scenario + 3 plays (one per asset class)
- `update_play_with_news()`: Determines if play should be modified based on news
- `generate_alerts()`: Creates alerts based on scenario/play/news combination

### News Fetching Strategy

The `NewsService` uses a **fallback pattern**:
1. Try NewsAPI if `NEWS_API_KEY` is set (better relevance, requires API key)
2. Fall back to RSS feeds (Reuters, Bloomberg, FT) with keyword matching
3. Sort by relevance score and recency, return top 10 articles

### TypeScript/Python Type Alignment

Frontend TypeScript interfaces in `api.ts` mirror backend Pydantic models in `schemas.py`:
- Both use the same field names and structure
- Enums like `AssetClass` match exactly
- DateTime fields are serialized as ISO strings

## API Endpoints

**Scenarios**:
- `POST /scenarios` - Create scenario and get investment plays
- `GET /scenarios` - List all scenarios
- `GET /scenarios/{id}` - Get specific scenario

**Tracking**:
- `POST /tracking/start` - Start tracking a scenario/play combination
- `GET /tracking` - List all tracked scenarios
- `GET /tracking/{scenario_id}/{play_id}` - Get specific tracked scenario
- `POST /tracking/{scenario_id}/{play_id}/refresh` - Refresh with latest news
- `DELETE /tracking/{scenario_id}/{play_id}` - Stop tracking

**Health**:
- `GET /health` - Health check with database counts

## Environment Configuration

**Backend** requires:
- `GEMINI_API_KEY` (required): Google Gemini API key for AI analysis
- `NEWS_API_KEY` (optional): NewsAPI.org key for enhanced news fetching

**Frontend** requires:
- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to http://localhost:8000)

## Technology Stack

**Backend**:
- FastAPI (web framework)
- Google Gemini AI (via `google-generativeai` SDK)
- Pydantic v2 (data validation)
- aiohttp (async HTTP client)
- feedparser (RSS feed parsing)

**Frontend**:
- Next.js 14 (React framework with App Router)
- TypeScript (type safety)
- Tailwind CSS (styling)
- axios (HTTP client)
- lucide-react (icons)
