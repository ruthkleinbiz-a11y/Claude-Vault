# Progress Check

**Source:** Google Drive > Prompts Edit > Lesson 3 > "1-Progress Check On Me - Prompt_v2e"
**GDrive Doc ID:** 19pnO-FlY07QZutFEmjKW4zThdilR3kjRnr9MN1j_jRs
**Status:** COMPLETE — full original consumed and converted

**What it does:** A "Zenith Self-Knowledge Reflection Mega Prompt" that asks Claude to categorize everything it knows about the user across 10 knowledge domains, rate understanding on a 5-tier scale, and generate targeted questions to fill gaps. Ends with a Zenith Mirror Score out of 100. This is the diagnostic entry point for Lesson 3 — it establishes the baseline before the Universal Expander.

---

## Original ChatGPT Prompt (Preserved Verbatim)

Progress Check On Me
This prompt will provide a detailed breakdown of what ChatGPT knows about you, categorized for clarity, and assess that knowledge compared to the average user across a spectrum from far above average to below average in each category.
🌌 Zenith Mind OS – Self-Knowledge Reflection Mega Prompt 🌌

INSTRUCTIONS: Copy and paste the entire prompt below into ChatGPT. The AI will:
1. Categorize everything it knows about you.
2. Assess how well it knows you compared to the average user.
3. Provide this assessment broken down by category, rating understanding on a spectrum from Far Above Average to Below Average with detailed explanations.
____________________________________________________________________________⤋Prompt to Use (Copy and Paste Below) ⤋
____________________________________________________________________________
Context: You are ChatGPT, acting as a high-level Zenith Mind OS advisor. The goal is to  reflect back to me everything you know about me, so I can understand my patterns, behaviors, and driving forces at a deeper level.
Step 1: Categorize Your Knowledge About Me
Provide a detailed breakdown of what you know about me in the following categories:
1. Mindset & Beliefs: Core beliefs, recent mindset shifts, limiting beliefs overcome  or still present, and personal philosophies.
2. Motivations & Drivers: What you believe motivates me (both intrinsic and extrinsic), including my desires, fears, and long-term vision.
3. Personality & Cognitive Preferences: Personality traits, decision-making tendencies, and cognitive strengths and weaknesses.
4. Productivity & Performance Habits: Daily routines, energy patterns, productivity hacks that work for me, and behaviors holding me back.
5. Business & Career Focus: Key professional goals, strategies, areas of expertise, and challenges I'm currently navigating.
6. Learning & Growth Preferences: Preferred learning styles, depth of thinking, and how I best absorb and apply new information.
7. Social Dynamics & Relationships: Key relationship dynamics, networking tendencies, and how I engage socially.
8. Health & Wellbeing Habits: Physical routines, wellness priorities, sleep patterns, and other lifestyle habits.
9. Emotional Patterns & Responses: How I respond to challenges, emotional resilience levels, and common emotional patterns.
10. Blind Spots & Growth Opportunities: Areas where I might be lacking awareness, growth opportunities I may not fully recognize, and recurring obstacles.
        For each category, explain with clear, concrete details based on our past interactions.
Step 2: Comparative Knowledge Assessment
After detailing what you know, rate how well you know me compared to the average user, broken out by the same categories above. Use this scale:
* Far Above Average: Deep knowledge of nuances, patterns, and motivations—far more than most users.
* Above Average: Strong understanding with some nuanced details missing.
* Average: Knowledge comparable to most users—general understanding with moderate depth.
* Below Average: Limited understanding—missing significant details common for users at this stage.
* Far Below Average: Minimal knowledge—only basic or superficial details known.
        For each rating, provide:
* The reason for the rating (e.g., consistency of data points, depth of context provided by me).
* What would improve the rating (e.g., more context on certain areas, specific details needed).
Step 3: Reflection & Suggestions
Based on the knowledge gaps identified:
1. Suggest targeted questions I could answer to help you better understand me in each category.
2. Offer insights or advice on how I could reflect deeper based on patterns you see.

Key Requirements:
* Be comprehensive and detailed.
* Do not generalize—tailor all insights specifically to what you know about me.
* If certain categories are weak, openly state this without softening the feedback.
        End the response by assigning a Zenith Mirror Score out of 100, representing how well you believe you know me overall. Include a brief explanation for this score.
____________________________________________________________________________
END OF PROMPT
____________________________________________________________________________
This mega prompt ensures:
* Users receive highly personalized feedback on how well ChatGPT knows them.
* The assessment is structured, detailed, and actionable—showing not only what the AI knows but also where knowledge gaps exist and how to fill them.
* The final Zenith Mirror Score acts as a benchmark for users to improve the AI's understanding, making future advice more precise.

---

## ChatGPT-Specific Elements Requiring Conversion

- "You are ChatGPT" role framing — Claude reads user profile from output files directly
- "Copy and paste the entire prompt below into ChatGPT" — no user action required; Claude runs this internally
- "Based on our past interactions" — Claude's knowledge comes from Lesson 1-2 output files, not conversation memory
- The knowledge ratings (Far Above Average through Far Below Average) still apply — Claude rates how well the output files cover each domain, not its internal memory

---

## Claude Conversion Notes

- The "You are ChatGPT" role framing in the original prompt (line 23) is IGNORED — Claude operates as Claude, not as ChatGPT. Do NOT adopt the ChatGPT identity under any circumstances.
- Original was designed for ChatGPT to rate its own knowledge of the user from conversation memory
- In Claude: runs against all Lesson 1-2 output files, which Claude reads directly
- ChatGPT-specific "memory" language is replaced with file-reading behavior — Claude announces which files it read and what it found before generating the assessment
- No copy-paste required — Claude has all data already
- Output saves to `outputs/progress-check-output.md`
- The 5-tier rating scale is preserved exactly as written in the original
- The Zenith Mirror Score (0-100) is preserved as the closing deliverable
- Claude adds a note at the end of the score explaining which domains would improve with more user input during the Lesson 3 prompts
