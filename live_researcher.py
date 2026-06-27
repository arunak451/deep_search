"""
Live Researcher Module
Performs real-time Google search + web scraping for each chatbot question.
This ensures the chatbot can find deep, specific answers instead of relying
only on the initial research data.
"""

from serpapi import GoogleSearch
from web_scraper import get_page_content, extract_page_text, extract_contact_info
import config


def live_search_and_scrape(entity_name, question):
    """
    Performs a targeted Google search using the entity name + user's question,
    then scrapes the top result pages to extract detailed content.
    
    Returns a string with all the freshly scraped data combined.
    """
    if not config.SERP_API_KEY:
        print("⚠️ SerpApi Key not configured! Cannot perform live research.")
        return ""

    # Build a targeted search query
    search_query = f'"{entity_name}" {question}'
    print(f"🔍 Live Research: Searching Google for: {search_query}")

    try:
        params = {
            "q": search_query,
            "api_key": config.SERP_API_KEY,
            "num": 5
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            print(f"⚠️ SerpApi Live Search Error: {results['error']}")
            return ""

        organic_results = results.get("organic_results", [])
        if not organic_results:
            print("⚠️ No organic results found for live research query.")
            return ""

        # Collect snippets from all search results first
        combined_parts = []
        combined_parts.append(f"=== LIVE GOOGLE SEARCH RESULTS FOR: {search_query} ===\n")

        for idx, item in enumerate(organic_results[:5]):
            title = item.get("title", "N/A")
            link = item.get("link", "N/A")
            snippet = item.get("snippet", "N/A")
            combined_parts.append(f"Result {idx+1}: {title}")
            combined_parts.append(f"URL: {link}")
            combined_parts.append(f"Snippet: {snippet}\n")

        # Now scrape the top 3 result pages for detailed content
        urls_to_scrape = []
        for item in organic_results[:2]:
            link = item.get("link", "")
            if link and link != "N/A":
                urls_to_scrape.append(link)

        combined_parts.append("\n=== DETAILED SCRAPED CONTENT FROM TOP RESULTS ===\n")

        for url in urls_to_scrape:
            print(f"🌐 Live scraping: {url}...")
            try:
                html_content = get_page_content(url)
                if html_content:
                    # Extract readable text
                    page_text = extract_page_text(html_content)
                    if page_text and len(page_text.strip()) > 50:
                        combined_parts.append(f"--- SCRAPED FROM: {url} ---")
                        combined_parts.append(page_text[:2000])  # Cap at 2KB per page
                        combined_parts.append("")

                    # Extract contact info from scraped pages
                    emails, phones, socials = extract_contact_info(html_content)
                    if emails:
                        combined_parts.append(f"Emails found on page: {', '.join(emails)}")
                    if phones:
                        combined_parts.append(f"Phones found on page: {', '.join(phones)}")
                    if socials:
                        combined_parts.append(f"Social links found: {', '.join(socials)}")
                    combined_parts.append("")
            except Exception as e:
                print(f"⚠️ Failed to scrape {url}: {e}")
                continue

        live_data = "\n".join(combined_parts)

        # Also try an answer box or knowledge graph if present
        answer_box = results.get("answer_box", {})
        if answer_box:
            ab_answer = answer_box.get("answer") or answer_box.get("snippet") or answer_box.get("result", "")
            if ab_answer:
                live_data += f"\n\n=== GOOGLE ANSWER BOX ===\n{ab_answer}\n"

        knowledge_graph = results.get("knowledge_graph", {})
        if knowledge_graph:
            live_data += "\n=== GOOGLE KNOWLEDGE GRAPH ===\n"
            for key, value in knowledge_graph.items():
                if isinstance(value, str) and len(value) < 500:
                    live_data += f"{key}: {value}\n"

        # Cap total live data to ~5KB to fit within Groq free tier token limits
        live_data = live_data[:5000]

        print(f"✅ Live research completed. Collected {len(live_data)} chars of fresh data.")
        return live_data

    except Exception as e:
        print(f"⚠️ Live research failed: {e}")
        return ""
