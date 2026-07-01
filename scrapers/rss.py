"""
RSS feed scraper for Geometric Magazine Opportunities Bot.
"""
import feedparser
import re
from datetime import date
from dateutil import parser as dateutil_parser
from config import RSS_SOURCES
from filter import detect_type


HEADERS = {
    "User-Agent": "GeometricMagazine-OpBot/1.0 (geometricmagazine.com)"
}


def _extract_date(text: str) -> date | None:
    """Try to extract a deadline date from free text."""
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


def _strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', ' ', text or '').strip()


def fetch_rss_sources() -> list[dict]:
    """Fetch and parse all RSS sources."""
    results = []

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"], request_headers=HEADERS)
            print(f"[RSS] {source['name']}: status={getattr(feed, 'status', 'N/A')} entries={len(feed.entries)} bozo={feed.bozo}")
            if feed.bozo and feed.bozo_exception:
                print(f"[RSS] {source['name']} bozo: {feed.bozo_exception}")
            for entry in feed.entries:
                title = _strip_html(entry.get("title", "")).strip()
                link  = entry.get("link", "")
                desc  = _strip_html(
                    entry.get("summary", "") or entry.get("description", "")
                ).strip()

                if not title or not link:
                    continue

                # Try to extract deadline from description
                full_text = f"{title} {desc}"
                deadline  = _extract_date(full_text)

                # Try published date as fallback info (not deadline)
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        from datetime import datetime
                        published = datetime(*entry.published_parsed[:6]).date()
                    except Exception:
                        pass

                results.append({
                    "title":      title,
                    "link":       link,
                    "description": desc[:600],
                    "deadline":   deadline,
                    "published":  published,
                    "source":     source["name"],
                    "type":       detect_type(full_text),
                })

        except Exception as e:
            print(f"[RSS] Error fetching {source['name']}: {e}")

    return results
