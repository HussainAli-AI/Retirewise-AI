"""Professional ReportLab PDF generator for RetireWise AI."""
import os
from io import BytesIO
from typing import Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import SuitabilityAssessmentResult


def generate_suitability_pdf_report(
    client: ClientProfile,
    profile: FinancialProfile,
    assessment: SuitabilityAssessmentResult,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Generates a 12-section professional suitability and retirement PDF report.
    If output_path is provided, writes to disk; always returns PDF bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0f2942")     # Deep Navy
    SECONDARY = colors.HexColor("#1b5e20")   # Forest Green
    ACCENT_ALERT = colors.HexColor("#b71c1c")# Alert Red
    BG_LIGHT = colors.HexColor("#f8f9fa")
    BORDER_COLOR = colors.HexColor("#dee2e6")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=PRIMARY,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#555555"),
        spaceAfter=12,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#222222"),
    )
    callout_alert = ParagraphStyle(
        "CalloutAlert",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=ACCENT_ALERT,
    )
    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=colors.white,
    )
    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
    )

    story = []

    # --- Header Banner ---
    story.append(Paragraph("RETIREWISE AI", title_style))
    story.append(Paragraph("Financial Suitability & Retirement Intelligence Assessment (Pakistan B2B Edition)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=10))

    # Assessment Metadata Table
    meta_data = [
        [
            Paragraph(f"<b>Assessment ID:</b> {assessment.assessment_id}", table_cell_style),
            Paragraph(f"<b>Date:</b> {assessment.created_at[:10]}", table_cell_style),
        ],
        [
            Paragraph(f"<b>Client:</b> {client.name}", table_cell_style),
            Paragraph(f"<b>Adviser:</b> {client.adviser_name}", table_cell_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # --- 1. Client Overview ---
    story.append(Paragraph("1. Client Demographic Profile", section_heading))
    client_info = [
        [Paragraph("<b>Current Age:</b>", table_cell_style), Paragraph(str(client.current_age), table_cell_style),
         Paragraph("<b>Retirement Age:</b>", table_cell_style), Paragraph(str(client.retirement_age), table_cell_style)],
        [Paragraph("<b>Planning Horizon:</b>", table_cell_style), Paragraph(f"{client.planning_horizon_age} years", table_cell_style),
         Paragraph("<b>Marital Status:</b>", table_cell_style), Paragraph(client.marital_status.value, table_cell_style)],
        [Paragraph("<b>Dependents:</b>", table_cell_style), Paragraph(str(client.dependents_count), table_cell_style),
         Paragraph("<b>Retirement Status:</b>", table_cell_style), Paragraph("Retired" if client.is_already_retired else f"{client.years_to_retirement} years to retirement", table_cell_style)],
    ]
    t_client = Table(client_info, colWidths=[120, 150, 120, 150])
    t_client.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_client)

    # --- 2. Financial Snapshot ---
    story.append(Paragraph("2. Financial Snapshot (PKR)", section_heading))
    fh = assessment.financial_health
    snapshot_data = [
        [Paragraph("<b>Financial Metric</b>", table_header_style), Paragraph("<b>Value (PKR)</b>", table_header_style), Paragraph("<b>Financial Metric</b>", table_header_style), Paragraph("<b>Value (PKR)</b>", table_header_style)],
        [Paragraph("Total Assets", table_cell_style), Paragraph(f"PKR {fh.total_assets_pkr:,.0f}", table_cell_style), Paragraph("Total Liabilities", table_cell_style), Paragraph(f"PKR {fh.total_liabilities_pkr:,.0f}", table_cell_style)],
        [Paragraph("Net Worth", table_cell_style), Paragraph(f"PKR {fh.net_worth_pkr:,.0f}", table_cell_style), Paragraph("Net Investable Capital", table_cell_style), Paragraph(f"PKR {fh.net_investable_retirement_capital_pkr:,.0f}", table_cell_style)],
        [Paragraph("Liquid Cash & Equivalents", table_cell_style), Paragraph(f"PKR {fh.liquid_assets_pkr:,.0f}", table_cell_style), Paragraph("Monthly Income Surplus", table_cell_style), Paragraph(f"PKR {fh.current_monthly_surplus_pkr:,.0f}", table_cell_style)],
        [Paragraph("Guaranteed Ret. Income / mo", table_cell_style), Paragraph(f"PKR {fh.guaranteed_monthly_retirement_income_pkr:,.0f}", table_cell_style), Paragraph("Projected Ret. Expense / mo", table_cell_style), Paragraph(f"PKR {fh.projected_monthly_retirement_expenses_pkr:,.0f}", table_cell_style)],
    ]
    t_snapshot = Table(snapshot_data, colWidths=[150, 120, 150, 120])
    t_snapshot.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_snapshot)

    # --- 3. Risk Tolerance & 4. Capacity for Loss ---
    story.append(Paragraph("3. Risk Tolerance vs. 4. Capacity for Loss", section_heading))
    rt = assessment.risk_tolerance
    cfl = assessment.capacity_for_loss

    risk_cap_data = [
        [Paragraph("<b>Evaluation Dimension</b>", table_header_style), Paragraph("<b>Score & Category</b>", table_header_style), Paragraph("<b>Key Implication</b>", table_header_style)],
        [
            Paragraph("<b>Risk Tolerance</b><br/>(Psychological Attitude)", table_cell_style),
            Paragraph(f"<b>{rt.normalized_score}/100</b><br/>({rt.category.value})", table_cell_style),
            Paragraph(rt.summary, table_cell_style),
        ],
        [
            Paragraph("<b>Capacity for Loss</b><br/>(Financial Ability)", table_cell_style),
            Paragraph(f"<b>{cfl.capacity_score}/100</b><br/>({cfl.category.value})", table_cell_style),
            Paragraph(f"Income dependency on capital: {cfl.income_dependency_pct}%. Liquid emergency reserve: {cfl.liquid_emergency_months} months.", table_cell_style),
        ],
    ]
    t_risk_cap = Table(risk_cap_data, colWidths=[150, 120, 270])
    t_risk_cap.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_risk_cap)

    # Conflict banner if present
    if assessment.has_suitability_conflict:
        story.append(Spacer(1, 6))
        alert_p = Paragraph(
            "<b>CRITICAL SUITABILITY MISMATCH DETECTED:</b> The client exhibits a higher psychological risk appetite than "
            "their objective financial capacity can endure. Portfolio recommendations must be governed by Capacity for Loss.",
            callout_alert,
        )
        alert_table = Table([[alert_p]], colWidths=[540])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ffebee")),
            ('BOX', (0, 0), (-1, -1), 1, ACCENT_ALERT),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(alert_table)

    # --- 6. Retirement Sustainability & 7. Scenario Analysis ---
    story.append(Paragraph("6. Retirement Sustainability & Stress Scenarios", section_heading))
    scen_rows = [
        [
            Paragraph("<b>Scenario</b>", table_header_style),
            Paragraph("<b>Return / Infl.</b>", table_header_style),
            Paragraph("<b>Solvent Years</b>", table_header_style),
            Paragraph("<b>Depletion Age</b>", table_header_style),
            Paragraph("<b>Terminal Capital</b>", table_header_style),
        ]
    ]
    for s in assessment.scenarios:
        scen_rows.append([
            Paragraph(f"<b>{s.scenario_name}</b>", table_cell_style),
            Paragraph(f"{s.annual_return_rate*100:.1f}% / {s.annual_inflation_rate*100:.1f}%", table_cell_style),
            Paragraph(f"{s.sustainability_years} yrs", table_cell_style),
            Paragraph(f"Age {s.capital_depletion_age}" if s.capital_depletion_age else "No Depletion", table_cell_style),
            Paragraph(f"PKR {s.ending_capital_pkr:,.0f}", table_cell_style),
        ])
    t_scen = Table(scen_rows, colWidths=[160, 90, 80, 90, 120])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_scen)

    # --- 8. Key Findings & AI Narrative ---
    story.append(Paragraph("8. Key Findings & Analytical Narrative", section_heading))
    summary_text = (
        f"{assessment.retirement_projection.summary_verdict}<br/><br/>"
        f"Initial annual portfolio withdrawal demand stands at PKR {fh.monthly_retirement_income_gap_pkr*12:,.0f} "
        f"({fh.annual_withdrawal_rate_pct:.1f}% of investable capital). In Pakistan's macroeconomic environment, withdrawal "
        f"rates exceeding 5-6% without inflation-indexed cash flows experience elevated sequence risk."
    )
    story.append(Paragraph(summary_text, body_style))

    # --- 9. Warnings & Conflicts ---
    if assessment.conflict_warnings:
        story.append(Paragraph("9. Warnings & Identified Vulnerabilities", section_heading))
        for w in assessment.conflict_warnings:
            warn_p = Paragraph(f"<b>[{w.severity.value}] {w.title}:</b> {w.description} <i>Adviser Action: {w.adviser_action}</i>", body_style)
            story.append(warn_p)
            story.append(Spacer(1, 3))

    # --- 10. Adviser Review Points ---
    story.append(Paragraph("10. Adviser Review Points", section_heading))
    review_points = (
        "• Rebalance allocation to prioritize capital preservation until emergency reserve reaches 6 months.<br/>"
        "• Validate expected gratuity/Provident Fund release dates and tax treatments under local law.<br/>"
        "• Review whether investment property yields can be enhanced or reallocated to defensive income funds.<br/>"
        "• Schedule annual review to update inflation assumptions and actual portfolio withdrawals."
    )
    story.append(Paragraph(review_points, body_style))

    # --- 11. Assumptions & Methodology ---
    story.append(Paragraph("11. Assumptions & Deterministic Methodology", section_heading))
    assumptions_text = (
        f"Projections model annual compounding with mid-year withdrawal timing. Baseline expected inflation is set to "
        f"{profile.goals.expected_annual_inflation_rate*100:.1f}% p.a. and nominal investment return is modeled at "
        f"{profile.goals.expected_annual_investment_return*100:.1f}% p.a. (Real return: "
        f"{(profile.goals.expected_annual_investment_return - profile.goals.expected_annual_inflation_rate)*100:.1f}%). "
        "Calculations are deterministic and transparent. No black-box statistical forecasting was employed."
    )
    story.append(Paragraph(assumptions_text, body_style))

    # --- 12. Statutory Disclaimer ---
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=6))
    story.append(Paragraph("12. Important Regulatory & Professional Disclaimer", section_heading))
    disclaimer_text = (
        "<b>CONFIDENTIAL & ADVISORY USE ONLY:</b> RetireWise AI is an open-source financial decision-support tool designed "
        "for licensed financial advisers and wealth managers. This report does not constitute autonomous financial advice, "
        "a guaranteed projection of future returns, or a certified regulatory recommendation. Projections are mathematical "
        "simulations based on user-provided inputs and stated assumptions. Actual financial market returns, taxation, and inflation "
        "will vary. Financial advisers must exercise independent judgment before implementing any client strategy."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle("Disc", parent=body_style, fontSize=7.5, leading=10, textColor=colors.HexColor("#777777"))))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes
