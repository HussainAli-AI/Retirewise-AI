# RetireWise AI (Open-Source MVP)
### Pakistan-Focused Financial Suitability & Retirement Intelligence Platform

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.32%2B-red.svg)](https://streamlit.io/)

---

## 1. What is RetireWise AI?
**RetireWise AI** is an open-source WealthTech & RetirementTech decision-support platform designed for financial advisers, Asset Management Companies (AMCs), pension managers, wealth managers, and insurers in Pakistan. 

It answers the critical retirement question:
> *Given a retiree's income, expenses, assets (Provident Fund, Gratuity, VPS, Gold, Property), liabilities, and dependents in Pakistan, how sustainable is their financial position under macroeconomic and personal stress scenarios?*

### The Cardinal Rule
> **"The LLM explains the numbers; it does not create the numbers."**

RetireWise AI maintains complete separation between **deterministic, transparent Python calculation engines** and the **AI narrative generation layer**.

📄 **[Institutional Product Requirements Document (PRD PDF)](RetireWise_AI_Product_Requirements_Document_PRD.pdf)**

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

## 4. MVP Capabilities
- **Pakistan-Specific Fact-Find (PKR)**: Captures Provident Fund (PF), Gratuity, Voluntary Pension Scheme (VPS), Gold, Property, and Family Dependents.
- **Deterministic Risk Engine (0-100)**: 8-question psychometric attitude-to-risk instrument.
- **Objective Capacity for Loss (0-100)**: Quantifies income dependency, emergency runway, and debt encumbrance.
- **Automated Suitability Conflict Detector**: Immediately flags mismatches (*High Risk Tolerance + Low Capacity for Loss*).
- **Multi-Year Retirement Cash Flow Engine**: Year-by-year compounding simulation predicting capital depletion age and horizon sustainability.
- **5 Stress Testing Scenarios**: Base Case, High Inflation Shock (+5%), Early Market Drawdown (-4%), Healthcare Crisis Shock, and Early Retirement Shock.
- **Provider-Agnostic AI Narrative Layer**: Pluggable support for Google Gemini, OpenAI, or a built-in deterministic rule engine (100% offline).
- **Professional 12-Section PDF Report**: Pixel-accurate, audit-ready ReportLab document export.

---

## 5. Technology Stack
- **Frontend**: Streamlit
- **Visualization**: Plotly Interactive Charts
- **Core Computational Logic**: Pure Python, Pydantic V2
- **Persistence**: SQLite (Migratable to PostgreSQL/Supabase)
- **PDF Reporting**: ReportLab
- **AI Layer**: Provider-agnostic client (Google Gemini / OpenAI / Offline Fallback)
- **Testing**: Pytest

---

## 6. Installation & Setup

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone the repository & create Virtual Environment
```bash
git clone https://github.com/your-org/retirewise-ai.git
cd retirewise-ai

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
*(Optional)* Add your `GEMINI_API_KEY` or `OPENAI_API_KEY`. If left blank, RetireWise AI automatically operates in deterministic offline mode with zero external dependencies.

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
To run the complete automated test suite:
```bash
pytest tests/ -v
```

---

## 10. Future Roadmap
- **V2**: Financial Digital Twin, Client Self-Service Portal, Shariah Asset Allocation Filters.
- **V3**: Institutional AMC/Bank Multi-Tenant Portals, Compliance Oversight Dashboards.
- **V4**: REST API Suite (Risk Profiling API, Capacity API, Stress-Testing API).

---

## 11. Regulatory & Safety Disclaimer
RetireWise AI is an open-source decision-support tool. It does not provide autonomous, regulated investment advice or guaranteed future outcomes. Calculations are deterministic mathematical simulations based on user inputs. Advisers must exercise independent judgment before making client recommendations.

---

## 12. License
Distributed under the **Apache License 2.0**. See `LICENSE` for details.
