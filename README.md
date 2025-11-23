# Hedge Fund Agent

An intelligent trading guidance tool that helps users explore and deploy investment opportunities across equities, commodities, and fixed income markets.

## Features

- **Scenario-Based Analysis**: Drop in market scenarios (e.g., "S&P down 5%", "Fed delays rate cuts") and get AI-powered insights
- **Smart Play Recommendations**: Get 3 recommended investment plays across different asset classes
- **Real-Time Tracking**: Track scenarios and plays with continuous updates from news and market data
- **AI-Powered Intelligence**: Leverages Google Gemini for scenario inference and play optimization
- **Clean Modern UI**: Intuitive interface for managing complex investment strategies

## Project Structure

```
hedge-fund-agent/
├── backend/          # FastAPI backend with Gemini integration
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── requirements.txt
├── frontend/         # Next.js React frontend
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   NEWS_API_KEY=your_news_api_key  # Optional
   ```

5. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

The UI will be available at `http://localhost:3000`

## Usage

1. **Create a Scenario**: Enter a market scenario in natural language (e.g., "Tech sector correction of 10%")
2. **Review Plays**: View AI-generated investment plays across equities, commodities, and fixed income
3. **Track & Monitor**: Start tracking a scenario to receive real-time updates and play adjustments

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Technology Stack

- **Backend**: FastAPI, Python, Google Gemini API
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **AI**: Google Gemini for scenario analysis and recommendations

## License

MIT
