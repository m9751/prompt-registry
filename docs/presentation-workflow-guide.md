---
id: PRM-GEM-001
title: MuleSoft Slide Briefing — Claude-to-Gem Handoff Prompt
domain: presentation
version: 4.0.0
last_updated: 2026-06-06
use_for: After finishing any customer discovery session or engineering document with Claude, run this prompt to produce a dense discovery brief. Paste that brief directly into the MuleSoft Master Deck Inventory Gem. Gem outputs the Apps Script line. Paste at line 10 of the shell deck generator. Run. Deck is built.
---

## Workflow

```
You + Claude  →  discovery / engineering / proposal session
     ↓
Paste THE PROMPT below into the same Claude session
     ↓
Claude outputs a dense Discovery Brief (unstructured prose)
     ↓
Paste that brief into Gemini Gem (MULESOFT MASTER DECK INVENTORY)
     ↓
Gem outputs:  var gemResponseText = `{...}`;
     ↓
Paste that line at line 10 of the Apps Script shell deck generator
     ↓
Run script → shell deck is built in Google Drive
```

---

## THE PROMPT
### Paste this into Claude at the end of your session:

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
```

---

## WHAT THE GEM DOES WITH THE BRIEF

The Gem (MULESOFT MASTER DECK INVENTORY) reads the brief and:

1. Selects `layoutsToFind` — 3–6 slide names from the master deck that fit the story
2. Extracts `extractedTerms` — categorizes key terms into `Core_Objectives`, `Current_Systems`, `Technical_Gaps`, `Process_Breakdowns`
3. Outputs this exact format, ready to paste at **line 10** of the Apps Script:

```
var gemResponseText = `{"layoutsToFind":[...],"extractedTerms":{...}}`;
```

---

## TIPS

- **More session context = better Gem output.** The brief works best when our Claude session covered discovery, architecture, and build status together.
- **If the Gem picks wrong layouts**, the reference table below shows what layouts exist and what triggers them. You can tell the Gem "replace X with Y" and re-run.
- **The Gem's fallback** (if your brief is thin): `"Title, single line"` and `"Cards - Two up"` — always safe defaults.

---

## LAYOUT REFERENCE — WHAT THE GEM CAN PICK

| Content type | Layout name the Gem will use |
|---|---|
| Cover slide | `Title of presentation` |
| Agenda | `Agenda` |
| Single column narrative | `Title, single line` |
| Two column split | `Title, two columns` |
| Three column split | `Title, three columns` |
| Large single card | `Card large` / `Card XL` |
| Two cards | `Cards - Two up` |
| Three cards / three pillars | `Cards - Three up` |
| Four cards | `Cards - Four up` |
| Five cards | `Cards - Five up` |
| Six cards (boxes) | `Cards - Six up boxes` |
| Next steps / action items | `Reflections / Next Steps` |
| MuleSoft 3-layer architecture | `How [Customer] Drives Efficiency` |
| Stats with radial | `Stat callouts` |
| Timeline by quarter | `Timeline - Quarters` |
| Event calendar | `Calendar` |
| Action items table | `Table - Action Items` |
| Table cards no subhead | `Table Cards - Headline Only` |
| Table cards with subhead | `Table Cards - with Subhead` |
| Bold statement / segue | `Bold statement that can span multiple lines` |
| Segue / transition | `Segue` |
| Big stat left | `This is a big stat slide` |
| Image right layout | `Image right, two lines` |

---

## PART 2 — POPULATION GUIDE PROMPT
### Run this in the SAME Claude session, immediately after the Discovery Brief

```
The Gemini Gem has returned the following slide selections:

[PASTE GEM OUTPUT HERE — the full var gemResponseText = `{...}`; line]

Now act as a Slide Population Strategist. Using everything from our session,
produce a Population Guide — a slide-by-slide cheat sheet I can use to fill
in the placeholder text in the shell deck manually in Google Slides.

For each slide the Gem selected, output a block in this format:

SLIDE [N] — [Layout name]
  [Slot name]: [Exact text to type]
  [Slot name]: [Exact text to type]
  ...
  NOTE: [One sentence on anything tricky about this slide — or omit if straightforward]

Rules:
- Use only real facts from our session. No invented content.
- Keep all text short enough to fit the slide — use the slot size hints below.
- For the architecture diagram slide, list what goes in each layer by name only.
  Do not try to describe coordinates or positions.
- For timeline slides, assign content to quarters based on actual build sequence.
- For card slides, give each card a bold header (3–5 words) and a body (1–2 sentences max).
- For table slides, give each row a header and a short description.
- For next steps slides, give each numbered item a single action sentence.
- Output nothing else. No intro. No commentary. Just the guide.

SLOT SIZE HINTS (keep text within these limits):
  Slide title:      6 words max
  Subtitle:         10 words max
  Card header:      4 words max
  Card body:        2 sentences max
  Table header:     3 words max
  Table body:       1 sentence max
  Timeline quarter: 2–3 bullet fragments max
  Next step item:   1 action sentence
  Architecture layer: comma-separated system names only

Write the Population Guide now.
```

---

## POPULATION GUIDE — CROSSROADS EXAMPLE OUTPUT
### What the guide looks like when it comes back (reference only)

```
SLIDE 1 — How [Customer] Drives Efficiency With API-led Connectivity
  Title:           How Crossroads Drives Efficiency With API-led Connectivity
  Experience layer: crossroads-hc-xapi (To Build)
  Process layer:   crossroads-hc-papi, Scheduling Write-Back
  System layer:    medgen-fhir-sys-api
  Source:          MedGen EHR
  NOTE: This slide uses placeholder boxes — replace each "Placeholder" label
        by clicking the text box and typing the system name directly in Google Slides.

SLIDE 2 — Cards - Three up
  Subtitle:        Where MuleSoft Connects Crossroads
  Card 1 header:   Census Growth
  Card 1 body:     Patient attribution gaps block the referral loop. MuleSoft
                   unifies acquisition signals across 11 disconnected systems.
  Card 2 header:   Scheduling Write-Back
  Card 2 body:     Cancel and reschedule flows are built and wired. One MedGen
                   API document away from going live.
  Card 3 header:   Platform Consolidation
  Card 3 body:     No persistent patient ID across MedGen, Salesforce, Care Logic,
                   Talkdesk, and PowerBI. MuleSoft creates the single source of truth.
  Footer:          MuleSoft Healthcare — Crossroads Treatment Centers

SLIDE 3 — Table Cards - Headline Only
  Label A:         Built & Tested
  Label B:         Blocked / Pending
  Row 1 header:    medgen-fhir-sys-api
  Row 1 body:      12 FHIR R4 flows. Deployed on CloudHub. Tested against HAPI.
  Row 1 label:     A
  Row 2 header:    crossroads-hc-papi
  Row 2 body:      Patient 360 + Available Slots. Running on CloudHub.
  Row 2 label:     A
  Row 3 header:    Scheduling Write-Back
  Row 3 body:      Cancel + Reschedule flows built. Awaiting MedGen API docs.
  Row 3 label:     B
  Row 4 header:    crossroads-hc-xapi
  Row 4 body:      Experience API not yet started. Planned for Phase 3.
  Row 4 label:     B

SLIDE 4 — Timeline - Quarters
  Subtitle:        Integration Delivery Sequence
  Q1:              medgen-fhir-sys-api deployed · HAPI tested · 12 FHIR flows live
  Q2:              crossroads-hc-papi live · Patient 360 · Available Slots running
  Q3:              MedGen shares scheduling docs · Cancel + Reschedule go live
  Q4:              crossroads-hc-xapi built · Agentforce connected · Health Cloud wired

SLIDE 5 — Reflections / Next Steps
  Item 1:          MedGen shares scheduling API documentation
  Item 2:          Validate Patient 360 against live MedGen credentials
  Item 3:          Crossroads confirms Agentforce scope for Phase 3
  Item 4:          MuleSoft deploys crossroads-hc-xapi experience layer
```

---

## Future: Full Automation via Apps Script Web App

**Status: Parked — not built. Validate Salesforce workspace permissions before pursuing.**

The current workflow requires one manual step: copying the Gem's `var gemResponseText` line and pasting it into the Apps Script editor. This step can be eliminated entirely.

**The idea:** Deploy the Apps Script as a Web App (`doPost` endpoint). Claude or any external trigger POSTs the Gem's JSON directly to that endpoint. The script runs automatically and the shell deck appears in Google Drive — no copy-paste, no editor, no manual step.

**Full automated loop:**
```
Claude outputs Discovery Brief
     ↓
Gem processes it → outputs JSON string
     ↓
Claude POSTs JSON to Apps Script Web App endpoint
     ↓
Shell deck appears in Google Drive automatically
```

**What needs to change in the Apps Script:**
- Replace the hardcoded `var gemResponseText = ...` at line 10 with a `doPost(e)` receiver that reads the JSON from the POST body
- Add a `doGet()` health check function so the endpoint can be verified in a browser
- Redeploy as a Web App (Deploy → New deployment → Web app → Execute as: Me → Who has access: Anyone)

**The blocker to investigate first:**
Salesforce enterprise Google Workspace accounts restrict "Anyone" access to mean "anyone inside Salesforce." If that restriction is in place, an external POST (from Claude, a Python script, or any unauthenticated caller) will be blocked by Google at the org level. Test by opening the deployment URL in an Incognito tab — if it prompts for Google login, the org is locked down.

If locked down: the alternative is the official Google Apps Script API with OAuth, which is significantly more complex and likely not worth it for this use case. Keep the manual paste step instead.

**When to pick this back up:** After the current workflow has been used on 2–3 real accounts and the manual step is confirmed to be the actual friction point.
