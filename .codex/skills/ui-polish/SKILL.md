---
name: ui-polish
description: Autonomously polish a UI to a target score — run it, capture screens and user flows, get scored reviews from two model families, fix and repeat. Use when asked to polish, improve, refine or redesign the look and UX of an interface.
---

Work autonomously: state the plan and budget, then run without questions. Ask only to exceed the round cap, change the product's identity or remove functionality, or take an irreversible step. For an audit-only request, stop after the first review.

## Setup

- Find how to run the UI from project instructions, manifests or scripts; start it in the background and wait until it serves. Use test data only.
- Pick the target screens and primary user flow from the request and the product. Capture each screen with headless `agent-browser` at 1440×900 and 390×844, in light and dark themes when supported, plus relevant states (empty, loading, error, focus). For non-web UIs use the platform's screenshot tool. Keep evidence in a session temp dir, not the repo.
- References: when the user names competitors or URLs, capture the same task at the same viewport and theme; otherwise compare against the baseline only.
- Defaults: target 9/10 on every criterion, cap 5 rounds, stop after 2 rounds without gain. Criteria: hierarchy, typography, layout/density, color/contrast, action clarity/feedback, flow, accessibility. User-given values replace the defaults.

## Council

- Two independent reviewers from different model families. Claude Code: an `Agent` with `model: opus`, plus `codex exec -s read-only -c model=<sol slug> -c model_reasoning_effort=high -i <screenshots> "<brief>"` (slug from `codex debug models`). Codex: a native subagent, plus `claude -p --model opus "<brief with screenshot paths>"`. If one is unavailable, use the other alone and say so; never present one model as two.
- Both get the same read-only packet: brief, criteria, current screenshots, references, flow results and revision. No earlier scores or other verdicts.
- Reply contract: `SCORES <criterion>=N/10 …`, then `F1 [blocker|should|nit] <screen>: <observation>. Fix: <suggestion>`. blocker = primary task broken or unreadable; should = a defect users will hit; nit = the rest. Missing evidence is `unassessed`, not a score.

## Loop

1. Verify each finding on the target. Fix blockers and shoulds with the smallest change; decline nits and taste-only changes in one line. Keep the product's identity and functionality, and do not let reviews grow scope.
2. Before editing, save `git diff` to `<temp>/round-N.patch`. Do not commit, stash or touch unrelated changes.
3. Re-capture the same set and re-run the primary flow, including keyboard/focus, narrow layout and themes. Passing builds or tests do not replace this.
4. Start the next round with fresh reviewers. Stop at the target with no open blocker/should and a passing flow, at the cap, or at a plateau. The end of the budget is not approval.

Report a score table per reviewer and round, changes, declined findings, before/after screenshot paths, flow results and what stayed unverified. Stop the server you started.
