"""Unit tests for input validation."""
import pytest
from models.client import ClientProfile, MaritalStatus
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)
from core.validation import validate_client_and_profile


@pytest.fixture
def valid_client_and_profile():
    client = ClientProfile(
        client_id="TEST-001",
        name="Test User",
        current_age=50,
        retirement_age=60,
        planning_horizon_age=85,
        marital_status=MaritalStatus.MARRIED,
        dependents_count=2,
    )
    profile = FinancialProfile(
        client_id=client.client_id,
        income=IncomeBreakdown(salary_monthly=200_000.0),
        expenses=ExpenseBreakdown(
            essential_expenses_monthly=80_000.0,
            expected_retirement_expenses_monthly=120_000.0,
        ),
        assets=AssetBreakdown(cash_and_savings=2_000_000.0),
        liabilities=LiabilityBreakdown(),
        goals=RetirementGoals(
            target_monthly_income_pkr=120_000.0,
            expected_annual_inflation_rate=0.08,
            expected_annual_investment_return=0.11,
        ),
    )
    return client, profile


def test_valid_profile_passes(valid_client_and_profile):
    client, profile = valid_client_and_profile
    is_valid, errors = validate_client_and_profile(client, profile)
    assert is_valid is True
    assert len(errors) == 0


def test_invalid_horizon_less_than_current_age(valid_client_and_profile):
    client, profile = valid_client_and_profile
    client.planning_horizon_age = 45  # less than current_age 50
    is_valid, errors = validate_client_and_profile(client, profile)
    assert is_valid is False
    assert any("Planning horizon age" in err for err in errors)


def test_invalid_negative_expenses(valid_client_and_profile):
    client, profile = valid_client_and_profile
    profile.expenses.essential_expenses_monthly = -5000.0
    is_valid, errors = validate_client_and_profile(client, profile)
    assert is_valid is False
    assert any("Essential monthly expenses cannot be negative" in err for err in errors)


def test_invalid_unrealistic_inflation(valid_client_and_profile):
    client, profile = valid_client_and_profile
    profile.goals.expected_annual_inflation_rate = 0.55  # 55%
    is_valid, errors = validate_client_and_profile(client, profile)
    assert is_valid is False
    assert any("Inflation rate must be between" in err for err in errors)
