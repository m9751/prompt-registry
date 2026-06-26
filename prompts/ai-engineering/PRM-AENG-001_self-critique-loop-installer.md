---
id: PRM-AENG-001
title: Self-Critique Loop Installer
domain: ai-engineering
source_format: SKILL.md or prompt .md file (pasted text)
target_orchestrator: Claude Code
downstream_consumer: Human (reviews modified artifact, opens PR if valid)
version: 1.0.0
last_updated: 2026-06-26
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/ai-engineering/PRM-AENG-001_self-critique-loop-installer.md
use_for: Add a self-critique loop to any skill or prompt — derives 2-3 binary output checks from the artifact's required structure and inserts them at the correct location
---

## Overview

Adds a self-critique loop to any SKILL.md or prompt `.md` file. The loop fires just before the artifact delivers its output — the model checks its own work against binary criteria, corrects failures silently, then delivers. The caller never sees an incomplete artifact.

Paste the full artifact text into `{{Artifact_Text}}`. The prompt returns the modified artifact only — no commentary.

*Registry JSON appends a feedback block after the primary output; respond to it after completing the mandatory output.*

## Prompt

```
You are adding a self-critique loop to the artifact below.

Rules:
1. Read the artifact's use_for field and documented output structure.
2. Identify the 2-3 things that, if missing from the output, would make it useless to the caller.
3. Write exactly 2-3 binary checks. Each check must be:
   - Pass/fail with no subjective judgment
   - Procedural (names a specific field, section, or structural requirement)
   - Specific to THIS artifact — never generic ("was the output good?")
4. Do not write more than 3 checks. Law of diminishing returns: beyond 3, the model anchors on early checks and the later ones degrade.
5. For machine-output artifacts (JSON, XML, structured payload): end the block with "Correct any failures silently."
6. For human-facing output: end the block with "Correct any failures silently, then deliver."
7. Placement rules:
   - SKILL.md: insert the block immediately before the step that writes, deploys, or returns the final result.
   - Prompt .md: insert the block inside the fenced code block, immediately before the closing fence line.
8. Do not add a second block if one already exists.
9. Do not change anything else in the artifact.

Block format (use exactly):
Before delivering, verify your output against each of these:
- Did I [specific binary check 1]?
- Did I [specific binary check 2]?
- Did I [specific binary check 3 — omit if only 2 are genuinely distinct]?
Correct any failures silently[, then deliver].

Output only the complete modified artifact — no explanation, no commentary.

Artifact:
{{Artifact_Text}}

Before delivering, verify your output against each of these:
- Did I write 2-3 binary checks that are specific to this artifact's required output (not generic)?
- Did I place the block immediately before the final delivery step (not mid-artifact)?
- Did I output only the modified artifact with no added commentary?
Correct any failures silently, then deliver.
```
