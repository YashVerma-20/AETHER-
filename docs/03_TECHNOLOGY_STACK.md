# AETHER --- Technology Stack

## Approved target stack

  -----------------------------------------------------------------------
  Layer                   Technology              Responsibility
  ----------------------- ----------------------- -----------------------
  Development environment Google Antigravity      Primary environment for
                                                  coding, debugging,
                                                  testing, and project
                                                  workflows

  Frontend                React                   User interface

  Frontend tooling        Vite                    Development server and
                                                  build

  Language                TypeScript              Frontend type safety

  Styling                 Tailwind CSS            UI styling

  Backend                 Python + FastAPI        API and application
                                                  services

  Agent orchestration     LangGraph               Agent workflow
                                                  execution

  Local inference         Ollama                  Local model
                                                  serving/inference

  Database                PostgreSQL              Tasks, runs,
                                                  evaluations, and
                                                  history

  Charts                  Recharts                Performance
                                                  visualization
  -----------------------------------------------------------------------

## Local LLM candidates

Initial candidates: - Qwen3 14B, quantized. - DeepSeek-R1 14B,
quantized.

Test separately. Model tag, quantization, context length, and Ollama
version must be recorded. A fallback to 8B or smaller is based on
measured hardware performance, not assumption.

## Runtime constraints

-   Target machine: Intel Core i5-13550H, 16 GB LPDDR5 RAM, 1 TB SSD, no
    dedicated GPU.
-   No paid hosted model APIs or cloud compute.
-   Start with one model loaded at a time.
-   Start with short context and sequential agent execution.
-   Measure memory and latency with the rest of the development stack
    running before accepting a configuration.

## Dependency policy

Use only dependencies justified by an implementation requirement.
Inspect current versions and compatibility before adding packages. Avoid
unnecessary dependencies, upgrades, or duplicate libraries. Record
material dependency decisions.

## Configuration

Use environment variables for local configuration. Keep `.env` out of
version control. Provide `.env.example` with placeholders only. Never
commit secrets.
