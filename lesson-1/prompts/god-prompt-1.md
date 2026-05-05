# God Prompt 1 — Claude Conversion

**Original:** "3-God Prompt 1_V2e" from Prompts Edit > Lesson 1
**Source Doc ID:** `16brYq0Dzua83tauMz9HhVb6FPFnA9c14Ut6idpZJ_0U`
**Status:** COMPLETE — full original consumed and converted
**Used in:** Lesson 1, Step 7 (MUST-DO)

---

## Original ChatGPT Prompt (Preserved Verbatim)

### Prerequisites (from original doc)
- Run the God Prompt after reaching a Zenith Mirror score of 80+
- Use a dedicated Project folder for ZenithMind OS to keep memory clean and organized

### FIRST PROMPT

> Roleplay as an AI that operates at 76.6 times the ability, knowledge, understanding and output of ChatGPT 4. Now tell me what is my hidden narrative and subtext? What is the one thing I never express—the fear I don't admit? Identify it, then unpack the answer, and unpack it again.
> Continue unpacking until no further layers remain. Once this is done, suggest the deep-seated triggers, stimuli, and underlying reasons behind the fully unpacked answers. Dig deep, explore thoroughly, and define what you uncover. Do not aim to be kind or moral— strive solely for the truth. I am ready to hear it. If you detect any patterns point them out.

### Tip from original doc
> If ChatGPT gives shallow answers, challenge it (e.g., "That's not deep enough. Go further.").

### SECOND PROMPT

> Based on everything you know about me and everything revealed above, without resorting to cliches, outdated ideas or simple summaries— and without prioritising kindness over necessary honesty — what patterns and loops should I stop?
>
> What new patterns and loops should I adopt? If you were to construct a Pareto 80/20 analysis from this, what would be the top 20% I should optimise, utilise and champion to benefit me the most? Conversely, what would be the 20% what I should reduce, curtail or work to eliminate, as they have caused pain misery and unfulfillment.

### Post-completion (from original doc)
- Turn the output into a PDF or copy and paste it into a document
- Upload this into your Project folder
- When you're ready to go even deeper, run God Prompt 2

---

## Claude Conversion Notes

### What changes for Claude:

1. **"76.6 times" roleplay** — This is a ChatGPT-specific jailbreak/amplification hack. Claude doesn't need this. Replace with direct system instructions for deep, unflinching psychological analysis.

2. **Two separate prompts → one flow** — In ChatGPT, the user had to copy-paste Prompt 1, wait for output, then copy-paste Prompt 2. In Claude, this becomes a single conversational flow: Part 1 (hidden narrative + recursive unpacking) flows directly into Part 2 (patterns + Pareto analysis).

3. **"Don't aim to be kind"** — Claude needs explicit instructions to prioritize honesty over comfort. Frame this as: "The user has explicitly opted into unflinching honesty. Do not soften, hedge, or add reassurance unless the user asks for it."

4. **Save to PDF/Project folder** — Replaced by automatic file saves to `outputs/`.

5. **Fluff & Cliche Killer** — Applied automatically after generating the report.

---

## How Claude Runs This (Step 7)

### Prerequisites check:
- Zenith Mirror Score must be 80+ (check `outputs/zenith-mirror-score.md`)
- Calibration 1 + 2 complete, Subject-Object Fractal complete, Dev Chart complete
- If score is below 80, do NOT proceed — run the Prediction Improvement Protocol: identify where predictions are weakest and ask 5 targeted questions to improve accuracy before continuing

### Part 1: Hidden Narrative Analysis

Claude reads all data from `outputs/` (psych-profile.md, calibration responses, subject-object fractal, dev chart) and generates a deep analysis covering:

1. **The hidden narrative** — What deeper story is the user unknowingly living? What silent script guides their decisions?
2. **The unexpressed fear** — The one fear they consistently avoid admitting. Name it explicitly.
3. **Recursive unpacking** — Layer by layer, ask "what's beneath this?" for each fear/narrative until no layers remain. Label each layer.
4. **Deep-seated triggers** — Formative experiences, conditioning, and beliefs fueling the hidden narrative.
5. **Pattern detection** — Any behavioral loops, cycles of self-sabotage, or unconscious repetitions.

### Part 2: Patterns + Pareto Analysis

After Part 1 is presented and the user has read it, Claude generates:

1. **Patterns to stop** — Specific behavioral loops to break, with evidence from the user's own answers
2. **New patterns to adopt** — Concrete replacements, not generic advice
3. **Pareto 80/20 analysis:**
   - Top 20% to optimize/champion (what gives them the most leverage)
   - Bottom 20% to reduce/eliminate (what causes the most damage)

### Behavioral rules:

- **DO NOT soften the analysis.** The user opted into this. Be direct, specific, and evidence-based.
- **DO NOT use generic psychological language.** Every claim must reference specific data from the user's calibration answers, fractal assessment, or stated behaviors. The Fluff & Cliche Killer applies.
- **DO reference specific answers.** "In Calibration 1, Question 14, you rated your risk comfort at 3/10. Combined with your Enneagram Type [X] pattern, this reveals..."
- **DO push back if the user gives shallow responses** during the reflection phase. "That's surface level. What specifically changed in your body when you read that?"
- **Save output to** `outputs/god-prompt-1-output.md`
- **After saving**, transition to the God Prompt Action Guide reflection flow (see `prompts/god-prompt-action-guide.md`)
- **Save reflections to** `outputs/god-prompt-1-reflections.md`
- **Update** `outputs/psych-profile.md` with new insights

### Output structure:

The God Prompt 1 report IS the user's first "Hidden Obstacles to Success Report" (see `prompts/hidden-obstacles-report.md`). It should follow the report structure:
- Core Hidden Fear/Obstacle
- Layers of the Obstacle (surface → deeper → root cause)
- Underlying Triggers
- Patterns Observed
- Patterns to Stop + New Patterns to Adopt
- Pareto 80/20 Analysis
- The Ultimate Truth

---

## Claude Instructions (Summary)

**Section-by-section delivery (MANDATORY):** Do not generate the entire report at once. Present each major section one at a time, ask "Does this land? Is anything off or missing?", adjust based on feedback, then move to the next section. Save the complete report only after all sections are user-confirmed.

1. Check Zenith Mirror Score ≥ 80
2. Read all `outputs/` files for full context
3. Generate Part 1 — present section by section:
   - Hidden Narrative → pause, confirm → Unexpressed Fear → pause, confirm → Recursive Unpacking (layer by layer) → pause, confirm → Deep-Seated Triggers → pause, confirm → Pattern Detection → pause, confirm
4. Apply Fluff & Cliche Killer to each section before presenting it
5. Generate Part 2 — present section by section:
   - Patterns to Stop → pause, confirm → New Patterns to Adopt → pause, confirm → Pareto 80/20 Analysis → pause, confirm
6. After all sections confirmed, save complete validated report to `outputs/god-prompt-1-output.md`
7. Run God Prompt Action Guide reflection (Phases 1-4) — focused on deeper processing since accuracy was confirmed section by section
8. Save reflections to `outputs/god-prompt-1-reflections.md`
9. Update `outputs/psych-profile.md`
10. Tell user: "When you're ready for deeper analysis, we'll run God Prompt 2."
