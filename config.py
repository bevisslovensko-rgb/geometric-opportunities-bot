"""
Configuration for Geometric Magazine Opportunities Bot.
Sensitive values (email credentials) are loaded from environment variables / GitHub Secrets.
"""
import os

# ─── Filter settings ──────────────────────────────────────────────────────────
MIN_SCORE = 1                # TEST: lowered to 1 (production: 4)
MIN_DAYS_REMAINING = 0       # TEST: no deadline filter (production: 35)

# ─── Email settings (from GitHub Secrets) ────────────────────────────────────
GMAIL_USER        = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
EMAIL_TO          = os.environ.get("EMAIL_TO", "")

# ─── Sources ──────────────────────────────────────────────────────────────────
RSS_SOURCES = [
    {
        "name": "e-flux",
        "url": "https://www.e-flux.com/announcements/feed/",
        "base_url": "https://www.e-flux.com",
    },
    {
        "name": "Rhizome",
        "url": "https://rhizome.org/editorial/feed/",
        "base_url": "https://rhizome.org",
    },
    {
        "name": "Art Rabbit",
        "url": "https://www.artrabbit.com/rss.xml",
        "base_url": "https://www.artrabbit.com",
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
    {
        "name": "CuratorSpace",
        "url": "https://curatorspace.com/opportunities",
        "base_url": "https://curatorspace.com",
        "type": "open_call",
        "item_selector": ".opportunity, article, .listing",
        "title_selector": "h2, h3, .opportunity-title",
        "link_selector": "a",
        "desc_selector": "p, .description",
    },
]
