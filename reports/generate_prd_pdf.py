"""Generate an institutional-grade Product Requirements Document (PRD) PDF for RetireWise AI."""
import os
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
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas for adding page numbers and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "RetireWise AI — Product Requirements Document (PRD) v1.0")
            self.setStrokeColor(colors.HexColor("#e0e0e0"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#e0e0e0"))
        self.setLineWidth(0.5)
        self.line(36, 45, 576, 45)
        self.drawString(36, 32, "Confidential — Open-Source WealthTech Specification | Apache 2.0")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 32, page_str)
        self.restoreState()


def build_prd_pdf(output_path: str = "RetireWise_AI_PRD.pdf") -> str:
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0f2942")     # Deep Institutional Navy
    SECONDARY = colors.HexColor("#1b5e20")   # Forest Emerald
    ACCENT = colors.HexColor("#0277bd")      # Tech Blue
    TEXT_DARK = colors.HexColor("#212529")
    TEXT_MUTED = colors.HexColor("#555555")
    BG_LIGHT = colors.HexColor("#f8f9fa")
    BORDER_COLOR = colors.HexColor("#dee2e6")

    # Typography Styles
    title_style = ParagraphStyle(
        "PRDTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "PRDSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=TEXT_MUTED,
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        "PRDH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "PRDH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "PRDBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "PRDBullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
    )

    callout_style = ParagraphStyle(
        "PRDCallout",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY,
    )

    table_header_style = ParagraphStyle(
        "PRDTH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        "PRDTC",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK,
    )

    table_cell_bold = ParagraphStyle(
        "PRDTCB",
        parent=table_cell_style,
        fontName="Helvetica-Bold",
        textColor=PRIMARY,
    )

    story = []

    # --- Header Banner ---
    story.append(Paragraph("RetireWise AI", title_style))
    story.append(Paragraph("Institutional Product Requirements Document (PRD) • Version 1.0", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=12))

    # --- Metadata Table ---
    meta_data = [
        [
            Paragraph("<b>Project:</b> RetireWise AI", table_cell_style),
            Paragraph("<b>Version:</b> 1.0 (MVP Complete) + V2 Roadmap", table_cell_style),
            Paragraph("<b>Classification:</b> Open-Source / Institutional", table_cell_style),
        ],
        [
            Paragraph("<b>Target Market:</b> Pakistan WealthTech / Pensions", table_cell_style),
            Paragraph("<b>License:</b> Apache 2.0 ($0 Cost)", table_cell_style),
            Paragraph("<b>Status:</b> Production Verified", table_cell_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 180])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # --- Section 1: Executive Summary & Mission ---
    story.append(Paragraph("1. Executive Summary & Vision", h1_style))
    story.append(Paragraph(
        "RetireWise AI is an open-source, institutional-grade retirement suitability and cash flow intelligence platform "
        "engineered specifically for the Pakistani macroeconomic environment. Designed for financial advisers, Wealth Managers, "
        "Asset Management Companies (AMCs), and Pension Fund Managers, RetireWise AI bridges the severe retirement readiness "
        "gap in Pakistan by replacing guesswork with transparent, deterministic financial mathematics and verifiable AI explanations.",
        body_style,
    ))

    # Callout: The Cardinal Rule
    cardinal_box = [
        [
            Paragraph(
                "<b>THE CARDINAL SYSTEM RULE:</b><br/>"
                "<i>\"The LLM explains the numbers; it does not create the numbers.\"</i><br/>"
                "All financial mathematics, solvency years, cash flows, and suitability scores are calculated deterministically "
                "in pure Python. The AI layer acts strictly as an audit and narrative translation layer, eliminating hallucination risks entirely.",
                callout_style,
            )
        ]
    ]
    cardinal_table = Table(cardinal_box, colWidths=[540])
    cardinal_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8f0fe")),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(cardinal_table)
    story.append(Spacer(1, 10))

    # --- Section 2: Problem Statement & Pakistan Context ---
    story.append(Paragraph("2. Problem Statement & Market Opportunity", h1_style))
    story.append(Paragraph(
        "Retirement planning in Pakistan faces three critical structural failures that standard Western financial software fails to solve:",
        body_style,
    ))
    story.append(Paragraph("• <b>Conflation of Risk Appetite with Loss Capacity:</b> Advisers routinely allocate retiree portfolios to volatile equities because the client has an 'aggressive attitude,' ignoring that an imminent market crash would permanently deplete their essential living capital.", bullet_style))
    story.append(Paragraph("• <b>Hyper-Inflation & Longevity Compounding:</b> With persistent double-digit inflation cycles in Pakistan (8%–15%+), static projections severely underestimate cost-of-living increases, leading to premature capital depletion in the 60s and 70s.", bullet_style))
    story.append(Paragraph("• <b>Local Instrument Realities:</b> In Pakistan, retirement wealth is concentrated in illiquid property, gold, Provident Funds, Gratuities, and Voluntary Pension Schemes (VPS), requiring local tax and liquidity modeling.", bullet_style))
    story.append(Spacer(1, 10))

    # --- Section 3: Target Personas ---
    story.append(Paragraph("3. Target User Personas", h1_style))
    personas_data = [
        [Paragraph("User Persona", table_header_style), Paragraph("Key Needs & Objectives", table_header_style), Paragraph("Platform Value Delivered", table_header_style)],
        [
            Paragraph("<b>Financial Adviser / Wealth Planner</b>", table_cell_bold),
            Paragraph("Institutional suitability compliance, Fact-Find automation, audit-proof recommendations, and PDF report delivery.", table_cell_style),
            Paragraph("Reduces assessment turnaround from 3 hours to 3 minutes with automated conflict detection and client-ready PDFs.", table_cell_style),
        ],
        [
            Paragraph("<b>Pre-Retiree / Client (Age 45–65)</b>", table_cell_bold),
            Paragraph("Clarity on whether savings will outlive them, realistic inflation expectations, and emergency reserve safety.", table_cell_style),
            Paragraph("Clear, plain-language executive summaries explaining safe withdrawal rates and stress test vulnerabilities.", table_cell_style),
        ],
        [
            Paragraph("<b>Institutional AMC / Pension Fund</b>", table_cell_bold),
            Paragraph("Regulatory compliance (SECP), anti-mis-selling safeguards, standardized risk-capacity scoring, and white-labeling.", table_cell_style),
            Paragraph("Standardized open-source calculation framework with full traceability and offline deployment capability.", table_cell_style),
        ],
    ]
    p_table = Table(personas_data, colWidths=[120, 210, 210])
    p_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 14))

    # --- Section 4: System Architecture & Engine Specifications ---
    story.append(Paragraph("4. Core Functional Modules & Specifications", h1_style))

    story.append(Paragraph("4.1. Attitudinal Risk vs. Objective Capacity for Loss", h2_style))
    story.append(Paragraph(
        "The system evaluates clients along two independent orthogonal axes to produce a 2D Suitability Matrix:<br/>"
        "1. <b>Attitudinal Risk Tolerance (0–100):</b> 8-question psychometric instrument scoring market volatility comfort, time horizon perception, and panic-selling triggers.<br/>"
        "2. <b>Objective Capacity for Loss (0–100):</b> Deterministic algorithmic formula evaluating liquid emergency runway, portfolio income dependency, and debt encumbrance ratio.<br/>"
        "3. <b>Suitability Conflict Detector:</b> Automated trigger identifying dangerous divergences (e.g. Persona C: High Risk Appetite 90 vs Low Capacity 20), outputting compulsory warnings and adviser action checklists.",
        body_style,
    ))

    story.append(Paragraph("4.2. Longevity Cash Flow & 5 Stress Scenarios", h2_style))
    story.append(Paragraph(
        "Simulates year-by-year cash flows across the entire planning horizon (up to age 85+). In each cycle, investment returns grow capital while inflation-indexed living expenses and guaranteed incomes determine net withdrawals. Every client profile is subjected to 5 distinct macroeconomic stressors:",
        body_style,
    ))

    scenarios_data = [
        [Paragraph("Scenario Name", table_header_style), Paragraph("Macroeconomic / Life Shock Applied", table_header_style), Paragraph("Key Vulnerability Exposed", table_header_style)],
        [Paragraph("<b>1. Base Case</b>", table_cell_bold), Paragraph("Baseline expected inflation and return rates", table_cell_style), Paragraph("Baseline capital depletion runway", table_cell_style)],
        [Paragraph("<b>2. High Inflation Shock</b>", table_cell_bold), Paragraph("+5.0% persistent inflation above baseline", table_cell_style), Paragraph("Purchasing power erosion and rapid reserve drain", table_cell_style)],
        [Paragraph("<b>3. Early Market Drawdown</b>", table_cell_bold), Paragraph("-4.0% annualized returns across years 1–5", table_cell_style), Paragraph("Sequence-of-returns risk during initial retirement", table_cell_style)],
        [Paragraph("<b>4. Medical Expense Shock</b>", table_cell_bold), Paragraph("PKR 2,500,000 lump sum healthcare cost at age 70", table_cell_style), Paragraph("Liquid buffer adequacy and catastrophic erosion", table_cell_style)],
        [Paragraph("<b>5. Early Retirement Shock</b>", table_cell_bold), Paragraph("Forced retirement 3 years ahead of schedule", table_cell_style), Paragraph("Loss of peak accumulation years + lengthened horizon", table_cell_style)],
    ]
    s_table = Table(scenarios_data, colWidths=[130, 200, 210])
    s_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(s_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("4.3. Provider-Agnostic AI Narrative Layer", h2_style))
    story.append(Paragraph(
        "The AI layer consumes condensed JSON payloads (<1,500 tokens) to generate plain-language executive summaries, "
        "audit flags, and client-facing discussion guides. It dynamically supports Groq (Llama 3.3 70B, Qwen 27B), Google Gemini, "
        "and OpenAI, alongside a built-in deterministic offline engine that functions with zero external dependencies.",
        body_style,
    ))
    story.append(Spacer(1, 10))

    # --- Section 5: Technical Stack & Security ---
    story.append(Paragraph("5. Technical Architecture, Security & Privacy", h1_style))
    tech_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology Selection", table_header_style), Paragraph("Rationale & Security Controls", table_header_style)],
        [Paragraph("<b>Computation Engine</b>", table_cell_bold), Paragraph("Python 3.10+, Pydantic V2", table_cell_style), Paragraph("Strict deterministic typing, zero math drift, 100% test coverage.", table_cell_style)],
        [Paragraph("<b>User Interface</b>", table_cell_bold), Paragraph("Streamlit, Plotly Interactive Charts", table_cell_style), Paragraph("Fast responsive B2B dashboard, dynamic fact-find editor.", table_cell_style)],
        [Paragraph("<b>Document Generator</b>", table_cell_bold), Paragraph("ReportLab Community Edition", table_cell_style), Paragraph("Direct binary PDF creation, client-side download, audit-compliant.", table_cell_style)],
        [Paragraph("<b>Database</b>", table_cell_bold), Paragraph("SQLite (Migratable to PostgreSQL)", table_cell_style), Paragraph("Zero-configuration persistence, isolated client case storage.", table_cell_style)],
        [Paragraph("<b>Secrets & Privacy</b>", table_cell_bold), Paragraph("Environment Isolation + DOM Masking", table_cell_style), Paragraph("Keys never rendered in HTML DOM; gitignored local credentials.", table_cell_style)],
    ]
    t_table = Table(tech_data, colWidths=[110, 180, 250])
    t_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 12))

    # --- Section 6: Release Roadmap ---
    story.append(Paragraph("6. Release Roadmap & Milestones", h1_style))
    roadmap_data = [
        [Paragraph("Milestone", table_header_style), Paragraph("Target Features & Capabilities", table_header_style), Paragraph("Status", table_header_style)],
        [
            Paragraph("<b>Version 1.0 (MVP)</b>", table_cell_bold),
            Paragraph("Deterministic calculation engines, Pakistan Fact-Find, 5 stress scenarios, ReportLab 12-section PDF, Streamlit UI, 15/15 tests passing.", table_cell_style),
            Paragraph("<font color='#1b5e20'><b>COMPLETED & LIVE</b></font>", table_cell_style),
        ],
        [
            Paragraph("<b>Version 2.0 (Planned)</b>", table_cell_bold),
            Paragraph("Vectorized Monte Carlo (1,000 runs), Dynamic Digital Twin What-If sliders, Pakistan Shariah Allocator (Sukuks, VPS, KMI-30), Client Portal, FastAPI backend.", table_cell_style),
            Paragraph("<font color='#0277bd'><b>IN DESIGN / SPRINT READY</b></font>", table_cell_style),
        ],
        [
            Paragraph("<b>Version 3.0 (Future)</b>", table_cell_bold),
            Paragraph("Multi-tenant AMC & Bank portals, SECP compliance surveillance dashboard, role-based access control (RBAC), multi-adviser branch hierarchies.", table_cell_style),
            Paragraph("Roadmap Backlog", table_cell_style),
        ],
        [
            Paragraph("<b>Version 4.0 (Enterprise)</b>", table_cell_bold),
            Paragraph("REST API Suite: Headless Risk Profiling API, Capacity Engine API, Core Banking Integration Microservices, CRM connectors.", table_cell_style),
            Paragraph("Roadmap Backlog", table_cell_style),
        ],
    ]
    r_table = Table(roadmap_data, colWidths=[110, 310, 120])
    r_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 14))

    # --- Section 7: Success Metrics ---
    story.append(Paragraph("7. Key Performance Indicators (KPIs)", h1_style))
    story.append(Paragraph("• <b>Mathematical Accuracy & Determinism:</b> 100% deterministic calculation reproducibility across all client portfolios.", bullet_style))
    story.append(Paragraph("• <b>Assessment Turnaround Speed:</b> Complete Fact-Find to multi-scenario stress test & PDF generation in under 60 seconds.", bullet_style))
    story.append(Paragraph("• <b>Mis-Selling Protection:</b> 100% capture rate of Risk-Capacity mismatches before product recommendations.", bullet_style))
    story.append(Paragraph("• <b>Open-Source Accessibility:</b> 100% free-tier and zero-cost stack compatibility for individual advisers and boutique wealth planners.", bullet_style))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path


if __name__ == "__main__":
    out_file = "RetireWise_AI_Product_Requirements_Document_PRD.pdf"
    build_prd_pdf(out_file)
    print(f"PRD PDF successfully generated at: {out_file}")
