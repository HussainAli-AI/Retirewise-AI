"""Unit tests for deterministic financial health engine."""
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)
from core.financial_engine import calculate_financial_health


def test_financial_health_calculations():
    profile = FinancialProfile(
        client_id="TEST-FIN-01",
        income=IncomeBreakdown(
            salary_monthly=300_000.0,
            pension_monthly=40_000.0,
            rental_income_monthly=30_000.0,
        ),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=100_000.0,
            discretionary_expenses_monthly=50_000.0,
            healthcare_monthly=10_000.0,
            debt_service_monthly=20_000.0,
            expected_retirement_expenses_monthly=150_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=2_000_000.0,
            liquid_investments=4_000_000.0,
            property_investment=10_000_000.0,
        ),
        liabilities=LiabilityBreakdown(
            mortgage_balance=1_000_000.0,
        ),
        goals=RetirementGoals(
            target_monthly_income_pkr=150_000.0,
            emergency_reserve_months=6,
        ),
    )

    fh = calculate_financial_health(profile)

    # Assets: 2M + 4M + 10M = 16M
    assert fh.total_assets_pkr == 16_000_000.0
    # Liabilities: 1M
    assert fh.total_liabilities_pkr == 1_000_000.0
    # Net Worth: 16M - 1M = 15M
    assert fh.net_worth_pkr == 15_000_000.0
    # Liquid Assets: 2M + 4M = 6M
    assert fh.liquid_assets_pkr == 6_000_000.0

    # Current Income: 300k + 40k + 30k = 370k
    assert fh.current_monthly_income_pkr == 370_000.0
    # Current Expenses: 100k + 50k + 10k + 20k = 180k
    assert fh.current_monthly_expenses_pkr == 180_000.0
    # Monthly Surplus: 370k - 180k = 190k
    assert fh.current_monthly_surplus_pkr == 190_000.0

    # Guaranteed Retirement Income: Pension(40k) + Rental(30k) = 70k
    assert fh.guaranteed_monthly_retirement_income_pkr == 70_000.0
    # Retirement gap: 150k - 70k = 80k
    assert fh.monthly_retirement_income_gap_pkr == 80_000.0

    # Target reserve: 6 months * 100k essential = 600k
    # Liquid assets: 6M -> Adequacy = 6M / 600k = 10.0
    assert fh.emergency_reserve_adequacy_ratio == 10.0
