import sys
import os

# Reconfigure stdout/stderr to UTF-8 to prevent UnicodeEncodeError in Windows terminal
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional

# Import DeepDig modules
import config
from search_engine import search_google, search_placement_details
from maps_fetcher import fetch_maps_data
from linkedin_fetcher import fetch_linkedin_data
from youtube_fetcher import fetch_youtube_videos
from news_fetcher import fetch_latest_news
from web_scraper import deep_scrape_website
from ai_summarizer import generate_ai_summary, chat_with_groq
from live_researcher import live_search_and_scrape
from exporter import export_to_text, export_to_excel, export_to_pdf, get_export_filename

def clean_data_list(data_list):
    """
    Removes duplicates, filters invalid values and formats lists.
    """
    if not data_list:
        return ["N/A"]
    clean = list(set([item.strip() for item in data_list if item and item.strip() and item.strip().lower() != "n/a"]))
    return clean if clean else ["N/A"]

app = FastAPI(title="DeepDig AI Research API")

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    """
    Serves the main frontend page.
    """
    return FileResponse("static/index.html")

@app.get("/api/search")
def search_endpoint(q: str):
    """
    Endpoint to search for a keyword and return top 10 search results.
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required.")
        
    results = search_google(q)
    return JSONResponse(content={"results": results})

class ResearchRequest(BaseModel):
    title: str
    link: str

@app.post("/api/research")
def research_endpoint(req: ResearchRequest):
    """
    Executes the 6-channel deep research flow for a selected search item.
    """
    target_name = req.title
    target_link = req.link
    
    # 1. Google Search Deep Dive
    deep_search = search_google(target_name, search_type="organic")
    
    # 2. Google Maps Details
    maps_data = fetch_maps_data(target_name)
    
    # 3. LinkedIn Details
    linkedin_data = fetch_linkedin_data(target_name)
    
    # 4. YouTube Videos
    youtube_data = fetch_youtube_videos(target_name)
    
    # 5. News Articles
    news_data = fetch_latest_news(target_name)
    
    # 6. Website Scrape
    # Resolve official website
    official_website = "N/A"
    if maps_data and maps_data.get("website") and maps_data.get("website") != "N/A":
        official_website = maps_data["website"]
    elif target_link:
        official_website = target_link
        
    scraped_details = {"emails": [], "phones": [], "socials": [], "page_text": "N/A"}
    if official_website and official_website != "N/A":
        scraped_details = deep_scrape_website(official_website)
        
    scraped_emails = clean_data_list(scraped_details.get("emails", []))
    scraped_phones = clean_data_list(scraped_details.get("phones", []))
    scraped_socials = clean_data_list(scraped_details.get("socials", []))
    scraped_text = scraped_details.get("page_text", "N/A")
    
    # 7. Targeted Placement Search
    placement_search = search_placement_details(target_name)
    
    contact_aggregate = {
        "website": official_website,
        "address": maps_data.get("address", "N/A") if maps_data else "N/A",
        "phone_number": maps_data.get("phone_number", "N/A") if maps_data else "N/A",
        "scraped_emails": scraped_emails,
        "scraped_phones": scraped_phones,
        "scraped_socials": scraped_socials
    }
    
    # Compile raw data for Groq
    combined_data = []
    combined_data.append(f"RESEARCH TARGET: {target_name}\n")
    
    if maps_data:
        combined_data.append("--- GOOGLE MAPS ---")
        for k, v in maps_data.items():
            combined_data.append(f"{k}: {v}")
        combined_data.append("")
        
    if linkedin_data:
        combined_data.append("--- LINKEDIN COMPANY DATA ---")
        for k, v in linkedin_data.items():
            combined_data.append(f"{k}: {v}")
        combined_data.append("")
        
    if youtube_data:
        combined_data.append("--- YOUTUBE VIDEOS ---")
        for idx, vid in enumerate(youtube_data):
            combined_data.append(f"Video {idx+1}: {vid['title']}\nURL: {vid['url']}\nViews: {vid['view_count']}\nLikes: {vid['like_count']}\nChannel: {vid['channel_name']}\nDescription: {vid['description']}\n")
        combined_data.append("")
        
    if news_data:
        combined_data.append("--- LATEST NEWS ---")
        for idx, art in enumerate(news_data):
            combined_data.append(f"Article {idx+1}: {art['title']}\nSource: {art['source_name']}\nDate: {art['published_date']}\nURL: {art['url']}\nDescription: {art['description']}\n")
        combined_data.append("")
        
    combined_data.append("--- WEBSITE CONTACTS & SCRAPED CONTENT ---")
    combined_data.append(f"Official Web URL: {official_website}")
    combined_data.append(f"Emails found: {', '.join(scraped_emails)}")
    combined_data.append(f"Phone numbers found: {', '.join(scraped_phones)}")
    combined_data.append(f"Social media profiles found: {', '.join(scraped_socials)}")
    combined_data.append(f"Cleaned Webpage Text Content:\n{scraped_text}")
    combined_data.append("")
    
    if placement_search:
        combined_data.append("--- TARGETED PLACEMENT & CONTACT GOOGLE SEARCH RESULTS ---")
        for res in placement_search:
            combined_data.append(f"Title: {res['title']}\nLink: {res['link']}\nSnippet: {res['snippet']}\n")
        combined_data.append("")
    
    if deep_search:
        combined_data.append("--- DEEP GOOGLE SEARCH RESULTS ---")
        for res in deep_search:
            combined_data.append(f"[{res['index']}] Title: {res['title']}\nLink: {res['link']}\nSnippet: {res['snippet']}\n")
        combined_data.append("")
        
    raw_data_string = "\n".join(combined_data)
    
    # Generate Groq Summary
    ai_report = generate_ai_summary(target_name, raw_data_string)
    
    return JSONResponse(content={
        "title": target_name,
        "ai_report": ai_report,
        "maps_data": maps_data,
        "linkedin_data": linkedin_data,
        "youtube_data": youtube_data,
        "news_data": news_data,
        "contact_data": contact_aggregate,
        "raw_data_string": raw_data_string
    })

class ExportRequest(BaseModel):
    format: str  # 'pdf', 'excel', 'txt'
    title: str
    ai_report: str
    contact_data: dict
    news_data: List[dict]
    youtube_data: List[dict]
    raw_data_string: str

class ChatRequest(BaseModel):
    title: str
    raw_data_string: str
    question: str
    history: Optional[List[dict]] = []

@app.post("/api/export")
def export_endpoint(req: ExportRequest):
    """
    Generates and returns the requested export file dynamically.
    """
    fmt = req.format.lower()
    title = req.title
    report = req.ai_report
    
    filepath = None
    
    if fmt == "pdf":
        filepath = export_to_pdf(title, report)
    elif fmt == "excel":
        filepath = export_to_excel(
            title, report, req.contact_data, req.news_data, req.youtube_data, req.raw_data_string
        )
    elif fmt == "txt":
        filepath = export_to_text(title, report)
    else:
        raise HTTPException(status_code=400, detail="Invalid export format. Must be pdf, excel, or txt.")
        
    if not filepath or not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail=f"Failed to generate export file for format '{fmt}'.")
        
    # Return file for download
    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/octet-stream"
    )

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Exposes chatbot functionality with LIVE web research.
    For every question, performs a real-time Google search + scrape,
    then combines with existing data before sending to Groq AI.
    """
    # Step 1: Perform live web research for this specific question
    print(f"🤖 Chat question received: {req.question}")
    live_data = live_search_and_scrape(req.title, req.question)
    
    # Step 2: Send both live + pre-collected data to Groq
    answer = chat_with_groq(
        req.title, 
        req.raw_data_string, 
        req.question, 
        req.history,
        live_research_data=live_data
    )
    return JSONResponse(content={"answer": answer})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"🚀 Starting DeepDig Web Server on http://localhost:{port}...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
