# RCA: Local main Divergence — prompt-registry — 2026-06-02

**Status:** Root cause confirmed. Fix applied (manual `git reset --hard origin/main`). Prevention gap identified.  
**Severity:** Low — no data lost, no prod impact. Registry was live and correct on origin throughout.  
**Written:** 2026-06-02, while fresh.

---

## What happened (symptom)

After PR #10 merged, running `git pull` from local `main` failed with:

```
fatal: Not possible to fast-forward, aborting.
```

Local `main` was at `646a70e` (2 commits). `origin/main` was at `92c7562` (10+ commits). The branches diverged and could not fast-forward.

---

## Root cause (confirmed)

**Two orphaned root commits were created at repo initialization time.**

Both commits share the exact same tree hash (`d3eb54ca`) — identical content — but have no parent relationship:

| Commit | Timestamp | Message | Branch |
| :--- | :--- | :--- | :--- |
| `f0cb850` | 2026-06-02 09:25:14 | `feat: initial prompt-registry scaffold` | `origin/feat/initial-scaffold` |
| `0e8a54a` | 2026-06-02 09:25:59 | `chore: initialize empty main branch` | `origin/main` |

These are **two separate root commits, 45 seconds apart, with identical trees.** They have no shared ancestor — they are entirely disconnected histories.

### How it happened

During the scaffold session (~09:25 today), the repo was initialized twice in quick succession:

1. **`f0cb850`** — the scaffold commit was pushed to `feat/initial-scaffold` (the first branch created)
2. **`0e8a54a`** — a second "initialize empty main branch" commit was created on `main` to establish branch protection, but it was created as a new orphan (`git checkout --orphan main` or equivalent), not by merging `feat/initial-scaffold` into `main`

The local clone (`~/repos/prompt-registry`) was cloned when `feat/initial-scaffold` was still the tip of the work, so **`git clone` set the local `main` tracking to `origin/feat/initial-scaffold`** — the branch that had the actual content at clone time — instead of `origin/main`.

All subsequent PRs (#5 through #10) merged into `origin/main` (the `0e8a54a` lineage). The local `main` stayed on the `f0cb850` lineage and accumulated no new commits. The tracking pointer was wrong, not the work.

### Why `git pull` failed

When upstream tracking was corrected to `origin/main`, the two histories had no common ancestor, so fast-forward was impossible. `git merge --no-ff` or `git reset --hard origin/main` were the only options. Since local `main` had no unique content (the 2 local commits were already merged into origin via PR squashes), `reset --hard` was safe.

---

## What this is NOT

- **Not the auto-sync worker.** The worker manages `~/repos/claude-config`, not `~/repos/prompt-registry`. It played no role here.
- **Not a Win11/Mac sync issue.** This repo is not in the sync engine's scope.
- **Not data loss.** The 2 local commits (`f0cb850`, `646a70e`) were scaffold content already present on `origin/main` via squash merges. Nothing unique was discarded.
- **Not related to the system-reminder file reversions seen during the session.** Those were the PR template and other files being reset by a linter or editor — separate issue, not connected to the branch divergence.

---

## Timeline

| Time | Event |
| :--- | :--- |
| 09:25:14 | Scaffold commit `f0cb850` pushed to `origin/feat/initial-scaffold` |
| 09:25:59 | Orphan `main` initialized at `0e8a54a` — divergent history created |
| ~09:26 | Repo cloned locally — clone tracked `feat/initial-scaffold` tip |
| 09:25–18:22 | PRs #1–#10 all merged into `origin/main` (`0e8a54a` lineage) |
| 18:22 | PR #10 merged; local `main` still tracking wrong upstream |
| 18:35 | `git pull` fails — divergence surfaced |
| 18:41 | Manual `git reset --hard origin/main` applied — local main now at `92c7562` |

---

## Current state (post-fix)

```
main (local)  →  92c7562  [origin/main]  ✅ synced
```

All stale feature branches (tracking wrong upstream) are still in the local clone but harmless — they track their own `origin/feat/*` refs correctly.

One live branch needs attention:

```
feat/prm-pdlv-006-overview-video  →  791f06b  [origin/main: ahead 1]
```

This branch has 1 commit ahead of `origin/main` — it is an open feature branch with work in progress. **Do not reset or delete this branch.** It needs a PR to merge.

---

## Prevention: what to fix

### Gap 1 — Orphan `main` initialization pattern

**What broke it:** creating `main` as an orphan instead of branching from `feat/initial-scaffold`.

**Fix for future repos:** when establishing branch protection on a new repo, always create `main` by merging the scaffold branch, not by `git checkout --orphan`. The correct sequence:

```bash
# On the scaffold branch with content:
git checkout -b main
git push origin main
# Set main as default branch in GitHub settings
# Then merge scaffold via PR
```

Or simpler: use `gh repo create --source=.` which initializes with `main` as the first branch.

### Gap 2 — Clone tracking not verified

**What broke it:** after cloning, the local `main` was silently tracking the wrong upstream. No one checked `git branch -vv` at clone time.

**Fix:** after any fresh clone of a repo that was initialized with branch gymnastics, run:

```bash
git branch -vv
```

and confirm local `main` tracks `origin/main`. If not:

```bash
git branch --set-upstream-to=origin/main main
```

### Gap 3 — No guard on `git pull` failure mode

**What broke it:** the divergence was only discovered when `git pull` failed. A proactive check (`git fetch && git status`) earlier would have surfaced it sooner.

---

## Pre-PR recommendation

No code change is needed — the divergence is fixed. The recommendation is a one-time cleanup:

1. **Delete stale local branches** that tracked the wrong upstream (optional, cosmetic):
   - `feat/add-prm-nblm-004`, `feat/add-use-for-column`, `feat/html-wrapper` — all merged, safe to prune
   - `git remote prune origin && git branch -d feat/add-prm-nblm-004 feat/add-use-for-column feat/html-wrapper`

2. **Handle `feat/prm-pdlv-006-overview-video`** — this has 1 real commit ahead of main. Open a PR or drop it if it was experimental.

3. **Document the orphan-init anti-pattern** in CONTRIBUTING.md under "Setting up a new domain" — this is a repo-initialization hazard, not a day-to-day contributor hazard, so it belongs in a "repo admin" note, not the main flow.

No migration, no schema change, no sync engine involvement required.

---

## Bottom line

> The divergence was caused by a one-time repo initialization error: two orphan root commits were created 45 seconds apart, splitting the history permanently. The local clone tracked the wrong one. The auto-sync worker, Win11/Mac sync, and the working files were never involved. The fix was a single `git reset --hard origin/main`. No data was lost.
