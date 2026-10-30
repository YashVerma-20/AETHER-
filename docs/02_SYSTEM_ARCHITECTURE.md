# AETHER --- Target System Architecture

## Identity

AETHER = **Adaptive Evaluation and Teaming through Historical Evidence
and Reasoning**.

## Logical architecture

``` text
React Frontend
  ├── Task Submission
  ├── Execution Results
  └── Performance Dashboard
          |
          v
FastAPI Backend
  ├── Request validation and task services
  ├── Run management and result APIs
  └── Application coordination
          |
          v
AETHER Adaptive Controller (Python)
  ├── Task analysis
  ├── Capability and constraint evaluation
  ├── Candidate workflow selection
  ├── Historical evidence retrieval
  └── Explainable decision record
          |
          v
LangGraph Orchestration
  ├── Selected agent nodes
  ├── Conditional transitions
  ├── Bounded review/revision
  └── Execution state and failure handling
          |
          v
Local Ollama Runtime
  └── One selected quantized open-weight model at a time
          |
          v
PostgreSQL
  ├── Tasks
  ├── Runs and agent executions
  ├── Team selections
  ├── Evaluations
  └── Feedback and performance history
```

## Component responsibilities

-   React: user interaction and visualization.
-   FastAPI: application API, validation, and service coordination.
-   Python controller: task-aware and evidence-informed workflow
    selection.
-   LangGraph: execution of selected agent workflows.
-   Ollama: local LLM inference.
-   PostgreSQL: persistent task, execution, evaluation, and history
    records.
-   Evaluation module: consistent measurement and scoring.

## Baseline workflow

Researcher → Analyst → Writer → Reviewer → Final response.

Use bounded retries and a fixed, documented revision policy.

## Adaptive workflow

Task analysis → candidate workflow generation → constraint checks →
selection using rules and available validated history → LangGraph
execution → evaluation → history update.

Example workflows are illustrative: - Simple: Analyst → Writer. -
Research-intensive: Researcher → Analyst → Writer. -
Verification-sensitive: Analyst → Writer → Reviewer. - Complex:
Researcher → Analyst → Writer → Reviewer.

Do not hard-code these examples as universally optimal.

## Feedback loop

Evaluate → Remember → Adapt → Collaborate → Evaluate.

Only validated evaluation evidence should influence future selection.
Store sample counts and avoid overconfidence from sparse history.

## Model and hardware approach

Test quantized 14B models first (Qwen3 14B and DeepSeek-R1 14B
separately). Measure actual RAM use, load time, latency, stability, and
quality. If not practical, evaluate 8B and then smaller candidates.
Begin with short context and sequential agent execution.

## Architecture boundaries

The LLM performs task-level language/reasoning work. The Python
controller owns team-selection policy and resource constraints.
LangGraph executes the selected workflow. PostgreSQL stores evidence. Do
not delegate the entire adaptive controller to an unconstrained LLM.

## Important limitation

This is a logical target architecture. Do not claim every component is
implemented until repository inspection and tests confirm it.
