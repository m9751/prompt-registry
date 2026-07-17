# PRM-INFRA-007 — Lessons learned (build + smoke test)

Living record for the repo-hardening loop prompt. Captures what the build and the first smoke test taught, so the lessons feed back into the `loop-consultant` advisor (smokin-knowledge) and future loop prompts.

## Origin

`loop-consultant` (smokin-knowledge name-dispatched advisor) analyzed the 28 prompt-registry prompts and picked **PRM-CDXP-002** as the strongest loop-engineering fit: verdict **FIT-WITH-HEDGES**, candidate family **`agent-loops:swe-loop`**. Its two hedges were the disciplines CDXP-002 lacks: one-change-per-iteration and explicit termination. The consultant's key structural finding: the loop wraps CDXP-002 (audit -> fix one gap -> re-audit + M9 -> repeat); CDXP-002 itself stays a read-only measurement. That drove the decision to ship a NEW sibling prompt (INFRA-007) rather than mutate the audit.

## Build decisions

- **New sibling prompt, not a rewrite of CDXP-002.** CDXP-002's `<action_safety>` is READ-ONLY; a mutating loop inside it would contradict its own contract. INFRA-007 is the writable driver; CDXP-002 is its read-only feedback signal. Separation of powers is explicit (`<the_signal_is_read_only>`): the driver may only write files under Target_Repo_Path and may never edit the audit, the playbook, or the M9 task. That is the "ground-truth signal is read-only" discipline made architectural.
- **Five-ingredient shape from `swe-loop`.** program / artifact / feedback signal (CDXP-002 AERR + M9) / run ledger / termination — mapped onto CDXP-002's real interface (`<prior_audit_result>` injection gives the §14 drift delta that the loop uses to attribute a fix; `<paired_task_result>` carries M9).

## Smoke test — 2026-07-17 (prompt-registry, simulated CDXP-002 via a driver agent, budget 2)

**Result:** loop terminated correctly at **baseline (Iteration 0)** on RESOLVED — prompt-registry already scores at the bar ([SIMULATED-AUDIT] AERR 100, M9 pass, no P0, playbook_conformance ~96%). No fix applied, no files touched.

**What this validated:** the termination gate fires correctly and the loop does not churn a repo that is already ready. Baseline measurement + M9 + ledger row 0 all produced as specified.

**What this did NOT exercise (known limitation):** because the repo was already at the bar, the fix -> re-measure -> attribute -> keep/revert path never ran under pressure. A real validation must run against a repo with an OPEN P0/P1 gap (a deliberately-degraded fixture, or a genuinely mid-readiness repo) so the keep/revert branch is exercised. Carry-forward. **RESOLVED 2026-07-17 — see degraded-fixture validation below.**

**Friction found in v1.0.0 (all fixed in v1.0.1):**
1. "Save snapshot" did not say where -> now writes `/tmp/infra007-snapshot-{n}.json`.
2. Prior-snapshot injection mechanics unspecified -> now "trailing `<prior_audit_result>{JSON}</prior_audit_result>` block in the dispatch".
3. "flat" (in EXHAUSTED) undefined -> now "AERR unchanged AND structural_verdict unchanged AND no gap reached drift_class = resolved".
4. Keep/revert "M9 did not regress" was uncheckable when M9 was optionally not re-run -> now "'M9 not re-run' counts as did-not-regress".
5. One-change-per-iteration was clear for playbook-Step gaps but not for smell/metric gaps -> added: for a non-playbook gap (e.g. M2), the ONE gap is the metric itself even if it touches README+Makefile+CI.
6. **Signal-shape mismatch:** CDXP-002 emits `metrics.M9` as a derived value in its §13 JSON, not the granular `paired_task_result` block INFRA-007 referenced. Clarified: the driver records run1 as a `<paired_task_result>` block and injects it (or sets M9 from the observed run); M9 runs AFTER the read-only audit, never during it.

## Degraded-fixture validation — 2026-07-17 (the keep/revert branch, run for real)

Ran the loop against a purpose-built degraded repo (`~/repos/_infra007-fixture`, a throwaway git repo, not shipped) so the fix -> re-measure -> attribute -> keep/revert path ran under real pressure. Signal path was the REAL one: `codex exec -C <fixture> -s read-only --add-dir $HOME/repos/smokin-os` dispatching the compiled PRM-CDXP-002 `prompt_text`, prior snapshot injected each iteration as `<prior_audit_result>`.

Fixture seeded with genuine, closeable gaps: README command-parity break (`make compile` vs Makefile/CI `make build`), no authority pointer in AGENTS.md, no STATUS.md / spec/README.md / CLAUDE.md, README not Step-1a shape, no `.env.example`.

**Run ledger (real audits, one change per iteration):**

| iter | gap_picked | file | aerr b->a | verdict b->a | conformance b->a | decision | note |
|---|---|---|---|---|---|---|---|
| 0 | (baseline) | - | -> 0 | -> No | -> 23 | - | baseline measure only; 2 P0s open |
| 1 | command_parity (P0) | README.md | 0 -> 50 | No -> Partial | 23 -> 33 | KEEP | M2 2->0, M5 no->yes, gap drift_class=resolved |
| 2 | authority_pointer (P0) | AGENTS.md | 50 -> 50 | Partial -> Partial | 33 -> 37 | KEEP | gap missing->partial, AERR flat, no regression |
| 3 | (deliberate non-fix) | src/widget.py | 50 -> 50 | Partial -> Partial | 37 -> 37 | REVERT | no gap resolved, flat signal -> discard |

**What this validated (that the baseline-only smoke test could not):**
- **KEEP on real improvement** (iter1): a single command-parity fix moved AERR 0->50 and flipped the verdict, fully attributable because exactly one file changed. The §14 drift delta independently confirmed `command_parity` and `ci_command_parity` reached drift_class=resolved.
- **KEEP on partial resolution + flat AERR** (iter2): authority-pointer went missing->partial (auditor withheld `present` because Step 2 also wants the pointer in CLAUDE.md, which does not exist yet). The keep-rule "gap resolved with AERR flat and no regression elsewhere" fired correctly, and the partial gap carries forward.
- **REVERT on a non-improving change** (iter3): a src docstring touched a file but resolved no structural gap; the loop detected zero gaps at drift_class=resolved and a flat signal, and reverted. This is the branch the first smoke test never reached.
- **Prior-snapshot injection** (v1.0.1 fix #2) worked end to end: every iteration got a real §14 drift table diffing against the previous snapshot.

**New friction found (feeds v1.0.2, not yet applied):**
1. **Dispatch-as-arg fails at scale.** INFRA-007 says "dispatching the compiled PRM-CDXP-002 prompt_text" (implying a CLI arg). At ~40 KB with `<prior_audit_result>` injected, `codex exec "<huge string>"` hangs on "Reading additional input from stdin" and never runs. **Fix:** pass the prompt on **stdin** (`codex exec -C ... -s read-only --add-dir ... < prompt.txt`) — codex reads the prompt from stdin when no PROMPT arg is given. INFRA-007's `<program>` should say stdin dispatch, not arg dispatch, for the re-audit step.
2. **Background `&` masks the child exit.** Launching the audit with a trailing `&` inside a tool call returns the wrapper's exit 0 while the codex child is still running (the known nohup-detached trap). A loop driver must confirm the audit process actually finished (poll `pgrep -f "codex exec"`) before reading the snapshot, or it will parse an empty/partial file. INFRA-007's re-measure step should note: verify the audit process settled before attributing.
3. **Revert is a `git checkout --` that a safety net may block.** The clean revert of an uncommitted non-improving fix is `git checkout -- <file>`, which a discard-guard can block. `git stash push -u <file>` is the non-destructive equivalent and clears the guard. INFRA-007's REVERT step should prefer stash over checkout so it survives a discard-guarded environment.

## Transferable lesson -> fold into `loop-consultant`

**Lesson (loop-signal interface check):** when the consultant calls a FIT and names an existing prompt/tool as the loop's feedback signal, it should verify that the signal actually EMITS the fields the loop will consume, in the shape the loop needs. CDXP-002 emits a derived `metrics.M9`, not the run1/run2 `paired_task_result` the driver wanted — a real integration seam the fit verdict glossed. The consultant's Stage-1 discipline checks (one-change, adversarial signal, read-only signal, termination) are about the LOOP's design; this adds a check about the SIGNAL's output contract: does the named signal expose an injectable prior-state and a machine-readable score the loop can diff? If not, the FIT carries an integration hedge, not a clean FIT.

**Recommended loop-consultant addition:** a fifth Stage-1 check — "Signal I/O contract: the feedback signal must (a) expose a machine-readable score the loop can compare across iterations, and (b) accept the loop's prior-state so re-measurement is a diff, not a fresh guess. If the signal only emits prose or cannot ingest prior state, flag it as a FIT-WITH-HEDGES integration gap."
