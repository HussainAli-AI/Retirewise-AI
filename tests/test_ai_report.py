"""Unit tests for AI explanation and audit generator."""
from ai.report_generator import AIReportNarrativeGenerator
from ai.llm_client import LLMClient
from database.database import Database


def test_condense_assessment_payload():
    db = Database("retirewise.db")
    assess = db.get_latest_assessment("CLIENT-001-TARIQ")
    assert assess is not None

    condensed = AIReportNarrativeGenerator._condense_assessment_payload(assess)
    
    # Verify core fields exist
    assert "assessment_id" in condensed
    assert "financial_health" in condensed
    assert "risk_tolerance" in condensed
    assert "capacity_for_loss" in condensed
    assert "base_case_projection" in condensed
    assert "stress_test_scenarios_summary" in condensed
    assert "conflict_warnings" in condensed

    # Verify no massive year-by-year cashflow arrays are present
    assert "yearly_trajectory" not in condensed["base_case_projection"]
    for scenario in condensed["stress_test_scenarios_summary"]:
        assert "yearly_trajectory" not in scenario


def test_ai_narrative_mock_fallback():
    db = Database("retirewise.db")
    assess = db.get_latest_assessment("CLIENT-001-TARIQ")
    assert assess is not None

    mock_client = LLMClient(provider="mock")
    generator = AIReportNarrativeGenerator(mock_client)
    
    narrative = generator.generate_assessment_explanation(assess)
    assert len(narrative) > 100
    assert "Deterministic Engine" in narrative or "RetireWise AI" in narrative
