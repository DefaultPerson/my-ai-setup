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
- **babysit** — filter log incidents within the current session and deadline; make authorized fixes and report here.
- **repo-maintain** — address security findings, PR/MR feedback and failing CI within the authorized scope; waits for CI and merges only through an explicit merge gate.

## Prerequisites

- Hooks: Python 3.10+; Claude's hook runner also uses `uv`.
- `publish`: Git and authenticated GitHub CLI (`gh`); `repo-maintain`: authenticated host API/CLI access.
- `svgl`: Bash, curl, jq and Python 3, with network access to svgl.app.
- `babysit`: Python 3 and readable logs. Claude Code runs the filter under its `Monitor` tool; Codex uses a session-owned event or foreground runner. Reports stay in the current chat, and monitoring ends with the session/deadline.
- `ui-polish`: a runnable UI, `agent-browser` for screenshots and flows, and Codex CLI for the second reviewer (Claude CLI when run from Codex).

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
