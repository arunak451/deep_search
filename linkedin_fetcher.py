import requests
import config

def fetch_linkedin_data(item_name):
    """
    Fetches company details from RapidAPI LinkedIn Data API.
    Uses 'search-companies' to find the company profile, and 'get-company-details'
    to retrieve detailed metadata.
    """
    if not config.RAPIDAPI_KEY:
        print("⚠️ RapidAPI Key not configured! Skipping LinkedIn data fetch.")
        return None

    headers = {
        "X-RapidAPI-Key": config.RAPIDAPI_KEY,
        "X-RapidAPI-Host": config.RAPIDAPI_HOST
    }

    try:
        # Step 1: Search for the company to get username / id
        search_url = f"https://{config.RAPIDAPI_HOST}/search-companies"
        
        # Try both 'query' and 'keyword' parameter conventions
        params = {"query": item_name}
        response = requests.get(search_url, headers=headers, params=params, timeout=15)
        
        # Fallback to 'keyword' if needed
        if response.status_code == 400 or response.status_code == 422:
            params = {"keyword": item_name}
            response = requests.get(search_url, headers=headers, params=params, timeout=15)

        if response.status_code != 200:
            print(f"⚠️ LinkedIn search endpoint returned status code {response.status_code}. Skipping...")
            return None

        search_results = response.json()
        
        # Parse search results
        # Depending on API response, it could be a list or a dictionary containing a list
        companies = []
        if isinstance(search_results, list):
            companies = search_results
        elif isinstance(search_results, dict):
            companies = search_results.get("items", search_results.get("data", []))
            
        if not companies:
            print("⚠️ No LinkedIn company profiles matched this query.")
            return None

        # Take the first matched company
        company_info = companies[0]
        # Get username or universal name to look up details
        username = company_info.get("username") or company_info.get("universalName") or company_info.get("id")
        
        if not username:
            print("⚠️ Matched company has no valid username/id.")
            return None

        # Step 2: Fetch company details using the username/id
        details_url = f"https://{config.RAPIDAPI_HOST}/get-company-details"
        details_params = {"username": username}
        
        details_resp = requests.get(details_url, headers=headers, params=details_params, timeout=15)
        
        # Fallback to 'id' parameter if username doesn't work
        if details_resp.status_code != 200:
            details_params = {"id": username}
            details_resp = requests.get(details_url, headers=headers, params=details_params, timeout=15)

        if details_resp.status_code == 200:
            details = details_resp.json()
        else:
            # Fallback to search result itself if details endpoint fails
            print("⚠️ LinkedIn details fetch failed, falling back to search result summary...")
            details = company_info

        # Extract Fields (with fallback variations)
        name = details.get("name") or details.get("companyName") or company_info.get("name") or "N/A"
        description = details.get("description") or details.get("about") or details.get("tagline") or "N/A"
        
        # Employee count
        employee_count = details.get("staffCount") or details.get("employeeCount") or "N/A"
        if employee_count == "N/A" and "staffCountRange" in details:
            employee_count = details["staffCountRange"]
            
        # Headquarters Location
        hq = details.get("headquarter") or details.get("hq") or {}
        hq_loc = "N/A"
        if isinstance(hq, dict):
            parts = [hq.get("city"), hq.get("geographicArea") or hq.get("state"), hq.get("country")]
            parts = [p for p in parts if p]
            if parts:
                hq_loc = ", ".join(parts)
        elif isinstance(hq, str):
            hq_loc = hq
            
        if hq_loc == "N/A" and "locations" in details and isinstance(details["locations"], list) and len(details["locations"]) > 0:
            loc = details["locations"][0]
            if isinstance(loc, dict):
                parts = [loc.get("city"), loc.get("state"), loc.get("country")]
                parts = [p for p in parts if p]
                if parts:
                    hq_loc = ", ".join(parts)

        linkedin_url = details.get("linkedinUrl") or details.get("url") or f"https://www.linkedin.com/company/{username}"
        industry = details.get("industry") or details.get("companyIndustries") or "N/A"
        if isinstance(industry, list) and len(industry) > 0:
            industry = industry[0]
            
        founded = details.get("founded") or details.get("foundedYear") or "N/A"

        return {
            "company_name": name,
            "company_description": description,
            "employee_count": employee_count,
            "headquarters_location": hq_loc,
            "linkedin_url": linkedin_url,
            "industry_type": industry,
            "founded_year": founded
        }

    except Exception as e:
        print(f"⚠️ LinkedIn data fetch failed: {e}, skipping...")
        return None
