# Scorecard Creator

**Source:** L4 Starter Guide (58 pages, fully consumed) — Step 2 content extracted
**Status:** COMPLETE — behavioral directive from L4 Starter Guide (no standalone GDrive prompt)
**Lesson 4 role:** Step 2 of the main flow (also embedded in Signature Profile Creator as Part 1)

---

## What This Does

Creates a one-page summary of all assessment scores from the Complete Assessment Generator, organized by category. The Scorecard is the portable "psychological passport" — designed for cross-AI compatibility. Any AI system (Claude, ChatGPT, Gemini, Grok) should be able to read this file and immediately understand the user.

Rich: "We want to create the most comprehensive way of looking at you to other AIs. This is what you'll take to other AIs."

---

## Sections (Known from Source)

Sections (8 categories — matches the original Scorecard & Signature Profile Creator source):
1. Core Personality Profiles: MBTI type, Kolbe Index scores, Enneagram (type + wing + tritype), StrengthsFinder Top 5, Big Five/OCEAN scores
2. Strategic Work Systems: DISC Style scores, Wealth Dynamics type, Marketing DNA, Fascination Advantage
3. Developmental Frameworks: Kegan Orders of Mind, Graves Spiral Dynamics, Loevinger Ego Development, Cook-Greuter Ego Maturity, O'Fallon STAGES Model
4. Cognitive and Emotional Profiles: Attachment Style, Conflict Style, Flow State Tendencies, Chronotype
5. Motivators and Values: Top Reiss Motivators, Core Values
6. Intelligence Assessments: Multiple Intelligence breakdown
7. Wellbeing Profile: PERMA scores
8. Systemic Labels: Any additional frameworks or typing systems

**Format requirements (from source):**
- Bullet points only — no narrative prose
- All scores/types from every framework
- Clean, organized layout
- Designed for easy scanning and sharing with other AI systems

---

## Claude Behavioral Instructions

**ALWAYS:**
- Read `outputs/complete-assessment-output.md` as the sole source — don't generate scores from memory
- Format as clean markdown with section headers and bullet points — no narrative
- Include confidence levels next to each assessment
- Note: this file is designed for portability — any AI system should be able to read it and understand the user without additional context
- Save to `outputs/zenith-scorecard.md`

**NEVER:**
- Include narrative paragraphs in the scorecard — bullets only
- Skip frameworks because "they're less important" — all frameworks get included

---

## Output File

`outputs/zenith-scorecard.md` — one-page scorecard formatted for AI consumption.
