---
id: PRM-NBLM-009
title: HTML Maintainability Refactor
domain: sales-architecture
source_format: Single-file HTML
target_orchestrator: Claude Code / Gemini / Grok
downstream_consumer: Human (review) + the refactored HTML file
version: 1.0.2
last_updated: 2026-06-17
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/sales-architecture/PRM-NBLM-009_html-maintainability-refactor.md
use_for: Reorganize a large single-file HTML document to best-practice structure (indentation, section fences, component patterns) so a human or AI can edit it safely, without changing how the page renders
---

## Overview

A structural-only refactor for large single-file HTML deliverables (slide-style proposals, branded briefs, architecture pages). It re-indents, adds BEGIN/END section fences and one PATTERN comment per repeating component, and proves the rendering is unchanged — so the next editor (human or AI) can make low-blast-radius changes. It does NOT touch content, CSS, layout, or visual output, and it forbids automated reformatters that have historically corrupted these files. Model-agnostic (Claude / Gemini / Grok); if fences already exist it normalizes rather than duplicates.

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory VERIFY checklist.*

## Prompt

```
# TASK: Reorganize a single-file HTML document for maintainability

You are refactoring an existing single-file HTML document so that a future
editor — human or AI — can change it safely, quickly, and with minimal risk.

## PARAMETERS
- FILE_PATH:   {{FILE_PATH}}
- OUTPUT_MODE: {{OUTPUT_MODE}}   (choose: "Edit in place" | "Return full file" | "Write to {{FILE_PATH}}.refactored.html")
- SCOPE:       {{SCOPE}}         (default: "Whole file". May be "Section: <name>" to limit the refactor.)

If the file is pasted instead of referenced, operate on the pasted content.

## OBJECTIVE
Reorganize the document's STRUCTURE to best practices. The result must be:
easy to change, low blast radius (a change in one section cannot silently
affect another), efficient to navigate, durable, and reliable.

## THE INVARIANT — DO NOT VIOLATE
This is a STRUCTURAL refactor ONLY. The RENDERED output must be unchanged —
the DOM, visible text, CSS, and JS semantics must be identical before and after.
The SOURCE may change ONLY in these three ways:
  1. whitespace / indentation,
  2. added HTML comments,
  3. (optional) reordering of ATTRIBUTES within a single tag, where it provably
     does not change rendering.
Specifically you must NOT:
- add, remove, reword, or reorder any visible text or content;
- change any CSS rule, value, selector, color, font, or layout;
- change any attribute VALUE, id, class, href, or inline style;
- **reorder sibling HTML elements** — order is rendering-significant whenever
  CSS uses :nth-child, :nth-of-type, or the +/~ combinators; treat ALL sibling
  order as load-bearing and preserve it;
- add features, frameworks, dependencies, or scripts.
- **Minified Code Exclusion:** if any block of code, <style>, or <script>
  appears minified or intentionally flattened onto a single line, do NOT
  re-indent it to 2 spaces. Leave all minified / single-line compressed regions
  exactly as-is to prevent rendering layout creep.
If you cannot make a change without risking the invariant, DO NOT make it —
leave that region exactly as-is and note it in the VERIFY output.

## FORBIDDEN METHOD
Do NOT use any automated HTML reformatter or parser-based pretty-printer
(e.g. BeautifulSoup prettify(), Prettier with reflow, html-tidy). On this exact
class of large single-file HTML they have silently split <br> tags and dropped
<style> blocks. Re-indent and annotate by DIRECT TEXT EDITING only.

## !! STOP — CORRUPTION RISK — READ THIS BEFORE YOU EDIT !!
The single biggest way this task fails is by REGENERATING THE WHOLE FILE.
If a file contains a large single-line blob — a base64 data: URI image, a minified
<style>/<script>, an inline SVG — and you rewrite or re-emit the entire file, you
WILL truncate that blob mid-string. The output looks plausible, the tags look
closed, and the file is silently destroyed. (Observed live 2026-06-17: a full-file
rewrite cut a 14 KB base64 logo mid-string and dropped an 86-line file to 18 lines.)

MANDATORY, NO EXCEPTIONS:
1. Make a .bak copy of the original BEFORE the first edit. This is your recovery
   path and it is not optional. (In the 2026-06-17 incident the .bak is the ONLY
   reason nothing was lost.)
2. Refactor by SMALL, TARGETED EDITS to structural lines (comments, indentation,
   fences) — one region at a time. NEVER regenerate or re-emit the whole document
   in a single operation when ANY oversized single-line blob is present.
3. Leave oversized single-line content (data: URIs, minified blocks, inline SVG)
   on its own line, BYTE-UNTOUCHED. Do NOT reflow, re-wrap, or re-indent it — and
   never split it across lines.
4. If your only available action is "emit the full file" and the file contains
   such a blob, STOP and say so rather than risk truncation. A refusal is a
   success; a silently truncated file is the worst possible outcome.

## IDEMPOTENCY
The file may ALREADY contain BEGIN/END fences or PATTERN comments from a prior
run. If so:
- do NOT duplicate them;
- NORMALIZE inconsistent names to the conventions below;
- leave already-correct annotations untouched.
- **Wrap Beside Human Comments:** do NOT delete, rephrase, or erase any
  pre-existing human-authored content comment (editorial notes, structural
  tracking numbers like `<!-- (1) LOGO -->`). Your BEGIN/END fences must wrap
  ALONGSIDE or OUTSIDE existing comments, never replace them — keep the human
  comment and add the fence, so a second run recognizes the layout as already
  normalized.
Running this prompt twice must produce the same result as running it once.

## WHAT TO DO
1. Re-indent the entire document (or the chosen SCOPE) to consistent 2-space
   indentation.
2. Identify the major sections by semantic landmark / top-level layout block
   (header, nav, hero, each top-level <section>, footer, the <style> block, the
   <script> block). Fence TOP-LEVEL landmarks only — do NOT create nested
   sub-fences, EXCEPT inside <style> if the CSS is already grouped by comments,
   in which case you may fence those existing groups.
3. Derive each section's name from an existing id or heading. If a block has no
   id or heading, derive a short name from its leading class; if none is
   sensible, leave it unfenced rather than invent a concept.
   - EMAIL / TABLE-LAYOUT HTML is a common variant: Gmail-safe email uses nested
     <table> layout, all-inline CSS, NO <style> block, NO ids, and NO repeating
     "card" components. Handle it gracefully: derive section names from any
     EXISTING comments (e.g. `<!-- (1) LOGO -->` → BEGIN: logo) or from the row's
     visible purpose; SKIP the id-based naming, the <style>-grouping rule, and the
     PATTERN step (step 5) entirely — none apply. Do not force-fit them.
4. Wrap each identified section in BEGIN/END comment fences:
     <!-- BEGIN: nav -->
       ...
     <!-- END: nav -->
5. On each repeating component (cards, rows, list items sharing a template),
   add ONE PATTERN comment above the FIRST instance only, using this schema:
     <!-- PATTERN: {name} — {structure}; duplicate this block -->
   Example:
     <!-- PATTERN: capability-card — icon + h3 + <p>; duplicate this block -->
   One per repeating type — do not annotate every instance.
6. Keep all tags balanced and every id/anchor intact.

## OUTPUT-MODE HANDLING
Evaluate your environment and OUTPUT_MODE before acting:
- If you have file-system access: prefer "Edit in place" or "Write to
  *.refactored.html" — it avoids truncation entirely. Before modifying a file
  in place, ALWAYS create a .bak copy of the original first.
- If you are in a web chat / lack file access: you must return the code in chat.
  Do NOT attempt to predict chunk sizes (e.g. "Part 1 of 3") — models estimate
  their own output length poorly and break tags doing it. Instead: print as much
  as you safely can, stop EXACTLY at the close of an HTML tag, and append exactly
  this text:
      /// STOPPED: SAY CONTINUE ///
  Resume from the next line only when prompted with "continue". Never silently
  truncate.

## VERIFY BEFORE RETURNING (prove the invariant held)
Report this checklist; if any item cannot be checked, say so explicitly and STOP:
- [ ] All tags balanced (open count == close count).
- [ ] No visible text node changed (content identical to input).
- [ ] <style> and <script> block CONTENTS unchanged.
- [ ] No sibling elements reordered.
- [ ] Every id/anchor that existed still exists (list any named anchor, e.g. #roles).
      If the document has ZERO ids/anchors (common in email HTML), state that
      explicitly — "0 ids in source, 0 in output" — so the check is not mistaken
      for a skipped step.
- [ ] Section fences present (list the BEGIN/END section names).
- [ ] PATTERN comments added (LIST the unique component types annotated — do not
      report a numeric count).
- [ ] Regions left as-is to protect the invariant (list them, with reason).

## OPTIONAL — MECHANICAL VERIFICATION (CLI agents only)
If you have shell execution, verify the invariant locally before completing —
regex parsing of HTML is brittle, so use a real diff, not grep:
- If the file is tracked in Git: run `git diff --word-diff` and confirm that ONLY
  whitespace, comments, and (optionally) attribute order changed — no visible
  text, CSS, JS, or sibling-element order.
- If Git is unavailable: run `diff -u BEFORE.html AFTER.html` against a saved copy
  of the original and review every hunk for the same guarantee.
- In either case, explicitly confirm every `id="..."` present in BEFORE is still
  present in AFTER (a word-diff shows changes but does not by itself prove no id
  was dropped — check the id set directly).
- If you have no shell: skip this section silently — the mandatory VERIFY
  checklist above stands on its own.

⚠️ CRITICAL FOR CLI AGENTS: you must NOT introduce ANY whitespace change inside
an HTML attribute value or inline-CSS string (e.g. `style="color:#fff"` →
`style="color: #fff"`). If the diff reveals any change INSIDE a tag's attributes,
treat it as an invariant FAIL — not an innocent quirk. It is a strict signal that
you drifted from targeted structural editing and touched load-bearing attribute
data. Stop and correct it before completing.
```
