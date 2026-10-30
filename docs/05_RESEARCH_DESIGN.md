# AETHER --- Research Design and Methodology

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-RES-001  
**Version:** 1.0 (Phase 1 Baseline)  
**Status:** Approved for Phase 1 Research Specification

---

## 1. Research Problem and Contribution

### 1.1 Problem Statement
Modern multi-agent architectures typically rely on static pipeline patterns (such as sequential chains of specialist agents) regardless of the specific task difficulty, domain nuance, or resource limits. This static design incurs significant penalties:
1. **Resource Inefficiency:** Simple tasks that require only basic analysis or drafting are forced through an exhaustive chain of agents, consuming excessive tokens, runtime memory, and latency.
2. **Fragility & Error Propagation:** In a static pipeline, errors early in the chain compound downstream. Inflexible review mechanisms either fail to address flaws or loop unconditionally.
3. **Absence of Memory-Driven Optimization:** Multi-agent systems rarely learn from their own execution history. If a two-agent team achieved 95% quality on a specific category of technical explanation with 40% lower latency, static systems remain incapable of exploiting this historical evidence.

### 1.2 Research Objectives
1. Design and formalize a dynamic agent-team selection framework that selects execution topologies based on task features and operational constraints.
2. Formulate an empirical performance history model that stores, indexes, and retrieves past multi-agent execution evidence.
3. Establish an explainable decision mechanism that justifies why a specific team topology was selected over alternatives.
4. Execute controlled comparative experiments evaluating task quality, execution latency, resource consumption, and reliability across static, rule-based, and history-aware configurations.

### 1.3 Core Scientific Contribution
The primary contribution of AETHER is **not** merely chaining multiple LLM prompts together or building a local chatbot UI. The contribution is the **performance-aware, explainable, and history-informed agent-team selection and evaluation framework**, demonstrating how feedback loops ($\text{Evaluate} \to \text{Remember} \to \text{Adapt} \to \text{Collaborate} \to \text{Evaluate}$) can systematically optimize the Pareto frontier between multi-agent response quality and computational cost on resource-constrained local hardware.

---

## 2. Research Questions and Testable Hypotheses

### 2.1 Research Questions (RQs)
- **RQ1 (Adaptive Collaboration):** Does dynamically selecting agent teams based on task characteristics improve overall performance compared with a fixed multi-agent pipeline?
- **RQ2 (Historical Evidence):** Does incorporating historical agent performance improve team-selection decisions compared with rule-based adaptation without historical evidence?
- **RQ3 (Resource Efficiency):** Can adaptive collaboration reduce execution latency and token consumption without significantly compromising output quality or task success?
- **RQ4 (Explainability):** Can the framework provide understandable, evidence-supported explanations for agent selection and collaboration decisions?
- **RQ5 (Feedback-Driven Improvement):** Does incorporating previous execution outcomes improve subsequent team-selection decisions under comparable task conditions?

### 2.2 Formal Hypotheses
Each hypothesis is structured with rigorous independent, dependent, and control variables, measurement protocols, falsification criteria, and confounding factors.

#### Hypothesis 1 (H1 — Adaptive Performance)
- **Statement:** Dynamic workflow selection based on task complexity and domain produces equal or higher task success rates ($S \ge S_{\text{baseline}}$) with significantly lower average wall-clock latency ($L < L_{\text{baseline}}$) across a heterogeneous benchmark task set compared to a fixed four-agent pipeline.
- **Independent Variable:** Orchestration Strategy (Fixed Baseline vs. Rule-Based Adaptive).
- **Dependent Variables:** Task Success Rate (%), Mean Wall-Clock Latency (seconds), Overall Output Quality Score (0.0–1.0).
- **Control Variables:** Underlying local LLM model and quantization, system prompt instructions, maximum token generation limits, host hardware state, task dataset inputs.
- **Measurement Procedure:** Execute 50 standardized benchmark tasks across both Group A and Group B. Record automated success criteria and double-blind rubric quality scores.
- **Evidence to Support:** Statistically significant ($p < 0.05$, paired t-test or Wilcoxon signed-rank) reduction in latency with non-inferior quality scores ($\Delta \text{Quality} > -0.05$).
- **Evidence to Reject:** Latency is equal or worse, or quality degrades significantly across tasks.
- **Confounders:** Host CPU thermal throttling, varying system background processes (mitigated by automated hardware temperature/load logging).

#### Hypothesis 2 (H2 — Historical Evidence Value)
- **Statement:** Incorporating validated historical execution evidence (Group C) achieves higher Pareto efficiency (quality per unit latency) on recurring task categories than rule-based adaptation without history (Group B).
- **Independent Variable:** History-Aware Decision Controller (Enabled with historical memory vs. Disabled rule-based).
- **Dependent Variables:** Utility Score $U = \text{Quality} / \log(\text{Latency})$, Task Success Rate (%).
- **Control Variables:** Task categories, initial model weights, prompt templates, hardware environment.
- **Measurement Procedure:** Run sequential batches of tasks where early runs populate PostgreSQL historical tables; observe team selection adaptations on subsequent batches of similar tasks.
- **Evidence to Support:** Group C selects more efficient topologies that achieve equivalent quality with fewer redundant agent calls than Group B after $\ge 10$ warm-up runs.
- **Evidence to Reject:** Group C selection converges to identical topologies as Group B or exhibits performance instability due to noisy historical records.
- **Confounders:** Small sample bias, cold-start volatility (mitigated by confidence thresholding $N \ge 3$ before historical override).

#### Hypothesis 3 (H3 — Resource Optimization)
- **Statement:** For tasks classified as Low or Moderate complexity (complexity $\le 2$), adaptive pruning of unnecessary agent roles (e.g., omitting Researcher or Reviewer) reduces wall-clock latency by at least 30% and total generated tokens by at least 35% without statistically significant degradation in task quality.
- **Independent Variable:** Team Configuration (Full 4-Agent vs. Pruned 2-Agent/3-Agent).
- **Dependent Variables:** Generated token count, wall-clock latency (ms), quality score.
- **Control Variables:** Prompt content, model temperature ($T = 0.2$), task complexity rating.
- **Measurement Procedure:** Sub-group analysis of Low/Moderate complexity tasks comparing Group A vs. Group B.
- **Evidence to Support:** Measured token reductions $\ge 35\%$ and latency reductions $\ge 30\%$ with quality difference $p > 0.05$.
- **Evidence to Reject:** Quality score drops by more than 10% when agents are pruned.
- **Confounders:** Task categorization accuracy.

#### Hypothesis 4 (H4 — Explainability & Traceability)
- **Statement:** Structured decision records comprising capability gap vectors, triggered rule IDs, and retrieved historical case citations produce verifiable, human-interpretable justifications for 100% of team selections.
- **Independent Variable:** Decision Logging Mechanism (Structured Explanation Record).
- **Dependent Variables:** Explanation Completeness (boolean), Rule Traceability (%), Human Understandability Score (Likert scale 1–5).
- **Control Variables:** Evaluation rubric, task set.
- **Measurement Procedure:** Audit of selection logs across all adaptive runs; human review of explanations for 30 randomly sampled selection decisions.
- **Evidence to Support:** 100% of runs have complete structured explanation schemas; mean human audit score $\ge 4.0/5.0$.
- **Evidence to Reject:** Explanations contain missing rule mappings, hallucinated history references, or fall below 3.5/5.0 in human review.
- **Confounders:** Subjectivity in human interpretability evaluation.

#### Hypothesis 5 (H5 — Feedback Convergence)
- **Statement:** Repeated execution with historical feedback updates exhibits convergence toward stable, high-performing team topologies for consistent task clusters over time.
- **Independent Variable:** Historical Run Count ($N = 0, 5, 10, 20$).
- **Dependent Variables:** Team Topology Variance, Mean Task Success Rate across iterations.
- **Control Variables:** Task cluster distribution, base model parameters.
- **Measurement Procedure:** Execute 4 successive iterations of a 15-task cluster; measure selection stability and success progression.
- **Evidence to Support:** Topology selection stabilizes (variance approaches zero) while success rate monotonically improves or plateaus at peak.
- **Evidence to Reject:** Continual oscillation between team topologies without performance gain.
- **Confounders:** Feedback score noise, reward hacking in evaluation metrics.

---

## 3. Experimental Design and Conditions

The research compares three rigorously controlled experimental conditions:

```
+-----------------------------------------------------------------------------------+
|                              EXPERIMENTAL CONDITIONS                              |
+-----------------------------------------------------------------------------------+
| Group A: Fixed Baseline Pipeline                                                  |
|   Topology: Researcher -> Analyst -> Writer -> Reviewer (Always all 4)             |
|   Selection Logic: Static / Invariant                                             |
|   Memory Usage: Zero history utilized                                             |
+-----------------------------------------------------------------------------------+
| Group B: Rule-Based Adaptive Collaboration                                        |
|   Topology: Dynamic (e.g., Analyst->Writer, Researcher->Analyst->Writer, etc.)   |
|   Selection Logic: Deterministic rules on Task Features & Constraints             |
|   Memory Usage: Zero history utilized                                             |
+-----------------------------------------------------------------------------------+
| Group C: History-Aware Adaptive Collaboration                                     |
|   Topology: Dynamic (Selected via empirical utility optimization)                 |
|   Selection Logic: Task Features + Similarity-Weighted Past Performance Records   |
|   Memory Usage: PostgreSQL Historical Execution & Evaluation Records              |
+-----------------------------------------------------------------------------------+
```

### 3.1 Experimental Controls
To prevent confounding factors, the following variables are strictly controlled across all groups:
1. **Host Inference Engine:** Local Ollama runtime running exclusively on the specified laptop hardware (Intel Core i5-13550H, 16 GB RAM, no GPU).
2. **Model Weights & Quantization:** Identical model weights (e.g., Qwen3 14B Q4_K_M or DeepSeek-R1 14B Q4_K_M) across all groups in a given trial. Model comparisons are conducted as separate orthogonal experiments.
3. **Hyperparameters:** Temperature fixed ($T = 0.2$ for deterministic reasoning; $T = 0.0$ for evaluation checks), seed fixed, top_p fixed, context window capped at 4096 tokens.
4. **Execution Modality:** Strictly sequential agent execution (single-agent resident in RAM at any time).
5. **Benchmark Dataset:** Identical benchmark dataset of 60 standardized tasks across 4 diverse domains (technical reasoning, synthesis, data extraction, and creative drafting) and 3 complexity tiers (Low, Medium, High).
6. **Zero External API Bias:** All local execution; zero fluctuating cloud latencies or dynamic rate limits.

---

## 4. Evaluation Metrics Specification

Every metric is defined with its operational formula, measurement unit, data source, and potential limitations.

### M-01: Wall-Clock Latency ($T_{\text{wall}}$)
- **Definition:** Total elapsed time from task submission to final response delivery.
- **Formula:** $T_{\text{wall}} = t_{\text{end}} - t_{\text{start}}$
- **Unit:** Milliseconds (ms)
- **Data Source:** Backend high-resolution timer (`time.perf_counter_ns()`).
- **Optimization Direction:** Lower is better ($\downarrow$).
- **Limitations:** Subject to operating system scheduling and CPU thermal management. Mitigated by reporting median and IQR over 3 repetitions.

### M-02: Token Consumption Proxy ($C_{\text{token}}$)
- **Definition:** Cumulative count of prompt and completion tokens processed by Ollama across all agents in the run.
- **Formula:** $C_{\text{token}} = \sum_{i=1}^{K} (\text{prompt\_tokens}_i + \text{completion\_tokens}_i)$ where $K$ is the number of agent calls.
- **Unit:** Integer token count
- **Data Source:** Ollama API response metadata (`prompt_eval_count` + `eval_count`).
- **Optimization Direction:** Lower is better ($\downarrow$).
- **Limitations:** Does not directly represent currency cost (since local inference is ₹0), but serves as the primary proxy for computational energy and memory-bus pressure.

### M-03: Task Success Rate ($S_{\text{task}}$)
- **Definition:** Binary indicator whether the output satisfies all explicit deterministic constraints (e.g., correct schema format, required sections present, length bounds respected, factual consistency checks passed).
- **Formula:** $S_{\text{task}} = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(\text{run}_j \text{ passes all constraints})$
- **Unit:** Percentage ($0.0\% - 100.0\%$)
- **Data Source:** Automated evaluation engine deterministic validators.
- **Optimization Direction:** Higher is better ($\uparrow$).
- **Limitations:** Captures syntactic and structural compliance; does not capture nuanced stylistic quality.

### M-04: Output Quality Score ($Q_{\text{out}}$)
- **Definition:** Multi-dimensional score assessing response correctness, completeness, logical coherence, and relevance.
- **Formula:** $Q_{\text{out}} = 0.35 \cdot Q_{\text{correctness}} + 0.25 \cdot Q_{\text{completeness}} + 0.20 \cdot Q_{\text{coherence}} + 0.20 \cdot Q_{\text{relevance}}$
- **Unit:** Normalized scalar ($0.00 - 1.00$)
- **Data Source:** Dual evaluation: automated rubric validator combined with structured human evaluation on sample subsets.
- **Optimization Direction:** Higher is better ($\uparrow$).
- **Limitations:** Unvalidated LLM self-evaluation is prohibited as ground truth to prevent self-enhancement bias.

### M-05: Agent Utilization Index ($\eta_{\text{agent}}$)
- **Definition:** Total number of agent invocations executed divided by the maximum possible pipeline size (4).
- **Formula:** $\eta_{\text{agent}} = \frac{K_{\text{invocations}}}{4}$
- **Unit:** Ratio ($0.25 - 1.50$ accounting for bounded review iterations).
- **Data Source:** LangGraph run state execution trace.
- **Optimization Direction:** Lower is better for simple tasks; matched to complexity for difficult tasks.

### M-06: Selection Pareto Efficiency ($E_{\text{pareto}}$)
- **Definition:** The ratio of output quality achieved per unit of normalized latency.
- **Formula:** $E_{\text{pareto}} = \frac{Q_{\text{out}}}{\ln(T_{\text{wall\_sec}} + 1)}$
- **Unit:** Scalar score.
- **Optimization Direction:** Higher is better ($\uparrow$).

### M-07: Decision Traceability & Explainability ($X_{\text{trace}}$)
- **Definition:** Proportion of selection decisions with complete, verifiable justification trails (rules triggered, capability delta, cited historical case IDs).
- **Formula:** $X_{\text{trace}} = \frac{N_{\text{valid\_explanations}}}{N_{\text{total\_runs}}}$
- **Unit:** Percentage ($100\%$ target).
- **Data Source:** PostgreSQL `TeamSelection` table audit queries.

### M-08: Reliability & Failure Rate ($R_{\text{fail}}$)
- **Definition:** Percentage of executions encountering unhandled runtime exceptions, model timeout terminations, or malformed unparseable outputs.
- **Formula:** $R_{\text{fail}} = \frac{N_{\text{failed\_runs}}}{N_{\text{total\_attempts}}} \times 100$
- **Unit:** Percentage.
- **Optimization Direction:** Zero is target ($0.0\%$).

---

## 5. Benchmark Task Dataset Design

The evaluation uses a balanced 60-task benchmark suite across 4 domains and 3 complexity levels:

| Domain | Low Complexity (1–2) | Medium Complexity (3) | High Complexity (4–5) | Total Tasks |
| :--- | :--- | :--- | :--- | :--- |
| **Technical Reasoning** | Syntax debugging, unit test writing | Algorithmic explanation, edge-case analysis | Distributed systems failure triage, formal verification | 15 |
| **Synthesis & Summarization** | Executive summary of 1-page memo | Comparative analysis of 2 proposals | Multi-source literature synthesis with conflicting data | 15 |
| **Structured Extraction** | JSON parsing from semi-structured log | Schema normalization from tabular text | Disambiguation of complex entity networks | 15 |
| **Analysis & Critique** | Fact-checking a single claim | Multi-faceted trade-off analysis | Comprehensive policy review with counter-arguments | 15 |
| **Total** | 20 tasks | 20 tasks | 20 tasks | **60 tasks** |

### Execution Protocol
1. **Cold-Start Benchmark:** Run 20 tasks across Group A, Group B, and Group C (Group C initially acts identically to Group B due to zero historical records, verifying cold-start fallback).
2. **History Population:** Execute 40 training runs to populate PostgreSQL performance history with verified evaluation metrics.
3. **Warm Evaluation Benchmark:** Run 40 test tasks across Group A, Group B, and Group C, measuring adaptation convergence, selection drift, latency savings, and quality maintenance.
