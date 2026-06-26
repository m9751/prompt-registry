---
id: PRM-PRES-002
title: MuleSoft Gem Slide Handoff
domain: presentation
source_format: Freeform Claude session transcript (discovery notes, engineering docs, proposal content)
target_orchestrator: Claude (Claude Code / Advanced Chat)
downstream_consumer: Human — pastes Discovery Brief into MuleSoft Master Deck Inventory Gemini Gem, then pastes Gem output into Apps Script shell deck generator at line 10; optionally receives Population Guide from Claude to fill placeholders manually in Google Slides
version: 1.0.0
last_updated: 2026-06-06
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/presentation/PRM-PRES-002_mulesoft-gem-slide-handoff.md
use_for: At the end of any customer discovery or engineering session, synthesize the full session into a dense Discovery Brief for the MuleSoft Master Deck Inventory Gem, then optionally generate a slide-by-slide Population Guide once the Gem returns its layout selections
---

## Overview

Runs in two stages from a single prompt, with a YES/NO gate between them.

**Stage 1:** Synthesizes session content into a 200–350 word Discovery Brief — dense, factual prose formatted for direct input into the MuleSoft Master Deck Inventory Gemini Gem. Ends with a `SLIDE BUILDER READY` gate.

**Stage 2 (triggered by YES + Gem output):** Generates a slide-by-slide Population Guide mapping real session content to each slide slot returned by the Gem. Fires immediately in the same thread — no second prompt needed.

Workflow:
1. Paste prompt into Claude at end of session → get Discovery Brief
2. Paste brief into Gemini Gem → Gem outputs `var gemResponseText = \`{...}\`;`
3. Paste Apps Script line at line 10 of shell deck generator → run → shell deck built
4. Return to Claude, paste Gem output, type YES → get Population Guide
5. Open shell deck in Google Slides → use guide to fill placeholders

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory checklist.*

```
We have finished our session. I now need to take everything we discussed
and feed it into our MuleSoft slide builder.

Act as a Discovery Brief Writer. Synthesize everything from our conversation
into a dense, factual discovery brief — written as if you are a senior
Solutions Architect handing off notes to a colleague before a presentation
build session.

Format rules:
- Write in tight, flowing prose. No bullet lists. No headers. No sections.
- Pack in every business objective, system name, integration gap, process
  pain point, technical requirement, and proposed workflow we discussed.
- Include specific product names, API names, platform names, and status
  details exactly as we discussed them.
- Include any build status, blockers, next steps, or customer asks.
- Keep it to 200–350 words. Dense and specific beats long and vague.
- Do not add introductions, conclusions, or commentary.
  Just output the brief, nothing else.

AFTER outputting the brief, you will wait. If I paste a Gemini Gem response
and type YES, immediately produce a slide-by-slide Population Guide using
the Gem's JSON and our session content (see Population Guide rules below).
If I type NO, acknowledge and end.

POPULATION GUIDE RULES (fire only on YES):
For each slide in the Gem's layoutsToFind array, output a block:

SLIDE [N] — [Layout name]
  [Slot]: [Exact text — real facts from our session only]
  NOTE: [Only if something is tricky — otherwise omit]

Slot size limits:
  Title: 6 words max | Subtitle: 10 words max | Card header: 4 words max
  Card body: 2 sentences max | Table header: 3 words max
  Table body: 1 sentence max | Timeline quarter: 2–3 bullet fragments
  Next step: 1 action sentence | Architecture layer: system names only

For the architecture diagram slide (How [Customer] Drives Efficiency):
  List system names per layer only. Do not describe positions or coordinates.
  Note that placeholder boxes must be replaced manually in Google Slides.

Output nothing outside the guide blocks. No intro. No commentary.

This brief will be pasted directly into a Gemini Gem that will:
1. Select 3–6 slide layouts from the MuleSoft Master Deck
2. Extract business and technical terms into a Word Pool
3. Output a single JavaScript variable line ready for Apps Script

Write the brief now. Then, on a new line after the brief, output exactly this:

---
SLIDE BUILDER READY.

Take the brief above and paste it into the MuleSoft Master Deck Inventory Gem.
When Gemini responds, paste its full output below and type YES to get your
Population Guide. Type NO to end here.

Before finishing, verify your output against each of these:
- Did I include all required Discovery Brief sections?
- Did I capture customer pain points and technical environment from the session?
- If the Gem returned layout selections, did I produce the Population Guide?
Correct any failures silently and output only the corrected result.
```
