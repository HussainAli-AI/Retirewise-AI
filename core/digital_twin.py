"""Digital Twin What-If sensitivity and scenario evaluation engine."""
from typing import Optional, Dict, Any
from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import FinancialHealthMetrics, MonteCarloResult
from core.monte_carlo_engine import run_monte_carlo_simulation
from core.retirement_engine import run_retirement_cash_flow_simulation


def simulate_digital_twin_what_if(
    client: ClientProfile,
    financial_profile: FinancialProfile,
    health: FinancialHealthMetrics,
    retirement_age_delta: int = 0,
    monthly_expense_multiplier: float = 1.0,
    lump_sum_event_amount: float = 0.0,
    lump_sum_event_age: Optional[int] = None,
    trials_count: int = 500,
) -> Dict[str, Any]:
    """
    Evaluates real-time 'What-If' shifts on the client's financial digital twin:
    - Shifting retirement age (e.g. retiring 2 years later or 3 years earlier)
    - Scaling retirement living expenses (e.g. 1.2x for lifestyle expansion or 0.85x for frugal plan)
    - One-time cash events (property sale/inheritance vs. medical shock/wedding)
    """
    adjusted_retirement_age = max(client.current_age + 1, client.retirement_age + retirement_age_delta)
    
    base_expenses = (
        financial_profile.expenses.expected_retirement_expenses_monthly
        or financial_profile.expenses.essential_expenses_monthly
    )
    adjusted_monthly_expenses = max(10_000.0, base_expenses * monthly_expense_multiplier)

    # Inflow vs Outflow determination
    inflow = lump_sum_event_amount if lump_sum_event_amount > 0 else 0.0
    outflow = abs(lump_sum_event_amount) if lump_sum_event_amount < 0 else 0.0

    # 1. Deterministic simulation with adjustments
    det_sim = run_retirement_cash_flow_simulation(
        client=client,
        profile=financial_profile,
        expense_multiplier=monthly_expense_multiplier,
        custom_retirement_age=adjusted_retirement_age,
    )

    # 2. Stochastic Monte Carlo simulation with adjustments
    mc_sim = run_monte_carlo_simulation(
        client=client,
        financial_profile=financial_profile,
        health=health,
        trials_count=trials_count,
        override_retirement_age=adjusted_retirement_age,
        override_monthly_expenses=adjusted_monthly_expenses,
        lump_sum_inflow=inflow,
        lump_sum_outflow=outflow,
        lump_sum_age=lump_sum_event_age,
    )

    return {
        "adjusted_retirement_age": adjusted_retirement_age,
        "adjusted_monthly_expenses_pkr": round(adjusted_monthly_expenses, 2),
        "lump_sum_event_amount_pkr": lump_sum_event_amount,
        "lump_sum_event_age": lump_sum_event_age,
        "baseline_sustainability_years": det_sim.sustainability_years,
        "baseline_depletion_age": det_sim.capital_depletion_age,
        "what_if_probability_of_success_pct": mc_sim.probability_of_success_pct,
        "what_if_median_depletion_age": mc_sim.median_depletion_age,
        "what_if_median_ending_capital_pkr": mc_sim.median_ending_capital_pkr,
        "confidence_verdict": mc_sim.confidence_verdict,
        "percentile_trajectories": [p.model_dump() for p in mc_sim.percentile_trajectories],
    }
