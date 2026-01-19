import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def search_web(query, max_results=2):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "url": r.get("href")
            })
            time.sleep(0.2)  # avoid rate limiting
    return results


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)
        return text[:3000]  # limit tokens
    except Exception:
        return ""
