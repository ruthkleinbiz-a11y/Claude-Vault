#!/usr/bin/env python3
"""
Visibility Archetype Quiz — Teaser PDF Generator
Sent immediately after the quiz. Reveals the archetype, teases what's inside the
full report, and drives the lead to book a 15-minute call to claim their $500 report.

Usage: python3 generate_teaser.py
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether,
)

# ── Brand colors ──────────────────────────────────────────────────────────────
GOLD       = colors.HexColor("#B8962E")
DARK_GOLD  = colors.HexColor("#8B6914")
CREAM      = colors.HexColor("#F5F0E8")
CHARCOAL   = colors.HexColor("#1C1C1C")
MID_GRAY   = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#DDDDDD")
WHITE      = colors.white

# ── Archetype data ────────────────────────────────────────────────────────────
ARCHETYPES = {
    "The Hidden Expert": {
        "range": (8, 14),
        "tagline": "Your expertise is real. Your visibility isn't — yet.",
        "teaser_lines": [
            "You have the credentials, the results, and the track record.",
            "But the people who need you most can't find you — and right now, "
            "someone with less expertise is getting the opportunities you deserve.",
            "Your full $500 Visibility Report breaks down exactly why this is happening "
            "and the specific moves that will change it. "
            "It's yours — free — on a 15-minute call with Ruth.",
        ],
        "peek": [
            "What's really keeping you invisible (it's not what you think)",
            "The one positioning shift that makes you immediately findable",
            "Your 4 highest-leverage visibility moves — ranked by impact",
            "Why your expertise alone will never be enough, and what to add",
        ],
    },
    "The Scattered Voice": {
        "range": (15, 20),
        "tagline": "You're putting in the effort. It's not compounding — yet.",
        "teaser_lines": [
            "You've tried. You've posted, pitched, and shown up — and the results "
            "feel random.",
            "That's not a work ethic problem. It's a strategy problem. "
            "And it's completely fixable.",
            "Your full $500 Visibility Report shows you exactly what's missing "
            "and the specific moves to make everything you're already doing start compounding. "
            "It's yours — free — on a 15-minute call with Ruth.",
        ],
        "peek": [
            "Why your content isn't converting — and the one fix that changes it",
            "The positioning anchor that makes your message stick",
            "How to turn scattered effort into a system that builds on itself",
            "Your 4 highest-leverage visibility moves — ranked by impact",
        ],
    },
    "The Rising Authority": {
        "range": (21, 27),
        "tagline": "You're building real momentum. Let's accelerate it.",
        "teaser_lines": [
            "You're closer than you think. The recognition is coming — "
            "opportunities are starting to find you, and people in your space know your name.",
            "The gap between where you are and the level of visibility you're capable of "
            "is smaller than it feels. But it's specific — and worth closing fast.",
            "Your full $500 Visibility Report shows you exactly where to push next. "
            "It's yours — free — on a 15-minute call with Ruth.",
        ],
        "peek": [
            "The amplification moves that compress years of visibility-building into months",
            "How to build a signature framework that makes you citable and unforgettable",
            "The borrowed-audience strategy that's the highest-leverage move at your stage",
            "Your 4 highest-leverage visibility moves — ranked by impact",
        ],
    },
    "The Magnetic Leader": {
        "range": (28, 32),
        "tagline": "You've built something rare. Now let's take it further.",
        "teaser_lines": [
            "You've already done what most people only dream about — "
            "a clear voice, a strong reputation, and a presence that works for you.",
            "The question now isn't how to get visible. It's how to use what you've built "
            "to step into a bigger stage, a wider reach, a larger mission.",
            "Your full $500 Visibility Report maps your next move. "
            "It's yours — free — on a 15-minute call with Ruth.",
        ],
        "peek": [
            "How to expand your authority into new markets without starting over",
            "The IP-building moves that let your expertise scale beyond your time",
            "The curated, high-signal visibility moments worth more than a year of daily posts",
            "Your 4 highest-leverage moves at this exact stage",
        ],
    },
}

# ── Scoring ───────────────────────────────────────────────────────────────────

def answers_to_score(answers: list) -> int:
    return sum({"A": 1, "B": 2, "C": 3, "D": 4}.get(a.strip().upper(), 0) for a in answers)

def score_to_archetype(score: int) -> str:
    for name, d in ARCHETYPES.items():
        lo, hi = d["range"]
        if lo <= score <= hi:
            return name
    return "The Hidden Expert"

# ── Styles ────────────────────────────────────────────────────────────────────

def build_styles():
    s = {}
    s["body"] = ParagraphStyle(
        "body", fontSize=12, textColor=CHARCOAL, fontName="Helvetica",
        leading=19, spaceAfter=10, alignment=TA_JUSTIFY,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontSize=12, textColor=CHARCOAL, fontName="Helvetica",
        leading=18, spaceAfter=5, leftIndent=16,
    )
    s["peek_item"] = ParagraphStyle(
        "peek_item", fontSize=12, textColor=MID_GRAY, fontName="Helvetica-Oblique",
        leading=18, spaceAfter=5, leftIndent=16,
    )
    s["footer"] = ParagraphStyle(
        "footer", fontSize=9, textColor=MID_GRAY, fontName="Helvetica",
        alignment=TA_CENTER,
    )
    return s

# ── Page builder ──────────────────────────────────────────────────────────────

def generate_teaser(first_name: str, answers: list, output_path: str):
    score = answers_to_score(answers)
    archetype = score_to_archetype(score)
    data = ARCHETYPES[archetype]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.75 * inch,
        title=f"Visibility Archetype Result — {first_name}",
        author="Ruth Klein",
        subject="Your Visibility Archetype",
    )

    styles = build_styles()
    story = []

    # ── Dark header banner ────────────────────────────────────────────────────
    banner_text = (
        f"<font color='#{GOLD.hexval()[2:]}' size='11'>FREE QUIZ RESULT</font><br/><br/>"
        f"<font color='white' size='11'>Your Visibility Archetype is:</font><br/><br/>"
        f"<font color='#{GOLD.hexval()[2:]}' size='26'><b>{archetype}</b></font><br/><br/>"
        f"<font color='#{CREAM.hexval()[2:]}' size='12'><i>{data['tagline']}</i></font>"
    )
    banner = Table(
        [[Paragraph(banner_text, ParagraphStyle(
            "banner", fontSize=14, fontName="Helvetica",
            alignment=TA_CENTER, leading=30, textColor=WHITE,
        ))]],
        colWidths=[6.5 * inch],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CHARCOAL),
        ("TOPPADDING", (0, 0), (-1, -1), 36),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 36),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
    ]))
    story.append(banner)
    story.append(Spacer(1, 22))

    # ── Teaser copy ───────────────────────────────────────────────────────────
    story.append(KeepTogether([
        Paragraph(f"Hi {first_name},", ParagraphStyle(
            "greeting", fontSize=13, fontName="Helvetica-Bold",
            textColor=CHARCOAL, spaceAfter=10,
        )),
        *[Paragraph(line, styles["body"]) for line in data["teaser_lines"]],
    ]))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=12))

    # ── "What's inside" peek ─────────────────────────────────────────────────
    peek_block = [
        Paragraph(
            "Here's a glimpse of what's waiting for you in your full report:",
            ParagraphStyle("peek_head", fontSize=12, fontName="Helvetica-Bold",
                           textColor=CHARCOAL, spaceAfter=8),
        ),
    ]
    for item in data["peek"]:
        peek_block.append(Paragraph(f"<i>→  {item}</i>", styles["peek_item"]))
    peek_block.append(Spacer(1, 4))
    peek_block.append(Paragraph(
        "… and more. The full report is 6 pages of analysis specific to your archetype — "
        "your strengths, your gaps, and a prioritized action plan.",
        styles["body"],
    ))
    story.append(KeepTogether(peek_block))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=12))

    # ── Main CTA box ──────────────────────────────────────────────────────────
    cta_items = [
        Paragraph(
            f"<font color='#{GOLD.hexval()[2:]}'><b>Claim Your Free $500 Visibility Report</b></font>",
            ParagraphStyle("cta_head", fontSize=16, fontName="Helvetica-Bold",
                           textColor=GOLD, alignment=TA_CENTER, spaceAfter=10),
        ),
        Paragraph(
            f"Book a free 15-minute Visibility Strategy Call with Ruth Klein "
            f"and she'll walk you through your full personalized report — live, together.",
            ParagraphStyle("cta_body", fontSize=12, fontName="Helvetica",
                           textColor=CHARCOAL, leading=19, spaceAfter=10,
                           alignment=TA_CENTER),
        ),
        Paragraph(
            "On this call, Ruth will:",
            ParagraphStyle("cta_sub", fontSize=12, fontName="Helvetica-Bold",
                           textColor=CHARCOAL, spaceAfter=6, alignment=TA_LEFT),
        ),
        Paragraph("→  Reveal the full analysis of your archetype — what it means for your specific situation",
                  styles["bullet"]),
        Paragraph("→  Pinpoint your single highest-leverage visibility move right now",
                  styles["bullet"]),
        Paragraph("→  Give you an honest, expert assessment of exactly what's standing between you "
                  "and the visibility and recognition you're ready for",
                  styles["bullet"]),
        Spacer(1, 8),
        Paragraph(
            "This is not a sales call. This is 15 minutes of real strategy — "
            "the kind people pay $500 for. Ruth gives this to quiz takers because "
            "she believes in leading with value, and because the right fit clients "
            "always know it after one conversation.",
            ParagraphStyle("cta_fine", fontSize=11, fontName="Helvetica-Oblique",
                           textColor=MID_GRAY, leading=17, spaceAfter=12,
                           alignment=TA_JUSTIFY),
        ),
        Paragraph(
            "<b>Spots are limited. Ruth works with a small number of clients at a time.</b>",
            ParagraphStyle("cta_scarcity", fontSize=12, fontName="Helvetica-Bold",
                           textColor=CHARCOAL, alignment=TA_CENTER, spaceAfter=10),
        ),
        Paragraph(
            "→  <b>ruthklein.com/calendar</b>  ←",
            ParagraphStyle("cta_link", fontSize=14, fontName="Helvetica-Bold",
                           textColor=GOLD, alignment=TA_CENTER),
        ),
    ]

    cta_table = Table([[elem] for elem in cta_items], colWidths=[6.0 * inch])
    cta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("BOX", (0, 0), (-1, -1), 2.5, GOLD),
    ]))
    story.append(KeepTogether([cta_table]))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "© Ruth Klein  |  ruthklein.com  |  Questions? Reply to this email.",
        styles["footer"],
    ))

    doc.build(story)
    print(f"\n✓  Teaser generated: {output_path}")
    print(f"   Archetype: {archetype}  (score {score}/32)\n")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  VISIBILITY TEASER GENERATOR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print("This creates the 1-page teaser sent to leads immediately after the quiz.")
    print("The full report is sent separately before the strategy call.\n")

    first_name = input("Lead's first name: ").strip() or "Friend"

    print("\nEnter the 8 quiz answers (e.g. ABCDBCDA):\n")
    raw = input("Answers: ").strip().replace(" ", "").replace(",", "")
    answers = list(raw)

    if len(answers) != 8:
        print(f"\n⚠  Expected 8 answers, got {len(answers)}.")
        sys.exit(1)

    safe_name = first_name.lower().replace(" ", "-")
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, f"visibility-teaser-{safe_name}.pdf")

    generate_teaser(first_name, answers, output_path)


if __name__ == "__main__":
    main()
