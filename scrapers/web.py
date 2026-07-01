"""
Web scraper for Geometric Magazine Opportunities Bot.
Uses requests + BeautifulSoup for static/SSR pages.
"""
import re
import requests
from datetime import date
from dateutil import parser as dateutil_parser
from bs4 import BeautifulSoup
from config import WEB_SOURCES
from filter import detect_type


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; GeometricMagazineBot/1.0; "
        "+https://geometricmagazine.com)"
    )
}
TIMEOUT = 15


def _strip_html(text: str) -> str:
    return re.sub(r'<[^>]+>', ' ', text or '').strip()


def _extract_date(text: str) -> date | None:
    patterns = [
        r'deadline[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})',
        r'closes?[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})',
        r'by[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})',
        r'due[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})',
        r'until[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})',
        r'(\d{1,2}[./]\d{1,2}[./]\d{4})',
        r'(\d{4}-\d{2}-\d{2})',
        r'([A-Za-z]+ \d{1,2},?\s*\d{4})',
    ]
    today = date.today()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                dt = dateutil_parser.parse(match.group(1), dayfirst=False)
                if dt.date() > today:
                    return dt.date()
            except Exception:
                continue
    return None


def _absolute_url(href: str, base_url: str) -> str:
    if not href:
        return ""
    if href.startswith("http"):
        return href
    return base_url.rstrip("/") + "/" + href.lstrip("/")


def _scrape_source(source: dict) -> list[dict]:
    results = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=TIMEOUT, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Try each selector until we find items
        items = []
        for selector in source["item_selector"].split(", "):
            items = soup.select(selector.strip())
            if items:
                break

        for item in items[:30]:  # Max 30 items per source
            # Title
            title_el = None
            for sel in source["title_selector"].split(", "):
                title_el = item.select_one(sel.strip())
                if title_el:
                    break
            title = title_el.get_text(strip=True) if title_el else ""

            # Link
            link_el = item.select_one("a")
            href = link_el.get("href", "") if link_el else ""
            link = _absolute_url(href, source["base_url"])

            # Description
            desc = ""
            for sel in source["desc_selector"].split(", "):
                desc_el = item.select_one(sel.strip())
                if desc_el:
                    desc = desc_el.get_text(strip=True)
                    break

            if not title or len(title) < 5:
                continue

            full_text = f"{title} {desc}"
            deadline  = _extract_date(full_text)

            results.append({
                "title":       title,
                "link":        link,
                "description": desc[:600],
                "deadline":    deadline,
                "published":   None,
                "source":      source["name"],
                "type":        source.get("type") or detect_type(full_text),
            })

    except Exception as e:
        print(f"[WEB] Error scraping {source['name']}: {e}")

    return results


def fetch_web_sources() -> list[dict]:
    results = []
    for source in WEB_SOURCES:
        items = _scrape_source(source)
        print(f"[WEB] {source['name']}: {len(items)} items")
        results.extend(items)
    return results
