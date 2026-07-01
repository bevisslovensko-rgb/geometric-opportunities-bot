"""
Keyword scoring filter for Geometric Magazine Opportunities Bot.
Returns relevance score (0-10) and matched keywords for each opportunity.
"""

# ─── TIER 1 — Direct geometric match (3 pts each) ────────────────────────────
TIER_1 = [
    "geometric", "geometry", "geometrical",
    "op art", "optical art", "optical illusion",
    "hard-edge", "hard edge", "hard edged",
    "minimalism", "minimalist", "minimal art",
    "constructivism", "constructivist", "constructive art",
    "concrete art", "konkrete kunst",
    "systemic art", "systematic art",
    "kinetic", "kinetic art", "kinetic sculpture",
    "geometric abstraction", "abstract geometric",
    "bauhaus", "de stijl", "neoplasticism",
    "color field", "colour field",
    "mathematical art", "generative art", "algorithmic art",
    "parametric", "computational art",
    "pattern art", "tessellation",
    "isometric", "grid-based",
]

# ─── TIER 2 — Compatible abstraction (2 pts each) ────────────────────────────
TIER_2 = [
    "abstract", "abstraction", "abstract art",
    "non-figurative", "nonfigurative",
    "installation", "installation art",
    "digital art", "new media", "media art",
    "public art", "public mural", "mural",
    "wall painting", "large-scale", "site-specific",
    "urban art", "street art",
    "abstract painting", "abstract sculpture",
    "experimental", "conceptual",
    "spatial", "three-dimensional", "dimensional",
    "structure", "form and space",
    "light art", "light installation",
    "mosaic", "ceramic art", "enamel",
    "printmaking abstract", "relief print",
]

# ─── TIER 3 — Broad but valid (1 pt each) ────────────────────────────────────
TIER_3 = [
    "painting", "sculpture", "drawing",
    "works on paper", "paper works",
    "printmaking", "print",
    "textile", "fiber art", "tapestry", "weaving",
    "ceramics", "pottery",
    "mixed media", "multimedia",
    "residency", "artist residency", "art residency",
    "grant", "art grant", "fellowship",
    "award", "prize", "art prize",
    "commission", "public commission",
    "open call", "open submission",
    "contemporary art", "visual art",
    "emerging artist", "established artist",
]

# ─── EXCLUDE — Automatic disqualification ────────────────────────────────────
EXCLUDE = [
    "figurative", "figure painting", "figure drawing",
    "portrait", "portraiture", "self-portrait",
    "landscape painting", "plein air",
    "photography only", "photo only", "photographic",
    "illustration", "editorial illustration", "children illustration",
    "narrative art", "storytelling", "comic", "sequential art",
    "social commentary", "political art", "activist art",
    "graffiti writing", "graffiti lettering",
    "realism", "hyperrealism", "photorealism",
    "representational", "traditional figurative",
]

# ─── OPPORTUNITY TYPE DETECTION ───────────────────────────────────────────────
TYPE_KEYWORDS = {
    "residency":  ["residency", "residence", "artist-in-residence", "air program", "studio residency"],
    "grant":      ["grant", "fellowship", "funding", "bursary", "stipend", "award money"],
    "prize":      ["prize", "award", "competition", "contest", "winner", "jury"],
    "commission": ["commission", "commissioned", "public commission", "paid commission"],
}


def detect_type(text: str) -> str:
    t = text.lower()
    for opp_type, keywords in TYPE_KEYWORDS.items():
        if any(kw in t for kw in keywords):
            return opp_type
    return "open_call"


def score(text: str) -> tuple:
    """
    Returns (score: int, matched_keywords: list[str])
    Score 0 = excluded or irrelevant
    Score 1-3 = Tier 3 only
    Score 4-6 = Tier 2 match
    Score 7-10 = Tier 1 match
    """
    t = text.lower()

    # Hard exclusions
    for kw in EXCLUDE:
        if kw in t:
            return 0, []

    matched, points = [], 0

    for kw in TIER_1:
        if kw in t:
            points += 3
            matched.append(kw)

    for kw in TIER_2:
        if kw in t:
            points += 2
            matched.append(kw)

    for kw in TIER_3:
        if kw in t:
            points += 1
            matched.append(kw)

    return min(points, 10), list(set(matched))


def tier_label(score: int) -> str:
    if score >= 7:
        return "Tier 1 — Geometrické"
    elif score >= 4:
        return "Tier 2 — Abstraktné / Kompatibilné"
    elif score >= 1:
        return "Tier 3 — Na tvoj úsudok"
    return "Irelevantné"
