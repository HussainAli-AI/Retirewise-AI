"""Input validation and sanity check engine."""
from typing import List, Tuple
from models.client import ClientProfile
from models.financial_profile import FinancialProfile


class ValidationError(Exception):
    """Raised when financial or demographic inputs fail validation."""
    def __init__(self, errors: List[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


def validate_client_and_profile(client: ClientProfile, profile: FinancialProfile) -> Tuple[bool, List[str]]:
    """
    Validates logical consistency between demographic parameters and financial profiles.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    # 1. Demographic sanity
    if client.current_age < 18:
        errors.append("Current age cannot be under 18.")
    if client.current_age > 110:
        errors.append("Current age exceeds realistic boundary (110).")
    if client.planning_horizon_age <= client.current_age:
        errors.append(f"Planning horizon age ({client.planning_horizon_age}) must be strictly greater than current age ({client.current_age}).")
    if client.planning_horizon_age <= client.retirement_age:
        errors.append(f"Planning horizon age ({client.planning_horizon_age}) must be strictly greater than retirement age ({client.retirement_age}).")

    # 2. Financial non-negativity
    if profile.expenses.essential_expenses_monthly < 0:
        errors.append("Essential monthly expenses cannot be negative.")
    if profile.expenses.expected_retirement_expenses_monthly < 0:
        errors.append("Expected retirement monthly expenses cannot be negative.")
    if profile.goals.target_monthly_income_pkr < 0:
        errors.append("Target retirement monthly income cannot be negative.")

    # 3. Minimum baseline checks
    if profile.expenses.expected_retirement_expenses_monthly == 0 and profile.goals.target_monthly_income_pkr == 0:
        errors.append("Both expected retirement expenses and target monthly income cannot be zero simultaneously.")

    # 4. Economic sanity
    if profile.goals.expected_annual_inflation_rate < 0 or profile.goals.expected_annual_inflation_rate > 0.40:
        errors.append("Inflation rate must be between 0% and 40% per annum.")
    if profile.goals.expected_annual_investment_return < -0.20 or profile.goals.expected_annual_investment_return > 0.50:
        errors.append("Expected investment return must be between -20% and 50% per annum.")

    return len(errors) == 0, errors
