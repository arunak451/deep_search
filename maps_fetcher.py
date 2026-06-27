from serpapi import GoogleSearch
import config

def fetch_maps_data(item_name):
    """
    Fetches place details from Google Maps via SerpApi google_maps engine.
    Extracts place name, rating, reviews count, address, phone, website,
    opening hours, thumbnail, and GPS coordinates.
    """
    if not config.SERP_API_KEY:
        print("⚠️ SerpApi Key not configured! Skipping Google Maps fetch.")
        return None

    try:
        params = {
            "engine": "google_maps",
            "q": item_name,
            "api_key": config.SERP_API_KEY
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            print(f"⚠️ Google Maps Error: {results['error']}")
            return None
            
        place = None
        
        # SerpApi can return either 'place_results' (direct place profile) or 
        # a list of search results in 'local_results' or 'places'.
        if "place_results" in results:
            place = results["place_results"]
        elif "local_results" in results and len(results["local_results"]) > 0:
            place = results["local_results"][0]
        elif "places" in results and len(results["places"]) > 0:
            place = results["places"][0]
            
        if not place:
            print("⚠️ No Google Maps location found for this item.")
            return None
            
        # Parse GPS Coordinates
        gps = place.get("gps_coordinates", {})
        latitude = gps.get("latitude", "N/A")
        longitude = gps.get("longitude", "N/A")
        
        # Parse Operating Hours
        operating_hours = place.get("operating_hours", {})
        if isinstance(operating_hours, dict):
            # Format hours as daily schedule if available, else check standard hours
            hours_list = []
            for day, time in operating_hours.items():
                if day != "schedule":
                    hours_list.append(f"{day}: {time}")
            hours_str = ", ".join(hours_list) if hours_list else "N/A"
        else:
            hours_str = str(operating_hours) if operating_hours else "N/A"
            
        data = {
            "place_name": place.get("title", "N/A"),
            "rating": place.get("rating", "N/A"),
            "reviews_count": place.get("reviews", "N/A"),
            "address": place.get("address", "N/A"),
            "phone_number": place.get("phone", "N/A"),
            "website": place.get("website", "N/A"),
            "opening_hours": hours_str,
            "thumbnail": place.get("thumbnail", "N/A"),
            "latitude": latitude,
            "longitude": longitude
        }
        
        return data
        
    except Exception as e:
        print(f"⚠️ Google Maps data fetch failed: {e}")
        return None
