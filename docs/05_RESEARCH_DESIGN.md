# AETHER --- Research Design and Methodology

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-RES-001  
**Version:** 2.1 (Phase 1 Final Audit Baseline)  
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
2. Formulate an empirical performance history model that stores, indexes, and retrieves past multi-agent execution evidence with explicit uncertainty representation and confidence gating.
3. Establish an explainable decision mechanism that justifies why a specific team topology was selected over alternatives.
4. Execute controlled comparative experiments evaluating task quality, execution latency, resource consumption, and reliability across static, rule-based, and history-aware configurations.

### 1.3 Core Scientific Contribution
The primary contribution of AETHER is **not** merely chaining multiple LLM prompts together or building a local chatbot UI. The contribution is the **performance-aware, explainable, and history-informed agent-team selection and evaluation framework**, demonstrating how feedback loops ($\text{Evaluate} \to \text{Remember} \to \text{Adapt} \to \text{Collaborate} \to \text{Evaluate}$) can systematically optimize the Pareto frontier between multi-agent response quality and computational cost on resource-constrained local hardware.

---

## 2. Literature Review and Related Work

To establish clear novelty boundaries, AETHER's architecture is positioned against contemporary research across multi-agent collaboration, dynamic routing, memory systems, and evaluation frameworks.

### 2.1 Multi-Agent Collaboration Frameworks
- **Established Literature:**
  - *AutoGen* (Wu et al., 2023; [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)): Demonstrates multi-agent conversation patterns via customizable conversational agents.
  - *MetaGPT* (Hong et al., 2023; [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)): Encodes Standard Operating Procedures (SOPs) into agent workflows for software engineering tasks.
  - *ChatDev* (Qian et al., 2023; [arXiv:2307.07924](https://arxiv.org/abs/2307.07924)): Utilizes a waterfall model of conversational phases (designing, coding, testing, documenting).
- **Known Limitations:** These architectures operate largely on static, pre-configured roles and sequences. While effective for domain-specific pipelines, they lack performance-aware adaptivity; every prompt triggers the same fixed communication topology regardless of prompt simplicity, local hardware load, or latency deadlines.
- **AETHER's Proposed Contribution:** Dynamic role pruning and dynamic graph synthesis conditioned on empirical performance trade-offs.

### 2.2 Dynamic Agent Routing and LLM Routing
- **Established Literature:**
  - *FrugalGPT* (Chen et al., 2023; [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)): Evaluates model cascades to route simple queries to smaller/cheaper models and complex queries to larger commercial APIs.
  - *RouteLLM* (Ong et al., 2024; [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)): Trains preference routers for cost-effective model dispatch.
  - *Dynamic LLM-Agent Selection* (e.g., AutoGen's `GroupChatManager` speaker selection): Uses an LLM to select the next speaker iteratively during execution.
- **Known Limitations:** Model routing selects single models rather than multi-agent collaboration topologies. Conversely, LLM-based next-speaker selection requires an expensive LLM call at *every turn*, increasing inference latency and memory pressure on local CPU/integrated hardware.
- **AETHER's Proposed Contribution:** A hybrid controller executing deterministic rule-filtering combined with similarity-weighted historical retrieval, selecting the optimal collaboration topology *ahead of execution* without invoking multi-turn LLM routing overhead.

### 2.3 Historical Memory and Experience in LLM Systems
- **Established Literature:**
  - *Generative Agents* (Park et al., 2023; [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)): Employs memory streams with recency, importance, and relevance retrieval for agent behavior.
  - *MemGPT* (Packer et al., 2023; [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)): Manages hierarchical memory tiers for long-context interactions.
  - *Reflexion* (Shinn et al., 2023; [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)): Uses verbal self-reflection stored in episodic memory to guide subsequent retries.
- **Known Limitations:** Existing episodic memory stores conversational facts, persona memories, or past textual self-critiques. They do not store structured empirical execution metrics (latency, token costs, failure modes, verified rubric scores) to inform organizational teaming decisions.
- **AETHER's Proposed Contribution:** Performance-Aware Historical Memory storing verified quantitative telemetry and qualitative scores to empirically weight team viability across task clusters.

### 2.4 Multi-Agent Evaluation Frameworks
- **Established Literature:**
  - *AgentBench* (Liu et al., 2023; [arXiv:2308.03688](https://arxiv.org/abs/2308.03688)): Evaluates LLM agents across diverse interactive environments.
  - *MT-Bench / Chatbot Arena* (Zheng et al., 2023; [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)): Explores LLM-as-a-judge methodologies and identifies known biases (position, verbosity, self-enhancement).
- **Known Limitations:** Evaluation studies commonly treat LLM self-evaluation as ground truth, or report overall benchmark scores without isolating computational efficiency, memory bounds, or ablation of individual agent nodes.
- **AETHER's Proposed Contribution:** A multi-dimensional evaluation methodology combining deterministic constraint verification with double-blind human-anchored rubrics, measuring empirical Pareto trade-offs on resource-constrained hardware.

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
- **Statistical Testing:** Tested at the experimental unit level ($N = 60$ distinct tasks, each aggregated over $R = 3$ repeated runs). Significance evaluated using the paired two-tailed Wilcoxon signed-rank test (or paired t-test if differences satisfy the Shapiro-Wilk normality test, $\alpha = 0.05$). Effect size reported via Cohen's $d$ or Cliff's delta.
- **Evidence to Support:** Statistically significant ($p < 0.05$) reduction in latency with non-inferior quality scores ($\Delta Q > -0.05$).
- **Evidence to Reject:** Latency reduction is non-significant ($p \ge 0.05$), or quality degrades beyond the non-inferiority margin ($\Delta Q \le -0.05$).
- **Confounders:** System thermal throttling and OS background processes (mitigated through hardware monitoring, execution order block randomization, and cold-run discards).

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

## 4. Rigorous Statistical Methodology & Experimental Independence

To maintain strict statistical validity and avoid conflating pseudoreplications with independent experimental units:

### 4.1 Experimental Units vs. Repeated Executions
- **Experimental Unit ($N = 60$ Tasks):** The fundamental unit of statistical inference is the **task**. Each task possesses an inherent difficulty, domain nuance, and required capability set.
- **Repeated Executions ($R = 3$ Runs per Task):** Running each task 3 times per experimental condition yields $60 \times 3 = 180$ runs per group (540 total runs). However, these $R = 3$ runs are **sub-sampling replicates (technical replicates)** intended to smooth out LLM output stochasticity and host scheduling variance; they do **not** constitute independent experimental units.
- **Aggregation Protocol:** For hypothesis testing comparing experimental groups, metric observations across the $R = 3$ runs will be aggregated at the task level (reporting the task-level mean $\bar{x}_i$ and standard deviation $s_i$). The primary statistical tests (Wilcoxon signed-rank test or paired t-test) are executed on the $N = 60$ paired task-level means.
- **Repeated-Measures / Linear Mixed-Effects Modeling (LMM):** To model run-level variance directly without discarding replicate data, a Linear Mixed-Effects Model will be fitted:
  $$y_{ijk} = \mu + \alpha_j + \beta_k + (\alpha\beta)_{jk} + u_i + \epsilon_{ijk}$$
  where $\alpha_j$ is the fixed effect of the experimental condition (Group A, B, C), $\beta_k$ is task complexity, $u_i \sim \mathcal{N}(0, \sigma_u^2)$ is the random intercept for task $i$ (capturing task-level dependence), and $\epsilon_{ijk}$ is the residual error.

### 4.2 Statistical Power Justification and Explicit Assumptions
- **Power Calculation Basis:** For a paired two-tailed comparison ($N = 60$ paired task means) with significance level $\alpha = 0.05$:
  - Under standard asymptotic assumptions (Student's t-distribution for paired differences), a sample size of $N = 60$ achieves a statistical power of $1 - \beta \approx 0.82$ for a medium effect size of Cohen's $d = 0.38$ ($d \ge 0.40$ gives power $> 0.85$).
  - For the non-parametric Wilcoxon signed-rank test, the Asymptotic Relative Efficiency (ARE) compared to the t-test is at least $0.864$ for any continuous distribution (and $0.955$ for normal distributions), meaning $N = 60$ preserves power $1 - \beta \ge 0.78$ for $d \ge 0.40$.
- **Explicit Assumptions & Limitations:**
  1. *Assumption:* Intra-task correlation across replicates is positive and stable ($\rho > 0$).
  2. *Assumption:* Differences between paired task means do not exhibit extreme heavy-tailed outliers (verified via Shapiro-Wilk and outlier inspection).
  3. *Limitation:* The experiment is not powered to detect small effects ($d < 0.25$, power $< 0.45$). If observed quality or latency differences have small effect sizes, they will be reported as statistically inconclusive rather than claiming evidence of equivalence.

### 4.3 Randomization, Warm-Up, and Cache Controls
- **Execution Order Block Randomization:** Tasks and conditions will be executed using randomized block scheduling rather than running Group A followed by Group B. This balances host thermal drift, power states, and background OS processes equally across conditions.
- **Model Warm-Up Discards:** 2 dummy inference prompts will be executed through Ollama prior to any experimental block to ensure model weights are loaded and computation buffers are initialized. The first run after model loading is never recorded.
- **Cache Eviction Verification:** Prompt context caching will be reset between task executions to ensure clean, identical starting memory states.

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

To ensure scientific integrity, prevent data leakage, and establish clear experimental boundaries, Group C is governed by distinct protocols:

### 6.1 Calibration vs. Held-Out Generalization Protocols
To evaluate history-informed adaptation without methodological confounding, the evaluation is structured into two explicit experimental protocols:

1. **Protocol 1 — Frozen-History Held-Out Evaluation (Generalization Test):**
   - **Phase A (Calibration Training, 40 Tasks):** 40 diverse calibration tasks are executed across various topologies to populate the PostgreSQL historical store with verified execution traces and rubric evaluations.
   - **Phase B (Frozen History Freeze):** The historical database is frozen (read-only mode). No new execution records from test tasks are permitted to enter the index.
   - **Phase C (Held-Out Evaluation, 20 Tasks):** The 20 held-out evaluation tasks are executed in Group C. The controller retrieves historical evidence *strictly from the 40 calibration tasks*. This guarantees zero test-task data leakage and rigorously tests cross-task historical generalization.

2. **Protocol 2 — Online Continual Adaptation (Convergence Test for H5):**
   - Conducted as an independent experiment using 4 sequential batches of 15 tasks containing recurring task clusters.
   - In this protocol, each completed task run is evaluated, verified, and appended to the history store with a timestamp $t$. Subsequent task $t+1$ can retrieve evidence from runs $1 \dots t$.
   - Strictly enforces **temporal sequencing**: evaluation metrics from task $t$ can only be ingested after task $t$ has completely terminated and passed validation checks. Forward leakage into simultaneous runs is prevented by the sequential inference lock (NFR-003).

### 6.2 Evidence Confidence and Uncertainty Representation
The confidence weighting mechanism is explicitly defined as a **bounded heuristic discounting function**, not an unvalidated statistical probability distribution:
- **Heuristic Confidence Formula:**
  $$w_{\text{conf}}(C, T) = \min\left(1.0, \frac{N_{C,T}}{10}\right) \cdot \max\left(0.1, 1.0 - \frac{s_{\text{quality}}}{0.5}\right)$$
  where:
  - $N_{C,T}$ is the count of verified historical runs for task cluster $C$ and topology $T$.
  - $s_{\text{quality}}$ is the sample standard deviation of historical quality scores ($s \in [0.0, 0.5]$). High variance ($s \to 0.5$) dampens confidence to a floor of $0.1$.
  - When $N_{C,T} < 5$ ($N_{\text{min}} = 5$), confidence is set to $0.0$, triggering a `COLD_START_FALLBACK` to Group B rule defaults.
- **Handling Contradictory & Stale Records:**
  - If a topology exhibits high historical variance ($s > 0.25$), the controller does not aggressively exploit historical rankings; it reverts to the rule-based recommendation or triggers a bounded verification topology.
  - An exponential time-decay factor $e^{-\lambda \Delta t}$ down-weights historical records generated under older prompt versions or runtime configurations.

### 6.3 Separation of Objective Telemetry from Subjective Quality
Historical records in PostgreSQL maintain strict physical separation between:
1. **Deterministic System Telemetry:** `wall_clock_ms`, `prompt_tokens`, `completion_tokens`, `agent_invocation_count`, `constraint_pass_boolean`.
2. **Subjective Evaluator Scores:** `rubric_correctness`, `rubric_completeness`, `rubric_coherence`, `human_eval_rating`.
This ensures that objective latency and success filters operate independently of subjective scoring distributions.

---

## 7. Evaluation Metrics Specification

Every metric is defined with its operational formula, measurement unit, data source, and limitations.

### M-01: Wall-Clock Latency ($T_{\text{wall}}$)
- **Definition:** Total elapsed time from task submission to final response delivery.
- **Formula:** $T_{\text{wall}} = t_{\text{end}} - t_{\text{start}}$
- **Unit:** Milliseconds (ms)
- **Data Source:** Backend high-resolution timer (`time.perf_counter_ns()`).
- **Optimization Direction:** Lower is better ($\downarrow$).
- **Limitations:** Influenced by CPU scheduling and background OS tasks. Mitigated by reporting median/IQR and task-level means over 3 randomized repetitions.

### M-02: Token Consumption Proxy ($C_{\text{token}}$)
- **Definition:** Cumulative count of prompt and completion tokens processed by Ollama across all agents in the run.
- **Formula:** $C_{\text{token}} = \sum_{i=1}^{K} (\text{prompt\_tokens}_i + \text{completion\_tokens}_i)$ where $K$ is the number of agent invocations.
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

### M-05: Agent Invocation Ratio ($\eta_{\text{invocations}}$)
- **Definition:** Total number of agent invocations executed in a run divided by the nominal 4-agent baseline pipeline size.
- **Formula:** $\eta_{\text{invocations}} = \frac{K_{\text{invocations}}}{4.0}$
- **Operational Clarity:**
  - $K_{\text{invocations}}$ measures the **total number of node execution calls**, including review loops and retries.
  - Distinct from **Team Size** ($|T_{\text{distinct}}| \in \{1, 2, 3, 4\}$), which represents the count of unique agent roles selected.
  - **Values:** $\eta = 0.50$ (2 calls, e.g., Analyst $\to$ Writer); $\eta = 1.00$ (4 calls, nominal 4-agent baseline); $\eta = 1.25 - 1.50$ (5 or 6 calls when a revision cycle occurs).
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

### Execution Protocol Summary
1. **Model Warm-Up:** 2 dummy prompts executed and discarded prior to benchmark logging.
2. **Experimental Run Block:** 60 tasks $\times$ 3 repetitions $\times$ 3 groups = 540 total runs, executed under randomized block scheduling.
3. **Partitioning:** 40 calibration tasks (populating historical database) and 20 held-out evaluation tasks (evaluating Group C generalization under frozen history).
