# AETHER --- Risk and Assumptions Register

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-RSK-001  
**Version:** 1.0 (Phase 1 Baseline)  
**Status:** Approved for Phase 1 Research Specification

---

## 1. Technical Risks and Mitigations

| Risk ID | Description | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **TR-01** | **Host Memory Overflow (16 GB RAM Limit):** Running 14B quantized models (Qwen3 14B / DeepSeek-R1 14B) alongside OS, PostgreSQL, FastAPI, and browser may trigger out-of-memory crashes or disk swapping. | Critical | High | 1. Enforce strict single-agent sequential execution (no concurrency).<br>2. Cap context window to 4096 tokens.<br>3. Benchmark RAM in Phase 2; if peak RAM exceeds 12.0 GB, immediately fall back to 8B or 7B quantized models as prescribed in architecture rules. |
| **TR-02** | **Inference Latency Bottlenecks:** CPU-only local inference on Intel Core i5-13550H may result in slow generation speeds (tokens/sec), making 4-agent loops impractically slow for interactive use. | High | High | 1. Use 4-bit quantization (Q4_K_M).<br>2. Bound review loops to maximum 1 iteration.<br>3. Optimize prompt lengths to minimize prompt evaluation time.<br>4. Leverage adaptive pruning to execute 2 or 3 agents instead of 4. |
| **TR-03** | **Model Output Non-Determinism & Parsing Failures:** Local quantized models may occasionally produce malformed JSON, markdown syntax errors, or ignore schema instructions. | Medium | Medium | 1. Implement robust Pydantic parsing with defensive regex fallbacks in backend adapter.<br>2. Implement a single bounded retry with temperature decay on schema parse error. |
| **TR-04** | **PostgreSQL Connection Overhead:** Repeated local database writes for high-frequency agent telemetry could degrade controller responsiveness. | Low | Low | Use SQLAlchemy async connection pooling and bulk telemetry write operations at run completion. |

---

## 2. Research and Methodology Risks and Mitigations

| Risk ID | Description | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **RR-01** | **LLM Evaluation Bias:** Using an LLM to evaluate the quality of another LLM's output introduces systematic leniency, position bias, and circular justification. | High | Medium | 1. Strictly forbid unvalidated LLM self-evaluation as ground truth.<br>2. Rely on objective deterministic checks (schema compliance, constraint verification) for success rate.<br>3. Use double-blind human rubric scoring on benchmark sample sets to anchor automated quality metrics. |
| **RR-02** | **Historical Feedback Instability (Cold-Start & Overfitting):** Early noisy or outlier runs in Group C might lead the history-aware selector to prematurely discard viable topologies. | High | Medium | 1. Enforce a cold-start threshold: Require $N \ge 5$ statistically consistent runs in a task cluster before historical weighting overrides rule defaults.<br>2. Apply confidence dampening based on historical variance ($1.0 - \sigma_{\text{quality}}$).<br>3. Enforce epsilon-greedy exploration ($\epsilon = 0.10$) to periodically re-test alternative topologies. |
| **RR-03** | **Confounding Hardware Variations:** Host background tasks, thermal throttling, or battery states on the laptop could skew latency and token rate measurements. | Medium | Medium | 1. Conduct all comparative benchmark runs under fixed conditions: plugged into AC power, high-performance power plan, idle background apps.<br>2. Log CPU temperature and clock frequency at run start and end; discard outlier runs with thermal throttling spikes. |

---

## 3. Financial and Resource Constraints

| Constraint ID | Description | Hard Limit | Enforcement Mechanism |
| :--- | :--- | :--- | :--- |
| **RC-01** | **Financial Budget:** Zero additional budget. | ₹0 | Zero paid API keys permitted in codebase or `.env`. No cloud subscriptions. Fully open-source local stack. |
| **RC-02** | **Compute Hardware:** Single host laptop (Intel i5-13550H, 16 GB RAM, no GPU). | Local CPU only | Model selection benchmark in Phase 2 strictly validates memory before proceeding. |

---

## 4. Fundamental Project Assumptions

1. **Local LLM Viability:** We assume that modern 4-bit quantized open-weight models (Qwen3 14B or 8B fallbacks) running locally via Ollama possess sufficient instruction-following fidelity to fulfill distinct agent roles (Researcher, Analyst, Writer, Reviewer).
2. **Task Categorization Feasibility:** We assume that user prompts can be reliably mapped into discrete complexity scores and capability requirements using lightweight rule-based or embedding-based heuristics without invoking expensive multi-second analysis.
3. **Pareto Superiority of Adaptive Teaming:** We hypothesize that tailoring team size and role composition to task difficulty outperforms static one-size-fits-all pipelines in resource-constrained environments.
4. **Provisional Performance Targets:** Quantitative efficiency targets in H3 ($\ge 30\%$ latency reduction, $\ge 35\%$ token reduction, $\le 0.05$ quality degradation margin) are provisional targets subject to empirical calibration against baseline measurements in Phase 4.

---

## 5. Unresolved Decisions and Future Milestones

| Decision ID | Description | Current Status | Milestone for Resolution |
| :--- | :--- | :--- | :--- |
| **UD-01** | **Primary Model Selection:** Whether Qwen 14B fits sustainably in 16 GB RAM without OS thrashing, or whether 7B/8B is required. | **RESOLVED:** `qwen2.5:7b` (Q4_K_M) selected based on Phase 2 empirical memory (5.1 GB) and speed (7.5–8.2 tok/s) benchmarks; 14B documented as unsafe for 16 GB host. | Phase 2 (Completed) |
| **UD-02** | **Task Similarity Algorithm:** Choice between lightweight local embedding cosine similarity vs. categorical feature distance for historical case retrieval. | Specification Defined (Categorical feature matching default, vector fallback) | Phase 6 (Adaptive Decision Engine) |
| **UD-03** | **External Context Retrieval:** Designing a local offline retrieval mechanism (e.g., local SQLite/Chroma vector store) to provide the Researcher agent with reference documents without internet access. | Deferred to offline corpora | Phase 4 / Phase 6 |
| **UD-04** | **Calibration of Efficiency Thresholds:** Empirically verifying whether the provisional $\ge 30\%$ latency and $\ge 35\%$ token savings in H3 represent realistic bounds on target hardware. | Open (Awaiting baseline timing data) | Phase 4 / Phase 5 |
| **UD-05** | **Human-Evaluator Cohort:** Establishing the exact size, training rubric, and inter-rater agreement threshold ($\alpha \ge 0.70$) for subjective quality audits. | Specification Defined | Phase 5 / Phase 10 |

