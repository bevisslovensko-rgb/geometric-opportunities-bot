"""
Configuration for Geometric Magazine Opportunities Bot.
"""
import os

# Filter settings
MIN_SCORE          = 2   # Low because sources are pre-curated opportunity pages
MIN_DAYS_REMAINING = 14  # Only include if deadline >= 14 days away

# Email settings (from GitHub Secrets)
GMAIL_USER         = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
EMAIL_TO           = os.environ.get("EMAIL_TO", "")

# Article sources: monthly curated roundup articles
# URL template uses {month} (lowercase) and {year}
ARTICLE_SOURCES = [
    {
        "name":         "Hyperallergic",
        "url_template": "https://hyperallergic.com/opportunities-in-{month}-{year}/",
    },
]

# RSS sources (currently empty - news feeds were not useful)
RSS_SOURCES = []

# Web sources: dedicated opportunity listing pages
WEB_SOURCES = [
    {
        "name":          "Res Artis",
        "url":           "https://resartis.org/open-calls/",
        "base_url":      "https://resartis.org",
        "type":          "residency",
        "item_selector": ".views-row, article, .listing-item, .residency-item, li",
        "title_selector":"h2, h3, h4, .title, strong, b",
        "link_selector": "a",
        "desc_selector": "p, .description, .field-content",
    },
]
