from googleapiclient.discovery import build
import config

def fetch_youtube_videos(item_name):
    """
    Searches YouTube for the selected item and returns the top 5 related videos
    with detailed statistics (views, likes, channel name, description, etc.).
    """
    if not config.YOUTUBE_API_KEY:
        print("⚠️ YouTube API Key not configured! Skipping YouTube fetch.")
        return []

    try:
        # Build YouTube client
        youtube = build("youtube", "v3", developerKey=config.YOUTUBE_API_KEY)
        
        # Step 1: Search for top 5 videos matching the item name
        search_request = youtube.search().list(
            q=item_name,
            part="id,snippet",
            maxResults=5,
            type="video"
        )
        search_response = search_request.execute()
        
        items = search_response.get("items", [])
        if not items:
            print("⚠️ No YouTube videos found for this topic.")
            return []
            
        video_ids = [item["id"]["videoId"] for item in items if "videoId" in item.get("id", {})]
        
        if not video_ids:
            print("⚠️ No video IDs retrieved.")
            return []
            
        # Step 2: Fetch detailed statistics (views, likes) for these video IDs
        videos_request = youtube.videos().list(
            id=",".join(video_ids),
            part="snippet,statistics"
        )
        videos_response = videos_request.execute()
        
        video_details = videos_response.get("items", [])
        
        results = []
        for video in video_details:
            snippet = video.get("snippet", {})
            stats = video.get("statistics", {})
            video_id = video.get("id")
            
            title = snippet.get("title", "N/A")
            video_url = f"https://youtube.com/watch?v={video_id}" if video_id else "N/A"
            views = stats.get("viewCount", "N/A")
            likes = stats.get("likeCount", "N/A")
            published_date = snippet.get("publishedAt", "N/A")
            channel_name = snippet.get("channelTitle", "N/A")
            description = snippet.get("description", "N/A")
            short_description = description[:200] + "..." if len(description) > 200 else description
            
            results.append({
                "title": title,
                "url": video_url,
                "view_count": views,
                "like_count": likes,
                "published_date": published_date,
                "channel_name": channel_name,
                "description": short_description
            })
            
        return results

    except Exception as e:
        print(f"⚠️ YouTube API data fetch failed: {e}")
        return []
