"""Vectorized 1,000-trial Monte Carlo stochastic simulation engine for retirement solvency."""
import numpy as np
from typing import Optional, List, Tuple
from models.assessment import (
    MonteCarloResult,
    MonteCarloTrajectoryPoint,
    FinancialHealthMetrics,
)
from models.client import ClientProfile
from models.financial_profile import FinancialProfile


def run_monte_carlo_simulation(
    client: ClientProfile,
    financial_profile: FinancialProfile,
    health: FinancialHealthMetrics,
    trials_count: int = 1000,
    mean_return: float = 0.12,
    return_std: float = 0.065,
    mean_inflation: float = 0.10,
    inflation_std: float = 0.035,
    seed: Optional[int] = 42,
    override_retirement_age: Optional[int] = None,
    override_monthly_expenses: Optional[float] = None,
    lump_sum_inflow: float = 0.0,
    lump_sum_outflow: float = 0.0,
    lump_sum_age: Optional[int] = None,
) -> MonteCarloResult:
    """
    Executes a vectorized 1,000-trial stochastic simulation over the retirement horizon.
    Models market volatility and inflation variance simultaneously.
    """
    if seed is not None:
        np.random.seed(seed)

    ret_age = override_retirement_age if override_retirement_age is not None else client.retirement_age
    horizon_age = client.planning_horizon_age
    horizon_years = max(1, horizon_age - ret_age)

    # Initial investable capital
    starting_capital = max(0.0, health.net_investable_retirement_capital_pkr)

    # Baseline monthly expenses and guaranteed monthly income
    base_monthly_expenses = (
        override_monthly_expenses
        if override_monthly_expenses is not None
        else (financial_profile.expenses.expected_retirement_expenses_monthly or financial_profile.expenses.essential_expenses_monthly)
    )
    annual_base_expenses = base_monthly_expenses * 12.0
    annual_guaranteed_income = health.guaranteed_monthly_retirement_income_pkr * 12.0

    if starting_capital <= 0.0 and (annual_base_expenses > annual_guaranteed_income):
        # Immediate depletion
        empty_points = [
            MonteCarloTrajectoryPoint(age=ret_age + yr, year_index=yr, p10_capital_pkr=0.0, p50_capital_pkr=0.0, p90_capital_pkr=0.0)
            for yr in range(horizon_years + 1)
        ]
        return MonteCarloResult(
            trials_count=trials_count,
            probability_of_success_pct=0.0,
            median_depletion_age=ret_age,
            median_ending_capital_pkr=0.0,
            p10_ending_capital_pkr=0.0,
            p90_ending_capital_pkr=0.0,
            percentile_trajectories=empty_points,
            confidence_verdict="Immediate Depletion (Zero Investable Reserves)",
        )

    # Generate random returns & inflation for all trials: shape (trials_count, horizon_years)
    # Clamp inflation >= 0.02 and returns >= -0.30 to represent realistic Pakistani macroeconomic boundaries
    raw_returns = np.random.normal(mean_return, return_std, size=(trials_count, horizon_years))
    returns_matrix = np.clip(raw_returns, -0.30, 0.40)

    raw_inflation = np.random.normal(mean_inflation, inflation_std, size=(trials_count, horizon_years))
    inflation_matrix = np.clip(raw_inflation, 0.02, 0.35)

    # Trajectory matrix: shape (trials_count, horizon_years + 1)
    capital_matrix = np.zeros((trials_count, horizon_years + 1), dtype=np.float64)
    capital_matrix[:, 0] = starting_capital

    # Track cumulative inflation index per trial
    cum_inflation_factors = np.ones(trials_count, dtype=np.float64)
    depletion_ages = np.full(trials_count, horizon_age + 1, dtype=np.int32)

    for yr in range(horizon_years):
        current_age = ret_age + yr
        current_cap = capital_matrix[:, yr]

        # 1. Growth on existing capital
        returns_this_yr = returns_matrix[:, yr]
        growth = np.where(current_cap > 0, current_cap * returns_this_yr, 0.0)
        cap_after_growth = current_cap + growth

        # 2. Cumulative inflation compounding on living expenses
        cum_inflation_factors *= (1.0 + inflation_matrix[:, yr])
        inflated_expenses = annual_base_expenses * cum_inflation_factors

        # 3. Guaranteed income (e.g. government pension)
        net_withdrawal = np.maximum(0.0, inflated_expenses - annual_guaranteed_income)

        # 4. Optional lump-sum cash events (e.g. inheritance or medical shock)
        if lump_sum_age is not None and current_age == lump_sum_age:
            net_withdrawal = net_withdrawal - lump_sum_inflow + lump_sum_outflow

        ending_cap = cap_after_growth - net_withdrawal
        ending_cap = np.maximum(0.0, ending_cap)
        capital_matrix[:, yr + 1] = ending_cap

        # Record depletion age on first year capital hits 0
        depleted_mask = (ending_cap <= 0.0) & (depletion_ages > horizon_age)
        depletion_ages = np.where(depleted_mask, current_age, depletion_ages)

    # Calculate Probability of Success (% where capital survived through horizon_age)
    survived_mask = capital_matrix[:, -1] > 0.0
    prob_success = float(np.mean(survived_mask) * 100.0)

    # Percentiles for every single year
    p10_curve = np.percentile(capital_matrix, 10, axis=0)
    p50_curve = np.percentile(capital_matrix, 50, axis=0)
    p90_curve = np.percentile(capital_matrix, 90, axis=0)

    trajectory_points = [
        MonteCarloTrajectoryPoint(
            age=ret_age + yr,
            year_index=yr,
            p10_capital_pkr=round(float(p10_curve[yr]), 2),
            p50_capital_pkr=round(float(p50_curve[yr]), 2),
            p90_capital_pkr=round(float(p90_curve[yr]), 2),
        )
        for yr in range(horizon_years + 1)
    ]

    # Median depletion age calculation
    median_depletion: Optional[int] = None
    depleted_runs = depletion_ages[depletion_ages <= horizon_age]
    if len(depleted_runs) > (trials_count * 0.5):
        median_depletion = int(np.median(depleted_runs))

    # Confidence verdict
    if prob_success >= 85.0:
        verdict = "High Confidence (Resilient Plan)"
    elif prob_success >= 65.0:
        verdict = "Moderate Confidence (Subject to Inflation Sensitivity)"
    elif prob_success >= 40.0:
        verdict = "Vulnerable (Significant Depletion Risk)"
    else:
        verdict = "Critical Underfunding (High Probability of Exhaustion)"

    return MonteCarloResult(
        trials_count=trials_count,
        probability_of_success_pct=round(prob_success, 1),
        median_depletion_age=median_depletion,
        median_ending_capital_pkr=round(float(p50_curve[-1]), 2),
        p10_ending_capital_pkr=round(float(p10_curve[-1]), 2),
        p90_ending_capital_pkr=round(float(p90_curve[-1]), 2),
        percentile_trajectories=trajectory_points,
        confidence_verdict=verdict,
    )
