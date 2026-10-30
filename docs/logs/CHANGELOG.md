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

### Status

-   Phase 1 Final Methodology Audit COMPLETED and fully verified.
-   Zero application code, dependencies, or model downloads created.
-   Phase 2 (Environment and Local LLM) pending authorization.




