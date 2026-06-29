"""Uses Claude to analyze all platform data and generate an HTML+PDF report."""

import json
import os
from datetime import datetime, timezone

import anthropic
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)


ACCENT = colors.HexColor("#2D4A8A")
LIGHT_BLUE = colors.HexColor("#EEF2FB")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#C62828")
ORANGE = colors.HexColor("#E65100")


def _trend_arrow(current, previous) -> str:
    if previous is None or previous == 0:
        return ""
    pct = ((current - previous) / previous) * 100
    if pct >= 5:
        return f"▲ +{pct:.1f}%"
    elif pct <= -5:
        return f"▼ {pct:.1f}%"
    return f"→ {pct:+.1f}%"


def _fmt(val) -> str:
    if val is None:
        return "—"
    if isinstance(val, float):
        if val < 1:
            return f"{val*100:.1f}%"
        return f"{val:,.1f}"
    return f"{int(val):,}"


def _build_claude_prompt(all_data: dict, previous_data: dict | None, config: dict) -> str:
    data_json = json.dumps(all_data, indent=2, default=str)
    prev_json = json.dumps(previous_data, indent=2, default=str) if previous_data else "No previous period data available."
    lookback = config["report"]["lookback_days"]

    return f"""You are a senior digital marketing analyst reviewing Ruth Klein's analytics across all platforms for the past {lookback} days.

CURRENT PERIOD DATA:
{data_json}

PREVIOUS PERIOD DATA (for comparison):
{prev_json}

Write a professional biweekly analytics report with these exact sections. Be specific, use actual numbers from the data, and be honest about what's working and what isn't.

## EXECUTIVE SUMMARY
3-5 bullet points. The most important things Ruth needs to know RIGHT NOW. Lead with wins, then concerns.

## TOP PERFORMERS THIS PERIOD
Which platforms and content types drove the most value? Name specific numbers. Why did they work?

## PLATFORMS TO WATCH
1-3 platforms showing concerning trends or missed opportunity. Be direct. What's declining and what could fix it?

## PLATFORM-BY-PLATFORM BREAKDOWN
For each platform with data, write 2-4 sentences: what happened, vs. last period, and one specific action to take.

## CONTENT & ENGAGEMENT INSIGHTS
Cross-platform patterns. What type of content is resonating? What isn't? Any day/time patterns worth noting?

## RECOMMENDATIONS FOR NEXT 2 WEEKS
5-7 specific, actionable recommendations ranked by impact. Not generic advice — tie each one to the data.

## THINGS TO KEEP AN EYE ON
Any anomalies, unexpected spikes or drops, or metrics that need investigation.

Be direct, data-driven, and write like you're briefing a CEO. No fluff."""


def analyze_with_claude(all_data: dict, previous_data: dict | None, config: dict) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = _build_claude_prompt(all_data, previous_data, config)

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _parse_sections(analysis: str) -> dict[str, str]:
    """Split Claude's markdown output into named sections."""
    sections = {}
    current_key = None
    current_lines = []

    for line in analysis.split("\n"):
        if line.startswith("## "):
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


def _platform_summary_table(all_data: dict) -> list:
    """Build a one-page summary table of all platforms."""
    rows = [["Platform", "Key Metric", "Value", "Secondary Metric", "Value"]]

    mappings = [
        ("instagram", "Instagram", "followers", "Followers", "impressions", "Impressions"),
        ("facebook", "Facebook", "page_fans", "Page Fans", "post_engagements", "Engagements"),
        ("youtube", "YouTube", "views", "Views", "subscribers", "Subscribers"),
        ("tiktok_organic", "TikTok", "video_views", "Video Views", "followers", "Followers"),
        ("pinterest", "Pinterest", "impressions", "Impressions", "outbound_clicks", "Outbound Clicks"),
        ("twitter", "Twitter / X", "impressions", "Impressions", "followers", "Followers"),
        ("gohighlevel", "HighLevel Email", "emails_sent", "Emails Sent", "open_rate", "Open Rate"),
        ("medium", "Medium", "views", "Views", "reads", "Reads"),
        ("substack", "Substack", "emails_sent", "Emails Sent", "open_rate", "Open Rate"),
    ]

    for source, label, k1, l1, k2, l2 in mappings:
        d = all_data.get(source, {}).get("data") or {}
        v1 = _fmt(d.get(k1))
        v2 = _fmt(d.get(k2))
        rows.append([label, l1, v1, l2, v2])

    # GA4 website rows
    ga4 = all_data.get("googleanalytics4", {})
    for group in ["blogs", "quiz", "lead_magnets", "other"]:
        d = ga4.get(group, {}).get("data") or {}
        label = f"Website ({group.replace('_', ' ').title()})"
        rows.append([label, "Sessions", _fmt(d.get("sessions")), "Users", _fmt(d.get("users"))])

    return rows


def generate_pdf(analysis: str, all_data: dict, config: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], textColor=ACCENT, fontSize=22, spaceAfter=4)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], textColor=colors.grey, fontSize=11, spaceAfter=16)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], textColor=ACCENT, fontSize=14, spaceBefore=18, spaceAfter=6)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=15, spaceAfter=6)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=10, leading=15, leftIndent=16, spaceAfter=4)

    run_date = datetime.now(tz=timezone.utc).strftime("%B %d, %Y")
    story = []

    # Header
    story.append(Paragraph(config["report"]["title"], title_style))
    story.append(Paragraph(f"Biweekly Report · {run_date} · Last {config['report']['lookback_days']} days", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT))
    story.append(Spacer(1, 12))

    # Platform summary table
    story.append(Paragraph("At a Glance — All Platforms", h2_style))
    table_data = _platform_summary_table(all_data)
    col_widths = [1.6 * inch, 1.4 * inch, 1.1 * inch, 1.6 * inch, 1.1 * inch]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))

    # Claude analysis sections
    sections = _parse_sections(analysis)
    for section_title, content in sections.items():
        story.append(Paragraph(section_title, h2_style))
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("- ") or line.startswith("• ") or line.startswith("* "):
                story.append(Paragraph(f"• {line[2:]}", bullet_style))
            elif line[0].isdigit() and ". " in line[:4]:
                story.append(Paragraph(f"&nbsp;&nbsp;{line}", bullet_style))
            else:
                story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 8))

    # Footer note
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Spacer(1, 6))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey)
    story.append(Paragraph(
        f"Generated automatically by the Ruth Klein Analytics Agent · {run_date} · Next report in ~14 days",
        footer_style
    ))

    doc.build(story)
    print(f"[report] PDF saved: {output_path}")
