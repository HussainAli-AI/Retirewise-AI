"""High-level AI report narrative and audit generator."""
import json
from typing import Dict, Any
from models.assessment import SuitabilityAssessmentResult
from models.financial_profile import FinancialProfile
from ai.llm_client import LLMClient
from ai.prompts import (
    RESULT_EXPLANATION_PROMPT,
    MISSING_DATA_AUDIT_PROMPT,
)


class AIReportNarrativeGenerator:
    """Coordinates AI-driven explanations strictly derived from structured engine data."""

    def __init__(self, llm_client: LLMClient):
        self.client = llm_client

    @staticmethod
    def _condense_assessment_payload(assessment: SuitabilityAssessmentResult) -> Dict[str, Any]:
        """Creates a token-efficient structured payload omitting bulky year-by-year cashflow arrays."""
        return {
            "assessment_id": assessment.assessment_id,
            "client_name": assessment.client_name,
            "financial_health": {
                "net_worth_pkr": round(assessment.financial_health.net_worth_pkr, 2),
                "liquid_assets_pkr": round(assessment.financial_health.liquid_assets_pkr, 2),
                "net_investable_retirement_capital_pkr": round(assessment.financial_health.net_investable_retirement_capital_pkr, 2),
                "current_monthly_income_pkr": round(assessment.financial_health.current_monthly_income_pkr, 2),
                "current_monthly_expenses_pkr": round(assessment.financial_health.current_monthly_expenses_pkr, 2),
                "projected_monthly_retirement_expenses_pkr": round(assessment.financial_health.projected_monthly_retirement_expenses_pkr, 2),
                "guaranteed_monthly_retirement_income_pkr": round(assessment.financial_health.guaranteed_monthly_retirement_income_pkr, 2),
                "monthly_retirement_income_gap_pkr": round(assessment.financial_health.monthly_retirement_income_gap_pkr, 2),
                "emergency_reserve_adequacy_ratio": round(assessment.financial_health.emergency_reserve_adequacy_ratio, 2),
                "annual_withdrawal_rate_pct": round(assessment.financial_health.annual_withdrawal_rate_pct, 2),
            },
            "risk_tolerance": {
                "score": round(assessment.risk_tolerance.normalized_score, 1),
                "category": assessment.risk_tolerance.category.value if hasattr(assessment.risk_tolerance.category, 'value') else str(assessment.risk_tolerance.category),
                "summary": assessment.risk_tolerance.summary,
            },
            "capacity_for_loss": {
                "score": round(assessment.capacity_for_loss.capacity_score, 1),
                "category": assessment.capacity_for_loss.category.value if hasattr(assessment.capacity_for_loss.category, 'value') else str(assessment.capacity_for_loss.category),
                "income_dependency_pct": round(assessment.capacity_for_loss.income_dependency_pct, 1),
                "liquid_emergency_months": round(assessment.capacity_for_loss.liquid_emergency_months, 1),
                "debt_to_assets_pct": round(assessment.capacity_for_loss.debt_to_assets_pct, 1),
                "key_drivers": assessment.capacity_for_loss.key_drivers,
                "warnings": assessment.capacity_for_loss.warnings,
            },
            "base_case_projection": {
                "sustainability_years": assessment.retirement_projection.sustainability_years,
                "capital_depletion_age": assessment.retirement_projection.capital_depletion_age,
                "is_sustainable_through_horizon": assessment.retirement_projection.is_sustainable_through_horizon,
                "ending_capital_at_horizon_pkr": round(assessment.retirement_projection.ending_capital_at_horizon_pkr, 2),
                "annual_withdrawal_rate_initial_pct": round(assessment.retirement_projection.annual_withdrawal_rate_initial_pct, 2),
                "summary_verdict": assessment.retirement_projection.summary_verdict,
            },
            "stress_test_scenarios_summary": [
                {
                    "scenario_name": s.scenario_name,
                    "annual_inflation_rate": s.annual_inflation_rate,
                    "annual_return_rate": s.annual_return_rate,
                    "sustainability_years": s.sustainability_years,
                    "capital_depletion_age": s.capital_depletion_age,
                    "is_sustainable": s.is_sustainable,
                    "ending_capital_pkr": round(s.ending_capital_pkr, 2),
                    "key_vulnerability": s.key_vulnerability,
                }
                for s in assessment.scenarios
            ],
            "has_suitability_conflict": assessment.has_suitability_conflict,
            "suitability_summary": assessment.suitability_summary,
            "conflict_warnings": [
                {
                    "severity": w.severity.value if hasattr(w.severity, 'value') else str(w.severity),
                    "title": w.title,
                    "description": w.description,
                    "adviser_action": w.adviser_action,
                }
                for w in assessment.conflict_warnings
            ],
        }

    def generate_assessment_explanation(self, assessment: SuitabilityAssessmentResult) -> str:
        """Generates comprehensive plain-language narrative for an assessment."""
        condensed = self._condense_assessment_payload(assessment)
        prompt = RESULT_EXPLANATION_PROMPT.format(
            client_name=assessment.client_name,
            assessment_json=json.dumps(condensed, indent=2),
        )
        return self.client.generate_text(prompt)

    def audit_missing_or_contradictory_data(self, profile: FinancialProfile) -> str:
        """Audits fact-find profile for omissions, zero-value risks, and inconsistencies."""
        prompt = MISSING_DATA_AUDIT_PROMPT.format(
            profile_json=profile.model_dump_json(indent=2),
        )
        return self.client.generate_text(prompt)
