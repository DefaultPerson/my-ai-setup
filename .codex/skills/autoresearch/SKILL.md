---
name: autoresearch
description: Optimize one measured goal through bounded Git experiments; keep improvements and revert failures.
---

Run in this session. Resolve scope, metric command, higher/lower direction, optional guard, command timeout and iteration cap (default 20). Undefined scope/measurement blocks the run. Require a clean tree and follow branch rules; no new branch, push or merge without authorization.

Baseline: metric exits 0 and prints exactly one finite number; guard passes. Freeze measurement commands, implementation and fixtures. Record iteration 0 and commit state. Report baseline, scope, cap, timeout and `--abort`.

Preserve the existing state format and unknown fields; update atomically:
- `autoresearch-scratchpad.md`: YAML frontmatter with goal, scope, metric_cmd, guard_cmd, direction (`higher_is_better`/`lower_is_better`), best_metric, best_commit, iteration, max_iterations, status (`active`/`complete`/`aborted`), command_timeout; body holds brief lessons and next idea.
- `autoresearch-history.tsv`: append-only columns iteration, commit, metric, delta, status, description, separated by actual tab characters; statuses BASELINE/KEEP/DISCARD/CRASH/GUARD_FAIL, delta against previous best. Preserve experiment SHAs even after reverting. Never replace another run's state without approval.

Each iteration:
1. Re-read state/history, check cap and unexplained dirty work; never stash/erase others' changes. Reconcile any interrupted experiment before starting another.
2. Make one scoped change, excluding measurement/state files. Commit only its paths; save its exact SHA as `pending_commit` in the scratchpad before measuring. No amend/rebase.
3. Measure and run the guard with the recorded timeout and fresh logs. Timeout, nonzero exit or invalid metric is CRASH; failing guard is GUARD_FAIL. KEEP only a strict improvement with a passing guard.
4. Otherwise `git revert --no-edit <experiment-SHA>`; conflicts stop the run. Never reset or assume HEAD is the experiment. On resume, check whether a pending SHA was already reverted; uncertainty stops the run rather than reverting twice.
5. Append outcome/lesson, update best only on KEEP, increment iteration, clear pending_commit and commit state after any revert. Report metric, delta and best. Pivot or stop when useful hypotheses run out.

`--continue` revalidates state, measurement and pending SHA; finished runs/exhausted caps need explicit extension. `--abort` reverts and records any unaccepted pending experiment, marks aborted and keeps accepted changes. At cap/no viable idea, mark complete. Report baseline→best, iterations/outcomes, best SHA and stop reason.
