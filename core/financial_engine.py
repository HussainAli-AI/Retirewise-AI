"""Deterministic financial health calculations."""
from models.financial_profile import FinancialProfile
from models.assessment import FinancialHealthMetrics


def calculate_financial_health(profile: FinancialProfile) -> FinancialHealthMetrics:
    """
    Computes objective, deterministic financial health metrics for a given client profile.
    Formulas are transparent, explainable, and fully reproducible.
    """
    total_assets = profile.assets.total_assets
    total_liabilities = profile.liabilities.total_liabilities
    net_worth = profile.net_worth
    liquid_assets = profile.assets.total_liquid_assets
    net_investable_capital = profile.net_investable_retirement_capital

    current_income = profile.income.total_monthly_income
    current_expenses = profile.expenses.total_current_monthly_expenses
    current_surplus = current_income - current_expenses

    guaranteed_ret_income = profile.income.guaranteed_passive_retirement_income
    projected_ret_expenses = profile.expenses.expected_retirement_expenses_monthly

    # Gap between target expenses and guaranteed passive income (monthly amount that must come from capital)
    monthly_ret_gap = max(0.0, projected_ret_expenses - guaranteed_ret_income)

    # Emergency reserve adequacy
    # Emergency reserve is target_months * essential_monthly_expenses
    target_reserve = profile.goals.emergency_reserve_months * max(1.0, profile.expenses.essential_expenses_monthly)
    emergency_adequacy_ratio = (liquid_assets / target_reserve) if target_reserve > 0 else 1.0

    # Initial annual withdrawal rate required from investable capital
    annual_funding_required = monthly_ret_gap * 12.0
    if net_investable_capital > 0:
        annual_withdrawal_rate_pct = (annual_funding_required / net_investable_capital) * 100.0
    else:
        annual_withdrawal_rate_pct = 999.9 if annual_funding_required > 0 else 0.0

    return FinancialHealthMetrics(
        total_assets_pkr=round(total_assets, 2),
        total_liabilities_pkr=round(total_liabilities, 2),
        net_worth_pkr=round(net_worth, 2),
        liquid_assets_pkr=round(liquid_assets, 2),
        net_investable_retirement_capital_pkr=round(net_investable_capital, 2),
        current_monthly_income_pkr=round(current_income, 2),
        current_monthly_expenses_pkr=round(current_expenses, 2),
        current_monthly_surplus_pkr=round(current_surplus, 2),
        guaranteed_monthly_retirement_income_pkr=round(guaranteed_ret_income, 2),
        projected_monthly_retirement_expenses_pkr=round(projected_ret_expenses, 2),
        monthly_retirement_income_gap_pkr=round(monthly_ret_gap, 2),
        emergency_reserve_adequacy_ratio=round(emergency_adequacy_ratio, 2),
        annual_withdrawal_rate_pct=round(annual_withdrawal_rate_pct, 2),
    )
