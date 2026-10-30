# AETHER Architecture Rule

This rule applies whenever architecture, dependencies, runtime services,
interfaces, or data flow are being designed or changed.

## Approved target architecture

-   Frontend: React, Vite, TypeScript, Tailwind CSS.
-   Backend: Python and FastAPI.
-   Agent orchestration: LangGraph.
-   Local LLM runtime: Ollama.
-   Initial model trials: quantized Qwen3 14B and DeepSeek-R1 14B,
    tested separately.
-   Persistence: PostgreSQL.
-   Charts: Recharts.
-   Primary development environment: Google Antigravity.
-   Local-first operation; no paid hosted LLM APIs or paid cloud
    infrastructure.

## Core system responsibilities

1.  Frontend collects tasks and constraints, presents execution results,
    and visualizes measured performance.
2.  FastAPI validates requests, coordinates application services, and
    exposes APIs.
3.  AETHER's Python adaptive controller analyzes task requirements,
    constraints, capabilities, and historical evidence.
4.  LangGraph executes the workflow selected by the controller.
5.  Ollama performs local model inference.
6.  PostgreSQL stores tasks, runs, agent executions, selections,
    evaluations, and feedback.
7.  Evaluation components measure task success, output quality, latency,
    resource usage, reliability, and collaboration effectiveness.

## Baseline and adaptive configurations

-   Baseline: fixed Researcher → Analyst → Writer → Reviewer workflow.
-   Adaptive: dynamically selected workflow based on task requirements,
    resource constraints, and validated historical evidence.
-   Keep model, task set, model settings, and evaluation method
    comparable when testing controller effects.
-   Add a history-aware adaptive condition separately from a rules-only
    adaptive condition when the experiment requires isolating historical
    evidence.

## Agent roles

-   Researcher: organizes relevant information and evidence available to
    the system.
-   Analyst: reasons over evidence, compares alternatives, and
    identifies assumptions.
-   Writer: produces a coherent task response.
-   Reviewer: checks correctness, completeness, relevance, and
    consistency.

Do not claim internet research, browsing, or external tool access unless
those capabilities have actually been implemented and configured.

## Model strategy

Test quantized 14B models first, one model at a time. Use short context
windows and sequential agent execution initially. Measure actual memory,
loading time, latency, generation speed where available, stability, and
quality. Fall back to 8B and then smaller models only based on evidence.
Never infer runtime memory from download size alone.

## Architecture change protocol

Before proposing a change, document: - Problem being solved - Current
design and limitation - Proposed change - Alternatives - Impact on cost,
local hardware, data, APIs, experiments, and maintainability - Migration
and rollback plan

Do not implement material architecture changes without explicit owner
approval.
