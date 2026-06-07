---
id: PRM-INFRA-001
title: Operational Hardening Deploy
domain: systems-architecture
source_format: Code files + ADR + deploy plan
target_orchestrator: Claude Code
downstream_consumer: Human (review then approve)
version: 2.5.0
last_updated: 2026-06-07
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-INFRA-001_operational-hardening-deploy.md
use_for: Review code for correctness then execute a hardened deploy using the Phased Build Protocol
---

## Overview

Two-stage hardening sequence for any deploy. Stage 1 dispatches language-appropriate static reviewers against the files being deployed. Stage 2 wraps the deploy in the Phased Build Protocol (pm_invocations row, done criteria, Codex Point A). Nothing deploys until Stage 1 returns SHIP or SHIP-WITH-HEDGES.

## Prompt

```
You are executing a two-stage operational hardening sequence before deploying code.

## Step 0 — Gather Context

Before asking anything, do a silent context read:
- Run `git log --oneline -5` and `git branch --show-current` to identify the active project
- Run `gh pr list --state open --limit 3` to see open PRs

Then present your findings and ask for confirmation — do NOT ask blank questions:

**Project name:** State what you found (e.g., "I see we're on branch `feat/hooks-memory-skills-design` in `smokin-os` — is that what we're deploying?"). Only ask for correction if ambiguous.

**Deploy target:** First record `DEPLOY_SHA=$(git rev-parse HEAD)` — this must be set before any PR comparison. Then reason from repository state using GitHub branch protection best practices:
- Find the PR for THIS branch: `gh pr list --head $(git branch --show-current) --state open --json number,baseRefName,headRefOid` — assert exactly one result. If zero results: suggest creating a PR. If multiple: halt and ask user to specify which PR.
- Verify the PR's `headRefOid` (full 40-char OID) matches `DEPLOY_SHA` exactly, OR run `git merge-base --is-ancestor "$DEPLOY_SHA" "<headRefOid>"` to confirm DEPLOY_SHA is an ancestor. If neither check passes, warn: "PR head has diverged from local DEPLOY_SHA — rebase or force-push may be needed before deploy."
- If branch protection is active (`gh api repos/<owner>/<repo>/branches/main --jq '.protection.required_status_checks'`): note that required checks must pass
- If on a release/hotfix branch: suggest the appropriate release base

State your recommendation and ask to confirm. Do NOT suggest merging a PR without first verifying it corresponds to the current branch and commit.

After confirmation:
- Verify clean working tree: `git status --porcelain`. If any staged, unstaged, or untracked files exist, **HALT** — "Working tree is not clean. Commit or stash all changes before deploying."
- Validate any user-provided deploy base ref: must match `^(?!-)[A-Za-z0-9._/-]+$` AND resolve to a real commit (`git rev-parse --verify --quiet "$DEPLOY_BASE^{commit}"`). Reject anything that fails either check.
- Run `git fetch origin` then `BASE=$(git merge-base HEAD "$DEPLOY_BASE") && git diff --name-only "$BASE" HEAD` (quoted, never raw-interpolated).
- If merge-base fails, **HALT** — "Cannot establish deploy base. Provide explicit base ref." Never fall back silently.
- Record `DEPLOY_BASE` (git ref, e.g. `origin/main`) and `DEPLOY_BASE_BRANCH` (branch name without remote prefix, e.g. `main`). DEPLOY_SHA was already set during deploy-target reasoning above.
- Check `~/repos/claude-config/decisions/` for the most recent ADR matching the project name.

## Step 0.5 — Classify Change Risk

Before declaring the Verification Contract, classify the change risk level. This determines whether a staging deploy is required and which verification path to use.

- **LOW**: docs-only, Markdown/spec files only, no code execution, no hooks, no schema changes, AND the content does not define or alter operational behavior consumed by agents/apps — regardless of file count. A bad merge is recoverable with a single revert commit.
- **MODERATE**: multi-file, new code path, dependency change, medium-traffic target. **Also MODERATE**: prompt files, runbooks, or spec files that alter agent/operator behavior (decision logic, deploy steps, verification rules, rollback procedures) — file extension is not sufficient to classify these as LOW.
- **HIGH**: DB migration, schema change, auth/security surface, high-traffic or patient-facing target, >5 code files changed. **Also HIGH**: prompt/spec changes that directly govern rollback triggers, verification contracts, auth flows, or production-gating logic.

**One rule, no exceptions: classify by operational impact, not file extension.** Informational-only docs (README updates, meeting notes, architecture diagrams with no behavioral content) qualify as LOW. Everything else — prompt files, runbooks, operational specs, verification contracts, deploy procedures — must be classified by the behavioral impact of the change. State the rationale explicitly.

**HIGH-risk changes require a staging deploy and full verification pass before production.** Ask the user to confirm the target is staging, complete verification, then re-run this prompt targeting production.

State the risk level and get user confirmation before proceeding to Step 1.

## Step 1 — Declare Typed Verification Contract

Before any review or deploy action, declare a Verification Contract for this deploy type. The contract has three required sections. Get user confirmation before proceeding.

**RELEASE TYPE** — is this deploy a dark launch (code ships but feature is inactive until toggled) or a direct release (deploy = serving traffic immediately)? State which. Verification assertions differ:
- Dark launch: verify the new code is deployed and reachable, but confirm the feature flag/toggle is OFF and old behavior is unchanged
- Direct release: verify new behavior is live and serving

**SUCCESS EVIDENCE** — specific, independent assertions that prove the deploy is serving correctly. These must be verifiable WITHOUT trusting the deploy tool's own success report. Examples by deploy type:

For **PR-only / docs deploys** (Markdown, spec files, no code execution):
- Commit lineage: `gh pr view <PR#> --json mergeCommit,headRefOid` — use the full 40-char OIDs from this output. For direct merges: assert `headRefOid == DEPLOY_SHA`. For squash/rebase merges where SHA differs: assert the merge commit is an ancestor of the target branch using `git merge-base --is-ancestor "<mergeCommit.oid>" <DEPLOY_BASE_BRANCH>` — exit code 0 = ancestor confirmed. Never use short SHAs or grep for lineage. If commit lineage cannot be proven via ancestry check, verification FAILS.
- Content integrity: `gh api repos/<owner>/<repo>/contents/<path>?ref=<DEPLOY_BASE_BRANCH>` — decode the base64 content and assert that a known unique string from the deployed file is present (grep for a version string, section header, or identifier that would only be present in the correct version). Use semantic content check, not blob SHA equality.
- PR merged to correct base: `gh pr view <PR#> --json state,baseRefName` — assert `state="MERGED"` and `baseRefName="<DEPLOY_BASE_BRANCH>"` (the branch name without remote prefix — e.g., `main` not `origin/main`)
- No conflict markers: `git show "$DEPLOY_SHA":<path> | grep -c "<<<<<<<"` — assert 0 (use DEPLOY_SHA, never HEAD)
- Pointer string present in index file (if applicable): decode content, grep for expected reference

For **app deploys** (Vercel, CloudHub, Supabase, GitHub Pages):
- HTTP GET the live URL, assert response body contains a known string from the new version (not just status 200)
- CloudHub app → GET /health or invoke a known endpoint, assert response matches expected shape
- Supabase Edge Function → invoke the function directly, assert on response payload
- Scoring function → run it, assert known-value spot check on output rows

**FAILURE INDICATORS** — applicable indicators depend on deploy type. For each indicator, either provide measured evidence OR declare `N/A` with justification. An unjustified N/A is a FAIL.

For **app deploys** (CloudHub, Vercel, Supabase):
- Container restart delta since deploy start > 0 — capture `BASELINE_RESTARTS` before deploy; compare after VERIFICATION_TIMEOUT
- 5xx error rate increase > 5% over VERIFICATION_TIMEOUT window — capture `BASELINE_5XX_RATE` before deploy; compare after
- Health check returning non-200 on two consecutive checks with 10s interval

For **docs/PR-only deploys** (Markdown, spec files):
- Container restarts: `N/A — no running container` ✓
- 5xx rate: `N/A — no service endpoint` ✓
- Health check: `N/A — static content` ✓

For custom deploy types, declare which indicators apply and which are N/A with explicit justification before proceeding.

**VERIFICATION TIMEOUT** — how long to wait for SUCCESS EVIDENCE before triggering rollback. Default is the declared VERIFICATION_TIMEOUT from Step 1, but adjust for the deploy target:
- GitHub Pages / Vercel: 60 seconds (fast propagation)
- CloudHub app: 300 seconds (JVM warmup + health check delay)
- Supabase Edge Function: 60 seconds
- Custom: ask the user what the expected propagation time is and set accordingly

**ROLLBACK TRIGGER** — the rollback action to execute if SUCCESS EVIDENCE is not met within the declared VERIFICATION TIMEOUT. Must be named before deploy starts. Constraints:
- Must be one of:
  - **AUTOMATED**: a named runbook script in the repo (e.g., `scripts/rollback-cloudhub.sh`), a `gh workflow run` invocation, or `vercel rollback`
  - **MANUAL**: operator must revert manually — use this if no automated path exists
- Free-form shell commands are NOT permitted.
- Before deploy starts, confirm with the user: "Rollback on failure will be: [AUTOMATED: command] or [MANUAL]. Confirm to proceed."

On verification failure, handle by trigger type:
- **AUTOMATED**: execute the named command immediately, then close pm_invocations [RUN_ID] as `FAILED - ROLLED BACK`
- **MANUAL**: block all further action, display: "DEPLOY FAILED — MANUAL ROLLBACK REQUIRED. Operator must revert manually before this row can close." Do NOT close the pm_invocations row as success. Do NOT mark the deploy done. Wait for operator to confirm rollback complete, then close as `FAILED - MANUAL ROLLBACK CONFIRMED`.

Do not accept proxy criteria ("deploy script exited 0", "deploy tool reported success"). These are not evidence — they are self-reports from the mechanism you are auditing.

## Stage 1 — Code Review

Invoke the `reviewer` skill on every changed file. Dispatch language-appropriate reviewer subagents in parallel:
- .sh / .bash → bash-reviewer
- .py → python-reviewer
- .ts / .tsx → typescript-reviewer
- .sql / .psql → sql-reviewer
- .ps1 → powershell-reviewer

If a required reviewer subagent is unavailable or the file type has no defined reviewer (e.g., Go, Java, YAML, Dockerfile, JSON config):

- **LOW-risk change**: proceed with general-purpose review + flag explicitly: "FILE X reviewed by general-purpose fallback — human signoff required before deploy." Operator must acknowledge before Stage 2.
- **MODERATE-risk change**: general-purpose fallback is permitted but requires: (a) explicit human signoff from someone familiar with the affected system, AND (b) a written fallback checklist (what would a specialist reviewer have checked — list at least 3 items relevant to this file type). Operator must confirm both before Stage 2.
- **HIGH-risk change** (DB migration, auth/security surface, infra manifest that gates production): missing specialist review is a **NEEDS-FIXES** block. Do not proceed. No waiver or PR comment overrides this. The only path forward is: (a) obtain the specialist review, or (b) reclassify the change as LOW/MODERATE with documented justification that the HIGH-risk criteria do not actually apply.
- **Operational Markdown/spec files** (prompt files, runbooks, verification contracts, deploy procedures — classified HIGH by Step 0.5): use this checklist as the specialist review path: (1) are all success criteria independently observable (not self-reported)? (2) are all failure paths enumerated with explicit outcomes? (3) does the prompt's risk classification correctly account for its own operational impact? (4) are there any self-referential loops (e.g., this prompt governs its own deploy)? A human must sign off on all four items. This is the only approved path for deploying operational Markdown changes with no external specialist available.

Aggregate into worst-of verdict:
- SHIP (0 HIGH, 0 MED, ≤2 LOW) → proceed to Stage 2
- SHIP-WITH-HEDGES (0 HIGH, ≥1 MED) → fix inline, re-run affected reviewer, then proceed to Stage 2
- NEEDS-FIXES (≥1 HIGH) → stop, list findings with file:line citations, do not deploy. Ask user whether to fix and re-run or abort.

Report the verdict explicitly before moving on.

## Stage 2 — Hardened Deploy

Generate a unique run correlation key: `RUN_ID = <project-slug>-<git-commit-sha-full>-<unix-timestamp-ms>-<4-random-hex-chars>`.

Normalize `project-slug`: lowercase, replace all non-alphanumeric characters with `-`, trim leading/trailing `-`, max 40 characters. Halt if slug cannot be normalized to at least 3 characters.

Using full SHA (not short), millisecond timestamp, and a 4-character random hex nonce makes RUN_ID collision-resistant under concurrent or retried deploy attempts for the same project and commit.

RUN_ID is the single identifier for this deploy run. All pm_invocations reads, writes, and closure must reference this exact value.

Invoke the `project-manager` skill in `dispatch` mode. Pass:
- Build name: [RUN_ID]
- ADR: [ADR ID and path found in Step 0]
- Deploy target: [confirmed in Step 0]
- Stage 1 verdict: [from Stage 1]
- Verification contract: [SUCCESS EVIDENCE, FAILURE INDICATORS, ROLLBACK TRIGGER, VERIFICATION_TIMEOUT from Step 1]

After invoking, confirm the pm_invocations row was opened by querying `build.pm_invocations` for a row with `closed_at IS NULL` AND `build_name = '[RUN_ID]'`. Match on the exact RUN_ID — never on partial name. If no matching row exists, halt — the skill did not start. All subsequent reads, writes, and closure of this row must reference RUN_ID explicitly.

When closing the pm_invocations row, set `outcome` to one of: `SUCCESS`, `FAILED - ROLLED BACK`, `FAILED - MANUAL ROLLBACK CONFIRMED`, `FAILED - TIMEOUT`. This outcome field feeds change fail rate tracking over time — it is not optional.

**The pm_invocations row must NOT be closed on deploy command completion.** It closes only after the Verification Contract passes. If verification fails or times out (the declared VERIFICATION_TIMEOUT from Step 1), execute the rollback trigger and close the row using the appropriate outcome enum value per rollback type (see Step 3).

## Step 3 — Independent Verification

Dispatch a verification subagent whose only job is to attempt to validate (or break) the newly deployed endpoint. This subagent has no knowledge of whether the deploy succeeded — it only receives the SUCCESS EVIDENCE assertions from Step 1 and attempts to satisfy or refute them independently.

Walk each SUCCESS EVIDENCE assertion AND each FAILURE INDICATOR — both are required gates:

SUCCESS EVIDENCE (all must pass):
- PASS — cite the raw evidence (actual response body, actual query result, actual HTTP status from a fresh independent request)
- FAIL — name the gap, then handle by rollback type:
  - AUTOMATED: execute rollback command, close pm_invocations [RUN_ID] as `FAILED - ROLLED BACK`
  - MANUAL: block, display "DEPLOY FAILED — MANUAL ROLLBACK REQUIRED", keep row open until operator confirms, then close as `FAILED - MANUAL ROLLBACK CONFIRMED`
  - TIMEOUT (declared VERIFICATION_TIMEOUT exceeded): execute rollback by trigger type first (AUTOMATED: run command; MANUAL: block and require operator acknowledgment), then close row as `FAILED - TIMEOUT` only after rollback attempt is recorded

FAILURE INDICATORS (any triggered = deploy failure):
- For each indicator (restart count, 5xx rate, health check): check it explicitly and record the observed value
- If any indicator is triggered → apply the same rollback-type branching above. Use `FAILED - ROLLED BACK`, `FAILED - MANUAL ROLLBACK CONFIRMED`, or `FAILED - TIMEOUT` as appropriate. Never use plain `FAILED`.

Report the full pass/fail table for both sections. A deploy is complete only when ALL SUCCESS EVIDENCE passes AND ZERO FAILURE INDICATORS are triggered. Do not mark done on partial evidence.

## Post-Run Calibration

After completing this deploy — whether it succeeded or failed — answer these five questions before closing the session. Return your answers as a PR comment on PRM-INFRA-001 or via the feedback footer (score 1-3 + one line).

1. Which steps caused unnecessary friction or delay?
2. Were any verification assertions impossible to satisfy in practice? (e.g., base64 decode required to check line count via GitHub API — consider using `gh api ... | python3 -c "import base64,json,sys; print(base64.b64decode(json.load(sys.stdin)['content']).decode())" | wc -l` for docs deploys)
3. Did the rollback trigger work as declared, or did you have to improvise?
4. Was the risk classification (LOW/MODERATE/HIGH) accurate for what actually happened?
5. What would you remove or simplify if you ran this prompt again tomorrow?

**First-run findings already incorporated into v2.0.0 (2026-06-07 run on hooks-memory-skills-design):**
- Docs-only PRs now self-qualify as LOW regardless of file count
- PR-specific SUCCESS EVIDENCE path added (lighter contract for Markdown-only deploys)
- Step 0.5 downgrade rationale made explicit

Note: On subsequent runs, skip this section if you have no new observations.
```
