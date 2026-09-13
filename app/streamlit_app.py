"""RetireWise AI — Open-Source Financial Suitability & Retirement Intelligence Platform."""
import sys
import os

# Add root directory to sys.path so imports work cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Load environment configuration from .env and .env.example
load_dotenv()
load_dotenv(".env.example")

from models.client import ClientProfile, MaritalStatus
from models.financial_profile import (
    FinancialProfile,
    IncomeBreakdown,
    ExpenseBreakdown,
    AssetBreakdown,
    LiabilityBreakdown,
    RetirementGoals,
)
from models.assessment import (
    SuitabilityAssessmentResult,
    WarningSeverity,
)
from core.validation import validate_client_and_profile
from core.financial_engine import calculate_financial_health
from core.risk_engine import calculate_risk_tolerance, RISK_QUESTIONS
from core.capacity_engine import calculate_capacity_for_loss, evaluate_suitability_conflicts
from core.retirement_engine import run_retirement_cash_flow_simulation
from core.scenario_engine import run_all_stress_scenarios
from core.monte_carlo_engine import run_monte_carlo_simulation
from core.shariah_engine import calculate_pakistan_asset_allocation
from core.digital_twin import simulate_digital_twin_what_if
from database.database import Database
from data.sample_clients import get_synthetic_personas
from ai.llm_client import LLMClient
from ai.report_generator import AIReportNarrativeGenerator
from reports.pdf_generator import generate_suitability_pdf_report
from app.ui_components import (
    create_capital_trajectory_chart,
    create_cash_flow_breakdown_chart,
    create_risk_vs_capacity_matrix,
    create_monte_carlo_fan_chart,
    create_asset_allocation_chart,
)

# Page configuration
st.set_page_config(
    page_title="RetireWise AI — Retirement Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header { font-size: 26px; font-weight: 700; color: var(--text-color, #0f2942); margin-bottom: 2px; }
    .sub-header { font-size: 14px; opacity: 0.8; margin-bottom: 20px; }
    .metric-card { 
        background-color: rgba(2, 136, 209, 0.08); 
        border: 1px solid rgba(2, 136, 209, 0.25);
        border-radius: 8px; 
        padding: 16px; 
        border-left: 5px solid #0288d1; 
        color: var(--text-color, inherit);
    }
    .metric-card h4 { color: #0288d1 !important; margin: 0 0 6px 0; font-size: 16px; }
    .metric-card p { color: var(--text-color, inherit) !important; margin: 0; font-size: 14px; }
    .conflict-card { 
        background-color: rgba(211, 47, 47, 0.1); 
        border: 1px solid rgba(211, 47, 47, 0.3);
        border-radius: 8px; 
        padding: 16px; 
        border-left: 5px solid #d32f2f; 
        margin-bottom: 14px; 
        color: var(--text-color, inherit);
    }
    .conflict-card h4 { color: #ef5350 !important; margin: 0 0 6px 0; }
    .conflict-card p { color: var(--text-color, inherit) !important; margin: 0; }
    .success-card { 
        background-color: rgba(46, 125, 50, 0.1); 
        border: 1px solid rgba(46, 125, 50, 0.3);
        border-radius: 8px; 
        padding: 16px; 
        border-left: 5px solid #2e7d32; 
        margin-bottom: 14px; 
        color: var(--text-color, inherit);
    }
    .success-card h4 { color: #4caf50 !important; margin: 0 0 6px 0; }
    .success-card p { color: var(--text-color, inherit) !important; margin: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Database & State
db = Database("retirewise.db")
llm_client = LLMClient()
ai_narrative_gen = AIReportNarrativeGenerator(llm_client)

if "active_client_id" not in st.session_state:
    st.session_state.active_client_id = "CLIENT-001-TARIQ"

# Pre-populate sample personas if DB is empty
existing_clients = db.list_clients()
if not existing_clients:
    for c, p, _ in get_synthetic_personas():
        db.save_client(c)
        db.save_financial_profile(p)
    existing_clients = db.list_clients()

# --- Sidebar: Case Selection & Navigation ---
with st.sidebar:
    st.markdown("### 🛡️ RetireWise AI")
    st.caption("Pakistan WealthTech Decision Support")
    st.markdown("---")

    client_options = {c.client_id: f"{c.name}" for c in existing_clients}
    selected_client_id = st.selectbox(
        "Select Client Case",
        options=list(client_options.keys()),
        format_func=lambda cid: client_options.get(cid, cid),
        index=list(client_options.keys()).index(st.session_state.active_client_id) if st.session_state.active_client_id in client_options else 0,
    )
    st.session_state.active_client_id = selected_client_id

    st.markdown("---")
    with st.expander("➕ Create New Client Case", expanded=False):
        with st.form("new_client_form", clear_on_submit=True):
            new_name = st.text_input("Client Full Name", placeholder="e.g. Farhan Ali")
            n_col1, n_col2 = st.columns(2)
            new_cur_age = n_col1.number_input("Current Age", min_value=18, max_value=95, value=52)
            new_ret_age = n_col2.number_input("Retirement Age", min_value=30, max_value=100, value=60)
            new_horizon = n_col1.number_input("Planning Horizon", min_value=50, max_value=110, value=85)
            new_deps = n_col2.number_input("Dependents", min_value=0, max_value=10, value=2)
            new_status = st.selectbox("Marital Status", ["Married", "Single", "Widowed", "Divorced"])
            new_adviser = st.text_input("Adviser Name", value="Usman Khan, CFP")
            create_btn = st.form_submit_button("Create Client Profile", type="primary")

            if create_btn and new_name.strip():
                clean_id = f"CLIENT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                new_client = ClientProfile(
                    client_id=clean_id,
                    name=new_name.strip(),
                    current_age=new_cur_age,
                    retirement_age=new_ret_age,
                    planning_horizon_age=new_horizon,
                    marital_status=MaritalStatus(new_status),
                    dependents_count=new_deps,
                    adviser_name=new_adviser.strip(),
                    notes="New client case created via adviser workstation.",
                )
                new_profile = FinancialProfile(
                    client_id=clean_id,
                    income=IncomeBreakdown(salary_monthly=300000.0, pension_monthly=0.0, rental_income_monthly=0.0),
                    expenses=ExpenseBreakdown(
                        essential_expenses_monthly=120000.0,
                        discretionary_expenses_monthly=40000.0,
                        healthcare_monthly=15000.0,
                        debt_service_monthly=0.0,
                        expected_retirement_expenses_monthly=180000.0,
                    ),
                    assets=AssetBreakdown(
                        cash_and_savings=2000000.0,
                        liquid_investments=3000000.0,
                        provident_fund=5000000.0,
                        gratuity_expected=2000000.0,
                        vps_pension_balance=1000000.0,
                        gold_and_valuables=1000000.0,
                        property_primary_residence=20000000.0,
                        property_investment=0.0,
                    ),
                    liabilities=LiabilityBreakdown(),
                    goals=RetirementGoals(
                        target_monthly_income_pkr=180000.0,
                        emergency_reserve_months=6,
                        expected_annual_inflation_rate=0.08,
                        expected_annual_investment_return=0.11,
                    ),
                )
                db.save_client(new_client)
                db.save_financial_profile(new_profile)
                st.session_state.active_client_id = clean_id
                st.success(f"Client '{new_name}' created!")
                st.rerun()

    st.markdown("---")
    st.markdown("**Quick Load Sample Personas**")
    col_p1, col_p2, col_p3 = st.columns(3)
    if col_p1.button("Persona A", help="Tariq: Conservative Retiree"):
        st.session_state.active_client_id = "CLIENT-001-TARIQ"
        st.rerun()
    if col_p2.button("Persona B", help="Ayesha: Moderate Near-Retiree"):
        st.session_state.active_client_id = "CLIENT-002-AYESHA"
        st.rerun()
    if col_p3.button("Persona C", help="Kamran: Suitability Conflict"):
        st.session_state.active_client_id = "CLIENT-003-KAMRAN"
        st.rerun()

    st.markdown("---")
    with st.expander("⚙️ AI Provider Settings", expanded=False):
        current_p = os.getenv("AI_PROVIDER", llm_client.provider).lower()
        provider_choices = ["mock", "groq", "gemini", "openai"]
        selected_p = st.selectbox(
            "Active AI Model",
            options=provider_choices,
            index=provider_choices.index(current_p) if current_p in provider_choices else 0,
            format_func=lambda p: {
                "mock": "Offline Fallback (Mock)",
                "groq": "Groq (Llama 3.3 70B)",
                "gemini": "Google Gemini (2.5 Flash)",
                "openai": "OpenAI (GPT-4o mini)",
            }.get(p, p),
        )
        api_key_input = ""
        if selected_p != "mock":
            has_existing = bool(os.getenv(f"{selected_p.upper()}_API_KEY", ""))
            try:
                if not has_existing and hasattr(st, "secrets") and f"{selected_p.upper()}_API_KEY" in st.secrets:
                    has_existing = bool(st.secrets[f"{selected_p.upper()}_API_KEY"])
            except Exception:
                pass

            placeholder_text = "•••••••• (Configured securely on server)" if has_existing else f"Enter {selected_p.upper()} key..."
            api_key_input = st.text_input(
                f"{selected_p.upper()} API Key",
                value="",
                type="password",
                placeholder=placeholder_text,
                help="Server secrets are hidden and never exposed to public visitors."
            )

        if st.button("Save AI Settings", type="primary"):
            os.environ["AI_PROVIDER"] = selected_p
            if selected_p == "groq" and api_key_input:
                os.environ["GROQ_API_KEY"] = api_key_input
            elif selected_p == "gemini" and api_key_input:
                os.environ["GEMINI_API_KEY"] = api_key_input
            elif selected_p == "openai" and api_key_input:
                os.environ["OPENAI_API_KEY"] = api_key_input
            st.success(f"AI Provider set to {selected_p.upper()}!")
            st.rerun()

    st.caption("Active Provider: **" + os.getenv("AI_PROVIDER", llm_client.provider).upper() + "**")
    st.caption("Default Currency: **PKR**")

# Load active client and profile
active_client = db.get_client(st.session_state.active_client_id)
active_profile = db.get_financial_profile(st.session_state.active_client_id)

if not active_client or not active_profile:
    st.error("Client profile could not be loaded. Please select a client case.")
    st.stop()

# Header
st.markdown(f"<div class='main-header'>Client Assessment: {active_client.name}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-header'>Adviser: {active_client.adviser_name} | Case ID: {active_client.client_id}</div>", unsafe_allow_html=True)

# Tabs
tab_overview, tab_factfind, tab_risk_capacity, tab_scenarios, tab_monte_carlo, tab_shariah, tab_ai_report = st.tabs([
    "📊 Financial Snapshot",
    "📝 Fact-Find & Goals",
    "⚖️ Risk & Capacity Suitability",
    "📈 Projections & Scenarios",
    "🎲 Monte Carlo & Digital Twin",
    "🕌 Shariah Asset Allocation",
    "📑 AI Insights & PDF Report",
])

# ==========================================
# TAB 1: FINANCIAL SNAPSHOT
# ==========================================
with tab_overview:
    fh = calculate_financial_health(active_profile)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net Worth", f"PKR {fh.net_worth_pkr:,.0f}")
        st.caption(f"Total Assets: PKR {fh.total_assets_pkr:,.0f}")
    with col2:
        st.metric("Investable Capital", f"PKR {fh.net_investable_retirement_capital_pkr:,.0f}")
        st.caption(f"Liquid Cash: PKR {fh.liquid_assets_pkr:,.0f}")
    with col3:
        st.metric("Monthly Ret. Gap", f"PKR {fh.monthly_retirement_income_gap_pkr:,.0f}/mo")
        st.caption(f"Guaranteed: PKR {fh.guaranteed_monthly_retirement_income_pkr:,.0f}/mo")
    with col4:
        st.metric("Emergency Reserve", f"{fh.emergency_reserve_adequacy_ratio:.1f}x Target")
        if fh.emergency_reserve_adequacy_ratio < 1.0:
            st.caption("⚠️ Deficit below emergency target")
        else:
            st.caption("✅ Adequate liquidity buffer")

    st.markdown("---")
    st.subheader("Current Cash Flow & Asset Breakdown")
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("**Monthly Cash Flow Position (PKR)**")
        st.write(f"- Active Employment Salary: **PKR {active_profile.income.salary_monthly:,.0f}**")
        st.write(f"- Guaranteed Pension: **PKR {active_profile.income.pension_monthly:,.0f}**")
        st.write(f"- Net Rental Income: **PKR {active_profile.income.rental_income_monthly:,.0f}**")
        st.write(f"- Total Monthly Income: **PKR {fh.current_monthly_income_pkr:,.0f}**")
        st.write(f"- Total Current Expenses: **PKR {fh.current_monthly_expenses_pkr:,.0f}**")
        st.write(f"- Current Monthly Surplus / (Deficit): **PKR {fh.current_monthly_surplus_pkr:,.0f}**")

    with c_right:
        st.markdown("**Retirement Wealth Portfolio (PKR)**")
        st.write(f"- Cash & Bank Savings: **PKR {active_profile.assets.cash_and_savings:,.0f}**")
        st.write(f"- Liquid Market Investments: **PKR {active_profile.assets.liquid_investments:,.0f}**")
        st.write(f"- Provident Fund (PF): **PKR {active_profile.assets.provident_fund:,.0f}**")
        st.write(f"- Gratuity Expected: **PKR {active_profile.assets.gratuity_expected:,.0f}**")
        st.write(f"- VPS Pension Balance: **PKR {active_profile.assets.vps_pension_balance:,.0f}**")
        st.write(f"- Gold & Precious Metals: **PKR {active_profile.assets.gold_and_valuables:,.0f}**")
        st.write(f"- Total Liabilities / Debt: **PKR {fh.total_liabilities_pkr:,.0f}**")

# ==========================================
# TAB 2: FACT-FIND & GOALS
# ==========================================
with tab_factfind:
    st.subheader("Edit Financial Fact-Find")
    with st.form("fact_find_form"):
        st.markdown("#### 1. Demographics & Planning Horizon")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        c_age = f_col1.number_input("Current Age", min_value=18, max_value=100, value=active_client.current_age)
        r_age = f_col2.number_input("Retirement Age", min_value=30, max_value=100, value=active_client.retirement_age)
        h_age = f_col3.number_input("Planning Horizon (Age)", min_value=50, max_value=110, value=active_client.planning_horizon_age)
        deps = f_col4.number_input("Dependents Count", min_value=0, max_value=15, value=active_client.dependents_count)

        st.markdown("#### 2. Monthly Income Streams (PKR)")
        i_col1, i_col2, i_col3 = st.columns(3)
        salary = i_col1.number_input("Pre-Retirement Salary", value=float(active_profile.income.salary_monthly), step=10000.0)
        pension = i_col2.number_input("Guaranteed Pension", value=float(active_profile.income.pension_monthly), step=5000.0)
        rental = i_col3.number_input("Rental Income", value=float(active_profile.income.rental_income_monthly), step=5000.0)

        st.markdown("#### 3. Monthly Expenses (PKR)")
        e_col1, e_col2, e_col3 = st.columns(3)
        essential_exp = e_col1.number_input("Essential Expenses / mo", value=float(active_profile.expenses.essential_expenses_monthly), step=10000.0)
        discretionary_exp = e_col2.number_input("Discretionary Expenses / mo", value=float(active_profile.expenses.discretionary_expenses_monthly), step=5000.0)
        ret_exp = e_col3.number_input("Expected Ret. Expenses / mo", value=float(active_profile.expenses.expected_retirement_expenses_monthly), step=10000.0)

        st.markdown("#### 4. Assets & Retirement Resources (PKR)")
        a_col1, a_col2, a_col3 = st.columns(3)
        cash_val = a_col1.number_input("Cash & Bank Savings", value=float(active_profile.assets.cash_and_savings), step=100000.0)
        invest_val = a_col2.number_input("Liquid Investments (Funds/Sukuk)", value=float(active_profile.assets.liquid_investments), step=100000.0)
        pf_val = a_col3.number_input("Provident Fund Balance", value=float(active_profile.assets.provident_fund), step=100000.0)

        a_col4, a_col5, a_col6 = st.columns(3)
        gratuity_val = a_col4.number_input("Gratuity Expected", value=float(active_profile.assets.gratuity_expected), step=100000.0)
        vps_val = a_col5.number_input("VPS Balance", value=float(active_profile.assets.vps_pension_balance), step=100000.0)
        gold_val = a_col6.number_input("Gold & Valuables", value=float(active_profile.assets.gold_and_valuables), step=50000.0)

        st.markdown("#### 5. Economic & Return Assumptions")
        g_col1, g_col2 = st.columns(2)
        inf_rate = g_col1.slider("Expected Annual Inflation Rate (%)", min_value=3.0, max_value=25.0, value=float(active_profile.goals.expected_annual_inflation_rate * 100.0), step=0.5) / 100.0
        ret_rate = g_col2.slider("Expected Annual Portfolio Return (%)", min_value=5.0, max_value=30.0, value=float(active_profile.goals.expected_annual_investment_return * 100.0), step=0.5) / 100.0

        save_btn = st.form_submit_button("💾 Save Fact-Find & Update Calculations")
        if save_btn:
            active_client.current_age = c_age
            active_client.retirement_age = r_age
            active_client.planning_horizon_age = h_age
            active_client.dependents_count = deps

            active_profile.income.salary_monthly = salary
            active_profile.income.pension_monthly = pension
            active_profile.income.rental_income_monthly = rental

            active_profile.expenses.essential_expenses_monthly = essential_exp
            active_profile.expenses.discretionary_expenses_monthly = discretionary_exp
            active_profile.expenses.expected_retirement_expenses_monthly = ret_exp

            active_profile.assets.cash_and_savings = cash_val
            active_profile.assets.liquid_investments = invest_val
            active_profile.assets.provident_fund = pf_val
            active_profile.assets.gratuity_expected = gratuity_val
            active_profile.assets.vps_pension_balance = vps_val
            active_profile.assets.gold_and_valuables = gold_val

            active_profile.goals.expected_annual_inflation_rate = inf_rate
            active_profile.goals.expected_annual_investment_return = ret_rate

            is_valid, errors = validate_client_and_profile(active_client, active_profile)
            if not is_valid:
                for err in errors:
                    st.error(f"Validation Error: {err}")
            else:
                db.save_client(active_client)
                db.save_financial_profile(active_profile)
                st.success("Fact-Find successfully saved and updated in SQLite database!")
                st.rerun()

# ==========================================
# TAB 3: RISK & CAPACITY SUITABILITY
# ==========================================
with tab_risk_capacity:
    st.subheader("Psychological Risk Tolerance Questionnaire")
    st.caption("Measure attitude toward financial losses and market volatility (1-4 scale).")

    # Get sample responses if available
    sample_personas = get_synthetic_personas()
    default_answers = {}
    for c, p, r_ans in sample_personas:
        if c.client_id == active_client.client_id:
            default_answers = r_ans
            break

    risk_responses = {}
    r_cols = st.columns(2)
    for idx, q in enumerate(RISK_QUESTIONS):
        col_target = r_cols[idx % 2]
        with col_target:
            st.markdown(f"**{idx+1}. {q['text']}**")
            current_choice = default_answers.get(q["id"], 2)
            options_labels = [opt["label"] for opt in q["options"]]
            choice = st.radio(
                f"Question {idx+1}",
                options=options_labels,
                index=max(0, min(len(options_labels)-1, current_choice - 1)),
                key=f"risk_q_{q['id']}",
                label_visibility="collapsed",
            )
            # Find chosen score
            chosen_score = next(opt["score"] for opt in q["options"] if opt["label"] == choice)
            risk_responses[q["id"]] = chosen_score

    # Compute Risk & Capacity
    risk_result = calculate_risk_tolerance(risk_responses)
    capacity_result = calculate_capacity_for_loss(active_client, active_profile)
    warnings, has_conflict = evaluate_suitability_conflicts(risk_result, capacity_result, active_profile, active_client)

    st.markdown("---")
    st.subheader("Suitability Evaluation: Risk Attitude vs. Capacity for Loss")

    if has_conflict:
        st.markdown(
            """
            <div class='conflict-card'>
                <h4 style='color:#b71c1c; margin:0;'>⚠️ CRITICAL SUITABILITY CONFLICT DETECTED</h4>
                <p style='margin:4px 0 0 0;'>The client expresses an aggressive appetite for risk, but possesses a fragile 
                objective financial capacity for loss. Regulatory suitability mandates that asset allocation be anchored 
                to <b>Capacity for Loss</b>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col_score1, col_score2 = st.columns(2)
    with col_score1:
        st.metric("Attitudinal Risk Tolerance", f"{risk_result.normalized_score}/100", delta=risk_result.category.value)
        st.info(f"**Category:** {risk_result.category.value}\n\n{risk_result.summary}")

    with col_score2:
        st.metric("Objective Capacity for Loss", f"{capacity_result.capacity_score}/100", delta=capacity_result.category.value)
        st.info(
            f"**Category:** {capacity_result.category.value}\n\n"
            f"- Income Dependency: **{capacity_result.income_dependency_pct}%** of living costs\n"
            f"- Emergency Cushion: **{capacity_result.liquid_emergency_months}** months in liquid reserves\n"
            f"- Debt Ratio: **{capacity_result.debt_to_assets_pct}%** of total assets"
        )

    st.plotly_chart(create_risk_vs_capacity_matrix(risk_result.normalized_score, capacity_result.capacity_score), use_container_width=True)

# ==========================================
# TAB 4: RETIREMENT PROJECTIONS & SCENARIOS
# ==========================================
with tab_scenarios:
    st.subheader("Deterministic Multi-Year Cash Flow Projections")
    scenarios = run_all_stress_scenarios(active_client, active_profile)
    base_scen = next(s for s in scenarios if s.scenario_type.value == "Base Case")

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.metric("Base Case Horizon", f"{base_scen.sustainability_years} Years", delta="Sustainable" if base_scen.is_sustainable else "Depleted")
    with p_col2:
        st.metric("Depletion Age", f"Age {base_scen.capital_depletion_age}" if base_scen.capital_depletion_age else "Solvent to Horizon")
    with p_col3:
        st.metric("Ending Capital at Horizon", f"PKR {base_scen.ending_capital_pkr:,.0f}")

    # Plotly Charts
    st.plotly_chart(create_capital_trajectory_chart(scenarios), use_container_width=True)
    st.plotly_chart(create_cash_flow_breakdown_chart(base_scen.yearly_trajectory), use_container_width=True)

    # Scenarios Comparison Table
    st.markdown("#### Scenario Stress Testing Matrix")
    scen_table_data = []
    for s in scenarios:
        scen_table_data.append({
            "Scenario": s.scenario_name,
            "Return / Inflation": f"{s.annual_return_rate*100:.1f}% / {s.annual_inflation_rate*100:.1f}%",
            "Solvent Years": f"{s.sustainability_years} yrs",
            "Depletion Age": f"Age {s.capital_depletion_age}" if s.capital_depletion_age else "Solvent through 85+",
            "Ending Capital (PKR)": f"PKR {s.ending_capital_pkr:,.0f}",
            "Key Vulnerability": s.key_vulnerability,
        })
    st.dataframe(scen_table_data, use_container_width=True)

# ==========================================
# TAB 5: MONTE CARLO & DIGITAL TWIN
# ==========================================
with tab_monte_carlo:
    st.subheader("🎲 Monte Carlo 1,000-Trial Stochastic Simulation")
    st.caption("Subjecting the client portfolio to 1,000 randomized market return and inflation cycles simultaneously.")

    mc_base = run_monte_carlo_simulation(active_client, active_profile, fh, trials_count=1000)

    mc_c1, mc_c2, mc_c3 = st.columns(3)
    with mc_c1:
        st.metric("Retirement Success Rate", f"{mc_base.probability_of_success_pct}%", delta=mc_base.confidence_verdict)
    with mc_c2:
        st.metric("Median Depletion Age", f"Age {mc_base.median_depletion_age}" if mc_base.median_depletion_age else "Solvent past 85+")
    with mc_c3:
        st.metric("Median Ending Capital", f"PKR {mc_base.median_ending_capital_pkr:,.0f}")

    # Render Fan Chart
    st.plotly_chart(create_monte_carlo_fan_chart(mc_base), use_container_width=True)

    # Real-time What-If Digital Twin Section
    st.markdown("---")
    st.subheader("🔮 Financial Digital Twin: Interactive 'What-If' Sandbox")
    st.caption("Adjust real-world life decisions below to see real-time recalculations on retirement solvency.")

    wt_col1, wt_col2, wt_col3 = st.columns(3)
    with wt_col1:
        ret_age_shift = st.slider("Retirement Age Shift (Years)", min_value=-5, max_value=5, value=0, help="Negative = Earlier, Positive = Delayed")
        adjusted_age = active_client.retirement_age + ret_age_shift
        st.caption(f"Adjusted Retirement Age: **{adjusted_age}**")
    with wt_col2:
        exp_multiplier = st.slider("Retirement Living Expenses Multiplier", min_value=0.7, max_value=1.4, value=1.0, step=0.05, help="1.0 = baseline, 0.8 = frugal, 1.2 = lifestyle expansion")
        base_exp = active_profile.expenses.expected_retirement_expenses_monthly or active_profile.expenses.essential_expenses_monthly
        st.caption(f"Adjusted Monthly Living Burn: **PKR {base_exp * exp_multiplier:,.0f}/mo**")
    with wt_col3:
        lump_amt = st.number_input("One-Time Event PKR (+ Inflow / - Outflow)", value=0.0, step=500_000.0, help="Positive = Property Sale/Inheritance; Negative = Medical/Wedding Shock")
        lump_age = st.slider("Event Age", min_value=active_client.current_age, max_value=active_client.planning_horizon_age, value=min(65, active_client.planning_horizon_age))

    # Evaluate digital twin
    if ret_age_shift != 0 or exp_multiplier != 1.0 or lump_amt != 0.0:
        dt_res = simulate_digital_twin_what_if(
            client=active_client,
            financial_profile=active_profile,
            health=fh,
            retirement_age_delta=ret_age_shift,
            monthly_expense_multiplier=exp_multiplier,
            lump_sum_event_amount=lump_amt,
            lump_sum_event_age=lump_age if lump_amt != 0.0 else None,
            trials_count=500,
        )
        delta_success = round(dt_res["what_if_probability_of_success_pct"] - mc_base.probability_of_success_pct, 1)
        st.markdown(
            f"""
            <div class='metric-card' style='margin-top:12px;'>
                <h4>What-If Scenario Impact:</h4>
                <p>
                    New Retirement Success Rate: <b>{dt_res['what_if_probability_of_success_pct']}%</b> 
                    (Change: <span style='color:{"#4caf50" if delta_success >= 0 else "#ef5350"}; font-weight:700;'><b>{delta_success:+0.1f}%</b></span>) &nbsp;|&nbsp; 
                    Status: <b>{dt_res['confidence_verdict']}</b> &nbsp;|&nbsp;
                    Median Depletion: <b>{'Age ' + str(dt_res['what_if_median_depletion_age']) if dt_res['what_if_median_depletion_age'] else 'Solvent Past 85+'}</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# TAB 6: SHARIAH ASSET ALLOCATION
# ==========================================
with tab_shariah:
    st.subheader("🕌 Pakistan Asset Allocation & Shariah Recommender")
    st.caption("Portfolio asset allocation strictly anchored to Objective Capacity for Loss, with Section 63 tax credit optimization.")

    standard_choice = st.radio(
        "Select Regulatory Framework",
        ["Shariah-Compliant (Islamic)", "Conventional Fixed Income"],
        horizontal=True,
    )
    is_shariah = (standard_choice == "Shariah-Compliant (Islamic)")

    shariah_res = calculate_pakistan_asset_allocation(
        client=active_client,
        financial_profile=active_profile,
        health=fh,
        capacity=capacity_result,
        risk=risk_result,
        is_shariah_mode=is_shariah,
    )

    sh_col1, sh_col2, sh_col3 = st.columns(3)
    with sh_col1:
        st.metric("Capacity Equity Ceiling", f"{shariah_res.capacity_equity_ceiling_pct}%", delta="Mandatory Max Cap")
    with sh_col2:
        recommended_equity = next((item.recommended_pct for item in shariah_res.recommended_allocations if "Equities" in item.asset_class), 0.0)
        st.metric("Recommended Equity Allocation", f"{recommended_equity}%")
    with sh_col3:
        st.metric("Est. Annual VPS Tax Credit", f"PKR {shariah_res.estimated_annual_tax_credit_pkr:,.0f}", delta="Sec 63 Rebate")

    st.info(f"⚖️ **Governing Suitability Directive:** {shariah_res.governing_rationale}")

    alloc_c1, alloc_c2 = st.columns([1, 1])
    with alloc_c1:
        st.plotly_chart(create_asset_allocation_chart(shariah_res), use_container_width=True)
    with alloc_c2:
        st.markdown("#### Recommended Voluntary Pension Scheme (VPS) Sub-Funds")
        st.markdown(
            f"""
            - **VPS Equity Sub-Fund:** **{shariah_res.vps_equity_sub_fund_pct}%**
            - **VPS Debt / Sukuk Sub-Fund:** **{shariah_res.vps_debt_sub_fund_pct}%**
            - **VPS Money Market Sub-Fund:** **{shariah_res.vps_money_market_sub_fund_pct}%**
            """
        )
        st.caption(shariah_res.tax_optimization_notes)

    st.markdown("#### Pakistani Instrument Allocation Breakdown")
    alloc_table = []
    for item in shariah_res.recommended_allocations:
        alloc_table.append({
            "Asset Class": item.asset_class,
            "Allocation %": f"{item.recommended_pct}%",
            "Target Amount (PKR)": f"PKR {item.allocation_amount_pkr:,.0f}",
            "Pakistani Market Examples": ", ".join(item.instrument_examples),
            "Strategic Rationale": item.rationale,
        })
    st.dataframe(alloc_table, use_container_width=True)

# ==========================================
# TAB 7: AI INSIGHTS & PDF REPORT
# ==========================================
with tab_ai_report:
    st.subheader("AI Financial Intelligence & Audit Layer")
    st.caption("AI strictly explains calculated deterministic results; it never creates or hallucinates financial figures.")

    # Assemble complete assessment object
    base_projection = run_retirement_cash_flow_simulation(active_client, active_profile)
    assessment = SuitabilityAssessmentResult(
        assessment_id=f"ASSESS-{active_client.client_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
        client_id=active_client.client_id,
        client_name=active_client.name,
        created_at=datetime.now().isoformat(),
        financial_health=fh,
        risk_tolerance=risk_result,
        capacity_for_loss=capacity_result,
        retirement_projection=base_projection,
        scenarios=scenarios,
        conflict_warnings=warnings,
        has_suitability_conflict=has_conflict,
        suitability_summary=(
            "Suitability Conflict Detected: Risk appetite exceeds financial resilience."
            if has_conflict
            else "Suitable: Risk attitude and financial capacity are aligned."
        ),
        monte_carlo=mc_base,
        shariah_allocation=shariah_res,
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🤖 Generate AI Narrative Explanation", type="primary"):
            with st.spinner(f"Analyzing structured financial calculations using {os.getenv('AI_PROVIDER', 'mock').upper()}..."):
                active_llm = LLMClient()
                explanation_text = AIReportNarrativeGenerator(active_llm).generate_assessment_explanation(assessment)
                st.session_state["latest_ai_explanation"] = explanation_text

    with col_btn2:
        if st.button("🔍 Run Missing Data & Inconsistency Audit"):
            with st.spinner(f"Auditing fact-find data points using {os.getenv('AI_PROVIDER', 'mock').upper()}..."):
                active_llm = LLMClient()
                audit_text = AIReportNarrativeGenerator(active_llm).audit_missing_or_contradictory_data(active_profile)
                st.session_state["latest_ai_audit"] = audit_text

    if "latest_ai_explanation" in st.session_state:
        st.markdown("### AI Analytical Assessment")
        st.markdown(st.session_state["latest_ai_explanation"])

    if "latest_ai_audit" in st.session_state:
        st.markdown("### Fact-Find Data & Quality Audit")
        st.markdown(st.session_state["latest_ai_audit"])

    st.markdown("---")
    st.subheader("Generate Professional Client PDF Report")
    st.write("Generates the complete 12-section printable suitability and retirement intelligence report matching all calculations.")

    pdf_filename = f"RetireWise_Report_{active_client.client_id}.pdf"
    pdf_bytes = generate_suitability_pdf_report(active_client, active_profile, assessment)

    st.download_button(
        label="📥 Download Professional PDF Suitability Report",
        data=pdf_bytes,
        file_name=pdf_filename,
        mime="application/pdf",
        type="primary",
    )
