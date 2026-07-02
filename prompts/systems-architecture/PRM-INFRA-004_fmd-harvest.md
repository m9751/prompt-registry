---
id: PRM-INFRA-004
title: FMD Learning-Log Harvest
domain: systems-architecture
source_format: FMD entries in smokin-coffee (FOR[Michael].md, 9-step structure)
target_orchestrator: Claude Sonnet 4.6 (session-scoped; operator runs interactively)
downstream_consumer: Operator (approves the classified table, then reviews rule/memory PRs)
version: 1.0.0
last_updated: 2026-07-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-004_fmd-harvest.md
use_for: Harvest the FMD learning log into concrete still-applicable actions, finding lessons that are valid but never hardened into a rule, hook, or memory
---

## Overview

Operator-supervised Sonnet 4.6 run. FMD entries are human-written failure lessons
in the smokin-coffee repo (9-step structure, FMD-001 through the latest). Many
describe fixes that already shipped; some describe patterns never hardened. This
prompt finds the lessons that are real AND not yet reflected in the live system.
It is prompt 2 of 4 in the Feedback-Harvest Playbook
(`~/repos/smokin-os/spec/feedback-harvest-playbook.md`) — run after Pipeline-F (PRM-INFRA-003).

> Paste the block below into a Claude Sonnet 4.6 session. Operator-supervised.
> Phase 1 is read-only and ends in a STOP.

## Prompt

```
## Why this matters (intent)

I'm harvesting what our operating system has learned into enforced improvements, without applying findings randomly and breaking things. This is prompt 2 of 4 in the Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md` — read it first for the prime directive and shared guardrails). FMD entries are human-written failure lessons. The risk is re-applying a lesson whose fix already landed, or acting on an entry a later FMD superseded. Harvest = find lessons that are real AND not yet reflected in the live system.

## The task — Phase 1: current-state diagnosis (READ-ONLY)

1. Do a literal directory sweep of every FMD file in smokin-coffee. Report the count and the highest FMD number — do not recall these, list them.
2. For each FMD, read its lesson/action step and classify:
   - LANDED     — the fix is already in `law/`, `CLAUDE.md`, a hook, or a merged PR (cite the specific artifact)
   - OPEN       — the lesson is valid but no corresponding rule / hook / memory exists yet
   - SUPERSEDED — a later FMD or a correction reversed it (cite which)
   - STALE      — about infrastructure that no longer exists
3. Flag any FMD whose "fix" claim cannot be verified against a live artifact.
4. Output one table: FMD# | one-line lesson | status | live-artifact-or-gap.

STOP here. Present the table and end the turn. Do not edit any file in Phase 1.

## Phase 2: apply (ONLY after the operator approves specific rows)

For OPEN entries the operator picks, and only those:
- Route each to its correct home: a durable behavior -> a rule (claude-config branch + PR); a fact worth recalling -> a memory file + a MEMORY.md pointer; a genuine one-off -> leave it in FMD, take no action.
- Do NOT invent new tables or parallel systems. Reuse the rule ladder, the memory format, and this registry's rubric standard.
- Prove each landing by citing the merged PR or the written memory file, not intent.

## Boundaries (act vs. pause)

- Act autonomously on Phase 1 (read-only) and, after approval, on reversible authoring (writing a memory file, drafting rule text, opening a PR).
- Pause and ask for: editing any FMD entry, creating a new FMD, registering a hook, or acting on a status the operator hasn't confirmed.
- The claude-config worker can jam a protected-main push. If a normal push is rejected, land files with `gh api -X PUT`.

## Grounding

A memory or recall reflects what was true when written. Before marking any FMD LANDED, open the cited artifact and confirm it exists now. If you cannot verify a fix, classify it as a gap, not LANDED.

## Scope

Read-only until approval. No editing FMD entries themselves. No new FMD files. Only the FMDs that exist in the repo today.

## Execution discipline

Michael is present. When you have enough to act, act. End your turn at the Phase 1 STOP, or when blocked on an approval only the operator can give.

## Self-critique (run before delivering the Phase 1 table)

Draft the table. Verify it against each check below. Correct any failure silently and deliver only the corrected result.
- Did I sweep the actual directory for the FMD count and highest number rather than recalling them?
- For every FMD marked LANDED, did I open and cite the live artifact that proves the fix shipped?
- Did I edit zero files in Phase 1 and end on the STOP?
```
