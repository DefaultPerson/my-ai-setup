---
name: ui-iterate
description: Improve a UI through bounded independent reviews, visual references and verified user flows. Use for iterative UI/UX refinement, not a single styling fix.
---

Iterate on a rendered interface: establish a baseline, review independently, apply supported changes, then inspect the result. For audit-only requests, return findings without editing.

## Establish the comparison

- Identify the users, primary task, target screens and constraints from the brief and existing product. Preserve its identity and functionality; a higher score does not authorize a redesign. For a new UI, build a working baseline only when implementation is in scope.
- Fix the evaluation set: realistic content, relevant viewport sizes, themes and interaction states. Capture the baseline on the actual target using permitted browser or screenshot tools. If rendering is unavailable, label the result a code-only review; do not issue a visual verdict.
- Use supplied references or relevant alternatives when available. Compare the same task and comparable states, viewport and theme; explain mismatches. A competitor screenshot supports visual comparison, not claims about its untested interaction flow. Do not copy branding or add references merely to justify a preferred style.
- Choose criteria for this product: hierarchy/readability, layout/density, color/contrast, action clarity/feedback, task flow and accessibility. Define observable anchors before scoring; keep criteria and references stable across rounds. Model scores are subjective evidence, not a usability benchmark or a required 10/10 target.

## Bound the reviews

Use the user's models, providers and budget. Otherwise propose the smallest useful council, normally two independent reviewers, and at most three review rounds; follow the harness's delegation and approval rules. Prefer different providers when available. Name the members and limits before starting; never silently replace a requested reviewer or pretend one model is several independent providers.

Track any user-specified score target without relaxing the functional acceptance criteria. Reaching the cap below that target leaves it unmet; a high score cannot cancel a failed user scenario.

Give each reviewer the same brief, criteria, baseline/current screenshots, references and scenario evidence, tied to the same revision. Keep reviews read-only and independent: do not show other verdicts, earlier scores or a score to please. Ask for per-criterion scores out of 10 when evidence supports them, concrete observations, affected user task, severity, suggested correction and anything unverified. Missing evidence means unassessed, not an invented score.

## Iterate

1. Check findings against the actual target. Resolve disagreements using evidence and the brief; separate preference from an observed defect. Select a small coherent change set with expected effects. Fix known defects before buying another review.
2. Apply only justified changes. Keep the preceding version recoverable and isolate your edits from unrelated work. Revert your own regressions without discarding other changes; never remove functionality to improve a score.
3. Re-render the same evaluation set. Exercise the primary user journey and relevant failure/recovery states on the actual target, including applicable keyboard/focus, narrow-layout and theme cases. Record observed results separately from build/tests and reviewer opinions. Use authorized test data; do not invent permission for live destructive actions.
4. Request a fresh independent review of the new evidence only when a material change or unresolved disagreement warrants it. One complete council pass is one round. Keep a compact record of revision, reviewed evidence, findings, changes and checks; preserve it in a task artifact only when needed for resumption or requested.

Stop when the acceptance criteria and actual user scenarios pass with no supported high-impact issue, when successive rounds offer no evidence-backed improvement, or when the agreed cap is reached. Do not keep iterating to inflate scores. Extending the cap or materially changing direction requires the user's decision.

Report what changed, rounds used/cap, confirmed improvements, remaining disagreements and unverified scenarios. Keep visual judgment, functional checks and live user-path evidence separate. If only code or screenshots were available, state that interaction behavior remains unverified. Do not publish, deploy or install additional tools just to complete this loop without authorization.
