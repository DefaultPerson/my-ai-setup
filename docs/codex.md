# Codex CLI Setup

## Setup

Paste into Codex — or follow the steps manually:

```
Prerequisites: Python 3.10+ (CI uses 3.12), available as python3. For /publish: git and authenticated gh.

1. Download https://github.com/DefaultPerson/my-ai-setup to ~/projects/misc/my-ai-setup.
2. Create ~/.codex/hooks/ if absent. Install the guard from the downloaded directory:
   install -m 0644 ~/projects/misc/my-ai-setup/.codex/hooks/guard.py ~/.codex/hooks/guard.py
   Preserve unrelated hook files.
3. Merge the PreToolUse entry from .codex/hooks.json into ~/.codex/hooks.json:
   matcher Bash|apply_patch, command python3 "$HOME/.codex/hooks/guard.py".
   Create the file if absent; preserve existing hooks, including agent integrations,
   and do not duplicate a matching entry.
4. Copy the desired directories from .codex/skills/ into ~/.codex/skills/.
   Include each skill's scripts and metadata; preserve unrelated skills. No plugin is needed.
5. Merge desired preferences from .codex/config.toml.sample into ~/.codex/config.toml;
   create the file if absent, preserving existing configuration and MCP servers.
6. Optionally merge AGENTS.md into ~/.codex/AGENTS.md — author's coding style and rules.
7. Optionally add shell aliases (see below).
8. Open /hooks in Codex and trust the PreToolUse hook; review it again after changing
   its command, matcher or timeout.
9. Start a fresh session. Check guard.py directly with representative hook JSON, without
   executing the tools: harmless input should be allowed and a protected operation denied.
   Configure the status line with /statusline.
10. Keep ~/projects/misc/my-ai-setup: guard updates use this source path.
```

See README for skill descriptions and their prerequisites. Invoke skills by their plain names, for example `$svgl` or `$grill-me`. `babysit` uses current-session events or foreground execution and reports in the same chat; it creates no persistent schedule.

When upgrading, verify the native skills load, then retire `as@as`, the Codex-only installation of `codex@openai-codex`, their unused marketplace sources, and old native `verify-done`/`verify-setup`/`autoresearch`/`repo-context` after checking saved copies. Keep the system `skill-creator` and one user copy of `publish` in `~/.codex/skills`.

Check project `.agents/skills` for old `commit`, `push-and-pr`, `publish` and `repo-context` copies too: ignored files are still discoverable. Copying this setup does not uninstall older hooks, skills or plugins; preserve unrelated installations.

**Key differences from Claude Code:**
- Config: `config.toml` (TOML) instead of `settings.json`
- Instructions: `AGENTS.md` instead of `CLAUDE.md`
- Status line: built-in `/statusline` picker and `tui.status_line` items
- MCP: configured in `config.toml` `[mcp_servers]` section or via `codex mcp add`

## Shell Aliases

Add to `.bashrc` / `.zshrc`:

```bash
alias cx="codex" cxr="codex resume" cxd="codex --yolo" cxdr="codex resume --yolo"
```
