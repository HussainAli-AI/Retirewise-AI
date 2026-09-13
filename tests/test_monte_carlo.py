"""Unit tests for the Monte Carlo stochastic simulation engine."""
from models.client import ClientProfile, MaritalStatus
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)
from core.financial_engine import calculate_financial_health
from core.monte_carlo_engine import run_monte_carlo_simulation


def get_test_client_and_profile():
    client = ClientProfile(
        client_id="TEST-MC-01",
        name="Test MC Client",
        current_age=60,
        retirement_age=60,
        planning_horizon_age=80,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=0,
        adviser_name="Adviser Test",
    )
    profile = FinancialProfile(
        client_id="TEST-MC-01",
        income=IncomeBreakdown(salary_monthly=0.0, pension_monthly=50_000.0),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=80_000.0,
            discretionary_expenses_monthly=20_000.0,
            expected_retirement_expenses_monthly=100_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=2_000_000.0,
            liquid_investments=18_000_000.0,
        ),
        liabilities=LiabilityBreakdown(),
        goals=RetirementGoals(target_monthly_income_pkr=100_000.0),
    )
    return client, profile


def test_monte_carlo_runs_and_produces_trajectories():
    client, profile = get_test_client_and_profile()
    health = calculate_financial_health(profile)

    mc = run_monte_carlo_simulation(client, profile, health, trials_count=200, seed=42)

    assert mc.trials_count == 200
    assert 0.0 <= mc.probability_of_success_pct <= 100.0
    assert len(mc.percentile_trajectories) == (client.planning_horizon_age - client.retirement_age + 1)

    # Verify percentiles ordering: p10 <= p50 <= p90
    for pt in mc.percentile_trajectories:
        assert pt.p10_capital_pkr <= pt.p50_capital_pkr + 0.01
        assert pt.p50_capital_pkr <= pt.p90_capital_pkr + 0.01


def test_monte_carlo_zero_capital_immediate_depletion():
    client, profile = get_test_client_and_profile()
    # Wipe out assets
    profile.assets.cash_and_savings = 0.0
    profile.assets.liquid_investments = 0.0
    profile.income.pension_monthly = 0.0
    health = calculate_financial_health(profile)

    mc = run_monte_carlo_simulation(client, profile, health, trials_count=100, seed=42)
    assert mc.probability_of_success_pct == 0.0
    assert mc.median_depletion_age == client.retirement_age
