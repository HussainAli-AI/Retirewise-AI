"""Attitudinal Risk Tolerance questionnaire and scoring engine."""
from typing import Dict, List, Any
from models.assessment import RiskCategory, RiskToleranceResult


RISK_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1_loss_reaction",
        "text": "If your retirement portfolio dropped by 15% in a single quarter due to a market downturn, what would you do?",
        "options": [
            {"label": "Sell everything immediately and move entirely into cash or National Savings", "score": 1},
            {"label": "Sell some high-risk assets and move into lower-risk instruments", "score": 2},
            {"label": "Do nothing and wait for the market to recover", "score": 3},
            {"label": "Consult my adviser and selectively rebalance or buy more at lower valuations", "score": 4},
        ],
    },
    {
        "id": "q2_volatility_comfort",
        "text": "How comfortable are you seeing the value of your investments fluctuate on a monthly basis?",
        "options": [
            {"label": "Extremely uncomfortable; I lose sleep over any nominal loss", "score": 1},
            {"label": "Somewhat uneasy; I prefer guaranteed stability even if returns are lower", "score": 2},
            {"label": "Reasonably comfortable; I understand market cycles and short-term volatility", "score": 3},
            {"label": "Very comfortable; volatility is an expected trade-off for higher long-term growth", "score": 4},
        ],
    },
    {
        "id": "q3_investment_experience",
        "text": "What is your prior experience with market-linked investments (e.g. equities, mutual funds, Sukuk)?",
        "options": [
            {"label": "None — I have only used bank savings accounts or cash", "score": 1},
            {"label": "Limited — mostly fixed deposits, prize bonds, or National Savings certificates", "score": 2},
            {"label": "Moderate — experience with mutual funds, VPS, or real estate rental yields", "score": 3},
            {"label": "Extensive — active experience in equity mutual funds, individual stocks, or business equity", "score": 4},
        ],
    },
    {
        "id": "q4_financial_knowledge",
        "text": "How would you rate your understanding of inflation, asset allocation, and market returns?",
        "options": [
            {"label": "Very basic or unfamiliar with financial concepts", "score": 1},
            {"label": "Basic understanding; familiar with bank interest rates and inflation erosion", "score": 2},
            {"label": "Good understanding; I understand the relationship between risk, inflation, and returns", "score": 3},
            {"label": "Advanced; I understand sequence-of-returns risk, real returns, and portfolio diversification", "score": 4},
        ],
    },
    {
        "id": "q5_horizon_perspective",
        "text": "When thinking about your retirement capital, what is your investment horizon perspective?",
        "options": [
            {"label": "Short-term: I need absolute certainty over the next 1–3 years", "score": 1},
            {"label": "Medium-term: 3–5 years, with low tolerance for drawdowns", "score": 2},
            {"label": "Long-term: 5–10 years, focused on beating inflation over time", "score": 3},
            {"label": "Multi-decade: 10+ years, preserving real purchasing power for life and legacy", "score": 4},
        ],
    },
    {
        "id": "q6_return_expectation",
        "text": "Which portfolio performance scenario would you prefer for your retirement funds?",
        "options": [
            {"label": "Portfolio A: Guarantees 8% return, with 0% chance of capital loss", "score": 1},
            {"label": "Portfolio B: Averages 11% return, with a slight chance of 5% loss in a bad year", "score": 2},
            {"label": "Portfolio C: Averages 15% return, with a potential 12% loss in a bad year", "score": 3},
            {"label": "Portfolio D: Averages 19% return, with a potential 25% loss in a bad year", "score": 4},
        ],
    },
    {
        "id": "q7_stability_vs_growth",
        "text": "What is your primary financial priority in retirement?",
        "options": [
            {"label": "100% Capital Preservation: Never accept a decline in nominal account balance", "score": 1},
            {"label": "Cautious Income: Steady income with minimal risk to initial capital", "score": 2},
            {"label": "Balanced: Balance steady income generation with moderate inflation-beating growth", "score": 3},
            {"label": "Aggressive Growth: Maximize long-term wealth growth, even if income is variable", "score": 4},
        ],
    },
    {
        "id": "q8_inflation_drawdown_tradeoff",
        "text": "Inflation in Pakistan can erode purchasing power significantly. How do you view this risk?",
        "options": [
            {"label": "I fear nominal market losses more than the slow erosion of inflation", "score": 1},
            {"label": "I want some inflation protection, but cannot tolerate substantial market drops", "score": 2},
            {"label": "I recognize inflation is the greatest long-term risk to my retirement and accept volatility", "score": 3},
            {"label": "I actively seek high-yielding equity/real asset investments to strongly outpace inflation", "score": 4},
        ],
    },
]


def calculate_risk_tolerance(responses: Dict[str, int]) -> RiskToleranceResult:
    """
    Computes attitudinal risk tolerance score from responses (1-4 scale per question).
    Normalized score ranges from 0.0 to 100.0.
    """
    total_score = 0
    max_possible = len(RISK_QUESTIONS) * 4
    min_possible = len(RISK_QUESTIONS) * 1

    dimension_scores: Dict[str, float] = {}

    for q in RISK_QUESTIONS:
        qid = q["id"]
        val = int(responses.get(qid, 2))  # default to conservative/moderate option if missing
        val = max(1, min(4, val))
        total_score += val
        dimension_scores[qid] = float(val)

    # Normalize between 0 and 100
    normalized_score = ((total_score - min_possible) / (max_possible - min_possible)) * 100.0
    normalized_score = round(max(0.0, min(100.0, normalized_score)), 2)

    # Categorize
    if normalized_score <= 20.0:
        category = RiskCategory.VERY_CONSERVATIVE
        summary = "Client exhibits very low willingness to take financial risk. Prioritizes nominal capital preservation above all else."
    elif normalized_score <= 40.0:
        category = RiskCategory.CONSERVATIVE
        summary = "Client has a conservative attitude toward risk. Prefers stable, predictable income and modest drawdown exposure."
    elif normalized_score <= 60.0:
        category = RiskCategory.MODERATE
        summary = "Client possesses a balanced risk tolerance, accepting moderate market fluctuations in pursuit of inflation-matching returns."
    elif normalized_score <= 80.0:
        category = RiskCategory.GROWTH
        summary = "Client has a growth orientation, willing to withstand meaningful market volatility to preserve purchasing power."
    else:
        category = RiskCategory.AGGRESSIVE
        summary = "Client expresses an aggressive appetite for risk, comfortable with substantial volatility in pursuit of high capital growth."

    return RiskToleranceResult(
        raw_score=float(total_score),
        normalized_score=normalized_score,
        category=category,
        dimension_scores=dimension_scores,
        summary=summary,
    )
