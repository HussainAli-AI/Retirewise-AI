"""End-to-end verification script for RetireWise AI."""
from datetime import datetime
from database.database import Database
from data.sample_clients import get_synthetic_personas
from core.financial_engine import calculate_financial_health
from core.risk_engine import calculate_risk_tolerance
from core.capacity_engine import calculate_capacity_for_loss, evaluate_suitability_conflicts
from core.retirement_engine import run_retirement_cash_flow_simulation
from core.scenario_engine import run_all_stress_scenarios
from models.assessment import SuitabilityAssessmentResult
from reports.pdf_generator import generate_suitability_pdf_report
from ai.llm_client import LLMClient
from ai.report_generator import AIReportNarrativeGenerator

def main():
    print("1. Initializing SQLite Database...")
    db = Database("retirewise.db")

    print("2. Loading synthetic personas...")
    personas = get_synthetic_personas()
    latest_assess = None

    for c, p, r_ans in personas:
        db.save_client(c)
        db.save_financial_profile(p)
        fh = calculate_financial_health(p)
        risk = calculate_risk_tolerance(r_ans)
        cap = calculate_capacity_for_loss(c, p)
        warns, conflict = evaluate_suitability_conflicts(risk, cap, p, c)
        proj = run_retirement_cash_flow_simulation(c, p)
        scens = run_all_stress_scenarios(c, p)

        latest_assess = SuitabilityAssessmentResult(
            assessment_id=f"ASSESS-{c.client_id}",
            client_id=c.client_id,
            client_name=c.name,
            created_at=datetime.now().isoformat(),
            financial_health=fh,
            risk_tolerance=risk,
            capacity_for_loss=cap,
            retirement_projection=proj,
            scenarios=scens,
            conflict_warnings=warns,
            has_suitability_conflict=conflict,
            suitability_summary="Suitability conflict detected" if conflict else "Suitable",
        )
        db.save_assessment(latest_assess)
        print(f"   -> Saved: {c.name} | Conflict: {conflict} | Solvency: {proj.sustainability_years} yrs")

    print("3. Testing ReportLab PDF Generation...")
    pdf_bytes = generate_suitability_pdf_report(
        client=personas[2][0],
        profile=personas[2][1],
        assessment=latest_assess,
        output_path="test_report_persona_c.pdf",
    )
    print(f"   -> PDF successfully written (Size: {len(pdf_bytes)} bytes)")

    print("4. Testing AI Narrative Generation (Deterministic Fallback / LLM)...")
    llm = LLMClient()
    gen = AIReportNarrativeGenerator(llm)
    narrative = gen.generate_assessment_explanation(latest_assess)
    print(f"   -> AI Narrative generated ({len(narrative)} chars)")

    print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
