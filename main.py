"""
Geometric Magazine Opportunities Bot — main entry point.
Fetches, filters, and emails relevant art opportunities every week.
"""
import datetime
from scrapers.rss import fetch_rss_sources
from scrapers.web import fetch_web_sources
from filter import score
from emailer import send_digest
from config import MIN_SCORE, MIN_DAYS_REMAINING


def run():
    today  = datetime.date.today()
    cutoff = today + datetime.timedelta(days=MIN_DAYS_REMAINING)

    print(f"[BOT] Running — {today} | Min score: {MIN_SCORE} | Min days: {MIN_DAYS_REMAINING}")

    # 1. Fetch from all sources
    raw = []
    raw.extend(fetch_rss_sources())
    raw.extend(fetch_web_sources())
    print(f"[BOT] Fetched {len(raw)} raw opportunities")

    # 2. Score and filter
    scored = []
    for opp in raw:
        text   = f"{opp.get('title', '')} {opp.get('description', '')}"
        points, matches = score(text)

        if points < MIN_SCORE:
            continue

        # Deadline filter — only include if deadline is far enough away
        deadline = opp.get("deadline")
        if deadline and deadline < cutoff:
            continue  # Too soon — skip

        opp["score"]    = points
        opp["keywords"] = matches
        scored.append(opp)

    # 3. Deduplicate by title
    seen, unique = set(), []
    for opp in scored:
        key = opp["title"].lower().strip()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(opp)

    print(f"[BOT] {len(unique)} relevant opportunities after filtering")

    if not unique:
        print("[BOT] Nothing to send this week.")
        return

    # 4. Sort: score DESC, then deadline ASC
    unique.sort(key=lambda x: (
        -x["score"],
        x.get("deadline") or datetime.date.max
    ))

    # 5. Save digest as markdown (committed to repo for history)
    _save_markdown(unique, today)

    # 6. Send email
    send_digest(unique, today)


def _save_markdown(opportunities: list[dict], run_date: datetime.date) -> None:
    """Save weekly digest as markdown file for easy review."""
    import os
    os.makedirs("digests", exist_ok=True)
    filename = f"digests/{run_date.isoformat()}.md"

    lines = [
        f"# Geometric Magazine — Opportunities {run_date.strftime('%B %Y')}",
        f"*{len(opportunities)} príležitostí | Vygenerované {run_date}*\n",
    ]

    current_type = None
    type_labels = {
        "open_call":  "Open Calls",
        "residency":  "Rezidencie",
        "grant":      "Granty & Fellowships",
        "prize":      "Ceny & Súťaže",
        "commission": "Komisie",
    }

    for opp in opportunities:
        opp_type = opp.get("type", "open_call")
        if opp_type != current_type:
            current_type = opp_type
            lines.append(f"\n## {type_labels.get(opp_type, opp_type)}\n")

        deadline = opp.get("deadline")
        dl_str   = deadline.strftime("%d %B %Y") if deadline else "Neuvedený"
        kw       = ", ".join(opp.get("keywords", [])[:5])

        lines += [
            f"### {opp['title']}",
            f"- **Zdroj:** {opp.get('source', '')}",
            f"- **Deadline:** {dl_str}",
            f"- **Score:** {opp.get('score', 0)}/10",
            f"- **Keywords:** {kw}",
            f"- **Link:** {opp.get('link', '')}",
            f"- **Popis:** {opp.get('description', '')[:300]}",
            "",
        ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[BOT] Saved digest → {filename}")


if __name__ == "__main__":
    run()
