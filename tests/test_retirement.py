"""Unit tests for retirement cash flow simulation engine."""
from models.client import ClientProfile, MaritalStatus
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)
from core.retirement_engine import run_retirement_cash_flow_simulation


def test_simulation_with_zero_capital_depletes():
    client = ClientProfile(
        client_id="TEST-ZERO",
        name="Zero Capital Test",
        current_age=60,
        retirement_age=60,
        planning_horizon_age=80,
        marital_status=MaritalStatus.SINGLE,
    )
    profile = FinancialProfile(
        client_id=client.client_id,
        income=IncomeBreakdown(pension_monthly=0.0),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=50_000.0,
            expected_retirement_expenses_monthly=50_000.0,
        ),
        assets=AssetBreakdown(cash_and_savings=0.0),
        liabilities=LiabilityBreakdown(),
        goals=RetirementGoals(target_monthly_income_pkr=50_000.0),
    )

    result = run_retirement_cash_flow_simulation(client, profile)
    assert result.is_sustainable_through_horizon is False
    assert result.sustainability_years == 0
    assert result.capital_depletion_age == 60


def test_simulation_with_abundant_capital_is_sustainable():
    client = ClientProfile(
        client_id="TEST-ABUNDANT",
        name="Abundant Capital Test",
        current_age=60,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
    )
    profile = FinancialProfile(
        client_id=client.client_id,
        income=IncomeBreakdown(pension_monthly=100_000.0),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=80_000.0,
            expected_retirement_expenses_monthly=120_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=10_000_000.0,
            liquid_investments=30_000_000.0,  # 40M total capital
        ),
        liabilities=LiabilityBreakdown(),
        goals=RetirementGoals(
            target_monthly_income_pkr=120_000.0,
            expected_annual_inflation_rate=0.06,
            expected_annual_investment_return=0.12,  # Positive real return
        ),
    )

    result = run_retirement_cash_flow_simulation(client, profile)
    assert result.is_sustainable_through_horizon is True
    assert result.capital_depletion_age is None
    assert len(result.yearly_trajectory) == 25  # 85 - 60 = 25 years
    assert result.ending_capital_at_horizon_pkr > 0
