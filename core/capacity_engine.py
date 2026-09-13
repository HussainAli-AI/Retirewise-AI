"""Objective Capacity for Loss calculation and Suitability Conflict Engine."""
from typing import List, Tuple
from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import (
    CapacityCategory,
    CapacityForLossResult,
    ConflictWarning,
    WarningSeverity,
    RiskToleranceResult,
    RiskCategory,
)


def calculate_capacity_for_loss(client: ClientProfile, profile: FinancialProfile) -> CapacityForLossResult:
    """
    Evaluates client's objective financial capacity to absorb market losses
    without jeopardizing their baseline standard of living.
    """
    key_drivers: List[str] = []
    warnings: List[str] = []

    ret_expenses = max(1.0, profile.expenses.expected_retirement_expenses_monthly)
    guaranteed_income = profile.income.guaranteed_passive_retirement_income

    # 1. Income Dependency Factor (0 - 30 points)
    # Higher dependency on capital withdrawals reduces capacity for loss
    income_dependency_ratio = max(0.0, min(1.0, (ret_expenses - guaranteed_income) / ret_expenses))
    income_dependency_pct = round(income_dependency_ratio * 100.0, 1)

    # If dependency is 0% (guaranteed income covers all expenses), max 30 points
    # If dependency is 100% (zero guaranteed income), 0 points
    dependency_score = (1.0 - income_dependency_ratio) * 30.0
    if income_dependency_pct > 75.0:
        key_drivers.append(f"High income dependency ({income_dependency_pct}% of living expenses require capital withdrawals).")
    else:
        key_drivers.append(f"Low-to-moderate income dependency ({income_dependency_pct}%).")

    # 2. Liquid Emergency Reserve Buffer (0 - 25 points)
    # Months of essential expenses in liquid cash/investments
    essential_exp = max(1.0, profile.expenses.essential_expenses_monthly)
    liquid_reserve_months = profile.assets.total_liquid_assets / essential_exp
    # 12+ months provides full 25 points
    reserve_score = min(25.0, (liquid_reserve_months / 12.0) * 25.0)

    if liquid_reserve_months < 6.0:
        warnings.append(f"Liquid emergency reserves ({liquid_reserve_months:.1f} months) are below recommended 6-month threshold.")
        key_drivers.append(f"Inadequate liquid cushion ({liquid_reserve_months:.1f} months).")
    else:
        key_drivers.append(f"Robust liquid reserves ({liquid_reserve_months:.1f} months).")

    # 3. Solvency & Debt Burden (0 - 20 points)
    total_assets = max(1.0, profile.assets.total_assets)
    total_liabilities = profile.liabilities.total_liabilities
    debt_to_assets_ratio = total_liabilities / total_assets
    debt_to_assets_pct = round(debt_to_assets_ratio * 100.0, 1)

    # 0% debt -> 20 points; >= 50% debt -> 0 points
    debt_score = max(0.0, 20.0 - (debt_to_assets_ratio * 40.0))
    if debt_to_assets_pct > 25.0:
        warnings.append(f"Elevated debt ratio ({debt_to_assets_pct}% of total assets).")
        key_drivers.append(f"Significant debt obligations ({debt_to_assets_pct}%).")
    else:
        key_drivers.append("Low leverage / minimal debt encumbrance.")

    # 4. Human Capital / Time to Replace Losses (0 - 15 points)
    # If client has years until retirement and active salary, they can recover from losses
    if not client.is_already_retired:
        years_left = client.years_to_retirement
        time_score = min(15.0, (years_left / 10.0) * 15.0)
        key_drivers.append(f"{years_left} pre-retirement working years remaining to absorb market volatility.")
    else:
        # Already retired: capacity to replace loss via employment is zero
        time_score = 0.0
        key_drivers.append("Client is currently retired with no active employment earnings to replenish losses.")

    # 5. Dependent Drag Factor (0 - 10 points)
    # Dependents increase essential financial fragility
    dep_count = client.dependents_count
    if dep_count == 0:
        dep_score = 10.0
    elif dep_count <= 2:
        dep_score = 6.0
    elif dep_count <= 4:
        dep_score = 3.0
    else:
        dep_score = 0.0
        warnings.append(f"High number of dependents ({dep_count}) places sustained demands on capital.")

    # Total score calculation (0 - 100)
    raw_capacity = dependency_score + reserve_score + debt_score + time_score + dep_score
    capacity_score = round(max(0.0, min(100.0, raw_capacity)), 1)

    # Categorize
    if capacity_score <= 25.0:
        category = CapacityCategory.VERY_LOW
    elif capacity_score <= 45.0:
        category = CapacityCategory.LOW
    elif capacity_score <= 65.0:
        category = CapacityCategory.MODERATE
    elif capacity_score <= 85.0:
        category = CapacityCategory.HIGH
    else:
        category = CapacityCategory.VERY_HIGH

    return CapacityForLossResult(
        capacity_score=capacity_score,
        category=category,
        income_dependency_pct=income_dependency_pct,
        liquid_emergency_months=round(liquid_reserve_months, 1),
        debt_to_assets_pct=debt_to_assets_pct,
        key_drivers=key_drivers,
        warnings=warnings,
    )


def evaluate_suitability_conflicts(
    risk_result: RiskToleranceResult,
    capacity_result: CapacityForLossResult,
    profile: FinancialProfile,
    client: ClientProfile,
) -> Tuple[List[ConflictWarning], bool]:
    """
    Evaluates mismatches between Risk Tolerance, Capacity for Loss, and Cash Flow constraints.
    Returns (list_of_warnings, has_suitability_conflict).
    """
    warnings: List[ConflictWarning] = []
    has_suitability_conflict = False

    # 1. Primary Conflict: High Risk Tolerance vs. Low Capacity for Loss
    is_high_risk = risk_result.category in [RiskCategory.GROWTH, RiskCategory.AGGRESSIVE]
    is_low_capacity = capacity_result.category in [CapacityCategory.VERY_LOW, CapacityCategory.LOW]

    if is_high_risk and is_low_capacity:
        has_suitability_conflict = True
        warnings.append(
            ConflictWarning(
                code="SUITABILITY_RISK_CAPACITY_MISMATCH",
                severity=WarningSeverity.CRITICAL,
                title="Critical Suitability Conflict: Risk Attitude Exceeds Financial Capacity",
                description=(
                    f"Client exhibits a {risk_result.category.value} risk tolerance, but has a "
                    f"{capacity_result.category.value} capacity for loss (Score: {capacity_result.capacity_score}/100). "
                    "Their financial position cannot withstand the drawdowns inherent to their psychological preference."
                ),
                adviser_action=(
                    "MANDATORY ADVISER INTERVENTION: Base asset allocation on objective Capacity for Loss, "
                    "not subjective Risk Tolerance. Counsel client on the danger of capital depletion."
                ),
            )
        )

    # 2. Extreme Income Dependency Warning
    if capacity_result.income_dependency_pct > 80.0 and client.is_already_retired:
        warnings.append(
            ConflictWarning(
                code="HIGH_RETIREMENT_DEPENDENCY",
                severity=WarningSeverity.WARNING,
                title="Severe Retirement Capital Dependency",
                description=(
                    f"{capacity_result.income_dependency_pct}% of monthly retirement expenditure depends on portfolio withdrawals, "
                    "with negligible guaranteed pension or rental income."
                ),
                adviser_action="Evaluate annuitization, VPS pension drawdowns, or allocating to stable dividend/Sukuk income funds.",
            )
        )

    # 3. Emergency Liquidity Shortfall Warning
    if capacity_result.liquid_emergency_months < 3.0:
        warnings.append(
            ConflictWarning(
                code="LIQUIDITY_DEFICIT",
                severity=WarningSeverity.CRITICAL,
                title="Severe Liquidity Deficit",
                description=(
                    f"Client holds only {capacity_result.liquid_emergency_months} months of essential expenses in liquid assets, "
                    "well below the safety threshold of 6 months."
                ),
                adviser_action="Build liquid emergency cash buffers immediately prior to committing any capital to long-term assets.",
            )
        )

    # 4. Debt Encumbrance Warning at or near retirement
    if capacity_result.debt_to_assets_pct > 30.0 and (client.is_already_retired or client.years_to_retirement <= 3):
        warnings.append(
            ConflictWarning(
                code="RETIREMENT_DEBT_BURDEN",
                severity=WarningSeverity.WARNING,
                title="Elevated Debt Burden Approaching Retirement",
                description=(
                    f"Outstanding debt represents {capacity_result.debt_to_assets_pct}% of total assets. "
                    "Debt service payments in retirement create a severe cash drag."
                ),
                adviser_action="Formulate a debt pre-payment strategy using provident fund or gratuity lump sums before retiring.",
            )
        )

    return warnings, has_suitability_conflict
