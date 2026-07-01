"""
Configuration for Geometric Magazine Opportunities Bot.
Sensitive values (email credentials) are loaded from environment variables / GitHub Secrets.
"""
import os

# ─── Filter settings ──────────────────────────────────────────────────────────
MIN_SCORE = 4                # Minimum relevance score (1-10)
MIN_DAYS_REMAINING = 35      # Only include if deadline is at least this many days away

# ─── Email settings (from GitHub Secrets) ────────────────────────────────────
GMAIL_USER        = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
EMAIL_TO          = os.environ.get("EMAIL_TO", "")

# ─── Sources ──────────────────────────────────────────────────────────────────
RSS_SOURCES = [
    {
        "name": "Artforum",
        "url": "https://www.artforum.com/feed/",
        "base_url": "https://www.artforum.com",
    },
    {
        "name": "Creative Capital",
        "url": "https://creative-capital.org/feed/",
        "base_url": "https://creative-capital.org",
    },
    {
        "name": "NYFA",
        "url": "https://www.nyfa.org/feed/",
        "base_url": "https://www.nyfa.org",
    },
    {
        "name": "Hyperallergic",
        "url": "https://hyperallergic.com/rss/",
        "base_url": "https://hyperallergic.com",
    },
]

WEB_SOURCES = [
    {
        "name": "Res Artis",
        "url": "https://www.resartis.org/residencies/",
        "base_url": "https://www.resartis.org",
        "type": "residency",
        "item_selector": "article, .residency-item, .listing-item",
        "title_selector": "h2, h3, .title",
        "link_selector": "a",
        "desc_selector": "p, .description, .excerpt",
    },
]
