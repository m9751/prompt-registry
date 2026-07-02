# Feedback-Harvest Playbook

**Purpose.** Turn what the SmokinTerritory operating system has *learned* into
enforced improvements without applying findings randomly and breaking things.

The system has several feedback mechanisms. Four of them carry harvestable
signal. This playbook sequences them, and each has a dedicated registry prompt
that hard-gates action behind an operator-approved diagnosis.

---

## The prime directive

Harvest, do not apply blindly. Every harvest prompt runs in two phases:

1. **Current-state diagnosis (read-only).** Classify every candidate finding
   (REAL / NOISE / DUPLICATE / LANDED / SUPERSEDED / STALE). Present the table.
   **STOP.** No file is edited in this phase.
2. **Apply-after-approval.** Act only on the findings the operator marks REAL /
   OPEN. Branch + PR for every change; prove each landing against a live
   artifact, never against intent.

A flagged pattern is a hypothesis, not a mandate. The rules=0 / missing=159
Pipeline-F dead-path incident (a renamed corpus path that flagged every pattern
as missing for weeks) is why phase 1 exists.

---

## The four mechanisms and their prompts

Run in this order — 1-3 discover and harvest, 4 verifies what landed. Running 4
first would find gaps that 1-3 are about to fill.

| # | Mechanism | Prompt | What it harvests |
| :--- | :--- | :--- | :--- |
| 1 | **Pipeline-F** | `PRM-INFRA-003` | Recurring session patterns + missing-rule candidates from the automated transcript sweep. Highest signal density (already quantified). |
| 2 | **FMD (smokin-coffee)** | `PRM-INFRA-004` | Human-written failure lessons; find the ones still OPEN (valid but never hardened into a rule/hook/memory). |
| 3 | **Memory (MEMORY.md + Hindsight)** | `PRM-INFRA-005` | Drift (stale, duplicate, contradicting entries) and corrections that recur often enough to become a rule. |
| 4 | **Rule ladder + cross-machine inbox** | `PRM-INFRA-006` | Coverage check: did the lessons from 1-3 actually harden into enforced rules/hooks and reach both machines? Not a discovery pass. |

**Priority rationale.** Density and independence. Start where signal is already
concentrated and quantified (Pipeline-F), then the curated human log (FMD), then
the noisy-but-large store (memory) for drift, and finally the plumbing
(ladder/inbox) as a did-it-land verification.

---

## Shared guardrails (every prompt inherits these)

- **Read before acting.** Cite the artifact read this session; never act from
  recall. A memory reflects what was true when written — spot-check that a named
  file/flag/PR still exists before trusting it.
- **Reuse, don't reinvent.** Route findings to the existing homes — the rule
  ladder (`law/` + CLAUDE.md + hooks), the memory format, this prompt registry's
  rubric standard. No parallel systems, no new tables.
- **claude-config edits are off-main, branch + PR.** Never edit on main.
- **A hook is not enforced until registered + installed.** Registering in
  `settings.json` is not activation; run the machine's install (Mac
  `make install` / Win11 `scripts\install.bat`) and prove it fires live.
- **An inbox note is "sent" only when on origin/main** — confirm `ON ORIGIN`.
- **merge=union files can't delete lines via squash when main diverged** —
  rebase + `--merge`, verify with `git show origin/main:FILE | wc -c`.

---

## How the prompts and this playbook stay linked

Each of `PRM-INFRA-003` through `PRM-INFRA-006` opens with a pointer back to this
playbook (Overview section). This file points forward to all four (table above).
Bidirectional, in-repo — the links can't rot across a repo boundary.

**Prompt source:** `prompts/systems-architecture/PRM-INFRA-00{3,4,5,6}_*.md`
**Compiled contract:** `dist/prompts_latest.json` (what agents/apps consume)
