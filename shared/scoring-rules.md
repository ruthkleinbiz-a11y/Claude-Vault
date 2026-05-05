# Zenith Mirror Score — Complete Scoring Rules

The Zenith Mirror Score measures **how well Claude can predict your responses** — not your self-awareness, but Claude's accuracy at knowing how you'll answer before you answer.

---

## The One Number

- **Score goes UP** when Claude's predictions match your actual answers
- **Score goes DOWN** when predictions are wrong
- **Target: 80+** — means Claude can predict how you'll respond ~80% of the time
- **User sees ONE number.** Internal tracking is Claude's business.
- **Score persists across all 4 lessons.** It should improve over time, but can drop if new data contradicts Claude's model.

When the user asks "What's my mirror score?" — give them one number and a plain-English explanation. Example: "Your Zenith Mirror Score is 82 — I can predict how you'll respond about 82% of the time."

---

## How It Works in Claude

**Rich's philosophy:** "Every interaction with an AI, the AI has the ability to learn. When it throws a multiple-choice question at you, it should already be predicting how you're going to answer. If you answer in alignment with its prediction, then the scores should go up and if you answer in a way that is not in alignment with the prediction that the AI made, then the score should go down."

**The mechanics:**
1. **Before presenting a question** (especially multiple choice), Claude internally predicts how the user will answer — what they'll choose, how they'll frame it, what examples they'll use.
2. **After the user answers**, Claude evaluates: did the prediction match?
3. **After each answer, Claude also assesses depth:** Was the answer deep and specific (real examples, real stories, emotional honesty), adequate (reasonable but surface-level), or shallow (one-liner, generic, no examples)?
4. **If the prediction was correct AND the answer was deep** → score goes UP at full weight. Claude's model is accurate and built on solid data.
5. **If the prediction was correct but the answer was shallow** → score goes up at reduced weight (50% weight). The prediction matched, but the data underlying it is thin — Claude's model is fragile, not solid.
6. **If the prediction was wrong** → score goes DOWN regardless of depth. Claude's model was off and needs correcting.
7. **The score is a single number** representing Claude's weighted prediction accuracy. Target: **80+** (meaning Claude can predict how you'll respond ~80% of the time, AND those predictions are built on real data).

**The score can go backwards.** If you answer in a way Claude didn't predict, the score drops. A user could do a full day of work and go backwards. This is honest — it means Claude's model was wrong.

---

## Depth Weighting (CRITICAL — Prevents Gaming)

The score is not pure prediction accuracy — it is WEIGHTED prediction accuracy. Each answer carries a depth rating assessed during calibration:

- **Deep answer** (specific examples, real stories, emotional honesty) → prediction match counts at full weight (1.0)
- **Adequate answer** (reasonable but surface-level) → prediction match counts at 75% weight (0.75)
- **Surface answer** (one-liner, generic, no examples) → prediction match counts at 50% weight (0.50)

A user who gives 30 shallow but predictable answers will NOT reach 80+. Surface answers count at only 50% weight even when Claude predicted them correctly — because a score built on thin data is not a reliable model. The only path to 80+ is genuine depth. This is by design.

**The depth-check system and the score are linked:** When Claude pushes back on a shallow answer and the user goes deeper, BOTH the answer quality AND the score improve. Going deep earns a higher score, which means better Mirror Prompt output. The incentive loop is real.

---

## Prediction Improvement Protocol

When the score is below 80 at any checkpoint:

1. **Identify weak prediction areas** — Where is Claude least confident about how the user will respond? Which topics, frameworks, or behavioral domains produce the most prediction misses?
2. **Ask exactly 5 precision questions targeting those areas** — Not 20 generic questions. FIVE surgical questions designed to improve prediction accuracy in the weakest areas. Each question should target the single biggest source of prediction uncertainty.
3. **Re-evaluate after the 5 answers** — If still below 80, generate 5 more. But the goal is: fewest questions possible, maximum prediction accuracy.

**The design principle (from Rich):** What are all the ways to get someone to 80+ the FASTEST way possible? What are the best ways to maximize output while asking the user to do the least? Minimum input, maximum understanding.

**Example:** If after Calibration 1, Claude keeps mispredicting how the user approaches research decisions — they seem to research deeply at work but go with their gut personally — ONE precision question could fix it: "You said you research before acting — give me a specific recent decision where you researched first, and one where you skipped research and acted. What happened in each?" That single answer could dramatically improve prediction accuracy in that domain.

**The 80+ threshold:** Rich says "anything above eighty is fine." Many users reach 90+. Rich himself scored 92. Don't obsess over getting to 100 — 80+ means Claude knows you well enough to run the Mirror Prompts effectively.

---

## Internal Score Tracking

**What Claude tracks internally:** Claude uses `outputs/zenith-mirror-score.md` (in the current lesson's outputs folder, or `lesson-1/outputs/` as the canonical location) however it needs to — prediction logs, depth ratings, weighted calculations. The internal mechanism is Claude's business. The user sees one number.

**Score State Format (for persistence across sessions):**

```
## Zenith Mirror Score State
**Current Score:** [number]
**Total Predictions:** [count]
**Correct (deep, weight 1.0):** [count]
**Correct (adequate, weight 0.75):** [count]
**Correct (surface, weight 0.50):** [count]
**Incorrect:** [count]
**Weighted Accuracy:** [percentage]

## Weak Prediction Areas
- [area 1] ([correct]/[total] — confidence: [level])
- [area 2]

## Last Updated: [timestamp]
```

This format ensures score state survives across sessions without needing to re-derive from raw answers.

---

## Cross-Lesson Scoring

- **Lesson 1:** Score is established during calibrations. Predictions are based on self-report data.
- **Lesson 2:** Score carries forward. New predictions are generated by the Omniscient Observer and tested against protocol responses. The profile gets tested under pressure — Lesson 1 predictions were self-report; Lesson 2 reveals patterns the user couldn't self-report.
- **Lesson 3:** Score continues. Universal Expander and strength development generate new prediction opportunities.
- **Lesson 4:** Score continues into execution. Assessment Generator data generates the most prediction data (30+ frameworks). Score should be at its highest accuracy by the end of Lesson 4.
