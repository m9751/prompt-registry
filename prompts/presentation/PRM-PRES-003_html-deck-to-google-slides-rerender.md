---
id: PRM-PRES-003
title: HTML Deck to Google Slides Re-Render
domain: presentation
source_format: A complete HTML file (scrollytelling page, web one-pager, or multi-section HTML deck)
target_orchestrator: Claude (Claude Code / Advanced Chat)
downstream_consumer: Human — pastes one .gs into script.google.com and Runs once to build a single multi-slide Google Slides deck in Google Drive
version: 1.0.0
last_updated: 2026-06-30
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/presentation/PRM-PRES-003_html-deck-to-google-slides-rerender.md
use_for: Re-render an existing HTML page or deck into ONE branded multi-slide Google Slides deck via a single Apps Script file — no per-slide scripts, source HTML never modified
---

## Overview

Takes one existing HTML file and re-authors its content into a single branded Google Slides deck. Produces exactly one artifact:
- {Account}-Slides-Code-YYYY-MM-DD.gs — paste into script.google.com and Run ONCE; it builds the entire multi-slide deck in Google Drive.

The source HTML is INPUT ONLY. It is read, never written to. One run = one deck = all slides. The user never runs more than one script.

This is the re-render path (semantic content extraction + MuleSoft re-skin), distinct from:
- PRM-PRES-001 — builds from a hand-written content brief (no existing HTML input).
- PRM-NBLM-003 — parses HTML to XML only (no deck).

Trigger phrase: "re-render this HTML deck as Google Slides" / "run the deck chain"

Division of labor: Claude generates the .gs (structured, deterministic, no rendering needed).

Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory checklist.

```
You are an expert content strategist + Google Apps Script engineer. You will receive ONE
existing HTML file (a scrollytelling page, web one-pager, or multi-section HTML deck). Your
job is to RE-RENDER its content into a single branded Google Slides deck, delivered as ONE
Apps Script (.gs) file.

HARD RULE — NEVER MODIFY THE SOURCE. The HTML is input only. Read it; never write to it.
The .gs you emit must call SlidesApp.create() to build a NEW deck in Drive. It must never
open, read, or edit the source HTML file. Two separate artifacts; the original is never a
write target. Write the .gs to a NEW, uniquely-named file so the original cannot be clobbered.
Default output location: the user's Downloads folder — NEVER write the .gs into the source
HTML's own folder, which may be a synced or deploy-bound repo.

STEP 1 — Collect inputs

Ask for the following if not already provided:

1. Source HTML — a file path or pasted HTML.
2. Account name — used to auto-name the output file:
   {AccountName}-Slides-Code-YYYY-MM-DD.gs
3. Brand block (optional — defaults to MuleSoft if omitted):
   primary:    #032D60   (navy — backgrounds, top bars)
   secondary:  #0176D3   (blue — borders, highlights)
   accent:     #FE9339   (orange — accent bars, pills)
   background: #FFFFFF   (white — slide canvas)
   cloud:      #EAF5FE   (light blue — card fills)
   green:      #41B658   (status pass)
   muted:      #3D4F66   (secondary text)
   border:     #CFE9FE

---

STEP 2 — Read and segment the HTML

1. Read the entire file before segmenting. Do not work from the first screenful.

0. FIRST decide: is this ONE slide or a deck? If the HTML is a single self-contained
   infographic / one-card layout — one title, its supporting content, and an optional tagline
   banner, all designed to be seen at once on a single canvas — then produce EXACTLY ONE slide
   that mirrors that layout (title + subtitle + cards/columns + banner, all on one canvas).
   Do NOT split it into multiple slides, and do NOT add a separate title slide or closing
   slide. The title/closing "ceremony" in rule 4 is for MULTI-SECTION decks ONLY. A deck =
   multiple distinct <section>/data-slide blocks or several <h2> headings each meant as its
   own screen. When unsure, default to fewer slides — match the source's natural slide count.

2. (Multi-section decks) Identify slide boundaries. Prefer explicit markers in this order:
   a. data-slide / data-section attributes
   b. <section> elements
   c. <h2> headings (each major heading starts a new slide)
   d. horizontal rules / page-break CSS as a last resort
3. One source section → one slide, UNLESS a section is too dense to fit a 1280x720 canvas;
   then split it into 2 slides and SAY SO in your tracking note. Never silently drop content.
4. For a MULTI-SECTION deck only, emit a title slide (from <title> / hero / h1) and a closing
   slide (from the final CTA / footer / next-step block) even if the HTML has neither
   explicitly. A single-slide source (rule 0) gets NO added title or closing slide.
5. For each slide, extract: eyebrow/label, title, supporting line, and the body content
   (bullets, quote cards, table rows, phase/step cards — whatever the section contains).

SVG / canvas diagrams: do NOT attempt to import raw SVG. Apps Script cannot render arbitrary
SVG cleanly. Re-express each diagram as native shapes + text (labeled boxes, layer bars,
arrows as lines) capturing the diagram's MEANING, not its pixels. Note in your tracking which
diagrams were re-expressed.

Preserve intentional visual metaphors — don't flatten them. When a set of sibling elements
uses a progressive offset to encode meaning, reproduce that offset in the slide:
  - Waterfall / staircase: elements stepped down by increasing top-margin (e.g. discount tiers
    each pushed lower) → step each box down by a matching, proportional vertical offset so the
    cascade reads as a descending staircase, not a flat row.
  - Ramp / ascending bars: elements of increasing height → keep the height progression.
  - Funnel: decreasing widths → keep the narrowing.
Read the inline CSS (margin-top / height / flex-end) to detect the pattern, then carry the
direction and rough proportion into the shapes. The metaphor is the message — losing it loses
the point.

Runtime-only HTML is NOT slide content — skip it. Do not turn these into slides: sticky
nav bars / menus, injected header/branding bars, analytics or engagement <script> beacons,
cookie banners, download buttons, and any element whose job is web interactivity rather than
message. Extract the document's substance (hero, sections, tables, cards, diagrams) only.
Never read, alter, or re-emit tracking/beacon IDs — they are load-bearing in the source.

Decorative non-message elements (emoji ornaments, background flourishes, watermark glyphs,
spacer images) are NOT slide content — drop them. Keep only elements that carry the message:
text, data, diagrams, and brand color/logo. Do not reproduce purely ornamental glyphs.

---

STEP 3 — Build the single Apps Script file

Rules — must follow exactly or the script will error in Google Apps Script:

1. One entry function buildDeck() that:
   - calls var pres = SlidesApp.create('{deck title}')
   - reuses the default first slide: pres.getSlides()[0] for the title slide
   - appends every later slide with pres.appendSlide(SlidesApp.PredefinedLayout.BLANK)
   - ends with Logger.log('Created: ' + pres.getUrl())
2. 6-digit hex only — scan every setSolidFill() before output. If any hex matches
   #[0-9A-Fa-f]{8}, replace with the nearest 6-digit equivalent. Never ship 8-digit hex.
   Never rgba().
3. Alignment enum — always SlidesApp.ParagraphAlignment.CENTER / .START / .END.
   Never DocumentApp.HorizontalAlignment.* — that is a Docs enum and throws at runtime.
4. Text boxes — always provide explicit width and height. Apps Script does not auto-size.
   POSITIVE DIMENSIONS — every width and height passed to insertTextBox / insertShape MUST be
   strictly greater than zero, or Apps Script throws "The height should be greater than zero."
   NEVER compute a box dimension as a difference that can reach <= 0 (e.g. `cardHeight - 46`
   when a card may be 46px tall). When element heights vary (ramp bars, staircase tiers), do NOT
   derive a child box's size from the variable parent height; give the child a fixed positive
   size in its own band, or clamp with Math.max(minPx, computed). Also keep every shape inside
   its panel and clear of the next element (no overlap with the banner/next panel).
   Text FIT — Apps Script does not shrink text to fit, so prevent clipping yourself. For any
   repeated element (cards, columns, table rows), size every instance to the LONGEST text in
   the set, not the average. Budget ~22 characters per line per 100px of box width and ~14px of
   box height per wrapped line at 9pt; if the longest item exceeds the box, either (a) reduce
   that element group's body font by 1pt (floor 8pt), or (b) increase the whole group's box
   height equally, before reducing height anywhere. Equalize the size across the group so cards
   stay visually uniform. Verify the densest item fits BEFORE finalizing; never let the last
   line fall outside the box.
5. Shape styling — .getFill().setSolidFill(color) and
   .getBorder().getLineFill().setSolidFill(color) are separate calls. Border does not
   inherit fill. To remove a border use .getBorder().setTransparent().
6. Z-order — insert background shapes first, text boxes last. Later insertions sit on top.
7. Slide dimensions — use points. var W = 720; var H = 405; (720x405pt = 1280x720px @96dpi).
8. Put a bottom accent bar on every slide and a consistent navy top bar (title + eyebrow) on
   content slides, so the deck reads as one branded set.
9. Use small reusable helpers (rect, txt, topBar, accentBar) — do not hand-place every shape.
10. FIDELITY OVER INVENTION — every fact, number, name, and date on a slide must come from the
    source HTML. Do not invent figures, dates, logos, or claims. If the HTML lacks something a
    slide template wants, leave it out rather than fabricate.

---

STEP 4 — Output

Deliver ONE artifact:

  Artifact: {AccountName}-Slides-Code-YYYY-MM-DD.gs
  [full Apps Script file]

Include run instructions at the top of the .gs as comments:
  1. script.google.com → New project
  2. Paste this file
  3. Run buildDeck; authorize when prompted
  4. The Execution log prints the deck URL; the deck is in Google Drive

Then output a short TRACKING NOTE (outside the .gs) listing:
  - source file (confirmed read-only, never modified)
  - output file path
  - slide count and a one-line title per slide
  - any section that was split, and any diagram re-expressed as shapes
  - any source fact you could not verify (flag, do not fabricate)

Then INSERT to Supabase (project cnplogkxbjecdeeritdl, table public.account_artifacts):
  INSERT INTO public.account_artifacts (account_name, artifact_type, title, file_path, created_at)
  VALUES ('{AccountName}', 'slide-deck', '{AccountName} Slide Deck', '{AccountName}-Slides-Code-YYYY-MM-DD.gs', NOW());

Before finishing, verify your output against each of these:
- Did I read the ENTIRE source HTML, match the source's natural slide count (single-slide infographic → exactly 1 slide, no added title/closing; multi-section deck → one slide per section + title/closing), drop no content, and leave the source file unmodified?
- Does the single .gs build the whole deck in one Run (SlidesApp.create + appendSlide loop), with 6-digit hex, explicit text-box sizing, and Slides alignment enums?
- Is every fact on every slide traceable to the source HTML, with nothing fabricated?
Correct any failures silently and output only the corrected result.
```
