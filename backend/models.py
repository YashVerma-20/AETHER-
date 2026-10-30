"""AETHER SQLAlchemy Relational Models.

Implements the 8 core entities supporting the research design:
1. Task (Experimental units, N=60)
2. ExperimentalCondition (Groups A, B, C)
3. ExperimentalRun (Replicate runs, R=3)
4. AgentExecutionRecord (Node-level telemetry)
5. PerformanceMeasurement (Deterministic telemetry & rubric scores)
6. TeamSelectionDecision (Controller teaming decisions)
7. DecisionExplanation (H4 explainability & traceability)
8. HistoricalPerformanceRecord (Group C experience store with protocol provenance)
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.database import Base


def utcnow() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class Task(Base):
    """Task entity representing an independent experimental unit (N=60)."""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_key = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    category = Column(String(64), nullable=False, index=True)  # e.g., RESEARCH, ANALYSIS, WRITING, CODE
    complexity_level = Column(Integer, nullable=False, index=True)  # 1=Low, 2=Moderate, 3=High
    protocol_split = Column(String(32), nullable=False, default="CALIBRATION")  # CALIBRATION vs HELD_OUT
    deterministic_constraints = Column(JSONB, nullable=False, default=dict)  # Schema rules, forbidden words
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    runs = relationship("ExperimentalRun", back_populates="task", cascade="all, delete-orphan")
    decisions = relationship("TeamSelectionDecision", back_populates="task")


class ExperimentalCondition(Base):
    """Experimental condition entity (Group A, Group B, Group C)."""

    __tablename__ = "experimental_conditions"

    id = Column(String(32), primary_key=True)  # e.g., GROUP_A, GROUP_B, GROUP_C
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    historical_memory_enabled = Column(Boolean, nullable=False, default=False)
    selection_policy = Column(String(64), nullable=False)  # FIXED_PIPELINE, DETERMINISTIC_RULES, UTILITY_OPTIMIZATION
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    runs = relationship("ExperimentalRun", back_populates="condition")
    decisions = relationship("TeamSelectionDecision", back_populates="condition")


class ExperimentalRun(Base):
    """Replicate technical run entity (R=3 per task per condition, 540 total runs)."""

    __tablename__ = "experimental_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    condition_id = Column(String(32), ForeignKey("experimental_conditions.id"), nullable=False, index=True)
    run_number = Column(Integer, nullable=False)  # 1, 2, or 3
    status = Column(String(32), nullable=False, default="PENDING", index=True)  # PENDING, RUNNING, COMPLETED, FAILED
    
    # Model runtime & configuration provenance
    model_id = Column(String(64), nullable=False, default="qwen2.5:7b")
    model_quantization = Column(String(32), nullable=False, default="Q4_K_M")
    context_window = Column(Integer, nullable=False, default=4096)
    temperature = Column(Float, nullable=False, default=0.2)
    random_seed = Column(Integer, nullable=True)
    
    # Output and timing
    final_output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    task = relationship("Task", back_populates="runs")
    condition = relationship("ExperimentalCondition", back_populates="runs")
    agent_executions = relationship("AgentExecutionRecord", back_populates="run", cascade="all, delete-orphan")
    performance_measurement = relationship("PerformanceMeasurement", back_populates="run", uselist=False, cascade="all, delete-orphan")
    decision = relationship("TeamSelectionDecision", back_populates="run", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_runs_task_condition_runnum", "task_id", "condition_id", "run_number", unique=True),
    )


class AgentExecutionRecord(Base):
    """Node-level agent execution trace within a run."""

    __tablename__ = "agent_execution_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("experimental_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name = Column(String(64), nullable=False)  # Researcher, Analyst, Writer, Reviewer
    execution_order = Column(Integer, nullable=False)  # Sequence index in execution path
    
    # Telemetry (allowing NULL if unavailable or skipped, never invented)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    
    status = Column(String(32), nullable=False, default="COMPLETED")  # COMPLETED, FAILED, SKIPPED
    input_payload = Column(JSONB, nullable=True)
    output_payload = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    run = relationship("ExperimentalRun", back_populates="agent_executions")


class PerformanceMeasurement(Base):
    """Deterministic telemetry and rubric evaluation record."""

    __tablename__ = "performance_measurements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("experimental_runs.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Deterministic telemetry (M-01, M-02)
    wall_clock_ms = Column(Integer, nullable=True)  # High-resolution wall-clock timer
    total_prompt_tokens = Column(Integer, nullable=True)  # Nullable if unavailable
    total_completion_tokens = Column(Integer, nullable=True)  # Nullable if unavailable
    total_tokens = Column(Integer, nullable=True)  # Nullable if unavailable
    
    # Deterministic constraint validation (M-03)
    constraint_success = Column(Boolean, nullable=True)
    constraint_details = Column(JSONB, nullable=True)  # Per-rule pass/fail details
    
    # Subjective rubric evaluation (M-04) — separated from objective telemetry
    rubric_quality_score = Column(Float, nullable=True)
    rubric_correctness = Column(Float, nullable=True)
    rubric_completeness = Column(Float, nullable=True)
    rubric_coherence = Column(Float, nullable=True)
    evaluated_by = Column(String(64), nullable=True)  # AUTOMATED_DETERMINISTIC, HUMAN_AUDITOR
    
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    run = relationship("ExperimentalRun", back_populates="performance_measurement")


class TeamSelectionDecision(Base):
    """Adaptive controller teaming decision record."""

    __tablename__ = "team_selection_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("experimental_runs.id", ondelete="CASCADE"), unique=True, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    condition_id = Column(String(32), ForeignKey("experimental_conditions.id"), nullable=False, index=True)
    
    selected_topology = Column(JSONB, nullable=False)  # e.g., ["Analyst", "Writer"]
    candidate_topologies = Column(JSONB, nullable=True)
    capability_gap_vector = Column(JSONB, nullable=True)
    triggered_rule_ids = Column(JSONB, nullable=True)
    historical_case_ids = Column(JSONB, nullable=True)
    
    confidence_score = Column(Float, nullable=True)  # Heuristic discounting factor [0.0, 1.0]
    latency_estimate_ms = Column(Integer, nullable=True)  # Unverified theoretical estimate
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    run = relationship("ExperimentalRun", back_populates="decision")
    task = relationship("Task", back_populates="decisions")
    condition = relationship("ExperimentalCondition", back_populates="decisions")
    explanation = relationship("DecisionExplanation", back_populates="decision", uselist=False, cascade="all, delete-orphan")


class DecisionExplanation(Base):
    """Explainability record supporting Hypothesis 4 and auditability."""

    __tablename__ = "decision_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id = Column(UUID(as_uuid=True), ForeignKey("team_selection_decisions.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    justification_text = Column(Text, nullable=False)
    rule_rationale = Column(Text, nullable=True)
    historical_evidence_summary = Column(Text, nullable=True)
    tradeoff_analysis = Column(Text, nullable=True)
    human_rated_understandability = Column(Float, nullable=True)  # Evaluated in Phase 5 human audit (Likert 1-5)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    decision = relationship("TeamSelectionDecision", back_populates="explanation")


class HistoricalPerformanceRecord(Base):
    """Empirical experience store for Group C with strict protocol provenance."""

    __tablename__ = "historical_performance_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_category = Column(String(64), nullable=False, index=True)
    complexity_level = Column(Integer, nullable=False, index=True)
    topology_signature = Column(String(128), nullable=False, index=True)  # e.g., "Analyst->Writer"
    
    # Provenance separation to prevent data leakage (Protocol 1 vs Protocol 2)
    protocol_origin = Column(String(32), nullable=False, default="CALIBRATION")  # CALIBRATION, FROZEN, ONLINE_BATCH
    
    sample_count = Column(Integer, nullable=False, default=0)
    mean_wall_clock_ms = Column(Float, nullable=True)
    std_wall_clock_ms = Column(Float, nullable=True)
    mean_quality_score = Column(Float, nullable=True)
    std_quality_score = Column(Float, nullable=True)
    mean_tokens = Column(Float, nullable=True)
    success_rate = Column(Float, nullable=True)
    
    last_updated_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    __table_args__ = (
        Index("ix_hist_cat_comp_topo_proto", "task_category", "complexity_level", "topology_signature", "protocol_origin", unique=True),
    )
