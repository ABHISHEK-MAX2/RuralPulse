import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_pitch_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)       # #0F172A Deep Slate Navy
    BG_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC Light Background
    PRIMARY_TEAL = RGBColor(13, 148, 136) # #0D9488 Vibrant Teal
    TEXT_DARK = RGBColor(30, 41, 59)     # #1E293B Slate Dark
    TEXT_LIGHT = RGBColor(255, 255, 255) # White
    TEXT_MUTED = RGBColor(100, 116, 139) # Muted Gray
    CARD_BG = RGBColor(255, 255, 255)    # White Card
    ACCENT_RED = RGBColor(220, 38, 38)   # Crimson Red
    ACCENT_BLUE = RGBColor(37, 99, 235)  # Royal Blue

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="RURALPULSE HACKATHON PITCH DECK"):
        # Header banner shape
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_DARK
        shape.line.fill.background()

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.6)
        tf.margin_top = Inches(0.15)

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_TEAL

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 1: SOLUTION OVERVIEW
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, BG_DARK)

    # Main Title Box
    txBox = slide1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.733), Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "RURALPULSE (KRHI)"
    p0.font.size = Pt(44)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY_TEAL

    p1 = tf.add_paragraph()
    p1.text = "Karnataka Rural Healthcare Intelligence & Decision Support Platform"
    p1.font.size = Pt(22)
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "\nProblem Statement: PS-HEALTH-04 — AI-Driven Healthcare Access & MMU Fleet Dispatch"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    p3 = tf.add_paragraph()
    p3.text = "Team Name: RuralPulse Innovators  |  Lead Architect: Ms. Sinchana Urs"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = PRIMARY_TEAL

    # Highlight Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(11.733), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card.line.color.rgb = PRIMARY_TEAL
    card.line.width = Pt(1.5)

    tf_card = card.text_frame
    tf_card.word_wrap = True
    tf_card.margin_left = Inches(0.4)
    tf_card.margin_top = Inches(0.3)

    cp0 = tf_card.paragraphs[0]
    cp0.text = "WHAT WE ARE BUILDING (ELEVATOR PITCH IN 10 SECONDS):"
    cp0.font.size = Pt(12)
    cp0.font.bold = True
    cp0.font.color.rgb = PRIMARY_TEAL

    cp1 = tf_card.add_paragraph()
    cp1.text = "RuralPulse is an AI-powered healthcare decision support platform for the Government of Karnataka that integrates 11 health domain datasets across 30,771 villages to predict rural vulnerability, eliminate healthcare dead zones, and dynamically dispatch Mobile Medical Units (MMUs) to high-risk villages before emergencies occur."
    cp1.font.size = Pt(16)
    cp1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 2: THE PROBLEM
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "Slide 2: The Problem — Rural Healthcare Accessibility Dead Zones")

    # Column 1: Text breakdown
    col1 = slide2.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(6.8), Inches(5.5))
    tf1 = col1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. What is the Problem?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p = tf1.add_paragraph()
    p.text = "Over 30,771 villages in Karnataka face severe spatial and seasonal barriers to primary healthcare access due to long transit distances, unpaved roads, monsoon flooding, and static MMU schedules."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    p = tf1.add_paragraph()
    p.text = "\n2. Who is Affected?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p = tf1.add_paragraph()
    p.text = "• 28.5M+ Rural Citizens (pregnant women needing ANC & infants needing immunization)\n• 40,000+ ASHA Workers & ANMs lacking predictive risk tracking tools\n• District Health Officers (DHOs) managing 31 districts without unified data visibility"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    p = tf1.add_paragraph()
    p.text = "\n3. Why is this Problem Important?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p = tf1.add_paragraph()
    p.text = "Preventable maternal and infant mortality; unoptimized MMU fleets operating on fixed routes; total village isolation during monsoons."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    # Column 2: Ground-Truth Metrics Table
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(1.4), Inches(5.0), Inches(5.5))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = RGBColor(226, 232, 240)

    tf2 = card2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "REAL-WORLD EVIDENCE & BASELINE DATA"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BG_DARK

    p = tf2.add_paragraph()
    p.text = "\n📍 14.2 km Average PHC Distance\nIn vulnerable rural taluks (transit time > 45 mins)."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    p = tf2.add_paragraph()
    p.text = "\n🛣 32.4% Seasonal Road Blockage\nRemote rural roads become impassable in monsoons."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    p = tf2.add_paragraph()
    p.text = "\n📉 27.8% Antenatal Care (ANC) Deficit\n4th-trimester ANC checkup deficit in remote villages."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    p = tf2.add_paragraph()
    p.text = "\n🚑 < 42% MMU Routing Efficiency\nUnoptimized static routes miss high-risk villages."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 3: OUR SOLUTION
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "Slide 3: Our Solution — Multi-Tier AI Platform & LGD 2026 Foundation")

    # Workflow Card across top
    wf_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.133), Inches(1.2))
    wf_box.fill.solid()
    wf_box.fill.fore_color.rgb = BG_DARK
    wf_box.line.fill.background()

    tf_wf = wf_box.text_frame
    tf_wf.word_wrap = True
    tf_wf.margin_left = Inches(0.4)
    tf_wf.margin_top = Inches(0.2)

    p = tf_wf.paragraphs[0]
    p.text = "SOLUTION FLOW:  PROBLEM ➔ OUR SOLUTION ➔ HOW IT WORKS ➔ EXPECTED OUTCOME"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf_wf.add_paragraph()
    p.text = "Isolated Rural Villages  ➔  RuralPulse AI Platform  ➔  7-Dimension Risk Engine + 4-Tier AI  ➔  Dynamic MMU Dispatch & Zero Maternal Delay"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    # 3 Feature Cards
    card_width = Inches(3.8)
    card_gap = Inches(0.36)

    # Card 1
    c1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.7), card_width, Inches(4.3))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = PRIMARY_TEAL
    c1.line.width = Pt(1.5)
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    p.text = "📊 11-Layer Data Layer"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "Standardizes official 6-digit LGD 2026 codes across 30,771 villages.\n\nCombines demographics, PHC transit, ANC gaps, immunization rates, monsoon road hazards, and water quality indices into a single unified profile."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # Card 2
    c2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + card_width + card_gap, Inches(2.7), card_width, Inches(4.3))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = PRIMARY_TEAL
    c2.line.width = Pt(1.5)
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    p.text = "🤖 4-Tier Zero-Failure AI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "Multi-tier LLM cascade for 100% reliable executive briefing generation:\n\n1. IBM watsonx.ai (Primary)\n2. Groq Cloud API (groq/compound)\n3. xAI Grok API (grok-beta)\n4. Deterministic Engine (Zero-Failure Shield)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # Card 3
    c3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + (card_width + card_gap)*2, Inches(2.7), card_width, Inches(4.3))
    c3.fill.solid()
    c3.fill.fore_color.rgb = CARD_BG
    c3.line.color.rgb = PRIMARY_TEAL
    c3.line.width = Pt(1.5)
    tf = c3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)

    p = tf.paragraphs[0]
    p.text = "🧮 Explainable AI (XAI)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "Transparent composite risk scoring (0–100).\n\nExplains EXACT risk drivers for health officers (e.g. +22.4 pts due to 18.5 km PHC distance, +18.1 pts monsoon road block) with role-scoped RBAC dashboards."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 4: USERS, BENEFICIARIES & STAKEHOLDERS
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "Slide 4: Users, Beneficiaries & Stakeholders")

    # Table of Users
    rows, cols = 4, 4
    table_shape = slide4.shapes.add_table(rows, cols, Inches(0.6), Inches(1.5), Inches(12.133), Inches(5.3))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(3.7)
    table.columns[3].width = Inches(3.033)

    headers = ["Category", "Who Are They?", "How They Use RuralPulse", "Direct Impact / Benefit"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_TEAL

    data = [
        ["Primary Users", "District Health Officers (DHO), MMU Fleet Coordinators, System Admins", "Login to role-scoped dashboards, view AI vulnerability rankings, approve MMU camp routes", "90% reduction in manual planning time; zero missed critical villages"],
        ["Beneficiaries", "28.5M Rural Citizens, Pregnant Women, Infants, ASHA Workers", "Receive weekly doorstep medical camps, emergency care, and vaccine supplies", "Doorstep healthcare within 30 minutes; zero maternal delays"],
        ["Stakeholders", "Dept of Health & Family Welfare Karnataka, NHM, DVDMS Portal", "Track state-wide health indicators, allocate annual budgets, monitor drug buffers", "Evidence-based public health budgeting & zero drug stockouts"]
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, cell_data in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = cell_data
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 5: IMPACT & METRICS
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "Slide 5: Evidence-Based Impact & Measurable Outcomes")

    # Metrics Table
    rows, cols = 5, 4
    table_shape5 = slide5.shapes.add_table(rows, cols, Inches(0.6), Inches(1.4), Inches(12.133), Inches(5.5))
    t5 = table_shape5.table

    t5.columns[0].width = Inches(3.0)
    t5.columns[1].width = Inches(3.0)
    t5.columns[2].width = Inches(3.0)
    t5.columns[3].width = Inches(3.133)

    headers5 = ["Impact Metric", "Current Situation (Baseline)", "Expected Outcome (RuralPulse)", "Validation / Measurement Method"]
    for i, h in enumerate(headers5):
        cell = t5.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_TEAL

    data5 = [
        ["MMU Emergency Response Time", "65–90 minutes average transit time to remote villages", "< 30 minutes via dynamic risk-based fleet dispatch", "GPS fleet tracking logs & MMU camp timestamp verification"],
        ["High-Risk Village Coverage", "38% of critical villages visited monthly", "95%+ monthly coverage of Critical (≥75.0) risk villages", "LGD village visit logs vs. vulnerability score index"],
        ["Maternal ANC Checkup Completion", "72.2% 4th-trimester ANC completion rate", "92.0%+ ANC checkup completion across rural taluks", "RCH (Reproductive & Child Health) portal sync"],
        ["Operational Fuel Cost Efficiency", "₹18.4 Lakh/MMU/year wasted on unoptimized routes", "28% reduction in fuel expenditure via smart routing", "MMU route mileage analytics & DVDMS log integration"]
    ]

    for row_idx, row_data in enumerate(data5, start=1):
        for col_idx, cell_data in enumerate(row_data):
            cell = t5.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = cell_data
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 6: PROTOTYPE / DEMONSTRATION
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "Slide 6: Working Prototype & Live System Demonstration")

    # Workflow Banner
    b6 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.133), Inches(1.0))
    b6.fill.solid()
    b6.fill.fore_color.rgb = PRIMARY_TEAL
    b6.line.fill.background()
    tf = b6.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.15)

    p = tf.paragraphs[0]
    p.text = "REAL USER SCENARIO DEMONSTRATION:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BG_DARK

    p = tf.add_paragraph()
    p.text = "User Problem (DHO identifies Honnalli Rural 84.5 Critical Risk) ➔ User Action (Clicks Intelligence Modal) ➔ System (IBM watsonx / Groq AI generates briefing) ➔ Output & Benefit (Dispatches MMU fleet; ASHA tracks 14 ANC mothers)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_LIGHT

    # 4 Screen Feature Cards
    screens = [
        ("Executive Dashboard", "Priority-sorted list of 30,771 villages ordered by risk score descending.\n\nRisk Badges: Critical (≥75), High (60-74.9), Medium (40-59.9), Low (<40)."),
        ("Village Intelligence Modal", "4 Interactive Tabs:\n• Explainable AI Factors\n• 11-Layer Data Grid\n• Intervention Matrix\n• IBM watsonx AI Copilot"),
        ("Map Intelligence", "Interactive MapLibre GL geospatial map.\n\nColor-coded risk markers and PHC radius overlays for spatial accessibility analysis."),
        ("Admin & Role Scoping", "JWT token-authenticated user management.\n\nRole-scoped views for DHOs, MMU Coordinators, State Administrators, and System Admins.")
    ]

    cw6 = Inches(2.8)
    cg6 = Inches(0.31)

    for idx, (s_title, s_desc) in enumerate(screens):
        c = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + idx*(cw6+cg6), Inches(2.5), cw6, Inches(4.5))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = RGBColor(203, 213, 225)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = f"🖥 {s_title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_TEAL

        p = tf.add_paragraph()
        p.text = f"\n{s_desc}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 7: SUSTAINABILITY / BUSINESS MODEL
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "Slide 7: Sustainability & Operating Model")

    c_width7 = Inches(3.8)
    c_gap7 = Inches(0.36)

    # Box 1: Funding
    b1 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), c_width7, Inches(5.4))
    b1.fill.solid()
    b1.fill.fore_color.rgb = CARD_BG
    b1.line.color.rgb = PRIMARY_TEAL
    b1.line.width = Pt(1.5)
    tf = b1.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "🏛 Funding & Adoption"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "\n• Government Primary Funder:\nAdopted by Dept of Health & Family Welfare under the National Health Mission (NHM) Digital Health Allocation.\n\n• Public-Private Partnerships (PPP):\nCSR funding from healthcare logistics providers and telecom infrastructure partners for field tablet hardware."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # Box 2: Operating Costs
    b2 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + c_width7 + c_gap7, Inches(1.5), c_width7, Inches(5.4))
    b2.fill.solid()
    b2.fill.fore_color.rgb = CARD_BG
    b2.line.color.rgb = PRIMARY_TEAL
    b2.line.width = Pt(1.5)
    tf = b2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "💵 Operating Cost Structure"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "\n• Cloud Infrastructure:\nScalable container hosting on Render / GCP ($120–$300/month state-wide).\n\n• Optimized AI Token Costs:\n4-tier cascade utilizes Groq Cloud API and Deterministic Engine to reduce LLM API expenditure by 75%.\n\n• Maintenance:\nIntegrated into District Health Office IT maintenance contracts."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # Box 3: Partnerships
    b3 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + (c_width7 + c_gap7)*2, Inches(1.5), c_width7, Inches(5.4))
    b3.fill.solid()
    b3.fill.fore_color.rgb = CARD_BG
    b3.line.color.rgb = PRIMARY_TEAL
    b3.line.width = Pt(1.5)
    tf = b3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "🤝 Key Strategic Partners"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "\n• NHM & ABDM:\nFull compliance with Ayushman Bharat Digital Mission standards.\n\n• DVDMS Supply Chain Portal:\nReal-time integration for drug buffer and vaccine replenishment.\n\n• ASHA & ANM Field Networks:\nZero-friction workflow adoption for 40,000+ field workers."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    # ==========================================
    # SLIDE 8: SCALABILITY & FUTURE POTENTIAL
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "Slide 8: Scalability & Future Growth Potential")

    # 3 Phase Cards
    phases = [
        ("PHASE 1: 90-Day Pilot", "Months 1–3", "2 Pilot Districts (Davanagere & Bagalkote)\n600+ Rural Villages\n12 MMU Fleets\nRefining 7-dimension risk weights & ASHA workflow integration."),
        ("PHASE 2: Statewide Rollout", "Months 4–9", "Statewide Karnataka Expansion\n31 Districts / 30,771 Villages\n100+ MMU Fleets\nFull integration with DVDMS portal & RCH maternal checkup tracking."),
        ("PHASE 3: National Scaling", "Year 2+", "National Expansion across 5+ Southern States (Andhra Pradesh, Tamil Nadu, Telangana, Kerala)\nNHM National Digital Health Stack adoption.")
    ]

    for idx, (p_title, p_sub, p_desc) in enumerate(phases):
        c = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + idx*(c_width7+c_gap7), Inches(1.4), c_width7, Inches(3.2))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = PRIMARY_TEAL
        c.line.width = Pt(1.5)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_TEAL

        p = tf.add_paragraph()
        p.text = p_sub
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

        p = tf.add_paragraph()
        p.text = f"\n{p_desc}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK

    # Bottom Future Capabilities Box
    fut_box = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.8), Inches(12.133), Inches(2.2))
    fut_box.fill.solid()
    fut_box.fill.fore_color.rgb = BG_DARK
    fut_box.line.fill.background()

    tf = fut_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_top = Inches(0.2)

    p = tf.paragraphs[0]
    p.text = "FUTURE INNOVATIONS & ADVANCED CAPABILITIES:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_TEAL

    p = tf.add_paragraph()
    p.text = "• 🛰 Satellite Monsoon Flood Prediction: Sentinel-2 satellite imagery integration to dynamically predict monsoon road blockages 7 days ahead.\n• 📱 Offline Mobile PWA for ASHA Workers: Offline-first progressive web app for field data entry in zero-connectivity rural pockets.\n• 🔮 Disease Outbreak Early Warning: ML models predicting Dengue/Malaria outbreaks 14 days in advance based on rainfall and water quality."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_LIGHT

    # Save presentation
    output_filename = "RuralPulse_Hackathon_Pitch_Deck.pptx"
    prs.save(output_filename)
    print(f"SUCCESS: Generated {output_filename}")

if __name__ == "__main__":
    create_pitch_deck()
