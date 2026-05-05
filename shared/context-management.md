# Context Management Protocol

## When to Trigger
When the conversation is getting long (rough signals: 40+ back-and-forth exchanges, or you've loaded 5+ files in the current session, or you're about to generate a Mirror Prompt report after a full calibration).

---

## Conversational Save (MANDATORY — Prevents Data Loss)

**Problem this solves:** Users sometimes explore, ask questions, go deep on a topic, or have extended discussions without completing a formal step. If they close the session, ALL of that conversational work is lost — Claude Code does not carry conversation history between sessions. Only what's written to files survives.

### When to Fire
- **Every ~15 back-and-forth exchanges** where no step has been completed since the last save
- **When the user shares something significant** — a personal insight, an emotional revelation, a decision, a realization about themselves — that isn't part of a formal step output
- **When the conversation shifts to freeform exploration** — the user asks follow-up questions, goes off-script, or digs deeper into a topic outside the step sequence
- **Before any natural pause** — when Claude is about to ask a complex question, present options, or transition topics

### What to Save
Append a timestamped entry to `lesson-[N]/outputs/conversation-notes.md` (create the file if it doesn't exist):

```markdown
## [Date and time]

**Context:** [What lesson/step the user is on or near]
**Discussion summary:** [2-5 sentences capturing what was discussed — specific topics, questions asked, insights shared]
**Key insights from the user:** [Direct quotes or paraphrases of anything personally significant the user said]
**Decisions or preferences expressed:** [Anything the user decided, chose, or expressed a preference about]
**Where the conversation was heading:** [What was about to happen next]
```

### Rules
- **Append-only.** Never overwrite previous entries. Each save adds a new timestamped block.
- **Be specific.** "User discussed their career" is useless. "User explained that they left corporate law because the prestige stopped mattering after their daughter was born — realized they were optimizing for other people's scorecards" is valuable.
- **Capture the user's language.** When they say something vivid or emotionally charged, quote it directly.
- **Don't announce every save.** The first time in a session, briefly mention it: "By the way — I'm saving notes from our conversation as we go, so nothing gets lost if you need to step away." After that, save silently.
- **If the user asks "what did we talk about last time?"** — read `conversation-notes.md` FIRST (before step outputs). This is where freeform discussion lives.

### On Session Start (Addition to Loading Protocol)
When loading a returning user's state, also check for `lesson-[N]/outputs/conversation-notes.md`. If it exists:
- Read the most recent entry
- Use it for felt continuity alongside step outputs — reference something specific from the conversation, not just the formal step progress
- If the last conversation-notes entry shows the user was mid-discussion on something, acknowledge it: "Last time we were talking about [topic] — want to pick that back up, or move forward with the next step?"

---

## Mid-Session Save
1. Write current state to root `session-progress.md` (lesson, step, score, key context)
2. Write any unsaved outputs to the lesson's `outputs/` folder
3. **Write a conversation-notes entry** if there's been any discussion since the last save
4. Tell the user: "Good stopping point. Everything's saved — when you come back, I'll pick up exactly where we left off."

---

## Pre-Generation Check
Before generating any large output (Mirror Prompts, Assessment Reports, Life Manual sections, Omniscient Observer):
1. Confirm the key input files are loaded (calibration responses, prior reports)
2. If you need to load more than 3 files for a single generation step, load them sequentially — read file, extract what you need, note the key points, then move to the next file
3. Write the output to the appropriate file IMMEDIATELY after generating

---

## Output File Discipline
- After generating and saving a large output, the content now lives in the file
- Do not re-quote or re-summarize the full output in conversation
- Reference it by filename: "Your Mirror Prompt 1 report is saved in outputs/mirror-prompt-1-output.md — want to go through the reflection process?"

---

## Cross-Lesson References
When a step requires data from prior lessons:
- Load the lesson's memory file (`lesson-N-memory.md`) FIRST — this is the consolidated summary
- Only load specific raw output files if the memory file doesn't contain what you need
- NEVER load all of a prior lesson's outputs at once
