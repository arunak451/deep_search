from serpapi import GoogleSearch
import config

def search_google(keyword, search_type="mixed"):
    """
    Searches Google via SerpApi.
    If search_type is 'mixed', it queries Google Maps and Google Organic search,
    combines and returns the top 10 merged results prioritizing place entities.
    If search_type is 'organic', it returns only standard organic results.
    Each result contains 'title', 'link', and 'snippet'.
    """
    if not config.SERP_API_KEY:
        print("⚠️ SerpApi Key not configured! Skipping Google search.")
        return []
    
    organic_results = []
    maps_results = []
    
    # 1. Fetch Organic Search Results
    try:
        params = {
            "q": keyword,
            "api_key": config.SERP_API_KEY,
            "num": 20
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" not in results:
            organic_raw = results.get("organic_results", [])
            for item in organic_raw[:20]:
                organic_results.append({
                    "title": item.get("title", "N/A"),
                    "link": item.get("link", "N/A"),
                    "snippet": item.get("snippet", "N/A")
                })
        else:
            print(f"⚠️ SerpApi Organic Search Error: {results['error']}")
    except Exception as e:
        print(f"⚠️ Google Organic Search failed: {e}")
        
    # 2. Fetch Google Maps Results (only if search_type is 'mixed')
    if search_type == "mixed":
        try:
            maps_params = {
                "engine": "google_maps",
                "q": keyword,
                "api_key": config.SERP_API_KEY
            }
            search = GoogleSearch(maps_params)
            results = search.get_dict()
            
            if "error" not in results:
                places = results.get("local_results", []) or results.get("places", [])
                for item in places[:20]:
                    title = item.get("title")
                    if not title:
                        continue
                    # For local places, website is the ideal link. Fallback to Maps link if not present.
                    link = item.get("website") or item.get("link") or "N/A"
                    rating = item.get("rating", "N/A")
                    reviews = item.get("reviews", "N/A")
                    address = item.get("address", "N/A")
                    place_type = item.get("type", "Local Entity")
                    
                    snippet = f"[{place_type}] ⭐ {rating} ({reviews} reviews) | {address}"
                    maps_results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
            else:
                print(f"⚠️ SerpApi Google Maps Search Error: {results['error']}")
        except Exception as e:
            print(f"⚠️ Google Maps Search failed: {e}")
            
    # 3. Merge Results (Prioritize Maps/Place entities for entity discovery)
    combined = []
    seen_titles = set()
    
    # Prepend local map listings
    for item in maps_results:
        title_lower = item["title"].lower().strip()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            combined.append(item)
            
    # Append organic listings
    for item in organic_results:
        title_lower = item["title"].lower().strip()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            combined.append(item)
            
    # Format and index the combined results
    formatted_results = []
    for index, item in enumerate(combined[:20]):
        formatted_results.append({
            "index": index + 1,
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })
        
    return formatted_results

def search_placement_details(target_name):
    """
    Performs a targeted Google search via SerpApi to find placement officer names,
    emails, and contact info for the target entity.
    """
    if not config.SERP_API_KEY:
        print("⚠️ SerpApi Key not configured! Skipping placement dorking search.")
        return []
        
    query = f'"{target_name}" (placement officer OR placement coordinator OR placement contact) (name OR email OR phone OR mobile)'
    print(f"🔍 Running targeted placement search: {query}...")
    
    try:
        params = {
            "q": query,
            "api_key": config.SERP_API_KEY,
            "num": 5
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        placement_snippets = []
        if "error" not in results:
            organic_raw = results.get("organic_results", [])
            for item in organic_raw[:5]:
                placement_snippets.append({
                    "title": item.get("title", "N/A"),
                    "link": item.get("link", "N/A"),
                    "snippet": item.get("snippet", "N/A")
                })
            return placement_snippets
        else:
            print(f"⚠️ SerpApi Placement Search Error: {results['error']}")
    except Exception as e:
        print(f"⚠️ SerpApi Placement Search failed: {e}")
        
    return []

