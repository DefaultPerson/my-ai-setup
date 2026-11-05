---
name: verify-done
description: Audit completed work against the original request with rerun proofs, independent scenarios and a DONE/NOT-DONE verdict; do not fix it.
---

Accept a plan file or the original task. `--deep` expands scenario coverage; `--block-on-quality` makes high-severity maintainability findings blocking.

1. Collect every `Done when:` proof, agreed constraint and unresolved decision. For prose-only intent, derive concrete checks. Include relevant build/test/regression commands. Missing intent requires clarification, not invented requirements.
2. Run checks against the actual changed tree and requested target. A clean checkout can omit uncommitted work; mocks cannot prove deployed behavior. Do not edit the implementation or run destructive/live mutations without authorization. Mark unavailable checks `UNKNOWN` with a reason.
3. Generate independent, risk-ranked user/edge/adversarial scenarios from the original intent. Tie each to a requirement, discard and count ungrounded candidates, then run the applicable cases. List every unrun case; a budget limit must not silently erase coverage.
4. When behavior passes, review maintainability: concrete regressions, unnecessary duplication/abstraction, broken boundaries or non-atomic state changes. Omit style nits and unrelated pre-existing issues. Quality is advisory unless the flag above makes a high-severity finding blocking.

Use ordinary available tools; no plugin, Workflow or other skill is required. Delegate only when useful and allowed, passing the full intent, current tree/target and evidence contract.

Report `VERDICT: DONE | NOT-DONE`, conformance `N/M PASS, K UNKNOWN`, scenarios generated/discarded/run, confirmed gaps, quality severity and everything not covered. UNKNOWN is neither PASS nor a confirmed failure.

DONE requires all proofs passing, no confirmed scenario gap, no high-risk case unrun, and no blocking quality finding. No runnable evidence means `NOT-DONE: could not verify`. With scenarios but no explicit proofs, label the verdict scenario-only. Return findings without fixing them.
