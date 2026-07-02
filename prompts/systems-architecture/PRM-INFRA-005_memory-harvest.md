---
id: PRM-INFRA-005
title: Memory Drift Audit and Harvest
domain: systems-architecture
source_format: MEMORY.md dashboard + Hindsight recall (memory files under ~/.claude/memory)
target_orchestrator: Claude Sonnet 4.6 (session-scoped; operator runs interactively)
downstream_consumer: Operator (approves the drift lists, then reviews deletions and rule PRs)
version: 1.0.0
last_updated: 2026-07-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-005_memory-harvest.md
use_for: Audit the memory store for drift (stale, duplicate, contradicting entries) and harvest recurring corrections into rules, gating deletions and rule-promotions behind approval
---

## Overview

Operator-supervised Sonnet 4.6 run. Memory (MEMORY.md + Hindsight) is the
largest, lowest-density store. Its failure mode is drift: stale entries that
contradict current reality, duplicates, and corrections that recur so often they
should be rules. Blind trimming risks deleting a load-bearing pointer; blind
rule-creation risks freezing a stale fact. This prompt surfaces drift and repeat
corrections and lets the operator decide. It is prompt 3 of 4 in the
Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md`).

> Paste the block below into a Claude Sonnet 4.6 session. Operator-supervised.
> Phase 1 is read-only; deletions and rule-promotions require approval.

## Prompt

```
## Why this matters (intent)

I'm harvesting what our operating system has learned into enforced improvements, without applying findings randomly and breaking things. This is prompt 3 of 4 in the Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md` — read it first for the prime directive and shared guardrails). Memory is the largest, lowest-density store; its failure mode is drift. Blind trimming can delete a load-bearing pointer; blind rule-creation can freeze a stale fact. Harvest = surface drift and repeat-corrections, then let the operator decide.

## The task — Phase 1: current-state diagnosis (READ-ONLY)

1. Read MEMORY.md end to end. Report total entries, and every entry pair that CONTRADICTS another (cite both) or DUPLICATES another (cite both).
2. Flag STALE-SUSPECT entries: any entry naming a file, flag, or PR — spot-check that the artifact still exists (a memory reflects what was true when written, not necessarily now).
3. Via Hindsight recall (cap limit ~= 3, tight queries, <= 3 KB per call — delegate large reads to a subagent), identify corrections that recur across multiple sessions. These are rule candidates, not memory.
4. Read the "Corrections (override stale entries)" block: identify which corrections have fully superseded their target, so the target can be deleted.
5. Output three lists: CONTRADICTIONS | STALE-SUSPECT | RULE-CANDIDATES.

STOP here. Present the three lists and end the turn. No deletions or writes in Phase 1.

## Phase 2: apply (ONLY after the operator approves specific items)

- Delete only entries the operator confirms stale/superseded, and update the MEMORY.md pointer in the same change. Note: merge=union files can't delete lines via squash when main has diverged — rebase + `--merge`, then verify the deletion landed with `git show origin/main:MEMORY.md | wc -c`.
- Promote a recurring correction to a rule (claude-config branch + PR) only on approval; leave the memory entry as its pointer.
- Never expand MEMORY.md net. A harvest should shrink or hold it, never grow it.

## Boundaries (act vs. pause)

- Act autonomously on Phase 1 (read/recall only).
- Pause and ask for: any deletion, any rule promotion, any Hindsight bank write. Recall is read-only and fine; retain/invalidate/delete are not.
- The claude-config worker can jam a protected-main push. If a normal push is rejected, land files with `gh api -X PUT`.

## Grounding

Before flagging an entry STALE, open the named artifact and confirm its state — do not infer staleness from the entry's age or wording alone. Report only contradictions and duplicates you can cite by line.

## Scope

No touching Hindsight banks beyond read/recall. No new memory categories. Cap recalls and route any big read to a subagent.

## Execution discipline

Michael is present. When you have enough to act, act. End your turn at the Phase 1 STOP, or when blocked on an approval only the operator can give.

## Self-critique (run before delivering the Phase 1 lists)

Draft the three lists. Verify against each check below. Correct any failure silently and deliver only the corrected result.
- For every STALE-SUSPECT entry, did I actually open the named file/flag/PR to confirm state, not infer it from age?
- Are RULE-CANDIDATES backed by recurrence across multiple sessions, not a single recall hit?
- Did I perform zero deletions or writes in Phase 1 and end on the STOP?
```
