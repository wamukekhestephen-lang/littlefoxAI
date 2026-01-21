import time
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

# ---------------------------------------
# HTTP settings
# ---------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 6
MAX_PAGE_CHARS = 3000
SEARCH_DELAY = 0.2  # avoid DDG rate limiting

# ---------------------------------------
# Block low-signal / junk domains
# ---------------------------------------
BLOCKED_DOMAINS = {
    "reddit.com",
    "pinterest.com",
    "tenor.com",
    "giphy.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "tiktok.com",
    "youtube.com",
    "instagram.com"
}

# ---------------------------------------
# Web search
# ---------------------------------------
def search_web(query: str, max_results: int = 3):
    """
    Perform a DuckDuckGo web search and return
    a filtered list of results with title, url, and snippet.
    Reduces Wikipedia and other low-quality spam.
    """
    blacklist = ("wikipedia.org", "reddit.com", "quora.com")
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results * 2):
            url = r.get("href", "")
            if not url:
                continue
            
            # Block blacklist domains
            if any(b in url for b in blacklist):
                continue
            
            # Filter junk domains
            if any(domain in url for domain in BLOCKED_DOMAINS):
                continue

            results.append({
                "title": r.get("title", "Source"),
                "url": url
            })

            if len(results) >= max_results:
                break

            time.sleep(0.15)

    return results


# ---------------------------------------
# Page fetching + extraction
# ---------------------------------------
def fetch_page(url: str) -> str:
    """
    Fetch a web page and extract readable text.
    Returns empty string on failure.
    """
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-content elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)

        # Safety cap for tokens
        return text[:MAX_PAGE_CHARS]

    except Exception:
        return ""
