"""Unit tests for Risk Tolerance scoring engine."""
from core.risk_engine import calculate_risk_tolerance, RISK_QUESTIONS
from models.assessment import RiskCategory


def test_risk_tolerance_minimum_score():
    # All minimum responses (1)
    min_responses = {q["id"]: 1 for q in RISK_QUESTIONS}
    result = calculate_risk_tolerance(min_responses)
    assert result.normalized_score == 0.0
    assert result.category == RiskCategory.VERY_CONSERVATIVE


def test_risk_tolerance_maximum_score():
    # All maximum responses (4)
    max_responses = {q["id"]: 4 for q in RISK_QUESTIONS}
    result = calculate_risk_tolerance(max_responses)
    assert result.normalized_score == 100.0
    assert result.category == RiskCategory.AGGRESSIVE


def test_risk_tolerance_moderate():
    # All 2 or 3 responses
    responses = {
        "q1_loss_reaction": 2,
        "q2_volatility_comfort": 3,
        "q3_investment_experience": 2,
        "q4_financial_knowledge": 3,
        "q5_horizon_perspective": 2,
        "q6_return_expectation": 3,
        "q7_stability_vs_growth": 2,
        "q8_inflation_drawdown_tradeoff": 3,
    }
    result = calculate_risk_tolerance(responses)
    assert 40.0 <= result.normalized_score <= 60.0
    assert result.category == RiskCategory.MODERATE
