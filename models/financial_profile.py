"""Financial profile and Fact-Find entities in PKR."""
from pydantic import BaseModel, Field


class IncomeBreakdown(BaseModel):
    """Monthly recurring income streams in PKR."""
    salary_monthly: float = Field(0.0, ge=0.0, description="Pre-retirement employment income")
    pension_monthly: float = Field(0.0, ge=0.0, description="Guaranteed government or corporate pension")
    rental_income_monthly: float = Field(0.0, ge=0.0, description="Net rental income from properties")
    business_income_monthly: float = Field(0.0, ge=0.0, description="Recurring business dividends/profits")
    other_income_monthly: float = Field(0.0, ge=0.0, description="Other recurring income (remittances, annuities, etc.)")

    @property
    def total_monthly_income(self) -> float:
        return (
            self.salary_monthly
            + self.pension_monthly
            + self.rental_income_monthly
            + self.business_income_monthly
            + self.other_income_monthly
        )

    @property
    def guaranteed_passive_retirement_income(self) -> float:
        """Guaranteed income streams that persist into retirement without depleting capital."""
        return self.pension_monthly + self.rental_income_monthly + self.other_income_monthly


class ExpenseBreakdown(BaseModel):
    """Monthly expenses in PKR."""
    essential_expenses_monthly: float = Field(..., ge=0.0, description="Utilities, food, basic necessities, household maintenance")
    discretionary_expenses_monthly: float = Field(0.0, ge=0.0, description="Travel, dining, entertainment, non-essential lifestyle")
    healthcare_monthly: float = Field(0.0, ge=0.0, description="Routine medical checkups, medicines, health insurance")
    debt_service_monthly: float = Field(0.0, ge=0.0, description="Monthly EMIs, loan repayments, credit obligations")
    expected_retirement_expenses_monthly: float = Field(
        ..., ge=0.0, description="Projected baseline total monthly spending required in retirement"
    )

    @property
    def total_current_monthly_expenses(self) -> float:
        return (
            self.essential_expenses_monthly
            + self.discretionary_expenses_monthly
            + self.healthcare_monthly
            + self.debt_service_monthly
        )


class AssetBreakdown(BaseModel):
    """Assets in PKR, highlighting Pakistan-specific retirement instruments."""
    cash_and_savings: float = Field(0.0, ge=0.0, description="Cash in bank accounts, prize bonds, liquid funds")
    liquid_investments: float = Field(0.0, ge=0.0, description="Mutual funds, listed equities, Sukuk, money market funds")
    provident_fund: float = Field(0.0, ge=0.0, description="Provident Fund (PF) balance")
    gratuity_expected: float = Field(0.0, ge=0.0, description="End-of-service gratuity lump sum")
    vps_pension_balance: float = Field(0.0, ge=0.0, description="Voluntary Pension Scheme (VPS) accumulated corpus")
    gold_and_valuables: float = Field(0.0, ge=0.0, description="Gold bullion, jewelry, convertible precious metals")
    property_primary_residence: float = Field(0.0, ge=0.0, description="Primary home value (illiquid/lifestyle)")
    property_investment: float = Field(0.0, ge=0.0, description="Commercial/residential investment plots & rental units")
    other_assets: float = Field(0.0, ge=0.0, description="Vehicles, business equity, National Savings / NSS certificates")

    @property
    def total_liquid_assets(self) -> float:
        """Immediately accessible reserves for emergencies or income generation."""
        return self.cash_and_savings + self.liquid_investments

    @property
    def total_retirement_investable_assets(self) -> float:
        """Assets readily available or convertible to support retirement cash flows."""
        return (
            self.cash_and_savings
            + self.liquid_investments
            + self.provident_fund
            + self.gratuity_expected
            + self.vps_pension_balance
            + self.gold_and_valuables
            + self.property_investment
        )

    @property
    def total_assets(self) -> float:
        return (
            self.cash_and_savings
            + self.liquid_investments
            + self.provident_fund
            + self.gratuity_expected
            + self.vps_pension_balance
            + self.gold_and_valuables
            + self.property_primary_residence
            + self.property_investment
            + self.other_assets
        )


class LiabilityBreakdown(BaseModel):
    """Liabilities and debt obligations in PKR."""
    mortgage_balance: float = Field(0.0, ge=0.0, description="Home loan outstanding principal")
    personal_loans: float = Field(0.0, ge=0.0, description="Personal or auto loans outstanding")
    credit_card_debt: float = Field(0.0, ge=0.0, description="Credit card balances / high-interest consumer debt")
    other_liabilities: float = Field(0.0, ge=0.0, description="Informal committee / family loans / business guarantees")

    @property
    def total_liabilities(self) -> float:
        return (
            self.mortgage_balance
            + self.personal_loans
            + self.credit_card_debt
            + self.other_liabilities
        )


class RetirementGoals(BaseModel):
    """Target retirement goals and parameters."""
    target_monthly_income_pkr: float = Field(..., ge=0.0, description="Desired monthly retirement income in PKR")
    emergency_reserve_months: int = Field(6, ge=1, le=36, description="Target months of essential expenses held in liquidity")
    healthcare_reserve_pkr: float = Field(0.0, ge=0.0, description="Earmarked lump-sum reserve for major medical emergencies")
    legacy_bequest_target_pkr: float = Field(0.0, ge=0.0, description="Intended legacy/inheritance to leave for heirs")
    expected_annual_inflation_rate: float = Field(0.08, ge=0.0, le=0.35, description="Expected annual inflation rate (default 8% for PKR)")
    expected_annual_investment_return: float = Field(0.11, ge=0.0, le=0.35, description="Expected nominal annual portfolio return (default 11% for PKR)")


class FinancialProfile(BaseModel):
    """Complete Fact-Find financial profile for a client."""
    client_id: str
    income: IncomeBreakdown
    expenses: ExpenseBreakdown
    assets: AssetBreakdown
    liabilities: LiabilityBreakdown
    goals: RetirementGoals

    @property
    def net_worth(self) -> float:
        return self.assets.total_assets - self.liabilities.total_liabilities

    @property
    def net_investable_retirement_capital(self) -> float:
        """Investable retirement capital minus total liabilities."""
        return max(0.0, self.assets.total_retirement_investable_assets - self.liabilities.total_liabilities)
