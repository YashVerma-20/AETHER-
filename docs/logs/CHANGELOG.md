# AETHER --- Changelog

Meaningful project changes are recorded here in concise form. Detailed
work-session history belongs in `ANTIGRAVITY_MASTER_LOG.md`.

## \[Unreleased\]

### Added --- 2026-10-30
 
 -   Prepared Stage A documentation pack for AETHER.
 -   Added Antigravity workspace instructions and
     safety/testing/architecture rules.
 -   Added project master reference, initial requirements, target
     architecture, technology stack, and 12-phase roadmap.
 -   Added master development log, phase tracker, and changelog.
 -   Initialized Git repository and synchronized documentation baseline to
     GitHub remote (`origin/main` at `9e06cac`).
 -   Configured isolated Python virtual environment at `.venv/` (Python 3.13.1,
     pip 26.2.2).
 -   Created root `.gitignore` to exclude `.venv/`, caches, and secrets.
 -   Updated `INSTALLATION.md` with Python venv instructions.
 -   Completed Phase 1 Research and Requirements specifications:
     - Formulated formal system requirements (`docs/01_PROJECT_REQUIREMENTS.md`) with FR-001–FR-012, NFR-001–NFR-009, and traceability matrix.
     - Formulated comprehensive research design (`docs/05_RESEARCH_DESIGN.md`) with RQ1–RQ5, H1–H5, experimental groups A, B, and C, control variables, and metrics M-01–M-08.
     - Defined complete agent specifications (`docs/06_AGENT_SPECIFICATIONS.md`) for Researcher, Analyst, Writer, and Reviewer, including state schemas and pruning rules.
     - Established risk and assumptions register (`docs/07_RISK_AND_ASSUMPTIONS_REGISTER.md`) with mitigations for host memory, thermal variation, and cold-start.
     - Updated project master reference (`docs/00_PROJECT_MASTER_REFERENCE.md`) and phase tracker (`docs/logs/PHASE_PROGRESS.md`).
 -   Refined Phase 1 Research Methodology & Governance:
     - Added Literature Review & Related Work in `docs/05_RESEARCH_DESIGN.md` citing AutoGen, MetaGPT, ChatDev, FrugalGPT, RouteLLM, Generative Agents, MemGPT, Reflexion, and AgentBench with genuine URLs.
     - Refined statistical methodology: 3 repeated runs per task ($N=60, R=3, 540$ runs total), paired Wilcoxon signed-rank / Student's t-test, Shapiro-Wilk normality tests, 95% CIs, effect sizes (Cohen's $d$, Cliff's delta), and execution order randomization.
     - Replaced arbitrary composite Pareto metric with dual-objective Pareto dominance and baseline-normalized index ($J_{\text{pareto}}$).
     - Explicitly marked H3 performance targets ($\ge 30\%$ latency, $\ge 35\%$ tokens, $\le 0.05$ quality degradation) as provisional targets subject to Phase 4 baseline calibration.
     - Refined H5 to eliminate monotonic improvement assumptions, modeling transition entropy, regression tracking, and baseline comparisons.
     - Hardened Group C safeguards: $N \ge 5$ confidence threshold, variance dampening, temporal separation, train/test task partitioning, and separation of objective telemetry from subjective scores.
     - Audited all metrics M-01 through M-08 (clarified agent utilization index $0.25 - 1.50$, split decision record completeness from human understandability, and treated zero failures as aspirational rather than assumed).
 -   Final Phase 1 Methodology Consistency Audit:
     - Formally distinguished 60 task-level experimental units from 540 repeated execution runs ($N=60, R=3$), establishing task-mean aggregation and Linear Mixed-Effects Models (LMM) to account for task-level clustering.
     - Documented exact mathematical assumptions for statistical power ($1-\beta \approx 0.82$ for medium effect $d \ge 0.38$ on $N=60$ paired task means) and declared explicit limitations for small effects.
     - Defined explicit protocols for Group C: Protocol 1 (Frozen-History Held-Out Evaluation on 40 calibration / 20 held-out tasks) to prevent data leakage, and Protocol 2 (Online Continual Adaptation) with strict temporal sequencing.
     - Formalized heuristic confidence weighting ($w_{\text{conf}}$) with variance dampening floor, clarifying it as a bounded engineering discount function rather than calibrated statistical probability.
     - Renamed Metric M-05 to Agent Invocation Ratio ($\eta_{\text{invocations}}$) and decoupled it from unique team size.
     - Verified all 9 cited academic literature entries and updated requirements traceability matrix.

-   Completed Phase 2 Development Environment and Local LLM Feasibility:
     - Verified local Ollama v0.40.13 service running on `http://127.0.0.1:11434`.
     - Confirmed Python 3.13.1 isolated virtual environment (`.venv`) functionality.
     - Followed Qwen-first directive: Evaluated 14B candidates vs 7B on Intel Core i5-13550H / 16 GB RAM host.
     - Downloaded and empirically benchmarked `qwen2.5:7b` (Q4_K_M, 4.7 GB disk footprint).
     - Measured empirical memory: 5.1 GB active RAM in Ollama runner, leaving 2.44 GB free physical RAM during active inference.
     - Measured CPU inference speeds: 7.33–8.24 tokens/sec with verified capabilities across structured JSON extraction, step-by-step logical reasoning, and reviewer constraint checking.
     - Created `docs/08_LOCAL_ENVIRONMENT_SETUP.md` (environment and runtime safety guide).
     - Created `docs/09_LLM_FEASIBILITY_REPORT.md` (feasibility analysis and working model justification).
 -   Phase 2 Evidence Validation Audit:
     - Audited Qwen model series: Clarified that `qwen3` series was NOT TESTED as Ollama currently serves production open weights under `qwen2.5`. Future `qwen3` re-evaluation scheduled for subsequent milestones.
     - Explicitly distinguished verified empirical measurements (`qwen2.5:7b`) from unexecuted registry metadata and memory projections (`qwen2.5:14b` and `deepseek-r1:14b` marked as NOT TESTED).
     - Clarified RAM measurements: 5.76 GB free before model load, 5.1 GB active model allocation in Ollama, leaving ~2.44 GB of free physical RAM during active generation (correcting previous overestimate of >5.5 GB headroom during inference).
     - Marked multi-agent pipeline latency projections (20–45s) as unverified theoretical estimates to be measured empirically in Phase 4.
  -   Completed Phase 3 Backend Foundation and Database:
      - Initialized isolated local PostgreSQL 17 cluster in `D:\AETHER\data\postgres` on port `5433` (`scram-sha-256`, `shared_buffers = 64MB`, `max_connections = 30`), preserving host's primary PostgreSQL service on port 5432 untouched.
      - Configured dedicated application database `aether_db` and role `aether_user`.
      - Updated `.gitignore` to exclude `data/` cluster directory and `*.log` files; established safe `.env.example` and local `.env`.
      - Installed and pinned Phase 3 dependencies in `requirements.txt` (`fastapi==0.162.0`, `uvicorn==0.54.0`, `sqlalchemy==2.1.6`, `alembic==1.20.1`, `psycopg[binary]==3.3.6`, `pydantic==2.14.2`, `pydantic-settings==2.16.2`, `pytest==9.2.0`, `httpx==0.28.1`, `pytest-asyncio==1.4.1`).
      - Architected modular backend package under `backend/`: `config.py` (pydantic-settings), `database.py` (engine and session pool), `models.py` (SQLAlchemy models for 8 research entities), `schemas.py` (Pydantic models), `routes/health.py` (live health & DB connectivity verification), and `main.py` (lifespan and CORS).
      - Configured Alembic migrations in `backend/alembic/` and applied initial migration `d7ab4a61601e` establishing all 8 core research tables in `aether_db`.
      - Implemented research schema safeguards: task-level experimental units ($N=60$) distinct from replicate runs ($R=3$); model configuration provenance; nullable token metrics; separation of objective telemetry from subjective rubric scores; explainability linkages; and protocol origin tagging in historical records.
      - Created comprehensive automated test suite `backend/tests/test_foundation.py` verifying startup, health endpoints, live PostgreSQL connectivity, session lifecycle, model cascades, and graceful 503 error handling on database downtime (6/6 tests passing).
      - Authored comprehensive database documentation in `docs/10_DATABASE_SCHEMA.md` and updated `docs/08_LOCAL_ENVIRONMENT_SETUP.md`.
  -   Phase 3 Security, Traceability, and Schema Audit:
      - Rotated exposed PostgreSQL passwords for both `postgres` superuser and `aether_user` using high-entropy random secrets, verifying connectivity without revealing credentials.
      - Stripped hardcoded development password fallback from `backend/config.py` so credentials must load strictly from `.env`.
      - Inspected Git commit history: confirmed `.env` was never committed; confirmed default placeholder was committed in `3355c34` and subsequently neutralized.
      - Confirmed and tested database-level unique constraint on `experimental_runs(task_id, condition_id, run_number)` via automated test `test_experimental_runs_uniqueness_enforcement`.
      - Added `source_run_ids` (JSONB) to `historical_performance_records` via Alembic migration `bee8c24b9098` for complete bi-directional auditability back to contributing experimental runs.
      - Documented held-out data leakage prevention protocols in `docs/10_DATABASE_SCHEMA.md`.
      - Corrected unsupported "zero memory risk" claims in documentation, framing RAM constraints accurately around active monitoring.
      - Expanded test suite to 7 automated tests (7/7 passing).

### Status

-   Phase 1 (Research & Specification), Phase 2 (Environment & Local LLM), and Phase 3 (Backend Foundation & Database) COMPLETED AND VERIFIED.
-   Dedicated local PostgreSQL 17 cluster active on port 5433 with conservative 64MB shared buffers.
-   `qwen2.5:7b` confirmed as verified local working model.
-   Zero commercial API costs incurred (₹0 budget preserved).
-   Phase 4 (Agent Implementation & LangGraph Orchestration) pending explicit authorization.






