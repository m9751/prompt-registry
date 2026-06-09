# PRM-CDXP-002 — Iteration log

Living record while the prompt is refined. **Not dispatch-ready** until ship gate is met.

## North star

**Reliable, consistent agent execution** — any capable agent clones the repo, follows one documented path, runs canonical commands, verifies completion, and stops the same way every time without tribal knowledge.

## Current snapshot

| Field | Value |
|-------|-------|
| **Version** | `1.6.2` |
| **Source** | `PRM-CDXP-002_repo-structure-audit.md` |
| **Compiled** | `dist/prompts_latest.json` |

### v1.6.2 — 2026-06-08 (playbook Step 1a + 8c wire)
- Track A: README "For Claude" must be repo-specific per playbook Step 1a template — generic filler → partial.
- Track A: Step 8c rules frontmatter row when `rules/` present (`last_incident`, `recurrence_count`, `load_bearing`).
- P1: generic "For Claude" filler; Step 8c partial/missing on rules corpus (not P0).

### v1.6.0 — 2026-06-09 (drift compare)
- §0 Audit metadata: audited_at, repo_path, remote, git_sha, branch, prompt/playbook version.
- §13 JSON snapshot (`prm-cdxp-002-snapshot-v1`) — scores/statuses only, persist for next run.
- §14 Drift delta when `<prior_audit_result>` injected (resolved/regressed/metric_delta/verdict_change).
- Optional variable: prior_audit_result (§13 JSON from previous run).

| **Status** | Iterating — live-test panel (v1.5.1) |

## Version history

### v1.5.1 — 2026-06-09 (live test #1 learnings)
- Dispatcher: `--add-dir $HOME/repos/smokin-os` documented in Overview + playbook_authority.
- Intake disambiguation: default code-repo when CI/scripts exist; org AGENTS.md ≠ knowledge-wrapper.
- B-routing gate: only when manifest.json, contract table, or routing_type frontmatter.
- Track B n/a: `.env.example` when no env surface; CI parity when no CI.
- Audit extensions relabeled (was Step 4e/1g gap refs).
- code-repo good_example_anchor added.
- P0 playbook gaps tied to cold-start/command parity blockers only.

### v1.5.0 — 2026-06-09 (playbook wire)
- **Playbook authority:** read `$HOME/repos/smokin-os/spec/new-repo-playbook.md` (or `$PLAYBOOK_ROOT`) before audit.
- **Step 0 intake:** playbook repo type (docs-only-index | code-repo | knowledge-wrapper | app/service | mixed) governs active tracks.
- **Track A:** navigation, governance, authority — Steps 1–3, 5, 8–9 gap table.
- **Track B:** code + app/service — Makefile, CI parity, `.env.example`, command path.
- **Track B-routing:** Steps 4, 6, 7 when multi-domain/routing detected.
- **Output §2:** Playbook conformance gap table + `playbook_conformance_pct`.
- **good_example_anchor:** playbook-conforming targets by repo type (replaces fictional-only anchor).
- Line cap 240; section 12 max 3 bullets.

### v1.4.0 — 2026-06-08 (Claude review)
- Workflow cartography cap: metadata only when >3 workflow files.
- `<good_example_anchor>`: fictional AERR ~92 target with smell scores.
- Line cap 220; section 11 max 3 bullets.

### v1.2.0 — 2026-06-08
- **Calibration validity:** AERR labeled structural proxy until M9 collected; weights hypothesized.
- **M9 paired_task_outcome:** pass | fail-with-rescue | inconsistent | not-run from injected `<paired_task_result>` (not executed in read-only audit).
- **M9 reconciliation:** calibration_mismatch / proxy_gap flags; validated_verdict vs structural_verdict.
- **Calibration protocol:** discriminant, predictive, consistency tests on 3–5 repo panel.
- Output §11: Calibration status.

### v1.1.0 — 2026-06-08
- Added `<objective>`: reliable + consistent agent execution north star.
- Added `<measurement_system>`: AERR (0–100), 8 raw metrics (M1–M8), verdict gates, audit_confidence.
- Output sections 8–10: AERR scorecard, execution verdict, audit effectiveness.
- `use_for` and Overview updated.

### v1.0.1 — 2026-06-08
- Cwd-first dispatch; sandbox-blocked tracer rules (governance hedges).

### v1.0.0 — 2026-06-08
- Initial structural audit prompt.

## AERR quick reference

| Verdict | Gates |
|---------|-------|
| **Yes** | AERR ≥ 80, M1 ≤ 1, M2 = 0, M6/M7/M8 ≥ 1 |
| **No** | AERR < 50 OR M7 = 0 OR no build path OR M1 ≥ 5 |
| **Partial** | else |

## Open backlog

- [ ] Calibration panel: 3–5 repos + paired fixed task for M9
- [ ] Extend playbook Steps 4e/4f/1g/5b (build/CI/.env) per Desktop analysis
- [ ] Governance re-review after measurement add
- [ ] Tune weights when calibration_mismatch / proxy_gap patterns emerge

## Session notes

- **2026-06-08:** User objective = perfect agent execution; prompt now measures effectiveness via AERR + audit_confidence.

- **2026-06-08:** Calibration validity + M9 — know we measure right things only after predictive paired runs.

## Live test — 2026-06-09 (prompt-registry, Codex read-only)

**Dispatch:** `codex exec -s read-only -C prompt-registry --add-dir smokin-os`  
**Duration:** ~132s | **Output:** 143 lines, all 12 sections  
**Repo verdict:** AERR 68 Partial, playbook_conformance 28%

### Prompt worked
- 12-section contract, playbook read, gap table, AERR arithmetic, sandbox-blocked handling

### Prompt friction (v1.5.1 candidates)
1. Dispatcher must `--add-dir` playbook root — not documented in prompt
2. Repo type over-classified `mixed` → B-routing over-applied (manifest P0)
3. B-routing denominator: need applicability gate (manifest vs org AGENTS folders)
4. `.env.example` should be n/a when no env surface
5. Step 4e/1g cited but not in playbook yet
6. Missing code-repo `good_example_anchor`

**Artifacts:** Desktop `PRM-CDXP-002-live-test-log.txt`, `PRM-CDXP-002-live-audit-prompt-registry.md`

### Live test #2 — 2026-06-09 (smokin-os, Codex v1.5.1)

**Result:** docs-only-index ✓, playbook 75%, AERR 20 No (false negative)  
**v1.5.1 fixes validated:** type classification, B-routing gate, P0 severity, applicable_count  
**v1.5.2 candidates:** docs-only alternate AERR/verdict; Tracer B/C n/a; execution smells n/a; M1 boundary rule

### v1.5.2 — 2026-06-09 (live test #2 learnings)
- docs-only-index: Tracer B/C n/a; execution smells n/a; navigation AERR formula + verdict gates.
- M1: cross-repo boundary pointers not scavenger when README declares runtime elsewhere.
- good_example_anchor: docs-only uses navigation AERR + playbook_conformance_pct.

### Live test #3 — 2026-06-09 (smokin-knowledge, Codex v1.5.2)
**Result:** knowledge-wrapper ✓, playbook 43%, AERR 40 No — needs navigation mode extension  
**v1.5.3 candidate:** knowledge-wrapper without executable code → navigation-weighted AERR

### smokin-os re-run (v1.5.2 validation)
navigation AERR 45, verdict Partial (fixed false negative from test #2)


### v1.5.4 — 2026-06-09 (smokin-mirror feedback)
- Dependency hygiene n/a for navigation-primary repos with no runtime dependency surface.
- M3_max navigation mode: 10 (was 12).
- smokin-mirror re-run: navigation AERR 65 (was 45), verdict Partial unchanged.

### v1.5.3 — 2026-06-09 (live test #3 learnings)
- Navigation-primary flag: docs-only-index OR knowledge-wrapper without Track B.
- Navigation mode AERR/verdict extended to knowledge-wrapper docs-only repos.
- Track A legacy partial rules for docs/specs and lessons paths.
- Step 7 reviewer paths: agents/ or .claude/agents/.
- smokin-knowledge re-run: navigation AERR 32, verdict Partial (was No at v1.5.2).


### prompt-registry re-run (v1.5.3 validation)
code-repo ✓, B-routing n/a ✓, .env n/a ✓, AERR 68 Partial — disambiguation fix confirmed.

### Live test #4 — 2026-06-09 (smokin-mirror, Codex v1.5.3)
**Repo:** https://github.com/m9751/smokin-mirror  
**Result:** docs-only-index, playbook 50%, nav AERR 45, Partial  
**Agent feedback (3/3):** Dependency hygiene should be n/a for manifest-free docs-only repos  
**v1.5.4 candidate:** docs-only Dependency hygiene n/a rule


### v1.5.5 — 2026-06-09 (smokin-mirror tracer feedback)
- Tracer gate moved first: navigation-primary → Tracer A only; B/C steps skipped entirely.
- Tracer B/C sections labeled "(navigation-primary = false only)".

### v1.6.1 — 2026-06-09 (Codex feedback batch)
- CI cartography: always metadata-only; ≤3 workflows max 30 lines; >3 filenames only.
- severity_bands: P0/P1/P2 hygiene rules (.gitignore, LICENSE = P2 never P0).
- §13 validation: schema prm-cdxp-002-snapshot-v1, gap counts must reconcile, verdict enum Yes|Partial|No.

