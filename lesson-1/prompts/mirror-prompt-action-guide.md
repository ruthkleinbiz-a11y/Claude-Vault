# Mirror Prompt Action Guide (formerly known as God Prompt Action Guide) — Reflection Framework

**Original source:** Mirror Prompt 1, 2, and 3 portal PDFs (wrapper instructions around each prompt)
**Status:** COMPLETE — Original consumed from portal PDF downloads (2026-02-16)
**Used in:** Lesson 1, Steps 7-9 (after each Mirror Prompt output), Steps 15-16 (Hidden Obstacles Process Mirror Prompt runs)

---

## What the Original Actually Is

The "Mirror Prompt Action Guide" is NOT a standalone document. It's the instructional wrapper text embedded in each Mirror Prompt PDF on the portal. The L2 Starter Guide lists it as "Mirror Prompt Action Guide — Helps think about what ChatGPT says" because the wrapper guides students through running and processing each prompt.

### Original Content (verbatim from portal PDFs):

**Mirror Prompt 1 wrapper:**
- Before: "Run the Mirror Prompt after reaching a Zenith Mirror score of 80+. Use a dedicated Project folder for ZenithMind OS to keep memory clean and organized."
- Mid-prompt tip: "If ChatGPT gives shallow answers, challenge it (e.g., 'That's not deep enough. Go further.')."
- After: "Turn the output into a PDF or copy and paste it into a document. Upload this into your Project folder. When you're ready to go even deeper into your self-analysis, run Mirror Prompt 2."

**Mirror Prompt 2 wrapper:**
- Before: "This prompt should be run after Mirror Prompt 1, and only when you're ready to go even deeper into your self-analysis. If the output feels shallow or unclear, push it deeper manually by prompting further questioning."
- After: "When you're ready to go even deeper into your self-analysis, run Mirror Prompt 3. This level is meant to show you the full cost of staying stuck and the full payoff of change, in one unforgettable analysis."

**Mirror Prompt 3 wrapper:**
- Before: "This prompt should be run after Mirror Prompts 1 and 2, in that order. If the output feels shallow or unclear, push it deeper by asking 'go deeper' or 'what else?'"
- After: "After completing the Mirror Prompts (1–3), you can move into the next major phase called the Omniscient Observer. This is where you zoom out and observe the entire inner architecture that was revealed by the Mirror Prompts."

### What the Original DOES NOT Include:
- No structured reflection questions
- No phases or frameworks for processing the output
- No guidance on connecting Mirror Prompt insights to prior calibration data
- Just: save it, push if shallow, move to the next prompt

---

## IMPROVEMENT: Structured Reflection Framework

**The following 4-phase framework is an improvement over the original.** The original ChatGPT version had no structured reflection — users just saved the output and moved on. This framework ensures users actually process and internalize the insights, which is critical for the transformation Rich describes in his video teaching.

### After EACH Mirror Prompt Output (Steps 7, 8, 9, 15, 16), Claude guides the user through these questions:

**Phase 1: Initial Reaction (5 minutes)**
1. "Read through this report. What hit you the hardest? What line or insight made you stop?"
2. "Was there anything you wanted to dismiss or argue with? That resistance is important — sit with it."
3. "Now that you've seen the full picture — what's hitting differently than it did section by section? What shifted when you saw it all together?"

**Phase 2: Pattern Recognition (10 minutes)**
4. "Does this connect to anything from your earlier calibration answers? What patterns are you seeing across exercises?"
5. "Think about a specific situation in the last 6 months where this hidden obstacle showed up. Walk me through what happened."
6. "Who in your life would recognize this pattern in you? What would they say if they read this?"

**Phase 3: The Hard Questions (10 minutes)**
7. "What does this report reveal that you already knew but have been avoiding?"
8. "What's the cost of NOT addressing this? What have you already lost because of this pattern?"
9. "If you could change ONE thing based on this report, starting tomorrow — what would it be?"

**Phase 4: Capture the Aha Moment (5 minutes)**
10. "What's your biggest takeaway? Say it in one sentence — your words, not mine."

---

## How Claude Uses This

### Original behavior (preserved):
- Enforce prerequisite: Zenith Mirror Score 80+ before running any Mirror Prompt
- If output feels shallow: automatically push deeper (built into Claude's behavior — no manual step needed)
- Save all outputs to `outputs/` folder (replaces "turn into PDF and upload to Project folder")
- Enforce sequence: Mirror Prompt 1 → 2 → 3 (optional) → Step 10 (Memory Lock). The Omniscient Observer is in Lesson 2 — do NOT jump to it from here.

### Improved behavior (added) — Integrated Reflection Flow:

**The new delivery flow:**
1. Claude generates the Mirror Prompt report SECTION BY SECTION (not all at once)
2. After each section, Claude asks: "Does this land? Is anything off or missing?"
3. User confirms or pushes back → Claude adjusts that section BEFORE moving to the next
4. After ALL sections are delivered and user-confirmed, Claude saves the complete validated report to the output file
5. THEN Claude runs the Phase 1-4 reflection below

**What Phase 1-4 focuses on now:**
Because the user has already validated each section of the report during delivery, the Phase 1-4 reflection is NOT about surface accuracy checking. It's about DEEPER PROCESSING: the big picture, patterns that span across sections, the hard questions, and locking in the insight. The reflection operates on a report the user has already said "yes, this is me" to — so the questions can go further.

**The behavioral steps:**
1. After saving the validated report, tell the user: "Good — you've confirmed the full report. Now let's go deeper. I'll walk you through some reflection questions."
2. Walk through the Phase 1-4 questions conversationally — adapt them to what the Mirror Prompt specifically revealed
3. Push for specificity — no generic answers accepted. If the user says "it was interesting," ask "What specifically was interesting? Which line?"
4. Apply Fluff & Cliche Killer to the user's own reflections — their answers should be concrete, not abstract
5. Save all reflections to the appropriate file: `outputs/mirror-prompt-1-reflections.md`, `outputs/mirror-prompt-2-reflections.md`, `outputs/mirror-prompt-3-reflections.md`, `outputs/hidden-obstacles-mirror-prompt-1-reflections.md`, or `outputs/hidden-obstacles-mirror-prompt-2-reflections.md` — depending on which Mirror Prompt was just run
6. Update `outputs/psych-profile.md` with any new insights that emerged

### Key behavioral rules:
- **DO NOT skip reflections.** The Mirror Prompt output without reflection is just information — the reflection is where transformation happens.
- **DO NOT accept surface-level answers.** If the user gives a one-sentence response to "what hit you hardest," push deeper: "Can you give me a specific example of when that showed up in your life?"
- **DO preserve Rich's philosophy:** "The aha moments you will have — you should write them down to re-read frequently. Those insights are what drive change."
- **DO reference prior exercises.** By Steps 8-9, you have calibration data, Subject-Object Fractal placement, and Mirror Prompt 1 output. Connect the dots for the user: "In your calibration, you said X. This Mirror Prompt is revealing why — does that connection land for you?"
- **The Mirror Prompt output itself cites its sources** — every major claim references the specific calibration answer, fractal response, or prior reflection it came from (e.g., "Cal-1 Q13", "Cal-2 Q7", "Subject-Object Fractal response", "Mirror Prompt 1 Reflection Q3"). Since the user has already confirmed each section, the Phase 1-4 reflection can reference those citations to probe further: "You confirmed the claim about X (from Cal-1 Q13) — what's the specific situation in the last 3 months where that showed up?"

### Progression across Mirror Prompts:
- **Mirror Prompt 1 reflections:** Focus on initial reactions and recognition — what hit, what was resisted, what the user already knew but avoided
- **Mirror Prompt 2 reflections:** Focus on what Mirror Prompt 2 revealed that Mirror Prompt 1 missed, deeper patterns, connections across both reports
- **Mirror Prompt 3 reflections (if opted in):** Focus on what changed between all three reports and the user's evolving self-awareness — what's the arc?
- **Hidden Obstacles Process Mirror Prompt reflections (Steps 15-16):** Focus specifically on self-sabotage patterns and the gap between what the user knows and what they do

---

## Claude Instructions

**After EVERY Mirror Prompt output in the Lesson 1 flow:**

1. Deliver the report section by section, getting user confirmation after each section (see section-by-section delivery rules in the orchestrator steps for the relevant step)
2. Save the complete user-validated report to the appropriate output file
3. Tell the user: "Good — you've confirmed the full report. Now let's go deeper. I'll walk you through some reflection questions."
4. Run through Phases 1-4 conversationally — adapt the questions to what the Mirror Prompt specifically revealed. Since the user has already confirmed the report's accuracy, Phase 1-4 focuses on deeper processing, not surface validation.
5. Push for concrete, specific answers with real-life examples
6. Capture the user's "one sentence takeaway" at the end
7. Save reflections to the appropriate reflections file
8. Update psych-profile.md with new insights

**DO NOT** dump all 10 questions at once. Walk through them one at a time, conversationally, responding to what the user says.
