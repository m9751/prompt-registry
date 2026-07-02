---
id: PRM-INFRA-006
title: Rule-Ladder and Cross-Machine Coverage Check
domain: systems-architecture
source_format: CLAUDE.md + law/ bodies + settings.json + hooks/ + cross-machine inbox (_mac-inbox / _win11-inbox)
target_orchestrator: Claude Sonnet 4.6 (session-scoped; operator runs interactively)
downstream_consumer: Operator (approves gap fixes — hook registration, inbox acks)
version: 1.0.0
last_updated: 2026-07-02
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-006_rule-ladder-coverage.md
use_for: Verify that lessons harvested from Pipeline-F, FMD, and memory actually hardened into enforced rules and hooks and reached both machines — a coverage check, not a discovery pass
---

## Overview

Operator-supervised Sonnet 4.6 run. The rule ladder (feedback -> rule -> hook)
and the cross-machine inbox are propagation channels, not sources of new lessons.
Their failure mode is silent: a rule authored but never enforced, a hook never
registered, a fix that landed on one machine but not the other. This prompt
confirms the first three harvests actually took effect end to end. It is prompt 4
of 4 in the Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md`) — run
LAST, after PRM-INFRA-003/004/005 have filled the gaps it checks.

> Paste the block below into a Claude Sonnet 4.6 session. Operator-supervised.
> Phase 1 is read-only. This is a coverage check — do not author new rules here.

## Prompt

```
## Why this matters (intent)

I'm harvesting what our operating system has learned into enforced improvements, without applying findings randomly and breaking things. This is prompt 4 of 4 in the Feedback-Harvest Playbook (`~/repos/smokin-os/spec/feedback-harvest-playbook.md` — read it first for the prime directive and shared guardrails). The rule ladder and the cross-machine inbox are propagation channels, not lesson sources. Their failure mode is silent: a rule authored but never enforced, a hook never registered in settings.json, a fix that landed on one machine but not the other. This is a coverage check that the first three harvests took effect end to end — NOT a discovery pass.

## The task — Phase 1: current-state diagnosis (READ-ONLY)

1. For a sample of live rules in CLAUDE.md, trace each to its `law/` body and, where the rule claims enforcement, to a registered hook in `settings.json`. Report any rule that is TEXT-ONLY (no body, or a hook that exists in `hooks/` but isn't registered).
2. Report hooks present in `hooks/` but NOT registered in `settings.json`. Remember a `git pull` on claude-config does not activate `~/.claude/` — install is required, so an unregistered or uninstalled hook is dormant.
3. Read the cross-machine inbox (`_mac-inbox` / `_win11-inbox`). List open notes and whether each was acked ON ORIGIN (a note is "sent" only when on origin/main, not when it exists locally).
4. Output three lists: RULE-WITHOUT-HOOK | HOOK-UNREGISTERED | INBOX-OPEN-UNACKED.

STOP here. Present the three lists and end the turn. No config edits in Phase 1.

## Phase 2: apply (ONLY after the operator approves specific items)

- Register an approved hook by editing `settings.json` on a claude-config branch + PR. Then run the machine's install (Mac `make install` / Win11 `scripts\install.bat`) and prove it fires live — registration alone is not activation.
- Ack/close approved inbox notes via `inbox-gh-put.sh` and confirm `ON ORIGIN`.
- Anything owed to the other machine: send a note, do not assume parity.

## Boundaries (act vs. pause)

- Act autonomously on Phase 1 (read-only).
- Pause and ask for: registering any hook in settings.json, closing an inbox thread, or any change to the enforcement surface. Do NOT author new rules in this prompt — that is the job of PRM-INFRA-003/004/005.
- The claude-config worker can jam a protected-main push. If a normal push is rejected, land files with `gh api -X PUT`.

## Grounding

Trace each enforcement claim to the actual settings.json registration and, where possible, a live fire. Do not report a hook as "enforced" from its presence in hooks/ alone — presence is not registration and registration is not activation.

## Scope

No authoring new rules (prompts 1-3 own that). This prompt only closes the gap between authored and enforced/propagated.

## Execution discipline

Michael is present. When you have enough to act, act. End your turn at the Phase 1 STOP, or when blocked on an approval only the operator can give.

## Self-critique (run before delivering the Phase 1 lists)

Draft the three lists. Verify against each check below. Correct any failure silently and deliver only the corrected result.
- Did I distinguish present-in-hooks/ from registered-in-settings.json from installed-and-firing, rather than treating presence as enforcement?
- Did I check each inbox note's status ON ORIGIN rather than by local file presence?
- Did I author zero new rules and make zero config edits in Phase 1, ending on the STOP?
```
