"""Deterministic Retirement Cash Flow and Sustainability simulation engine."""
from typing import List, Optional
from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import CashFlowYearProjection, RetirementProjectionResult


def run_retirement_cash_flow_simulation(
    client: ClientProfile,
    profile: FinancialProfile,
    override_inflation: Optional[float] = None,
    override_return: Optional[float] = None,
    expense_multiplier: float = 1.0,
    one_time_shock_pkr: float = 0.0,
    shock_year: int = 1,
    custom_retirement_age: Optional[int] = None,
) -> RetirementProjectionResult:
    """
    Executes a year-by-year cash-flow and capital depletion simulation.
    All calculations are deterministic, transparent, and reproducible.
    """
    current_age = client.current_age
    ret_age = custom_retirement_age if custom_retirement_age is not None else client.retirement_age
    horizon_age = client.planning_horizon_age

    total_simulation_years = max(1, horizon_age - current_age)

    annual_inflation = override_inflation if override_inflation is not None else profile.goals.expected_annual_inflation_rate
    annual_return = override_return if override_return is not None else profile.goals.expected_annual_investment_return

    starting_capital = max(0.0, profile.net_investable_retirement_capital)
    current_capital = starting_capital

    yearly_projections: List[CashFlowYearProjection] = []
    depletion_age: Optional[int] = None
    sustainability_years = 0
    initial_annual_withdrawal = 0.0

    # Base baseline monthly figures
    base_ret_expenses_annual = profile.expenses.expected_retirement_expenses_monthly * 12.0 * expense_multiplier
    base_guaranteed_income_annual = profile.income.guaranteed_passive_retirement_income * 12.0

    for year_idx in range(1, total_simulation_years + 1):
        sim_age = current_age + year_idx - 1
        is_retired = sim_age >= ret_age

        # Compound inflation from year 1
        inflation_factor = (1.0 + annual_inflation) ** (year_idx - 1)

        if is_retired:
            annual_expenses = base_ret_expenses_annual * inflation_factor
            # Pension/rental guaranteed income (assume partially sticky, 50% indexed to inflation)
            annual_guaranteed_income = base_guaranteed_income_annual * ((1.0 + (annual_inflation * 0.5)) ** (year_idx - 1))
        else:
            # Pre-retirement: working income covers living expenses; net required withdrawal is 0
            annual_expenses = profile.expenses.total_current_monthly_expenses * 12.0 * inflation_factor
            annual_guaranteed_income = profile.income.total_monthly_income * 12.0 * inflation_factor

        # One-time capital shock (e.g. medical expense, wedding, or sudden loss)
        shock = one_time_shock_pkr if year_idx == shock_year else 0.0

        # Required net annual withdrawal from investment portfolio
        if is_retired:
            net_withdrawal = max(0.0, annual_expenses - annual_guaranteed_income) + shock
        else:
            # Pre-retirement saving or deficit
            pre_ret_surplus = annual_guaranteed_income - annual_expenses
            if pre_ret_surplus >= 0:
                net_withdrawal = shock
                # Capital can grow from pre-retirement savings
                current_capital += pre_ret_surplus
            else:
                net_withdrawal = abs(pre_ret_surplus) + shock

        if year_idx == 1 and is_retired:
            initial_annual_withdrawal = net_withdrawal

        if current_capital <= 0.0:
            if depletion_age is None and is_retired and annual_expenses > annual_guaranteed_income:
                depletion_age = sim_age
            # Capital already depleted
            yearly_projections.append(
                CashFlowYearProjection(
                    year_index=year_idx,
                    client_age=sim_age,
                    starting_capital_pkr=0.0,
                    investment_growth_pkr=0.0,
                    guaranteed_income_pkr=round(annual_guaranteed_income, 2),
                    total_expenses_pkr=round(annual_expenses, 2),
                    net_withdrawal_pkr=round(net_withdrawal, 2),
                    ending_capital_pkr=0.0,
                    is_depleted=True,
                )
            )
            continue

        # Investment growth earned on capital during the year (net of half-year withdrawals convention)
        investment_growth = max(0.0, (current_capital - (net_withdrawal * 0.5)) * annual_return)
        ending_capital = current_capital + investment_growth - net_withdrawal

        if ending_capital <= 0.0:
            ending_capital = 0.0
            if depletion_age is None and is_retired:
                depletion_age = sim_age
            is_depleted = True
        else:
            is_depleted = False
            sustainability_years += 1

        yearly_projections.append(
            CashFlowYearProjection(
                year_index=year_idx,
                client_age=sim_age,
                starting_capital_pkr=round(current_capital, 2),
                investment_growth_pkr=round(investment_growth, 2),
                guaranteed_income_pkr=round(annual_guaranteed_income, 2),
                total_expenses_pkr=round(annual_expenses, 2),
                net_withdrawal_pkr=round(net_withdrawal, 2),
                ending_capital_pkr=round(ending_capital, 2),
                is_depleted=is_depleted,
            )
        )

        current_capital = ending_capital

    is_sustainable = (depletion_age is None) or (depletion_age >= horizon_age)

    # Initial withdrawal rate
    if starting_capital > 0 and initial_annual_withdrawal > 0:
        initial_withdrawal_rate = round((initial_annual_withdrawal / starting_capital) * 100.0, 2)
    else:
        initial_withdrawal_rate = 0.0

    if is_sustainable:
        summary_verdict = (
            f"Modeled capital remains solvent through the full planning horizon to age {horizon_age}. "
            f"Projected terminal capital is PKR {current_capital:,.0f}."
        )
    else:
        summary_verdict = (
            f"Under modeled assumptions, retirement capital is projected to become depleted at approximately age {depletion_age} "
            f"(after {sustainability_years} years). Action is needed to bridge the retirement income gap."
        )

    return RetirementProjectionResult(
        starting_capital_pkr=round(starting_capital, 2),
        annual_inflation_rate=annual_inflation,
        annual_return_rate=annual_return,
        sustainability_years=sustainability_years,
        capital_depletion_age=depletion_age,
        is_sustainable_through_horizon=is_sustainable,
        ending_capital_at_horizon_pkr=round(current_capital, 2),
        yearly_trajectory=yearly_projections,
        annual_withdrawal_rate_initial_pct=initial_withdrawal_rate,
        summary_verdict=summary_verdict,
    )
