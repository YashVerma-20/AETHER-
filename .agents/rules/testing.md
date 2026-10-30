# AETHER Testing and Verification Rule

## Before testing

-   Identify the expected behavior and acceptance criteria.
-   Inspect available test commands and project scripts.
-   Do not invent commands or claim a test suite exists without
    checking.

## Verification

Run the narrowest relevant checks first, then broader checks where
practical: - Unit tests for changed logic. - Integration tests for
affected services. - Frontend lint/build checks for frontend changes. -
Backend tests and type/static checks where configured. - End-to-end or
manual runtime checks for integrated behavior.

## Report exact status

For each check, report one of: - PASSED --- executed and passed. -
FAILED --- executed and failed; include the relevant error. - BLOCKED
--- could not execute due to a dependency or environment issue. - NOT
RUN --- not attempted.

Include the actual command and a concise result. Do not convert warnings
into passes or omit failing tests.

## Research integrity

-   Keep benchmark inputs, model identifiers, quantization, context
    settings, prompts, and evaluation rubrics recorded.
-   Do not compare baseline and adaptive runs under materially different
    conditions unless explicitly testing that difference.
-   Do not invent token usage or monetary costs for local inference.
-   Preserve failed runs and negative findings.
-   Distinguish measured values from estimates and subjective judgments.
-   Do not use unvalidated model self-evaluation as ground truth.

## Phase completion

A phase is complete only when its documented acceptance criteria have
been met and evidence is recorded. If any criterion is incomplete, mark
the phase `IN PROGRESS` or `BLOCKED`, not `COMPLETED`.
