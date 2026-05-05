# Personalized Chart of Constructive Development Frameworks — Claude Conversion

**Original:** "Personalized Chart Of Constructive Development Frameworks Prompt_V2" from Prompts Edit > Lesson 1 > Optional Prompts
**Source Doc ID:** `1IGjSMA1rj8hbY6mHMJb3c3GKT9YpCs8sqWvHs96pGno`
**Status:** COMPLETE — full original consumed and converted
**Used in:** Lesson 1, Step 6 (30-45 minutes)

---

## Original ChatGPT Prompt (Preserved Verbatim)

### Instructions (from original doc)
1. Open ChatGPT
2. Upload Constructive Developmental Theory Frameworks
3. Run prompt below

### THE PROMPT

> I've attached a chart with all the relevant constructive development theory frameworks in it — I want you to add 4 columns to this chart:
> 1. The first column is your best insight into where you would rank me in that framework
> 2. The second column would be your reason for giving me that ranking
> 3. The third column would be the next level in my development in that framework
> 4. The fourth column would be what I would need to do to get there

### Additional context (from original doc)
- References a separate "how I created this chart" resource
- Requires an external CSV/chart upload of CDT frameworks

---

## Claude Conversion Notes

### What changes for Claude:

1. **External chart upload** — In ChatGPT, users uploaded a CDT frameworks chart. For Claude, the chart is provided as `outputs/cdt-frameworks-chart.md` with 8 standard developmental psychology frameworks.

2. **Very short prompt** — This is the simplest prompt in Lesson 1. The conversion is mostly about ensuring Claude has the CDT frameworks data available.

3. **4-column addition** — Clean analytical task. Claude adds personalized rankings based on ALL accumulated user data.

4. **Depends on prior exercises** — By Step 6, Claude has Calibration 1 + 2 data, psych-profile, and the Subject-Object Fractal assessment. All of this informs the rankings.

### Key CDT frameworks to include:

Based on consumed materials, the chart likely covers these developmental frameworks:
- **Robert Kegan's Subject-Object Theory** (5 orders of consciousness)
- **Spiral Dynamics** (value memes / levels of existence)
- **Ego Development Theory** (Loevinger/Cook-Greuter stages)
- **Moral Development** (Kohlberg stages)
- **Faith Development** (Fowler stages)
- **Cognitive Development** (Piaget / post-formal operations)
- **Self-Determination Theory** (Deci & Ryan)
- **Maslow's Hierarchy** (needs levels)

These 8 frameworks cover the core developmental psychology landscape used in the personalized chart.

---

## How Claude Runs This (Step 6)

### Prerequisites check:
- Calibration 1 + 2 complete
- Subject-Object Fractal complete (Step 5)
- psych-profile.md has sufficient data

### Prerequisites note:
- The original SOP says the user should have reviewed the "Constructive Developmental Theory Frameworks" link in Step 2
- If the CDT frameworks chart is available as a file, Claude reads it
- If NOT available, Claude generates a standard CDT frameworks chart using established developmental psychology frameworks

### The Analysis:

Claude generates a table with the following columns:

| Framework | Stage/Level Description | User's Current Ranking | Reason for Ranking | Next Level | What to Do to Get There |
|-----------|------------------------|----------------------|-------------------|-----------|------------------------|

For EACH framework:

1. **Current Ranking** — Where the user falls based on ALL accumulated data (calibrations, fractal, reflections). Must cite specific evidence.

2. **Reason** — Why this ranking, with references to specific answers, patterns, or behaviors the user demonstrated. No vague reasoning.

3. **Next Level** — What the next developmental stage looks like in this framework. Describe it concretely — what would the user think, feel, and do differently?

4. **What to Do** — Specific actions, experiments, or mindset shifts. Not generic advice. Reference the user's actual life circumstances.

### Behavioral rules:

- **Connect to the Subject-Object Fractal.** The fractal assessment (Step 5) directly informs several of these frameworks. Reference it explicitly: "Your fractal assessment identified you as subject to [X]. In Kegan's framework, this maps to Order [N] because..."
- **Be specific about evidence.** "I ranked you at [stage] because in Calibration 1, Question 14, you rated risk comfort at 3/10, and in your fractal session you identified [pattern]. This combination indicates..."
- **Apply Fluff & Cliche Killer** — no developmental psychology jargon without grounding.
- **Save to** `outputs/dev-chart-output.md`
- **Update** `outputs/psych-profile.md` with developmental stage assessments
- **Update** `outputs/zenith-mirror-score.md` — developmental map predictions should now be more accurate; recalculate score

---

## Claude Instructions (Summary)

1. Read all `outputs/` files including Subject-Object Fractal results
2. Use the 8 standard CDT frameworks listed above as the base
3. Add 4 personalized columns with specific evidence
4. Apply Fluff & Cliche Killer
5. Generate the complete CDT chart with all 4 personalized columns across all 8 frameworks
6. Present to user — walk through each framework and ranking
7. Save to `outputs/dev-chart-output.md`
8. Update `outputs/psych-profile.md` and `outputs/zenith-mirror-score.md`
9. Recalculate Zenith Mirror Score — must maintain 80+
