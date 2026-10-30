# AETHER Development Safety Rule

## Inspect before editing

Before changing code: - Inspect the repository tree and relevant source
files. - Check Git status and recent history when Git is available. -
Identify existing implementations, tests, conventions, and
dependencies. - Check whether the requested functionality already
exists. - Report unexpected or uncommitted changes before touching
affected files.

## Minimal-change principle

-   Make the smallest targeted change that satisfies the task.
-   Preserve existing working behavior.
-   Do not rewrite or regenerate entire files when a focused edit is
    sufficient.
-   Do not perform unrelated cleanup, formatting sweeps, dependency
    upgrades, renaming, or refactoring.
-   Do not create placeholder modules or speculative features merely to
    fill the roadmap.

## Approval required

Ask the project owner before: - Deleting or moving files. - Replacing
frameworks, libraries, databases, or major dependencies. - Changing
public API contracts or database schemas in a breaking way. -
Introducing paid services, external accounts, API keys, or cloud
resources. - Changing model strategy or experimental controls. -
Modifying files outside the approved task scope. - Running destructive
commands or migrations that may lose data. - Making broad refactors or
changing established architecture.

## Data and secrets

-   Never commit API keys, passwords, tokens, private data, or local
    secret files.
-   Keep `.env` out of Git; maintain `.env.example` with placeholders
    only.
-   Do not place secrets in prompts, logs, screenshots, or
    documentation.
-   Do not delete experiment data or historical records without explicit
    approval.
-   Back up important data before potentially destructive operations.

## Git discipline

-   Inspect status before work.
-   Do not discard, reset, or overwrite user changes.
-   Use focused commits/checkpoints when requested or approved.
-   Never amend, force-push, or rewrite shared history without approval.
-   Record commit IDs in the work log when available.

## Uncertainty

If requirements, existing behavior, or intended scope are unclear, stop
and ask one focused question rather than guessing.
