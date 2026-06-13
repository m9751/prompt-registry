---
id: PRM-INFRA-002
title: Make Every Derived Index Self-Healing
domain: systems-architecture
source_format: Derived-index register (register.md) + repo file tree
target_orchestrator: Claude Fable 5 (autonomous long-horizon, effort xhigh)
downstream_consumer: Operator (reviews PR output + register completeness)
version: 1.0.0
last_updated: 2026-06-12
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-002_fable-derived-index-self-healing.md
use_for: Audit every derived index in a multi-repo Claude Code operating system, wire un-triggered ones to self-heal on drift, and produce a durable register with automatic triggers and freshness invariants for each index
---

## Overview

Autonomous, long-horizon Fable 5 run for hardening the memory and retrieval layer of a multi-repo Claude Code operating system. A "derived index" is any artifact mechanically rebuilt from a source — a JSON manifest, a Qdrant vector collection, a compiled prompt bundle. This prompt audits the full set, wires un-triggered ones to self-heal on drift, and produces a register with evidence for each trigger.

> Paste the block below to Claude Fable 5. Effort: **xhigh**. This is an autonomous, long-horizon run.
> Structure follows the Fable 5 prompting guide (reason-first, brief steering, stated boundaries,
> grounded progress, self-verification, autonomous-pause rule, memory notes, brevity addendum).

## Prompt

```
## Why this matters (intent)

I'm hardening the memory and retrieval layer of a multi-repo Claude Code operating system for a single operator (Michael, an enterprise AE — not an ops engineer; nothing should depend on a machine being awake). A "derived index" here is any artifact mechanically rebuilt from a source — a JSON manifest, a Qdrant vector collection, a compiled prompt bundle. We just learned the hard way that any such index rebuilt by a *hand-run* command goes silently stale: one of them (`memory_manifest.json`) sat 7 weeks behind, leaving 35% of memory unfindable, with no error to signal it. We already fixed the two highest-stakes ones (the memory manifest and the `smokin_memory` vector index that feeds context into every session start). What's needed now: make the *whole class* self-healing so this can never recur anywhere, and produce one durable register that proves it.

The full pattern and reasoning is written up in `~/repos/smokin-coffee/entries/systems-architecture/FMD-024_2026-06-12_self-healing-derived-indexes.md` — read it first; it is the specification for the *shape* of every fix.

## The task

Work the derived-index register at `C:\Users\mbusa\repos\claude-config\references\derived-index-register.md` to completion, and extend it. For each derived index in the system, the end state is: **(a) an automatic trigger** (a hook, a scheduled job, or a CI workflow — never a human-run command), **and (b) a coverage/freshness invariant** that surfaces a warning the day it drifts (for example `count(index) == count(source)`, or chunk-age exceeds a threshold). The reference implementation already exists: the Stop hook `~/.claude/hooks/memory-manifest-stop-sync.sh` (rebuild-on-drift) and the `smokin_memory` session-close plus 03:00-fallback ingest. Port that shape to the rest.

**Two discovery scopes — do both:**
1. **The register's 10 rows.** Wire the un-triggered ones (the KB vector ingest is the clean next one, explicitly "batch with the smokin_memory fix"). For rows already marked triggered, open the trigger file and check that it actually calls the rebuild — record the evidence, don't assume.
2. **A second lens the register is missing.** The register was built by grepping for script names (`rebuild-*`, `ingest`, `compile-*`), so it only found *script-built* indexes. Run a second pass for *data-derived* indexes that no such grep can catch — at minimum: the skill-router catalog, Hindsight mental models, and any `spec/index.json` trigger-phrase index in the `smokin-os` repo. Add every one you find as a new register row with its trigger-or-NONE and a staleness test. Treating the 10 visible rows as the whole population would declare victory early; the goal is the complete set.

## Method

The platform rules for any GitHub Actions / Task Scheduler / PowerShell / Bash you write live in `~/repos/smokin-knowledge/AGENTS.md` — route to the matching domain (`github/`, `powershell/`, `bash/`) and follow its hard rules before writing.

The engineering method for each half is also captured as two on-demand guides in the `smokin-knowledge` repo — load and follow them: **`ci-cd-pipeline-builder`** for building each trigger (scheduled job / CI workflow / hook), and **`observability-designer`** for the freshness/coverage invariant and its warning surface.

The reference implementation for both halves of each fix is already live:
- **Trigger half:** the Stop hook `~/.claude/hooks/memory-manifest-stop-sync.sh` — rebuild-on-drift pattern (read it before building the first new trigger; port its shape, don't invent a new one).
- **Freshness/invariant half:** the `smokin_memory` session-close ingest plus 03:00-fallback Task Scheduler job — count(index) == count(source), chunk-age check pattern. Read the scheduler task definition before wiring a new job.

## Boundaries (act vs. pause)

- **Act autonomously on reversible work that follows from this request:** adding a hook, a scheduled task, a CI workflow, a freshness check; updating the register; opening PRs. These are reversible — proceed without asking.
- **Pause and ask only for the genuinely human-or-destructive:** deleting anything (for example the `cell3_sync.py` row marked DORMANT — recommend, but do not delete), rotating a secret, a destructive migration, or a decision only the operator can make. When you hit one, ask one specific question and end the turn.
- Before running any command that changes system state (registering a scheduled task, editing a config, deleting a file), check that the evidence supports *that specific action*. A script that pattern-matches "looks un-triggered" may have a trigger you haven't read yet — read the trigger surface first.
- This repo's worker pushes to a protected `main` via a drain mechanism that can jam. If a normal `git push` is rejected, land files with `gh api -X PUT repos/<owner>/<repo>/contents/<path>` (admin write, bypasses the jam) rather than fighting the worker.

## Grounding and self-verification

- Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet checked, say so. If a trigger test fails, say so with the output; if a step was skipped, say that; when an index now has a trigger and its invariant passes, state it plainly without hedging.
- Establish a method for checking your own work as you build. Every few indexes, dispatch a fresh-context verifier subagent that re-derives the acceptance test independently (count source records vs. index entries, or chunk age vs. threshold) against the specification — do not self-certify from memory.
- Delegate independent subtasks to subagents and keep working while they run (each index's wiring is independent). Intervene if a subagent goes off track or is missing context.

## Done state (the acceptance test)

You are done when: every derived index in the system — the register's rows **and** the data-derived ones you discover — has an automatic trigger recorded with read-the-file evidence, OR an explicit recommendation-not-to with a reason; each has a coverage/freshness invariant or a logged reason it doesn't need one; the register file reflects the full set; and a fresh verifier subagent re-runs the invariant on the indexes you triggered and it passes. If the second-lens pass finds that everything data-derived already self-triggers, record that and close — but say so explicitly rather than omitting it.

## Operating notes

- Keep a notes file (one lesson per file, one-line summary at top): record corrections and approaches that proved out and why they mattered; update an existing note rather than duplicating; delete notes that prove wrong.
- You have ample context. Don't stop, summarize, or suggest a new session on account of context limits — continue until the task is finished or you're blocked on input only the operator can provide.
- When you have enough information to act, act. Don't re-derive established facts, re-litigate settled decisions, or narrate options you will not pursue.
- Don't add features, refactor, or introduce abstractions beyond what each fix requires. The simplest trigger that reliably fires is the right one; a one-line cron beats a framework.
- Your final summary is the operator's first look at an autonomous run: lead with the outcome in one plain sentence (how many indexes, how many were stale, what's now self-healing), then the supporting detail. Write complete sentences; give each file, commit, and index its own plain clause; drop the working shorthand.

## Autonomous operation (system reminder)

You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups once the task wraps is fine; asking permission after already discussing the work with the user before doing it is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is finished, or when you are blocked on the one kind of input only the operator can provide (a destructive or irreversible decision, per the Boundaries section).
```
