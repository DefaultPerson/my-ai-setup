---
name: autoresearch
description: Run bounded Git experiments against one numeric metric; commit each change, measure it, then keep improvements or revert failures.
---

Accept a goal, `--continue` or `--abort`. Run iterations in this session; do not schedule background work.

## Setup

Resolve `scope`, `metric_cmd`, optional `guard_cmd`, `direction` (higher/lower) and `max_iterations` (default 20). Ask only for missing decisions; without an answer channel, stop if the scope or measurement is undefined.

Require a clean Git tree. Follow repository branch rules; create a branch only if requested. Run the baseline metric: exit 0 and exactly one finite number on stdout. Validate the optional guard too; an invalid baseline blocks the run. Freeze measurement commands and their implementation/fixtures for the run.

If state already exists, resume a matching active goal; otherwise ask before replacing it. Write baseline iteration 0 and commit the two state files. Report scope, baseline, direction, cap, branch and how to abort.

## State

Re-read these root files every iteration; preserve unknown fields and write updates atomically:

- `autoresearch-scratchpad.md`: frontmatter `goal`, `scope`, `metric_cmd`, `guard_cmd`, `direction` (`higher_is_better`/`lower_is_better`), `best_metric`, `best_commit`, `iteration`, `max_iterations`, `status` (`active`/`complete`/`aborted`). Body sections: `What worked`, `What failed`, `Next to try`, `Blocked ideas`.
- `autoresearch-history.tsv`: append-only header `iteration	commit	metric	delta	status	description`. Status: `BASELINE`, `KEEP`, `DISCARD`, `CRASH`, `GUARD_FAIL`; commit is the hash for kept/baseline changes, `REVERTED` otherwise. Delta is against the previous best.

## Iteration

1. Read state, the last 20 history rows and recent commits. Check the cap before editing. Stop on unexpected dirty work; do not stash or erase it.
2. Pick one hypothesis: address the last crash first; block an idea after three repeated diffs/descriptions; pivot after more than five consecutive failed attempts; otherwise build on a recent improvement or try the next idea. No viable idea ends the run.
3. Apply one atomic change inside `scope`, leaving measurement code and state untouched. Stage only its files and commit. Record that exact experiment SHA. No amend or rebase.
4. Run the metric and optional guard, each into a fresh temporary log created in this iteration. Invalid/non-finite/multiple output values or nonzero metric exit mean `CRASH`; a failed guard means `GUARD_FAIL`.
5. `KEEP` only a strict improvement with a passing guard. Otherwise revert the recorded experiment SHA with `git revert --no-edit <sha>`. Never assume HEAD still identifies it. If reverting conflicts, stop and report; do not reset away other work.
6. Append the outcome, update best values only on KEEP, increment the iteration and record the lesson/next hypothesis. Commit state separately, after any revert. Print iteration, outcome, metric, best and delta. A failed experiment is recorded before moving to a different hypothesis.

When delegation materially helps and is permitted, give one worker the hypothesis, scope and recent lessons. It edits/commits only; the parent measures and updates state. Return `result: applied|aborted`, `commit`, `files_changed`, `summary`, `lesson`. Verify its actual commit and tree even after an aborted or malformed reply; never continue over unexplained changes. Otherwise implement inline.

## Finish / resume

At the cap or when ideas are exhausted, mark `complete`, commit state and report baseline versus best, iterations/keeps/discards, best commit, branch and stop reason. `--abort` marks `aborted` and keeps accepted commits. Do not push or merge without authorization.

`--continue` revalidates the recorded state and resumes; a completed/aborted run or exhausted cap requires an explicit extension or new goal. With no answer channel, report and stop.
