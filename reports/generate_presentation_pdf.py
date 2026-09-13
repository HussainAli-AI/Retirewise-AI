"""Generate an institutional-grade presentation deck PDF (landscape) for RetireWise AI."""
import os
from reportlab.lib.pagesizes import letter, landscape
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


class SlideCanvas(canvas.Canvas):
    """Custom canvas for landscape presentation slide headers, footers, and numbering."""
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
            self.draw_slide_frame(num_pages)
            super().showPage()
        super().save()

    def draw_slide_frame(self, page_count):
        self.saveState()
        # Top Accent Line
        self.setFillColor(colors.HexColor("#0f2942"))
        self.rect(0, 598, 792, 14, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#0288d1"))
        self.rect(0, 595, 792, 3, fill=1, stroke=0)

        # Footer Line
        self.setStrokeColor(colors.HexColor("#e0e0e0"))
        self.setLineWidth(0.8)
        self.line(40, 36, 752, 36)

        # Footer Text
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawString(40, 24, "RetireWise AI — Institutional WealthTech Pitch Deck")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(752, 24, page_str)
        self.restoreState()


def build_presentation_pdf(output_path: str = "RetireWise_AI_Presentation_Deck.pdf") -> str:
    # 792 x 612 pt (Landscape Letter)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    PRIMARY = colors.HexColor("#0f2942")     # Navy
    SECONDARY = colors.HexColor("#1b5e20")   # Forest
    ACCENT = colors.HexColor("#0277bd")      # Tech Cyan
    ALERT = colors.HexColor("#b71c1c")       # Red Alert
    TEXT_DARK = colors.HexColor("#212529")
    TEXT_MUTED = colors.HexColor("#555555")
    BG_LIGHT = colors.HexColor("#f8f9fa")
    BG_CARD = colors.HexColor("#f1f5f9")
    BORDER_COLOR = colors.HexColor("#cbd5e1")

    # Typography Styles
    slide_title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=3,
    )

    slide_subtitle_style = ParagraphStyle(
        "SlideSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=ACCENT,
        spaceAfter=12,
    )

    card_header = ParagraphStyle(
        "CardH",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=PRIMARY,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "SlideBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
    )

    body_bold = ParagraphStyle(
        "SlideBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=PRIMARY,
    )

    speaker_note_style = ParagraphStyle(
        "SpeakerNote",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=TEXT_MUTED,
    )

    story = []

    # =========================================================================
    # SLIDE 1: Cover / Title Slide
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("<font color='#0277bd'><b>WEALTHTECH & RETIREMENTTECH INNOVATION</b></font>", ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceAfter=8)))
    story.append(Paragraph("RetireWise AI", ParagraphStyle("BigTitle", fontName="Helvetica-Bold", fontSize=34, leading=38, textColor=PRIMARY, spaceAfter=8)))
    story.append(Paragraph("Intelligent Retirement Suitability, Cash Flow Solvency & Risk Protection Platform", ParagraphStyle("BigSub", fontName="Helvetica", fontSize=15, leading=19, textColor=TEXT_MUTED, spaceAfter=20)))
    story.append(HRFlowable(width="100%", thickness=2.5, color=PRIMARY, spaceBefore=0, spaceAfter=20))

    cover_meta = [
        [
            Paragraph("<b>Core Thesis:</b> The LLM explains the numbers; it never creates the numbers.", body_style),
            Paragraph("<b>Target Audience:</b> Advisers, AMCs, Banks, & Retirees", body_style),
            Paragraph("<b>Open-Source:</b> Apache 2.0 (100% Free Stack)", body_style),
        ]
    ]
    t_cover = Table(cover_meta, colWidths=[240, 240, 232])
    t_cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Speaker Note (0:45s):</b> <i>'Judges and investors, retirement is the single largest financial transaction of a person’s life. In Pakistan, millions face an invisible catastrophe: receiving a large lump sum from Provident Fund or Gratuity, but having zero mathematical certainty whether that capital will last through double-digit inflation. Today, we introduce RetireWise AI.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: The Problem Statement
    # =========================================================================
    story.append(Paragraph("The Crisis: The 'Lump-Sum Illusion' & Mis-Selling", slide_title_style))
    story.append(Paragraph("Why traditional retirement advice fails retirees in developing macroeconomic environments", slide_subtitle_style))

    p_col1 = [
        Paragraph("1. The 'Lump-Sum Illusion'", card_header),
        Paragraph("Retirees receive PKR 15M–30M from Provident Fund / Gratuity. They feel wealthy, leading to excessive early spending and misallocation, unaware that compounding inflation drains it in 8–12 years.", body_style),
        Spacer(1, 8),
        Paragraph("2. Confusing Risk Appetite with Capacity", card_header),
        Paragraph("Advisers ask: <i>'Are you comfortable with stocks?'</i> If yes, they allocate aggressively—ignoring that the client has ZERO financial buffer to absorb a 20% drawdown.", body_style),
    ]
    p_col2 = [
        Paragraph("3. Hyper-Inflation Shock Cycles", card_header),
        Paragraph("Pakistan's persistent 8%–15%+ inflation cycles rapidly erode purchasing power. A basket costing PKR 150,000/mo doubles to PKR 300,000+ in under 7 years.", body_style),
        Spacer(1, 8),
        Paragraph("4. Hallucinating Chatbots & Black Boxes", card_header),
        Paragraph("Generic LLMs invent return rates, hallucinate arithmetic, and give non-compliant advice that violates SECP and fiduciary suitability standards.", body_style),
    ]

    t_prob = Table([[p_col1, p_col2]], colWidths=[350, 350])
    t_prob.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), BG_CARD),
        ("BACKGROUND", (1, 0), (1, 0), BG_CARD),
        ("BOX", (0, 0), (0, 0), 1, BORDER_COLOR),
        ("BOX", (1, 0), (1, 0), 1, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (1:30s):</b> <i>'The retirement landscape in Pakistan has a critical vulnerability. People confuse emotional risk tolerance with cold, hard financial capacity. If an adviser mis-allocates a 60-year-old's retirement fund into an aggressive equity fund and the market drops 25%, that retiree cannot go back to work. Furthermore, existing AI tools hallucinate math. We built RetireWise AI to solve this fundamentally.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: The Solution — 2D Suitability & Cash Flow Engine
    # =========================================================================
    story.append(Paragraph("The Solution: Two-Dimensional Decision Intelligence", slide_title_style))
    story.append(Paragraph("Separating psychological risk attitude from mathematical capacity for loss", slide_subtitle_style))

    sol_cards = [
        [
            Paragraph("<b>Fact-Find Profiling</b><br/><font color='#555555'>Captures local Pakistani reality: Provident Fund, Gratuity, VPS, Gold, Property, and Family Dependents.</font>", body_style),
            Paragraph("<b>Psychometric Risk (0-100)</b><br/><font color='#555555'>8-question standardized questionnaire quantifying attitudinal volatility tolerance.</font>", body_style),
            Paragraph("<b>Capacity for Loss (0-100)</b><br/><font color='#555555'>Deterministic formula analyzing liquid runway, debt encumbrance, and income gap.</font>", body_style),
        ],
        [
            Paragraph("<b>Conflict Detection</b><br/><font color='#b71c1c'><b>Automated Mis-Selling Guard:</b> Flags dangerous mismatches (e.g. High Appetite + Low Capacity).</font>", body_style),
            Paragraph("<b>30-Year Cash Flow Sim</b><br/><font color='#555555'>Year-by-year inflation-indexed simulation predicting exact capital depletion age.</font>", body_style),
            Paragraph("<b>Audit-Ready PDF Export</b><br/><font color='#1b5e20'>Instant 12-section compliance and decision-support PDF report for client delivery.</font>", body_style),
        ]
    ]
    t_sol = Table(sol_cards, colWidths=[234, 234, 234])
    t_sol.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_sol)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Speaker Note (2:15s):</b> <i>'RetireWise AI introduces a two-dimensional suitability matrix. It scores both Attitudinal Risk and Objective Capacity on independent 0-to-100 scales. If there is a mismatch—for instance, a retiree who wants aggressive growth but has only 2 months of liquid reserves—the engine halts and generates an automated mis-selling warning.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: High-Level System Architecture & Cardinal Rule
    # =========================================================================
    story.append(Paragraph("System Architecture: The Cardinal Rule", slide_title_style))
    story.append(Paragraph("Architectural separation of deterministic math from generative AI explanations", slide_subtitle_style))

    arch_flow = [
        [
            Paragraph("<b>1. INPUT</b><br/>Adviser / Client Fact-Find (PKR)", ParagraphStyle("A1", parent=body_style, alignment=1)),
            Paragraph("<b>2. CORE ENGINES</b><br/>Deterministic Python (Math, Risk, Capacity, Cashflow)", ParagraphStyle("A2", parent=body_style, alignment=1)),
            Paragraph("<b>3. STRUCTURED DATA</b><br/>Validated Assessment JSON Schema", ParagraphStyle("A3", parent=body_style, alignment=1)),
            Paragraph("<b>4. AI LAYER</b><br/>LLM Explanation (Groq / Gemini / Offline)", ParagraphStyle("A4", parent=body_style, alignment=1)),
            Paragraph("<b>5. DELIVERY</b><br/>Streamlit UI & 12-Section PDF Report", ParagraphStyle("A5", parent=body_style, alignment=1)),
        ]
    ]
    t_arch = Table(arch_flow, colWidths=[140, 150, 130, 140, 142])
    t_arch.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#e3f2fd")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#e8f5e9")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#fff3e0")),
        ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#ede7f6")),
        ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#fce4ec")),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.HexColor("#cccccc")),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    rule_box = [
        [
            Paragraph(
                "<b>CARDINAL RULE ENFORCEMENT:</b><br/>"
                "• <b>NO MATH HALLUCINATIONS:</b> The LLM NEVER calculates returns, taxes, or depletion years.<br/>"
                "• <b>DETERMINISTIC VERIFIABILITY:</b> 100% of calculations are verifiable in unit tests with zero drift.<br/>"
                "• <b>OFFLINE RESILIENCE:</b> Operates completely offline with built-in rule-based narrative engine if no API keys are present.",
                body_style,
            )
        ]
    ]
    t_rule = Table(rule_box, colWidths=[702])
    t_rule.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, PRIMARY),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_rule)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (3:00s):</b> <i>'Notice our architectural pipeline on this slide. The cardinal rule of RetireWise AI is: The LLM explains the numbers; it never creates the numbers. The core calculation engines are deterministic pure Python and Pydantic models. The AI layer receives clean, structured JSON and translates it into institutional plain-language narratives.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: Technology Stack (100% Free & Open-Source)
    # =========================================================================
    story.append(Paragraph("Technology Stack: 100% Free & Open-Source", slide_title_style))
    story.append(Paragraph("Modern institutional-grade stack with zero licensing fees or vendor lock-in", slide_subtitle_style))

    tech_table_data = [
        [Paragraph("Category", card_header), Paragraph("Technology Selection", card_header), Paragraph("Strategic Advantage & Zero-Cost Status", card_header)],
        [Paragraph("<b>Core Computational Engine</b>", body_bold), Paragraph("Python 3.10+ / Pydantic V2", body_style), Paragraph("Type-safe deterministic execution, pure math, zero hallucinations.", body_style)],
        [Paragraph("<b>User Interface & Vis</b>", body_bold), Paragraph("Streamlit + Plotly Interactive", body_style), Paragraph("Dynamic sliders, multi-scenario depletion fan curves, instant UI reactivity.", body_style)],
        [Paragraph("<b>Persistence Layer</b>", body_bold), Paragraph("SQLite (PostgreSQL ready)", body_style), Paragraph("Lightweight, zero-config local storage; seamless cloud migration.", body_style)],
        [Paragraph("<b>AI Narrative Layer</b>", body_bold), Paragraph("Groq (Llama 3.3) / Gemini / Offline", body_style), Paragraph("Ultra-fast sub-3s inference via Groq; full offline rule fallback.", body_style)],
        [Paragraph("<b>Reporting Engine</b>", body_bold), Paragraph("ReportLab Community Edition", body_style), Paragraph("Direct pixel-perfect 12-section PDF generation without external services.", body_style)],
        [Paragraph("<b>DevOps & Testing</b>", body_bold), Paragraph("Git, GitHub, Pytest, Streamlit Cloud", body_style), Paragraph("15/15 automated unit tests passing; 1-click cloud deployment.", body_style)],
    ]
    t_tech = Table(tech_table_data, colWidths=[160, 200, 342])
    t_tech.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (3:45s):</b> <i>'Every single library in our stack is open-source under permissive licenses. There are zero software licensing costs. Furthermore, through our prompt condensation optimization, we reduced token payload from 23,000 tokens to under 1,500, allowing us to run on Groq’s free tier with sub-3-second responses.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: Live Case Study & Demo Flow
    # =========================================================================
    story.append(Paragraph("Live Demo: Case Study (Kamran Aslam — Conflict Case)", slide_title_style))
    story.append(Paragraph("Demonstrating automated mis-selling detection on a real-world retirement profile", slide_subtitle_style))

    case_steps = [
        [
            Paragraph("<b>1. Fact-Find Inputs</b>", card_header),
            Paragraph("• Age 58 (Retiring at 60)<br/>• Liquid Capital: PKR 1.8M<br/>• Monthly Expenses: PKR 210k<br/>• Pension: PKR 0 (Nil)<br/>• Dependents: 3 children", body_style),
        ],
        [
            Paragraph("<b>2. Engine Evaluation</b>", card_header),
            Paragraph("• <b>Risk Tolerance: 90 / 100</b> (Aggressive psychological appetite)<br/>• <b>Loss Capacity: 20 / 100</b> (Fragile: only 2 mos reserve runway)<br/>• <b>Mismatch: CRITICAL</b>", body_style),
        ],
        [
            Paragraph("<b>3. AI Audit & PDF Delivery</b>", card_header),
            Paragraph("• <b>Depletion: In under 1 year!</b><br/>• <b>AI Warning:</b> Prohibits equity allocation.<br/>• <b>PDF Export:</b> Generated instantly with adviser discussion points.", body_style),
        ],
    ]
    t_case = Table([case_steps[0], case_steps[1], case_steps[2]], colWidths=[234, 234, 234])
    t_case.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_case)
    story.append(Spacer(1, 15))

    alert_box = [
        [
            Paragraph(
                "<font color='#b71c1c'><b>SUITABILITY CONFLICT DETECTED:</b></font> "
                "<i>'Client displays high risk appetite (90/100) but has severe liquidity deficits. A conventional broker would have sold him high-risk equities. RetireWise AI overrides appetite with capacity, enforcing capital preservation to prevent bankruptcy.'</i>",
                body_style,
            )
        ]
    ]
    t_alert = Table(alert_box, colWidths=[702])
    t_alert.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffebee")),
        ("BOX", (0, 0), (-1, -1), 1, ALERT),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(t_alert)
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Speaker Note (4:30s):</b> <i>'Let's look at a live test case: Kamran Aslam. Kamran thinks he is an aggressive investor—his risk questionnaire scored 90/100. But our Capacity for Loss engine calculated a score of only 20/100 because he has 3 dependent children and only 2 months of emergency runway. RetireWise AI immediately sounds the alarm: do not buy equities. This directly prevents devastating financial ruin.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: Stress Testing & 5 Scenario Depletions
    # =========================================================================
    story.append(Paragraph("Multi-Scenario Stress Testing", slide_title_style))
    story.append(Paragraph("Beyond static forecasts: subjecting portfolios to macroeconomic shocks", slide_subtitle_style))

    scen_data = [
        [Paragraph("Stress Test Scenario", card_header), Paragraph("Shock Parameters", card_header), Paragraph("Impact on Solvency Runway", card_header), Paragraph("Adviser Strategic Action", card_header)],
        [Paragraph("<b>1. Base Case</b>", body_bold), Paragraph("Baseline inflation & returns", body_style), Paragraph("Healthy solvency trajectory", body_style), Paragraph("Monitor annual withdrawals.", body_style)],
        [Paragraph("<b>2. High Inflation</b>", body_bold), Paragraph("+5.0% persistent inflation", body_style), Paragraph("Depletes capital 7–10 yrs earlier", body_style), Paragraph("Index to defensive growth assets.", body_style)],
        [Paragraph("<b>3. Early Market Drawdown</b>", body_bold), Paragraph("-4.0% in years 1–5 (Sequence risk)", body_style), Paragraph("Irreversible early capital drain", body_style), Paragraph("Maintain 2-year cash wedge.", body_style)],
        [Paragraph("<b>4. Medical Expense Shock</b>", body_bold), Paragraph("PKR 2.5M emergency at age 70", body_style), Paragraph("Immediate liquid reserve breach", body_style), Paragraph("Earmark dedicated Takaful/reserve.", body_style)],
        [Paragraph("<b>5. Early Retirement Shock</b>", body_bold), Paragraph("Retirement forced 3 yrs early", body_style), Paragraph("Loss of peak savings years", body_style), Paragraph("Scale back discretionary spending.", body_style)],
    ]
    t_scen = Table(scen_data, colWidths=[150, 170, 180, 202])
    t_scen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_scen)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (5:15s):</b> <i>'Retirement plans do not fail on average days; they fail during crises. Our scenario engine runs 5 stress tests simultaneously. The adviser can show the client exact visual curves of what happens during a double-digit inflation spike or a sequence-of-returns market crash, building genuine financial resilience.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: Team Members & Core Roles
    # =========================================================================
    story.append(Paragraph("The Team: Engineering & Domain Expertise", slide_title_style))
    story.append(Paragraph("Passionate builders uniting WealthTech, quantitative modeling, and AI engineering", slide_subtitle_style))

    team_data = [
        [
            Paragraph("<b>Hussain Ali</b><br/><font color='#0277bd'><b>Lead AI & Full-Stack Architect</b></font><br/><br/>• System architecture & deterministic financial engine design.<br/>• Streamlit interactive UI & Plotly visualization pipeline.<br/>• Provider-agnostic LLM client & prompt token optimization.<br/>• Database design & ReportLab PDF generator.", body_style),
            Paragraph("<b>Financial Engineering Lead</b><br/><font color='#1b5e20'><b>Quantitative Modeling & Compliance</b></font><br/><br/>• Two-dimensional risk & capacity mathematical scoring.<br/>• Pakistan macroeconomic inflation & longevity modeling.<br/>• SECP regulatory alignment & anti-mis-selling rules.<br/>• Scenario stress testing design.", body_style),
            Paragraph("<b>Product & UX Strategy Lead</b><br/><font color='#7b1fa2'><b>Adviser Experience & Research</b></font><br/><br/>• Financial adviser workflow optimization & usability testing.<br/>• Fact-Find questionnaire psychometric validation.<br/>• Institutional PDF compliance reporting structure.<br/>• Client onboarding portal design.", body_style),
        ]
    ]
    t_team = Table(team_data, colWidths=[234, 234, 234])
    t_team.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (6:00s):</b> <i>'Our team combines full-stack AI engineering with deep quantitative financial modeling. We built this platform from the ground up to address real structural problems in emerging WealthTech markets.'</i>", speaker_note_style))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: Vision, Roadmap & Closing
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<font color='#0277bd'><b>THE ROAD AHEAD</b></font>", ParagraphStyle("RoadTag", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceAfter=6)))
    story.append(Paragraph("Making Retirement Decisions Clearer and Smarter", ParagraphStyle("CloseTitle", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=PRIMARY, spaceAfter=14)))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=14))

    roadmap_cols = [
        [
            Paragraph("<b>V1 — MVP (COMPLETE)</b><br/>• Deterministic Engines<br/>• 2D Suitability Matrix<br/>• 5 Stress Scenarios<br/>• Streamlit UI & PDF<br/>• 15/15 Tests Passing", body_style),
            Paragraph("<b>V2 — DIGITAL TWIN (NEXT)</b><br/>• Monte Carlo Simulation (1,000 runs)<br/>• Dynamic What-If Sliders<br/>• Shariah Asset Allocator<br/>• Client Self-Service Portal<br/>• FastAPI REST Microservice", body_style),
            Paragraph("<b>V3 — INSTITUTIONAL</b><br/>• AMC Multi-Tenant SaaS<br/>• Compliance Surveillance Portal<br/>• Core Banking Connectors<br/>• SECP Audit Trail Logs", body_style),
        ]
    ]
    t_road = Table(roadmap_cols, colWidths=[234, 234, 234])
    t_road.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 20))

    call_to_action = [
        [
            Paragraph(
                "<font size='11' color='#0f2942'><b>RetireWise AI — Making Retirement Decisions Clearer and Smarter.</b></font><br/>"
                "Live GitHub Repo: <b>github.com/HussainAli-AI/Retirewise-AI</b> | Open-Source Apache 2.0",
                ParagraphStyle("CTA", fontName="Helvetica", fontSize=9.5, leading=14, alignment=1),
            )
        ]
    ]
    t_cta = Table(call_to_action, colWidths=[702])
    t_cta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8f0fe")),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cta)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Speaker Note (6:45s):</b> <i>'In conclusion, RetireWise AI takes the guesswork out of retirement planning. By combining verifiable mathematical rigor with transparent AI explanations, we empower advisers and retirees to face the future with confidence. Thank you, and we welcome your questions!'</i>", speaker_note_style))

    # Build PDF
    doc.build(story, canvasmaker=SlideCanvas)
    return output_path


if __name__ == "__main__":
    out_file = "RetireWise_AI_Presentation_Deck.pdf"
    build_presentation_pdf(out_file)
    print(f"Presentation deck PDF successfully generated at: {out_file}")
