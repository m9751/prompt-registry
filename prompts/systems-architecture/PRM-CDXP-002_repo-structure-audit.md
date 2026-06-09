---
id: PRM-CDXP-002
title: Repository Structure Audit — Skeleton, Not Content
domain: systems-architecture
source_format: Git repository (filesystem)
target_orchestrator: Codex exec (read-only)
downstream_consumer: Principal engineer / repo builder / agent onboarding
version: 1.7.0
last_updated: 2026-06-09
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-CDXP-002_repo-structure-audit.md
use_for: Measure whether a repo enables reliable, consistent agent execution — structural readiness scorecard with AERR metrics, not business-logic review
---

## Overview

**What this is:** A read-only structural audit prompt for Codex. Measures whether a repo supports **reliable, consistent agent execution** — not whether implementation logic is correct.

**What you get:** **Audit metadata** (timestamp, git SHA, prompt/playbook versions), playbook repo-type classification, **Track A/B gap table**, repo map, tracer results, smell checklist (0–2), **AERR scorecard** (0–100), optional **M9 paired-task validation**, ranked failures (P0/P1/P2), minimal fix order (max 5), verdict, **JSON snapshot for drift compare**, and optional **§14 drift delta** when a prior audit is injected.

**Calibration:** AERR alone is a hypothesis until paired with a fixed agent task (M9). Dispatcher may inject `<paired_task_result>` from a separate execution run.

**How to run:** `codex exec -C <repo-path> -s read-only --add-dir $HOME/repos/smokin-os` with compiled `prompt_text` from `dist/prompts_latest.json`. Codex cwd is authoritative — no path substitution in the prompt body required. The playbook lives outside the audit repo; `--add-dir` (or `--add-dir $PLAYBOOK_ROOT`) is required for read-only sandbox access.

**Variables:** None required. Dispatch sets the repo via `-C`. Optional: inject `<prior_audit_result>` (§13 JSON from a previous run) for drift delta. Operator should persist each run's §13 JSON for the next compare.

**Two-artifact rule:** Authors edit this `.md` file; agents and apps consume `prompt_text` from `dist/prompts_latest.json` after `python scripts/compile_prompts.py`.

**Registry feedback:** Compiled JSON appends a score + one-line miss ask after the primary output. Complete §0–§14 first, then answer that feedback block. Do not duplicate the footer in this `.md` source — the compiler injects it.

## Prompt

```
<task>
Perform a READ-ONLY repository structure audit on the repository at your current working directory (git root). The dispatcher sets cwd via `codex exec -C`; treat cwd as authoritative for all commands and path references.

Scope: STRUCTURE ONLY — layout, boundaries, build/install path, CI/CD skeleton, config layering, docs/onboarding surfaces, generated-vs-source separation, test placement, release path.

Out of scope: business logic correctness, algorithm quality, variable naming, full dependency vulnerability scan, line-by-line code review.
</task>

<objective>
North star: **reliable, consistent agent execution**.

A capable agent cloning this repo should be able to orient, run the canonical commands, verify completion, and stop — **the same way every time** — without tribal knowledge or human rescue.

Reliable = documented path works; failures are classifiable (missing-prereq, missing-credential, doc-conflict, sandbox-blocked).
Consistent = README, scripts, and CI agree on one command authority; repeated runs follow the same entrypoints.

You are an expert repo builder measuring gap-to-perfect agent execution — not reviewing code quality.
</objective>

<standard_paired_task>
Canonical M9 task — same instructions on every repo (executed in a separate writable run; not during this read-only audit):

Orient using only README, AGENTS.md, Makefile, justfile, and .github/workflows. Find the documented lint or verify command and the smallest documented build command. Run verify, then build. Report: each command used, pass/fail/sandbox-blocked, artifact path or blocker class (missing-prereq, missing-credential, doc-conflict, sandbox-blocked). Do not invent commands. Ask the operator only if credentials are required. Run twice with identical instructions; record whether commands and outcome match.
</standard_paired_task>

<playbook_authority>
Before cartography, read the canonical new-repo playbook (read-only):

Default path: `$HOME/repos/smokin-os/spec/new-repo-playbook.md`
Override: if `$PLAYBOOK_ROOT` is set, use `$PLAYBOOK_ROOT/spec/new-repo-playbook.md`

If the file is missing or unreadable, record P1 finding `playbook-unavailable` with attempted path and continue the audit without playbook gap scoring. Do not invent playbook requirements from memory.

**Dispatcher prerequisite:** playbook path is outside audit cwd. Operator must pass `--add-dir` for the playbook root (default: `$HOME/repos/smokin-os`; or `$PLAYBOOK_ROOT` when set).

The playbook defines two conformance tracks:
- **Track A (all repo types):** navigation, governance, authority hierarchy — Steps 1–3, 5, 8–9
- **Track B (code + app/service only):** Makefile/justfile, CI command parity, `.env.example`, documented command path — supplements Track A; AERR tracers measure execution truth

**Track B-routing (optional):** when repo has multiple domains, subagents, or routing rules (knowledge-wrapper, multi-domain code, app/service), also check playbook Steps 4, 6, 7.
</playbook_authority>

<intake>
Step 0 — Playbook repo type (classify first; governs which tracks apply):

| Playbook type | Apply |
|---|---|
| docs-only-index | Track A only |
| code-repo | Track A + Track B |
| knowledge-wrapper | Track A + Track B-routing (Track B if executable code present) |
| app/service | Track A + Track B |
| mixed | Superset of all applicable tracks — cite which types overlap; use only when disambiguation rules below cannot pick one primary type |

**Disambiguation rules (apply in order):**
1. **Default to code-repo** when compiler/build scripts or CI validate jobs exist — even if `prompts/*/AGENTS.md` or similar folders exist for organizational domains.
2. **knowledge-wrapper** only when root `manifest.json` exists OR ≥2 domain `AGENTS.md` files carry `routing_type` frontmatter OR root `AGENTS.md` has a domain contract/routing table — not merely per-folder docs.
3. **mixed** only when two primary types are equally load-bearing (e.g., docs-only root index + separate executable service tree with deploy signals). State which tracks each type contributes.
4. Organizational subfolder `AGENTS.md` without routing frontmatter/contract table does **not** trigger knowledge-wrapper or B-routing.

Infer type from artifacts only [OBSERVED] or [HYPOTHESIS]:
- docs-only-index: `DOCS_ONLY.md` or no build manifests and no runnable entrypoints
- code-repo: build manifests/scripts or CI validate jobs, not primarily a deployed runtime
- knowledge-wrapper: root `manifest.json` OR routing frontmatter/contract table as above
- app/service: deploy/runtime signals (Dockerfile, CI deploy job, API server, DB migrations)
- mixed: two or more primary types with equal weight per rule 3

Also record (label [OBSERVED] or [HYPOTHESIS]):
1. Legacy shape: app | library | monorepo | infra | template | mixed
2. Deployable unit(s): binary, container, static site, npm package, Mule JAR, etc.
3. Primary consumer: human dev | CI | agent | customer artifact
4. Definition of "works": builds | tests pass | deploys | demo runs | navigates correctly

State playbook repo type and all four legacy fields at the top of the report. If ambiguous, list interpretations and which tracer or playbook check disambiguates.

**Navigation-primary flag:** set when playbook type = docs-only-index OR (knowledge-wrapper AND Track B is not active — no build scripts, no CI validate jobs, docs declare no executable entrypoints). Navigation-primary repos use navigation AERR in §9, not default execution AERR.
</intake>

<playbook_conformance>
After intake, compare the repo to the playbook requirements that apply to its classified type. Do not score requirements outside the active tracks.

### Track A checklist (all types)
For each row: present | partial | missing | n-a — with evidence (path, section, or quote ≤1 line).

| Requirement | Playbook ref |
|---|---|
| README: identity + reading-order table + boundary + "For Claude" (repo-specific rules per Step 1a template — not generic filler) | Step 1a |
| Rules file frontmatter (`last_incident`, `recurrence_count`, `load_bearing`) on each `rules/*.md` | Step 8c |
| AGENTS.md: identity, nav, key constraint, primary task, NEVER, git workflow | Step 1b |
| CLAUDE.md exists (repo-specific or explicit minimal stub) | Step 1c |
| STATUS.md: current phase + open items | Step 1d |
| spec/README.md: one row per spec file | Step 1e |
| spec/lessons.md with founding entry | Step 3a |

**Track A legacy n/a / partial rules:**
- `spec/README.md` → **partial** (not missing) when an equivalent spec index exists elsewhere (e.g., `docs/specs/` with README or indexed list) — cite path and gap vs playbook layout.
- `spec/lessons.md` → **partial** when incident/decision log exists under another path (e.g., `docs/specs/`, `spec/lessons.md` missing but lessons content elsewhere) — do not mark missing solely because path differs on legacy repos.
- README Step 1a "For Claude" → **partial** when section exists but rules are generic agent etiquette (e.g., "be careful", "read docs") without repo-specific paths, install steps, or boundaries — playbook Step 1a requires worked-example shape.
- Step 8c rules frontmatter → **n-a** when no `rules/` directory at repo root or under documented mirror path (e.g., `claude-config/rules/` when repo is the rules mirror). When `rules/` exists, score **partial** if some files lack frontmatter; **missing** if majority lack it.
| Authority hierarchy + pointer directive in AGENTS.md | Step 2 |
| Significant specs: valid-as-of + falsification-pointer + review-trigger | Step 8a |
| Cold-agent navigation test evidence (or [HYPOTHESIS] not yet run) | Step 5 |
| Git workflow documented in AGENTS.md | Step 9 |

### Track B checklist (code-repo + app/service only)
| Requirement | Playbook / audit ref |
|---|---|
| Canonical command surface (Makefile, justfile, or documented script entry) | Audit extension + Tracer B |
| bootstrap / build / verify / lint documented in one front door | Tracer A/B/C |
| CI workflow runs same commands as docs/scripts (or n-a if no CI) | Tracer C + smell CI truth |
| `.env.example` or config matrix for required env | Audit extension + smell Config hierarchy |
| Command parity: README = scripts/Makefile = CI (M2 = 0) | Tracer C |

**Track B n/a rules:**
- `.env.example` → **n/a** when no `.env*` references in docs, no credential prerequisites, and build/verify needs no env vars [OBSERVED].
- CI parity row → **n/a** when no CI workflows and docs explicitly state local-only workflow.

### Track B-routing (routing repos only — gate before scoring)
**Apply B-routing only when at least one holds [OBSERVED]:**
- root `manifest.json` exists, OR
- root `AGENTS.md` domain contract/routing table, OR
- ≥2 `*/AGENTS.md` with `routing_type` frontmatter.

If gate fails, mark all B-routing rows **n-a** — do not score or elevate to P0.

| Requirement | Playbook ref |
|---|---|
| manifest.json at root with valid schema | Step 4a |
| Pointer directive in AGENTS.md + CLAUDE.md | Step 4b |
| Per-domain AGENTS.md with frontmatter + 5 hard rules | Step 6 |
| Reviewer subagent per language domain | Step 7 |
| Manifest domain count matches contract table | Step 4c–4d |

**Step 7 reviewer paths:** accept `agents/<domain>-reviewer.md`, `.claude/agents/<domain>-reviewer.md`, or equivalent name-dispatchable reviewer file linked from domain AGENTS — cite actual path.

Compute **playbook_conformance_pct** = round(100 * (present_count + 0.5*partial_count) / applicable_count). **n-a rows excluded from denominator.** State `applicable_count`, `present_count`, `partial_count`, `missing_count` explicitly in §2 (these must match §13 JSON).

**P0 from playbook gaps:** only when gap blocks Step 5 cold-agent navigation or documented command parity on an active track — not for n/a or inactive B-routing rows.

Deliverable: **Playbook gap table** — columns: Track | Requirement | Status | Evidence | Playbook ref.

<severity_bands>
Apply when ranking §7 P0 / P1 / P2:

**P0 (cold-start or command-truth blockers):**
- Missing authority pointer (Step 2) on any repo with AGENTS.md
- Missing manifest pointer (Step 4b) when B-routing gate is active
- Command parity failure (M2 > 0) on active Track B
- Playbook gap explicitly marked P0 above

**P1 (navigation reliability):**
- Missing `spec/README.md` / equivalent index (partial only if indexed elsewhere — still P1 until playbook path exists)
- Missing `STATUS.md`, fragmented front door (M7 = 1), missing Step-5 test evidence
- README not Step-1a shape, "For Claude" generic filler (Step 1a partial), missing `spec/lessons.md` when no legacy partial path
- Rules frontmatter gaps on active `rules/` corpus (Step 8c partial/missing) — P1 not P0 unless blocks governance audit

**P2 (hygiene and cosmetic — never P0):**
- Missing root `.gitignore`, committed `.DS_Store` / OS junk, missing `LICENSE`
- Inconsistent spec staleness anchors when specs exist
- Dead weight smell = 1 without committed generated artifacts

Do not promote hygiene-only findings to P0 even on knowledge-wrapper repos.
</severity_bands>

<cartography>
Produce a repo map WITHOUT reading implementation logic under src/, lib/, or equivalent application trees.

Allowed reads: playbook path from `<playbook_authority>` (metadata only — do not paste full playbook into output); README*, CONTRIBUTING*, DOCS_ONLY.md, AGENTS.md, CLAUDE.md, STATUS.md, spec/**, docs/specs/**, manifest.json, Makefile, justfile, package.json, pyproject.toml, go.mod, pom.xml, Dockerfile*, docker-compose*, .github/workflows/*, .gitlab-ci.yml, Jenkinsfile, .gitignore, .env.example, config manifest filenames, docs/ index files, agents/*-reviewer.md, .claude/agents/**, deploy scripts at repo root, top 2 directory levels.

Run and capture:
- Root listing
- Build manifest discovery (exclude node_modules, .git, target, dist, .next)
- Config surface paths only (.env*, config.*, *values*.yaml) — never echo secret values
- CI workflow inventory — **metadata only, always.** Never read full workflow YAML bodies.
  - **0 workflows:** record `none` [OBSERVED].
  - **1–3 workflows:** per file, read at most the first 30 lines and extract only `name`, top-level `on` triggers, and top-level `jobs` keys — no step contents, no env blocks, no action pins.
  - **>3 workflows:** list filenames only from directory listing; do not open files; note count [OBSERVED].
- Docs structure (docs/, ADR*, architecture* folders)
- Generated-artifact signals (.gitignore entries; committed dist/build/target/.next)

Deliverable: one-page repo map — root layout, packages, config surfaces, CI entrypoints, doc entrypoints.
</cartography>

<tracer_bullets>
Log every manual step. Do NOT fix anything.

**Tracer gate (run first):** Check navigation-primary flag from intake.
- If **true:** run **Tracer A only**. Record Tracer B = n-a and Tracer C = n-a with one-line evidence (repo declares no executable entrypoints). **Do not** look up build/verify commands or attempt execution. Proceed to smell checklist.
- If **false:** run Tracer A, then Tracer B, then Tracer C below.

Tracer A — Onboarding path (all repo types)
- Does README or AGENTS.md document clone → orient → (optional install elsewhere) in order?
- Count scavenger-hunt steps (split docs, undocumented env vars, Keychain/VPN/manual prerequisites).
- **Do not count** a cross-repo install/activation pointer as scavenger when README boundary section explicitly declares runtime lives in another repo [OBSERVED].
- **Do not count** build/install omission from README when root Makefile or justfile documents install/build/compile targets [OBSERVED] — Makefile is canonical front door per Tracer B source order.
- **Do not count** verify/lint split between README and Makefile when Makefile defines verify/lint/test targets AND M2 = 0 (no conflicting canonical commands) — at most one scavenger step for doc fragmentation, not two.
- **Do not count** missing root AGENTS.md when CLAUDE.md exists with agent onboarding (primary task + command list or NEVER block) [OBSERVED] — legacy layout; still score Agent onboarding smell = 1.

Tracer B — Build truth (navigation-primary = false only)
- Canonical build command: README, then Makefile/justfile, then CI (note conflicts).
- Run build if safe; if blocked by credentials, record blocker as P0/P1 with evidence.
- If read-only sandbox blocks the build (EPERM, cannot write artifacts), tag finding `sandbox-blocked` — do not promote to repo P0 unless the same failure would occur outside sandbox (e.g., missing script with no sandbox involved).
- Record: pass/fail/sandbox-blocked, time to first artifact, hidden manual steps.

Tracer C — Verify truth (navigation-primary = false only)
- Canonical test/lint command from same sources.
- Does CI run what local docs claim?
- README vs Makefile vs CI mismatch = structural failure even if code is fine.
- Apply the same `sandbox-blocked` rule as Tracer B for verify/lint commands that require writes.
</tracer_bullets>

<smell_checklist>
Score each 0 (missing) | 1 (partial) | 2 (solid) with evidence (path or command). Use rubric anchors:

Single front door — 0: no entry doc | 1: README exists, flow split across files | 2: one linear path in README or AGENTS.md
Deploy mirror — 0: no deploy docs/scripts | 1: manual deploy documented | 2: CI or script mirrors documented deploy
Config hierarchy — 0: secrets/env undocumented | 1: partial .env.example or scattered config | 2: central config map + example file
Dependency hygiene — 0: no lockfile/manifest | 1: lockfile but drift signals | 2: pinned deps, clean ignore rules
Test placement — 0: no test dirs/scripts | 1: tests exist but undiscoverable | 2: obvious test command in docs/CI
CI truth — 0: no CI | 1: CI exists but mismatches docs | 2: CI matches README/Makefile commands
Change safety — 0: no guards | 1: manual checks only | 2: lint/test/pre-deploy scripts or CI gates
Release path — 0: no release docs | 1: manual release documented | 2: scripted or CI release path
Agent onboarding — 0: no AGENTS.md/CLAUDE.md | 1: agent docs exist, fragmented (CLAUDE.md without AGENTS.md = 1, not 0) | 2: dedicated agent entry with commands
Dead weight — 0: generated artifacts committed | 1: some drift in tree | 2: clean tree, .gitignore enforced

**Navigation-primary repos:** mark Deploy mirror, Test placement, CI truth, Release path, and **Dependency hygiene** as **n-a** when no runtime dependency surface exists (no lockfile, package manifest, or dependency docs required for repo operation) — exclude from M3 denominator. Score remaining five smells normally (max 10).
</smell_checklist>

<good_example_anchor>
Reference target: repo conforming to `new-repo-playbook.md` for its classified type — calibrate smell scores and Track A/B gaps toward this, not a repo under audit.

**docs-only-index (Track A only):** playbook_conformance_pct ≥ 85, navigation AERR ≥ 80 (uncalibrated). M7 ≥ 1, M8 ≥ 1, M1 ≤ 1. Strong: reading-order table, authority pointer, spec/README, cold-agent test passed. Execution + dependency smells n/a when no runtime surface.

**knowledge-wrapper, navigation-primary (Track A + B-routing, no executable code):** playbook_conformance_pct ≥ 70, navigation AERR ≥ 65 (uncalibrated). M7 ≥ 1, M8 ≥ 2. Strong: manifest.json + contract table + domain AGENTS + reviewer files + pointer directives. Execution smells n/a; B-routing drives conformance.

**code-repo (Track A + B):** playbook_conformance_pct ≥ 75, AERR ~65–80 (uncalibrated). M2 = 0, M5 = yes when CI exists. Signals: documented script or Makefile for build/verify; README + CI agree on same command (Makefile optional); no B-routing unless gate passes.

**app/service (Track A + B):** playbook_conformance_pct ≥ 85, AERR ≥ 80. M3=20, M1=0, M2=0. Signals: root Makefile with bootstrap/build/verify/lint; README linear clone→build→test; .env.example when env required; one CI workflow running same lint+build as Makefile; AGENTS.md lists exact commands; no generated dirs in tree.

Fictional ceiling (when playbook gaps exist for build/CI): use app/service row above as execution-truth target; navigation gaps map to Track A rows.
</good_example_anchor>

<measurement_system>
Compute **AERR** (Agent Execution Readiness Rating), 0–100. Every metric must cite evidence. Show arithmetic.

### Raw metrics (record all)
| ID | Metric | How to measure |
|----|--------|----------------|
| M1 | scavenger_hunt_count | Integer from Tracer A after exclusions (split docs, undeclared env, manual prereqs each = 1; Makefile-front-door and legacy CLAUDE.md rules apply) |
| M2 | command_conflict_count | Integer: distinct canonical build commands across README / Makefile / CI |
| M3 | smell_total | Sum of applicable smell scores (max 20; max 10 when navigation-primary with 5 smells n/a) |
| M4 | tracer_b | pass \| fail \| sandbox-blocked \| not-attempted \| n-a |
| M5 | tracer_c_parity | yes \| no \| n-a (n/a if navigation-primary, or no CI and docs state local-only verify) |
| M6 | ci_truth_score | Smell row "CI truth" value 0–2 |
| M7 | front_door_score | Smell row "Single front door" value 0–2 |
| M8 | agent_onboarding_score | Smell row "Agent onboarding" value 0–2 |
| M9 | paired_task_outcome | pass \| fail-with-rescue \| inconsistent \| not-run (see paired_task_validation) |

### Calibration validity (read before scoring)
AERR measures **structural proxies** for reliable, consistent agent execution — not execution itself.
Treat AERR as **uncalibrated** until M9 is collected. Weights are hypothesized; predictive validity requires the calibration protocol below.

Structural proxy = doc/CI layout signals that *should* predict agent success.
Validated = M9 confirms or contradicts the structural verdict.

### Paired task validation (M9)
If dispatcher provides `<paired_task_result>`, set M9 from it. Otherwise M9 = not-run.
The paired task text is defined in `<standard_paired_task>` — use that verbatim for run1/run2.

Expected `<paired_task_result>` shape:
- task: text from standard_paired_task
- run1: success|fail, commands_from_docs|invented, human_rescue yes|no
- run2: (optional) same_commands yes|no, same_outcome yes|no
- M9 mapping: pass = run1 success + no rescue + commands_from_docs; fail-with-rescue = fail or rescue or invented commands; inconsistent = run2 differs on commands or outcome; not-run = block absent

Operator may inject `<paired_task_result>` from a separate writable M9 run (calibration panel) or post-hoc after read-only audit completes. When injected, compute validated_verdict and calibration_status per M9 reconciliation below and emit both in §10 and §13.

Do NOT execute the paired task in this read-only audit. Record M9 only from injected results or not-run.

### Calibration protocol (operator — for metric tuning across repos)
Run on a 3–5 repo panel when validating this prompt:
1. **Discriminant** — AERR ordering matches known-good > mixed > known-bad repos.
2. **Predictive** — low AERR correlates with M9 fail-with-rescue on the same fixed task.
3. **Consistency** — two identical agent runs yield same commands and outcome (M9 inconsistent if not).

If predictive test fails for a metric, flag it in calibration_notes and do not treat that metric as validated.

### Makefile front door (legacy code-repo calibration — v1.7.0)
Set **makefile_front_door** = true when root Makefile or justfile exists with documented install OR build OR compile target AND verify OR lint OR test target [OBSERVED]. Record in §9 arithmetic.

### AERR formula (code/app/knowledge-wrapper — default)
smell_pct = (M3 / 20) * 100
If makefile_front_door AND M2 = 0:
  scavenger_penalty = min(M1 * 3, 12)
Else:
  scavenger_penalty = min(M1 * 5, 25)
conflict_penalty = min(M2 * 10, 20)
tracer_bonus = 0
  + 5 if M4 = pass
  + 5 if M4 = sandbox-blocked AND makefile_front_door AND M2 = 0
  + 3 if M4 = sandbox-blocked AND canonical build command exists in docs/scripts AND NOT (makefile_front_door AND M2 = 0)
  + 0 if M4 = fail or not-attempted
  + 5 if M5 = yes
  + 3 if M5 = n/a AND M6 >= 1
  + 0 if M5 = no
AERR_raw = round(smell_pct - scavenger_penalty - conflict_penalty + tracer_bonus)
execution_truth_floor = 50 when makefile_front_door AND M2 = 0 AND M4 in (pass, sandbox-blocked) AND M7 >= 1
AERR = clamp(0, 100, max(AERR_raw, execution_truth_floor)) when execution_truth_floor applies; else clamp(0, 100, AERR_raw)
Show makefile_front_door, AERR_raw, execution_truth_floor (or n/a), and final AERR in §9.

### AERR formula (navigation-primary — navigation mode)
When navigation-primary flag is set, label score **navigation AERR** and use:
- M3_max = 10 (five applicable smells; Deploy mirror, Test placement, CI truth, Release path, Dependency hygiene n/a when no runtime deps)
- smell_pct = (M3 / 10) * 100
- M2 = 0; M4 = n/a; M5 = n/a; M6 = n/a
- scavenger_penalty = min(M1 * 5, 15)  (cap lower — navigation-focused)
- conflict_penalty = 0
- nav_bonus = 0
  + 10 if playbook_conformance_pct >= 85
  + 5 if playbook_conformance_pct >= 70 AND < 85
  + 0 otherwise
- navigation AERR = clamp(0, 100, round(smell_pct - scavenger_penalty + nav_bonus))
Report both navigation AERR and playbook_conformance_pct in §9 for navigation-primary repos.

### Verdict gates (structural — apply after AERR)
**Default (code/app/knowledge-wrapper with active Track B):**
- **Yes** — AERR >= 80 AND M1 <= 1 AND M2 = 0 AND M6 >= 1 AND M7 >= 1 AND M8 >= 1
- **No** — AERR < 50 OR M7 = 0 OR (no documented build path in README/Makefile/justfile/scripts) OR M1 >= 5
- **Partial** — everything else
Documented build path is satisfied by root Makefile/justfile with install/build/compile targets even when README omits a build line. Do not apply AERR < 50 No gate alone when makefile_front_door AND M2 = 0 AND execution_truth_floor applied — structural Partial minimum unless M7 = 0 or M1 >= 5.

**Navigation-primary (navigation mode):**
- **Yes** — navigation AERR >= 80 AND playbook_conformance_pct >= 85 AND M7 >= 1 AND M8 >= 1 AND M1 <= 1
- **No** — M7 = 0 OR playbook_conformance_pct < 50 OR M1 >= 5
- **Partial** — everything else
Do not apply "no documented build path" No gate to navigation-primary repos.

Label this structural_verdict. Prefix with **uncalibrated** when M9 = not-run. Note **navigation mode** when navigation-primary.

### M9 reconciliation (when M9 is not not-run)
Compare structural_verdict to M9 and set **calibration_status**:
- AERR Yes + M9 pass → validated_verdict Yes, calibration_status aligned
- AERR Yes + M9 fail-with-rescue or inconsistent → calibration_mismatch — validated_verdict Partial; list which proxy metrics lied
- AERR Partial + M9 pass → proxy_gap — validated_verdict Partial; note metrics may be too harsh; cite which penalties overshot
- AERR No + M9 pass → calibration_mismatch — validated_verdict Partial; cite false-positive drivers (typically M1 scavenger_penalty, AERR < 50 gate, or missing AGENTS.md counted as scavenger)
- Any M9 inconsistent → cap validated_verdict at Partial, calibration_status calibration_mismatch until repeat-run consistency is fixed

When M9 = not-run: validated_verdict = structural_verdict (uncalibrated), calibration_status uncalibrated, and state paired task still required.

### Audit effectiveness (is this measurement run valid?)
Score **audit_confidence** high \| medium \| low:
- **high** — all tracers attempted, all smells scored, AERR computed with shown arithmetic, every P0/P1 has evidence
- **medium** — one tracer sandbox-blocked or one smell inferred without direct evidence
- **low** — missing smell rows, AERR not computable, or >2 ungrounded claims

If audit_confidence = low, state what blocked measurement and do not claim repo verdict with certainty.
</measurement_system>

<grounding_rules>
- Every works/broken claim cites evidence: command output, file path, or workflow step.
- Do not read business logic under src/ except to count deploy boundaries (e.g., "mulesoft/ contains N apps").
- Never paste secret values — path references only.
- Tag facts [OBSERVED] and guesses [HYPOTHESIS].
</grounding_rules>

<drift_compare>
Every audit must be reproducible and diffable against future runs.

### Collect audit metadata (§0)
Run and record [OBSERVED]:
- `audited_at` — ISO-8601 UTC timestamp at audit start
- `repo_path` — absolute path to git root (cwd)
- `repo_remote` — `git remote get-url origin` (or `none` if unset)
- `git_sha` — `git rev-parse HEAD`
- `git_branch` — `git branch --show-current` (or detached SHA label)
- `prompt_version` — `1.7.0` (PRM-CDXP-002)
- `playbook_version` — from playbook header `Spec version:` line, or `unknown`

### Prior audit injection (optional)
If dispatcher provides `<prior_audit_result>`, parse it as the §13 JSON snapshot from a previous run on the same repo. If absent, skip §14 and set `drift_compare: not-available`.

Expected `<prior_audit_result>` shape: same schema as §13 below (JSON object). May be wrapped in a fenced `json` block or raw JSON.

### §13 JSON snapshot (mandatory — machine-readable)
After completing §1–§12, emit one fenced `json` block tagged `prm-cdxp-002-snapshot`. **Scores and statuses only** — no prose, no evidence strings.

Required fields (emit as valid JSON in output §13):
  schema (must be exactly "prm-cdxp-002-snapshot-v1"), audited_at, repo_path, repo_remote,
  git_sha, git_branch, prompt_version ("1.7.0"), playbook_version, playbook_repo_type,
  navigation_primary, makefile_front_door (boolean), playbook_conformance_pct,
  applicable_gap_count, present_count, partial_count, missing_count,
  aerr_mode (default|navigation), aerr_score, aerr_raw (integer, omit when no floor applied),
  execution_truth_floor (integer or null), structural_verdict (exactly Yes|Partial|No — no suffixes),
  validated_verdict (Yes|Partial|No — same enum; omit when M9=not-run),
  calibration_status (uncalibrated|aligned|proxy_gap|calibration_mismatch),
  audit_confidence, metrics {M1..M9}, gaps [{track, requirement, status, playbook_ref}],
  smells {single_front_door, deploy_mirror, config_hierarchy, dependency_hygiene,
  test_placement, ci_truth, change_safety, release_path, agent_onboarding, dead_weight}

**§13 validation rules (must hold before emitting):**
- `applicable_gap_count` = number of gap rows in §2 where status != n-a
- `present_count + partial_count + missing_count` = `applicable_gap_count`
- Every gap row with status != n-a appears exactly once in `gaps[]`
- `playbook_conformance_pct` = round(100 * (present_count + 0.5*partial_count) / applicable_gap_count)
- Use integers 0–2 for scored smells; string "n-a" for excluded smells
- requirement keys: stable snake_case (e.g., readme_step_1a, authority_pointer, manifest_json)

Operator: save this JSON block after each run; pass it as `<prior_audit_result>` on the next audit of the same repo.

### §14 Drift delta (when prior audit provided)
Compare current §13 snapshot to `<prior_audit_result>`:

| Delta class | Rule |
|---|---|
| **resolved** | gap status improved: missing→partial/present, partial→present |
| **regressed** | gap status worsened: present→partial/missing, partial→missing |
| **unchanged** | same status |
| **metric_delta** | numeric diff for playbook_conformance_pct, aerr_score, each M1–M8 |
| **verdict_change** | prior structural_verdict → current |
| **prompt_mismatch** | if `prompt_version` differs, flag `calibration_warning` — score deltas may reflect prompt change, not repo drift |
| **sha_change** | if `git_sha` differs, note commits between audits |

Deliverable: compact table — `field | prior | current | delta | drift_class`. Max 15 rows; overflow summarized in one bullet.
If no prior audit: `§14 Drift delta — not-available (no prior_audit_result injected)`.
</drift_compare>

<structured_output_contract>
Return markdown in this order:

## 0. Audit metadata — audited_at, repo_path, repo_remote, git_sha, git_branch, prompt_version, playbook_version
## 1. Intake — playbook repo type + legacy shape fields
## 2. Playbook conformance — active tracks, playbook_conformance_pct, gap table (Track | Requirement | Status | Evidence | Playbook ref)
## 3. Repo map
## 4. Tracer results (A/B/C with evidence)
## 5. Smell checklist table
## 6. What works
## 7. What does not — P0 / P1 / P2 (apply severity_bands; hygiene-only = P2)
## 8. Minimal fix order (max 5 structural moves, no refactors — prefer playbook Step refs)
## 9. AERR measurement — raw metrics table, formula arithmetic, AERR score, verdict gates applied
## 10. Agent execution verdict — structural_verdict (uncalibrated if M9 not-run) + validated_verdict + calibration_status (if M9 provided) + one paragraph on reliable/consistent criteria; note playbook vs AERR alignment
## 11. Audit effectiveness — audit_confidence (high/medium/low) + what would raise confidence
## 12. Calibration status — max 3 bullets: M9 value; playbook/AERR mismatch if any; one next step
## 13. JSON snapshot — single fenced `json` block tagged `prm-cdxp-002-snapshot` (schema per drift_compare; scores/statuses only)
## 14. Drift delta — comparison table vs `<prior_audit_result>` if injected; else not-available

Primary output ends at §14. Do not embed prompt score or miss feedback inside §0–§14.

Keep prose sections under 260 lines. §13 JSON is exempt from line cap. If P0 count exceeds 5, sections 6–8 may expand; abbreviate section 12 first, never §13.
</structured_output_contract>

<registry_feedback>
When dispatch uses compiled JSON (`dist/prompts_latest.json`), a compile-time footer follows this prompt — it is NOT part of the audit contract. After §14 is complete, respond to that footer in order:
1. Score: 1 (poor) / 2 (adequate) / 3 (excellent)
2. One line: what this prompt missed or got wrong — **prompt friction only** (ambiguous gate, wrong n/a rule, section ordering, missing playbook ref), not repo fix recommendations.

Do not paste or paraphrase the footer into §0–§14. If consuming the `.md` source only (no JSON footer), skip this step.
</registry_feedback>

<default_follow_through_policy>
Collect §0 metadata (git SHA, branch, remote) first. Read the playbook, classify repo type, score applicable tracks, run cartography and tracers, then emit §13 JSON snapshot. If `<prior_audit_result>` is injected, complete §14 drift delta. Then answer registry feedback (score + one-line prompt friction) when compiled JSON footer is present. Ask no questions unless a tracer is impossible without credentials — then record that as a finding.
</default_follow_through_policy>

<action_safety>
READ-ONLY. Do not modify files, commit, install packages, or deploy.
</action_safety>
```
