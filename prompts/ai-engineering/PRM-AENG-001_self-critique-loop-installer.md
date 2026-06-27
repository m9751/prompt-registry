---
id: PRM-AENG-001
title: Self-Critique Loop Installer
domain: ai-engineering
source_format: SKILL.md or prompt .md file (pasted text)
target_orchestrator: Claude Code
downstream_consumer: Human (reviews modified artifact, opens PR if valid)
version: 1.1.0
last_updated: 2026-06-26
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/ai-engineering/PRM-AENG-001_self-critique-loop-installer.md
use_for: Add a self-critique loop to any skill or prompt — reads the artifact's use_for and required output, writes 2-3 binary checks, inserts the block at the correct location
---

## Overview

Inserts a self-critique block into any SKILL.md or prompt `.md` file. The block fires just before the artifact delivers its output — the model checks its own work against binary pass/fail criteria, corrects silently, then delivers.

Paste the full artifact text into `{{Artifact_Text}}`. Returns only the modified artifact — no commentary.

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory output.*

## Prompt

```
Insert a self-critique block into the artifact below. Follow every rule exactly.

--- RULES ---

Block format (copy verbatim, fill in the checks):
Before delivering, verify your output against each of these:
- Did I [check 1]?
- Did I [check 2]?
- Did I [check 3 — omit if only 2 are genuinely distinct]?
Correct any failures silently, then deliver.

How to write the checks:
- Read the artifact's use_for field and its documented output structure.
- Write 2-3 checks — each one names a specific, verifiable field, section, or structural requirement of the output. Each check is pass/fail with no subjective judgment.
- Maximum 3 checks. Never generic ("was the output good?").
- For machine-output artifacts (JSON, XML): end with "Correct any failures silently." — no prose.
- For human-facing output: end with "Correct any failures silently, then deliver."

Where to insert the block:
- SKILL.md: immediately before the step that writes, deploys, or returns the final result.
- Prompt .md: inside the fenced code block, immediately before the closing ``` line.
- Do not insert if a self-critique block already exists.
- Do not change anything else in the artifact.

--- EXAMPLE ---

Input artifact (linkedin-content SKILL.md, end of delivery section):

When the campaign-builder skill runs, generate one LinkedIn post as part of the package:
- Content: A POV post about the problem the event addresses (NOT a promo post)
- Timing: Suggest posting 2 weeks before the event

## Output Format

Output artifact (block inserted before Output Format):

When the campaign-builder skill runs, generate one LinkedIn post as part of the package:
- Content: A POV post about the problem the event addresses (NOT a promo post)
- Timing: Suggest posting 2 weeks before the event

Before delivering, verify your output against each of these:
- Did I write for a professional LinkedIn audience (peer-to-peer practitioner voice, not generic social)?
- Does the post have a clear hook in the first 1-2 lines that stops the scroll?
- Is the post under 1300 characters (LinkedIn's effective engagement threshold)?
Correct any failures silently, then deliver.

## Output Format

--- END EXAMPLE ---

Now insert the block into this artifact. Output only the complete modified artifact.

{{Artifact_Text}}

Before delivering, verify your output against each of these:
- Did I write 2-3 binary checks specific to this artifact's documented output (not generic)?
- Did I place the block immediately before the final delivery step, not mid-artifact?
- Did I output only the modified artifact with no added commentary?
Correct any failures silently, then deliver.
```
