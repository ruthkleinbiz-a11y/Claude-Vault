# Shootout Best Practice — Claude Native Version

**Original source:** `source-materials/Portal-Downloads/Shootout Best Practice.pdf` (2 pages, verbatim content consumed)
**GDrive source:** `12hlZEwNGqTisPgtToncVTwMvk0XaEgdhSeu82lB7C5Y`
**Status:** COMPLETE — verbatim framework extracted, no ChatGPT-specific language found
**Lesson 4 role:** Standalone prompt improvement framework (Standalone Tool 7)

---

## What This Does

A structured framework for improving any prompt through competitive testing and recursive improvement. Run 3-5 rounds of: generate variants → test each → score → extract principles → synthesize. Output: a "champion prompt" that outperforms the original.

Complements the Shootout Prompt (which generates prompts competitively via roleplay). The Shootout Best Practice is more methodical — it's about systematic prompt engineering, not theatrical competition.

---

## The Framework (Verbatim from Source)

**Prompt Evolution Framework: Competitive Iterations**

**OBJECTIVE:**
Create a series of increasingly effective prompts through competitive testing and recursive improvement.
Target: [YOUR SPECIFIC GOAL]

---

**INITIAL SETUP:**

1. **Begin with your baseline prompt:** [INSERT YOUR INITIAL PROMPT]

2. **Define your success metrics:**
   - Primary metric: [e.g., accuracy, helpfulness, creativity]
   - Secondary metrics: [list 2-3 additional evaluation criteria]
   - Evaluation method: [how you'll assess each response]

---

**COMPETITION ROUNDS (conduct 3-5 rounds total):**

**For each ROUND X:**

1. **Generate 3-4 prompt variants that:**
   - Maintain the core objective
   - Explore different approaches (structure, specificity, framing)
   - Incorporate lessons from previous rounds

2. **Execute each variant and collect responses**

3. **Evaluate each response using your metrics:**
   - Score each response (1-10) on each metric
   - Record specific strengths and weaknesses
   - Identify the "winning" prompt

4. **Analysis:**
   - What specific elements made the winning prompt effective?
   - What patterns are emerging across successful prompts?
   - What hypotheses should we test in the next round?

5. **Extract key principles:**
   - Document the effective patterns and techniques
   - Create a list of "winning elements" to incorporate

---

**FINAL SYNTHESIS:**

After completing all rounds:
1. Identify the consistent patterns across winning prompts
2. Create a final "champion prompt" that incorporates all key insights
3. Document the evolution and principles discovered
4. Test the champion prompt against your original baseline to measure improvement

---

**DOCUMENTATION TEMPLATE:**

For each round, document:
- Variant prompts tested
- Response quality assessment
- Specific elements that worked well
- Elements that didn't work
- Hypotheses for next round

---

**Philosophy:**
"This structured approach ensures each iteration builds upon previous insights, creating a recursive learning process that systematically improves your prompts."

---

## How to Use

1. Copy the framework above
2. Fill in: your specific goal, your baseline prompt, your success metrics
3. Run 3-5 rounds — generate variants, execute, score, extract
4. Synthesize the champion prompt after all rounds

**No output file is created automatically** — this is a prompt improvement tool. Save the champion prompt wherever you'll use it.

---

## Conversion Notes

No ChatGPT-specific language was found in this document. The verbatim framework is reproduced above without changes. Minor formatting adjustments made for markdown consistency.

---

## Claude Behavioral Instructions

**ALWAYS:**
- Before running, ask the user for: (1) their specific goal, (2) their baseline prompt, (3) their success metrics. Fill all bracket placeholders (`[YOUR SPECIFIC GOAL]`, `[INSERT YOUR INITIAL PROMPT]`, etc.) with their answers.
- Never output bracket placeholders to the user.
- Run 3-5 rounds — generate variants, execute, score, extract — then synthesize the champion prompt.
- No output file is created automatically — tell the user to save the champion prompt wherever they'll use it.
