---
name: publish
description: Publish the repository to GitHub or review and update its GitHub setup when explicitly requested.
---

Use `git` and authenticated `gh`. Inspect the current `origin` and GitHub repository before changing their setup.

- Publish only when explicitly requested; a review alone authorizes no changes, commits or pushes.
- Default a new repository to private. Ask only for choices needed to complete the request that are not already specified or safely inferable.
- Preserve existing files and settings; apply only the requested changes. Extra setup such as a license, Pages, CI or Dependabot needs to be in scope.
- Report the repository URL and what changed.
