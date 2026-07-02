---
id: PRM-INFRA-003
title: Pipeline-F Finding Harvest
domain: systems-architecture
source_format: Pipeline-F proposal + run JSON (pipeline-f/proposals, pipeline-f/*/YYYY-MM-DD.json)
target_orchestrator: Claude Sonnet 4.6 (session-scoped; operator runs interactively)
downstream_consumer: Operator (approves the classified table, then reviews rule/hook PRs)
version: 1.0.0
last_updated: 2026-07-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-003_pipeline-f-harvest.md
use_for: Harvest the latest Pipeline-F proposal into approved rule and hook changes, gating every edit behind an operator-confirmed diagnosis so false gates never ship
---

## Overview

Operator-supervised Sonnet 4.6 run. Pipeline-F sweeps session transcripts against
the rule corpus and flags recurring patterns and missing-rule candidates. This
prompt converts genuine signal into enforced rules without introducing false
gates. It is prompt 1 of 4 in the Feedback-Harvest Playbook
(`~/repos/smokin-os/spec/feedback-harvest-playbook.md`) — run it first.

> Paste the block below into a Claude Sonnet 4.6 session. Operator-supervised —
> Michael is present. Phase 1 is read-only and ends in a STOP; nothing is edited
> until the diagnosis table is approved.

## Prompt

```
## Why this matters (intent)

I'm harvesting what our operating system has learned into enforced improvements, without applying findings randomly and breaking things. This is prompt 1 of 4 in the Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md` — read it first for the prime directive and shared guardrails). Pipeline-F flags recurring session patterns and missing-rule candidates, but a flagged pattern is a hypothesis, not a mandate. We once shipped a corpus-path bug that flagged every pattern as missing (rules=0 / missing=159) and it ran green for weeks. So diagnosis comes before any edit.

## The task — Phase 1: current-state diagnosis (READ-ONLY)

1. Read the latest Pipeline-F proposal (newest file under `pipeline-f/proposals`).
2. Read the latest run JSON (`pipeline-f/*/YYYY-MM-DD.json`, newest date) and report the raw counts verbatim: rules, patterns, recurring, missing, consolidation.
3. Sanity-gate the run before trusting it: confirm rules > 0 and the rule-corpus path resolves. A missing count once spiked purely from a renamed `rules/` -> `law/` path. If rules == 0, stop and report the dead path — do not classify anything as missing.
4. For EACH recurring pattern and EACH missing-rule candidate, classify it:
   - REAL      — recurs across >= 3 distinct sessions AND maps to a concrete failure
   - NOISE     — one-off, or an artifact of a measurement/path bug
   - DUPLICATE — already covered by an existing rule in `law/` (cite the file)
5. Output one table: pattern | classification | evidence | existing-rule-if-any.

STOP here. Present the table and end the turn. Do not edit any file in Phase 1.

## Phase 2: apply (ONLY after the operator approves specific rows)

For patterns the operator marks REAL, and only those:
- Draft a one-line checklist entry for `CLAUDE.md` PLUS a full body for `law/<name>.md`, matching the existing rule voice (imperative, no em-dashes, no emojis).
- If a pattern warrants enforcement, propose the hook, but do NOT register it in `settings.json` without explicit sign-off — a bad gate blocks real work.
- Work claude-config off-main on a branch + PR.
- Before claiming done: show the diff; for any hook, show a live-fire test proving it fires on a violation AND that a compliant action passes (no false positive). Registration is not activation — run the machine's install and prove the fire.

## Boundaries (act vs. pause)

- Act autonomously on Phase 1 (all read-only) and, after approval, on reversible authoring (drafting rule text, opening a PR).
- Pause and ask for: registering any hook in settings.json, anything destructive, or any classification the operator hasn't confirmed.
- The claude-config worker pushes to a protected main via a drain that can jam. If a normal push is rejected, land files with `gh api -X PUT repos/<owner>/<repo>/contents/<path>` rather than fighting the worker.

## Grounding

Audit every claim against a tool result from this session. If the run JSON shows rules == 0, say so and stop — do not narrate a plausible pattern list from memory. Report only patterns you can cite from the proposal.

## Scope

Only patterns in THIS proposal. No refactoring the pipeline itself. No rule that isn't backed by a flagged, operator-approved pattern.

## Execution discipline

Michael is present. When you have enough to act, act. End your turn at the Phase 1 STOP, or when blocked on an approval only the operator can give.

## Self-critique (run before delivering the Phase 1 table)

Draft the table. Verify it against each check below. Correct any failure silently and deliver only the corrected result.
- Did I confirm rules > 0 and the corpus path resolves BEFORE classifying anything as missing?
- Does every REAL classification cite evidence of recurrence across >= 3 distinct sessions?
- Did I edit zero files in Phase 1 and end on the STOP?
```
