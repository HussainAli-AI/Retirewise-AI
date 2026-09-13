# RetireWise AI (Version 2.0)
### Pakistan-Focused Financial Suitability & Retirement Intelligence Platform

[![Version](https://img.shields.io/badge/Release-v2.0--Complete-brightgreen.svg)](https://github.com/HussainAli-AI/Retirewise-AI)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.32%2B-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)

---

## 1. What is RetireWise AI?
**RetireWise AI** is an open-source WealthTech & RetirementTech decision-support platform designed for financial advisers, Asset Management Companies (AMCs), pension managers, wealth managers, and insurers in Pakistan. 

It answers the critical retirement question:
> *Given a retiree's income, expenses, assets (Provident Fund, Gratuity, VPS, Gold, Property), liabilities, and dependents in Pakistan, how sustainable is their financial position under macroeconomic and personal stress scenarios?*

### The Cardinal Rule
> **"The LLM explains the numbers; it does not create the numbers."**

RetireWise AI maintains complete separation between **deterministic, transparent Python calculation engines** and the **AI narrative generation layer**.

📄 **[Institutional Product Requirements Document (PRD PDF)](RetireWise_AI_Product_Requirements_Document_PRD.pdf)**  
📊 **[Executive Presentation Pitch Deck (PDF)](RetireWise_AI_Presentation_Deck.pdf)**

---

## 2. The Problem
Retirement planning in Pakistan suffers from:
1. **Confusing Risk Tolerance with Capacity for Loss**: Advisers frequently allow an aggressive risk appetite to dictate portfolio choices, even when the client's objective financial capacity to absorb drawdowns is fragile.
2. **Double-Digit Inflation Cycles**: Pakistan's persistent inflation rapidly erodes purchasing power if cash flows are unindexed.
3. **Black-Box Tools or Hallucinatory Chatbots**: Generic conversational AI bots hallucinate financial arithmetic and invent returns.

---

## 3. Target Users
- **Primary**: Financial Advisers, Wealth Planners, Private Bankers, Mutual Fund Consultants.
- **Secondary**: Pre-retirees and Retirees completing structured Fact-Find questionnaires.
- **Future Institutional**: AMCs, Pension Fund Managers, Life Insurance Companies, Corporate Retirement Boards.

---

## 4. Platform Capabilities

### Core Engines (V1)
- **Pakistan-Specific Fact-Find (PKR)**: Captures Provident Fund (PF), Gratuity, Voluntary Pension Scheme (VPS), Gold, Property, and Family Dependents.
- **Deterministic Risk Engine (0-100)**: 8-question psychometric attitude-to-risk instrument.
- **Objective Capacity for Loss (0-100)**: Quantifies income dependency, emergency runway, and debt encumbrance.
- **Automated Suitability Conflict Detector**: Immediately flags mismatches (*High Risk Tolerance + Low Capacity for Loss*).
- **Multi-Year Retirement Cash Flow Engine**: Year-by-year compounding simulation predicting capital depletion age and horizon sustainability.
- **5 Stress Testing Scenarios**: Base Case, High Inflation Shock (+5%), Early Market Drawdown (-4%), Healthcare Crisis Shock, and Early Retirement Shock.
- **Provider-Agnostic AI Narrative Layer**: Pluggable support for Groq (Llama 3.3), Google Gemini, OpenAI, or a built-in deterministic rule engine (100% offline).
- **Professional 12-Section PDF Report**: Pixel-accurate, audit-ready ReportLab document export.

### Advanced Intelligence & Simulation (V2)
- **1,000-Trial Vectorized Monte Carlo Engine (`numpy`)**: Stochastic return and inflation simulation with 10th, 50th, and 90th percentile confidence cones and exact **Probability of Retirement Success %**.
- **Financial Digital Twin Sandbox**: Real-time What-If sensitivity controls (retirement age shift, living expense scaling, and lump-sum cash events).
- **Pakistan Shariah Asset Allocation Engine**: Capacity-governed equity caps, sovereign Sukuks, KMI-30 equities, VPS sub-funds, and **Section 63 ITO tax credit optimizer**.
- **Client Self-Service Onboarding Portal**: Standalone pre-consultation onboarding flow (`pages/1_Client_Onboarding.py`).
- **Headless FastAPI REST Microservice**: Production-grade REST API with interactive Swagger documentation (`/docs`).

---

## 5. Technology Stack
- **Frontend**: Streamlit
- **Backend REST Microservice**: FastAPI + Uvicorn
- **Stochastic & Computational Math**: NumPy, Pure Python, Pydantic V2
- **Visualization**: Plotly Interactive Charts
- **Persistence**: SQLite (Migratable to PostgreSQL/Supabase)
- **PDF Reporting**: ReportLab
- **AI Layer**: Provider-agnostic client (Groq / Google Gemini / OpenAI / Offline Fallback)
- **Testing**: Pytest (25/25 automated tests passing)

---

## 6. Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone the repository & create Virtual Environment
```bash
git clone https://github.com/HussainAli-AI/Retirewise-AI.git
cd Retirewise-AI

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional)* Add your `GROQ_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY`. If left blank, RetireWise AI automatically operates in deterministic offline mode with zero external dependencies and zero cloud cost.

---

## 7. Running the Application

Launch the Streamlit dashboard:
```bash
streamlit run app/streamlit_app.py
```
Open your browser at `http://localhost:8501`.

---

## 8. Synthetic Personas Included for Demo
RetireWise AI comes preloaded with three synthetic client profiles:
1. **Persona A — Tariq Mahmood (Conservative Retiree)**: Age 62, PKR 20M capital, low risk tolerance, conservative capacity.
2. **Persona B — Ayesha Siddiqui (Moderate Near-Retiree)**: Age 54, senior corporate executive with balanced portfolio and high capacity.
3. **Persona C — Kamran Aslam (Suitability Conflict Case)**: High psychological risk tolerance (Score 90) but very low objective capacity for loss (Score 20) with severe liquidity deficits.

---

## 9. Running Tests
To run the complete automated test suite (25 tests covering math, capacity, Monte Carlo, Shariah, and FastAPI):
```bash
pytest tests/ -v
```

---

## 10. Running the FastAPI REST Microservice
RetireWise AI includes a headless FastAPI service for banking and AMC integration:
```bash
uvicorn api.main:app --port 8000 --reload
```
Interactive OpenAPI / Swagger documentation is available at:
`http://localhost:8000/docs`

---

## 11. Project Architecture & Directory Structure
```text
Retirewise-AI/
├── .env.example              # Template environment variables
├── requirements.txt          # Python dependencies
├── LICENSE                   # Apache 2.0 Open-Source License
├── README.md                 # Institutional documentation & guide
├── RetireWise_AI_Product_Requirements_Document_PRD.pdf  # Comprehensive PRD
├── RetireWise_AI_Presentation_Deck.pdf                 # Executive Pitch Deck
│
├── api/                      # Headless REST Microservice
│   └── main.py               # FastAPI router & OpenAPI endpoints (/docs)
│
├── app/                      # Streamlit User Interface
│   ├── streamlit_app.py      # Main dashboard & multi-tab navigation
│   └── ui_components.py      # Theme-adaptive cards, inputs & Plotly charts
│
├── pages/                    # Multi-page Streamlit Apps
│   └── 1_Client_Onboarding.py # Self-service pre-consultation client portal
│
├── core/                     # Deterministic Calculation Engines
│   ├── models.py             # Pydantic V2 data models & type schemas
│   ├── risk_engine.py        # 8-question psychometric attitude-to-risk (0-100)
│   ├── capacity_engine.py    # Objective capacity for loss & liquidity scoring
│   ├── suitability_matrix.py # Conflict detection (Risk Appetite vs. Capacity)
│   ├── cashflow_engine.py    # Multi-year compounding & depletion forecast
│   ├── stress_engine.py      # 5 Pakistan stress scenarios
│   ├── monte_carlo_engine.py # 1,000-trial vectorized stochastic engine
│   ├── digital_twin.py       # Real-time What-If sensitivity sandbox
│   └── shariah_engine.py     # Sovereign Sukuk, KMI-30 & Sec 63 Tax optimizer
│
├── ai/                       # Explainability & Narrative Layer
│   ├── report_generator.py   # Token-condensed LLM prompt dispatcher
│   └── rule_engine.py        # 100% deterministic offline narrative fallback
│
├── data/                     # Database & Default Profiles
│   ├── client_store.py       # SQLite persistence for assessments & clients
│   └── synthetic_data.py     # 3 preloaded Pakistan client test cases
│
├── reports/                  # Audit-Ready PDF Generation
│   ├── pdf_generator.py      # 12-section institutional client advisory PDF
│   ├── generate_prd_pdf.py   # PRD PDF generation script
│   └── generate_presentation_pdf.py # Presentation deck generation script
│
└── tests/                    # Automated Test Suite (25 Tests)
    ├── test_math_verification.py
    ├── test_capacity_engine.py
    ├── test_suitability.py
    ├── test_stress_testing.py
    ├── test_v2_engines.py
    └── verify_monte_carlo.py
```

---

## 12. Version History & Roadmap
- **V1 (Completed)**: Core deterministic engines, Pakistan Fact-Find, 5 stress scenarios, 12-section ReportLab PDF, Streamlit UI.
- **V2 (Completed)**:
  - **1,000-Trial Monte Carlo Engine**: Stochastic simulation with 10th/50th/90th percentile confidence cone and probability of success %.
  - **Financial Digital Twin**: Real-time What-If sandbox (retirement age shifts, expense scaling, lump-sum events).
  - **Pakistan Shariah & Asset Allocation**: Sovereign Sukuks, KMI-30 equities, VPS sub-funds, and Section 63 ITO tax credit optimizer.
  - **Client Self-Service Portal**: Pre-consultation onboarding flow (`pages/1_Client_Onboarding.py`).
  - **Headless FastAPI REST API**: Endpoints for assessments, Monte Carlo, Shariah allocations, and client management.
- **V3 (Planned)**: Institutional AMC/Bank Multi-Tenant Portals, Compliance Oversight Dashboards.
- **V4 (Planned)**: Core Banking Connectors & Enterprise CRM Integrations.

---

## 13. Regulatory & Safety Disclaimer
RetireWise AI is an open-source decision-support tool. It does not provide autonomous, regulated investment advice or guaranteed future outcomes. Calculations are deterministic mathematical simulations based on user inputs. Advisers must exercise independent judgment before making client recommendations.

---

## 14. License
Distributed under the **Apache License 2.0**. See `LICENSE` for details.
