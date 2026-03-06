"""
IDEAM Production Scraper for RAG
--------------------------------
• Normalizes URLs
• Removes duplicate paragraphs
• Removes navigation/footer
• Saves clean structured JSON
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import time

# ===== PATH CONFIG =====
CURRENT_FILE = os.path.abspath(__file__)
SCRAPERS_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_ROOT = os.path.dirname(SCRAPERS_DIR)

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "ideam_raw.json")

START_URL = "https://ideam.ie"
MAX_PAGES = 50

visited = set()
structured_data = []


def clean_text(text):
    return " ".join(text.split()).strip()


def normalize_url(url):
    return url.rstrip("/")


def extract_structured_content(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["nav", "footer", "header", "script", "style", "form"]):
            tag.decompose()

        page_title = soup.title.string.strip() if soup.title else ""

        page_content = []
        current_heading = ""
        seen_text = set()

        for element in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            text = clean_text(element.get_text())

            if len(text) < 40:
                continue

            if element.name in ["h1", "h2", "h3"]:
                current_heading = text
            else:
                if text not in seen_text:
                    page_content.append({
                        "heading": current_heading,
                        "text": text
                    })
                    seen_text.add(text)

        return {
            "url": normalize_url(url),
            "title": page_title,
            "content": page_content
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def crawl_site(start_url):
    domain = urlparse(start_url).netloc
    to_visit = [normalize_url(start_url)]

    while to_visit and len(visited) < MAX_PAGES:
        url = normalize_url(to_visit.pop(0))

        if url in visited:
            continue

        visited.add(url)
        print("Crawling:", url)

        page_data = extract_structured_content(url)
        if page_data:
            structured_data.append(page_data)

        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                link = normalize_url(urljoin(url, a["href"]))
                if domain in link and link not in visited and "#" not in link:
                    to_visit.append(link)
        except:
            pass

        time.sleep(0.3)

    print("\nTotal pages scraped:", len(structured_data))


def save_raw_data():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)

    print("Raw data saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    crawl_site(START_URL)
    save_raw_data()