import aiohttp
import feedparser
from typing import List, Dict
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class NewsService:
    """
    Service for fetching financial news relevant to scenarios and plays
    """
    
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        # RSS feeds for financial news (fallback if no API key)
        self.rss_feeds = [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.ft.com/rss/home",
        ]
    
    async def fetch_news_for_scenario(self, scenario: str, instruments: List[str]) -> List[Dict]:
        """
        Fetch news articles relevant to a scenario and instruments
        """
        articles = []
        
        # Try NewsAPI if key is available
        if self.news_api_key:
            articles.extend(await self._fetch_from_newsapi(scenario, instruments))
        
        # Fallback to RSS feeds
        if len(articles) < 5:
            articles.extend(await self._fetch_from_rss(scenario, instruments))
        
        # Sort by relevance and recency
        articles.sort(key=lambda x: (x['relevance_score'], x['published_at']), reverse=True)
        
        return articles[:10]  # Return top 10
    
    async def _fetch_from_newsapi(self, scenario: str, instruments: List[str]) -> List[Dict]:
        """
        Fetch from NewsAPI (if API key available)
        """
        articles = []
        
        try:
            # Build query from scenario and instruments
            query_terms = [scenario] + instruments
            query = " OR ".join(query_terms)
            
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": self.news_api_key,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": 10,
                "from": (datetime.now() - timedelta(days=7)).isoformat(),
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for article in data.get("articles", []):
                            articles.append({
                                "title": article.get("title", ""),
                                "url": article.get("url", ""),
                                "source": article.get("source", {}).get("name", "Unknown"),
                                "published_at": datetime.fromisoformat(
                                    article.get("publishedAt", "").replace("Z", "+00:00")
                                ),
                                "summary": article.get("description", "")[:200],
                                "relevance_score": 0.8,  # NewsAPI relevancy
                            })
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
        
        return articles
    
    async def _fetch_from_rss(self, scenario: str, instruments: List[str]) -> List[Dict]:
        """
        Fetch from RSS feeds as fallback
        """
        articles = []
        
        try:
            for feed_url in self.rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:5]:  # Top 5 from each feed
                        # Simple relevance scoring based on keywords
                        text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
                        relevance = sum(
                            1 for term in (scenario.lower().split() + [i.lower() for i in instruments])
                            if term in text
                        )
                        
                        if relevance > 0:
                            published = entry.get("published_parsed")
                            pub_date = datetime(*published[:6]) if published else datetime.now()
                            
                            articles.append({
                                "title": entry.get("title", ""),
                                "url": entry.get("link", ""),
                                "source": feed.feed.get("title", "RSS Feed"),
                                "published_at": pub_date,
                                "summary": entry.get("summary", "")[:200],
                                "relevance_score": min(relevance / 5.0, 1.0),
                            })
                except Exception as e:
                    print(f"Error parsing feed {feed_url}: {e}")
                    continue
        except Exception as e:
            print(f"Error fetching RSS feeds: {e}")
        
        return articles
    
    async def get_market_sentiment(self, instruments: List[str]) -> Dict:
        """
        Get overall market sentiment for given instruments
        """
        articles = await self.fetch_news_for_scenario("market analysis", instruments)
        
        # Simple sentiment analysis based on keywords
        positive_keywords = ["rally", "gain", "up", "bullish", "growth", "surge"]
        negative_keywords = ["fall", "drop", "down", "bearish", "decline", "crash"]
        
        sentiment_score = 0
        for article in articles:
            text = (article["title"] + " " + article["summary"]).lower()
            sentiment_score += sum(1 for kw in positive_keywords if kw in text)
            sentiment_score -= sum(1 for kw in negative_keywords if kw in text)
        
        total_articles = len(articles)
        normalized_sentiment = sentiment_score / max(total_articles, 1)
        
        return {
            "score": max(-1.0, min(1.0, normalized_sentiment)),
            "articles_analyzed": total_articles,
            "sentiment": "positive" if normalized_sentiment > 0.2 else "negative" if normalized_sentiment < -0.2 else "neutral"
        }
