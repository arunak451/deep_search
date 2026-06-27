import requests
import config

def fetch_latest_news(item_name):
    """
    Fetches the top 5 latest news articles matching the selected item name
    using the News API (newsapi.org).
    """
    if not config.NEWS_API_KEY:
        print("⚠️ News API Key not configured! Skipping News fetch.")
        return []

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": item_name,
            "apiKey": config.NEWS_API_KEY,
            "pageSize": 5,
            "sortBy": "relevancy",
            "language": "en"
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ News API returned status code {response.status_code}. Skipping...")
            return []
            
        data = response.json()
        articles = data.get("articles", [])
        
        results = []
        for article in articles[:5]:
            source = article.get("source", {})
            source_name = source.get("name", "N/A")
            
            results.append({
                "title": article.get("title", "N/A"),
                "description": article.get("description", "N/A") or "N/A",
                "url": article.get("url", "N/A"),
                "published_date": article.get("publishedAt", "N/A"),
                "source_name": source_name
            })
            
        return results
        
    except Exception as e:
        print(f"⚠️ News API data fetch failed: {e}")
        return []
