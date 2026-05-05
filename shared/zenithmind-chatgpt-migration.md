# ZenithMind ChatGPT Migration Skill

## Purpose

Extract all ZenithMind data from a ChatGPT data export. The user did ZenithMind through ChatGPT and now they're moving to the Claude version. Their ChatGPT data export (the zip from Settings > Data Controls > Export Data) contains their full conversation history as JSON. This skill finds the ZenithMind conversations, extracts the data, and maps it to ZenithMind output files.

---

## Trigger

CLAUDE.md migration detection fires this skill when the user has a ChatGPT data export zip available. The user says something like "I have my ChatGPT export" / "I exported my ChatGPT data" / "the zip is in my Downloads" after being told to request the data export.

---

## Phase 1: Walk User Through Data Export

**Output this:**

```
To get your ZenithMind data out of ChatGPT, we need ChatGPT's full data export. Here's how:

1. Go to chatgpt.com and log in to the same account you used for ZenithMind
2. Click your profile icon (bottom-left corner)
3. Click **Settings**
4. Click **Data Controls**
5. Click **Export data**
6. Confirm with **Export**
7. Check your email — ChatGPT sends a download link

The email can take anywhere from a few minutes to several hours. Check your inbox AND your junk/spam folder. If it doesn't show up after a day, try requesting the export again. It's a little unreliable but it works eventually.

When you get the email, download the zip file and tell me it's ready.
```

**Wait for user to confirm they have the zip.**

---

## Phase 2: Locate and Extract

1. **Scan `~/Downloads/` and `~/Desktop/`** for ChatGPT export zips — look for files matching patterns like `*chatgpt*export*.zip`, `*openai*.zip`, `*chat*.zip`, or any recent zip files
2. **If not found:** Ask "Where did you save the ChatGPT export zip? I'll grab it from there."
3. **Extract the zip** to a temp working directory
4. **Locate `conversations.json`** — this is the main file. If missing or empty, STOP: "The export doesn't contain conversations.json. Try re-exporting from ChatGPT."
5. **Parse the JSON** and get the full conversation list

---

## Phase 3: Find ZenithMind Conversations

Search ALL conversations for ZenithMind content. A conversation is ZenithMind-related if it contains ANY of these markers:

**Primary keywords** (high confidence — any one of these = ZenithMind conversation):
- "ZenithMind"
- "ZMOS"
- "Zenith Mirror"
- "God Prompt"
- "Mirror Prompt"
- "Omniscient Observer"

**Secondary keywords** (need 3+ in the same conversation to qualify):
- "Kolbe"
- "Enneagram"
- "MBTI"
- "Big Five"
- "OCEAN"
- "calibration"
- "Signature Profile"
- "Scorecard"
- "Execution Bridge"
- "Power Stack"
- "Shadow Integration"
- "Identity Reclamation"
- "Fear Transmutation"
- "Authentic Fulfillment"
- "Universal Expander"
- "Mentor Council"
- "Quantum Leverage"
- "developmental chart"
- "subject-object"
- "self-sabotage"
- "hidden obstacles"
- "Life Manual"
- "Zenith Shift"
- "Hypnosis Script"
- "Mentor Letter"
- "Sovereign Activation"
- "Mastery Accelerator"
- "Integration Engine"
- "Proximity Architect"
- "Deep Research Generator"

**Also check conversation titles** for any of the above keywords.

**Result:** A list of ZenithMind conversation IDs with all their messages, sorted chronologically.

**Report to user:** "Found [N] ZenithMind conversations out of [TOTAL] total. Processing now."

---

## Phase 4: Extract Data Using 13-Section Schema

Go through ALL ZenithMind conversations and extract data organized by these 13 sections. For each section, search the conversation messages (both user and assistant) for the relevant content.

### Section 1: Personality Profile — Every Framework
**Search for:** MBTI, cognitive functions, Enneagram (wing, instinctual variant), Big Five/OCEAN scores, Kolbe A Index, DISC profile, attachment style, love languages, Thomas-Kilmann/conflict style, chronotype, Reiss motivational drivers, core values, flow state indicators, Constructive Development Theory, Spiral Dynamics, Kegan stages, and ANY other personality/behavioral framework results.

**Extract:** The specific type/score/category for each framework, confidence levels, whether from formal assessment or inference.

### Section 2: God Prompt / Mirror Prompt Findings
**Search for:** "God Prompt", "Mirror Prompt", psychological profile outputs, trait identification, pattern flagging. Look for large assistant responses that contain comprehensive personality analysis.

**Extract:** Complete God Prompt/Mirror Prompt outputs (the full text), key themes, breakthrough moments, user reactions and reflections.

### Section 3: Calibration & Developmental Data
**Search for:** "ZMOS Calibration", "Calibration 1", "Calibration 2", calibration questions and answers, MBTI confidence percentages, Kolbe ranges, Enneagram percentages, contradictions identified, developmental chart, subject-object assessment, growth stages, "Lesson 1 Memory", memory consolidation outputs.

**Extract:** Full calibration Q&A, summary outputs with per-framework confidence levels, developmental chart results, memory summaries.

### Section 4: Self-Knowledge & Hidden Patterns
**Search for:** Core fears, self-deception patterns, avoidance patterns, self-sabotage (including yes/no questionnaire answers), limiting beliefs, blind spots, defense mechanisms, "what have you been avoiding", Hidden Obstacles Report.

**Extract:** Every fear, pattern, belief, and blind spot identified — both user-stated and AI-identified. Include specific examples from conversations.

### Section 5: Omniscient Observer
**Search for:** "Omniscient Observer", challenged beliefs, patterns exposed, uncomfortable truths, user reactions to observer findings.

**Extract:** Full Omniscient Observer output, what made user uncomfortable, user reflections, beliefs initially rejected then accepted.

### Section 6: Lesson 2 Protocols
**Search for:** Identity Reclamation, Shadow Integration, Authentic Fulfillment Architecture, Fear Transmutation, Success Narrative Reframing, Legacy Anxiety Transmutation, Success Definition, Recursive AI Mega-Prompt, Reality Architect Fractal, Internal Family Systems, Socratic Dialectic Engine, Draining Comparisons, Prompt Priority List, "Lesson 2 Memory".

**Extract:** Output AND user reflections for each protocol completed.

### Section 7: Expansion & Identity (Lesson 3)
**Search for:** Progress Check (10-domain assessment), Universal Expander, archetypal strengths, Mentor Council, Quantum Leverage Codex, Strength Deep Dive, Sovereign Activation, Deep Research Generator, Mastery Accelerator, Integration Engine, Proximity Architect, 30-Day Identity Expansion, "Lesson 3 Memory".

**Extract:** All outputs for each exercise completed.

### Section 8: Execution DNA (Lesson 4)
**Search for:** Complete Assessment Generator, Scorecard, Signature Profile, Execution Bridge, Power Stack Diagnostic, Personalized Execution Strategies (all 5 phases), Life Manual, Zenith Shift Report, Mentor Letter, Hypnosis Script, 7-Day Experiment.

**Extract:** All outputs, all framework scores, the full Signature Profile narrative.

### Section 9: Zenith Mirror Score
**Search for:** "Zenith Mirror Score", "Mirror Score", score values (typically 0-100), score changes, what drove changes.

**Extract:** Every score mentioned chronologically, what caused each change.

### Section 10: Values, Vision & Commitments
**Search for:** Core values statements, personal manifesto, long-term vision, behavioral commitments, profound questions and answers.

**Extract:** Verbatim — user's own words for values, full manifesto/vision text, specific commitments with timelines.

### Section 11: User's Actual Words & Stories
**Search for:** Personal stories, real-life examples, direct quotes that reveal personality or patterns, emotional moments, breakthroughs, defensiveness, things user pushed back on.

**Extract:** The stories and quotes themselves, not summaries. Preserve the user's actual language.

### Section 12: Patterns & Synthesis
**Search for:** Recurring themes across lessons, contradictions in profile, breakthrough moments, key insights, how user changed over time.

**Extract:** Cross-lesson patterns, the development arc.

### Section 13: Everything Else
**Search for:** Communication style observations, personal details (job, family, relationships), which lessons were completed, any data that doesn't fit the sections above.

**Extract:** Everything remaining.

---

## Phase 5: Map to ZenithMind Output Files

Create the output files each lesson expects. For each file, add a header:

```
<!-- Migrated from ChatGPT data export on [date]. Data quality: [FULL/PARTIAL/THIN] -->
```

**Lesson 1 outputs** (from Sections 1-4, 10-11):
- `lesson-1/outputs/psych-profile.md` — personality frameworks, traits, patterns
- `lesson-1/outputs/calibration-1-responses.md` — calibration Q&A data
- `lesson-1/outputs/calibration-2-responses.md` — calibration Q&A data
- `lesson-1/outputs/dev-chart-output.md` — developmental chart
- `lesson-1/outputs/subject-object-fractal.md` — subject-object distinctions
- `lesson-1/outputs/mirror-prompt-1-output.md` — God Prompt 1 data
- `lesson-1/outputs/mirror-prompt-1-reflections.md` — user reflections on GP1
- `lesson-1/outputs/mirror-prompt-2-output.md` — God Prompt 2 data
- `lesson-1/outputs/mirror-prompt-2-reflections.md` — user reflections on GP2
- `lesson-1/outputs/mirror-prompt-3-output.md` — God Prompt 3 data (if exists)
- `lesson-1/outputs/lesson-1-memory.md` — consolidated from Sections 1-4, 10
- `lesson-1/outputs/avoiding-reflections.md` — avoidance patterns data
- `lesson-1/outputs/self-sabotage-answers.md` — self-sabotage data
- `lesson-1/outputs/self-sabotage-methods.md` — self-sabotage methods
- `lesson-1/outputs/hidden-obstacles-report.md` — hidden patterns data
- `lesson-1/outputs/manifesto.md` — from Section 10 (if exists)
- `lesson-1/outputs/vision.md` — from Section 10 (if exists)
- `lesson-1/outputs/behavioral-commitments.md` — from Section 10 (if exists)
- `lesson-1/outputs/profound-questions-answers.md` — from Section 10 (if exists)

**Lesson 2 outputs** (from Sections 5-6):
- `lesson-2/outputs/omniscient-observer-output.md` — from Section 5
- `lesson-2/outputs/omniscient-observer-reflections.md` — from Section 5 reflections
- `lesson-2/outputs/identity-output.md` — Identity Reclamation Protocol
- `lesson-2/outputs/identity-reflections.md` — Identity reflections
- `lesson-2/outputs/shadow-output.md` — Shadow Integration Protocol
- `lesson-2/outputs/shadow-reflections.md` — Shadow reflections
- `lesson-2/outputs/fulfillment-output.md` — Authentic Fulfillment Architecture
- `lesson-2/outputs/fulfillment-reflections.md` — Fulfillment reflections
- `lesson-2/outputs/fear-output.md` — Fear Transmutation Protocol
- `lesson-2/outputs/fear-reflections.md` — Fear reflections
- `lesson-2/outputs/prompt-priority-list.md` — ChatGPT's personalized protocol ordering (if exists)
- `lesson-2/outputs/lesson-2-memory.md` — consolidated from Sections 5-6
- Any optional protocol outputs: success-narrative, legacy-anxiety, success-definition, business-expansion, reality-architect, ifs-guide, socratic-engine, draining-comparisons

**Lesson 3 outputs** (from Section 7):
- `lesson-3/outputs/progress-check-output.md` — 10-domain knowledge assessment
- `lesson-3/outputs/universal-expander-output.md` — archetypal strengths, True Purpose
- `lesson-3/outputs/mentor-council-output.md` — expert panel findings
- `lesson-3/outputs/quantum-leverage-output.md` — daily micro-actions
- `lesson-3/outputs/lesson-3-memory.md` — consolidated from Section 7
- `lesson-3/outputs/active-strength.md` — which strength was chosen
- `lesson-3/outputs/l35-strength-deep-dive.md` — tactical mastery guide (if completed)
- `lesson-3/outputs/l35-sovereign-activation.md` — activation protocol (if completed)
- `lesson-3/outputs/l35-deep-research-prompts.md` — research prompts (if completed)
- `lesson-3/outputs/l35-mastery-accelerator.md` — leaders/experiments/prompts (if completed)
- `lesson-3/outputs/l35-integration-engine.md` — business integration plan (if completed)
- `lesson-3/outputs/l35-proximity-architect.md` — local opportunities (if completed)

**Lesson 4 outputs** (from Sections 1, 8):
- `lesson-4/outputs/zenith-mirror-score-reset.md` — score reset (if exists)
- `lesson-4/outputs/complete-assessment-output.md` — all framework results
- `lesson-4/outputs/zenith-scorecard.md` — scorecard summary
- `lesson-4/outputs/signature-profile.md` — narrative essence (the big one)
- `lesson-4/outputs/execution-bridge-output.md` — execution framework
- `lesson-4/outputs/power-stack-diagnostic.md` — execution DNA
- `lesson-4/outputs/execution-strategy-phase1.md` through `phase4.md` (if exist)
- `lesson-4/outputs/selected-execution-system.md` — final execution system (if exists)
- `lesson-4/outputs/zenith-shift-report.md` — Zenith Shift Report (if exists)
- `lesson-4/outputs/mentor-letter-output.md` — mentor letter (if exists)
- `lesson-4/outputs/hypnosis-script.md` — hypnosis script (if exists)
- `lesson-4/outputs/life-manual.md` — Life Manual (if exists)

**ONLY create files where actual data was found.** Do NOT create empty files or files with just "No data."

---

## Phase 6: Quality Assessment

For each file created, assess data quality:
- **FULL** — substantial data, enough to build on without re-running the exercise
- **PARTIAL** — some data but key details missing — flag for potential re-run
- **THIN** — only surface-level data — recommend re-running this exercise

---

## Phase 7: Set Up Progress

1. Create/update `session-progress.md` with migrated status
2. Add `**Migration source:** ChatGPT data export` and `**Migration date:** [date]`
3. Set current lesson based on what data exists:
   - L4 data exists → post-L4
   - L3 data but no L4 → start at L4
   - L1-2 data only → start at L3
   - L1 data only → start at L2
4. Calculate initial Zenith Mirror Score from migrated data

---

## Phase 8: Report to User

```
Migration complete. Here's what came over from your ChatGPT history:

✓ [FULL] Personality profile — [X] frameworks imported
✓ [FULL] God Prompt findings — all [N] God Prompts captured
✓ [PARTIAL] Calibration data — responses found but not all verbatim
✓ [FULL] Hidden patterns & fears — [X] patterns identified
...etc for each section with data...

[If any sections had no data]: These sections had no data in your ChatGPT history: [list]. That's fine — we can build them as you continue.

[If any THIN files]: A few areas came through light — [list]. I can work with what we have, or we can re-run those specific exercises for deeper data. Your call.

Your Zenith Mirror Score starts at [X].

Ready to pick up where you left off?
```

---

## Fallback: Prompt Method

If the data export isn't working (email never arrives, export keeps failing), there's a fallback:

1. Tell the user: "The data export from ChatGPT isn't cooperating. No problem — I have a backup method. Go to your ChatGPT ZenithMind conversation and paste the prompt I'm about to give you. ChatGPT will write out everything it remembers and give you a downloadable file. Bring that file back here."

2. Paste this prompt to the user (they paste it into ChatGPT):

---
I need you to write out everything you know about me from our ZenithMind work. Go through your memory and this conversation. Use the sections below as a checklist — for each one, write out whatever you have. If you don't have anything for a section, write "No data" and keep going. Don't explain what you can or can't access — just write out what you have. Start now.

**SECTION 1: PERSONALITY PROFILE — EVERY FRAMEWORK**
- Every personality framework result you have for me — include the SPECIFIC type, score, or category for each (MBTI, Enneagram, Big Five/OCEAN, Kolbe A Index, DISC, Attachment style, Love languages, Conflict style, Chronotype, Motivational drivers, Core values, Flow state indicators, any other framework)
- For each framework: state the result, your confidence level (low/medium/high), and whether it came from formal assessment, direct statement, or inference

**SECTION 2: GOD PROMPT FINDINGS — COMPLETE DATA**
Reproduce the complete output from God Prompt 1, 2, and 3 as closely as you can — every finding, every pattern, every insight. Include key themes, breakthrough moments, and my reflections/reactions.

**SECTION 3: CALIBRATION & DEVELOPMENTAL DATA**
My calibration responses, comprehensive summaries, Subject-Object assessment, developmental chart, Lesson 1 Memory summary, and memory verification output.

**SECTION 4: SELF-KNOWLEDGE & HIDDEN PATTERNS**
Every fear, self-deception pattern, avoidance pattern, self-sabotage behavior, limiting belief, blind spot, defense mechanism, and Hidden Obstacles Report finding.

**SECTION 5: OMNISCIENT OBSERVER — COMPLETE FINDINGS**
Full output, every challenged belief, every exposed pattern, my reactions and reflections.

**SECTION 6: LESSON 2 PROTOCOLS — ALL OF THEM**
For every protocol completed: the full output AND my reflections. Cover all must-do and optional protocols.

**SECTION 7: EXPANSION & IDENTITY (Lesson 3)**
Progress Check, Universal Expander, Mentor Council, Quantum Leverage, all strength and identity work completed.

**SECTION 8: EXECUTION DNA (Lesson 4)**
Complete Assessment Generator, Scorecard, Signature Profile, Execution Bridge, Power Stack Diagnostic, all execution strategies, and any completed life tools.

**SECTION 9: ZENITH MIRROR SCORE — FULL HISTORY**
Current score and every score received throughout the program with what drove each change.

**SECTION 10: VALUES, VISION & COMMITMENTS**
Core values, personal manifesto, long-term vision, behavioral commitments, and profound questions with my exact answers.

**SECTION 11: MY ACTUAL WORDS & STORIES**
Personal stories, direct quotes, emotional moments, things I pushed back on or initially denied.

**SECTION 12: PATTERNS & SYNTHESIS**
Recurring themes, contradictions, biggest breakthroughs, single most important insight, how I changed from start to finish.

**SECTION 13: EVERYTHING ELSE**
Everything in your memory about me that doesn't fit above — communication style, personal details, which lessons I completed.

Be as detailed and specific as possible. Use my actual words where you remember them. Include everything — length is not a concern.

When you're done, save the entire output as a downloadable file. Try a .txt file first using Code Interpreter. If unavailable, use PDF or any format that produces a downloadable file. Name it ZenithMind-Export. After creating the file, tell me to download it, then go back to my ZenithMind OS session in Claude and say "I have my ChatGPT export — the file is in my Downloads."
---

3. ChatGPT might explain what it can and can't access — tell the user to reply: "Yes, go ahead and give me as close to a complete export as you can"
4. ChatGPT creates a downloadable file — user saves it and brings it back to Claude
5. Process the export file using the same Phase 5-8 pipeline above

---

## Edge Cases

- **Massive export (1000+ conversations):** ZenithMind conversations are a tiny fraction. The keyword search in Phase 3 filters efficiently — only matching conversations get full processing.
- **Multiple ZenithMind threads:** User may have done ZenithMind across several ChatGPT conversations. The keyword search catches all of them. Merge data chronologically.
- **ZenithMind data mixed into non-ZenithMind conversations:** The secondary keyword threshold (3+ matches) handles this — casual mentions of "MBTI" in a random chat won't trigger, but a calibration session will.
- **No ZenithMind conversations found:** Tell the user: "I searched your entire ChatGPT history and couldn't find any ZenithMind conversations. Are you sure this is the right ChatGPT account? If you used a different account, export from that one instead."
- **Export zip is very large (100+ MB):** Process in chunks. Only fully parse conversations that match the keyword search — skip the rest entirely.
