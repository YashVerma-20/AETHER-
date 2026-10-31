"""Unit and Integration Tests for AETHER Backend and Database Foundation.

Verifies:
1. FastAPI application startup and lifespan.
2. GET /health endpoint response.
3. Live PostgreSQL database connectivity and GET /health/database response.
4. Database session creation and cleanup.
5. Database model insertion, relationships, and foreign key cascades.
6. Safe error handling when database is disconnected.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.config import get_settings
from backend.database import get_db, Base, check_database_connection
from backend.models import (
    Task,
    ExperimentalCondition,
    ExperimentalRun,
    AgentExecutionRecord,
    PerformanceMeasurement,
    TeamSelectionDecision,
    DecisionExplanation,
    HistoricalPerformanceRecord,
)

settings = get_settings()
client = TestClient(app)


def test_fastapi_app_startup():
    """Verify FastAPI application starts and serves OpenAPI metadata."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "AETHER Backend Foundation"
    assert data["info"]["version"] == "0.3.0"


def test_health_endpoint():
    """Verify GET /health returns HTTP 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["environment"] == settings.AETHER_ENV
    assert payload["version"] == "0.3.0"


def test_database_health_endpoint():
    """Verify GET /health/database connects to live PostgreSQL on port 5433."""
    response = client.get("/health/database")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["connected"] is True
    assert payload["database"] == "aether_db"
    assert payload["port"] == 5433
    assert "PostgreSQL 17" in payload["version"]
    assert payload["error"] is None


def test_database_session_creation_and_cleanup():
    """Verify get_db dependency yields a clean, operable session and closes safely."""
    gen = get_db()
    db = next(gen)
    try:
        result = db.execute(text("SELECT 1 AS alive")).mappings().first()
        assert result["alive"] == 1
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


def test_models_and_relationship_validity():
    """Verify research entity insertion, foreign key constraints, and cascade cleanup."""
    gen = get_db()
    db = next(gen)
    try:
        # 1. Condition
        cond_id = f"TEST_GRP_{uuid.uuid4().hex[:6]}"
        condition = ExperimentalCondition(
            id=cond_id,
            name="Test Condition",
            description="Integration test condition",
            historical_memory_enabled=False,
            selection_policy="FIXED_PIPELINE",
        )
        db.add(condition)

        # 2. Task (Experimental Unit)
        task_key = f"TEST-TASK-{uuid.uuid4().hex[:6]}"
        task = Task(
            task_key=task_key,
            title="Test Task Unit",
            prompt="Analyze architectural trade-offs.",
            category="ANALYSIS",
            complexity_level=2,
            protocol_split="CALIBRATION",
            deterministic_constraints={"schema": "json"},
        )
        db.add(task)
        db.commit()

        # 3. Replicate Run
        run = ExperimentalRun(
            task_id=task.id,
            condition_id=condition.id,
            run_number=1,
            status="COMPLETED",
            model_id="qwen2.5:7b",
            model_quantization="Q4_K_M",
            temperature=0.2,
        )
        db.add(run)
        db.commit()

        # 4. Agent Execution Record (Node telemetry with nullable tokens)
        agent_exec = AgentExecutionRecord(
            run_id=run.id,
            agent_name="Analyst",
            execution_order=1,
            prompt_tokens=150,
            completion_tokens=220,
            latency_ms=18500,
            status="COMPLETED",
        )
        db.add(agent_exec)

        # 5. Performance Measurement (Deterministic telemetry & rubric separation)
        measurement = PerformanceMeasurement(
            run_id=run.id,
            wall_clock_ms=18500,
            total_prompt_tokens=150,
            total_completion_tokens=220,
            total_tokens=370,
            constraint_success=True,
            constraint_details={"schema": True},
            rubric_quality_score=0.88,
            rubric_correctness=0.90,
            rubric_completeness=0.85,
            rubric_coherence=0.89,
            evaluated_by="HUMAN_AUDITOR",
        )
        db.add(measurement)

        # 6. Team Selection Decision
        decision = TeamSelectionDecision(
            run_id=run.id,
            task_id=task.id,
            condition_id=condition.id,
            selected_topology=["Analyst", "Writer"],
            candidate_topologies=[["Analyst", "Writer"], ["Researcher", "Analyst", "Writer"]],
            confidence_score=0.75,
            latency_estimate_ms=35000,
        )
        db.add(decision)
        db.commit()

        # 7. Decision Explanation (H4 Traceability)
        explanation = DecisionExplanation(
            decision_id=decision.id,
            justification_text="Moderate complexity task requiring analysis and drafting.",
            rule_rationale="Triggered Rule R-02.",
        )
        db.add(explanation)

        # 8. Historical Performance Record with protocol provenance & source_run_ids
        test_cat = f"ANALYSIS_{uuid.uuid4().hex[:6]}"
        hist_record = HistoricalPerformanceRecord(
            task_category=test_cat,
            complexity_level=2,
            topology_signature="Analyst->Writer",
            protocol_origin="CALIBRATION",
            source_run_ids=[str(run.id)],
            sample_count=1,
            mean_wall_clock_ms=18500.0,
            mean_quality_score=0.88,
            mean_tokens=370.0,
            success_rate=1.0,
        )
        db.add(hist_record)
        db.commit()

        # Assert query relationships
        fetched_run = db.query(ExperimentalRun).filter_by(id=run.id).first()
        assert fetched_run is not None
        assert fetched_run.task.task_key == task_key
        assert fetched_run.condition.id == cond_id
        assert len(fetched_run.agent_executions) == 1
        assert fetched_run.performance_measurement.constraint_success is True
        assert fetched_run.decision.selected_topology == ["Analyst", "Writer"]
        assert fetched_run.decision.explanation.rule_rationale == "Triggered Rule R-02."

        # Assert historical record traceability and provenance
        fetched_hist = db.query(HistoricalPerformanceRecord).filter_by(id=hist_record.id).first()
        assert fetched_hist is not None
        assert fetched_hist.protocol_origin == "CALIBRATION"
        assert str(run.id) in fetched_hist.source_run_ids

        # Cascade cleanup: deleting task deletes runs, agent executions, measurements, and decisions
        db.delete(task)
        db.delete(condition)
        db.delete(hist_record)
        db.commit()

        # Verify cascades
        assert db.query(ExperimentalRun).filter_by(id=run.id).first() is None
        assert db.query(AgentExecutionRecord).filter_by(id=agent_exec.id).first() is None
        assert db.query(PerformanceMeasurement).filter_by(id=measurement.id).first() is None
        assert db.query(TeamSelectionDecision).filter_by(id=decision.id).first() is None
        assert db.query(DecisionExplanation).filter_by(id=explanation.id).first() is None

    finally:
        try:
            next(gen)
        except StopIteration:
            pass


def test_database_connection_failure_safe_handling(monkeypatch):
    """Verify GET /health/database safely handles database downtime returning HTTP 503."""
    # Temporarily monkeypatch check_database_connection to simulate database unreachable
    def mock_failure():
        return {
            "status": "unhealthy",
            "connected": False,
            "error": "Connection refused to PostgreSQL on port 5433",
            "database": "aether_db",
            "port": 5433,
        }

    monkeypatch.setattr("backend.routes.health.check_database_connection", mock_failure)

    response = client.get("/health/database")
    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "unhealthy"
    assert payload["connected"] is False
    assert "Connection refused" in payload["error"]


def test_experimental_runs_uniqueness_enforcement():
    """Verify database-level uniqueness constraint on (task_id, condition_id, run_number)."""
    gen = get_db()
    db = next(gen)
    try:
        # Create test task and condition
        cond_id = f"UNIQ_GRP_{uuid.uuid4().hex[:6]}"
        condition = ExperimentalCondition(
            id=cond_id,
            name="Uniqueness Condition",
            historical_memory_enabled=False,
            selection_policy="FIXED_PIPELINE",
        )
        task = Task(
            task_key=f"UNIQ-TASK-{uuid.uuid4().hex[:6]}",
            title="Uniqueness Task",
            prompt="Prompt",
            category="CODE",
            complexity_level=1,
            protocol_split="CALIBRATION",
            deterministic_constraints={},
        )
        db.add(condition)
        db.add(task)
        db.commit()

        # Insert run 1
        run1 = ExperimentalRun(
            task_id=task.id,
            condition_id=condition.id,
            run_number=1,
            status="COMPLETED",
            model_id="qwen2.5:7b",
        )
        db.add(run1)
        db.commit()

        # Attempt duplicate insertion with same task_id, condition_id, run_number=1
        run2_duplicate = ExperimentalRun(
            task_id=task.id,
            condition_id=condition.id,
            run_number=1,
            status="COMPLETED",
            model_id="qwen2.5:7b",
        )
        db.add(run2_duplicate)
        with pytest.raises(Exception) as exc_info:
            db.commit()

        assert "ix_runs_task_condition_runnum" in str(exc_info.value) or "duplicate key" in str(exc_info.value)
        db.rollback()

        # Clean up
        db.delete(task)
        db.delete(condition)
        db.commit()
    finally:
        try:
            next(gen)
        except StopIteration:
            pass
