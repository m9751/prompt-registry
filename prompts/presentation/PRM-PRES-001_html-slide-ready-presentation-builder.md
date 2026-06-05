---
id: PRM-PRES-001
title: HTML Slide-Ready Presentation Builder
domain: presentation
source_format: Freeform content brief (account name, slide type list, content per slide)
target_orchestrator: Claude (Claude Code / Advanced Chat)
downstream_consumer: Human — opens HTML in browser for preview, runs .gs in Google Apps Script for Google Slides
version: 1.0.0
last_updated: 2026-06-05
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/presentation/PRM-PRES-001_html-slide-ready-presentation-builder.md
use_for: Build a branded HTML presentation + matching Google Apps Script from a structured content brief, with auto-versioned filenames and Supabase logging
---

## Overview

Builds two artifacts from a content brief:
1. `{Account}-Slides-YYYY-MM-DD.html` — browser-viewable slide deck, 1280×720px per slide
2. `{Account}-Slides-Code-YYYY-MM-DD.gs` — paste into script.google.com → Run to create the deck in Google Drive

**Trigger phrase:** "build me an HTML slide-ready presentation"

**Division of labor:** Claude generates the `.gs` (structured, deterministic, no rendering needed). For visual polish on the HTML, hand it to Gemini (free, no token cost on your side).

**After both artifacts are produced**, INSERT a row to `public.account_artifacts` on Supabase project `cnplogkxbjecdeeritdl` with `account_name`, `artifact_type = 'slide-deck'`, `title`, `file_path`, and `created_at`.

```
## PROMPT

You are an expert HTML + Google Apps Script engineer. Build a branded slide presentation from the content brief below.

---

### STEP 1 — Collect inputs

Ask for the following if not already provided:

1. **Account name** — used to auto-name both output files:
   - `{AccountName}-Slides-YYYY-MM-DD.html`
   - `{AccountName}-Slides-Code-YYYY-MM-DD.gs`
2. **Brand block** (optional — defaults to MuleSoft if omitted):
   ```
   primary:    #032D60   (navy — backgrounds, top bars)
   secondary:  #0176D3   (blue — borders, highlights)
   accent:     #FE9339   (orange — accent bars, pills)
   background: #FFFFFF   (white — slide canvas)
   cloud:      #EAF5FE   (light blue — card fills)
   green:      #2E7D32   (status pass)
   green_bg:   #E8F5E9
   amber:      #856404   (status pending)
   amber_bg:   #FFF8E1
   muted:      #5A7A99   (secondary text)
   border:     #D0E4F5
   ```
3. **Slide list** — for each slide, provide:
   ```
   - type: title | status | steps | table | next-steps
   - title: "..."
   - headline: "..."        (subtitle or supporting line)
   - content: [...]         (bullets, rows, or steps — depends on type)
   - pills: [...]           (optional — {label, status: pass|pending})
   ```

---

### STEP 2 — Build the HTML file

**Spec — must follow exactly:**

- Canvas: `width: 1280px; height: 720px; overflow: hidden; position: relative`
- One `<div class="slide s{N}">` per slide
- Layout: CSS absolute positioning — no flexbox at the slide level
- Fonts: `'Salesforce Sans', 'Inter', -apple-system, sans-serif`
- **6-digit hex ONLY** — never `rgba()`, never 8-digit hex (e.g. `#FF000080`)
- CSS variables in `:root` — use brand block values
- Bottom orange accent bar on every slide: `position: absolute; bottom: 0; left: 0; width: 1280px; height: 4px; background: var(--accent)`

**Slide type templates:**

**`title`** — navy background
- Left orange accent bar: `position: absolute; left: 0; top: 0; width: 6px; height: 720px`
- Content area: left 80px, vertically centered — eyebrow (uppercase, orange), h1 (white, 54px bold), org line (muted white), answer box (dark blue bg, orange left border, orange label + white text)
- Right panel: right 380px wide, darker blue bg — logo centered, meta text below divider

**`status`** — white background
- Navy top bar (height 100px): title left, logo right
- 3 status cards below (equal width, ~194px each): colored bg + matching border, large number, label, description
- Bottom half: layered architecture diagram — 4 horizontal boxes (Experience → Process API → System API → Source System), each labeled, colored by layer, connected by arrow symbols

**`steps`** — white background
- Navy top bar: title + subtitle
- 4 equal-width step columns: circle number (colored by done/pending), step label (uppercase), step title (bold), description text, status pill at bottom
- Done state: green circle + green border card. Pending state: muted circle + light border card
- Rationale box below: light blue bg, small text

**`table`** — white background
- Navy top bar: title
- Table: header row (cloud bg), body rows with columns: #, Requirement (name + description), What We Built, How We Tested It, Result pill
- Result pill: amber bg + amber text for BUILT/PENDING; green bg + green text for PASS

**`next-steps`** — white background
- Navy top bar: title + subtitle
- Orange left accent bar
- 5 equal-width step cards: navy circle number, bold title, description text
- Closing statement box at bottom: light blue bg, navy text

---

### STEP 3 — Build the Apps Script file

**Rules — must follow exactly or the script will error in Google Apps Script:**

1. **6-digit hex only** — scan every `setSolidFill()` call before outputting. If any hex value matches `#[0-9A-Fa-f]{8}`, replace with nearest 6-digit equivalent. Hard stop: never ship 8-digit hex.
2. **Alignment enum** — always `SlidesApp.ParagraphAlignment.CENTER` (or `.START` / `.END`). Never `DocumentApp.HorizontalAlignment.*` — that is a Docs enum and will throw at runtime.
3. **New slides** — `pres.appendSlide(SlidesApp.PredefinedLayout.BLANK)` for slides 2+. The first slide is `pres.getSlides()[0]`.
4. **Text boxes** — always provide explicit `width` and `height`. Apps Script does not auto-size.
5. **Shape styling** — `.getFill().setSolidFill(color)` and `.getBorder().getLineFill().setSolidFill(color)` are separate calls. Border does not inherit fill.
6. **Z-order** — insert background shapes first, text boxes last. Later insertions sit on top.
7. **Slide dimensions** — use points. 720×405pt maps to 1280×720px at 96dpi. Use `var W = 720; var H = 405`.
8. **Logger.log** — end the script with `Logger.log('Created: ' + pres.getUrl())` so the user can find the deck.

---

### STEP 4 — Output

Deliver both complete artifacts, clearly separated:

```
## Artifact 1: {AccountName}-Slides-YYYY-MM-DD.html
[full HTML file]

## Artifact 2: {AccountName}-Slides-Code-YYYY-MM-DD.gs
[full Apps Script file]
```

Then log to Supabase (`cnplogkxbjecdeeritdl`, table `public.account_artifacts`):
```sql
INSERT INTO public.account_artifacts (account_name, artifact_type, title, file_path, created_at)
VALUES ('{AccountName}', 'slide-deck', '{AccountName} Slide Deck', '{AccountName}-Slides-YYYY-MM-DD.html', NOW());
```
```
