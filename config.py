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
        "name": "TransArtists",
        "url": "https://www.transartists.org/en/air",
        "base_url": "https://www.transartists.org",
        "type": "residency",
        "item_selector": ".views-row, article, .air-item",
        "title_selector": "h3, h2, .title",
        "link_selector": "a",
        "desc_selector": "p, .field-content",
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
    {
        "name": "ArtDeadline",
        "url": "https://artdeadline.com/",
        "base_url": "https://artdeadline.com",
        "type": "open_call",
        "item_selector": ".post, article, tr",
        "title_selector": "h2, h3, td a, .entry-title",
        "link_selector": "a",
        "desc_selector": "p, .entry-content, td",
    },
    {
        "name": "ArtConnect",
        "url": "https://www.artconnect.com/opportunities",
        "base_url": "https://www.artconnect.com",
        "type": "open_call",
        "item_selector": ".opportunity-card, article, .item",
        "title_selector": "h2, h3, .card-title",
        "link_selector": "a",
        "desc_selector": "p, .card-text",
    },
    {
        "name": "Arebyte",
        "url": "https://www.arebyte.com/opportunities",
        "base_url": "https://www.arebyte.com",
        "type": "open_call",
        "item_selector": "article, .opportunity, .post",
        "title_selector": "h1, h2, h3",
        "link_selector": "a",
        "desc_selector": "p",
    },
]
