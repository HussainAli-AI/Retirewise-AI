"""Unit tests for the FastAPI REST microservice endpoints."""
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"


def test_api_risk_questions():
    res = client.get("/api/v1/risk-questions")
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) == 8


def test_api_clients_list():
    res = client.get("/api/v1/clients")
    assert res.status_code == 200
    clients = res.json()
    assert isinstance(clients, list)
    assert len(clients) >= 3


def test_api_monte_carlo():
    payload = {"client_id": "CLIENT-001-TARIQ", "trials_count": 50}
    res = client.post("/api/v1/monte-carlo", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "probability_of_success_pct" in data
    assert "percentile_trajectories" in data


def test_api_shariah_allocation():
    payload = {"client_id": "CLIENT-001-TARIQ", "is_shariah_mode": True}
    res = client.post("/api/v1/shariah-allocation", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "capacity_equity_ceiling_pct" in data
    assert "recommended_allocations" in data
    assert len(data["recommended_allocations"]) > 0


def test_api_what_if():
    payload = {
        "client_id": "CLIENT-001-TARIQ",
        "retirement_age_delta": 2,
        "monthly_expense_multiplier": 0.9,
    }
    res = client.post("/api/v1/what-if", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "what_if_probability_of_success_pct" in data
    assert data["adjusted_retirement_age"] == 63
