"""Unit tests for Capacity for Loss and Suitability Conflict engine."""
from models.assessment import RiskCategory, CapacityCategory
from core.capacity_engine import calculate_capacity_for_loss, evaluate_suitability_conflicts
from core.risk_engine import calculate_risk_tolerance
from data.sample_clients import get_synthetic_personas


def test_capacity_for_loss_persona_c_conflict():
    personas = get_synthetic_personas()
    # Persona C is Kamran (High-Risk / Low-Capacity Conflict)
    client_c, profile_c, risk_answers_c = personas[2]

    risk_result = calculate_risk_tolerance(risk_answers_c)
    capacity_result = calculate_capacity_for_loss(client_c, profile_c)
    warnings, has_conflict = evaluate_suitability_conflicts(risk_result, capacity_result, profile_c, client_c)

    # Risk should be aggressive or growth
    assert risk_result.category in [RiskCategory.GROWTH, RiskCategory.AGGRESSIVE]
    # Capacity must be low or very low due to low liquid reserve & high dependency
    assert capacity_result.category in [CapacityCategory.VERY_LOW, CapacityCategory.LOW]

    # Must trigger critical suitability conflict!
    assert has_conflict is True
    assert any(w.code == "SUITABILITY_RISK_CAPACITY_MISMATCH" for w in warnings)


def test_capacity_for_loss_persona_b_healthy():
    personas = get_synthetic_personas()
    client_b, profile_b, _ = personas[1]

    capacity_result = calculate_capacity_for_loss(client_b, profile_b)
    # Persona B has strong reserves and 6 pre-retirement working years
    assert capacity_result.capacity_score >= 50.0
    assert capacity_result.category in [CapacityCategory.MODERATE, CapacityCategory.HIGH, CapacityCategory.VERY_HIGH]
