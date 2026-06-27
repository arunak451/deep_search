import re
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
import urllib3

class TLSAdapter(HTTPAdapter):
    """
    Custom HTTPAdapter to lower SSL/TLS security level to SECLEVEL=1.
    Allows connecting to sites with weak DH key sizes (e.g. DH_KEY_TOO_SMALL).
    """
    def init_poolmanager(self, *args, **kwargs):
        ctx = urllib3.util.ssl_.create_urllib3_context(
            ciphers='DEFAULT@SECLEVEL=1'
        )
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

# Regex Patterns requested by user
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
# We combine the user's two phone regex requests to cover both phone variations
PHONE_PATTERN = re.compile(r'(?:\+91[\-\s]?)?[0]?[6789]\d{9}|[\+]?[91]?[0-9]{10,13}')
SOCIAL_PATTERN = re.compile(r'https?://(?:www\.)?(?:facebook|instagram|twitter|linkedin)\.com/[^\s"<>]+')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_contact_info(text):
    """
    Extracts emails, phone numbers, and social links from text using regex patterns.
    """
    emails = set(re.findall(EMAIL_PATTERN, text))
    phones = set(re.findall(PHONE_PATTERN, text))
    socials = set(re.findall(SOCIAL_PATTERN, text))
    
    # Filter out obvious invalid emails
    valid_emails = set()
    for email in emails:
        # Check if email ends with common static resource extensions
        if not any(email.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.css', '.js']):
            valid_emails.add(email)
            
    # Clean phone numbers (remove spaces or dashes for standardization, but keep format readable)
    valid_phones = set()
    for phone in phones:
        clean = phone.strip()
        # Ensure it has sufficient digits to be a phone number
        digit_count = sum(1 for c in clean if c.isdigit())
        if 8 <= digit_count <= 15:
            valid_phones.add(clean)

    return valid_emails, valid_phones, socials

def get_page_content(url):
    """
    Fetches the HTML text from a URL using requests.
    Implements anti-blocking headers, timeout, and TLSAdapter to bypass weak DH key errors.
    """
    try:
        # Anti-blocking delay
        time.sleep(random.uniform(1.5, 3.5))
        
        session = requests.Session()
        session.headers.update(HEADERS)
        # Mount TLS adapter for HTTPS requests
        session.mount("https://", TLSAdapter())
        
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text
    except Exception as e:
        print(f"⚠️ Failed to load webpage {url}: {e}")
    return None

def extract_page_text(html_content):
    """
    Extracts readable, cleaned text from HTML content.
    Removes script, style, header, footer, nav.
    """
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove non-readable elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        
        # Clean lines: remove empty, and only keep lines that look like actual content (length > 15)
        cleaned_lines = []
        for line in lines:
            if len(line) > 15:
                # Compress multiple spaces
                line = re.sub(r'\s+', ' ', line)
                cleaned_lines.append(line)
                
        # Limit to first 120 lines to keep context sizes reasonable
        return "\n".join(cleaned_lines[:120])
    except Exception as e:
        print(f"⚠️ Failed to extract text from HTML: {e}")
        return ""

def deep_scrape_website(start_url):
    """
    Scrapes the homepage, and finds About / Contact / Placement / Career pages to scrape them.
    Aggregates emails, phones, social links, and readable text context.
    """
    if not start_url or start_url == "N/A":
        return {
            "emails": ["N/A"],
            "phones": ["N/A"],
            "socials": ["N/A"],
            "page_text": "N/A"
        }

    # Ensure URL has a scheme
    if not start_url.startswith(("http://", "https://")):
        start_url = "https://" + start_url

    print(f"🌐 Scraping base website: {start_url}...")
    
    all_emails = set()
    all_phones = set()
    all_socials = set()
    scraped_text_blocks = []
    
    homepage_html = get_page_content(start_url)
    if not homepage_html:
        return {
            "emails": ["N/A"],
            "phones": ["N/A"],
            "socials": ["N/A"],
            "page_text": "N/A"
        }
        
    # Scrape homepage contacts
    emails, phones, socials = extract_contact_info(homepage_html)
    all_emails.update(emails)
    all_phones.update(phones)
    all_socials.update(socials)
    
    # Scrape homepage text
    hp_text = extract_page_text(homepage_html)
    if hp_text:
        scraped_text_blocks.append(f"### HOMEPAGE TEXT ###\n{hp_text}")
    
    # Parse HTML to find links to About / Contact / Placements / Career pages
    soup = BeautifulSoup(homepage_html, 'html.parser')
    
    parsed_start = urlparse(start_url)
    start_domain = parsed_start.netloc.lower()
    if start_domain.startswith("www."):
        start_domain = start_domain[4:]
    
    secondary_urls = set()
    
    # Target keywords for secondary subpages
    target_keywords = ['about', 'contact', 'placement', 'career', 'job', 'recruit', 'admission', 'course', 'faculty', 'staff', 'reach']
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href'].strip()
        text = a_tag.get_text().lower()
        
        # Check if the href contains target keywords or tag text matches
        is_match = any(word in text or word in href.lower() for word in target_keywords)
        
        if is_match:
            absolute_url = urljoin(start_url, href)
            link_domain = urlparse(absolute_url).netloc.lower()
            if link_domain.startswith("www."):
                link_domain = link_domain[4:]
                
            # Allow matching subdomains or exact base domain
            if link_domain == start_domain or link_domain.endswith("." + start_domain):
                secondary_urls.add(absolute_url)
                
    # Limit secondary pages to max 5 to prevent hanging / too much data
    secondary_urls = list(secondary_urls)[:5]
    
    for sec_url in secondary_urls:
        print(f"🔗 Scraping subpage: {sec_url}...")
        sec_html = get_page_content(sec_url)
        if sec_html:
            # Extract contact info from subpage
            emails, phones, socials = extract_contact_info(sec_html)
            all_emails.update(emails)
            all_phones.update(phones)
            all_socials.update(socials)
            
            # Extract readable page text from subpage
            sub_text = extract_page_text(sec_html)
            if sub_text:
                page_path = urlparse(sec_url).path
                scraped_text_blocks.append(f"### SUBPAGE TEXT ({page_path}) ###\n{sub_text}")
                
    # Format results
    res_emails = list(all_emails)
    res_phones = list(all_phones)
    res_socials = list(all_socials)
    
    combined_text = "\n\n".join(scraped_text_blocks)
    # Cap total character limit of scraped text to ~12KB
    combined_text = combined_text[:12000]
    
    return {
        "emails": res_emails if res_emails else ["N/A"],
        "phones": res_phones if res_phones else ["N/A"],
        "socials": res_socials if res_socials else ["N/A"],
        "page_text": combined_text if combined_text.strip() else "N/A"
    }
