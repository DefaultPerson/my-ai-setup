# Codex CLI Setup

## Setup

Paste into Codex — or follow the steps manually:

```
Prerequisites: Python 3.10+ (CI uses 3.12), available as python3. For /publish: git and authenticated gh.

1. Download https://github.com/DefaultPerson/ai-setup to ~/projects/misc/ai-setup.
2. Create ~/.codex/hooks/ if absent. Install the guard from the downloaded directory:
   install -m 0644 ~/projects/misc/ai-setup/.codex/hooks/guard.py ~/.codex/hooks/guard.py
   Preserve unrelated hook files.
3. Merge the PreToolUse entry from .codex/hooks.json into ~/.codex/hooks.json:
   matcher Bash|apply_patch, command python3 "$HOME/.codex/hooks/guard.py".
   Create the file if absent; preserve existing hooks, including agent integrations,
   and do not duplicate a matching entry.
4. Copy .codex/skills/publish into ~/.codex/skills/; preserve unrelated skills.
5. Merge desired preferences from .codex/config.toml.sample into ~/.codex/config.toml;
   create the file if absent, preserving existing configuration and MCP servers.
6. Optionally merge AGENTS.md into ~/.codex/AGENTS.md — author's coding style and rules.
7. Optionally add shell aliases (see below).
8. Open /hooks in Codex and trust the PreToolUse hook; review it again after changing
   its command, matcher or timeout.
9. Start a fresh session. Check guard.py directly with representative hook JSON, without
   executing the tools: harmless input should be allowed and a protected operation denied.
   Configure the status line with /statusline.
10. Keep ~/projects/misc/ai-setup: guard updates use this source path.
```

Copying this setup does not remove hooks or skills from an older installation; review those separately.

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
