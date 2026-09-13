"""Stress Testing and Scenario Analysis Engine."""
from typing import List
from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import ScenarioResult, ScenarioType
from core.retirement_engine import run_retirement_cash_flow_simulation


def run_all_stress_scenarios(client: ClientProfile, profile: FinancialProfile) -> List[ScenarioResult]:
    """
    Executes a structured suite of deterministic macroeconomic and personal stress tests.
    """
    results: List[ScenarioResult] = []

    base_inflation = profile.goals.expected_annual_inflation_rate
    base_return = profile.goals.expected_annual_investment_return

    # Scenario 1: Base Case
    base_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=profile,
        override_inflation=base_inflation,
        override_return=base_return,
    )
    results.append(
        ScenarioResult(
            scenario_type=ScenarioType.BASE_CASE,
            scenario_name="Base Case (Current Assumptions)",
            description=f"Standard expectation with {base_return*100:.1f}% annual return and {base_inflation*100:.1f}% annual inflation.",
            annual_inflation_rate=base_inflation,
            annual_return_rate=base_return,
            sustainability_years=base_sim.sustainability_years,
            capital_depletion_age=base_sim.capital_depletion_age,
            is_sustainable=base_sim.is_sustainable_through_horizon,
            ending_capital_pkr=base_sim.ending_capital_at_horizon_pkr,
            key_vulnerability="Vulnerable to prolonged macroeconomic shocks or systemic inflation surges.",
            yearly_trajectory=base_sim.yearly_trajectory,
        )
    )

    # Scenario 2: High Inflation Shock (Critical for Pakistan)
    # Inflation increases by 500 bps (e.g., from 8% to 13%) while returns fail to catch up completely
    high_inf_rate = min(0.30, base_inflation + 0.05)
    inf_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=profile,
        override_inflation=high_inf_rate,
        override_return=base_return,  # Nominal returns stagnate
    )
    results.append(
        ScenarioResult(
            scenario_type=ScenarioType.HIGH_INFLATION,
            scenario_name="High Inflation Shock (+5% p.a.)",
            description=f"Persistent inflation spike to {high_inf_rate*100:.1f}% p.a. while portfolio return remains at {base_return*100:.1f}%.",
            annual_inflation_rate=high_inf_rate,
            annual_return_rate=base_return,
            sustainability_years=inf_sim.sustainability_years,
            capital_depletion_age=inf_sim.capital_depletion_age,
            is_sustainable=inf_sim.is_sustainable_through_horizon,
            ending_capital_pkr=inf_sim.ending_capital_at_horizon_pkr,
            key_vulnerability="Rapid erosion of living standards; expenses double significantly faster.",
            yearly_trajectory=inf_sim.yearly_trajectory,
        )
    )

    # Scenario 3: Early Market Drawdown (Sequence-of-Returns Shock)
    # Returns drop significantly by 400 bps across the horizon or early years
    stressed_return = max(0.02, base_return - 0.04)
    market_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=profile,
        override_inflation=base_inflation,
        override_return=stressed_return,
    )
    results.append(
        ScenarioResult(
            scenario_type=ScenarioType.MARKET_STRESS,
            scenario_name="Adverse Market Returns (-4% p.a.)",
            description=f"Subdued portfolio performance averaging {stressed_return*100:.1f}% p.a. across the retirement horizon.",
            annual_inflation_rate=base_inflation,
            annual_return_rate=stressed_return,
            sustainability_years=market_sim.sustainability_years,
            capital_depletion_age=market_sim.capital_depletion_age,
            is_sustainable=market_sim.is_sustainable_through_horizon,
            ending_capital_pkr=market_sim.ending_capital_at_horizon_pkr,
            key_vulnerability="Negative compound growth accelerates portfolio exhaustion.",
            yearly_trajectory=market_sim.yearly_trajectory,
        )
    )

    # Scenario 4: Major Healthcare / Medical Shock
    # One-time medical shock of PKR 2,500,000 in year 3 + 15% permanent recurring healthcare expense increase
    medical_shock_pkr = 2_500_000.0
    med_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=profile,
        override_inflation=base_inflation,
        override_return=base_return,
        expense_multiplier=1.15,
        one_time_shock_pkr=medical_shock_pkr,
        shock_year=3,
    )
    results.append(
        ScenarioResult(
            scenario_type=ScenarioType.MEDICAL_SHOCK,
            scenario_name="Healthcare Crisis Shock",
            description="Lump-sum medical event of PKR 2.5M in year 3 plus 15% ongoing rise in healthcare expenses.",
            annual_inflation_rate=base_inflation,
            annual_return_rate=base_return,
            sustainability_years=med_sim.sustainability_years,
            capital_depletion_age=med_sim.capital_depletion_age,
            is_sustainable=med_sim.is_sustainable_through_horizon,
            ending_capital_pkr=med_sim.ending_capital_at_horizon_pkr,
            key_vulnerability="Lump-sum drawdowns permanently impair capital base early in retirement.",
            yearly_trajectory=med_sim.yearly_trajectory,
        )
    )

    # Scenario 5: Early Retirement / Forced Income Reduction
    # Retiring 3 years earlier or starting withdrawals sooner
    early_ret_age = max(client.current_age, client.retirement_age - 3)
    early_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=profile,
        override_inflation=base_inflation,
        override_return=base_return,
        custom_retirement_age=early_ret_age,
    )
    results.append(
        ScenarioResult(
            scenario_type=ScenarioType.EARLY_RETIREMENT,
            scenario_name="Early Retirement (-3 Years)",
            description=f"Retirement begins 3 years earlier at age {early_ret_age}, lengthening the withdrawal period.",
            annual_inflation_rate=base_inflation,
            annual_return_rate=base_return,
            sustainability_years=early_sim.sustainability_years,
            capital_depletion_age=early_sim.capital_depletion_age,
            is_sustainable=early_sim.is_sustainable_through_horizon,
            ending_capital_pkr=early_sim.ending_capital_at_horizon_pkr,
            key_vulnerability="Loss of 3 accumulation years and 3 additional years of capital drawdown.",
            yearly_trajectory=early_sim.yearly_trajectory,
        )
    )

    return results
