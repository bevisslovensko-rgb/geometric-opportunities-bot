"""
Email digest sender for Geometric Magazine Opportunities Bot.
Sends a clean HTML email grouped by opportunity type and tier.
"""
import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_TO
from filter import tier_label


TYPE_LABELS = {
    "open_call":  "Open Calls",
    "residency":  "Rezidencie",
    "grant":      "Granty & Fellowships",
    "prize":      "Ceny & Súťaže",
    "commission": "Komisie",
}

TYPE_ORDER = ["open_call", "residency", "grant", "prize", "commission"]


def _days_left(deadline: date | None) -> str:
    if not deadline:
        return "Deadline neuvedený"
    delta = (deadline - date.today()).days
    return f"{deadline.strftime('%d %B %Y')} — {delta} dní"


def _opp_card(opp: dict, index: int) -> str:
    score    = opp.get("score", 0)
    keywords = ", ".join(opp.get("keywords", [])[:5])
    deadline = _days_left(opp.get("deadline"))
    tier     = tier_label(score)
    source   = opp.get("source", "")
    link     = opp.get("link", "#")
    title    = opp.get("title", "Bez názvu")
    desc     = opp.get("description", "")[:280]
    if desc:
        desc = desc + ("..." if len(opp.get("description","")) > 280 else "")

    tier_color = "#0a0a0a" if score >= 7 else "#555555" if score >= 4 else "#999999"

    return f"""
<tr>
  <td style="padding: 20px 0; border-bottom: 1px solid #e8e4dc;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td>
          <span style="font-size:11px; color:{tier_color}; font-weight:600;
                       letter-spacing:0.08em; text-transform:uppercase;">
            {tier} · Score {score}/10
          </span>
        </td>
        <td align="right">
          <span style="font-size:11px; color:#999; letter-spacing:0.04em;">
            {source}
          </span>
        </td>
      </tr>
      <tr>
        <td colspan="2" style="padding-top:6px;">
          <a href="{link}" style="font-size:17px; font-weight:600; color:#0a0a0a;
                                   text-decoration:none; line-height:1.3;">
            {title}
          </a>
        </td>
      </tr>
      {"<tr><td colspan='2' style='padding-top:6px;'><span style='font-size:13px; color:#555; line-height:1.6;'>" + desc + "</span></td></tr>" if desc else ""}
      <tr>
        <td colspan="2" style="padding-top:10px;">
          <span style="font-size:12px; color:#333;">
            📅 <strong>{deadline}</strong>
          </span>
        </td>
      </tr>
      {"<tr><td colspan='2' style='padding-top:4px;'><span style='font-size:11px; color:#aaa;'>🏷 " + keywords + "</span></td></tr>" if keywords else ""}
      <tr>
        <td colspan="2" style="padding-top:12px;">
          <a href="{link}" style="display:inline-block; padding:7px 16px;
                                   background:#0a0a0a; color:#f4f1eb;
                                   font-size:11px; font-weight:600;
                                   letter-spacing:0.08em; text-decoration:none;
                                   text-transform:uppercase;">
            Zobraziť príležitosť →
          </a>
        </td>
      </tr>
    </table>
  </td>
</tr>
"""


def build_html(opportunities: list[dict], run_date: date) -> str:
    # Group by type
    grouped: dict[str, list] = {t: [] for t in TYPE_ORDER}
    for opp in opportunities:
        t = opp.get("type", "open_call")
        if t in grouped:
            grouped[t].append(opp)
        else:
            grouped["open_call"].append(opp)

    total = len(opportunities)
    month = run_date.strftime("%B %Y")

    sections_html = ""
    for opp_type in TYPE_ORDER:
        items = grouped[opp_type]
        if not items:
            continue
        label = TYPE_LABELS[opp_type]
        cards  = "".join(_opp_card(o, i) for i, o in enumerate(items))
        sections_html += f"""
<tr>
  <td style="padding: 28px 0 8px 0;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="border-top: 2px solid #0a0a0a; padding-top: 14px;">
          <span style="font-size:13px; font-weight:700; letter-spacing:0.12em;
                       text-transform:uppercase; color:#0a0a0a;">
            {label} ({len(items)})
          </span>
        </td>
      </tr>
    </table>
  </td>
</tr>
{cards}
"""

    return f"""<!DOCTYPE html>
<html lang="sk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Geometric Magazine — Opportunities {month}</title>
</head>
<body style="margin:0; padding:0; background:#f4f1eb; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f1eb; padding: 32px 16px;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0"
               style="background:#ffffff; padding:40px 48px; max-width:620px;">

          <!-- Header -->
          <tr>
            <td style="border-bottom: 1px solid #e8e4dc; padding-bottom: 20px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <span style="font-size:11px; font-weight:700; letter-spacing:0.2em;
                                 text-transform:uppercase; color:#0a0a0a;">
                      GEOMETRIC MAGAZINE
                    </span>
                  </td>
                  <td align="right">
                    <span style="font-size:11px; color:#aaa; letter-spacing:0.06em;">
                      {month}
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td style="padding: 28px 0 8px 0;">
              <h1 style="margin:0; font-size:26px; font-weight:700; color:#0a0a0a;
                          letter-spacing:-0.01em; line-height:1.2;">
                Opportunities
              </h1>
              <p style="margin:8px 0 0; font-size:13px; color:#888;">
                {total} príležitostí pre geometrických, abstraktných a konceptuálnych umelcov.
                Zoradené podľa relevancie. Deadline min. 35 dní.
              </p>
            </td>
          </tr>

          <!-- Opportunities -->
          <table width="100%" cellpadding="0" cellspacing="0">
            {sections_html}
          </table>

          <!-- Footer -->
          <tr>
            <td style="padding-top: 36px; border-top: 1px solid #e8e4dc; margin-top: 20px;">
              <p style="margin:0; font-size:11px; color:#bbb; line-height:1.7;">
                Tento digest generuje Geometric Magazine Opportunities Bot každý pondelok.<br>
                Príležitosti sú kurátorsky filtrované pre geometrické, abstraktné
                a konceptuálne umenie.<br>
                <a href="https://geometricmagazine.com" style="color:#0a0a0a;">
                  geometricmagazine.com
                </a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_digest(opportunities: list[dict], run_date: date) -> None:
    if not GMAIL_USER or not GMAIL_APP_PASSWORD or not EMAIL_TO:
        print("[EMAIL] Missing credentials — skipping send. Set GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_TO.")
        return

    total = len(opportunities)
    month = run_date.strftime("%B %Y")
    subject = f"◻ Geometric Magazine — {total} Opportunities · {month}"

    html_body = build_html(opportunities, run_date)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Geometric Magazine Bot <{GMAIL_USER}>"
    msg["To"]      = EMAIL_TO
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, EMAIL_TO, msg.as_string())
        print(f"[EMAIL] Sent to {EMAIL_TO} — {total} opportunities")
