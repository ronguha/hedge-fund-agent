import os
import json
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def analyze_scenario(self, scenario_description: str) -> Dict:
        """
        Analyze a market scenario and generate investment plays
        """
        prompt = f"""You are a hedge fund analyst. Analyze the following market scenario and provide detailed investment recommendations.

Scenario: {scenario_description}

Please provide:
1. A clear interpretation of what this scenario means for the markets
2. THREE specific investment plays - one each for:
   - Equities
   - Commodities  
   - Fixed Income

For each play, provide:
- A clear title
- Detailed description
- Specific action (Buy/Sell/Short/Long)
- Specific instruments (ticker symbols, ETFs, or asset names)
- Detailed rationale explaining why this play makes sense
- Risk level (Low/Medium/High)
- Time horizon (Short-term: <3 months, Medium-term: 3-12 months, Long-term: >12 months)
- Confidence score (0.0 to 1.0)

Return your response as a JSON object with this exact structure:
{{
  "interpreted_scenario": "clear interpretation of the scenario",
  "plays": [
    {{
      "asset_class": "equity",
      "title": "play title",
      "description": "detailed description",
      "action": "Buy/Sell/Short/Long",
      "instruments": ["TICKER1", "TICKER2"],
      "rationale": "why this play makes sense",
      "risk_level": "Low/Medium/High",
      "time_horizon": "Short-term/Medium-term/Long-term",
      "confidence_score": 0.75
    }},
    {{
      "asset_class": "commodity",
      ...
    }},
    {{
      "asset_class": "fixed_income",
      ...
    }}
  ]
}}
"""
        
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON from markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(text)
            return result
        except json.JSONDecodeError as e:
            # Fallback: try to parse without code blocks
            return json.loads(text)
    
    async def update_play_with_news(self, play: Dict, news_articles: List[Dict]) -> Dict:
        """
        Update a play based on latest news and market information
        """
        news_summary = "\n".join([
            f"- {article['title']}: {article['summary']}"
            for article in news_articles[:5]  # Use top 5 most relevant
        ])
        
        prompt = f"""You are a hedge fund analyst monitoring an active investment play. Based on recent news, provide updates or modifications to the play if needed.

Current Play:
- Asset Class: {play['asset_class']}
- Title: {play['title']}
- Action: {play['action']}
- Instruments: {', '.join(play['instruments'])}
- Rationale: {play['rationale']}
- Risk Level: {play['risk_level']}

Recent News:
{news_summary}

Please provide:
1. Whether the play should be modified (yes/no)
2. If yes, what specific changes should be made
3. Updated confidence score (0.0 to 1.0)
4. Any new alerts or warnings

Return your response as JSON:
{{
  "should_modify": true/false,
  "modifications": "description of changes, or empty string if no changes",
  "updated_confidence_score": 0.75,
  "alerts": ["alert message 1", "alert message 2"]
}}
"""
        
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON from markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(text)
            return result
        except json.JSONDecodeError:
            return json.loads(text)
    
    async def generate_alerts(self, scenario: str, play: Dict, news_articles: List[Dict]) -> List[Dict]:
        """
        Generate alerts based on scenario, play, and news
        """
        news_summary = "\n".join([
            f"- {article['title']}"
            for article in news_articles[:3]
        ])
        
        prompt = f"""You are monitoring an investment scenario. Analyze if any alerts should be triggered.

Scenario: {scenario}
Play: {play['title']} - {play['action']} {', '.join(play['instruments'])}

Recent News:
{news_summary}

Generate alerts if there are:
- Significant market movements affecting the play
- News that contradicts the play thesis
- Risk level changes

Return as JSON array:
[
  {{
    "message": "alert message",
    "severity": "info/warning/critical"
  }}
]

If no alerts needed, return empty array: []
"""
        
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            result = json.loads(text)
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            return []
