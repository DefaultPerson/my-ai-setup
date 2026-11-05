---
name: verify-setup
description: Set up project verification in agent instructions using existing checks and real user scenarios.
---

Make verification discoverable for the clients actually used by this project, without building a new test framework.

1. Read project instructions, manifests, scripts, CI and the user's goal. Identify the actual clients, existing verification guidance, relevant commands, target and observable user scenario; clarify only missing facts that change the checks.
2. Reuse sufficient commands. Add a tiny script only for repeatable checks that existing commands cannot express; use concise `docs/verification.md` only when manual/live steps need more space. Do not invent generic tests or add unrelated tooling/CI.
3. Add only a few relevant lines to `AGENTS.md` and/or `CLAUDE.md` for those clients: when to verify, exact commands or a documentation link, and the required real-target scenario. Reuse shared instructions where the clients already load them; avoid duplicate or contradictory blocks.
4. Update equivalent existing guidance in place. Preserve unrelated content; rerunning setup must not append another block, script or document. Keep commands project-relative and record prerequisites or working directories where needed.
5. Follow the resulting instructions yourself against the current tree and intended target, including the observable user path. A build, mock, healthcheck, HTTP 200 or queued action alone cannot establish that path. Do not infer permission to deploy, publish or mutate an external system from setup authorization.
6. Report changed paths, commands/scenarios run and their observed results. Mark unavailable checks `UNKNOWN` with the reason and exact way to check; say `applied, not verified` when the real target was not exercised. Do not claim success from instructions merely existing.

Leave reasoning and findings in the reply; generated instructions hold only what to run or know. No other skill, plugin or agent is required.
