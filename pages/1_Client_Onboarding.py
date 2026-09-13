"""RetireWise AI — Client Self-Service Onboarding & Pre-Consultation Portal."""
import sys
import os
from datetime import datetime

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
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
from core.financial_engine import calculate_financial_health
from core.risk_engine import calculate_risk_tolerance, RISK_QUESTIONS
from core.capacity_engine import calculate_capacity_for_loss
from database.database import Database

# Page Configuration
st.set_page_config(
    page_title="Client Self-Service Portal — RetireWise AI",
    page_icon="📋",
    layout="wide",
)

st.markdown(
    """
    <style>
    .portal-header { font-size: 26px; font-weight: 700; color: var(--text-color, #0f2942); margin-bottom: 2px; }
    .portal-sub { font-size: 14px; opacity: 0.8; margin-bottom: 20px; }
    .card-box { 
        background-color: rgba(2, 136, 209, 0.08); 
        border: 1px solid rgba(2, 136, 209, 0.25);
        border-radius: 8px; 
        padding: 16px; 
        border-left: 5px solid #0288d1; 
        margin-bottom: 15px; 
        color: var(--text-color, inherit);
    }
    .card-box h4 { color: #0288d1 !important; margin: 0 0 6px 0; }
    .card-box p { color: var(--text-color, inherit) !important; margin: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='portal-header'>📋 Client Self-Service Fact-Find Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='portal-sub'>Complete your confidential pre-consultation financial information before your meeting with your Wealth Adviser.</div>", unsafe_allow_html=True)

db = Database("retirewise.db")

with st.form("client_self_onboarding_form"):
    st.subheader("1. Personal & Retirement Timeline")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Legal Name", placeholder="e.g. Imran Raza")
        current_age = st.number_input("Current Age (Years)", min_value=18, max_value=95, value=48)
        planning_horizon = st.number_input("Planning Horizon Age (Life Expectancy)", min_value=50, max_value=110, value=85)
        adviser_name = st.text_input("Assigned Adviser / Branch", value="RetireWise Advisory Services")
    with col2:
        marital_status = st.selectbox("Marital Status", ["Married", "Single", "Widowed", "Divorced"])
        retirement_age = st.number_input("Target Retirement Age (Years)", min_value=30, max_value=100, value=60)
        dependents = st.number_input("Number of Financial Dependents (Children / Parents)", min_value=0, max_value=10, value=2)

    st.markdown("---")
    st.subheader("2. Monthly Inflow & Cash Flow (PKR)")
    inc_col1, inc_col2, inc_col3 = st.columns(3)
    with inc_col1:
        salary = st.number_input("Monthly Salary / Business Income (PKR)", min_value=0.0, value=350_000.0, step=25_000.0)
    with inc_col2:
        pension = st.number_input("Expected Monthly Pension (PKR)", min_value=0.0, value=0.0, step=10_000.0)
    with inc_col3:
        rental = st.number_input("Monthly Rental / Other Passive (PKR)", min_value=0.0, value=35_000.0, step=10_000.0)

    st.markdown("---")
    st.subheader("3. Monthly Living Expenses (PKR)")
    exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
    with exp_col1:
        essential_exp = st.number_input("Essential Needs (Food, Utilities, Groceries)", min_value=0.0, value=120_000.0, step=10_000.0)
    with exp_col2:
        discretionary_exp = st.number_input("Discretionary (Dining, Travel, Lifestyle)", min_value=0.0, value=40_000.0, step=10_000.0)
    with exp_col3:
        healthcare_exp = st.number_input("Monthly Medical & Medication Burn", min_value=0.0, value=15_000.0, step=5_000.0)
    with exp_col4:
        expected_ret_exp = st.number_input("Expected Total Retirement Expenses/mo", min_value=0.0, value=180_000.0, step=10_000.0)

    st.markdown("---")
    st.subheader("4. Assets & Wealth Portfolio (PKR)")
    ast_col1, ast_col2, ast_col3 = st.columns(3)
    with ast_col1:
        cash_savings = st.number_input("Liquid Bank Cash & Savings Accounts", min_value=0.0, value=2_500_000.0, step=250_000.0)
        investments = st.number_input("Liquid Stocks & Mutual Funds", min_value=0.0, value=3_000_000.0, step=250_000.0)
    with ast_col2:
        provident_fund = st.number_input("Provident Fund (PF) Balance", min_value=0.0, value=6_000_000.0, step=500_000.0)
        gratuity = st.number_input("Expected Gratuity Lump-Sum", min_value=0.0, value=2_000_000.0, step=250_000.0)
    with ast_col3:
        vps_balance = st.number_input("Voluntary Pension Scheme (VPS) Balance", min_value=0.0, value=1_500_000.0, step=250_000.0)
        property_invest = st.number_input("Investment Real Estate (Rental Plots/Flats)", min_value=0.0, value=12_000_000.0, step=1_000_000.0)

    st.markdown("---")
    st.subheader("5. Liabilities & Outstanding Debt (PKR)")
    liab_col1, liab_col2 = st.columns(2)
    with liab_col1:
        mortgage = st.number_input("Remaining Home Loan / Mortgage Balance", min_value=0.0, value=1_500_000.0, step=250_000.0)
    with liab_col2:
        personal_debt = st.number_input("Car Loan, Credit Cards, or Personal Debt", min_value=0.0, value=0.0, step=100_000.0)

    st.markdown("---")
    st.subheader("6. Investment Risk & Volatility Questionnaire")
    st.caption("Please indicate your natural comfort level with investment volatility.")

    risk_answers = {}
    r_cols = st.columns(2)
    for idx, q in enumerate(RISK_QUESTIONS):
        col_t = r_cols[idx % 2]
        with col_t:
            st.markdown(f"**{idx+1}. {q['text']}**")
            labels = [opt["label"] for opt in q["options"]]
            sel = st.radio(f"Q_{q['id']}", options=labels, index=1, key=f"portal_rq_{q['id']}", label_visibility="collapsed")
            score = next(opt["score"] for opt in q["options"] if opt["label"] == sel)
            risk_answers[q["id"]] = score

    submit_btn = st.form_submit_button("🚀 Submit Confidential Fact-Find", type="primary")

if submit_btn:
    if not full_name.strip():
        st.error("Please enter your full legal name.")
    else:
        new_client_id = f"CLIENT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        new_client = ClientProfile(
            client_id=new_client_id,
            name=full_name.strip(),
            current_age=current_age,
            retirement_age=retirement_age,
            planning_horizon_age=planning_horizon,
            marital_status=MaritalStatus(marital_status),
            dependents_count=dependents,
            adviser_name=adviser_name.strip(),
            notes="Client self-onboarded via pre-consultation web portal.",
        )
        new_profile = FinancialProfile(
            client_id=new_client_id,
            income=IncomeBreakdown(
                salary_monthly=salary,
                pension_monthly=pension,
                rental_income_monthly=rental,
            ),
            expenses=ExpenseBreakdown(
                essential_expenses_monthly=essential_exp,
                discretionary_expenses_monthly=discretionary_exp,
                healthcare_monthly=healthcare_exp,
                debt_service_monthly=0.0,
                expected_retirement_expenses_monthly=expected_ret_exp,
            ),
            assets=AssetBreakdown(
                cash_and_savings=cash_savings,
                liquid_investments=investments,
                provident_fund=provident_fund,
                gratuity_expected=gratuity,
                vps_pension_balance=vps_balance,
                property_investment=property_invest,
            ),
            liabilities=LiabilityBreakdown(
                mortgage_balance=mortgage,
                personal_loans=personal_debt,
            ),
            goals=RetirementGoals(
                target_monthly_income_pkr=expected_ret_exp,
                emergency_reserve_months=6,
            ),
        )

        validation_errors = validate_client_and_profile(new_client, new_profile)
        if validation_errors:
            for err in validation_errors:
                st.error(f"Validation Note: {err.message}")
        else:
            db.save_client(new_client)
            db.save_financial_profile(new_profile)

            # Instant snapshot calculation
            fh = calculate_financial_health(new_profile)
            risk_res = calculate_risk_tolerance(risk_answers)
            cap_res = calculate_capacity_for_loss(new_client, new_profile)

            st.success(f"🎉 Pre-Consultation Fact-Find Successfully Submitted! (Case Ref: {new_client_id})")
            st.markdown(
                f"""
                <div class='card-box'>
                    <h4 style='color:#1b5e20; margin:0;'>Initial Financial Health Snapshot</h4>
                    <p style='margin:6px 0 0 0;'>
                        • Estimated Net Worth: <b>PKR {fh.net_worth_pkr:,.0f}</b><br/>
                        • Liquid Emergency Reserves: <b>{cap_res.liquid_emergency_months:.1f} months</b> of essential living costs<br/>
                        • Risk Tolerance Category: <b>{risk_res.category.value} ({risk_res.normalized_score:.0f}/100)</b><br/>
                        • Objective Loss Capacity: <b>{cap_res.category.value} ({cap_res.capacity_score:.0f}/100)</b><br/>
                    </p>
                    <p style='color:#555555; margin-top:8px;'>Your Wealth Adviser has received your case and will have a comprehensive 
                    multi-scenario longevity assessment prepared for your consultation.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
