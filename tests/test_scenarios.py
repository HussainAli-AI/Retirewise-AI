"""Unit tests for Scenario and Stress Testing engine."""
from models.assessment import ScenarioType
from core.scenario_engine import run_all_stress_scenarios
from data.sample_clients import get_synthetic_personas


def test_all_stress_scenarios_generated():
    personas = get_synthetic_personas()
    client_a, profile_a, _ = personas[0]

    scenarios = run_all_stress_scenarios(client_a, profile_a)
    assert len(scenarios) == 5

    types = [s.scenario_type for s in scenarios]
    assert ScenarioType.BASE_CASE in types
    assert ScenarioType.HIGH_INFLATION in types
    assert ScenarioType.MARKET_STRESS in types
    assert ScenarioType.MEDICAL_SHOCK in types
    assert ScenarioType.EARLY_RETIREMENT in types

    base_scen = next(s for s in scenarios if s.scenario_type == ScenarioType.BASE_CASE)
    inf_scen = next(s for s in scenarios if s.scenario_type == ScenarioType.HIGH_INFLATION)

    # High inflation shock must result in lower ending capital than base case
    assert inf_scen.ending_capital_pkr <= base_scen.ending_capital_pkr
