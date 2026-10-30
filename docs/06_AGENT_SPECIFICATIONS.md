# AETHER --- Agent Specifications

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-AGT-001  
**Version:** 1.0 (Phase 1 Baseline)  
**Status:** Approved for Phase 1 Research Specification

---

## 1. Multi-Agent System Overview

AETHER employs four specialized initial agent roles: **Researcher**, **Analyst**, **Writer**, and **Reviewer**. 

Unlike conventional pipelines where every agent is executed in lockstep, AETHER dynamically configures graphs containing only the agents necessary for the specific task and operational constraints:
- **Minimal Drafting Topology:** Analyst $\to$ Writer (omits Researcher when context is complete; omits Reviewer for low-risk tasks).
- **Research-Heavy Topology:** Researcher $\to$ Analyst $\to$ Writer (for tasks requiring dense synthesis of provided context).
- **Verification-Sensitive Topology:** Analyst $\to$ Writer $\to$ Reviewer (for tasks demanding strict logical correctness or schema adherence).
- **Full Static Pipeline (Baseline):** Researcher $\to$ Analyst $\to$ Writer $\to$ Reviewer (with bounded 1-iteration review loop).

All agent interactions occur sequentially through shared LangGraph state dictionaries. Concurrent multi-agent execution is prohibited to preserve the 16 GB host memory envelope.

---

## 2. Agent Specifications

### 2.1 Researcher Agent

- **Role Identity:** Information Gatherer and Evidence Organizer.
- **Purpose:** Extracts, categorizes, and organizes relevant factual information from the user-provided prompt or local context files. Identifies facts, underlying assumptions, and missing information.
- **Strict Boundary:** The Researcher operates **strictly on provided local context**. It does **not** perform unverified internet browsing, web scraping, or access external paid APIs.
- **Inputs:**
  - `task_prompt`: User-provided task text and raw context.
  - `domain`: Classified task domain.
  - `required_capabilities`: Extracted capability tags.
- **Outputs (LangGraph State Update):**
  - `research_notes`: Structured list of key factual assertions.
  - `assumptions_identified`: Explicit list of assumptions detected in context.
  - `information_gaps`: Missing data or ambiguities requiring analytical attention.
- **Required Capabilities:**
  - `context_extraction`
  - `evidence_organization`
  - `fact_assumption_disambiguation`
- **Selection Conditions:**
  - Selected when task context exceeds 500 words, contains dense unstructured documentation, or when `information_gathering` capability is flagged.
  - **Pruned (Omitted)** when task prompt is concise ($\le 150$ words), fully structured, or self-contained.
- **Failure Conditions:**
  - Hallucinating external facts not present in provided context.
  - Exceeding allocated context window tokens.
- **Evaluation Criteria:**
  - Precision of extracted factual claims against source context.
  - Recall of key task constraints.

---

### 2.2 Analyst Agent

- **Role Identity:** Reasoner, Trade-Off Evaluator, and Synthesizer.
- **Purpose:** Examines research findings or direct task prompts, conducts logical deductions, evaluates comparative trade-offs, and structures the logical outline for the final response.
- **Inputs:**
  - `task_prompt`: User task description.
  - `research_notes`: Extracted context (if Researcher was executed).
  - `assumptions_identified`: Contextual assumptions.
- **Outputs (LangGraph State Update):**
  - `analysis_outline`: Step-by-step reasoning chain and logical structure.
  - `trade_off_matrix`: Comparative analysis of approaches or evidence.
  - `key_conclusions`: Core findings to be communicated in final output.
- **Required Capabilities:**
  - `logical_deduction`
  - `comparative_analysis`
  - `counter_argument_formulation`
- **Selection Conditions:**
  - Selected when task complexity $\ge 2$, involves multi-criteria comparison, policy analysis, debugging, or complex reasoning.
  - **Pruned (Omitted)** only in purely formatting or direct syntactic extraction tasks where direct writing suffices.
- **Failure Conditions:**
  - Logical inconsistencies or non-sequiturs in analytical outline.
  - Failing to address negative constraints or trade-offs.
- **Evaluation Criteria:**
  - Soundness of deductions.
  - Identification of edge cases and counter-perspectives.

---

### 2.3 Writer Agent

- **Role Identity:** Synthesizer and Final Response Generator.
- **Purpose:** Translates analytical conclusions, evidence, and task guidelines into a fluent, cohesive, professional response formatted according to the user's requested schema.
- **Inputs:**
  - `task_prompt`: Original user prompt.
  - `analysis_outline`: Logical structure from Analyst (if present).
  - `research_notes`: Evidence from Researcher (if present).
  - `review_feedback`: Critique notes from Reviewer (if in a revision cycle).
- **Outputs (LangGraph State Update):**
  - `draft_response`: The complete synthesized text or structured JSON artifact.
  - `generation_metadata`: Token count, formatting style used.
- **Required Capabilities:**
  - `structured_synthesis`
  - `stylistic_adaptation`
  - `schema_compliance`
- **Selection Conditions:**
  - **Always Required:** The Writer is mandatory across all topologies as the primary generative node that produces the deliverables.
- **Failure Conditions:**
  - Failing to satisfy requested output format (e.g., producing raw text instead of requested Markdown/JSON).
  - Introducing contradictions to the Analyst's conclusions.
- **Evaluation Criteria:**
  - Fluency, readability, adherence to requested formatting, and completeness against user requirements.

---

### 2.4 Reviewer Agent

- **Role Identity:** Quality Auditor, Fact Checker, and Revision Gatekeeper.
- **Purpose:** Rigorously verifies the Writer's draft against the original prompt, constraints, and analytical outline. Determines whether the response is approved or requires revision.
- **Inputs:**
  - `task_prompt`: Original requirements and constraints.
  - `draft_response`: Output produced by Writer.
  - `analysis_outline`: Underlying logical reasoning.
  - `iteration_count`: Current revision index (to enforce bounded loops).
- **Outputs (LangGraph State Update):**
  - `review_passed`: Boolean flag (`True` = deliver response; `False` = route back to Writer).
  - `critique_items`: Bulleted actionable flaws, omissions, or formatting errors.
  - `severity_level`: Minor (acceptable) vs. Major (requires revision).
- **Required Capabilities:**
  - `fact_checking`
  - `constraint_verification`
  - `actionable_critique`
- **Selection Conditions:**
  - Selected when task complexity $\ge 3$, when quality priority is set to "High Precision", or for safety/logic-critical domains.
  - **Pruned (Omitted)** for low-complexity drafting (complexity 1–2), speed-prioritized queries, or exploratory ideation tasks.
- **Loop Bounding:**
  - Maximum of **1 revision cycle** allowed (Writer $\to$ Reviewer $\to$ Writer $\to$ Final Delivery). Unbounded review loops are strictly prohibited to protect runtime latency.
- **Failure Conditions:**
  - Nitpicking stylistic trivialities resulting in unnecessary revision loops.
  - Approving outputs that violate explicit negative constraints.
- **Evaluation Criteria:**
  - Critique accuracy and precision of defect detection.

---

## 3. Agent Communication & State Schema

All agents communicate via a unified, typed LangGraph state dictionary:

```python
# Conceptual LangGraph State Schema (Specification Only - Not Implementation)
class AetherWorkflowState:
    task_id: str
    prompt: str
    complexity: int
    quality_priority: str  # "speed" | "balanced" | "precision"
    
    # Node outputs
    research_notes: list[str]
    analysis_outline: dict
    draft_response: str
    critique_items: list[str]
    review_passed: bool
    revision_count: int
    
    # Telemetry
    node_latency_ms: dict[str, int]
    node_token_counts: dict[str, int]
```

---

## 4. Pruning and Efficiency Rules

To satisfy Research Question 3 (Resource Efficiency) without compromising quality:
1. **Rule PRUNE-01 (Direct Drafting):** If `complexity == 1` and `length < 100 words`, select `{Analyst, Writer}`. Bypasses Researcher and Reviewer, saving ~50% wall-clock latency.
2. **Rule PRUNE-02 (Pre-Packaged Context):** If `context_complete == True` (user supplies bulleted factual reference data), bypass `Researcher`.
3. **Rule PRUNE-03 (Speed Constraint):** If `latency_budget < 30_000 ms`, omit `Reviewer` and set `revision_count = 0`.
