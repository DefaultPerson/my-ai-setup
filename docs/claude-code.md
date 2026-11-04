# Claude Code Setup

## Setup

Paste into Claude Code — or follow the steps manually:

```
Prerequisites: Python 3.10+ (CI uses 3.12), uv. For /publish: git and authenticated gh.

1. Download https://github.com/DefaultPerson/ai-setup to ~/projects/misc/ai-setup.
2. Create ~/.claude/hooks/ if absent. Install the guard from the downloaded directory:
   install -m 0644 ~/projects/misc/ai-setup/.claude/hooks/guard.py ~/.claude/hooks/guard.py
   Copy .claude/hooks/statusline.py there; preserve unrelated hook files.
3. Copy .claude/skills/publish into ~/.claude/skills/; preserve unrelated skills.
4. Merge the needed entries from .claude/settings.example.json into ~/.claude/settings.json:
   the guard PreToolUse hook, statusLine, and relevant preferences. Create the file if absent;
   preserve existing settings and hooks, including agent integrations. Do not duplicate matching entries.
   # Windows: install Git Bash for the hook runner; keep the $HOME paths as they are
5. Optionally merge CLAUDE.md into ~/.claude/CLAUDE.md — author's coding style and rules.
   # machine-specific rules (paths, services, sudo habits) go in ~/.claude/rules/<name>.md, not in CLAUDE.md
6. Optionally add shell aliases (see below).
7. Restart Claude Code and check that the status line appears. Check guard.py directly
   with representative hook JSON, without executing the tools: harmless input should be
   allowed and a protected operation denied.
8. Keep ~/projects/misc/ai-setup: guard updates use this source path.
```

Claude's five-hour status line segment is disabled in the script; weekly limits and the reset countdown remain enabled. Copying this setup does not remove hooks or skills from an older installation; review those separately.

## Shell Aliases

Add to `.bashrc` / `.zshrc`:

```bash
alias cc="claude" ccr="claude --resume" ccd="claude --dangerously-skip-permissions" ccdr="claude --dangerously-skip-permissions --resume"
```
