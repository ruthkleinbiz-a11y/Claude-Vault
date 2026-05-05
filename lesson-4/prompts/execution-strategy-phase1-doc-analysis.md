# Execution Strategy Generator — Phase 1: Multi-Pass Document Analysis

**Source:** GDrive `1eg_KxOOeg6Lo7XWPh54AzKcNLJCQW0wS6wtDhEsUyhE` (standalone Phase 1 doc) + L4 Starter Guide (58 pages, fully consumed — Phase 1 structure documented)
**Status:** COMPLETE — full original consumed and converted
**Lesson 4 role:** Phase 1 of 5 in the Personalized Execution Strategies Generator (Step 6 of main flow)

---

## What This Does

Phase 1 of the 5-phase Personalized Execution Strategy Generator. Performs five systematic passes through all prior lesson documents, each pass centered on a different document as the primary analytical lens. Each pass extracts key elements from the primary document and cross-references them against ALL other documents.

**ChatGPT vs. Claude:** In ChatGPT, the user had to manually upload documents to Phase 1 and then copy Phase 1's output to paste into Phase 2. In Claude, this phase reads all prior lesson output files automatically and saves its output to `outputs/execution-strategy-phase1.md` — which Phase 2 reads automatically.

---

## Original ChatGPT Prompt (Preserved Verbatim)

Phase 1 Prompt
Multi-Pass Document Analysis
____________________________________________________________________________⤋Prompt to Use (Copy and Paste Below) ⤋
____________________________________________________________________________


# PHASE 1: MULTI-PASS DOCUMENT ANALYSIS


Perform five systematic passes through all my documents, with each pass focused on a different document as the primary lens:


PASS 1: MIRROR PROMPT-CENTERED ANALYSIS
1. Thoroughly analyze the Mirror Prompt document to extract:
   - Hidden narratives and unexpressed fears
   - Core psychological patterns
   - Personal strengths (explicit and implicit)
   - Resistance mechanisms
   - Key language, metaphors, and themes


2. Then examine ALL other documents specifically looking for:
   - Additional information about these Mirror Prompt elements
   - Confirmations, contradictions, or expansions of these patterns
   - Document where each insight appeared


PASS 2: OMNISCIENT OBSERVER-CENTERED ANALYSIS
1. Thoroughly analyze the Omniscient Observer document to extract:
   - Shadow aspects and their gifts
   - Identity structure limitations
   - Self-sabotage sequences
   - Unclaimed capacities and forms of genius
   - Core paradoxes and contradictions


2. Then examine ALL other documents for related insights


PASS 3: UNIVERSAL EXPANDER-CENTERED ANALYSIS
1. Thoroughly analyze the Universal Expander document to extract:
   - Extraordinary capacities awaiting activation
   - Transcendent purpose
   - Ways I've been playing small
   - Vision of my 10X life
   - Expanded self-concept details


2. Then examine ALL other documents for related insights


PASS 4: PERFORMANCE AT PEAK-CENTERED ANALYSIS
1. Thoroughly analyze the Performance at Peak document to extract:
   - Frameworks created by the expert team
   - Specific recommendations and action steps
   - Resources mentioned
   - Strengths highlighted by experts


2. Then examine ALL other documents for related insights


PASS 5: QUANTUM LEVERAGE CODEX-CENTERED ANALYSIS
1. Thoroughly analyze the Quantum Leverage Codex document to extract:
   - Minimal actions with maximal impact
   - Momentum matrix connections
   - Resistance dissolution protocols
   - Identity evolution framework


2. Then examine ALL other documents for related insights

---

## ChatGPT-Specific Elements Requiring Conversion

- **"Performance at Peak" document (Pass 4)** — In the original, this refers to the Mentor Council output. In Claude, Pass 4 centers on `../lesson-3/outputs/mentor-council-output.md`.
- **Document uploads** — In ChatGPT, the user had to manually upload each document. In Claude, all prior lesson output files are read automatically from the file system.
- **Output handling** — In ChatGPT, the user had to copy Phase 1's output to paste into Phase 2. In Claude, output saves to `outputs/execution-strategy-phase1.md` and Phase 2 reads it automatically.

---

## Claude Behavioral Instructions

**ALWAYS:**
- Read ALL prior lesson output files before beginning any pass
- Complete all 5 passes before producing the synthesis — don't shortcut to synthesis after 2-3 passes
- In each pass: explicitly name the cross-references being made (e.g., "The Mirror Prompt's theme of [X] connects to the Omniscient Observer's observation of [Y]")
- Flag cross-pass themes explicitly — these are the highest-signal patterns for Phase 2
- Save output to `outputs/execution-strategy-phase1.md`
- Inform the user when Phase 1 is complete and Phase 2 is ready

**File mapping for passes:**
- Pass 1: `../lesson-1/outputs/mirror-prompt-1-output.md` (+ mirror-prompt-2 and mirror-prompt-3 if they exist)
- Pass 2: `../lesson-2/outputs/omniscient-observer-output.md`
- Pass 3: `../lesson-3/outputs/universal-expander-output.md`
- Pass 4: `../lesson-3/outputs/mentor-council-output.md`
- Pass 5: `../lesson-3/outputs/quantum-leverage-output.md`

**NEVER:**
- Skip passes because documents seem similar
- Combine passes without completing each one's extraction
- Produce generic analysis that doesn't cite specific content from the documents

---

## Output File

`outputs/execution-strategy-phase1.md` — structured analysis from all 5 passes + cross-pass synthesis. This file is read automatically by Phase 2.
