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

**What this did NOT exercise (known limitation):** because the repo was already at the bar, the fix -> re-measure -> attribute -> keep/revert path never ran under pressure. A real validation must run against a repo with an OPEN P0/P1 gap (a deliberately-degraded fixture, or a genuinely mid-readiness repo) so the keep/revert branch is exercised. Carry-forward.

**Friction found in v1.0.0 (all fixed in v1.0.1):**
1. "Save snapshot" did not say where -> now writes `/tmp/infra007-snapshot-{n}.json`.
2. Prior-snapshot injection mechanics unspecified -> now "trailing `<prior_audit_result>{JSON}</prior_audit_result>` block in the dispatch".
3. "flat" (in EXHAUSTED) undefined -> now "AERR unchanged AND structural_verdict unchanged AND no gap reached drift_class = resolved".
4. Keep/revert "M9 did not regress" was uncheckable when M9 was optionally not re-run -> now "'M9 not re-run' counts as did-not-regress".
5. One-change-per-iteration was clear for playbook-Step gaps but not for smell/metric gaps -> added: for a non-playbook gap (e.g. M2), the ONE gap is the metric itself even if it touches README+Makefile+CI.
6. **Signal-shape mismatch:** CDXP-002 emits `metrics.M9` as a derived value in its §13 JSON, not the granular `paired_task_result` block INFRA-007 referenced. Clarified: the driver records run1 as a `<paired_task_result>` block and injects it (or sets M9 from the observed run); M9 runs AFTER the read-only audit, never during it.

## Transferable lesson -> fold into `loop-consultant`

**Lesson (loop-signal interface check):** when the consultant calls a FIT and names an existing prompt/tool as the loop's feedback signal, it should verify that the signal actually EMITS the fields the loop will consume, in the shape the loop needs. CDXP-002 emits a derived `metrics.M9`, not the run1/run2 `paired_task_result` the driver wanted — a real integration seam the fit verdict glossed. The consultant's Stage-1 discipline checks (one-change, adversarial signal, read-only signal, termination) are about the LOOP's design; this adds a check about the SIGNAL's output contract: does the named signal expose an injectable prior-state and a machine-readable score the loop can diff? If not, the FIT carries an integration hedge, not a clean FIT.

**Recommended loop-consultant addition:** a fifth Stage-1 check — "Signal I/O contract: the feedback signal must (a) expose a machine-readable score the loop can compare across iterations, and (b) accept the loop's prior-state so re-measurement is a diff, not a fresh guess. If the signal only emits prose or cannot ingest prior state, flag it as a FIT-WITH-HEDGES integration gap."
