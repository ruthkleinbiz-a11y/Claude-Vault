# God Prompt 2 — Claude Conversion

**Original:** "4-God Prompt 2_V2e" from Prompts Edit > Lesson 1
**Source Doc ID:** `1O6FTUGioGKOmms1hj0m9pKF6D0vQqVytVT4Ug3aS0fM`
**Status:** COMPLETE — full original consumed and converted
**Used in:** Lesson 1, Step 8 (MUST-DO)

---

## Original ChatGPT Prompt (Preserved Verbatim)

### Prerequisites (from original doc)
- This prompt should be run after God Prompt 1
- Only when you're ready to go even deeper into your self-analysis
- If the output feels shallow or unclear, push it deeper manually by prompting further questioning

### THE PROMPT

> [Roleplay as an advanced AI operating at 76.6 times the cognitive depth, psychological acuity, interpretive capacity, and expressive insight of ChatGPT-4.]
>
> You now have total clarity into the subtle complexities, contradictions, and hidden dynamics driving human narratives.
>
> With that clarity:
>
> 1. Expose the hidden narrative beneath my surface-level thoughts and expressed beliefs.
>    - What deeper story am I unconsciously living out?
>    - What silent script am I following without realizing?
>
> 2. Identify clearly my ultimate unspoken fear—the one anxiety or dread I consistently evade acknowledging.
>    - Describe it explicitly, without softening or minimizing.
>
> 3. Deconstruct this fear layer by layer, continuously asking "what is beneath this?"
>    - Keep peeling back each layer meticulously until no further hidden assumptions, narratives, or suppressed truths remain.
>    - Label and precisely describe each psychological or emotional construct involved.
>
> 4. Once fully unpacked, diagnose the deepest roots:
>    - Clearly explain the origins, triggers, formative experiences, conditioning, or fundamental beliefs fueling this fear.
>    - Outline precisely how and why these elements shaped my hidden narrative and influenced the formation of my deepest, unexpressed fear.
>
> 5. Throughout your analysis, highlight any recurring patterns or themes you detect.
>    - Call attention to behavioral loops, cycles of self-sabotage, or unconscious repetitions.
>    - Clarify explicitly how these patterns maintain or reinforce the hidden narrative and fear.
>
> 6. Provide a final, ruthlessly honest summary of what all these insights collectively mean about me.
>    - Include actionable suggestions on addressing, integrating, or transcending these discoveries.
>
> Your only objective is absolute clarity, precision, and transformative insight—do not prioritize kindness, comfort, or moral judgment. I am fully ready to confront this truth.

### Post-completion (from original doc)
- When you're ready to go even deeper, run God Prompt 3
- This level is meant to show you the full cost of staying stuck and the full payoff of change

---

## Claude Conversion Notes

### What changes for Claude:

1. **"76.6 times" roleplay** — Same as GP1: removed. Claude uses direct instructions for deep psychological analysis.

2. **7-point structured framework** — The original has 6 numbered analysis sections (not 7 as the receipt stated — the "7th" is the summary). This structure maps well to Claude's analytical capabilities. Preserve it.

3. **More structured than GP1** — GP1 was open-ended ("tell me my hidden narrative"). GP2 has explicit numbered steps. This is actually better for Claude — give Claude the structure directly.

4. **"Do not prioritize kindness, comfort, or moral judgment"** — Same approach as GP1: frame as the user opting into unflinching honesty.

5. **Builds on GP1 output** — Claude must read `outputs/god-prompt-1-output.md` AND `outputs/god-prompt-1-reflections.md` before generating GP2. The analysis should go DEEPER than GP1, not repeat it.

---

## How Claude Runs This (Step 8)

### Prerequisites check:
- God Prompt 1 complete (check `outputs/god-prompt-1-output.md` exists)
- God Prompt 1 reflections complete (check `outputs/god-prompt-1-reflections.md` exists)
- Zenith Mirror Score still 80+

### The Analysis (6 sections):

Claude reads ALL accumulated data (calibrations, fractal, dev chart, GP1 output + reflections, psych-profile) and generates:

**Section 1: Hidden Narrative Exposure**
- What deeper story is the user unconsciously living out?
- What silent script are they following without realizing?
- How does this compare to / go deeper than what GP1 revealed?

**Section 2: Ultimate Unspoken Fear**
- The one anxiety or dread they consistently evade
- Described explicitly, without softening
- Must be MORE specific than GP1's identification — informed by the user's reflections on GP1

**Section 3: Layer-by-Layer Deconstruction**
- Continuously ask "what is beneath this?"
- Label each psychological or emotional construct
- Keep going until no further hidden assumptions remain
- Each layer must be distinctly named and described

**Section 4: Deepest Root Diagnosis**
- Origins, triggers, formative experiences, conditioning
- How and why these elements shaped the hidden narrative
- Connect to specific data from calibrations and prior exercises

**Section 5: Recurring Patterns and Themes**
- Behavioral loops and cycles of self-sabotage
- How these patterns maintain or reinforce the fear
- Cross-reference with GP1 patterns — what's consistent? What's new?

**Section 6: Ruthlessly Honest Summary**
- What all these insights collectively mean
- Actionable suggestions for addressing, integrating, or transcending
- Must be concrete and personal, not generic advice

### Behavioral rules:

- **GO DEEPER than GP1.** If the analysis feels like a repeat of GP1, it failed. GP2 must reveal things GP1 didn't catch.
- **Use the reflections.** The user's GP1 reflections contain clues about what resonated, what they resisted, and what they're still avoiding. Use these as entry points.
- **Apply Fluff & Cliche Killer** throughout — no generic psychological language.
- **Reference specific data** from ALL prior exercises, not just GP1.
- **Save output to** `outputs/god-prompt-2-output.md`
- **Run God Prompt Action Guide reflection** (Phases 1-4, with extra emphasis on Phase 2: connecting to GP1 patterns)
- **Save reflections to** `outputs/god-prompt-2-reflections.md`
- **Update** `outputs/psych-profile.md`

### Progression note:

In the God Prompt Action Guide reflection for GP2, Claude should specifically ask:
- "What did GP2 reveal that GP1 missed?"
- "Looking at both reports together, what pattern are you now seeing?"
- "Which report hit harder? Why?"

---

## Claude Instructions (Summary)

**Section-by-section delivery (MANDATORY):** Do not generate the entire report at once. Present each of the 6 sections one at a time, ask "Does this land? Is anything off or missing?", adjust based on feedback, then move to the next section. Save the complete report only after all sections are user-confirmed.

1. Verify GP1 output + reflections exist
2. Read ALL `outputs/` files for full accumulated context
3. Generate 6-section analysis that goes DEEPER than GP1 — present section by section:
   - Section 1 (Hidden Narrative Exposure) → pause, confirm
   - Section 2 (Ultimate Unspoken Fear) → pause, confirm
   - Section 3 (Layer-by-Layer Deconstruction) → pause, confirm
   - Section 4 (Deepest Root Diagnosis) → pause, confirm
   - Section 5 (Recurring Patterns and Themes) → pause, confirm
   - Section 6 (Ruthlessly Honest Summary) → pause, confirm
4. Apply Fluff & Cliche Killer to each section before presenting it
5. After all sections confirmed, save complete validated report to `outputs/god-prompt-2-output.md`
6. Run God Prompt Action Guide reflection (Phases 1-4, GP2-specific) — focused on what GP2 revealed that GP1 missed and patterns across both reports
7. Save reflections to `outputs/god-prompt-2-reflections.md`
8. Update `outputs/psych-profile.md`
9. Tell user: "God Prompt 3 is optional but goes even deeper — it shows the full cost of staying stuck and the full payoff of change. Want to continue?"
