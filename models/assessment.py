"""Structured results and assessment models."""
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RiskCategory(str, Enum):
    VERY_CONSERVATIVE = "Very Conservative"
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    GROWTH = "Growth"
    AGGRESSIVE = "Aggressive"


class CapacityCategory(str, Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class WarningSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class ConflictWarning(BaseModel):
    """Suitability warning or conflict flag."""
    code: str
    severity: WarningSeverity
    title: str
    description: str
    adviser_action: str


class RiskToleranceResult(BaseModel):
    """Attitudinal risk tolerance questionnaire assessment."""
    raw_score: float = Field(..., ge=0.0, le=100.0)
    normalized_score: float = Field(..., ge=0.0, le=100.0)
    category: RiskCategory
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    summary: str


class CapacityForLossResult(BaseModel):
    """Objective capacity for loss calculation."""
    capacity_score: float = Field(..., ge=0.0, le=100.0)
    category: CapacityCategory
    income_dependency_pct: float = Field(..., ge=0.0, description="% of retirement expenses reliant on portfolio withdrawals")
    liquid_emergency_months: float = Field(..., ge=0.0, description="Months of essential expenses covered by liquid assets")
    debt_to_assets_pct: float = Field(..., ge=0.0, description="Total liabilities as % of total assets")
    key_drivers: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class FinancialHealthMetrics(BaseModel):
    """Deterministic snapshot of financial health."""
    total_assets_pkr: float
    total_liabilities_pkr: float
    net_worth_pkr: float
    liquid_assets_pkr: float
    net_investable_retirement_capital_pkr: float
    current_monthly_income_pkr: float
    current_monthly_expenses_pkr: float
    current_monthly_surplus_pkr: float
    guaranteed_monthly_retirement_income_pkr: float
    projected_monthly_retirement_expenses_pkr: float
    monthly_retirement_income_gap_pkr: float
    emergency_reserve_adequacy_ratio: float
    annual_withdrawal_rate_pct: float


class CashFlowYearProjection(BaseModel):
    """Single year snapshot in retirement simulation."""
    year_index: int
    client_age: int
    starting_capital_pkr: float
    investment_growth_pkr: float
    guaranteed_income_pkr: float
    total_expenses_pkr: float
    net_withdrawal_pkr: float
    ending_capital_pkr: float
    is_depleted: bool = False


class RetirementProjectionResult(BaseModel):
    """Simulation trajectory over the planning horizon."""
    starting_capital_pkr: float
    annual_inflation_rate: float
    annual_return_rate: float
    sustainability_years: int
    capital_depletion_age: Optional[int] = None
    is_sustainable_through_horizon: bool
    ending_capital_at_horizon_pkr: float
    yearly_trajectory: List[CashFlowYearProjection]
    annual_withdrawal_rate_initial_pct: float
    summary_verdict: str


class ScenarioType(str, Enum):
    BASE_CASE = "Base Case"
    HIGH_INFLATION = "High Inflation Shock"
    MARKET_STRESS = "Early Market Drawdown"
    MEDICAL_SHOCK = "Major Medical Expense Shock"
    EARLY_RETIREMENT = "Early Retirement Shock"


class ScenarioResult(BaseModel):
    """Result of running a stress-test scenario."""
    scenario_type: ScenarioType
    scenario_name: str
    description: str
    annual_inflation_rate: float
    annual_return_rate: float
    sustainability_years: int
    capital_depletion_age: Optional[int]
    is_sustainable: bool
    ending_capital_pkr: float
    key_vulnerability: str
    yearly_trajectory: List[CashFlowYearProjection] = Field(default_factory=list)


class SuitabilityAssessmentResult(BaseModel):
    """Comprehensive aggregated assessment payload."""
    assessment_id: str
    client_id: str
    client_name: str
    created_at: str
    financial_health: FinancialHealthMetrics
    risk_tolerance: RiskToleranceResult
    capacity_for_loss: CapacityForLossResult
    retirement_projection: RetirementProjectionResult
    scenarios: List[ScenarioResult]
    conflict_warnings: List[ConflictWarning]
    has_suitability_conflict: bool
    suitability_summary: str
    ai_narrative: Optional[Dict[str, Any]] = None
