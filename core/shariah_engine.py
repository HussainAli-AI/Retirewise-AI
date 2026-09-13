"""Pakistan Shariah & conventional asset allocation engine with Section 63 tax credit optimizer."""
from typing import List, Dict, Any
from models.assessment import (
    CapacityCategory,
    RiskCategory,
    ShariahAllocationResult,
    AssetAllocationItem,
    FinancialHealthMetrics,
    CapacityForLossResult,
    RiskToleranceResult,
)
from models.client import ClientProfile
from models.financial_profile import FinancialProfile


# Hard equity ceilings dictated by objective Capacity for Loss
CAPACITY_EQUITY_CEILINGS: Dict[CapacityCategory, float] = {
    CapacityCategory.VERY_LOW: 10.0,
    CapacityCategory.LOW: 20.0,
    CapacityCategory.MODERATE: 45.0,
    CapacityCategory.HIGH: 65.0,
    CapacityCategory.VERY_HIGH: 80.0,
}

# Ideal equity weights dictated by attitudinal Risk Tolerance
RISK_TOLERANCE_EQUITY_TARGETS: Dict[RiskCategory, float] = {
    RiskCategory.VERY_CONSERVATIVE: 5.0,
    RiskCategory.CONSERVATIVE: 15.0,
    RiskCategory.MODERATE: 35.0,
    RiskCategory.GROWTH: 60.0,
    RiskCategory.AGGRESSIVE: 80.0,
}


def calculate_pakistan_asset_allocation(
    client: ClientProfile,
    financial_profile: FinancialProfile,
    health: FinancialHealthMetrics,
    capacity: CapacityForLossResult,
    risk: RiskToleranceResult,
    is_shariah_mode: bool = True,
) -> ShariahAllocationResult:
    """
    Computes an asset allocation tailored to Pakistani financial markets.
    Strictly enforces Capacity-for-Loss ceilings over psychological risk appetite.
    Calculates Section 63 Income Tax Ordinance (ITO) voluntary pension tax savings.
    """
    investable_capital = max(0.0, health.net_investable_retirement_capital_pkr)
    equity_ceiling = CAPACITY_EQUITY_CEILINGS.get(capacity.category, 20.0)
    risk_target = RISK_TOLERANCE_EQUITY_TARGETS.get(risk.category, 20.0)

    # Effective equity percentage: cannot exceed Capacity ceiling
    recommended_equity_pct = min(equity_ceiling, risk_target)

    # Cash / Emergency Buffer percentage (minimum 10% for liquidity safety)
    cash_pct = max(10.0, min(30.0, 100.0 - (health.emergency_reserve_adequacy_ratio * 5.0)))
    if capacity.category in [CapacityCategory.VERY_LOW, CapacityCategory.LOW]:
        cash_pct = max(25.0, cash_pct)

    # Gold / Inflation Hedge: 5% - 10%
    gold_pct = 7.5

    # Remainder to Sovereign Sukuks / Fixed Income
    fixed_income_pct = max(0.0, 100.0 - recommended_equity_pct - cash_pct - gold_pct)

    allocations: List[AssetAllocationItem] = []

    if is_shariah_mode:
        # 1. Sovereign Ijara Sukuks & Islamic Income Funds
        allocations.append(
            AssetAllocationItem(
                asset_class="Sovereign Ijara Sukuks & Islamic Fixed Income",
                recommended_pct=round(fixed_income_pct, 1),
                allocation_amount_pkr=round(investable_capital * (fixed_income_pct / 100.0), 2),
                instrument_examples=["GOP Ijara Sukuks (1-Yr, 3-Yr, 5-Yr)", "Al-Ameen Islamic Sovereign Fund", "Meezan Sovereign Fund"],
                is_shariah_compliant=True,
                rationale="Provides predictable, Shariah-compliant rental income yields with sovereign default protection.",
            )
        )
        # 2. Shariah Equities (KMI-30)
        allocations.append(
            AssetAllocationItem(
                asset_class="Shariah Equities (KMI-30)",
                recommended_pct=round(recommended_equity_pct, 1),
                allocation_amount_pkr=round(investable_capital * (recommended_equity_pct / 100.0), 2),
                instrument_examples=["Meezan Islamic Fund (MIF)", "Al-Ameen Shariah Stock Fund", "KMI-30 ETF"],
                is_shariah_compliant=True,
                rationale=f"Long-term inflation hedge capped at {equity_ceiling}% to honor objective capacity for loss.",
            )
        )
        # 3. Islamic Money Market & Cash Reserves
        allocations.append(
            AssetAllocationItem(
                asset_class="Islamic Money Market & Bank TDRs",
                recommended_pct=round(cash_pct, 1),
                allocation_amount_pkr=round(investable_capital * (cash_pct / 100.0), 2),
                instrument_examples=["Meezan Daily Income Fund (MDIP)", "Faysal Islamic Cash Fund", "Islamic Bank TDRs"],
                is_shariah_compliant=True,
                rationale="Ensures liquid reserves for routine withdrawals without having to sell growth assets during market dips.",
            )
        )
        # 4. Physical Gold / Commodity
        allocations.append(
            AssetAllocationItem(
                asset_class="Physical Gold / Commodities",
                recommended_pct=round(gold_pct, 1),
                allocation_amount_pkr=round(investable_capital * (gold_pct / 100.0), 2),
                instrument_examples=["Meezan Gold Fund (MGF)", "Physical 24K Certified Bullion Bars"],
                is_shariah_compliant=True,
                rationale="Hedging local currency rupee depreciation against USD and global geopolitical risk.",
            )
        )
    else:
        # Conventional Allocations
        allocations.append(
            AssetAllocationItem(
                asset_class="Sovereign Bonds (PIBs & T-Bills)",
                recommended_pct=round(fixed_income_pct, 1),
                allocation_amount_pkr=round(investable_capital * (fixed_income_pct / 100.0), 2),
                instrument_examples=["Pakistan Investment Bonds (PIBs)", "Treasury Bills (T-Bills)", "Behbood Savings Certificates"],
                is_shariah_compliant=False,
                rationale="Core fixed-income sovereign yield matching baseline spending needs.",
            )
        )
        allocations.append(
            AssetAllocationItem(
                asset_class="Equities (KSE-100)",
                recommended_pct=round(recommended_equity_pct, 1),
                allocation_amount_pkr=round(investable_capital * (recommended_equity_pct / 100.0), 2),
                instrument_examples=["KSE-100 Index Tracker Funds", "Large-Cap Dividend Paying Stocks"],
                is_shariah_compliant=False,
                rationale=f"Growth component strictly limited to {equity_ceiling}% based on risk capacity.",
            )
        )
        allocations.append(
            AssetAllocationItem(
                asset_class="Conventional Money Market & Deposits",
                recommended_pct=round(cash_pct, 1),
                allocation_amount_pkr=round(investable_capital * (cash_pct / 100.0), 2),
                instrument_examples=["Cash Management Funds", "Commercial Bank Term Deposits"],
                is_shariah_compliant=False,
                rationale="Immediate liquid reserve covering emergency runway.",
            )
        )
        allocations.append(
            AssetAllocationItem(
                asset_class="Gold / Commodities",
                recommended_pct=round(gold_pct, 1),
                allocation_amount_pkr=round(investable_capital * (gold_pct / 100.0), 2),
                instrument_examples=["PMEX Gold Futures", "Physical Gold"],
                is_shariah_compliant=False,
                rationale="Store of value against PKR devaluation.",
            )
        )

    # VPS Sub-Fund Breakdown mapping
    vps_equity = recommended_equity_pct
    vps_debt = fixed_income_pct
    vps_money_market = 100.0 - vps_equity - vps_debt

    # Section 63 Tax Credit Optimization (Income Tax Ordinance 2001)
    # Allows tax rebate on contribution up to 20% of taxable income + 2% per year of age over 40 (max 50% eligible)
    annual_salary = financial_profile.income.salary_monthly * 12.0
    age_bonus_pct = max(0, min(30, (client.current_age - 40) * 2)) if client.current_age > 40 else 0
    max_eligible_contribution_pct = min(50.0, 20.0 + age_bonus_pct)
    max_tax_deductible_vps_contribution = annual_salary * (max_eligible_contribution_pct / 100.0)

    # Average effective marginal tax rate estimate in Pakistan (~15-20% for typical executive salary bracket)
    effective_marginal_tax_rate = 0.20
    estimated_tax_savings = round(max_tax_deductible_vps_contribution * effective_marginal_tax_rate, 2)

    tax_notes = (
        f"Under Section 63 of the Income Tax Ordinance, contributions to Voluntary Pension Schemes (VPS) qualify for a direct "
        f"tax credit on up to {max_eligible_contribution_pct:.0f}% of annual taxable salary (including age bonus for age {client.current_age}). "
        f"Contributing PKR {max_tax_deductible_vps_contribution:,.0f} annually can yield up to ~PKR {estimated_tax_savings:,.0f} in income tax rebates."
    )

    governing_rationale = (
        f"Allocation governed by Objective Capacity for Loss category '{capacity.category.value}' with an equity ceiling of {equity_ceiling:.0f}%. "
        f"Psychological risk appetite target was {risk_target:.0f}%. "
        + ("Appetite safely accommodated." if risk_target <= equity_ceiling else f"Appetite curbed from {risk_target:.0f}% down to {equity_ceiling:.0f}% to protect essential living capital.")
    )

    return ShariahAllocationResult(
        is_shariah_mode=is_shariah_mode,
        capacity_equity_ceiling_pct=equity_ceiling,
        recommended_allocations=allocations,
        vps_equity_sub_fund_pct=round(vps_equity, 1),
        vps_debt_sub_fund_pct=round(vps_debt, 1),
        vps_money_market_sub_fund_pct=round(vps_money_market, 1),
        estimated_annual_tax_credit_pkr=estimated_tax_savings,
        tax_optimization_notes=tax_notes,
        governing_rationale=governing_rationale,
    )
