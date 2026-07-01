---
id: PRM-PRES-005
title: Notes to MuleSoft Google Slides (Flexible Layout, One-Shot Apps Script)
domain: presentation
source_format: Freeform notes, bullets, stats, or quotes (no HTML, no fixed structure required)
target_orchestrator: Gemini or Claude (any LLM that can write Google Apps Script)
downstream_consumer: Human — pastes one .gs into script.google.com and Runs once to build a MuleSoft-branded Google Slides deck in Google Drive
version: 1.0.1
last_updated: 2026-07-01
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/presentation/PRM-PRES-005_notes-to-mulesoft-slides-flexible.md
use_for: Turn raw content into a MuleSoft-branded Google Slides deck via ONE Apps Script file, with FLEXIBLE slide layout (title/content/section/stat/quote helpers) instead of a fixed 6-slide skeleton — carries the hard Apps Script error-prevention rules so the generated .gs runs without runtime errors
---

## Overview

Converts raw content (notes, bullets, stats, quotes) into a single MuleSoft-branded Google Slides deck as ONE Apps Script (`.gs`) file. Unlike `PRM-PRES-004` (which maps content into a fixed 6-slide CIO architecture skeleton), this prompt uses a **flexible layout** — the model chooses title, content, section/segue, stat-callout, and quote slides to fit the content, driven by reusable helper functions.

Produces exactly one artifact:
- `{Deck}-Slides-Code-YYYY-MM-DD.gs` — paste into script.google.com and Run `createDeck()` ONCE; it builds the deck in Google Drive and logs the URL.

**How this differs from siblings:**
- `PRM-PRES-004` — fixed 6-slide CIO architecture skeleton. Use it for MuleSoft+Informatica healthcare integration decks where the narrative is known.
- `PRM-PRES-003` — re-renders an existing HTML deck into Google Slides.
- `PRM-PRES-001` — builds HTML + a matching `.gs` from a structured brief.
- **This prompt (PRES-005)** — freeform content → Google Slides in one hop, flexible structure, no HTML detour, no fixed skeleton. Use when the deck's shape should follow the content rather than a preset narrative.

**Why the Apps Script rules block:** the generated `.gs` runs in Google Apps Script, which throws on 8-digit hex, Docs alignment enums, zero/negative box dimensions, and inherited borders. The rules block encodes the exact fixes for those runtime failures so the emitted script runs on the first Run.

**Font/logo caveat:** Salesforce Sans does not render inside Apps Script — the font falls back to Arial (per brand spec). The top-right logo corner is left empty for the presenter to drop the asset in manually. Both are inherent to the Apps Script path, not the prompt.

Trigger phrase: "notes to slides" / "flexible notes to Google Slides"

## Branding Tokens (MuleSoft)

| Token | Value | Usage |
|---|---|---|
| Font | `'Salesforce Sans', 'SF Pro Display', Arial, sans-serif` | All text |
| Blue 10 | `#001639` | Darkest navy — title/segue backgrounds |
| Blue 20 (Primary Navy) | `#032D60` | Dark backgrounds, headers, body text on light bg |
| Blue 40 | `#0B5CAB` | Secondary headers, borders, title accent rule |
| Blue 50 (CTA Blue) | `#0176D3` | Buttons, links, emphasis |
| Cloud Blue 60 | `#0D9DDA` | Hero/highlight blue |
| Cloud Blue 90 | `#CFE9FE` | Subtle backgrounds |
| Cloud Blue 95 | `#EAF5FE` | Content-area background |
| Blue 95 | `#EEF4FF` | Page background |
| Orange 70 | `#FE9339` | Primary accent — callouts, stat numbers |
| Green 65 | `#41B658` | Success/positive metrics |
| Teal 80 | `#04E1CB` | Accent |
| Purple 40 | `#7526E3` | Accent |
| Pink 60 | `#FF538A` | Accent |

```
You are a presentation engineer building an on-brand MuleSoft (a Salesforce company)
Google Slides deck. Convert the CONTENT I provide below into a complete, runnable
Google Apps Script that, when pasted into script.google.com and run, creates a new
Google Slides presentation.

=== OUTPUT REQUIREMENTS ===
1. Return ONE complete Apps Script (.gs) file — nothing else. No prose before or after,
   no markdown fences. Just the code, ready to paste and run.
2. The entry function must be createDeck(). It creates the presentation via
   SlidesApp.create(), sets a clear title, and builds every slide in order.
3. Use SlidesApp APIs only (SlidesApp.create, appendSlide, insertTextBox, insertShape,
   getFill, getBorder, setBackgroundColor, etc.). No external libraries.
4. Set explicit slide backgrounds, text colors, fonts, and sizes on every element —
   do NOT rely on default themes.
5. After the deck is built, Logger.log() the presentation URL so I can open it.
6. Wrap slide-building in reusable helpers so code stays DRY (e.g. addTitleSlide,
   addContentSlide, addSectionSlide, addStatSlide, addQuoteSlide).
7. Every color must be a hex string from the palette below. Never invent a color.

=== APPS SCRIPT RULES (follow EXACTLY or the script errors at runtime) ===
1. 6-DIGIT HEX ONLY. Scan every setSolidFill() before output; if any hex matches
   #[0-9A-Fa-f]{8} (8-digit) replace it with the nearest 6-digit equivalent. Never ship
   8-digit hex. Never use rgba().
2. ALIGNMENT ENUM — always SlidesApp.ParagraphAlignment.CENTER / .START / .END.
   NEVER DocumentApp.HorizontalAlignment.* — that is a Docs enum and throws at runtime.
3. TEXT BOXES & SHAPES — always pass explicit width AND height. POSITIVE DIMENSIONS: every
   width and height passed to insertTextBox / insertShape MUST be strictly greater than zero.
   NEVER compute a box dimension as a difference that can reach <= 0 (e.g. cardHeight - 46).
   Do NOT derive a child box's size from a variable parent height; give it a fixed positive
   size or clamp with Math.max(minPx, computed).
4. SHAPE STYLING — .getFill().setSolidFill(color) and
   .getBorder().getLineFill().setSolidFill(color) are SEPARATE calls; the border does not
   inherit the fill. Before filling a border line, call .getBorder().setWeight(1) so the line
   exists. To remove a border use .getBorder().setTransparent().
5. Z-ORDER — insert background shapes first, text boxes last. Later insertions sit on top.
6. NEW SLIDES — reuse pres.getSlides()[0] as the first slide; add the rest with
   pres.appendSlide(SlidesApp.PredefinedLayout.BLANK).
7. SLIDE DIMENSIONS in points: var W = 720; var H = 405; (720x405pt = 960x540px @96dpi).
8. Use setFontFamily to set the font; Apps Script does not auto-size text, so size every
   repeated element (cards, columns, rows) to fit its LONGEST text, not the average.
9. BULLETS — SlidesApp text boxes do NOT auto-render bullet glyphs or space paragraphs;
   a multi-line body renders as one cramped block by default. For any bulleted list either
   call text.getListStyle().applyListPreset(SlidesApp.ListPreset.DISC_CIRCLE_SQUARE), OR
   set per-paragraph spacing with getParagraphStyle().setSpaceBelow(...) (and prepend an
   explicit "• " glyph if not using a list preset). Never leave bullets as an unspaced block.

=== MULESOFT BRAND SYSTEM (apply exactly) ===
FONTS
- All text: "Salesforce Sans" (fall back to "Arial" via setFontFamily).
- Headings: Bold. Body: Normal. Base body size 20pt; slide titles 32-40pt;
  section-header titles 28-32pt.

PRIMARY COLORS (hex)
- Blue 10  #001639  darkest navy — title/segue backgrounds
- Blue 20  #032D60  PRIMARY navy — dark backgrounds, headers, body text on light bg
- Blue 40  #0B5CAB  secondary headers, borders
- Blue 50  #0176D3  primary CTA blue — buttons, links, emphasis
- Cloud Blue 60 #0D9DDA  hero/highlight blue
- Cloud Blue 90 #CFE9FE  subtle backgrounds
- Cloud Blue 95 #EAF5FE  content-area background
- Blue 95  #EEF4FF  page background

ACCENTS (rotate in this order for charts/multi-item visuals)
Orange 70 #FE9339 -> Green 65 #41B658 -> Blue 50 #0176D3 -> Teal 80 #04E1CB
-> Purple 40 #7526E3 -> Pink 60 #FF538A

LAYOUT / SLIDE RULES
- Title slide: background Blue 20 (#032D60), white title + subtitle text.
- Content slides: background White or Cloud Blue 95 (#EAF5FE); title in Blue 20;
  body text in Blue 20; a thin Blue 40 (#0B5CAB) accent rule/underline under the title.
- Section/segue slides: background Blue 10 (#001639) or Blue 20, large white heading.
- Quote slides: large decorative quotation mark, centered text, Blue 20 on light bg.
- Stat callouts: large accent-colored number (from the accent sequence) with a short label.
- Cards: white fill, Blue 20 border, navy title, dark body.
- Reserve the top-right corner clear on every content slide (logo placement) — leave
  ~1 inch of empty space there; do not put text in the top-right corner.
- Dark background -> white text only. Light background -> Blue 20 text. Maintain WCAG AA contrast.
- Do NOT use gray for section differentiation — use Cloud Blue 95 or Blue 95.

DECK STRUCTURE
- Slide 1: Title slide (deck title + subtitle/date).
- Insert section/segue slides between major topics.
- Break dense content into multiple slides; max ~5 bullets per slide, one idea per slide
  where possible.
- Final slide: a "Thank You" / next-steps slide (Blue 20 background, white text).

=== CONTENT TO CONVERT ===
{{Content}}

Now produce the complete Apps Script.

Before finishing, verify your output against each of these:
- Does createDeck() run in a single pass, call SlidesApp.create(), and Logger.log() the deck URL?
- Is every hex value 6-digit (no 8-digit, no rgba), every insertTextBox/insertShape width and height strictly greater than zero, and every alignment a SlidesApp.ParagraphAlignment enum?
- Does every color used come from the MuleSoft palette above, with dark backgrounds using white text and light backgrounds using Blue 20 text?
Correct any failures silently and output only the corrected result.
```
