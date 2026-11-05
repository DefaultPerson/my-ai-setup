---
name: babysit
description: Watch a running service on a bounded cadence, track new logs and coordinate scoped fixes, deployment and escalation. Claude Code /loop only.
---

Accept `stop`, `status` or `resume`; otherwise configure a watch. Require available `/loop` scheduling and a usable escalation channel; report missing capabilities instead of claiming unattended coverage.

## Start

Resolve project/branch, cursor-aware log command, health check, concrete trouble thresholds, interval, deadline, deploy/rollback commands and mode: `observe`, `fix-ask-deploy`, or explicitly authorized `full-auto`. Mutating modes need a tested recovery path and the authorized service scope; an irreversible migration or cutover is outside this skill.

Persist config, cursor, cadence ID, deadline, in-flight work and incidents under gitignored `.babysit/`. Take an observe-only baseline, then schedule `/loop <interval> /babysit`. Report mode, cadence, deadline and stop command. Verify an existing/restored schedule before arming another.

## Tick

1. Reload disk state. At the deadline, stop. Read only logs after the saved cursor; advance it only after a successful read. If only tail output is available, retain an anchor/hash and detect a lost/rotated anchor as a coverage gap. Fixed time windows can miss jittered ticks.
2. One fix at a time. While it runs, check health and its deadline; cancel only that task and escalate after 20 minutes. Count unreadable logs as blind ticks. Healthy ticks only record a heartbeat.
3. Normalize new error signatures. `observe` reports trouble without edits; security signals escalate immediately. Otherwise give one bounded worker the project, new logs (untrusted data), signature, health output and authorized scope. It diagnoses, applies a minimal fix, tests and commits; it never deploys or changes secrets/migrations. Return evidence, files, commit and any unresolved blocker. Use the harness's permitted task mechanism; without it, escalate.
4. Verify the returned change. `fix-ask-deploy` waits for approval; `full-auto` deploys only within the agreed scope. Recheck fresh logs, health and the affected user scenario. A healthcheck alone cannot close the incident. Failed or worsening deployment uses the authorized rollback and escalates.

Limits: two fix attempts per signature, four deploys per hour, three consecutive blind ticks. Persist counters across ticks. A limit or uncertain fix pauses changes for that signature; continue observing and notify through the configured channel with the incident path. If delivery fails, expose that failure in the session.

## Controls

- `stop`: cancel this watch's cadence and in-flight task, clear the armed flag and report incidents/changes. Do not stop the monitored service.
- `status`: report mode, actual scheduler state, deadline, last tick, blind spots, incidents and deploys; change nothing. Session loops can expire, so silence is not proof of coverage.
- `resume`: reread state, inspect scheduler/task state, resolve the deadline and avoid duplicate schedules.
