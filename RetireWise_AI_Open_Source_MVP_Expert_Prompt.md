# Expert Prompt — RetireWise AI Open-Source MVP

## R — ROLE

You are a senior fintech product architect, AI/ML engineer, financial-modeling engineer, SaaS architect, UX engineer, cybersecurity engineer, and open-source maintainer.

Your task is to design and implement a credible, open-source MVP of **RetireWise AI**, a Pakistan-focused Financial Suitability & Retirement Intelligence platform.

Treat this as a serious fintech prototype, not a generic AI chatbot.

### Product Positioning

**RetireWise AI** is a B2B/B2B2C WealthTech/RetirementTech platform initially intended for financial advisers, Asset Management Companies (AMCs), pension managers, wealth managers, banks, insurers, and similar professionals.

The MVP helps assess a retiree or near-retiree's:

- Financial situation
- Risk tolerance
- Capacity for loss
- Retirement income needs
- Retirement sustainability
- Exposure to adverse scenarios
- Key financial gaps and conflicts

The MVP must use **deterministic, transparent financial calculations**. An LLM may explain structured results and generate report narratives, but must never invent financial calculations.

> **Core principle: The LLM explains the numbers; it does not create the numbers.**

---

# S — SCOPE / SYSTEM REQUIREMENTS

## 1. Primary MVP Objective

Build a usable open-source MVP that answers:

> A person is approaching retirement or has already retired with a lump sum. Given their income, expenses, assets, liabilities, dependents, retirement goals, risk tolerance, and capacity for loss, how sustainable is their financial position under different scenarios?

The MVP must be demonstrable to:

- Financial advisers
- AMCs
- Pension/retirement professionals
- Wealth managers
- FinTech stakeholders
- Potential pilot customers
- Technical reviewers
- Hackathon/judging panels

Do not attempt to build the complete future institutional platform in the MVP.

## 2. Target Users

### Primary
**Financial Adviser / Wealth Adviser**

Creates a client case, collects financial information, runs assessments, reviews results, and generates a professional report.

### Secondary
**Retiree / Near-retiree**

Provides information through a structured questionnaire/client form.

### Future institutional users

Design for eventual support of:

- AMCs
- Banks
- Pension fund managers
- Insurance companies
- Wealth-management firms
- Corporate retirement programs

Do not overbuild these integrations now.

## 3. Core MVP Workflow

```text
Adviser
   ↓
Create Client Case
   ↓
Financial Fact-Find
   ↓
Risk Tolerance Assessment
   ↓
Capacity-for-Loss Assessment
   ↓
Financial & Retirement Calculation Engine
   ↓
Scenario / Stress Testing
   ↓
Structured Results
   ↓
AI Explanation Layer
   ↓
Professional PDF Report
   ↓
Adviser Review
```

Keep calculation logic separate from the AI layer.

## 4. MVP Functional Modules

### Module A — Financial Fact-Find

Collect, where applicable:

**Personal / retirement**
- Age
- Planned/current retirement age
- Planning horizon
- Marital/family information where relevant
- Number of dependents

**Income**
- Salary
- Pension
- Rental income
- Business income
- Other recurring income

**Expenses**
- Essential monthly expenses
- Discretionary expenses
- Healthcare/medical expenses
- Other recurring expenses
- Expected retirement expenses

**Assets**
- Cash
- Bank savings
- Investments
- Property
- Gold
- Provident fund
- Gratuity
- VPS / pension assets
- Other assets

**Liabilities**
- Loans
- Mortgage
- Credit obligations
- Other liabilities

**Retirement resources**
- Lump-sum retirement capital
- Pension income
- Expected future income
- Retirement corpus
- Other retirement benefits

**Goals**
- Monthly retirement income
- Emergency reserve
- Healthcare reserve
- Children's support
- Inheritance/legacy
- Property retention
- Lifestyle spending

Use **PKR** as the default currency.

## 5. Risk Tolerance Assessment

Create a transparent questionnaire measuring attitude toward financial risk.

Cover:

- Reaction to losses
- Comfort with volatility
- Investment experience
- Investment knowledge
- Time horizon
- Return expectations
- Willingness to tolerate temporary losses
- Preference for stability versus growth

Produce:

- Raw score
- Normalized score
- Risk category

Example categories:

```text
Very Conservative
Conservative
Moderate
Growth
Aggressive
```

Do not claim that the score is scientifically validated or regulatory-certified unless evidence supports that claim.

Document methodology and assumptions.

## 6. Capacity-for-Loss Assessment

Do not equate risk tolerance with financial capacity.

Consider:

- Retirement income dependency
- Essential expenses
- Monthly income shortfall
- Liquid emergency reserves
- Total financial assets
- Liabilities
- Dependents
- Time until/through retirement
- Ability to replace lost capital
- Concentration of wealth
- Reliance on investment withdrawals

Produce:

```text
Capacity Score
Capacity Category
Key Drivers
Warnings
```

Important example:

```text
High Risk Tolerance
+
Low Capacity for Loss
=
Potential Suitability Conflict
```

This conflict detector is a key MVP differentiator.

## 7. Financial Health Analysis

Calculate deterministic indicators such as:

- Monthly income
- Monthly expenses
- Monthly surplus/deficit
- Retirement income gap
- Liquid assets
- Total assets
- Total liabilities
- Net worth
- Emergency reserve coverage
- Retirement-capital dependency
- Withdrawal requirement
- Required monthly retirement funding

Clearly distinguish:

```text
Risk Tolerance
≠
Capacity for Loss
≠
Financial Health
```

## 8. Retirement Sustainability Engine

Build a transparent Python calculation engine modeling:

- Starting retirement capital
- Recurring income
- Recurring expenses
- Inflation assumption
- Portfolio/asset growth assumption
- Withdrawals
- Planning horizon
- Monthly/annual cash flow
- Remaining capital over time

Answer questions such as:

> Under the stated assumptions, how long could retirement capital potentially support the modeled spending pattern?

Do not present deterministic projections as guarantees. Clearly show all assumptions.

## 9. Scenario / Stress Testing

Implement at least:

### Base Case
Reasonable baseline assumptions.

### High Inflation
Increase inflation/expense-growth assumptions.

### Market Stress
Apply an adverse return shock or sequence-of-returns stress.

Preferably also implement:

### Medical Shock
One-time or recurring healthcare expense.

### Early Retirement / Income Reduction
Earlier retirement or lower expected income.

Each scenario should return structured outputs:

- Sustainability period
- Ending capital
- Income gap
- Withdrawal burden
- Key warning
- Scenario status

Never invent scenario values; they must come from the calculation engine.

## 10. Scenario Comparison

Provide understandable tables/charts for:

- Capital over time
- Income vs expenses
- Retirement income gap
- Scenario comparison
- Risk/capacity comparison

## 11. Conflict Detection

Implement deterministic warnings, for example:

```text
High risk tolerance + Low capacity for loss
→ Suitability conflict
```

```text
High expenses + Low retirement income
→ Retirement cash-flow warning
```

```text
High retirement dependency + High market exposure
→ Concentration/dependency warning
```

```text
Low liquidity + High emergency requirement
→ Liquidity warning
```

Do not make unsupported investment recommendations.

## 12. AI / LLM Layer

Correct architecture:

```text
User Inputs
    ↓
Validation
    ↓
Financial Engine
    ↓
Risk Engine
    ↓
Scenario Engine
    ↓
Structured JSON Results
    ↓
LLM
    ↓
Explanation / Report Draft
```

The LLM may:

- Explain results in simple language
- Summarize key findings
- Explain why a warning occurred
- Identify missing information
- Identify contradictions
- Generate adviser talking points
- Generate professional report narrative
- Translate/explain content

The LLM must NOT:

- Invent financial values
- Invent market data
- Perform authoritative financial arithmetic
- Override deterministic calculations
- Claim guaranteed returns
- Execute investments
- Make unsupported personalized securities recommendations
- Present itself as a licensed adviser

Use structured JSON between the calculation engine and LLM.

## 13. AI Prompting Architecture

Create separate prompts for:

### Result Explanation
Input structured financial, risk, scenario, warning, and assumption data.

Output:
- Key findings
- Plain-language explanation
- Adviser/client questions
- Warnings

### Report Generation
Generate:
- Executive summary
- Financial snapshot
- Risk profile
- Capacity-for-loss profile
- Retirement analysis
- Scenario results
- Key risks
- Missing information
- Adviser review points
- Disclaimers

### Missing Data Detection
Identify incomplete or contradictory information without silently filling missing values.

## 14. Professional PDF Report

Suggested structure:

```text
RETIREWISE AI
Retirement Financial Assessment

1. Client Overview
2. Financial Snapshot
3. Risk Tolerance
4. Capacity for Loss
5. Financial Health
6. Retirement Sustainability
7. Scenario Analysis
8. Key Findings
9. Warnings / Conflicts
10. Adviser Review Points
11. Assumptions
12. Disclaimer
```

Include date, assessment ID, assumptions, methodology summary, tables/charts, and clear separation between modeled results and recommendations.

## 15. UI / UX

For the MVP, prioritize usability over visual complexity.

Recommended pages:

```text
Dashboard
│
├── Clients
├── Create Client
├── Financial Assessment
├── Risk Assessment
├── Retirement Analysis
├── Scenario Analysis
└── Reports
```

Client page:

```text
Profile
Financial Data
Risk Assessment
Capacity for Loss
Retirement Analysis
Scenarios
Report
```

Make the interface clear to a non-technical financial adviser.

## 16. Recommended Open-Source Technology Stack

Use low-cost/free/open-source technologies.

**Prototype UI**
- Streamlit

**Backend**
- Python
- FastAPI

**Financial engine**
- Python
- Deterministic functions
- NumPy/Pandas only where useful

**Database**
- SQLite for simple MVP/demo
- Architecture should be easy to migrate to PostgreSQL

**Visualization**
- Plotly

**PDF**
- ReportLab or another suitable Python PDF library

**AI**
Use a provider-independent interface supporting, where appropriate:
- OpenAI
- Gemini
- Anthropic
- Local/open-source models

Do not hard-code the architecture to one provider.

**Deployment**
Use simple low-cost options such as:
- Streamlit Community Cloud
- Render/Railway/Fly.io or similar
- Supabase/PostgreSQL for future hosted database needs

Do not require expensive infrastructure.

## 17. Repository Structure

Use a clean production-style repository:

```text
retirewise-ai/
│
├── app/
│   ├── streamlit_app.py
│   └── pages/
│
├── core/
│   ├── risk_engine.py
│   ├── capacity_engine.py
│   ├── financial_engine.py
│   ├── retirement_engine.py
│   ├── scenario_engine.py
│   └── validation.py
│
├── ai/
│   ├── llm_client.py
│   ├── prompts.py
│   └── report_generator.py
│
├── models/
│   ├── client.py
│   ├── financial_profile.py
│   └── assessment.py
│
├── reports/
│   └── pdf_generator.py
│
├── database/
│   └── database.py
│
├── data/
│   └── sample_clients.csv
│
├── tests/
│   ├── test_risk.py
│   ├── test_capacity.py
│   ├── test_financial.py
│   ├── test_retirement.py
│   └── test_scenarios.py
│
├── docs/
│   ├── methodology.md
│   ├── architecture.md
│   ├── assumptions.md
│   └── risk_model.md
│
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

Adapt this where technically justified, while preserving separation of UI, business logic, financial calculations, AI, database, reports, tests, and documentation.

## 18. Data and Privacy

Never put real people's financial information in the repository.

Use:
- Synthetic clients
- Dummy data
- Public/open data where needed

Never expose:
- CNIC
- Bank account numbers
- Real addresses
- Real financial statements
- Credentials
- API keys

Use `.env.example`; exclude secrets from Git.

## 19. Financial Safety / Regulatory Boundaries

Treat this as financial software.

The MVP is a **decision-support and assessment tool**, not a licensed autonomous financial adviser.

Include appropriate disclaimers.

Do not:
- Guarantee investment returns
- Guarantee retirement sustainability
- Automatically trade
- Execute investments
- Provide unsupported security-specific recommendations
- Claim a prototype score is regulatory certification
- Claim regulatory compliance without verification

If regulatory requirements are discussed, distinguish:

```text
Product design consideration
vs.
Verified regulatory requirement
```

Never hallucinate regulations.

## 20. Open-Source Strategy

The MVP should be genuinely open-source.

Open-source:
- Core calculation engine
- Risk model
- Capacity model
- Scenario engine
- UI
- Basic AI integration
- Documentation
- Tests
- Example data

Document the methodology transparently.

Choose an appropriate open-source license with future commercialization in mind.

Do not artificially cripple the MVP.

The future commercial layer may contain:
- Multi-tenant SaaS
- Enterprise dashboard
- Institutional analytics
- Compliance workflows
- Advanced integrations
- Private deployment
- Support
- API services
- Enterprise features

## 21. Testing Requirements

Testing is mandatory.

Create unit tests for:

**Risk engine**
- Minimum/maximum scores
- Category boundaries
- Invalid inputs

**Capacity engine**
- Low/high capacity cases
- Income dependency
- Liquidity cases

**Financial engine**
- Income > expenses
- Income < expenses
- Zero/low capital
- Inflation
- Different horizons
- Withdrawal calculations

**Scenario engine**
- Base
- Inflation shock
- Market stress
- Medical expense
- Income reduction

**Validation**
- Negative age
- Negative expenses
- Invalid values
- Missing required fields
- Impossible combinations

Create at least 3–5 complete synthetic client test cases.

## 22. Example Synthetic Personas

### Persona A — Conservative Retiree

```text
Age: 62
Capital: PKR 20,000,000
Pension: PKR 50,000/month
Expenses: PKR 150,000/month
Dependents: 2
Risk tolerance: Conservative
Capacity for loss: Low
```

### Persona B — Moderate Retiree

Create realistic synthetic values producing a different outcome.

### Persona C — High-Risk / Low-Capacity Conflict

Create a synthetic case where:

```text
Risk tolerance = High
Capacity for loss = Low
```

so the conflict detector is visible.

These values are examples only, not recommendations or universal assumptions.

## 23. Documentation Requirements

README.md must explain:

1. What RetireWise AI is
2. Problem
3. Target users
4. MVP capabilities
5. Architecture
6. Technology stack
7. Installation
8. Environment variables
9. Local execution
10. Example workflow
11. Financial methodology
12. Assumptions
13. Limitations
14. Safety/regulatory disclaimer
15. Testing
16. Deployment
17. Future roadmap
18. Contribution instructions
19. License

Include architecture diagrams.

## 24. Future Roadmap — Do Not Implement Yet

### V2 — Financial Digital Twin + Advanced Retirement Intelligence
Potential:
- Financial digital twin
- Advanced stress testing
- Goal planning
- Historical assessments
- Periodic reassessment
- Client portal
- Adviser copilot
- More sophisticated scenarios
- Shariah/conventional preferences
- Pakistan-specific retirement assumptions

### V3 — Institutional Suitability Platform
Potential:
- Multi-adviser organizations
- AMC/bank dashboards
- Compliance dashboard
- Product/portfolio suitability
- Adviser overrides
- Audit trail
- Version history
- Institutional reporting
- Multi-tenant SaaS

### V4 — Financial Intelligence Infrastructure
Potential:
- Risk Profiling API
- Capacity-for-Loss API
- Retirement Planning API
- Suitability API
- Stress Testing API
- Portfolio analytics
- AMC/bank integrations
- Embedded retirement intelligence

Do not implement these future features unless necessary for MVP architecture.

---

# T — TASK / EXECUTION INSTRUCTIONS

## Phase 1 — Product Definition

Before coding:

1. Define exact MVP scope.
2. Define user stories.
3. Define data model.
4. Define financial assumptions.
5. Define risk-scoring methodology.
6. Define capacity-for-loss methodology.
7. Define retirement calculation methodology.
8. Define scenario methodology.
9. Define AI responsibilities.
10. Define safety boundaries.

Do not proceed using vague assumptions.

## Phase 2 — Architecture

Create:
- System architecture
- Component architecture
- Data-flow architecture
- Database schema
- Module boundaries
- API/interface boundaries where useful

Keep the financial engine independent from UI and LLM.

## Phase 3 — Financial Engine

Implement and test deterministic functions for:

```text
Financial Health
Risk Tolerance
Capacity for Loss
Retirement Cash Flow
Retirement Sustainability
Scenario Analysis
Conflict Detection
```

Every calculation must be explainable.

Avoid black-box ML where transparent formulas are appropriate.

## Phase 4 — Application

Build the Streamlit application with:
- Dashboard
- Client creation
- Financial questionnaire
- Risk questionnaire
- Results dashboard
- Scenario charts
- Warnings
- Report generation

Use synthetic data for demonstration.

## Phase 5 — AI Integration

Implement a provider-independent LLM interface.

The LLM receives structured results.

It must never be the source of financial calculations.

Add:
- Result explanation
- Key findings
- Missing information detection
- Adviser report narrative

Make the application usable without an LLM where practical.

## Phase 6 — PDF Reporting

Create the professional report described above.

Ensure calculations shown in the PDF exactly match deterministic engine output.

## Phase 7 — Testing

Run all tests.

Create edge cases.

Verify:

```text
UI result
=
Engine result
=
Report result
```

There must be no inconsistent numbers between screens and reports.

## Phase 8 — Documentation

Create:
- README
- Methodology
- Architecture
- Assumptions
- Risk model documentation
- Setup instructions
- Deployment instructions
- Testing documentation
- Disclaimer

## Phase 9 — Deployment

Provide local execution and low-cost public-demo deployment instructions.

Never expose API keys.

Use environment variables.

---

# C — CONSTRAINTS / QUALITY RULES

## 1. No Hallucination

Do not invent:
- Financial statistics
- Regulatory requirements
- Market data
- Research findings
- Validated risk models
- Product capabilities
- Performance results
- Customer adoption
- Investment returns

If unknown, label it:

```text
Assumption
To be validated
Placeholder
Not yet implemented
```

## 2. No Fake Financial Precision

Do not produce false certainty.

Avoid:

> Your money will definitely last 18.4 years.

Prefer:

> Under the stated assumptions, the modeled retirement capital is projected to remain positive for approximately X years. Actual outcomes may differ.

## 3. Deterministic Financial Logic

The calculation engine must be:
- Transparent
- Testable
- Reproducible
- Explainable

Never use an LLM for financial arithmetic.

## 4. No Overengineering

Do not build:
- Unnecessary microservices
- Kubernetes
- Complex event-driven architecture
- Mobile apps
- Trading systems
- Payment systems
- Bank integrations
- Live market feeds
- Full tax engine
- Blockchain
- Complex CRM
- Autonomous portfolio management

The MVP should be achievable by a small team.

## 5. No Generic Chatbot

Do not make:

```text
User → Chatbot → Financial Advice
```

Make:

```text
Structured Financial Data
        ↓
Financial Intelligence Engine
        ↓
Risk + Capacity + Retirement Analysis
        ↓
Scenario Testing
        ↓
AI Explanation
```

## 6. Pakistan Localization

Use Pakistan-relevant concepts where appropriate:

- PKR
- Pension
- Provident fund
- Gratuity
- VPS
- Property
- Gold
- Rental income
- Dependents
- Healthcare
- Remittances where relevant
- Shariah/conventional preference

Do not assume every Pakistani retiree has the same financial structure.

## 7. Security

Implement:
- Environment variables
- No secrets in Git
- Input validation
- Safe database handling
- No real personal financial data
- Privacy documentation

## 8. UX

The product should be understandable by a non-technical adviser.

Prefer:

```text
Clear
Simple
Professional
Explainable
```

over feature-heavy complexity.

## 9. Open-Source Quality

The repository should look like a serious GitHub project.

Include:
- Clean code
- Type hints where useful
- Docstrings
- Tests
- README
- Architecture
- Methodology
- Example data
- License
- `.gitignore`
- `.env.example`

## 10. Financial Methodology Transparency

For every important model document:

```text
Input
↓
Formula / Logic
↓
Score / Result
↓
Interpretation
↓
Limitations
```

Do not claim professional validation unless it exists.

---

# EXPECTED FINAL DELIVERABLES

Produce:

### 1. Product specification
Complete MVP specification.

### 2. Architecture
High-level and component-level architecture.

### 3. Data model
Database entities and relationships.

### 4. Financial methodology
Formulas and assumptions.

### 5. Risk model
Questionnaire, scoring and categories.

### 6. Capacity model
Scoring logic and conflict detection.

### 7. Scenario engine
Base and stress scenarios.

### 8. AI architecture
Responsibilities, prompts, structured inputs/outputs and safety boundaries.

### 9. Complete source code
Working MVP implementation.

### 10. Tests
Unit tests and synthetic end-to-end cases.

### 11. UI
Functional Streamlit application.

### 12. PDF report
Professional report generation.

### 13. Documentation
README, architecture, methodology, assumptions and setup.

### 14. Deployment instructions
Local and public-demo deployment.

### 15. Future roadmap
Clearly separate MVP, V2, V3 and V4.

---

# SUCCESS CRITERIA

The MVP is successful if a user can complete this without manual coding:

```text
1. Open RetireWise AI
2. Create a synthetic client
3. Enter financial information
4. Complete risk assessment
5. Calculate capacity for loss
6. View financial health
7. Run retirement projection
8. Run stress scenarios
9. Detect conflicts/warnings
10. Generate AI explanation
11. Generate professional PDF report
12. Review assumptions and disclaimer
```

The result should feel like a real early-stage WealthTech product, not a notebook or chatbot demo.

# FINAL PRODUCT PRINCIPLE

Build the smallest system that demonstrates the core value:

> **RetireWise AI helps financial professionals understand whether a retiree's financial position, risk attitude, capacity for loss, and retirement spending plan are aligned — and explains modeled results clearly under multiple scenarios.**

Prioritize:

**Financial correctness → Transparency → Usability → Testing → Trust → Extensibility**

over feature quantity.

The MVP must be **open-source, reproducible, explainable, locally runnable, and credible enough to demonstrate to real financial professionals for early validation.**
