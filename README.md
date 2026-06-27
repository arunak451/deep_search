# DeepDig 🔍

DeepDig is a production-ready, modular command-line tool built in Python. It acts as an AI-powered Deep Research Search Engine, retrieving, compiling, scraping, and analyzing data about businesses, organizations, and entities from 6 distinct channels:
1. **Google Search (via SerpApi)**: Performs deep dive organic search analysis.
2. **Google Maps Place Details (via SerpApi)**: Pulls coordinates, rating, reviews, address, phone number, and hours.
3. **LinkedIn Company Data (via RapidAPI)**: Gathers employee size, founding year, headquarters, industry, and description.
4. **YouTube Data API v3**: Retrieves top 5 relevant videos with metadata (titles, channels, views, likes).
5. **News API**: Pulls top 5 relevant recent news articles matching the target entity.
6. **BeautifulSoup Scraper**: Deeply crawls the target website (homepage, `/about`, `/contact`, etc.) to extract emails, phone numbers, and social media profile links (Facebook, Instagram, Twitter, LinkedIn).

All gathered data is compiled and sent to **Groq's Llama 3.1 8B Instant** LLM to generate a professional, structured Markdown report. Finally, users can export results to **PDF, Excel (multi-sheet), or plain TXT formats**.

---

## Code Structure

```text
📁 DeepDig/
├── .env                 # API Keys storage (ignored in VCS)
├── requirements.txt     # Python package dependencies
├── config.py            # Loads and validates environment variables
├── search_engine.py     # SerpApi Google Search helper
├── maps_fetcher.py      # SerpApi Google Maps details helper
├── linkedin_fetcher.py  # RapidAPI LinkedIn Company Data connector
├── youtube_fetcher.py   # YouTube Data API v3 integration
├── news_fetcher.py      # News API integration
├── web_scraper.py       # BS4 scraper for emails, phones & social media
├── ai_summarizer.py     # Groq Llama 3.1 LLM reporter
├── exporter.py          # PDF, Excel, and Text export handlers
└── main.py              # CLI main entry point loop
```

---

## Installation & Setup

### 1. Clone or copy files
Ensure all Python files are located in your workspace directory.

### 2. Install dependencies
Install all the required python libraries using:
```bash
pip install -r requirements.txt
```

### 3. Setup configuration keys
Open or create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY="YOUR_GROQ_KEY"
SERP_API_KEY="YOUR_SERP_KEY"
RAPIDAPI_KEY="YOUR_RAPIDAPI_KEY"
RAPIDAPI_HOST="linkedin-data-api.p.rapidapi.com"
YOUTUBE_API_KEY="YOUR_YOUTUBE_KEY"
NEWS_API_KEY="YOUR_NEWS_KEY"
PORT=3000
```

---

## How to Run

Launch the application:
```bash
python main.py
```

### Flow Breakdown:
1. **Search**: Enter the keyword query in the CLI prompt (e.g., `PSG College of Technology`).
2. **Selection**: Select a number from the top 10 search results to start a deep-dive research.
3. **Research**: The application crawls and queries all 6 data channels sequentially with real-time status indicators.
4. **Summary**: The model compiles the raw data into an analytical research report shown directly in the terminal.
5. **Export/Loop**: Choose an option to save as PDF, Excel, or Text format, start a new research, or exit the program.
