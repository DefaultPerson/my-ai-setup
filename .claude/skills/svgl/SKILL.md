---
name: svgl
description: Fetch brand and technology SVG logos from svgl.app by name or category, with theme and wordmark variants.
---

Use the bundled `scripts/svgl.sh` (Bash, curl, jq, Python 3); resolve its path from this skill directory.

- `categories` lists exact category names; `search <query> [limit]` and `category <name> [limit]` return JSON; `download <url> <outfile>` saves one asset.
- User options: `--theme light|dark|both` (default both), `--wordmark`, `--out` (default `./svgl`), `--limit`, `--all`, `--json`, `--force`. Interpret these yourself; the helper accepts only the subcommands above. `--json` returns metadata without downloads.
- Search is a case-insensitive literal substring: try `next`, not `nextjs`. Prefer an exact title; clarify ambiguous matches. Resolve categories from `categories`; confirm bulk downloads unless already requested.
- `route` and optional `wordmark` can be a URL or a `{light, dark}` object; `category` can be a string or array. Select requested variants, deduplicate identical URLs and report missing variants.
- Name files `<slug>[-light|-dark][-wordmark].svg`. Check existence before calling `download`: skip existing files unless `--force` was requested. Do not modify project imports or commit assets unless asked.
- Use `https://api.svgl.app`; combined API `limit` can override search/category, so the helper limits client-side. It maps 404 to no results and bounds 429 retries; report other failures without inventing matches.
- Report saved paths, skipped files and unavailable logos.
