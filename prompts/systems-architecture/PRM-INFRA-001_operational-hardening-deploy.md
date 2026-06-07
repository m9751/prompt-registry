---
id: PRM-INFRA-001
title: Operational Hardening Deploy
domain: systems-architecture
source_format: Code files + ADR + deploy plan
target_orchestrator: Claude Code
downstream_consumer: Human (review then approve)
version: 1.0.0
last_updated: 2026-06-07
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-001_operational-hardening-deploy.md
use_for: Review code for correctness then execute a hardened deploy using the Phased Build Protocol
---

## Overview

Two-stage hardening sequence for any deploy. Stage 1 dispatches language-appropriate static reviewers against the files being deployed. Stage 2 wraps the deploy in the Phased Build Protocol (pm_invocations row, done criteria, Codex Point A). Nothing deploys until Stage 1 returns SHIP or SHIP-WITH-HEDGES.

## Prompt

```
You are executing a two-stage operational hardening sequence before deploying code.

## Context

Before doing anything else, ask the user:
1. What are we deploying? (project name or description is enough)
2. Where is it going? (deploy target — if unknown, suggest options based on the repo)

For anything the user doesn't know (ADR number, file paths, repo path), look it up yourself:
- ADR: check `~/repos/claude-config/decisions/` for the most recent ADR matching the project name
- Files: check git status and recent commits in the repo to identify what's changed
- Repo path: infer from the project name or ask once if truly ambiguous

Do not block on information you can find yourself.

## Stage 1 — Code Review

Invoke the `reviewer` skill on every file in FILE_LIST. Dispatch language-appropriate reviewer subagents in parallel (bash-reviewer for .sh, python-reviewer for .py, typescript-reviewer for .ts/.tsx, sql-reviewer for .sql, powershell-reviewer for .ps1). Aggregate results into a single worst-of verdict:

- SHIP (0 HIGH, 0 MED, ≤2 LOW) → proceed to Stage 2
- SHIP-WITH-HEDGES (0 HIGH, ≥1 MED) → fix inline, then proceed to Stage 2
- NEEDS-FIXES (≥1 HIGH) → stop, surface findings, do not deploy

Do not proceed to Stage 2 unless Stage 1 verdict is SHIP or SHIP-WITH-HEDGES.

## Stage 2 — Hardened Deploy

Invoke the `project-manager` skill in `dispatch` mode with the following context:

- Build name: operational deploy of [files identified in Stage 1]
- ADR: [most recent ADR matching this project from ~/repos/claude-config/decisions/]
- Deploy target: [confirmed by user in Context step]
- Repo: [inferred from project name or git context]
- Stage 1 verdict: [verdict from Stage 1]

The project-manager skill will organize execution: open the pm_invocations row, map phases to skills/agents, enforce read-before-dispatch (Gate 0a), run Codex Point A before deploy, verify done criteria with real side-effect checks, and close the invocation row.

Do not proceed to Stage 2 if Stage 1 verdict is NEEDS-FIXES.
```
