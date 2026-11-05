---
name: repo-maintain
description: Resolve authorized repository security findings and PR/MR issues, verifying the resulting commit and CI.
---

Use available native tools/APIs, `gh` or `glab`; no other skill or plugin is required. A read-only request authorizes inspection only.

1. Identify the repository, host, default branch, current branch/HEAD, dirty work and requested scope. Discover actual authenticated API access and provider features; do not assume GitHub and GitLab expose equivalent endpoints.
2. Inventory with pagination: dependency security alerts (Dependabot on GitHub) and dependency graph/data; code scanning and secret scanning separately; open PRs/MRs, unresolved review discussions and CI/checks. Record each source's coverage. Missing permissions, disabled features, unsupported APIs or unavailable data are `UNKNOWN`, never an empty queue or proof of no issues. Report secret names/locations or alert IDs, never secret values.
3. Prioritize relevant security exposure, failing required checks and actionable review feedback. Verify each finding against the current code and affected scenario before changing anything; retain unrelated findings as brief handback items.
4. Apply only authorized fixes. Work on the default branch unless the user requests another; for an existing PR/MR, respect its author branch and agreed workflow without silently switching or creating branches. Preserve unrelated dirty work and stop for a real branch/ownership conflict. Fix authorization does not by itself authorize publication, alert dismissal, merge or resolving other people's threads.
5. Stage explicit paths and inspect the staged diff. Before an authorized push, verify outgoing commits contain only the intended work; never overwrite another author's changes. Record the exact final commit and PR/MR head.
6. Run relevant existing checks and affected real user scenarios against the final tree/target. After an authorized push, fetch CI/check results for that exact pushed commit, not an earlier green run. Re-read the latest remote head before reporting or mutating review state; a changed head invalidates stale conclusions.
7. Resolve a review thread only with publication authorization and evidence that its specific remark is addressed at the latest head. Do not resolve unrelated or unproven remarks. Dismiss alerts or merge only under explicit applicable policy/authorization and verified prerequisites; an empty queue is not a goal by itself.
8. For pending CI, follow the harness's watch/continuation rules; use bounded polling only where permitted. Set an explicit deadline; at expiry, return pending checks, commit IDs and unresolved items instead of claiming completion or waiting forever.

Report inventory coverage/counts, scoped changes, exact commit/target evidence and unresolved or `UNKNOWN` items. Distinguish local tests from the requested live scenario; without its user-visible result, report `applied, not verified`.
