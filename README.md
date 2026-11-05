# my-ai-setup

Shared setup for [Claude Code](https://code.claude.com/docs) and [OpenAI Codex CLI](https://developers.openai.com/codex/cli).

## Features

- **Guard** — blocks selected destructive commands and credential reads with a reason.
- **Status line** — Claude Code script with context, cost and weekly limits with reset countdown; Codex uses its built-in status line.

## Skills

Native skill folders, without a plugin or marketplace. Claude: `/name`; Codex: `$name`.

- **publish** — publish a repository or update its GitHub setup within the requested scope.
- **svgl** — fetch brand and technology SVG logos, including theme and wordmark variants.
- **autoresearch** — bounded experiments against one metric: commit, measure, keep or revert.
- **verify-done** — check the original requirements and real scenarios; report gaps without fixing them.
- **grill-me** — stress-test a plan through questions ordered by their dependencies, before implementation.
- **babysit** — watch a service, coordinate scoped fixes and deployment, and escalate trouble; Claude Code only.

## Prerequisites

- Hooks: Python 3.10+; Claude's hook runner also uses `uv`.
- `publish`: Git and authenticated GitHub CLI (`gh`); `autoresearch`: Git and the project's metric/test tools.
- `svgl`: Bash, curl, jq and Python 3, with network access to svgl.app.
- `babysit`: Claude Code `/loop`, service log/health access and an escalation channel; deployment modes need a recovery path.

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
