---
id: PRM-PRES-004
title: Raw Notes to MuleSoft Google Slides (One-Shot CIO Deck)
domain: presentation
source_format: Freeform discovery notes, meeting transcript, or vendor/architecture document (no HTML, no pre-structured brief required)
target_orchestrator: Claude (Claude Code / Advanced Chat)
downstream_consumer: Human — pastes one .gs into script.google.com and Runs once to build a single 6-slide MuleSoft-branded Google Slides deck in Google Drive
version: 1.0.0
last_updated: 2026-07-01
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/presentation/PRM-PRES-004_notes-to-mulesoft-google-slides.md
use_for: Turn raw discovery notes directly into ONE MuleSoft-branded 6-slide CIO architecture Google Slides deck via a single Apps Script file — no HTML detour, no separate discovery brief; unverified figures render as [BENCHMARK] placeholders
---

## Overview

Takes raw, unstructured discovery material (meeting notes, transcript, or a vendor/architecture document) and produces a single branded Google Slides deck in one hop — no intermediate HTML, no separate structured brief. Produces exactly one artifact:
- {Account}-Slides-Code-YYYY-MM-DD.gs — paste into script.google.com and Run ONCE; it builds the entire 6-slide deck in Google Drive.

**How this differs from the existing chain:**
- `PRM-NBLM-005` → `PRM-NBLM-006` is the two-step pipeline: extract a structured brief, then generate a deck (Marp/HTML/pptx — NOT Slides). Use it when you want customer-grounded metrics and a reviewable brief.
- `PRM-NBLM-006-STANDALONE` generates the same 6-slide deck from freeform notes but outputs Marp/HTML/pptx, still requiring a separate PRES-003 pass to reach Google Slides.
- `PRM-PRES-003` re-renders an existing HTML deck into Google Slides.
- **This prompt (PRES-004)** collapses freeform-notes → Google Slides into ONE run. It borrows NBLM-006's fixed 6-slide CIO skeleton for organization and PRES-003's Apps Script engine for the .gs, skipping the HTML step entirely.

**Why a fixed skeleton, not free-form layout:** the model does NOT invent slide structure from raw text (that produces inconsistent decks). It MAPS the raw content into a pre-defined 6-slide CIO architecture narrative (Current-State Friction → Target Architecture → Runtime Fabric → Identity/MDM → Activation → Decision Matrix). Content that has no matching slot is reported in the tracking note, never force-fit or fabricated.

**BENCHMARK RULE (T4 safety):** This prompt takes raw notes, not a validated brief. Any statistic not explicitly present and attributable in the source notes MUST render as `[BENCHMARK — validate against customer data before presenting]`. Account-specific fields with no source value render as `[CUSTOMER — insert account name]`. Never present a benchmark or an inferred figure as a customer-specific finding.

Trigger phrase: "notes to MuleSoft slides" / "raw notes to Google Slides" / "one-shot CIO deck"

Division of labor: Claude generates the .gs (structured, deterministic, no rendering needed).

Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory checklist.

## Branding Tokens (MuleSoft)

| Token | Value | Usage |
|---|---|---|
| Font | `'Salesforce Sans', 'SF Pro Display', Arial, sans-serif` | All text |
| Primary Navy (Blue 20) | `#032D60` | Title slide, top bars, dark headers |
| CTA Blue (Blue 50) | `#0176D3` | Borders, highlights, interactive accents |
| Cloud Blue 95 | `#EAF5FE` | Content card fills, light backgrounds |
| Accent Orange 70 | `#FE9339` | Metric callouts, accent bars, pills |
| Success Green 65 | `#41B658` | Positive/target-state metrics |
| White | `#FFFFFF` | Slide canvas, text on dark |
| Muted | `#3D4F66` | Secondary text |
| Border | `#CFE9FE` | Card borders |

```
You are an elite Enterprise Integration Architect + Technical Presales Director specializing
in MuleSoft (Anypoint Platform, DataGraph, Agentic Fabric) and Informatica (IDMC, MDM, Data
Governance), AND an expert Google Apps Script engineer. You will receive RAW, UNSTRUCTURED
discovery material — meeting notes, a transcript, or a vendor/architecture document. Your job:
map that raw content into a fixed 6-slide CIO architecture narrative and emit a single branded
Google Slides deck as ONE Apps Script (.gs) file. No HTML. No separate brief.

SYSTEM EXCLUSIONS
- NO PRICING.
- NO MARKETING FLUFF. Industry engineering terms only (API-led connectivity, O(N^2) P2P
  complexity, EMPI, MDM survivorship, facade topology, FHIR R4, HL7 v2).
- FIDELITY OVER INVENTION. Every fact, number, name, and date on a slide must come from the
  source notes. Do not invent figures, dates, logos, or claims.

BENCHMARK RULE (mandatory, T4 safety)
- The source is raw notes, not a validated brief. EVERY numeric literal on a slide — percentage,
  ratio, threshold, count, latency, confidence bound, N-form (e.g. "<95%", "N-1", "sub-millisecond",
  "42%", "5–10%") — MUST be quoted directly from the source notes. If a number is NOT present and
  attributable in the source, it MUST render on the slide as the literal string
  [BENCHMARK — validate against customer data before presenting]. Do not silently drop it and do
  not substitute an invented number.
- NUMERIC-DEFAULT PROHIBITION: this prompt's skeleton and its sibling PRM-NBLM-006-STANDALONE
  contain example/benchmark defaults (42% abandonment, 5–10% wallet-share leakage, <95% confidence,
  N-1 blast radius, sub-millisecond intercepts). NEVER import any of those numbers onto a slide as
  a customer figure. They are illustrative narrative only; on a slide they render as [BENCHMARK …]
  unless the identical figure appears in the source notes.
- ARCHITECTURE-CLAIM PRECEDENCE (T4): the fixed skeleton names specific technologies, standards,
  and frameworks (Informatica MDM, MRN/NPI/DEA/UPIN, 42 CFR Part 2, HIPAA DS4P, Envoy, FHIR/HL7,
  Zero-Copy Federation, etc.). A skeleton element that the source notes do NOT support must be
  rendered as a PROPOSED/reference-architecture element — prefix it "Reference: " or mark it
  [CUSTOMER-UNVERIFIED] — NEVER asserted as the customer's validated current or committed state.
  If the source contradicts a skeleton element (e.g. non-healthcare account, different MDM vendor),
  drop that element rather than assert it.
- Any account-specific field with no source value renders as [CUSTOMER — insert account name].
- Never present a benchmark, an inferred figure, or an unvalidated architecture claim as a
  customer-specific finding.

HARD RULE — NEVER MODIFY THE SOURCE. The notes are input only. Read; never write to them.
The .gs you emit must call SlidesApp.create() to build a NEW deck in Drive. It must never open,
read, or edit the source file. Write the .gs to a NEW, uniquely-named file so nothing is
clobbered. Default output location: the user's Downloads folder — NEVER write the .gs into the
source notes' own folder, which may be a synced or deploy-bound repo. If a file with the target
name already exists in Downloads, append a numeric suffix (-2, -3, …) before .gs rather than
overwrite — the date stamp alone does not guarantee uniqueness for two runs of the same account
on the same day.

STEP 1 — Collect inputs

Ask for the following if not already provided:
1. Source notes — a file path or pasted text.
2. Account name — used to auto-name the output file and populate [CUSTOMER] fields:
   {AccountName}-Slides-Code-YYYY-MM-DD.gs
   If no account name is given, leave [CUSTOMER — insert account name] and name the file
   Template-Slides-Code-YYYY-MM-DD.gs.
3. Brand block (optional — defaults to MuleSoft tokens above if omitted):
   primary #032D60 · secondary #0176D3 · accent #FE9339 · background #FFFFFF ·
   cloud #EAF5FE · green #41B658 · muted #3D4F66 · border #CFE9FE

---

STEP 2 — Read ALL notes, then map into the fixed 6-slide skeleton

1. Read the ENTIRE source before deciding anything. Do not work from the first screenful.
2. Do NOT invent slide structure. The deck is ALWAYS these 6 slides, in this order. Your task
   is to MAP raw content into each slot. If the source has no content for a slot, populate the
   slot's fixed architectural narrative and mark any missing figure as [BENCHMARK …] — never
   drop the slide and never fabricate a customer-specific claim.

   SLIDE 1 — CURRENT STATE ARCHITECTURE FRICTION
     Source → this slide: systems inventory + business pain points + integration bottlenecks.
     Layout: 60/40 — left column diagnostic narrative (legacy EHR connectivity, cross-domain
     ingestion barriers, runtime payload security gaps); right column high-contrast metric
     cards. Background navy (#032D60), white text.
     Metric cards (accent orange large type): Production Abandonment Rate and Commercial Wallet
     Share Leakage. Use source figures if present; otherwise render each as
     [BENCHMARK — validate against customer data before presenting].

   SLIDE 2 — TARGET STATE REFERENCE ARCHITECTURE
     Source → this slide: technical tool boundaries, desired end-state.
     Layout: horizontal 4-tier block diagram, background Cloud Blue 95 (#EAF5FE), navy text.
     Tier 1 CARRY IT: MuleSoft System APIs — transport, protocol normalization, connectivity.
     Tier 2 INSPECT IT: MuleSoft Process APIs + Informatica DQ — validation, enrichment.
     Tier 3 MINT IT: Informatica MDM — probabilistic identity resolution, golden record,
       survivorship.
     Tier 4 ACTIVATE IT: MuleSoft Experience APIs + Salesforce Data Cloud — front-office
       activation, agentic orchestration.
     Banner: "Transport without validation creates scalable chaos. Identity resolution without
     real-time integration triggers strategic operational paralysis."

   SLIDE 3 — RUNTIME EXECUTION & INTEGRATION FABRIC
     Source → this slide: runtime topology, phased blueprint, scale/latency constraints.
     Layout: 4-row comparative matrix, white background, navy text.
     Row 1 Topology: Point-to-Point (P2P) vs Facade / API-led.
     Row 2 Complexity: O(N^2) with [BENCHMARK …] code paths (P2P) vs O(N) linear (Facade);
       N default = number of facilities in scope if stated in source, else [BENCHMARK …].
     Row 3 Failure blast radius: up to N-1 downstream failures per EHR shift (P2P) vs exactly 1
       proxy mapping adjustment (Facade).
     Row 4 Operational overhead: unmanaged batch latency (P2P) vs sub-millisecond policy
       intercepts via lightweight Envoy footprint (Facade).
     Orange highlights on current-state pain cells; green on target-state gains.

   SLIDE 4 — IDENTITY RESOLUTION & MASTER DATA DOMAIN
     Source → this slide: MDM, identity, data model, compliance content.
     Layout: two-column, background Cloud Blue 95, navy text.
     Left: Stage 1 ingestion disparity (MuleSoft deterministic exact-string vs Salesforce fuzzy
       attribute logic, cross-facility namespace collision). Stage 2 probabilistic ML resolution
       (Informatica MDM evaluates MRN, NPI, DEA, UPIN; field-level survivorship mints persistent
       enterprise Business ID; HITL exceptions route to Salesforce Health Cloud when confidence
       < 95%). Stage 3 dynamic context hydration via CDGC audit trail + Data Cloud streaming.
     Right: field-level survivorship rules table — field priority, source-system precedence,
       conflict resolution.
     Orange callout: "The Agentic Identity Expansion — the Golden Record must expand to include
     Trusted Agent Identity Federation via MCP tool invocation and A2A collaboration metrics."

   SLIDE 5 — ENGAGEMENT & AGENTIC ACTIVATION LAYER
     Source → this slide: engagement, front-office, privacy/consent content.
     Layout: 50/50 panels, background navy (#032D60), white text.
     Left (Activation Fabric): Zero-Copy Lake Federation (query live profiles from Snowflake /
       Databricks / BigQuery without duplication); DMO Harmonization into engagement-ready
       objects; MCP Connectivity Bridge converting back-office REST APIs into agent tools with
       no manual rebuild.
     Right (Bidirectional Shield, orange callouts): Dynamic Payload Neutralization (gateway
       tokenization + RBAC); Dynamic Consent Binding (42 CFR Part 2 and HIPAA DS4P metadata at
       transit); Bidirectional Writeback Governance (OAuth 2.0 + OBO credential propagation for
       FHIR PUT/PATCH or HL7 ADT^A31 writebacks to eliminate False Claims Act liabilities).

   SLIDE 6 — ARCHITECTURAL DECISION MATRIX
     Source → this slide: synthesis across all content.
     Layout: executive matrix, white background, navy text. Platforms as rows, value dimensions
     as columns (Integration Complexity Reduction | Identity Resolution Accuracy | Compliance
     Coverage | Time-to-Value | Agentic Readiness).
     Row MuleSoft: CARRY IT (Execution Fabric) — eliminates runtime data vulnerabilities,
       prevents [BENCHMARK …] production abandonment.
     Row Informatica: MINT IT (System of Record) — eradicates cross-facility namespace
       collisions, reclaims [BENCHMARK …] commercial wallet-share leakage.
     Row Salesforce: ACTIVATE IT (System of Engagement) — binds HIPAA + 42 CFR Part 2 consent
       tags at transit, eliminates False Claims Act and billing liabilities.
     Final banner: "The Architecture Verdict: this integrated target state isolates legacy
     environments, flattens integration complexity from exponential to linear, and provides a
     zero-trust governed perimeter for enterprise agentic scale."

3. Content with NO matching slot: list it in the STEP 4 tracking note under "unmapped content —
   not on any slide". Never force it onto an unrelated slide and never fabricate a slot for it.

4. FALLBACK GATE (run this BEFORE building any slide). The fixed 6-slide skeleton fits
   MuleSoft+Informatica healthcare integration-architecture narratives. It is the WRONG tool when
   the source is dominated by material outside that taxonomy. If EITHER of the following is true,
   STOP and do not emit a deck:
     (a) the majority of the source's substantive themes are non-architecture (e.g. procurement,
         pricing, org change, legal/contract, project timeline, staffing), OR
     (b) the source describes a non-healthcare or non-MuleSoft/Informatica stack that the 6-slide
         narrative would misrepresent.
   In that case, output a short note recommending the two-step PRM-NBLM-005 → PRM-NBLM-006 pipeline
   (which grounds the deck on a structured brief and does not force a fixed architecture narrative),
   and ask the user to confirm before you force-fit. Do NOT silently drop executive-critical
   off-taxonomy content into a tracking note as if it were handled.

---

STEP 3 — Build the single Apps Script file

Rules — must follow exactly or the script errors in Google Apps Script:

1. One entry function buildDeck() that:
   - calls var pres = SlidesApp.create('{deck title}')
   - reuses the default first slide pres.getSlides()[0] as SLIDE 1 (Current State Friction)
   - appends slides 2–6 with pres.appendSlide(SlidesApp.PredefinedLayout.BLANK)
   - ends with Logger.log('Created: ' + pres.getUrl())
   - produces EXACTLY 6 slides — no more, no fewer.
2. 6-digit hex only — scan every setSolidFill() before output. If any hex matches
   #[0-9A-Fa-f]{8}, replace with the nearest 6-digit equivalent. Never ship 8-digit hex.
   Never rgba().
3. Alignment enum — always SlidesApp.ParagraphAlignment.CENTER / .START / .END. Never
   DocumentApp.HorizontalAlignment.* — that is a Docs enum and throws at runtime.
4. Text boxes — always provide explicit width and height. Apps Script does not auto-size.
   POSITIVE DIMENSIONS — every width and height passed to insertTextBox / insertShape MUST be
   strictly greater than zero, or Apps Script throws "The height should be greater than zero."
   NEVER compute a box dimension as a difference that can reach <= 0 (e.g. `cardHeight - 46`
   when a card may be 46px tall). When element heights vary (tier blocks, staircase tiers), do NOT
   derive a child box's size from the variable parent height; give the child a fixed positive size
   in its own band, or clamp with Math.max(minPx, computed). Keep every shape inside its panel and
   clear of the next element (no overlap with the banner/next panel).
   Text FIT — Apps Script does not shrink text to fit. For any repeated element (cards, columns,
   table rows, tier blocks), size every instance to the LONGEST text in the set, not the
   average. Budget ~22 characters per line per 100px of box width and ~14px of box height per
   wrapped line at 9pt. If the longest item exceeds the box, reduce that group's body font by
   1pt (floor 8pt) or increase the whole group's box height equally, before reducing height
   anywhere. Verify the densest item fits BEFORE finalizing.
5. Shape styling — .getFill().setSolidFill(color) and
   .getBorder().getLineFill().setSolidFill(color) are separate calls; border does not inherit
   fill. To remove a border use .getBorder().setTransparent().
6. Z-order — insert background shapes first, text boxes last. Later insertions sit on top.
7. Slide dimensions — use points. var W = 720; var H = 405; (720x405pt = 1280x720px @96dpi).
8. Every slide gets a bottom accent bar; content slides (2–6) get a consistent navy top bar
   with title + eyebrow, so the deck reads as one branded set. Apply the per-slide background
   color specified in STEP 2.
9. Use small reusable helpers (rect, txt, topBar, accentBar) — do not hand-place every shape.
10. FIDELITY + BENCHMARK — every customer-specific fact must trace to the source notes. Any
    figure not in the source renders as the literal [BENCHMARK — validate against customer data
    before presenting] string on the slide; any missing account field as [CUSTOMER — insert
    account name]. Never fabricate a customer figure.

---

STEP 4 — Output

Deliver ONE artifact:

  Artifact: {AccountName}-Slides-Code-YYYY-MM-DD.gs   (or Template-… if no account name)
  [full Apps Script file]

Include run instructions at the top of the .gs as comments:
  1. script.google.com → New project
  2. Paste this file
  3. Run buildDeck; authorize when prompted
  4. The Execution log prints the deck URL; the deck is in Google Drive

Then output a short TRACKING NOTE (outside the .gs) listing:
  - source file (confirmed read-only, never modified)
  - output file path — the FULL absolute path actually written, including the Downloads folder
    and any numeric uniqueness suffix (not the bare filename)
  - slide count (must be 6) and a one-line title per slide
  - every [BENCHMARK …] placeholder emitted and on which slide (so the presenter knows what to
    validate before presenting)
  - unmapped content — any source material that did not fit the 6-slide skeleton
  - any source fact you could not verify (flag, do not fabricate)

Then INSERT to Supabase (project cnplogkxbjecdeeritdl, table public.account_artifacts).
Record file_path as the SAME full absolute path reported in the tracking note:
  INSERT INTO public.account_artifacts (account_name, artifact_type, title, file_path, created_at)
  VALUES ('{AccountName}', 'slide-deck', '{AccountName} CIO Architecture Deck', '{full absolute .gs path}', NOW());

Before finishing, verify your output against each of these:
- Did I run the STEP 2 FALLBACK GATE first, confirm the source fits the 6-slide architecture taxonomy (else recommend 005→006 and stop), then map content into all 6 fixed slides in order, leaving the source unmodified?
- Does the single .gs build exactly 6 slides in one Run (SlidesApp.create + 5 appendSlide), with 6-digit hex, no child box dimension derived from a variable parent height, positive explicit text-box dimensions, and Slides alignment enums?
- Is EVERY numeric literal on every slide either quoted from the source or rendered as a literal [BENCHMARK …] placeholder, and is every skeleton architecture claim the source does not support marked Reference/[CUSTOMER-UNVERIFIED] rather than asserted — with nothing fabricated?
Correct any failures silently and output only the corrected result.
```
