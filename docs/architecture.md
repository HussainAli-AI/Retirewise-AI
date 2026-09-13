# RetireWise AI — Architecture Specification

## 1. Architectural Philosophy

RetireWise AI follows a strict **Deterministic Financial Architecture**:
> **"The LLM explains the numbers; it does not create the numbers."**

All financial arithmetic, risk scoring, capacity modeling, and cash flow simulations are executed by deterministic Python engines. The generative AI layer only consumes validated, structured JSON payloads emitted by the engines.

```
+----------------------------------------------------------------+
|                        Adviser / Client Inputs                 |
|             (Streamlit Fact-Find & Risk Questionnaire)         |
+-------------------------------+--------------------------------+
                                |
                                v
+----------------------------------------------------------------+
|                  Validation Engine (core/validation.py)        |
+-------------------------------+--------------------------------+
                                |
                                v
+----------------------------------------------------------------+
|               Deterministic Computational Layer                |
|  - Financial Engine: Net worth, monthly surplus, liquid buffer |
|  - Risk Engine: 8-question attitudinal questionnaire (0-100)   |
|  - Capacity Engine: Objective financial resilience (0-100)     |
|  - Conflict Detector: Identifies High Risk + Low Capacity gaps |
|  - Retirement Engine: Multi-year cash-flow simulation in PKR   |
|  - Scenario Engine: 5 macro and personal stress shock tests    |
+-------------------------------+--------------------------------+
                                |
                                v
+----------------------------------------------------------------+
|                   Structured JSON Result Payload               |
+-------------------------------+--------------------------------+
                                |
                +---------------+---------------+
                |                               |
                v                               v
+-------------------------------+   +----------------------------+
|     AI Explanation Layer      |   |   ReportLab PDF Generator  |
|  - Plain-language narrative   |   |   - 12-section printable   |
|  - Inconsistency audit        |   |     suitability report     |
|  - Provider-agnostic client   |   |   - Audit-ready document   |
+-------------------------------+   +----------------------------+
```

## 2. Directory Layout & Module Boundaries

- `models/`: Pydantic V2 data structures ensuring strict type safety and schema validation.
- `core/`: 100% deterministic, dependency-light financial calculation routines.
- `database/`: SQLite persistence layer for managing client cases, Fact-Find profiles, and assessments.
- `data/`: Synthetic client personas for instant demonstration (Tariq, Ayesha, Kamran).
- `ai/`: Provider-agnostic LLM interface supporting Gemini, OpenAI, and a zero-dependency deterministic fallback.
- `reports/`: ReportLab PDF engine rendering printable, audit-ready suitability documentation.
- `app/`: Interactive Streamlit dashboard with Plotly charts.
- `tests/`: Automated unit test suite verifying mathematical consistency and boundary constraints.
