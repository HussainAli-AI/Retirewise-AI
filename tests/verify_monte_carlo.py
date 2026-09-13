"""Standalone verification script for Monte Carlo & Digital Twin sensitivity."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import Database
from core.monte_carlo_engine import run_monte_carlo_simulation
from core.digital_twin import simulate_digital_twin_what_if
from core.financial_engine import calculate_financial_health

def main():
    db = Database("retirewise.db")

    print("================================================================")
    print("1. RUNNING MONTE CARLO (1,000 TRIALS) ACROSS ALL 3 PERSONAS")
    print("================================================================")

    for pid in ["CLIENT-001-TARIQ", "CLIENT-002-AYESHA", "CLIENT-003-KAMRAN"]:
        c = db.get_client(pid)
        p = db.get_financial_profile(pid)
        fh = calculate_financial_health(p)
        mc = run_monte_carlo_simulation(c, p, fh, trials_count=1000, seed=42)
        print(f"\n--- {c.name} ({pid}) ---")
        print(f"  • Net Investable Capital: PKR {fh.net_investable_retirement_capital_pkr:,.0f}")
        print(f"  • Monthly Ret. Gap:       PKR {fh.monthly_retirement_income_gap_pkr:,.0f}/mo")
        print(f"  • Probability of Success: {mc.probability_of_success_pct}%")
        print(f"  • Median Depletion Age:   {mc.median_depletion_age if mc.median_depletion_age else 'Solvent through 85+'}")
        print(f"  • Median Ending Capital:  PKR {mc.median_ending_capital_pkr:,.0f}")
        print(f"  • 10th Percentile (Bear): PKR {mc.p10_ending_capital_pkr:,.0f}")
        print(f"  • 90th Percentile (Bull): PKR {mc.p90_ending_capital_pkr:,.0f}")
        print(f"  • Verdict:                {mc.confidence_verdict}")

    print("\n================================================================")
    print("2. TESTING DIGITAL TWIN SENSITIVITY & WHAT-IF LOGIC (Tariq)")
    print("================================================================")

    c = db.get_client("CLIENT-001-TARIQ")
    p = db.get_financial_profile("CLIENT-001-TARIQ")
    fh = calculate_financial_health(p)
    base_mc = run_monte_carlo_simulation(c, p, fh, trials_count=1000, seed=42)
    print(f"Baseline (Retire at {c.retirement_age}, Normal Expenses): {base_mc.probability_of_success_pct}% Success")

    # Test 1: Delay Retirement by 3 years
    dt_delay = simulate_digital_twin_what_if(c, p, fh, retirement_age_delta=3, trials_count=500)
    delta_delay = dt_delay["what_if_probability_of_success_pct"] - base_mc.probability_of_success_pct
    print(f"  [+] Delay Retirement +3 yrs (Age {dt_delay['adjusted_retirement_age']}): {dt_delay['what_if_probability_of_success_pct']}% ({delta_delay:+.1f}%)")
    assert dt_delay["what_if_probability_of_success_pct"] >= base_mc.probability_of_success_pct, "Delaying retirement should improve or maintain solvency"

    # Test 2: Frugal Expenses (-25%)
    dt_frugal = simulate_digital_twin_what_if(c, p, fh, monthly_expense_multiplier=0.75, trials_count=500)
    delta_frugal = dt_frugal["what_if_probability_of_success_pct"] - base_mc.probability_of_success_pct
    print(f"  [+] Frugal Expenses -25%:                                 {dt_frugal['what_if_probability_of_success_pct']}% ({delta_frugal:+.1f}%)")
    assert dt_frugal["what_if_probability_of_success_pct"] >= base_mc.probability_of_success_pct, "Lower expenses should improve solvency"

    # Test 3: Lifestyle Expansion (+30%)
    dt_expand = simulate_digital_twin_what_if(c, p, fh, monthly_expense_multiplier=1.30, trials_count=500)
    delta_expand = dt_expand["what_if_probability_of_success_pct"] - base_mc.probability_of_success_pct
    print(f"  [-] Lifestyle Burn +30%:                                  {dt_expand['what_if_probability_of_success_pct']}% ({delta_expand:+.1f}%)")
    assert dt_expand["what_if_probability_of_success_pct"] <= base_mc.probability_of_success_pct, "Higher expenses should decrease solvency"

    # Test 4: Lump Sum Inflow (PKR 10M property liquidation at Age 65)
    dt_inflow = simulate_digital_twin_what_if(c, p, fh, lump_sum_event_amount=10_000_000, lump_sum_event_age=65, trials_count=500)
    delta_inflow = dt_inflow["what_if_probability_of_success_pct"] - base_mc.probability_of_success_pct
    print(f"  [+] Inflow +10M PKR at Age 65:                           {dt_inflow['what_if_probability_of_success_pct']}% ({delta_inflow:+.1f}%)")
    assert dt_inflow["what_if_probability_of_success_pct"] >= base_mc.probability_of_success_pct, "Large capital inflow should improve solvency"

    # Test 5: Lump Sum Outflow (-PKR 5M Medical Shock at Age 65)
    dt_outflow = simulate_digital_twin_what_if(c, p, fh, lump_sum_event_amount=-5_000_000, lump_sum_event_age=65, trials_count=500)
    delta_outflow = dt_outflow["what_if_probability_of_success_pct"] - base_mc.probability_of_success_pct
    print(f"  [-] Outflow -5M PKR shock at Age 65:                     {dt_outflow['what_if_probability_of_success_pct']}% ({delta_outflow:+.1f}%)")
    assert dt_outflow["what_if_probability_of_success_pct"] <= base_mc.probability_of_success_pct, "Shock outflow should reduce solvency"

    print("\n================================================================")
    print("ALL TESTS PASSED: MONTE CARLO & DIGITAL TWIN ARE 100% OPERATIONAL!")
    print("================================================================")

if __name__ == "__main__":
    main()
