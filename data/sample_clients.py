"""Synthetic personas and sample test data for RetireWise AI."""
from typing import List, Tuple, Dict
from models.client import ClientProfile, MaritalStatus
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)


def get_synthetic_personas() -> List[Tuple[ClientProfile, FinancialProfile, Dict[str, int]]]:
    """
    Returns 3 realistic synthetic personas matching the specification:
    1. Persona A: Conservative Retiree (Age 62, PKR 20M capital, PKR 50k pension, PKR 150k expenses, 2 dependents)
    2. Persona B: Moderate Near-Retiree (Age 55, High savings, balanced profile)
    3. Persona C: High-Risk / Low-Capacity Conflict (Aggressive risk attitude, fragile financial capacity)
    """

    # --- Persona A: Conservative Retiree ---
    client_a = ClientProfile(
        client_id="CLIENT-001-TARIQ",
        name="Tariq Mahmood (Persona A - Conservative Retiree)",
        current_age=62,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=2,
        adviser_name="Usman Khan, CFP",
        notes="Retired corporate director. Primary goal is stable income and capital preservation.",
    )
    profile_a = FinancialProfile(
        client_id=client_a.client_id,
        income=IncomeBreakdown(
            salary_monthly=0.0,
            pension_monthly=50_000.0,
            rental_income_monthly=0.0,
            business_income_monthly=0.0,
            other_income_monthly=0.0,
        ),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=110_000.0,
            discretionary_expenses_monthly=40_000.0,
            healthcare_monthly=15_000.0,
            debt_service_monthly=0.0,
            expected_retirement_expenses_monthly=150_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=4_000_000.0,
            liquid_investments=6_000_000.0,
            provident_fund=0.0,
            gratuity_expected=0.0,
            vps_pension_balance=0.0,
            gold_and_valuables=2_000_000.0,
            property_primary_residence=25_000_000.0,
            property_investment=8_000_000.0,
            other_assets=0.0,
        ),
        liabilities=LiabilityBreakdown(
            mortgage_balance=0.0,
            personal_loans=0.0,
            credit_card_debt=0.0,
            other_liabilities=0.0,
        ),
        goals=RetirementGoals(
            target_monthly_income_pkr=150_000.0,
            emergency_reserve_months=12,
            healthcare_reserve_pkr=1_500_000.0,
            legacy_bequest_target_pkr=10_000_000.0,
            expected_annual_inflation_rate=0.08,
            expected_annual_investment_return=0.10,
        ),
    )
    # Answers reflecting conservative preferences (Score ~25)
    risk_a: Dict[str, int] = {
        "q1_loss_reaction": 1,
        "q2_volatility_comfort": 1,
        "q3_investment_experience": 2,
        "q4_financial_knowledge": 2,
        "q5_horizon_perspective": 2,
        "q6_return_expectation": 1,
        "q7_stability_vs_growth": 1,
        "q8_inflation_drawdown_tradeoff": 1,
    }

    # --- Persona B: Moderate Near-Retiree ---
    client_b = ClientProfile(
        client_id="CLIENT-002-AYESHA",
        name="Ayesha Siddiqui (Persona B - Moderate Near-Retiree)",
        current_age=54,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=1,
        adviser_name="Usman Khan, CFP",
        notes="Senior banking executive 6 years from retirement. Healthy savings and diversified portfolio.",
    )
    profile_b = FinancialProfile(
        client_id=client_b.client_id,
        income=IncomeBreakdown(
            salary_monthly=550_000.0,
            pension_monthly=0.0,
            rental_income_monthly=80_000.0,
            business_income_monthly=0.0,
            other_income_monthly=0.0,
        ),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=160_000.0,
            discretionary_expenses_monthly=90_000.0,
            healthcare_monthly=20_000.0,
            debt_service_monthly=45_000.0,
            expected_retirement_expenses_monthly=250_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=5_000_000.0,
            liquid_investments=14_000_000.0,
            provident_fund=12_000_000.0,
            gratuity_expected=6_000_000.0,
            vps_pension_balance=4_000_000.0,
            gold_and_valuables=4_000_000.0,
            property_primary_residence=40_000_000.0,
            property_investment=18_000_000.0,
            other_assets=2_000_000.0,
        ),
        liabilities=LiabilityBreakdown(
            mortgage_balance=2_500_000.0,
            personal_loans=0.0,
            credit_card_debt=150_000.0,
            other_liabilities=0.0,
        ),
        goals=RetirementGoals(
            target_monthly_income_pkr=250_000.0,
            emergency_reserve_months=6,
            healthcare_reserve_pkr=2_500_000.0,
            legacy_bequest_target_pkr=20_000_000.0,
            expected_annual_inflation_rate=0.08,
            expected_annual_investment_return=0.12,
        ),
    )
    # Answers reflecting moderate preferences (Score ~50)
    risk_b: Dict[str, int] = {
        "q1_loss_reaction": 3,
        "q2_volatility_comfort": 3,
        "q3_investment_experience": 3,
        "q4_financial_knowledge": 3,
        "q5_horizon_perspective": 3,
        "q6_return_expectation": 2,
        "q7_stability_vs_growth": 3,
        "q8_inflation_drawdown_tradeoff": 3,
    }

    # --- Persona C: High-Risk / Low-Capacity Conflict ---
    client_c = ClientProfile(
        client_id="CLIENT-003-KAMRAN",
        name="Kamran Aslam (Persona C - High-Risk / Low-Capacity Conflict)",
        current_age=60,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=3,
        adviser_name="Usman Khan, CFP",
        notes="Recently retired businessman. Highly speculative mindset but very limited liquid reserves and high expenses.",
    )
    profile_c = FinancialProfile(
        client_id=client_c.client_id,
        income=IncomeBreakdown(
            salary_monthly=0.0,
            pension_monthly=0.0,
            rental_income_monthly=20_000.0,
            business_income_monthly=0.0,
            other_income_monthly=0.0,
        ),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=140_000.0,
            discretionary_expenses_monthly=50_000.0,
            healthcare_monthly=25_000.0,
            debt_service_monthly=15_000.0,
            expected_retirement_expenses_monthly=200_000.0,
        ),
        assets=AssetBreakdown(
            cash_and_savings=200_000.0,  # < 2 months liquid emergency reserve!
            liquid_investments=100_000.0,
            provident_fund=0.0,
            gratuity_expected=0.0,
            vps_pension_balance=0.0,
            gold_and_valuables=500_000.0,
            property_primary_residence=18_000_000.0,  # Illiquid
            property_investment=3_000_000.0,
            other_assets=0.0,
        ),
        liabilities=LiabilityBreakdown(
            mortgage_balance=0.0,
            personal_loans=1_200_000.0,
            credit_card_debt=450_000.0,
            other_liabilities=350_000.0,
        ),
        goals=RetirementGoals(
            target_monthly_income_pkr=200_000.0,
            emergency_reserve_months=6,
            healthcare_reserve_pkr=500_000.0,
            legacy_bequest_target_pkr=5_000_000.0,
            expected_annual_inflation_rate=0.08,
            expected_annual_investment_return=0.15,
        ),
    )
    # Answers reflecting aggressive preferences (Score ~90)
    risk_c: Dict[str, int] = {
        "q1_loss_reaction": 4,
        "q2_volatility_comfort": 4,
        "q3_investment_experience": 4,
        "q4_financial_knowledge": 3,
        "q5_horizon_perspective": 4,
        "q6_return_expectation": 4,
        "q7_stability_vs_growth": 4,
        "q8_inflation_drawdown_tradeoff": 4,
    }

    return [(client_a, profile_a, risk_a), (client_b, profile_b, risk_b), (client_c, profile_c, risk_c)]
