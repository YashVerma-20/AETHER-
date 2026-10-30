# AETHER --- Research Design and Methodology

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-RES-001  
**Version:** 2.0 (Phase 1 Refinement Baseline)  
**Status:** Approved for Phase 1 Research Specification

---

## 1. Research Problem and Contribution

### 1.1 Problem Statement
Modern multi-agent architectures typically rely on static pipeline patterns (such as sequential chains of specialist agents) regardless of the specific task difficulty, domain nuance, or resource limits. This static design incurs significant penalties:
1. **Resource Inefficiency:** Simple tasks that require only basic analysis or drafting are forced through an exhaustive chain of agents, consuming excessive tokens, runtime memory, and latency.
2. **Fragility & Error Cascades:** In a static pipeline, errors early in the chain compound downstream. Inflexible review mechanisms either fail to address flaws or loop unconditionally.
3. **Absence of Memory-Driven Optimization:** Multi-agent systems rarely learn from their own execution history. If a two-agent team achieved high quality on a specific category of technical explanation with substantially lower latency, static systems remain incapable of exploiting this historical evidence.

### 1.2 Research Objectives
1. Formalize a dynamic agent-team selection framework that configures execution topologies based on task features and operational constraints.
2. Formulate an empirical performance history model that stores, indexes, and retrieves past multi-agent execution evidence with strict uncertainty and confidence gating.
3. Establish an explainable decision mechanism that justifies why a specific team topology was selected over alternatives.
4. Execute controlled comparative experiments evaluating task quality, execution latency, resource consumption, and reliability across static, rule-based, and history-aware configurations.

### 1.3 Core Scientific Contribution
The primary contribution of AETHER is **not** merely chaining multiple LLM prompts together or building a local chatbot UI. The contribution is the **performance-aware, explainable, and history-informed agent-team selection and evaluation framework**, demonstrating how feedback loops ($\text{Evaluate} \to \text{Remember} \to \text{Adapt} \to \text{Collaborate} \to \text{Evaluate}$) can systematically optimize the Pareto frontier between multi-agent response quality and computational cost on resource-constrained local hardware.

---

## 2. Literature Review and Related Work

To establish clear novelty boundaries, AETHER's architecture is positioned against contemporary research in multi-agent collaboration, dynamic routing, memory systems, and evaluation frameworks.

### 2.1 Multi-Agent Collaboration Frameworks
- **Established Literature:**
  - *AutoGen* (Wu et al., 2023; [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)): Demonstrates multi-agent conversation patterns via customizable conversational agents.
  - *MetaGPT* (Hong et al., 2023; [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)): Encodes Standard Operating Procedures (SOPs) into agent workflows for software engineering tasks.
  - *ChatDev* (Qian et al., 2023; [arXiv:2307.07924](https://arxiv.org/abs/2307.07924)): Utilizes a waterfall model of conversational phases (designing, coding, testing, documenting).
- **Known Limitations:** These architectures operate largely on static, pre-configured roles and sequences. While effective for domain-specific pipelines, they lack performance-aware adaptivity; every prompt triggers the same fixed communication topology regardless of prompt simplicity, local hardware load, or latency deadlines.
- **AETHER's Contribution:** Dynamic role pruning and dynamic graph synthesis conditioned on empirical performance trade-offs.

### 2.2 Dynamic Agent Routing and LLM Routing
- **Established Literature:**
  - *FrugalGPT* (Chen et al., 2023; [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)): Evaluates model cascades to route simple queries to smaller/cheaper models and complex queries to larger commercial APIs.
  - *RouteLLM* (Ong et al., 2024; [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)): Trains preference routers for cost-effective model dispatch.
  - *Dynamic LLM-Agent Selection* (e.g., AutoGen's `GroupChatManager` speaker selection): Uses an LLM to select the next speaker iteratively during execution.
- **Known Limitations:** Model routing selects single models rather than multi-agent collaboration topologies. Conversely, LLM-based next-speaker selection requires an expensive LLM call at *every turn*, increasing inference latency and memory pressure on local CPU/integrated hardware.
- **AETHER's Contribution:** A hybrid controller executing deterministic rule-filtering combined with similarity-weighted historical retrieval, selecting the optimal collaboration topology *ahead of execution* without invoking multi-turn LLM routing overhead.

### 2.3 Historical Memory and Experience in LLM Systems
- **Established Literature:**
  - *Generative Agents* (Park et al., 2023; [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)): Employs memory streams with recency, importance, and relevance retrieval for agent behavior.
  - *MemGPT* (Packer et al., 2023; [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)): Manages hierarchical memory tiers for long-context interactions.
  - *Reflexion* (Shinn et al., 2023; [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)): Uses verbal self-reflection stored in episodic memory to guide subsequent retries.
- **Known Limitations:** Existing episodic memory stores conversational or task facts, or past self-critiques. They do not store structured empirical execution metrics (latency, token costs, failure modes, verified rubric scores) to inform organizational teaming decisions.
- **AETHER's Contribution:** Performance-Aware Historical Memory storing verified quantitative telemetry and qualitative scores to empirically weight team viability across task clusters.

### 2.4 Multi-Agent Evaluation Frameworks
- **Established Literature:**
  - *AgentBench* (Liu et al., 2023; [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)): Evaluates LLM agents across diverse interactive environments.
  - *MT-Bench / Chatbot Arena* (Zheng et al., 2023; [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)): Explores LLM-as-a-judge methodologies and identifies known biases (position, verbosity, self-enhancement).
- **Known Limitations:** Evaluation studies commonly treat LLM self-evaluation as ground truth, or report overall benchmark scores without isolating computational efficiency, memory bounds, or ablation of individual agent nodes.
- **AETHER's Contribution:** A multi-dimensional evaluation methodology combining deterministic constraint verification with double-blind human-anchored rubrics, measuring empirical Pareto trade-offs on resource-constrained hardware.

---

## 3. Research Questions and Refined Testable Hypotheses

### 3.1 Research Questions (RQs)
- **RQ1 (Adaptive Collaboration):** Does dynamically selecting agent teams based on task characteristics improve overall performance compared with a fixed multi-agent pipeline?
- **RQ2 (Historical Evidence):** Does incorporating historical agent performance improve team-selection decisions compared with rule-based adaptation without historical evidence?
- **RQ3 (Resource Efficiency):** Can adaptive collaboration reduce execution latency and token consumption without significantly compromising output quality or task success?
- **RQ4 (Explainability):** Can the framework provide understandable, evidence-supported explanations for agent selection and collaboration decisions?
- **RQ5 (Feedback-Driven Improvement):** Does incorporating previous execution outcomes improve subsequent team-selection decisions under comparable task conditions?

### 3.2 Formal Hypotheses

#### Hypothesis 1 (H1 — Adaptive Performance)
- **Statement:** Dynamic workflow selection based on task complexity and domain produces non-inferior task success rates ($S_{\text{adaptive}} \ge S_{\text{baseline}} - \delta$, where non-inferiority margin $\delta = 0.05$) with statistically significant reductions in mean wall-clock latency compared to a fixed four-agent baseline pipeline across a heterogeneous benchmark task set.
- **Independent Variable:** Orchestration Strategy (Fixed Baseline vs. Rule-Based Adaptive).
- **Dependent Variables:** Task Success Rate ($S_{\text{task}}$), Mean Wall-Clock Latency ($T_{\text{wall}}$ in ms), Output Quality Score ($Q_{\text{out}} \in [0.0, 1.0]$).
- **Control Variables:** Base LLM model and quantization format, prompt templates, temperature ($T=0.2$), random seed, context length limit (4096 tokens), host hardware state.
- **Measurement & Statistical Procedure:** 60 benchmark tasks executed with $R = 3$ repeated runs per task (180 runs per group). Paired comparisons conducted on task-level means. Significance evaluated using the two-tailed Wilcoxon signed-rank test (or paired t-test if differences are normally distributed via Shapiro-Wilk check, $\alpha = 0.05$). Effect size quantified using Cohen's $d$ or Cliff's delta.
- **Evidence to Support:** Statistically significant ($p < 0.05$) reduction in latency with non-inferior quality scores ($\Delta Q > -0.05$).
- **Evidence to Reject:** Latency reduction is non-significant ($p \ge 0.05$), or quality degrades beyond the margin ($\Delta Q \le -0.05$).
- **Confounders:** System thermal throttling and OS background processes (mitigated through hardware monitoring, execution order randomization, and cold-run discards).

#### Hypothesis 2 (H2 — Historical Evidence Value & Pareto Dominance)
- **Statement:** On recurring task categories with verified historical records ($N \ge 5$), history-aware adaptive collaboration (Group C) Pareto-dominates rule-based adaptive collaboration (Group B) by achieving equivalent or superior quality ($Q_C \ge Q_B - 0.02$) at lower latency ($T_C < T_B$), or higher quality ($Q_C > Q_B$) at equivalent latency.
- **Independent Variable:** Historical Memory Integration (Enabled with confidence-weighted retrieval vs. Disabled rule-based).
- **Dependent Variables:** Output Quality Score ($Q_{\text{out}}$), Wall-Clock Latency ($T_{\text{wall}}$), Normalized Pareto Trade-Off Index ($J_{\text{pareto}}$).
- **Control Variables:** Task categories, model weights, prompt templates, hardware environment.
- **Measurement Procedure:** Sequential execution over recurring task clusters. Pareto dominance evaluated via joint coordinate analysis in $(T_{\text{wall}}, Q_{\text{out}})$ space.
- **Evidence to Support:** Group C data points strictly dominate or lie on an advanced empirical Pareto frontier relative to Group B on recurring task sets with $N \ge 5$ historical cases.
- **Evidence to Reject:** Group C selection converges to identical topologies as Group B, or displays Pareto inferiority due to noisy or outdated historical records.
- **Confounders:** Small sample volatility, historical record stale-bias.

#### Hypothesis 3 (H3 — Resource Optimization)
- **Statement:** For tasks classified as Low or Moderate complexity (complexity $\le 2$), adaptive pruning of unnecessary agent roles (e.g., executing `{Analyst, Writer}` instead of the full pipeline) yields substantial reductions in wall-clock latency and token consumption without statistically significant degradation in task quality.
  - *Provisional Targets (Requiring Phase 2/4 empirical baseline calibration):* Latency reduction target $\ge 30\%$, token reduction target $\ge 35\%$, quality degradation bound $\le 0.05$.
- **Independent Variable:** Team Configuration (Full 4-Agent vs. Pruned Topologies).
- **Dependent Variables:** Generated token count ($C_{\text{token}}$), wall-clock latency ($T_{\text{wall}}$), quality score ($Q_{\text{out}}$).
- **Control Variables:** Prompt content, model temperature ($T = 0.2$), task complexity rating.
- **Measurement Procedure:** Sub-group analysis of Low/Moderate complexity tasks comparing Group A vs. Group B.
- **Evidence to Support:** Statistically significant reductions in token count and latency meeting calibrated targets, with quality difference $p > 0.05$.
- **Evidence to Reject:** Quality score drops significantly ($p < 0.05$ with large effect size) when roles are pruned.
- **Confounders:** Subjectivity in manual complexity categorization.

#### Hypothesis 4 (H4 — Explainability & Traceability)
- **Statement:** Structured decision records comprising capability gap vectors, triggered rule IDs, and retrieved historical case citations produce verifiable, human-interpretable justifications for 100% of team selections.
- **Independent Variable:** Decision Logging Mechanism (Structured Explanation Record).
- **Dependent Variables:** Decision Record Completeness ($X_{\text{complete}} \in \{0, 1\}$), Human-Rated Understandability ($U_{\text{human}} \in [1, 5]$ on Likert scale).
- **Control Variables:** Evaluation rubric, task set.
- **Measurement Procedure:** Dual evaluation: 100% automated database audit of schema compliance, plus a double-blind human audit of 30 randomly sampled selection explanations evaluated by independent reviewers.
- **Evidence to Support:** $100\%$ automated schema completeness and mean human understandability score $\ge 4.0/5.0$.
- **Evidence to Reject:** Incomplete schema records ($X_{\text{complete}} < 1.0$) or mean human rating $< 3.5/5.0$.
- **Confounders:** Inter-rater variability in human evaluations (mitigated by calculating Krippendorff’s alpha $\ge 0.70$).

#### Hypothesis 5 (H5 — Feedback Convergence and Non-Monotonic Adaptation)
- **Statement:** When exposed to sequential batches of heterogeneous tasks, history-aware adaptation exhibits systematic exploration and stabilization, converging toward optimal topologies for recurring task clusters while explicitly logging and recovering from performance regressions.
- **Independent Variable:** Historical Batch Iteration ($k = 1, 2, 3, 4$).
- **Dependent Variables:** Team Topology Transition Entropy ($H_{\text{topo}}$), Task Cluster Success Rate ($S_k$), Empirical Performance Delta ($\Delta P_k = P_k - P_{k-1}$).
- **Control Variables:** Task cluster distribution, base model parameters.
- **Measurement Procedure:** Run 4 successive batches of 15 tasks containing recurring clusters. Measure topology selection shifts. Explicitly record regressions ($\Delta P_k < 0$), analyze failure causes, and measure recovery in subsequent iterations compared to static Group A baseline.
- **Evidence to Support:** Topology selection entropy decreases over successive iterations for recurring clusters while aggregate success rate improves relative to iteration 1 and exceeds static baseline.
- **Evidence to Reject:** Persistent chaotic oscillation in topology selection without stability or improvement over Group B.
- **Confounders:** Non-stationary task distributions, metric noise.

---

## 4. Rigorous Statistical Methodology

To guarantee scientific validity and eliminate measurement artifacts, the experimental protocol enforces strict statistical controls:

### 4.1 Repeated Executions and Paired Comparisons
- **Repetition Count ($R = 3$):** Each of the 60 benchmark tasks will be executed 3 independent times per experimental group ($60 \times 3 \times 3 = 540$ total experimental runs).
- **Paired Experimental Design:** Tasks serve as their own paired controls across Group A, Group B, and Group C. Comparisons evaluate intra-task performance differences ($\Delta = X_B - X_A$ or $X_C - X_B$).
- **Central Tendency Reporting:** For latency and token counts, both Mean $\pm$ Standard Deviation and Median $\pm$ Interquartile Range (IQR) will be reported to account for skewness.

### 4.2 Randomization, Warm-Up, and Cache Controls
- **Execution Order Randomization:** Tasks and experimental conditions will be executed in randomized block order rather than sequential group blocks. This balances systemic drift, thermal changes, or temporary OS resource contention evenly across all three groups.
- **Model Warm-Up Discards:** Before every experimental session, 2 discardable dummy inference prompts will be executed through Ollama to load model weights fully into memory and compile computation kernels. The first execution after model loading is never included in experimental measurements.
- **Cache Eviction Verification:** Prompt context caching will be disabled or reset between task executions to ensure identical evaluation states.

### 4.3 Hypothesis Testing, Confidence Intervals, and Power Analysis
- **Normality Testing:** Every distribution of differences will be tested for normality using the **Shapiro-Wilk test** ($\alpha = 0.05$).
- **Parametric vs. Non-Parametric Tests:**
  - If normally distributed: Paired two-tailed Student's t-test.
  - If non-normal: Two-tailed **Wilcoxon signed-rank test**.
  - For categorical success rates: **McNemar's test** for paired nominal data.
- **Confidence Intervals & Effect Sizes:** 
  - 95% Confidence Intervals will be computed for all performance deltas.
  - Effect sizes reported as Cohen's $d$ (for parametric) or Cliff's delta / Rank-biserial correlation (for non-parametric).
- **Sample Size Justification & Power Limitations:** With $N = 60$ distinct paired tasks and $R = 3$ repetitions ($N_{\text{total}} = 180$), the experiment is powered to detect medium-to-large effect sizes ($d \ge 0.40$ at $\alpha = 0.05$ with power $1 - \beta = 0.80$). Precise post-hoc power calculations will be reported in Phase 10 based on measured sample variance, explicitly noting limitations if small-effect detection is constrained.

---

## 5. Experimental Design and Conditions

```
+-----------------------------------------------------------------------------------+
|                              EXPERIMENTAL CONDITIONS                              |
+-----------------------------------------------------------------------------------+
| Group A: Fixed Baseline Pipeline                                                  |
|   Topology: Researcher -> Analyst -> Writer -> Reviewer (Always all 4)             |
|   Selection Logic: Static / Invariant                                             |
|   Historical Memory: Disabled (Zero history utilized)                             |
+-----------------------------------------------------------------------------------+
| Group B: Rule-Based Adaptive Collaboration                                        |
|   Topology: Dynamic (e.g., Analyst->Writer, Researcher->Analyst->Writer, etc.)   |
|   Selection Logic: Deterministic rules on Task Features & Constraints             |
|   Historical Memory: Disabled (Zero history utilized)                             |
+-----------------------------------------------------------------------------------+
| Group C: History-Aware Adaptive Collaboration                                     |
|   Topology: Dynamic (Selected via empirical utility optimization)                 |
|   Selection Logic: Task Features + Similarity-Weighted Past Performance Records   |
|   Historical Memory: Enabled (PostgreSQL Historical Execution & Evaluation DB)    |
|   Safeguards: Confidence gating (N >= 5), temporal separation, outlier filtering  |
+-----------------------------------------------------------------------------------+
```

---

## 6. Historical Evidence Safeguards and Data Governance (Group C)

To ensure scientific integrity and prevent historical memory from introducing bias or runaway failures:

### 6.1 Statistical Confidence and Minimum Evidence Gating
- **Sample Size Threshold ($N_{\text{min}} = 5$):** Historical evidence for a specific task cluster and topology will **not** be considered authoritative unless at least $N = 5$ verified past runs exist.
- **Cold-Start Fallback:** When $N < 5$, the controller automatically falls back to Group B rule-based defaults, logging a `COLD_START_FALLBACK` status in the decision explanation.
- **Confidence Weighting:** Historical utility scores are weighted by an empirical confidence factor:
  $$w_{\text{conf}} = \min\left(1.0, \frac{N}{10}\right) \cdot (1.0 - \sigma_{\text{quality}})$$
  where high variance ($\sigma_{\text{quality}}$) dampens historical influence.

### 6.2 Temporal Separation and Leakage Prevention
- **Strict Temporal Sequencing:** Evaluation metrics from run $t$ cannot enter the historical database or influence selection until run $t$ has completely finished, persisted its results, and passed verification.
- **Train/Test Partitioning:** In benchmark experiments, historical data will be populated exclusively from a dedicated set of 40 calibration tasks. The 20 held-out evaluation tasks will test generalization without data leakage.

### 6.3 Handling Sparse, Contradictory, Stale, and Noisy Data
- **Outlier Rejection:** Runs terminated due to host system anomalies (e.g., external OS process interruptions, memory allocation errors) are tagged as `SYSTEM_FAULT` and excluded from the historical performance index.
- **Contradictory Evidence Resolution:** When historical runs for the same topology exhibit bimodal outcomes (e.g., success and failure), the controller selects the conservative topology (higher verification capability) and flags the cluster for investigation.
- **Recency Decay:** While historical records are append-only in PostgreSQL, the retrieval query applies a half-life recency decay to down-weight runs conducted under older configurations or superseded prompt templates.

### 6.4 Separation of Objective Telemetry from Subjective Quality
- Historical records store objective execution facts (`wall_clock_ms`, `token_count`, `agent_call_count`, `deterministic_constraint_success`) strictly separate from subjective rubric evaluation scores (`human_rubric_quality`). The controller can evaluate constraints independently of subjective scores.

---

## 7. Evaluation Metrics Specification

Every metric is defined with its operational formula, measurement unit, data source, and limitations.

### M-01: Wall-Clock Latency ($T_{\text{wall}}$)
- **Definition:** Total elapsed time from task submission to final response delivery.
- **Formula:** $T_{\text{wall}} = t_{\text{end}} - t_{\text{start}}$
- **Unit:** Milliseconds (ms)
- **Data Source:** Backend high-resolution timer (`time.perf_counter_ns()`).
- **Optimization Direction:** Lower is better ($\downarrow$).
- **Limitations:** Influenced by CPU scheduling and background OS tasks. Mitigated by reporting median/IQR over 3 randomized repetitions.

### M-02: Token Consumption Proxy ($C_{\text{token}}$)
- **Definition:** Cumulative count of prompt and completion tokens processed by Ollama across all agents in the run.
- **Formula:** $C_{\text{token}} = \sum_{i=1}^{K} (\text{prompt\_tokens}_i + \text{completion\_tokens}_i)$ where $K$ is the number of agent calls.
- **Unit:** Integer token count.
- **Data Source:** Ollama API response metadata (`prompt_eval_count` + `eval_count`).
- **Optimization Direction:** Lower is better ($\downarrow$).
- **Limitations:** Represents computational workload and memory-bus pressure rather than financial cost (since local inference is ₹0).

### M-03: Task Success Rate ($S_{\text{task}}$)
- **Definition:** Binary indicator whether the output satisfies all explicit deterministic constraints (schema format, section existence, length bounds, factual consistency).
- **Formula:** $S_{\text{task}} = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(\text{run}_j \text{ passes all constraints})$
- **Unit:** Percentage ($0.0\% - 100.0\%$).
- **Data Source:** Automated deterministic validators.
- **Optimization Direction:** Higher is better ($\uparrow$).

### M-04: Output Quality Score ($Q_{\text{out}}$)
- **Definition:** Multi-dimensional score assessing response correctness, completeness, logical coherence, and relevance.
- **Formula:** $Q_{\text{out}} = 0.35 \cdot Q_{\text{correctness}} + 0.25 \cdot Q_{\text{completeness}} + 0.20 \cdot Q_{\text{coherence}} + 0.20 \cdot Q_{\text{relevance}}$
- **Unit:** Normalized scalar ($0.00 - 1.00$).
- **Data Source:** Structured human rubric evaluation on sample subsets, combined with automated deterministic checks. LLM self-evaluation is strictly prohibited as ground truth.
- **Optimization Direction:** Higher is better ($\uparrow$).

### M-05: Agent Utilization Index ($\eta_{\text{agent}}$)
- **Definition:** Total number of agent invocations executed in a run divided by the nominal 4-agent baseline pipeline size.
- **Formula:** $\eta_{\text{agent}} = \frac{K_{\text{invocations}}}{4.0}$
- **Range & Value Explanation:**
  - $\eta = 0.25$ (1 agent invocation, e.g., direct generation).
  - $\eta = 0.50$ (2 agent invocations, e.g., Analyst $\to$ Writer).
  - $\eta = 0.75$ (3 agent invocations, e.g., Researcher $\to$ Analyst $\to$ Writer).
  - $\eta = 1.00$ (4 agent invocations, standard 4-agent single-pass baseline).
  - $\eta = 1.25 - 1.50$ (Up to 5 or 6 agent invocations when a revision cycle occurs, e.g., Writer $\to$ Reviewer $\to$ Writer $\to$ Reviewer).
- **Optimization Direction:** Minimized for low-complexity tasks; scaled proportionally for high-complexity tasks.

### M-06: Pareto Trade-Off Analysis and Efficiency Index
- **Primary Method: Dual-Objective Pareto Dominance:** Quality ($Q_{\text{out}}$) and Latency ($T_{\text{wall}}$) are primarily analyzed as distinct objectives. Condition $X$ dominates Condition $Y$ iff:
  $$(Q_X \ge Q_Y \land T_X \le T_Y) \land (Q_X > Q_Y \lor T_X < T_Y)$$
- **Secondary Composite Index (Normalized Pareto Index, $J_{\text{pareto}}$):**
  To summarize multi-task trends without unit-scaling bias, latency is normalized against the fixed baseline group mean on that specific task:
  $$\hat{T} = \frac{T_{\text{wall}}}{T_{\text{baseline\_mean}}}$$
  $$J_{\text{pareto}} = \frac{Q_{\text{out}}}{\hat{T}}$$
- **Limitations of Composite Index:** Normalization prevents arbitrary millisecond-vs-second scaling distortions, but composite indices compress two independent trade-off dimensions into a single scalar. Therefore, $J_{\text{pareto}}$ will always be presented alongside multi-objective Pareto scatter plots.

### M-07: Decision Traceability & Human-Rated Explainability
- **M-07a: Decision Record Completeness ($X_{\text{complete}}$):** Percentage of runs containing valid, parseable schema records with capability gap vectors, triggered rule IDs, and historical case citations. ($100\%$ target, $\uparrow$).
- **M-07b: Human Understandability Score ($U_{\text{human}}$):** Average score on a 1–5 Likert scale assessed by independent human reviewers evaluating whether the recorded justification clearly explains the topology choice. ($\ge 4.0/5.0$ target, $\uparrow$).

### M-08: Reliability & Failure Rate ($R_{\text{fail}}$)
- **Definition:** The measured percentage of execution attempts that encounter unhandled exceptions, local model timeouts, out-of-memory terminations, or unparseable corrupted responses.
- **Formula:** $R_{\text{fail}} = \frac{N_{\text{failed\_runs}}}{N_{\text{total\_attempts}}} \times 100$
- **Unit:** Percentage.
- **Reporting Clarification:** Zero failure is an aspirational design objective, **not** an assumed outcome. Actual measured failure counts will be rigorously tracked and reported across all phases.

---

## 8. Benchmark Task Dataset Design

The evaluation utilizes a balanced 60-task benchmark suite across 4 domains and 3 complexity levels:

| Domain | Low Complexity (1–2) | Medium Complexity (3) | High Complexity (4–5) | Total Tasks |
| :--- | :--- | :--- | :--- | :--- |
| **Technical Reasoning** | Syntax debugging, unit test writing | Algorithmic explanation, edge-case analysis | Distributed systems failure triage, formal verification | 15 |
| **Synthesis & Summarization** | Executive summary of 1-page memo | Comparative analysis of 2 proposals | Multi-source literature synthesis with conflicting data | 15 |
| **Structured Extraction** | JSON parsing from semi-structured log | Schema normalization from tabular text | Disambiguation of complex entity networks | 15 |
| **Analysis & Critique** | Fact-checking a single claim | Multi-faceted trade-off analysis | Comprehensive policy review with counter-arguments | 15 |
| **Total** | 20 tasks | 20 tasks | 20 tasks | **60 tasks** |

### Execution Protocol
1. **Model Warm-Up:** 2 dummy prompts executed and discarded.
2. **Experimental Run Block:** 60 tasks $\times$ 3 repetitions $\times$ 3 groups = 540 total runs, randomized in block design.
3. **Partitioning:** 40 calibration tasks (populating historical database) and 20 held-out evaluation tasks (evaluating Group C generalization).
