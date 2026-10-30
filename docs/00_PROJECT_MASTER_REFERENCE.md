# AETHER --- Project Master Reference

## Official identity

**AETHER** = **Adaptive Evaluation and Teaming through Historical
Evidence and Reasoning**.

**Full project title:** *Adaptive Multi Agent Intelligence: A
Performance-Aware Framework for Dynamic Agent Collaboration and
Evaluation*.

Use this exact acronym expansion and title consistently in project
documentation, diagrams, reports, and presentations.

## Purpose

AETHER investigates whether dynamically selecting and coordinating AI
agents using task requirements, resource constraints, and validated
historical performance evidence can improve the quality-efficiency
trade-off compared with a fixed multi-agent pipeline.

## Core problem

Conventional multi-agent implementations often apply a static team or
workflow regardless of task complexity, quality requirements, latency
constraints, available resources, or prior outcomes. This can cause
unnecessary agent calls, avoidable latency, and inefficient resource
use.

## Proposed approach

AETHER uses a feedback loop:

**Evaluate → Remember → Adapt → Collaborate → Evaluate**

1.  Analyze the incoming task and constraints.
2.  Determine required capabilities and feasible workflows.
3.  Select a team using transparent rules and, when reliable evidence
    exists, historical performance.
4.  Execute the selected workflow through LangGraph.
5.  Evaluate the outcome and resource use.
6.  Store validated results and use them to inform future selections.

## Research contribution

The central contribution is the performance-aware, explainable,
history-informed agent-team selection and evaluation framework. The LLM,
agents, UI, and orchestration framework are supporting components.

## Baseline

A fixed workflow: Researcher → Analyst → Writer → Reviewer.

## Proposed adaptive system

Select a minimal or larger workflow based on task requirements,
capabilities, resource constraints, and validated historical evidence.
Do not assume every task requires all four agents.

## Agent responsibilities

-   Researcher: organizes relevant information and evidence available to
    the system.
-   Analyst: reasons over findings, compares alternatives, and
    identifies assumptions.
-   Writer: produces the task response.
-   Reviewer: checks correctness, completeness, relevance, and
    consistency.

External browsing or tool use is not implied; document it only if
implemented.

## Approved target stack

-   Development environment: Google Antigravity.
-   Frontend: React, Vite, TypeScript, Tailwind CSS.
-   Backend: Python, FastAPI.
-   Orchestration: LangGraph.
-   Local model runtime: Ollama.
-   Initial model candidates: quantized Qwen3 14B and DeepSeek-R1 14B,
    tested separately.
-   Database: PostgreSQL.
-   Charts: Recharts.

## Resource constraints

-   Additional budget: ₹0.
-   No paid hosted LLM API keys.
-   No paid cloud compute or hosted services.
-   Use the existing laptop for local inference.
-   Hardware reference: Intel Core i5-13550H, 16 GB LPDDR5 RAM, 1 TB
    SSD, no dedicated GPU.
-   14B is an experiment, not a guaranteed smooth configuration.
    Benchmark it. Fall back to 8B and then smaller models only when
    measurements justify it.
-   Start with one model loaded at a time, short contexts, and
    sequential agent execution.

## Research controls

For controller comparisons, keep the underlying model, task set, model
settings, evaluation rubric, hardware, and execution limits comparable.
Separate model-quality experiments from adaptive-controller experiments.

## Status discipline

The roadmap is a target plan, not evidence of implementation. Every
feature must be verified in the repository. Every metric must be
measured or clearly labeled as an estimate. A phase is complete only
after its acceptance criteria are verified.

## Development workflow

Antigravity must follow root `AGENTS.md` and `.agents/rules/`. It must
inspect before editing, make minimal changes, run relevant checks, and
append a factual work-session record to
`docs/logs/ANTIGRAVITY_MASTER_LOG.md`.

## Phase 1 & 2 Status

Phase 1 established the formal requirements, experimental design, agent specifications, evaluation metrics, and risk registers.

Phase 2 established and verified the local development and inference environment:
- `docs/08_LOCAL_ENVIRONMENT_SETUP.md`: Local Ollama setup, Python 3.13.1 `.venv`, and runtime safety configuration.
- `docs/09_LLM_FEASIBILITY_REPORT.md`: Empirical evaluation of Qwen family on host hardware. Selected `qwen2.5:7b` (Q4_K_M) based on measured memory safety (5.1 GB active RAM) and CPU generation speed (7.5–8.2 tok/s), satisfying the ₹0 constraint.

No backend/frontend application code has been implemented. Implementation begins upon explicit authorization of Phase 3.


