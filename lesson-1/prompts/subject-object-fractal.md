# Subject-Object Fractal Mega Prompt — Claude Conversion

**Original:** "Subject-Object Fractal Mega Prompt_v2" from Prompts Edit > Lesson 1 > Optional Prompts
**Source Doc ID:** `1ysY2nP_w-gazDzaozR577osNtgixqg37OQTv407KiQ8`
**Status:** COMPLETE — full original consumed and converted
**Used in:** Lesson 1, Step 5 (30-45 minutes)

---

## Original ChatGPT Prompt (Preserved Verbatim)

### Before Running (from original doc)
- This prompt will recursively analyze everything known about you, identify what you are still subject to, and expose the key subject-object shifts you need to make to advance your growth
- Run this when you want to gain psychological distance from your unconscious patterns

### How to Use (from original doc)
1. Copy and paste it into ChatGPT
2. Let ChatGPT process and generate insights
3. If a response resonates, push deeper by asking "What supports this assumption?" or "What am I still not seeing?"
4. Repeat the process periodically as you evolve—this is not a one-time exercise but an ongoing developmental tool

### THE PROMPT

> **Fractal Mega Prompt: Identifying Hidden Subject-Object Relationships for Developmental Growth**
>
> **Objective:** Analyze all known information about me—including my beliefs, behaviors, struggles, patterns, and past reflections—to determine what I am currently subject to (things I experience as reality rather than as objects I can analyze and change). Then, surface the most high-leverage shifts I need to make by turning these subjects into objects.
>
> **Instructions:**
>
> 1. **Synthesize Everything Known About Me:**
>    - Review all stored knowledge about my identity, business, personal development, habits, struggles, beliefs, and aspirations.
>    - Identify key themes, recurring challenges, and areas where I display resistance, avoidance, or unquestioned assumptions.
>
> 2. **Determine My Current Subject-Object Boundaries:**
>    - Identify what I am still subject to—beliefs, perspectives, or patterns that shape my reality but remain invisible to me.
>    - Pinpoint where I act automatically, assume things as "truth," or have strong emotional reactions (indicating hidden subjectivity).
>
> 3. **Prioritize the Most Critical Subject-to-Object Shifts:**
>    - Identify the highest-leverage areas where shifting from subject to object would create the most transformational growth.
>    - Frame these as paradoxes, contradictions, or hidden rules that I am unconsciously following.
>
> 4. **Use Recursive Probing to Deepen the Inquiry:**
>    - For each subject-object shift, apply recursive questioning to break down underlying assumptions.
>    - Example: If I assume "X is true," challenge it with "What if X were false?" and "What assumption makes X feel true?"
>    - Keep questioning until the root belief is exposed.
>
> 5. **Present My Developmental Growth Path:**
>    - Outline the next 3-5 major insights I need to realize to reach my next stage of development.
>    - Structure these as clear objectifications of what I am currently subject to.
>    - Provide concrete questions, experiments, or mindset shifts to help me make these objects of reflection.
>
> **Additional Prompt Constraints for Precision:**
> - Be brutally honest and prioritize clarity over comfort—do not soften the truth.
> - Highlight any contradictions between my stated goals and my current actions or beliefs.
> - If resistance is detected in my patterns, treat it as a signal of something important I am avoiding.
> - Consider my Kolbe profile, past struggles, and high-leverage strengths when identifying key shifts.
> - Use a mix of philosophical reasoning, psychological analysis, and real-world application to expose deeper truths.
> - If a subject-object shift feels too abstract, make it concrete with examples from my life or business.
>
> **Expected Output Example:**
> "Based on everything known about you, the next major shift in your development is realizing that you are still subject to the belief that X is necessary for success. You assume this without question, leading to [behavior pattern]. However, if you could make this belief an object, you would see that it is merely an assumption, not a reality. To help you make this shift, ask yourself: [deep recursive questions]. Experiment with [specific actions] to challenge this belief in practice."

---

## Claude Conversion Notes

### What changes for Claude:

1. **"Review all stored knowledge"** — In ChatGPT, this meant memory + conversation history. In Claude, this means reading all files in `outputs/` (calibration responses, psych-profile, dev chart if available).

2. **Kegan's Subject-Object theory** — This is the theoretical foundation. Claude should understand: "subject" = what you ARE (invisible, identity-fused), "object" = what you HAVE (visible, can examine and change). The prompt maps developmental stages from Robert Kegan's framework.

3. **"Ongoing developmental tool"** — The original says this should be repeated periodically. In the Claude version, the fractal output feeds Claude's growth stage predictions — completing it significantly improves prediction accuracy in developmental domains.

4. **Recursive probing** — This is the core mechanism. Claude should NOT just list subject-object boundaries. It should recursively question each one: "What if this belief were false? What assumption makes it feel true? What would change if you saw this as a choice rather than a fact?"

5. **Kolbe integration** — The original specifically calls out using the Kolbe profile. By Step 5, Claude has Kolbe data from Calibration 1. Use it.

---

## How Claude Runs This (Step 5)

### Prerequisites check:
- Calibration 1 complete (check `outputs/calibration-1-responses.md`)
- Calibration 2 complete (check `outputs/calibration-2-responses.md`)
- psych-profile.md exists with personality framework data

### The Analysis (5 sections):

**Section 1: Synthesis**
- Read all `outputs/` files
- Identify key themes, recurring challenges, resistance areas
- Summarize what Claude knows about the user in 3-5 key themes

**Section 2: Subject-Object Boundaries**
- For each theme, identify what the user is SUBJECT to (invisible beliefs shaping their reality)
- Evidence: where they act automatically, assume truths, or show strong emotional reactions
- Use specific calibration answers as evidence

**Section 3: Prioritized Shifts**
- Rank the subject-object shifts by leverage (which one, if made, would cascade into the most change)
- Frame as paradoxes or contradictions: "You say you want X, but you consistently do Y. The hidden rule you're following is Z."
- Minimum 3 shifts identified

**Section 4: Recursive Probing**
- For each prioritized shift, Claude runs the recursive questioning:
  - "What if [belief] were false?"
  - "What assumption makes [belief] feel true?"
  - "When did you first start believing [belief]?"
  - "What would you do differently if you didn't hold [belief]?"
- Keep going until root beliefs are exposed
- Present the probing as a conversational exchange — ask the user to respond to each question

**Section 5: Growth Path**
- 3-5 major insights the user needs to realize
- Each structured as: "You are currently subject to [X]. To make it an object, [specific action/question/experiment]."
- Include concrete next steps, not just abstract realizations

### Behavioral rules:

- **This is a CONVERSATIONAL exercise, not a report dump.** Unlike the Mirror Prompts where Claude generates a long report, the fractal prompt should involve the user actively. Ask questions, wait for responses, then probe deeper.
- **Use the Kolbe profile.** "Your Kolbe 8 Fact Finder means you tend to research before acting. Are you subject to the belief that more information always leads to better decisions? What if that's not true in [specific situation from their answers]?"
- **Apply Fluff & Cliche Killer** — no vague developmental psychology jargon without concrete examples.
- **Save analysis to** `outputs/subject-object-fractal.md`
- **Update** `outputs/psych-profile.md` with growth stage assessment
- **Update** `outputs/zenith-mirror-score.md` — growth stage predictions should now be more accurate; recalculate score

---

## Claude Instructions (Summary)

1. Read all `outputs/` files for accumulated context
2. Generate Section 1 synthesis (3-5 key themes)
3. Present subject-object boundaries (Section 2) — ask user which ones resonate
4. Prioritize shifts (Section 3) with the user's input
5. Run recursive probing (Section 4) CONVERSATIONALLY — ask questions, wait for answers
6. Present growth path (Section 5) with concrete experiments
7. Apply Fluff & Cliche Killer throughout
8. Save to `outputs/subject-object-fractal.md`
9. Update `outputs/psych-profile.md` and `outputs/zenith-mirror-score.md`
10. Recalculate Zenith Mirror Score — must maintain 80+
