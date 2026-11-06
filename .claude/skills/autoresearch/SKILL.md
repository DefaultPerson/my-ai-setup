---
name: autoresearch
description: Optimize one measured goal through bounded Git experiments; keep improvements and revert failures.
argument-hint: "<goal> | --continue | --abort"
---

Resolve scope, metric command, direction, optional guard, command timeout and iteration cap (default 20); without scope or metric, stop and ask. Require a clean tree.

Baseline: the metric exits 0 and prints exactly one finite number, and the guard passes. Freeze the metric, guard and fixtures for the run. Report baseline, scope, cap, timeout and `--abort`.

State (preserve unknown fields; write atomically; never replace another run's state without approval):
- `autoresearch-scratchpad.md`: YAML frontmatter with goal, scope, metric_cmd, guard_cmd, direction (`higher_is_better`/`lower_is_better`), best_metric, best_commit, iteration, max_iterations, status (`active`/`complete`/`aborted`), command_timeout, pending_commit; the body holds brief lessons and the next idea.
- `autoresearch-history.tsv`: append-only, tab-separated: iteration, commit, metric, delta, status, description. Statuses BASELINE/KEEP/DISCARD/CRASH/GUARD_FAIL; delta is against the previous best; keep experiment SHAs after reverts.

Each iteration:
1. Re-read state and history, check the cap, and reconcile any pending experiment first.
2. Make one scoped change outside measurement and state files, commit only its paths, and save the SHA as `pending_commit` before measuring. No amend or rebase.
3. Measure and run the guard with the timeout. Timeout, nonzero exit or an invalid number is CRASH; a failing guard is GUARD_FAIL. KEEP only a strict improvement with a passing guard.
4. Otherwise `git revert --no-edit <SHA>`, never reset; a conflict stops the run. On resume, if it is unclear whether the pending SHA was reverted, stop rather than revert twice.
5. Append the outcome, update best only on KEEP, increment iteration, clear `pending_commit` and commit state. Report metric, delta and best.

`--continue` revalidates state, measurement and the pending SHA; a finished run or exhausted cap needs explicit extension. `--abort` reverts and records an unaccepted pending experiment, marks the run aborted and keeps accepted changes. Mark complete at the cap or when ideas run out, and report baseline→best, outcomes, best SHA and the stop reason.
