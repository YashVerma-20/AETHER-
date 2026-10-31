# AETHER — Database Schema and Data Dictionary

**Document ID:** AETHER-DB-001  
**Version:** 1.0 (Phase 3 Baseline)  
**Status:** Approved Schema Specification  
**Database Engine:** PostgreSQL 17  
**Database Name:** `aether_db` (Port 5433)  
**ORM:** SQLAlchemy 2.1  
**Migration Tool:** Alembic 1.20  

---

## 1. Relational Architecture Overview

The database design implements the scientific data model required for AETHER's multi-agent experimentation across Groups A, B, and C. It guarantees strict separation between:
1. **Experimental Units:** The 60 distinct tasks (`tasks`).
2. **Replicate Technical Executions:** The $R=3$ technical replicates per task per condition (`experimental_runs`).
3. **Objective System Telemetry:** Deterministic wall-clock latency, token counts, and constraint evaluations (`performance_measurements`, `agent_execution_records`).
4. **Subjective Evaluator Judgments:** Rubric scores evaluated via double-blind scoring (`rubric_quality_score`, `rubric_correctness`, etc.).
5. **Explainability & Traceability:** Capability gap vectors, triggered rule IDs, and retrieved historical case citations (`team_selection_decisions`, `decision_explanations`).
6. **Experience Store with Protocol Provenance:** Historical performance records tagged with experimental protocol (`CALIBRATION` vs `HELD_OUT` vs `ONLINE_BATCH`) to prevent data leakage (`historical_performance_records`).

---

## 2. Entity Specifications & Data Dictionary

### 2.1 `tasks` (Experimental Units, N=60)
The primary unit of statistical analysis.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique identifier for task entity |
| `task_key` | VARCHAR(64) | UNIQUE, NOT NULL, INDEX | Human-readable key (e.g. `TASK-001`) |
| `title` | VARCHAR(255) | NOT NULL | Task summary title |
| `prompt` | TEXT | NOT NULL | Raw input prompt administered to agent teams |
| `category` | VARCHAR(64) | NOT NULL, INDEX | Domain category (`RESEARCH`, `ANALYSIS`, `WRITING`, `CODE`) |
| `complexity_level` | INTEGER | NOT NULL, INDEX | Complexity rating (`1=Low`, `2=Moderate`, `3=High`) |
| `protocol_split` | VARCHAR(32) | NOT NULL | Evaluation dataset split (`CALIBRATION` or `HELD_OUT`) |
| `deterministic_constraints`| JSONB | NOT NULL, DEFAULT `{}` | Structured constraint rules (JSON schema, forbidden words, length) |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Record modification timestamp |

---

### 2.2 `experimental_conditions` (Experimental Groups)
Represents the three experimental treatment arms.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR(32) | PRIMARY KEY | Condition identifier (`GROUP_A`, `GROUP_B`, `GROUP_C`) |
| `name` | VARCHAR(128) | NOT NULL | Human-readable condition title |
| `description` | TEXT | NULLABLE | Detailed description of orchestration policy |
| `historical_memory_enabled`| BOOLEAN | NOT NULL, DEFAULT `FALSE` | Flag controlling access to historical records |
| `selection_policy` | VARCHAR(64) | NOT NULL | Controller policy (`FIXED_PIPELINE`, `DETERMINISTIC_RULES`, `UTILITY_OPTIMIZATION`) |
| `created_at` | TIMESTAMPTZ | NOT NULL | Condition definition timestamp |

---

### 2.3 `experimental_runs` (Replicate Executions, R=3 per Task/Condition)
Individual execution attempts. Repeated runs for the same task are never collapsed into a single row.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique run identifier |
| `task_id` | UUID | FK -> `tasks.id` (ON DELETE CASCADE), INDEX | Parent task reference |
| `condition_id` | VARCHAR(32) | FK -> `experimental_conditions.id`, INDEX | Experimental condition reference |
| `run_number` | INTEGER | NOT NULL | Technical replicate sequence (`1`, `2`, or `3`) |
| `status` | VARCHAR(32) | NOT NULL, INDEX | Execution status (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`) |
| `model_id` | VARCHAR(64) | NOT NULL, DEFAULT `qwen2.5:7b` | Specific LLM model identifier used |
| `model_quantization` | VARCHAR(32) | NOT NULL, DEFAULT `Q4_K_M` | Quantization format |
| `context_window` | INTEGER | NOT NULL, DEFAULT `4096` | Inference context length limit |
| `temperature` | FLOAT | NOT NULL, DEFAULT `0.2` | Sampling temperature |
| `random_seed` | INTEGER | NULLABLE | Random seed for reproducibility |
| `final_output` | TEXT | NULLABLE | Combined final response text |
| `error_message` | TEXT | NULLABLE | Stack trace or failure description |
| `started_at` | TIMESTAMPTZ | NULLABLE | Execution start timestamp |
| `completed_at` | TIMESTAMPTZ | NULLABLE | Execution termination timestamp |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

*Index:* Unique composite index on `(task_id, condition_id, run_number)`.

---

### 2.4 `agent_execution_records` (Node-Level Telemetry)
Captures execution traces of individual agent nodes within a run.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique trace identifier |
| `run_id` | UUID | FK -> `experimental_runs.id` (ON DELETE CASCADE), INDEX | Parent run reference |
| `agent_name` | VARCHAR(64) | NOT NULL | Node name (`Researcher`, `Analyst`, `Writer`, `Reviewer`) |
| `execution_order` | INTEGER | NOT NULL | Execution sequence index (`1, 2, 3...`) |
| `prompt_tokens` | INTEGER | NULLABLE | Prompt token count (NULL if unavailable, never invented) |
| `completion_tokens`| INTEGER | NULLABLE | Generated token count (NULL if unavailable, never invented) |
| `latency_ms` | INTEGER | NULLABLE | Agent invocation latency in milliseconds |
| `status` | VARCHAR(32) | NOT NULL, DEFAULT `COMPLETED` | Node execution status (`COMPLETED`, `FAILED`, `SKIPPED`) |
| `input_payload` | JSONB | NULLABLE | Serialized input payload to agent |
| `output_payload` | JSONB | NULLABLE | Serialized output payload from agent |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

---

### 2.5 `performance_measurements` (Telemetry & Evaluation)
Stores deterministic system measurements and separated subjective quality evaluations for each run.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique measurement identifier |
| `run_id` | UUID | FK -> `experimental_runs.id` (ON DELETE CASCADE), UNIQUE | One-to-one parent run link |
| `wall_clock_ms` | INTEGER | NULLABLE | Total wall-clock duration ($T_{\text{wall}}$) |
| `total_prompt_tokens` | INTEGER | NULLABLE | Cumulative prompt tokens ($C_{\text{token}}$) |
| `total_completion_tokens` | INTEGER | NULLABLE | Cumulative completion tokens |
| `total_tokens` | INTEGER | NULLABLE | Cumulative total tokens processed |
| `constraint_success` | BOOLEAN | NULLABLE | Binary deterministic constraint check ($S_{\text{task}}$) |
| `constraint_details` | JSONB | NULLABLE | Per-constraint pass/fail evaluation results |
| `rubric_quality_score` | FLOAT | NULLABLE | Multi-dimensional response quality ($Q_{\text{out}} \in [0.0, 1.0]$) |
| `rubric_correctness` | FLOAT | NULLABLE | Correctness sub-score |
| `rubric_completeness` | FLOAT | NULLABLE | Completeness sub-score |
| `rubric_coherence` | FLOAT | NULLABLE | Coherence sub-score |
| `evaluated_by` | VARCHAR(64) | NULLABLE | Evaluator identifier (`AUTOMATED_DETERMINISTIC`, `HUMAN_AUDITOR`) |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

---

### 2.6 `team_selection_decisions` (Controller Teaming Decisions)
Stores the teaming decisions made by the controller before or during execution.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique decision identifier |
| `run_id` | UUID | FK -> `experimental_runs.id` (ON DELETE CASCADE), UNIQUE | Associated run |
| `task_id` | UUID | FK -> `tasks.id` (ON DELETE CASCADE), INDEX | Target task |
| `condition_id` | VARCHAR(32) | FK -> `experimental_conditions.id`, INDEX | Experimental condition |
| `selected_topology` | JSONB | NOT NULL | Array of selected agent roles (e.g. `["Analyst", "Writer"]`) |
| `candidate_topologies` | JSONB | NULLABLE | Topologies evaluated prior to final selection |
| `capability_gap_vector` | JSONB | NULLABLE | Vector of required vs. available capabilities |
| `triggered_rule_ids` | JSONB | NULLABLE | List of rule IDs invoked in Group B or C |
| `historical_case_ids` | JSONB | NULLABLE | List of historical cases retrieved in Group C |
| `confidence_score` | FLOAT | NULLABLE | Heuristic discounting confidence ($w_{\text{conf}} \in [0.0, 1.0]$) |
| `latency_estimate_ms` | INTEGER | NULLABLE | Unverified theoretical latency projection |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

---

### 2.7 `decision_explanations` (Explainability & Traceability, H4)
Provides complete natural-language and rule justifications for team selections.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique explanation identifier |
| `decision_id` | UUID | FK -> `team_selection_decisions.id` (ON DELETE CASCADE), UNIQUE | Parent decision reference |
| `justification_text` | TEXT | NOT NULL | High-level natural language explanation |
| `rule_rationale` | TEXT | NULLABLE | Specific rules and boundary conditions triggered |
| `historical_evidence_summary` | TEXT | NULLABLE | Summary of past performance retrieved |
| `tradeoff_analysis` | TEXT | NULLABLE | Pareto tradeoff analysis justification |
| `human_rated_understandability` | FLOAT | NULLABLE | Likert score (1-5) assessed during Phase 5 human audit |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

---

### 2.8 `historical_performance_records` (Group C Experience Store)
Aggregated performance store queried by Group C controller to evaluate candidate topologies.

#### Protocol Provenance and Held-Out Data Leakage Prevention:
To prevent circular evaluation and data leakage in accordance with Section 6 of `05_RESEARCH_DESIGN.md`:
1. **Calibration Tasks (N=40):** Populates historical aggregates tagged with `protocol_origin = 'CALIBRATION'`.
2. **Frozen History Freeze:** Prior to held-out evaluation, historical aggregates are frozen (`protocol_origin = 'FROZEN'`).
3. **Held-Out Test Tasks (N=20):** Group C queries historical evidence strictly where `protocol_origin IN ('CALIBRATION', 'FROZEN')`. No evaluation outcomes from held-out runs are permitted to update or create historical aggregates during the held-out testing phase.
4. **Source Run Traceability:** Every aggregate record stores `source_run_ids` (JSONB array of contributing `experimental_runs.id` UUIDs), ensuring full bi-directional auditability from aggregate back to individual technical runs.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique record identifier |
| `task_category` | VARCHAR(64) | NOT NULL, INDEX | Task category (`RESEARCH`, `ANALYSIS`, etc.) |
| `complexity_level` | INTEGER | NOT NULL, INDEX | Complexity rating (`1`, `2`, `3`) |
| `topology_signature` | VARCHAR(128) | NOT NULL, INDEX | Canonical topology string (e.g. `Analyst->Writer`) |
| `protocol_origin` | VARCHAR(32) | NOT NULL | Protocol provenance (`CALIBRATION`, `FROZEN`, `ONLINE_BATCH`) |
| `source_run_ids` | JSONB | NOT NULL, DEFAULT `[]` | List of contributing `experimental_runs.id` UUIDs for full traceability |
| `sample_count` | INTEGER | NOT NULL, DEFAULT `0` | Number of verified runs aggregated ($N_{C,T}$) |
| `mean_wall_clock_ms` | FLOAT | NULLABLE | Mean latency across historical runs |
| `std_wall_clock_ms` | FLOAT | NULLABLE | Standard deviation of latency |
| `mean_quality_score` | FLOAT | NULLABLE | Mean rubric quality score |
| `std_quality_score` | FLOAT | NULLABLE | Standard deviation of quality score |
| `mean_tokens` | FLOAT | NULLABLE | Mean tokens processed |
| `success_rate` | FLOAT | NULLABLE | Constraint success percentage |
| `last_updated_at` | TIMESTAMPTZ | NOT NULL | Last update timestamp |
| `created_at` | TIMESTAMPTZ | NOT NULL | Record creation timestamp |

*Index:* Unique composite index on `(task_category, complexity_level, topology_signature, protocol_origin)`.
