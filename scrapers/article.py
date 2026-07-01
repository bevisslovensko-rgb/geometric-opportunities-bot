"""
Article scraper for Geometric Magazine Opportunities Bot.
Handles formatted monthly opportunity roundup articles (e.g. Hyperallergic).
"""
import re
import requests
from datetime import date
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from config import ARTICLE_SOURCES
from filter import detect_type

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; GeometricMagazineBot/1.0; "
        "+https://geometricmagazine.com)"
    )
}
TIMEOUT = 15


def _build_url(template: str, d: date) -> str:
    return template.format(month=d.strftime("%B").lower(), year=d.year)


def _extract_deadline(text: str):
    patterns = [
        r"[Dd]eadline[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})",
        r"[Dd]eadline[:\s]+(\d{1,2}/\d{1,2}/\d{4})",
        r"[Dd]ue[:\s]+([A-Za-z]+ \d{1,2},?\s*\d{4})",
        r"([A-Za-z]+ \d{1,2},?\s*\d{4})",
    ]
    today = date.today()
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                dt = dateutil_parser.parse(m.group(1), dayfirst=False)
                if dt.date() > today:
                    return dt.date()
            except Exception:
                continue
    return None


def _parse_article(html: str, source_name: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    results = []
    seen_titles = set()

    for strong in soup.find_all("strong"):
        # Skip headings and navigation
        if strong.find_parent(["h1", "h2", "h3", "h4", "nav", "header", "footer"]):
            continue

        title = strong.get_text(strip=True)
        if not title or len(title) < 8 or title.lower() in seen_titles:
            continue
        if len(title.split()) < 2:
            continue

        parent_p = strong.find_parent("p")
        if not parent_p:
            continue

        # Skip if strong is not near start of paragraph (cross-reference)
        prev_text = ""
        for sib in strong.previous_siblings:
            prev_text = (sib.get_text() if hasattr(sib, "get_text") else str(sib)) + prev_text
        if len(prev_text.strip()) > 20:
            continue

        seen_titles.add(title.lower())

        # Description: rest of paragraph after the title
        full_text = parent_p.get_text(" ", strip=True)
        desc = full_text.replace(title, "", 1).strip(" -\n\t")

        # Next sibling paragraph: usually "Deadline: DATE | link"
        next_p = parent_p.find_next_sibling("p")
        deadline_line = next_p.get_text(" ", strip=True) if next_p else ""

        # Skip if next paragraph starts another opportunity
        if next_p and next_p.find("strong"):
            deadline_line = ""
            next_p = None

        deadline = _extract_deadline(deadline_line) or _extract_deadline(desc)

        link = ""
        if next_p:
            a = next_p.find("a", href=True)
            if a and a["href"].startswith("http"):
                link = a["href"]
        if not link:
            a = parent_p.find("a", href=True)
            if a and a["href"].startswith("http"):
                link = a["href"]

        combined = "{} {} {}".format(title, desc, deadline_line)

        results.append({
            "title":       title,
            "link":        link,
            "description": "{} {}".format(desc, deadline_line).strip()[:600],
            "deadline":    deadline,
            "published":   None,
            "source":      source_name,
            "type":        detect_type(combined),
        })

    return results


def fetch_article_sources() -> list:
    today = date.today()
    results = []

    for source in ARTICLE_SOURCES:
        candidates = [
            _build_url(source["url_template"], today),
            _build_url(source["url_template"], today - relativedelta(months=1)),
        ]

        fetched = False
        for url in candidates:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                if resp.status_code == 404:
                    continue
                resp.raise_for_status()
                items = _parse_article(resp.text, source["name"])
                print("[ARTICLE] {}: {} items from {}".format(source["name"], len(items), url))
                results.extend(items)
                fetched = True
                break
            except Exception as e:
                print("[ARTICLE] {} error ({}): {}".format(source["name"], url, e))

        if not fetched:
            print("[ARTICLE] {}: no article found for {}".format(source["name"], today))

    return results
