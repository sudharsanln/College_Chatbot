import os
import time
import requests
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient

# Create output folder
os.makedirs("college-data", exist_ok=True)
print("Saving to folder:", os.path.abspath("college-data"))

# Initialize ScrapingBee
SCRAPINGBEE_API_KEY = 'NTQ49KIS6BU0SHU61YLT0GEHH6DNY7M7M6QM90388GH403LQJWRJR423ZAW1MMFNXVNGNU2USE2BVAY9'  
client = ScrapingBeeClient(api_key=SCRAPINGBEE_API_KEY)

# Pages to scrape
pages = {
    "about": "https://www.snuchennai.edu.in/about-us/",
    "academics": "https://www.snuchennai.edu.in/academics/",
    "ug_admissions": "https://www.snuchennai.edu.in/ug-admissions/",
    "pg_admissions": "https://www.snuchennai.edu.in/pg-admissions/",
    "law_admissions": "https://law.snuchennai.edu.in/admissions/",
    "phd_admissions": "https://www.snuchennai.edu.in/phd-admissions/",
    "placements": "https://www.snuchennai.edu.in/placements/",
    "careers": "https://www.snuchennai.edu.in/careers/",
    "faculty": "https://www.snuchennai.edu.in/faculty/",
    "campus_life": "https://www.snuchennai.edu.in/campus-life/",
    "scholarships": "https://www.snuchennai.edu.in/scholarship/",
    "contact": "https://www.snuchennai.edu.in/contact-us/",
    "practitioner_semester_law": "https://law.snuchennai.edu.in/practitioner-semester/",
    "law_faculty": "https://law.snuchennai.edu.in/faculty/",
    "distinguished_visiting_faculty": "https://www.snuchennai.edu.in/faculty/cse-dg-visiting-faculty/"
}

programs = [
    ("btech_ai_ds", "https://www.snuchennai.edu.in/b-tech-ai-data-science/"),
    ("btech_iot", "https://www.snuchennai.edu.in/b-tech-computer-science-and-engineering-with-specialisation-in-iot/"),
    ("btech_cs", "https://www.snuchennai.edu.in/b-tech-computer-science-engineering-cyber-security/"),
    ("bcom", "https://www.snuchennai.edu.in/b-com/"),
    ("bcom_pa", "https://www.snuchennai.edu.in/b-com-professional-accounting/"),
    ("bsc_eco", "https://www.snuchennai.edu.in/b-sc-economics/"),
    ("ba_llb", "https://law.snuchennai.edu.in/academics/"),
]

# Helper: common menu words to ignore
COMMON_HEADERS = [
    "home", "about us", "admissions", "apply now", "campus life", "contact",
    "placements", "departments", "careers", "faculty", "programs", "student life", "downloads"
]

def is_common_header(text):
    """Detect and remove boilerplate headers/links."""
    t = text.lower().strip()
    return (
        t in COMMON_HEADERS
        or len(t) <= 2
        or t.startswith("©")
        or "snu chennai" in t
    )

def fetch_html(url):
    """Fetch HTML using ScrapingBee or fallback to requests."""
    try:
        print(f"Fetching via ScrapingBee: {url}")
        response = client.get(url, params={"render_js": "true"})
        if response.status_code == 200:
            return response.content.decode("utf-8")
        else:
            print(f"ScrapingBee failed ({response.status_code}), falling back to requests.")
    except Exception as e:
        print(f"ScrapingBee error: {e}")
    
    try:
        print(f"Fetching via requests: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
            "Referer": "https://www.google.com"
        }
        res = requests.get(url, timeout=20, headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            print(f"Requests failed ({res.status_code})")
    except Exception as e:
        print(f"Requests error: {e}")
    
    return ""

def extract_clean_text(html):
    """Extract and clean visible text from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "lxml")

    # Remove irrelevant tags immediately
    for tag in soup(["script", "style", "nav", "footer", "form", "header", "aside"]):
        tag.decompose()

    # Define blacklist keywords
    blacklist_keywords = ["menu", "navbar", "footer", "breadcrumb", "sidebar", "social", "links", "header"]

    # Collect tags to remove (don't decompose while iterating)
    tags_to_remove = []
    for tag in soup.find_all(True):
        tag_classes = tag.get("class") or []
        tag_id = tag.get("id") or ""

        # Check if any blacklist keyword is in the class names or id
        if any(any(k in cls.lower() for k in blacklist_keywords) for cls in tag_classes):
            tags_to_remove.append(tag)
        elif any(k in tag_id.lower() for k in blacklist_keywords):
            tags_to_remove.append(tag)

    # Remove the collected tags
    for tag in tags_to_remove:
        tag.decompose()

    # Extract and clean text
    content = soup.get_text(separator="\n")
    lines = [line.strip() for line in content.splitlines()]
    lines = [line for line in lines if line and not is_common_header(line)]

    return "\n".join(lines)

def scrape_and_save(pages_dict, prefix=""):
    """Main scraper: extract and save clean text for each URL."""
    for name, url in pages_dict.items():
        print(f"Scraping {name}...")
        html = fetch_html(url)
        if html:
            text = extract_clean_text(html)
            file_path = f"college-data/{prefix}{name}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved to {file_path}")
        else:
            print(f"Failed to scrape {url}")
            
# Run scraper
scrape_and_save(pages)
scrape_and_save(dict(programs), prefix="program_")