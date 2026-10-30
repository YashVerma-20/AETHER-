# AETHER --- Antigravity Workspace Instructions

## Project identity

AETHER means **Adaptive Evaluation and Teaming through Historical
Evidence and Reasoning**.

Full project title: **Adaptive Multi Agent Intelligence: A
Performance-Aware Framework for Dynamic Agent Collaboration and
Evaluation**.

Google Antigravity is the primary development environment throughout
this project. It is an IDE/agentic development environment, not a
replacement for the runtime technologies.

## Source of truth

Before acting, read: 1. `AGENTS.md` 2. `.agents/rules/architecture.md`
3. `.agents/rules/development-safety.md` 4. `.agents/rules/testing.md`
5. Relevant documents in `docs/` 6. `docs/logs/PHASE_PROGRESS.md` 7. The
latest relevant entries in `docs/logs/ANTIGRAVITY_MASTER_LOG.md`

If instructions conflict, do not guess. Identify the conflict and ask
the project owner. The approved project documents and explicit owner
decisions take precedence over assumptions made by the agent.

## Current project status

This pack establishes Stage A project references. It does not prove that
any application component exists, works, or has been tested. Inspect the
repository and record the actual state before implementation. Do not
overwrite or rebuild existing work merely because this roadmap describes
a fresh target architecture.

## Operating procedure for every work session

1.  Identify the active phase, task, scope, and acceptance criteria.
2.  Inspect the repository, Git status, relevant files, and existing
    implementation before editing.
3.  Present a concise plan for non-trivial changes. Wait for approval
    where the safety rules require it.
4.  Make the smallest change that satisfies the approved task.
5.  Run relevant tests, builds, and runtime checks where possible.
6.  Record actual files changed, commands executed, test outcomes,
    errors, decisions, and remaining work in
    `docs/logs/ANTIGRAVITY_MASTER_LOG.md`.
7.  Update `docs/logs/PHASE_PROGRESS.md` only when evidence supports the
    status change.
8.  Update `docs/logs/CHANGELOG.md` for meaningful project changes.
9.  Report what was changed and what was not verified.

## Non-negotiable constraints

-   No paid LLM APIs or hosted LLM API keys.
-   No paid cloud services or paid compute.
-   Target inference is local Ollama on the user's existing laptop.
-   Test quantized 14B candidates first; use smaller models only if
    measured hardware constraints make 14B impractical.
-   Do not assume a model will fit or run smoothly. Measure RAM,
    latency, stability, and output quality.
-   Use the same underlying model and comparable settings for
    baseline/adaptive experiments unless a specific experiment is
    explicitly designed to compare models.
-   The primary research contribution is performance-aware, explainable,
    history-informed agent-team selection and evaluation---not merely
    integrating an LLM or creating multiple agents.
-   Google Antigravity is the primary development environment.
-   Keep secrets out of source control and logs.

## Change control

Do not independently: - Change the approved architecture or technology
stack. - Replace a technology with a different framework or service. -
Add paid dependencies or external services. - Delete files, rewrite
working modules, rename major directories, or perform broad refactors. -
Change database schemas in a destructive or incompatible way. - Change
experimental controls, metrics, or evaluation procedures after results
have been collected.

For any such change, explain the reason, alternatives, impact,
migration/rollback plan, and request owner approval before proceeding.

## Accuracy and reporting

-   Never claim a feature is implemented unless the repository supports
    that claim.
-   Never claim a test/build passed unless it was actually executed and
    passed.
-   Distinguish `not run`, `blocked`, `failed`, and `passed`.
-   Do not invent benchmark results, token counts, costs, timings, or
    model capabilities.
-   Do not mark a phase complete until its acceptance criteria are
    verified.
-   Preserve failed runs and negative results in research records.
-   Record assumptions explicitly and seek confirmation for material
    unknowns.

## Completion report format

For each task, report: - Task and active phase - Summary of work - Files
created/modified/deleted - Commands executed - Tests/builds and exact
outcomes - Known issues or unverified items - Logbook entry reference -
Remaining tasks and requested decisions
