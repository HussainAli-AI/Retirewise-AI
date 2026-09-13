"""Unit tests for Pakistan Shariah asset allocation engine and Section 63 tax optimizer."""
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
from core.capacity_engine import calculate_capacity_for_loss
from core.risk_engine import calculate_risk_tolerance
from core.shariah_engine import calculate_pakistan_asset_allocation


def test_shariah_capacity_equity_ceiling_enforced():
    # Client with low capacity (e.g. 2 months reserves, high debt) but aggressive risk appetite
    client = ClientProfile(
        client_id="TEST-SH-01",
        name="Test Shariah Client",
        current_age=50,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=3,
        adviser_name="Adviser Test",
    )
    profile = FinancialProfile(
        client_id="TEST-SH-01",
        income=IncomeBreakdown(salary_monthly=300_000.0),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=150_000.0,
            expected_retirement_expenses_monthly=180_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=300_000.0,  # Only 2 months essential
            liquid_investments=500_000.0,
        ),
        liabilities=LiabilityBreakdown(personal_loans=500_000.0),
        goals=RetirementGoals(target_monthly_income_pkr=180_000.0),
    )

    health = calculate_financial_health(profile)
    capacity = calculate_capacity_for_loss(client, profile)
    # Aggressive risk answers (all 3) -> normalized score ~100
    risk = calculate_risk_tolerance({"q1": 3, "q2": 3, "q3": 3, "q4": 3, "q5": 3, "q6": 3, "q7": 3, "q8": 3})

    shariah_res = calculate_pakistan_asset_allocation(client, profile, health, capacity, risk, is_shariah_mode=True)

    # Verify equity ceiling is strictly enforced
    equity_item = next(item for item in shariah_res.recommended_allocations if "Equities" in item.asset_class)
    assert equity_item.recommended_pct <= shariah_res.capacity_equity_ceiling_pct
    assert equity_item.recommended_pct < 80.0  # Curtailed from aggressive appetite


def test_section_63_tax_credit_calculation():
    client = ClientProfile(
        client_id="TEST-SH-02",
        name="Test Tax Client",
        current_age=46,  # Age 46 (>40) gets 6% age bonus
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.SINGLE,
        dependents_count=0,
        adviser_name="Adviser Test",
    )
    profile = FinancialProfile(
        client_id="TEST-SH-02",
        income=IncomeBreakdown(salary_monthly=500_000.0),  # PKR 6M annual
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=100_000.0,
            expected_retirement_expenses_monthly=120_000.0,
        ),
        assets=AssetBreakdown(cash_and_savings=2_000_000.0),
        liabilities=LiabilityBreakdown(),
        goals=RetirementGoals(target_monthly_income_pkr=150_000.0),
    )

    health = calculate_financial_health(profile)
    capacity = calculate_capacity_for_loss(client, profile)
    risk = calculate_risk_tolerance({"q1": 2, "q2": 2, "q3": 2, "q4": 2, "q5": 2, "q6": 2, "q7": 2, "q8": 2})

    shariah_res = calculate_pakistan_asset_allocation(client, profile, health, capacity, risk, is_shariah_mode=True)

    # Annual salary = 6,000,000. Eligible fraction = 20% + (46-40)*2% = 26%. Max contrib = 1,560,000.
    # Estimated 20% tax savings = 312,000 PKR
    assert shariah_res.estimated_annual_tax_credit_pkr > 100_000.0
    assert "Section 63" in shariah_res.tax_optimization_notes
