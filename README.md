# my-ai-setup

Shared setup for [Claude Code](https://code.claude.com/docs) and [OpenAI Codex CLI](https://developers.openai.com/codex/cli).

## Features

- **Guard** — blocks selected destructive commands and credential reads with a reason.
- **Status line** — Claude Code script with context, cost and weekly limits with reset countdown; Codex uses its built-in status line.

## Skills

Native skill folders, without a plugin or marketplace. Claude: `/name`; Codex: `$name`.

- **publish** — publish a repository or update its GitHub setup within the requested scope.
- **svgl** — fetch brand and technology SVG logos, including theme and wordmark variants.
- **grill-me** — stress-test a plan through questions ordered by their dependencies, before implementation; also invoked automatically when you ask to be grilled.
- **ui-polish** — autonomously polish a UI to a target score: screenshots, scored reviews from two model families, fixes and real user-flow checks.
- **babysit** — watch journald, `docker logs` or a log file through a `grep | awk` dedup filter for the session; make authorized fixes and report here.
- **repo-maintain** — address security findings, PR/MR feedback and failing CI within the authorized scope; waits for CI and merges only through an explicit merge gate.
- **audit** — audit an app for performance, security and reliability: pick what matters for this software, go deep on the riskiest areas, skip the rest with reasons; report only by default.

## Prerequisites

- Hooks: Python 3.10+; Claude's hook runner also uses `uv`.
- `publish`: Git and authenticated GitHub CLI (`gh`); `repo-maintain`: authenticated host API/CLI access.
- `svgl`: Bash, curl, jq and Python 3, with network access to svgl.app.
- `babysit`: a log source (`journalctl`, `docker logs` over ssh, `tail -F`), `grep` and `awk`. Claude Code runs the pipeline under its `Monitor` tool; Codex runs it in timed foreground slices. Reports stay in the current chat, and monitoring ends with the session/deadline.
- `ui-polish`: a runnable UI, `agent-browser` for screenshots and flows, and Codex CLI for the second reviewer (Claude CLI when run from Codex).
- `audit`: network access to raw.githubusercontent.com and api.github.com for the pinned references; load and scan tools (`k6`/`oha`/`wrk`, `py-spy`, `pprof`, `govulncheck`, `pip-audit`, `npm audit`, `gitleaks`) are used only when installed.

`babysit` is available in both clients and creates no persistent schedule.

## Setup

- [Claude Code setup](docs/claude-code.md)
- [Codex CLI setup](docs/codex.md)

## Reply shortcuts

When sent as the entire message:

- `scr`: simplify, compress and repeat your last response.
- `eli`: explain it like I'm 18, in plain words, shorter.
- `foc`: boil it down to the one thing that matters most here.

## Recommendations

- **Development** — [Herdr](https://github.com/herdrdev/herdr) and [T3 Code](https://github.com/pingdotgg/t3code).
- **Remote** — [Herdrgram](https://github.com/DefaultPerson/herdrgram) and [T3 Code Remote](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md).

## License

MIT
