import wikipedia

# Set language to English
wikipedia.set_lang("en")

def fetch_wikipedia_summary(entity_name):
    """
    Searches Wikipedia for the given entity name, retrieves the page summary,
    and returns a dictionary containing page title, summary, and page URL.
    """
    try:
        # Search for matching pages
        search_results = wikipedia.search(entity_name)
        if not search_results:
            return None
            
        # Select the first page result
        page_title = search_results[0]
        
        try:
            # Load page details
            page = wikipedia.page(page_title, auto_suggest=False)
            return {
                "title": page.title,
                "summary": page.summary,
                "url": page.url
            }
        except wikipedia.DisambiguationError as de:
            # If it's a disambiguation page, try the first alternative option
            if de.options:
                alt_title = de.options[0]
                page = wikipedia.page(alt_title, auto_suggest=False)
                return {
                    "title": page.title,
                    "summary": page.summary,
                    "url": page.url
                }
            return None
        except wikipedia.PageError:
            return None
            
    except Exception as e:
        print(f"⚠️ Wikipedia summary fetch failed: {e}")
        return None
