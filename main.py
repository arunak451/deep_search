import sys
import os

# Reconfigure stdout/stderr to UTF-8 to prevent UnicodeEncodeError in Windows terminal
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import urllib.parse
import config
from search_engine import search_google, search_placement_details
from maps_fetcher import fetch_maps_data
from linkedin_fetcher import fetch_linkedin_data
from youtube_fetcher import fetch_youtube_videos
from news_fetcher import fetch_latest_news
from web_scraper import deep_scrape_website
from ai_summarizer import generate_ai_summary
from exporter import export_to_text, export_to_excel, export_to_pdf

def get_domain(url):
    """
    Helper to extract hostname from a website URL.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc or url
    except Exception:
        return url

def clean_data_list(data_list):
    """
    Removes duplicates, filters invalid values and formats lists.
    """
    if not data_list:
        return ["N/A"]
    clean = list(set([item.strip() for item in data_list if item and item.strip() and item.strip().lower() != "n/a"]))
    return clean if clean else ["N/A"]

def main():
    print("=" * 60)
    print("         🔍 DeepDig: AI-POWERED DEEP RESEARCH ENGINE         ")
    print("=" * 60)
    
    # Validate API keys
    config.validate_config()
    
    while True:
        try:
            # Step 1: User Input
            keyword = input("\n🔍 Search Keyword: ").strip()
            if not keyword:
                print("⚠️ Search keyword cannot be empty. Try again.")
                continue
                
            print(f"\n🔎 Searching Google for '{keyword}'...")
            search_results = search_google(keyword)
            
            if not search_results:
                print("❌ No results found or SerpApi search failed.")
                retry = input("Do you want to search for something else? (yes/no): ").strip().lower()
                if retry in ['yes', 'y']:
                    continue
                else:
                    break
                    
            print("\nTop 10 Google Search Results:")
            print("-" * 50)
            for res in search_results:
                # Extract clean hostname for pretty formatting
                domain = get_domain(res['link'])
                print(f"{res['index']}. {res['title']} - {domain}")
            print("-" * 50)
            
            # Select target
            selection = None
            while True:
                sel_str = input("\n👉 Etha pathi deep research pannanum? Enter Number (1-10) or '0' to search again: ").strip()
                if sel_str == '0':
                    break
                try:
                    num = int(sel_str)
                    if 1 <= num <= len(search_results):
                        selection = search_results[num - 1]
                        break
                    else:
                        print(f"⚠️ Invalid choice. Please enter a number between 1 and {len(search_results)}.")
                except ValueError:
                    print("⚠️ Please enter a valid number.")
            
            if sel_str == '0' or not selection:
                continue
                
            selected_item_name = selection['title']
            selected_item_link = selection['link']
            
            print(f"\n🚀 Initiating Deep Research on: '{selected_item_name}'")
            print("=" * 50)
            
            # --- 3A. Google Search Deep Dive ---
            print("🔍 Step 1/6: Google Search Deep Dive...", end="", flush=True)
            deep_search_results = search_google(selected_item_name, search_type="organic")
            print(f" ✅ Done ({len(deep_search_results)} results found)")
            
            # --- 3B. Google Maps ---
            print("🗺️ Step 2/6: Google Maps Data...", end="", flush=True)
            maps_data = fetch_maps_data(selected_item_name)
            if maps_data:
                rating = maps_data.get("rating", "N/A")
                print(f" ✅ Done (Rating: {rating})")
            else:
                print(" ⚠️ Skipped / No data found")
                
            # --- 3C. LinkedIn ---
            print("💼 Step 3/6: LinkedIn Company Details...", end="", flush=True)
            linkedin_data = fetch_linkedin_data(selected_item_name)
            if linkedin_data:
                print(" ✅ Done (Profile found)")
            else:
                print(" ⚠️ Skipped / Details not found")
                
            # --- 3D. YouTube ---
            print("🎥 Step 4/6: YouTube Videos...", end="", flush=True)
            youtube_data = fetch_youtube_videos(selected_item_name)
            print(f" ✅ Done ({len(youtube_data)} videos found)")
            
            # --- 3E. News ---
            print("📰 Step 5/6: News Articles...", end="", flush=True)
            news_data = fetch_latest_news(selected_item_name)
            print(f" ✅ Done ({len(news_data)} articles found)")
            
            # --- 3F. Website Scrape ---
            # Resolve official site: prefer Maps website, fallback to the top Google search link
            official_website = "N/A"
            if maps_data and maps_data.get("website") and maps_data.get("website") != "N/A":
                official_website = maps_data["website"]
            elif selected_item_link:
                official_website = selected_item_link
                
            print("🌐 Step 6/6: Website Scraping...", end="", flush=True)
            scraped_details = {"emails": ["N/A"], "phones": ["N/A"], "socials": ["N/A"], "page_text": "N/A"}
            if official_website and official_website != "N/A":
                scraped_details = deep_scrape_website(official_website)
                email_cnt = len([e for e in scraped_details.get("emails", []) if e != "N/A"])
                print(f" ✅ Done ({email_cnt} emails found)")
            else:
                print(" ⚠️ Skipped (No official website URL)")
                
            # Aggregate and format contact details for Excel exporter
            scraped_emails = clean_data_list(scraped_details.get("emails", []))
            scraped_phones = clean_data_list(scraped_details.get("phones", []))
            scraped_socials = clean_data_list(scraped_details.get("socials", []))
            scraped_text = scraped_details.get("page_text", "N/A")
            
            # Step 7: Targeted Placement search
            print("🔍 Step 7/7: Running Targeted Placement & Contact search...", end="", flush=True)
            placement_search = search_placement_details(selected_item_name)
            print(" ✅ Done")
            
            contact_aggregate = {
                "website": official_website,
                "address": maps_data.get("address", "N/A") if maps_data else "N/A",
                "phone_number": maps_data.get("phone_number", "N/A") if maps_data else "N/A",
                "scraped_emails": scraped_emails,
                "scraped_phones": scraped_phones,
                "scraped_socials": scraped_socials
            }
            
            # Prepare Combined String for LLM
            combined_data = []
            combined_data.append(f"RESEARCH TARGET: {selected_item_name}\n")
            
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
            
            if deep_search_results:
                combined_data.append("--- DEEP GOOGLE SEARCH RESULTS ---")
                for res in deep_search_results:
                    combined_data.append(f"[{res['index']}] Title: {res['title']}\nLink: {res['link']}\nSnippet: {res['snippet']}\n")
                combined_data.append("")
                
            raw_data_string = "\n".join(combined_data)
            
            # --- AI Summarization ---
            print("🤖 Generating AI Summary...", end="", flush=True)
            ai_report = generate_ai_summary(selected_item_name, raw_data_string)
            print(" ✅ Done!")
            
            print("\n" + "=" * 60)
            print("                       DEEP DIG REPORT                       ")
            print("=" * 60)
            print(ai_report)
            print("=" * 60 + "\n")
            
            # Export Loop
            while True:
                print("Export Options:")
                print("1. 📄 Save as PDF")
                print("2. 📊 Save as Excel")
                print("3. 📝 Save as Text file")
                print("4. 🔄 New Search")
                print("5. ❌ Exit")
                
                exp_choice = input("\n👉 Enter selection (1-5): ").strip()
                
                if exp_choice == '1':
                    export_to_pdf(selected_item_name, ai_report)
                elif exp_choice == '2':
                    export_to_excel(selected_item_name, ai_report, contact_aggregate, news_data, youtube_data, raw_data_string)
                elif exp_choice == '3':
                    export_to_text(selected_item_name, ai_report)
                elif exp_choice == '4':
                    print("\nStarting new search...")
                    break
                elif exp_choice == '5':
                    print("\nThank you for using DeepDig. Goodbye! 👋")
                    sys.exit(0)
                else:
                    print("⚠️ Invalid choice. Select between 1 and 5.")
                print("-" * 50)
                
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user. Exiting... 👋")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️ An unexpected error occurred: {e}")
            retry = input("Do you want to try again? (yes/no): ").strip().lower()
            if retry not in ['yes', 'y']:
                print("Exiting DeepDig. Goodbye! 👋")
                break

if __name__ == "__main__":
    main()
