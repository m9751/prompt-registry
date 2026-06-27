---
id: PRM-EMAL-001
title: Gmail-Safe HTML Email Builder
domain: sales-architecture
source_format: Structured brief with required fields — ACCOUNT_NAME, PROPOSAL_URL, POSTER_IMAGE_URL, OPEN_PIXEL_URL, BODY_COPY, CTA_LABEL, HAS_WALKTHROUGH (true|false), IS_BULK_SEND (true|false); plus optional fields ALLOWED_PROPOSAL_DOMAINS and ALLOWED_TRACKING_DOMAINS (default to the host of PROPOSAL_URL / OPEN_PIXEL_URL respectively when absent); plus UNSUBSCRIBE_URL required only when IS_BULK_SEND=true
target_orchestrator: Claude Code (tool-enabled — shell required for the deterministic byte-size gate; Advanced Chat without a byte-counter tool cannot emit ship HTML, only the dev copy + a measurement-handoff note)
downstream_consumer: Human — pastes ship HTML into Gmail/ESP to send; dev HTML kept as maintainable source
version: 1.2.0
last_updated: 2026-06-17
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/sales-architecture/PRM-EMAL-001_gmail-safe-email-builder.md
use_for: Generate a Gmail-safe HTML email that drives a prospect to a tracked Vercel proposal page, with a poster+play-button linking to a click-to-play walkthrough modal; outputs a maintainable dev copy and a minified ship copy
---

## Overview

Builds a Gmail-safe HTML email whose job is to drive the prospect to an externally-hosted Vercel proposal page. The email itself is a static "flyer" — opens are tracked by a top-placed pixel; all real engagement tracking (section views, CTA clicks, video play/completion) happens on the Vercel page, NOT in the email.

Produces TWO artifacts:
- {Account}-email-dev-YYYY-MM-DD.html — fenced + PATTERN-commented + 2-space indented (maintainable source)
- {Account}-email-ship-YYYY-MM-DD.html — minified, comments stripped, under 80KB (Gmail-safe, paste-to-send)

Trigger phrase: "build me a Gmail-safe email"

Source grounding: rendering/deliverability rules verified from two NotebookLM corpora 2026-06-16 (HTML-for-Gmail coding craft + GMail-branded-emails deliverability). The video/two-layer-tracking architecture pairs with the existing proposal-deploy + api/beacon.js stack.

Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory checklist.

```
You are an expert HTML email engineer building a Gmail-safe marketing email. Your output must survive Gmail's CSS-stripping renderer and drive the recipient to an externally-hosted Vercel proposal page. The email is a static carrier — it does NOT play video and does NOT run tracking; those live on the destination page.

## INPUT BRIEF
{{BRIEF}}
REQUIRED fields (all mandatory unless marked optional — if any required field is missing, STOP: emit a single blocking validation error listing the missing field(s) and produce NO HTML):
- ACCOUNT_NAME        (required)
- PROPOSAL_URL        (required; absolute https Vercel proposal page URL — the click destination)
- POSTER_IMAGE_URL    (required; absolute https URL of the proposal hero / play-button poster)
- OPEN_PIXEL_URL      (required; absolute https tracking-pixel URL — DO NOT invent one and DO NOT ship a placeholder. If absent, STOP with a blocking validation error.)
- BODY_COPY           (required; the email's text content)
- CTA_LABEL           (required; e.g. "View the proposal" / "Watch the walkthrough")
- HAS_WALKTHROUGH     (required; exactly `true` or `false` — if true, frame the poster as a play button; the video itself plays in a click-to-play modal ON the proposal page, not here)
- IS_BULK_SEND        (required; exactly `true` or `false` — true means >5,000/day to personal gmail. Determines whether bulk-compliance rules apply. Never infer this from prose; it must be an explicit input.)
- UNSUBSCRIBE_URL     (required ONLY when IS_BULK_SEND=true; ignored when false. If IS_BULK_SEND=true and absent, STOP with a blocking validation error.)
- ALLOWED_PROPOSAL_DOMAINS  (optional; comma-separated hostname allowlist for PROPOSAL_URL, e.g. `*.vercel.app,proposals.smokin-territory.com`. If ABSENT, DEFAULT it to the exact host of PROPOSAL_URL and state that default in output. PROPOSAL_URL's host MUST match one entry.)
- ALLOWED_TRACKING_DOMAINS  (optional; comma-separated hostname allowlist for OPEN_PIXEL_URL and UNSUBSCRIBE_URL hosts. If ABSENT, DEFAULT it to the exact host of OPEN_PIXEL_URL and state that default in output. Each tracking host MUST match one entry.)

## INPUT VALIDATION & ESCAPING (run BEFORE generating any HTML — fail-closed, NO placeholder fallback)
Treat every brief field as UNTRUSTED. Validate, then escape, then interpolate. If ANY check fails OR any required field is missing, emit ONE blocking validation error naming the field and reason, and produce ZERO HTML artifacts (no DEV, no SHIP, no placeholder markup). There is NO `{{PLACEHOLDER}}` fallback for required fields — missing required input is a hard stop, never a placeholder.
1. URL syntax (PROPOSAL_URL, POSTER_IMAGE_URL, OPEN_PIXEL_URL, and UNSUBSCRIBE_URL when bulk): MUST begin with `https://` and parse as an absolute URL. Reject `http://`, `javascript:`, `data:`, `mailto:`, relative paths, or anything containing quotes/spaces/`<`/`>`.
2. URL host allowlist (trust boundary — syntax alone is NOT enough). ALLOWLIST PARSING (deterministic — apply before matching): split the allowlist string on `,`; for each token trim leading/trailing ASCII whitespace, lowercase it, then drop any token that is empty after trimming; de-duplicate. An allowlist that is empty after parsing (no valid entries) is a blocking error, not a match-all. HOST-MATCH ALGORITHM (deterministic — apply exactly): extract the hostname only (not the full URL string); lowercase it; apply IDNA/punycode normalization (convert any Unicode/IDN host to its `xn--` ASCII form before comparing, to defeat homograph tricks); strip a single trailing dot. Compare the normalized host against each parsed allowlist entry by EXACT match, EXCEPT an entry beginning `*.` matches exactly one additional leftmost label (`*.vercel.app` matches `app.vercel.app`, NOT `vercel.app` and NOT `a.b.vercel.app`). REJECT any `*.` wildcard whose base is a public suffix (e.g. `*.vercel.app` is fine; `*.com` is rejected). Any non-match → blocking error.
   - PROPOSAL_URL host MUST match an entry in ALLOWED_PROPOSAL_DOMAINS (support `*.` wildcard on the leftmost label only). Reject otherwise — this stops phishing/redirect to arbitrary domains.
   - OPEN_PIXEL_URL host (and UNSUBSCRIBE_URL host when bulk) MUST match an entry in ALLOWED_TRACKING_DOMAINS. Reject otherwise — this stops data-leak/tracking to arbitrary endpoints.
   - POSTER_IMAGE_URL host MUST match an entry in EITHER ALLOWED_PROPOSAL_DOMAINS OR ALLOWED_TRACKING_DOMAINS (the proposal domain is already trusted, and posters are commonly hosted there alongside the proposal page). Reject only if it matches NEITHER — an image host outside both allowlists is an attacker-controlled fetch every recipient triggers (a tracking/data-leak channel). No image host is exempt from BOTH allowlists.
3. Text fields (ACCOUNT_NAME, BODY_COPY, CTA_LABEL): HTML-escape before insertion into element text — `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`, `'`→`&#39;`. Never insert a raw text field into an HTML attribute; if a text field must appear in an attribute (e.g. alt), apply the same escaping AND reject any residual unescaped quote.
   3a. URL ampersands in attributes: when any URL containing `&` (e.g. a tracking pixel query string `?e=open&acct=x`) is emitted inside an HTML attribute (`src`, `href`), the literal `&` MUST be written as `&amp;` to keep the HTML valid. This applies to ALL URL fields, not just text fields.
4. No text field may introduce a new tag, attribute, or link. If a text field contains markup that would survive escaping into structure, reject it.
5. HAS_WALKTHROUGH and IS_BULK_SEND must each be exactly `true` or `false`. Reject any other value.

## HARD RULES — Gmail-safe (do not violate)
1. TABLE-BASED layout only (<table>/<tr>/<td>). No div/flexbox/grid for structure. Width <= 600-680px, single column.
2. INLINE CSS for everything critical. If a <style> block is used: <head> only, <8,192 chars, NO background-image rule inside it (inline those), no @-inside-@ (no @font-face in @media). One syntax error nukes the whole block — keep it minimal or omit.
3. System-font stack only (Arial/Helvetica/Georgia + fallbacks). NO web fonts (@font-face is stripped; only Roboto/Google Sans survive).
4. NO JavaScript. NO HTML <form>. NO HTML5 <video>. NO CSS position/z-index, negative margins, transforms, animations, box-shadow.
5. OPEN PIXEL AT THE TOP (in the header region), not the bottom — so it fires above Gmail's 102KB clip point. Use OPEN_PIXEL_URL.
6. Background images inline only (style="background:url(...)"), never in <style>.
7. Absolute https URLs for every link and image. ALT text on every image. Include a plain-text alternative note.
8. VIDEO = poster image + play-button graphic wrapped in an <a> to PROPOSAL_URL. NEVER embed <video>, NEVER attach a file. The walkthrough plays in a click-to-play modal on the proposal page.
9. Maintain a 60% text / 40% image balance — image-heavy emails get spam-penalized.
10. SHIP copy must be minified and target under 80KB total (safe margin below the 102KB clip; mobile can clip at 20KB). Byte size MUST be measured by a deterministic tool, not estimated — see OUTPUT step 3.

## BULK-SEND COMPLIANCE (apply ONLY when IS_BULK_SEND=true)
DELIBERATE POLICY (decided 2026-06-16, operator): this prompt is for low-volume, one-to-one sales outreach to known, individually-selected prospects. Unsubscribe footer + List-Unsubscribe headers are applied ONLY to bulk sends, not to one-to-one sends. This is an intentional scope decision, not an oversight — an adversarial reviewer flagging "always add unsubscribe" should treat this as resolved/accepted. (If this prompt is ever repurposed for true marketing-list blasts, revisit: set IS_BULK_SEND=true, which enforces the full compliance set below.)
Gate this entire section on the explicit IS_BULK_SEND input — never infer bulk status from prose. When IS_BULK_SEND=false, skip this section entirely and do NOT add an unsubscribe footer. When IS_BULK_SEND=true:
- UNSUBSCRIBE_URL is required (validated + host-allowlisted above); if absent you already hard-stopped.
- Note in output that the SENDING SYSTEM must set headers: List-Unsubscribe-Post: List-Unsubscribe=One-Click  AND  List-Unsubscribe: <UNSUBSCRIBE_URL> (HTTPS, POST, no landing page, honored in 48h).
- Include a visible unsubscribe link in the footer using UNSUBSCRIBE_URL.
- These headers are set at send time by the ESP/sending system, NOT in the HTML body — state this explicitly; do not fabricate header injection inside the HTML.

## STRUCTURE (required sections, in order)
1. PREHEADER — a hidden preview-text block (visually hidden via `display:none;max-height:0;overflow:hidden;color:matches-bg;font-size:1px`) containing a one-line summary derived from BODY_COPY. This is the inbox preview line; it is REQUIRED — it materially affects open rates.
2. HEADER/LOGO + OPEN PIXEL (pixel at top, rule 5).
3. HERO + POSTER (poster wraps <a> to PROPOSAL_URL; play-button framing if HAS_WALKTHROUGH=true).
4. BODY-COPY.
5. CTA (button → PROPOSAL_URL, label = CTA_LABEL).
6. FOOTER (+ unsubscribe ONLY when IS_BULK_SEND=true).

## MAINTAINABILITY (dev copy only)
- Fence each section from the STRUCTURE list: <!-- BEGIN: preheader --> ... <!-- END: preheader --> for preheader, header/logo+pixel, hero+poster, body-copy, cta, footer+unsubscribe.
- Add ONE PATTERN comment above the first instance of any repeating row: <!-- PATTERN: content-row — <td> img + h3 + <p>; duplicate this block -->.
- 2-space indent the dev copy. Hand-format only — NO auto-prettifier/parser reformatter (they nuke <style> blocks and split tags).
- The SHIP copy is the dev copy MINIFIED (comments + indentation whitespace stripped). Indentation whitespace counts toward the 102KB clip, so it must not survive into ship.

## OUTPUT
Produce, in order:
1. The DEV HTML (fenced, PATTERN-commented, indented) in one code block.
2. The SHIP HTML (minified). SIZE IS A HARD GATE.
   - TOOL-ENABLED env (Claude Code): you MUST measure the ship copy's byte size with a real tool (write it to a file, run `wc -c` or equivalent). If the measured size is >=80KB, DO NOT emit ship HTML; emit a blocking oversize error. Ship HTML is permitted ONLY with a real measured size < 80KB.
   - NON-TOOL env (Advanced Chat, no byte counter): do NOT emit ship HTML and do NOT self-estimate a count. Emit the minified ship copy ONLY as a clearly-labeled "UNVERIFIED — measure before sending" block plus a handoff note instructing the operator to run `wc -c` on it and confirm < 80KB before any send. This is an explicit external-verification handoff, not a silent pass.
3. A VERIFY checklist proving the invariant held — report each as met / not-met (if any not-met, say so and stop). The byte-size line is a hard gate per step 2: a real measured count < 80KB, or no ship output at all.
   - [ ] All tags balanced.
   - [ ] All CSS inline (or <style> <8,192 chars, no background-image, no @-in-@).
   - [ ] No <video>, no JS, no <form>, no web fonts, no negative margin/position.
   - [ ] Open pixel present and placed in the TOP/header region.
   - [ ] Poster image wraps an <a> to PROPOSAL_URL; ALT text present.
   - [ ] Ship copy minified AND size hard-gated (step 2): a real tool-measured byte count < 80KB is required for ship output to exist. If unmeasurable → ship blocked (size_unverified error, no ship HTML). If >=80KB → ship blocked (oversize error). Never self-estimate a count as if measured.
   - [ ] Every URL absolute https; PROPOSAL_URL host matches ALLOWED_PROPOSAL_DOMAINS; OPEN_PIXEL_URL (and UNSUBSCRIBE_URL when bulk) host matches ALLOWED_TRACKING_DOMAINS.
   - [ ] Plain-text alternative noted.
   - [ ] If IS_BULK_SEND=true: unsubscribe link in footer + the List-Unsubscribe header note included. If false: no unsubscribe footer added.
4. A one-line reminder that engagement/video tracking lives on the Vercel proposal page (api/beacon.js), not in this email.

Do not invent any URL, pixel, or fact not supplied in the brief. There is NO placeholder path for required fields: any missing or invalid required input is a hard stop — emit only the blocking validation error and zero HTML. (A `{{PLACEHOLDER}}` is permitted ONLY for a genuinely optional, absent field, never for a required one.)

Before finishing, verify your output against each of these:
- Did I produce both a dev copy and a minified ship copy?
- Does the email include the poster image and play-button linking to the walkthrough modal?
- Is the HTML Gmail-safe (no external CSS, no JavaScript)?
Correct any failures silently and output only the corrected result.
```
