"""RetireWise AI — Institutional Headless REST API Microservice."""
import os
import sys
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure root path is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import (
    SuitabilityAssessmentResult,
    MonteCarloResult,
    ShariahAllocationResult,
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

app = FastAPI(
    title="RetireWise AI API",
    description="Headless WealthTech & Retirement Suitability Intelligence REST API for Pakistan.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for institutional portal integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database("retirewise.db")


# --- Request Schemas ---
class AssessmentRequest(BaseModel):
    client: ClientProfile
    financial_profile: FinancialProfile
    risk_questionnaire_answers: Dict[str, int] = Field(
        default_factory=dict,
        description="Map of question IDs (q1..q8) to chosen answer score",
    )


class MonteCarloRequest(BaseModel):
    client_id: Optional[str] = None
    trials_count: int = 1000
    override_retirement_age: Optional[int] = None
    override_monthly_expenses: Optional[float] = None


class WhatIfRequest(BaseModel):
    client_id: str
    retirement_age_delta: int = 0
    monthly_expense_multiplier: float = 1.0
    lump_sum_event_amount: float = 0.0
    lump_sum_event_age: Optional[int] = None


class ShariahAllocationRequest(BaseModel):
    client_id: str
    is_shariah_mode: bool = True


# --- Endpoints ---

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RetireWise AI WealthTech Microservice",
        "version": "2.0.0",
        "database": "sqlite_connected",
    }


@app.get("/api/v1/risk-questions", tags=["Risk Profiling"])
def get_risk_questions():
    """Returns the standardized 8-question psychometric attitude-to-risk instrument."""
    return RISK_QUESTIONS


@app.get("/api/v1/clients", tags=["Clients"])
def list_clients():
    """Lists all registered client cases."""
    clients = db.list_clients()
    return [{"client_id": c.client_id, "name": c.name, "age": c.current_age, "ret_age": c.retirement_age} for c in clients]


@app.get("/api/v1/clients/{client_id}", tags=["Clients"])
def get_client(client_id: str):
    """Retrieves full client and financial profile."""
    client = db.get_client(client_id)
    profile = db.get_financial_profile(client_id)
    if not client or not profile:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"client": client, "profile": profile}


@app.post("/api/v1/assessments", response_model=SuitabilityAssessmentResult, tags=["Assessments"])
def run_full_assessment(payload: AssessmentRequest):
    """Runs end-to-end suitability assessment, 2D matrix evaluation, and 5 stress scenarios."""
    errors = validate_client_and_profile(payload.client, payload.financial_profile)
    if errors:
        raise HTTPException(status_code=422, detail=[e.model_dump() for e in errors])

    fh = calculate_financial_health(payload.financial_profile)
    risk_res = calculate_risk_tolerance(payload.risk_questionnaire_answers)
    cap_res = calculate_capacity_for_loss(payload.client, payload.financial_profile)
    warnings, has_conflict = evaluate_suitability_conflicts(risk_res, cap_res, payload.financial_profile, payload.client)
    base_proj = run_retirement_cash_flow_simulation(payload.client, payload.financial_profile)
    scenarios = run_all_stress_scenarios(payload.client, payload.financial_profile)
    mc_res = run_monte_carlo_simulation(payload.client, payload.financial_profile, fh, trials_count=1000)
    shariah_res = calculate_pakistan_asset_allocation(payload.client, payload.financial_profile, fh, cap_res, risk_res)

    result = SuitabilityAssessmentResult(
        assessment_id=f"ASSESS-{payload.client.client_id}-API",
        client_id=payload.client.client_id,
        client_name=payload.client.name,
        created_at="2026-09-13T00:00:00Z",
        financial_health=fh,
        risk_tolerance=risk_res,
        capacity_for_loss=cap_res,
        retirement_projection=base_proj,
        scenarios=scenarios,
        conflict_warnings=warnings,
        has_suitability_conflict=has_conflict,
        suitability_summary="Suitable" if not has_conflict else "Critical Suitability Conflict Detected",
        monte_carlo=mc_res,
        shariah_allocation=shariah_res,
    )
    return result


@app.post("/api/v1/monte-carlo", response_model=MonteCarloResult, tags=["Simulation"])
def run_monte_carlo(req: MonteCarloRequest):
    """Executes vectorized 1,000-trial Monte Carlo stochastic simulation."""
    client_id = req.client_id or "CLIENT-001-TARIQ"
    client = db.get_client(client_id)
    profile = db.get_financial_profile(client_id)
    if not client or not profile:
        raise HTTPException(status_code=404, detail=f"Client '{client_id}' not found")

    fh = calculate_financial_health(profile)
    return run_monte_carlo_simulation(
        client=client,
        financial_profile=profile,
        health=fh,
        trials_count=req.trials_count,
        override_retirement_age=req.override_retirement_age,
        override_monthly_expenses=req.override_monthly_expenses,
    )


@app.post("/api/v1/shariah-allocation", response_model=ShariahAllocationResult, tags=["Asset Allocation"])
def get_shariah_allocation(req: ShariahAllocationRequest):
    """Calculates capacity-governed Pakistani Shariah asset allocation and Section 63 tax rebate."""
    client = db.get_client(req.client_id)
    profile = db.get_financial_profile(req.client_id)
    if not client or not profile:
        raise HTTPException(status_code=404, detail=f"Client '{req.client_id}' not found")

    fh = calculate_financial_health(profile)
    cap_res = calculate_capacity_for_loss(client, profile)
    # Default moderate answers if questionnaire not submitted
    risk_res = calculate_risk_tolerance({"q1": 2, "q2": 2, "q3": 2, "q4": 2, "q5": 2, "q6": 2, "q7": 2, "q8": 2})

    return calculate_pakistan_asset_allocation(
        client=client,
        financial_profile=profile,
        health=fh,
        capacity=cap_res,
        risk=risk_res,
        is_shariah_mode=req.is_shariah_mode,
    )


@app.post("/api/v1/what-if", tags=["Digital Twin"])
def run_what_if_simulation(req: WhatIfRequest):
    """Runs a real-time What-If sensitivity analysis on the client's financial digital twin."""
    client = db.get_client(req.client_id)
    profile = db.get_financial_profile(req.client_id)
    if not client or not profile:
        raise HTTPException(status_code=404, detail=f"Client '{req.client_id}' not found")

    fh = calculate_financial_health(profile)
    return simulate_digital_twin_what_if(
        client=client,
        financial_profile=profile,
        health=fh,
        retirement_age_delta=req.retirement_age_delta,
        monthly_expense_multiplier=req.monthly_expense_multiplier,
        lump_sum_event_amount=req.lump_sum_event_amount,
        lump_sum_event_age=req.lump_sum_event_age,
    )
