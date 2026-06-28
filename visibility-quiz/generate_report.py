#!/usr/bin/env python3
"""
Visibility Archetype Quiz — PDF Report Generator
Usage: python3 generate_report.py
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak

# ── Brand colors ──────────────────────────────────────────────────────────────
GOLD        = colors.HexColor("#B8962E")
DARK_GOLD   = colors.HexColor("#8B6914")
CREAM       = colors.HexColor("#F5F0E8")
CHARCOAL    = colors.HexColor("#1C1C1C")
MID_GRAY    = colors.HexColor("#555555")
LIGHT_GRAY  = colors.HexColor("#DDDDDD")
WHITE       = colors.white

# ── Archetype data ────────────────────────────────────────────────────────────
ARCHETYPES = {
    "The Hidden Expert": {
        "range": (8, 14),
        "tagline": "Your expertise is real. Your visibility isn't — yet.",
        "summary": (
            "You're doing excellent work, but you're operating on the wrong side of a glass wall. "
            "The people who need you most can't find you, and you're not sure how to change that "
            "without feeling salesy or self-promotional. "
            "Your credentials aren't the problem. Your strategy is."
        ),
        "strengths": [
            "Deep, hard-won expertise that others can't replicate",
            "High-quality work and strong results for those who do find you",
            "Authenticity — you haven't compromised your message to chase trends",
            "A clean slate: no bad reputation to undo, just a presence to build",
        ],
        "gaps": [
            "No consistent system for getting in front of the right people",
            "A message that works in conversation but doesn't travel well in writing or content",
            "Discomfort with self-promotion that keeps you playing smaller than you should",
            "Opportunities going to people with less expertise because they're more visible",
        ],
        "moves": [
            ("Define your Clear Choice Position",
             "In one sentence, you need to be able to say who you help, what you help them do, "
             "and why you're the one to do it. Not a paragraph — one sentence. This becomes the "
             "foundation of every piece of content, every bio, every conversation."),
            ("Choose one platform and own it",
             "Trying to be everywhere is how scattered voices stay scattered. Pick the one place "
             "your ideal clients actually spend time, and show up there consistently for 90 days "
             "before adding anything else."),
            ("Let your clients speak for you",
             "The fastest credibility shortcut available to you is testimonials and case studies. "
             "The transformation your clients experience is your most powerful marketing asset — "
             "and you're probably not using it."),
            ("Reframe visibility as service",
             "The people who need your expertise are out there right now, hiring someone with "
             "less experience because they couldn't find you. Getting visible isn't self-promotion "
             "— it's how you reach the people you're meant to serve."),
        ],
        "cta_hook": (
            "You're one strategy away from the people who need you most finally being able to find you. "
            "That strategy starts with a single conversation."
        ),
    },
    "The Scattered Voice": {
        "range": (15, 20),
        "tagline": "You're putting in the effort. It's not compounding — yet.",
        "summary": (
            "You know you need to be more visible and you've made real attempts — but the results "
            "feel random and the effort doesn't compound the way you hoped. You're active in bursts, "
            "but without a clear positioning strategy and a consistent message, every post and every "
            "pitch starts from zero. The fix isn't more content. It's clarity first."
        ),
        "strengths": [
            "Willingness to show up — you're not afraid to try",
            "Real expertise and genuine value to offer",
            "Some momentum and recognition, even if it feels inconsistent",
            "Awareness that something needs to change — which puts you ahead of most",
        ],
        "gaps": [
            "No clear positioning that makes you the obvious choice vs. the obvious option",
            "Inconsistent message across platforms, making it hard for your audience to follow you",
            "Content that educates without converting — visibility without lead generation",
            "Starting over with each new attempt instead of building on what's working",
        ],
        "moves": [
            ("Audit what's already working",
             "Before adding anything new, look at your last 90 days of content, conversations, "
             "and clients. What actually brought people to you? What post got the most response? "
             "What you're already doing that works is your signal — follow it."),
            ("Build a positioning anchor",
             "Pick one core message and repeat it across everything for 60 days. Consistency "
             "feels boring before it starts compounding. Your audience needs to hear the same "
             "thing multiple times before they remember it — and you're likely switching messages "
             "before they get the chance."),
            ("Create a content system, not just content",
             "One pillar piece per week (a LinkedIn post, a newsletter, a short video) repurposed "
             "into 3–5 shorter pieces is more effective than creating from scratch every day. "
             "Volume isn't the problem; system is."),
            ("Add a clear next step to everything you create",
             "Your content is probably informative without being directive. Every piece should "
             "tell your ideal client exactly what to do next — book a call, reply to this email, "
             "take the quiz. Without a next step, visibility stays visibility instead of becoming opportunity."),
        ],
        "cta_hook": (
            "The gap between scattered and strategic is smaller than it feels. "
            "A focused conversation can help you identify exactly what to stop, start, and double down on."
        ),
    },
    "The Rising Authority": {
        "range": (21, 27),
        "tagline": "You're building real momentum. Let's accelerate it.",
        "summary": (
            "Your expertise is recognized, your message is getting sharper, and opportunities are "
            "starting to find you. The gap between where you are and where you want to be is smaller "
            "than it feels — but it matters. What you're missing is the strategic amplification to "
            "turn what you're already doing into a consistent, compounding presence that earns you "
            "the visibility your work deserves."
        ),
        "strengths": [
            "A clear enough message that the right people are starting to respond to it",
            "Established credibility in your space — people know your name",
            "A track record of results that speaks for itself",
            "The discipline to show up consistently — which most people never master",
        ],
        "gaps": [
            "Visibility that's growing but not yet compounding — you're still working hard for each win",
            "A network that knows you but isn't actively amplifying you",
            "Content that's good but not yet generating consistent inbound leads",
            "The next level of stage — speaking, media, strategic partnerships — still out of reach",
        ],
        "moves": [
            ("Identify your amplifiers",
             "Who in your network has access to your ideal audience and trusts you enough to "
             "make an introduction? Strategic relationships — podcast hosts, event organizers, "
             "complementary experts — can compress years of visibility-building into months."),
            ("Build your signature framework",
             "The most visible experts in any field are known for a specific approach, not just "
             "their expertise. A named methodology, a signature process, a proprietary framework "
             "— this is what makes you citable, quotable, and memorable in a way that generic "
             "expertise never is."),
            ("Pursue borrowed audiences intentionally",
             "Guest podcasts, collaborative content, speaking slots — these get you in front of "
             "audiences that already trust the person who introduced you. At your stage, this is "
             "the highest-leverage visibility move available."),
            ("Systematize your lead generation",
             "You're past the 'get visible' phase. Now the goal is to make your visibility "
             "convert consistently. That means a clear lead capture mechanism, a nurture sequence, "
             "and a repeatable way to move people from 'following you' to 'working with you.'"),
        ],
        "cta_hook": (
            "You're closer than you think to the kind of visibility that creates consistent, "
            "compounding opportunity. A focused conversation can show you exactly where to push next."
        ),
    },
    "The Magnetic Leader": {
        "range": (28, 32),
        "tagline": "You've built something rare. Now let's take it further.",
        "summary": (
            "You've built what most people only aspire to — a clear voice, a strong reputation, "
            "and a presence that works for you. People seek you out. Your network generates "
            "opportunity. You're recognized in your space. The question now isn't how to get "
            "visible — it's how to use your visibility to create the next level of impact."
        ),
        "strengths": [
            "A distinctive, recognized voice that people associate with a specific outcome",
            "A network that actively sends you opportunities without being asked",
            "Proven authority — you've done it and can demonstrate the results",
            "The confidence and clarity to say no to the wrong opportunities",
        ],
        "gaps": [
            "Visibility that's powerful in your current market but not yet in new ones",
            "A platform built for who you've been, not necessarily who you're becoming",
            "The gap between your current reach and the size of the stage you're ready for",
            "Systems and leverage that would let your expertise scale beyond your time",
        ],
        "moves": [
            ("Define your next stage",
             "What does visibility look like at the next level of your ambition? A book? "
             "A keynote career? A media presence? A larger audience? Getting specific about "
             "the next stage is what allows you to build toward it deliberately instead of "
             "waiting for it to happen."),
            ("Expand your positioning to a new market",
             "Your authority in one space is transferable — but it doesn't automatically "
             "travel. Entering a new market or a larger stage requires a deliberate re-positioning "
             "strategy, not just showing up and expecting recognition to follow."),
            ("Build IP that scales without you",
             "The Magnetic Leader's next move is almost always productizing their expertise: "
             "a book, a course, a framework, a signature talk. This creates visibility and "
             "revenue that doesn't require you to be in the room."),
            ("Orchestrate strategic visibility moments",
             "At this stage, random content isn't the move — curated, high-signal moments are. "
             "A TEDx talk, a major podcast, a book launch, a keynote at a flagship industry event. "
             "One well-placed, well-executed visibility moment can do more than a year of daily posts."),
        ],
        "cta_hook": (
            "You've already proven you can build visibility. The conversation now is about "
            "using it to create something bigger — and doing it strategically."
        ),
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def score_to_archetype(score: int) -> str:
    for name, data in ARCHETYPES.items():
        lo, hi = data["range"]
        if lo <= score <= hi:
            return name
    return "The Hidden Expert"

def answers_to_score(answers: list) -> int:
    mapping = {"A": 1, "B": 2, "C": 3, "D": 4}
    return sum(mapping.get(a.strip().upper(), 0) for a in answers)

# ── Styles ────────────────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["cover_name"] = ParagraphStyle(
        "cover_name", fontSize=22, textColor=GOLD, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=4,
    )
    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontSize=30, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=6, leading=36,
    )
    styles["cover_archetype"] = ParagraphStyle(
        "cover_archetype", fontSize=18, textColor=GOLD, fontName="Helvetica-BoldOblique",
        alignment=TA_CENTER, spaceAfter=4,
    )
    styles["cover_tagline"] = ParagraphStyle(
        "cover_tagline", fontSize=13, textColor=CREAM, fontName="Helvetica-Oblique",
        alignment=TA_CENTER, spaceAfter=0,
    )
    styles["section_head"] = ParagraphStyle(
        "section_head", fontSize=14, textColor=GOLD, fontName="Helvetica-Bold",
        spaceBefore=18, spaceAfter=6,
    )
    styles["body"] = ParagraphStyle(
        "body", fontSize=11, textColor=CHARCOAL, fontName="Helvetica",
        leading=17, spaceAfter=8, alignment=TA_JUSTIFY,
    )
    styles["body_bold"] = ParagraphStyle(
        "body_bold", fontSize=11, textColor=CHARCOAL, fontName="Helvetica-Bold",
        leading=17, spaceAfter=4,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=11, textColor=CHARCOAL, fontName="Helvetica",
        leading=17, spaceAfter=4, leftIndent=16,
    )
    styles["move_title"] = ParagraphStyle(
        "move_title", fontSize=11, textColor=DARK_GOLD, fontName="Helvetica-Bold",
        leading=15, spaceAfter=2,
    )
    styles["move_body"] = ParagraphStyle(
        "move_body", fontSize=11, textColor=MID_GRAY, fontName="Helvetica",
        leading=16, spaceAfter=10, leftIndent=14, alignment=TA_JUSTIFY,
    )
    styles["cta_text"] = ParagraphStyle(
        "cta_text", fontSize=12, textColor=CHARCOAL, fontName="Helvetica",
        leading=18, spaceAfter=8, alignment=TA_JUSTIFY,
    )
    styles["cta_bold"] = ParagraphStyle(
        "cta_bold", fontSize=12, textColor=CHARCOAL, fontName="Helvetica-Bold",
        leading=18, spaceAfter=6,
    )
    styles["footer"] = ParagraphStyle(
        "footer", fontSize=9, textColor=MID_GRAY, fontName="Helvetica",
        alignment=TA_CENTER,
    )
    return styles


# ── Cover page ────────────────────────────────────────────────────────────────

def cover_page(story, first_name: str, archetype: str, data: dict, styles):
    # Dark banner background via a table
    banner_text = (
        f"<font color='#{GOLD.hexval()[2:]}'>Free Quiz Report</font><br/><br/>"
        f"<font color='white' size='28'><b>What's Your<br/>Visibility Archetype?</b></font><br/><br/>"
        f"<font color='#{CREAM.hexval()[2:]}' size='13'>Prepared for: </font>"
        f"<font color='#{GOLD.hexval()[2:]}' size='13'><b>{first_name}</b></font>"
    )
    banner = Table(
        [[Paragraph(banner_text, ParagraphStyle(
            "banner_inner", fontSize=14, fontName="Helvetica",
            alignment=TA_CENTER, leading=28, textColor=WHITE,
        ))]],
        colWidths=[6.5 * inch],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CHARCOAL),
        ("TOPPADDING", (0, 0), (-1, -1), 40),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 40),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
    ]))
    story.append(banner)
    story.append(Spacer(1, 20))

    # Archetype reveal box
    arch_box = Table(
        [[Paragraph(
            f"<font color='#{GOLD.hexval()[2:]}' size='11'>YOUR ARCHETYPE</font><br/>"
            f"<font size='22'><b>{archetype}</b></font><br/>"
            f"<font color='#{MID_GRAY.hexval()[2:]}' size='11'><i>{data['tagline']}</i></font>",
            ParagraphStyle("arch_box_inner", fontName="Helvetica",
                           alignment=TA_CENTER, leading=26, textColor=CHARCOAL),
        )]],
        colWidths=[6.5 * inch],
    )
    arch_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("BOX", (0, 0), (-1, -1), 1.5, GOLD),
    ]))
    story.append(arch_box)
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This report was created from your quiz responses to give you a clear picture of "
        "where you are, what's working, and exactly what to do next to become the clear "
        "choice in your field.",
        styles["body"],
    ))


# ── Section builder ───────────────────────────────────────────────────────────

def section_header(story, title: str, styles):
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=4))
    story.append(Paragraph(title, styles["section_head"]))


def build_summary(story, data: dict, styles):
    section_header(story, "What This Means For You", styles)
    story.append(Paragraph(data["summary"], styles["body"]))


def build_strengths(story, data: dict, styles):
    section_header(story, "What You're Already Doing Right", styles)
    story.append(Paragraph(
        "These aren't small wins — they're the foundation everything else gets built on:", styles["body"]
    ))
    for item in data["strengths"]:
        story.append(Paragraph(f"<b>→</b>  {item}", styles["bullet"]))


def build_gaps(story, data: dict, styles):
    section_header(story, "Where the Gap Lives", styles)
    story.append(Paragraph(
        "Understanding the gap is the first step to closing it:", styles["body"]
    ))
    for item in data["gaps"]:
        story.append(Paragraph(f"<b>→</b>  {item}", styles["bullet"]))


def build_moves(story, data: dict, styles):
    section_header(story, "Your 4 Priority Moves", styles)
    story.append(Paragraph(
        "These are the highest-leverage actions for someone at your exact stage:", styles["body"]
    ))
    for i, (title, body) in enumerate(data["moves"], 1):
        block = [
            Paragraph(f"{i}. {title}", styles["move_title"]),
            Paragraph(body, styles["move_body"]),
        ]
        story.append(KeepTogether(block))


def build_cta(story, first_name: str, data: dict, styles):
    story.append(Spacer(1, 10))
    cta_content = [
        [Paragraph(
            f"<font color='#{GOLD.hexval()[2:]}'><b>Ready to Move Faster, {first_name}?</b></font>",
            ParagraphStyle("cta_head", fontSize=15, fontName="Helvetica-Bold",
                           textColor=GOLD, alignment=TA_LEFT, spaceAfter=8),
        )],
        [Paragraph(data["cta_hook"], styles["cta_text"])],
        [Spacer(1, 4)],
        [Paragraph(
            "I work with experts, executives, and business owners who are ready to stop "
            "being the best-kept secret in their field — and become the clear choice. "
            "My clients don't just get more visible. They get visible in a way that "
            "generates real opportunities, real revenue, and real impact.",
            styles["cta_text"],
        )],
        [Spacer(1, 4)],
        [Paragraph(
            "<b>Book a complimentary 30-minute Visibility Strategy Call with me.</b>",
            styles["cta_bold"],
        )],
        [Paragraph(
            "We'll look at your specific situation, identify your fastest path to visibility, "
            "and you'll leave with clarity on exactly what to do next — whether we work "
            "together or not.",
            styles["cta_text"],
        )],
        [Spacer(1, 8)],
        [Paragraph(
            "→  <b>ruthklein.com/strategy-call</b>  ←",
            ParagraphStyle("cta_link", fontSize=13, fontName="Helvetica-Bold",
                           textColor=GOLD, alignment=TA_CENTER),
        )],
    ]
    flat = []
    for row in cta_content:
        flat.append(row[0])

    cta_table = Table([[elem] for elem in flat], colWidths=[6.0 * inch])
    cta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 22),
        ("RIGHTPADDING", (0, 0), (-1, -1), 22),
        ("BOX", (0, 0), (-1, -1), 2, GOLD),
    ]))
    story.append(cta_table)


def build_about(story, styles):
    story.append(Spacer(1, 16))
    section_header(story, "About Ruth Klein", styles)
    story.append(Paragraph(
        "Ruth Klein is a visibility strategist, bestselling author, and business acceleration "
        "expert who has helped hundreds of entrepreneurs, executives, and thought leaders "
        "build the kind of presence that creates consistent opportunity. Her clients become "
        "the recognized authorities in their fields — not by doing more, but by getting "
        "strategic about exactly how, where, and to whom they show up.",
        styles["body"],
    ))
    story.append(Paragraph(
        "Ruth's work has been featured in major media, and she brings decades of real-world "
        "experience helping experts stop being invisible and start being irresistible to "
        "the clients and opportunities they're meant to attract.",
        styles["body"],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("ruthklein.com", ParagraphStyle(
        "website", fontSize=11, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER,
    )))


# ── Main generator ────────────────────────────────────────────────────────────

def generate_report(first_name: str, answers: list, output_path: str):
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
        title=f"Visibility Archetype Report — {first_name}",
        author="Ruth Klein",
        subject="Visibility Archetype Quiz Report",
    )

    styles = build_styles()
    story = []

    cover_page(story, first_name, archetype, data, styles)
    story.append(Spacer(1, 16))
    build_summary(story, data, styles)
    build_strengths(story, data, styles)
    build_gaps(story, data, styles)
    build_moves(story, data, styles)
    story.append(Spacer(1, 10))
    build_cta(story, first_name, data, styles)
    build_about(story, styles)

    # Footer note
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"© Ruth Klein  |  ruthklein.com  |  This report was generated from your quiz responses.",
        styles["footer"],
    ))

    doc.build(story)
    print(f"\n✓  Report generated: {output_path}")
    print(f"   Archetype: {archetype}  (score {score}/32)\n")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  VISIBILITY ARCHETYPE REPORT GENERATOR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    first_name = input("Lead's first name: ").strip()
    if not first_name:
        first_name = "Friend"

    print("\nEnter the 8 quiz answers (A, B, C, or D for each question).")
    print("You can enter them as a single string (e.g. ABCDBCDA) or space-separated:\n")
    raw = input("Answers: ").strip().replace(" ", "").replace(",", "")
    answers = list(raw)

    if len(answers) != 8:
        print(f"\n⚠  Expected 8 answers, got {len(answers)}. Check your input and try again.")
        sys.exit(1)

    safe_name = first_name.lower().replace(" ", "-")
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, f"visibility-report-{safe_name}.pdf")

    generate_report(first_name, answers, output_path)


if __name__ == "__main__":
    main()
