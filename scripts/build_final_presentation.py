"""
EduVision_DV - Final Presentation Builder
Creates a premier 20-slide executive presentation for Infosys Springboard Virtual Internship 7.0 (Batch 3).
Adheres strictly to the visual storytelling, color palette, card architecture, and design philosophy of the
mentor's reference presentation (CampusEventHub), fully customized with verified EduVision_DV intelligence.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'Milestone 3', 'screenshots')
OUTPUT_FINAL_PROJECT = os.path.join(BASE_DIR, 'Final Project', 'Final_Presentation.pptx')

# Color Palette inspired by CampusEventHub Reference Presentation
# Deep Midnight Navy background, Indigo cards, Electric Cyan / Royal Purple / Mint / Amber accents
BG_COLOR = RGBColor(7, 11, 40)        # #070B28 - Deep Midnight Navy
CARD_BG = RGBColor(17, 23, 66)        # #111742 - Deep Indigo Card Fill
CARD_BORDER = RGBColor(38, 51, 122)   # #26337A - Refined Indigo Border
CYAN = RGBColor(85, 208, 250)         # #55D0FA - Electric Cyan (Primary Accent / Tags / Metrics)
PURPLE = RGBColor(121, 107, 255)      # #796BFF - Royal Purple / Violet (Secondary Accent)
MINT = RGBColor(43, 202, 129)         # #2BCA81 - Vibrant Mint Green (Solutions / Successes)
AMBER = RGBColor(255, 159, 28)        # #FF9F1C - Vibrant Amber (Warm Accent / Challenges)
TEXT_WHITE = RGBColor(255, 255, 255)  # #FFFFFF - Crisp Title & Header Text
TEXT_LAVENDER = RGBColor(176, 175, 211) # #B0AFD3 - Soft Lavender / Periwinkle (Body / Bullets)
TEXT_MUTED = RGBColor(117, 130, 181)  # #7582B5 - Dimmed / Metadata Text

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard layout: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_blank_slide():
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return slide

    def add_header(slide, tag, title, subtitle=""):
        # Section Category Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_tag = tb_tag.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.name = 'Arial'
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN

        # Main Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.55))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Optional Subtitle / Lead text
        if subtitle:
            tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.35))
            tf_sub = tb_sub.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = 'Arial'
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = TEXT_LAVENDER

    def add_card(slide, left, top, width, height, title="", desc="", badge="", custom_spacing=None, desc_font_size=10.5, border_color=CARD_BORDER, bg_color=CARD_BG, badge_color=CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.24), top + Inches(0.2), width - Inches(0.48), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        if badge:
            p0.text = badge.upper()
            p0.font.name = 'Arial'
            p0.font.size = Pt(9.5)
            p0.font.bold = True
            p0.font.color.rgb = badge_color
            p0.space_after = Pt(4)
            p_title = tf.add_paragraph()
        else:
            p_title = p0

        if title:
            p_title.text = title
            p_title.font.name = 'Arial'
            p_title.font.size = Pt(14)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_WHITE
            p_title.space_after = Pt(6)

        if desc:
            if isinstance(desc, str):
                raw_items = [line.strip() for line in desc.replace('\r', '').split('\n') if line.strip()]
            else:
                raw_items = [str(item).strip() for item in desc if str(item).strip()]

            for idx, item in enumerate(raw_items):
                p_item = tf.add_paragraph()
                p_item.font.name = 'Arial'
                
                if item.startswith("• "):
                    p_item.text = item
                    p_item.font.size = Pt(desc_font_size)
                    p_item.font.color.rgb = TEXT_LAVENDER
                    p_item.space_after = Pt(custom_spacing) if custom_spacing is not None else Pt(4)
                elif item.startswith("Challenge: "):
                    p_item.space_after = Pt(3)
                    r1 = p_item.add_run()
                    r1.text = "Challenge: "
                    r1.font.name = 'Arial'
                    r1.font.bold = True
                    r1.font.size = Pt(desc_font_size)
                    r1.font.color.rgb = AMBER
                    r2 = p_item.add_run()
                    r2.text = item[len("Challenge: "):]
                    r2.font.name = 'Arial'
                    r2.font.size = Pt(desc_font_size)
                    r2.font.color.rgb = TEXT_LAVENDER
                elif item.startswith("Solution: "):
                    p_item.space_after = Pt(6)
                    r1 = p_item.add_run()
                    r1.text = "Solution: "
                    r1.font.name = 'Arial'
                    r1.font.bold = True
                    r1.font.size = Pt(desc_font_size)
                    r1.font.color.rgb = MINT
                    r2 = p_item.add_run()
                    r2.text = item[len("Solution: "):]
                    r2.font.name = 'Arial'
                    r2.font.size = Pt(desc_font_size)
                    r2.font.color.rgb = TEXT_WHITE
                elif "· Modules" in item or "Weeks " in item:
                    p_item.text = item
                    p_item.font.size = Pt(desc_font_size)
                    p_item.font.bold = True
                    p_item.font.color.rgb = CYAN
                    p_item.space_after = Pt(4)
                elif item.startswith("Dashboard "):
                    p_item.text = item
                    p_item.font.size = Pt(desc_font_size + 0.5)
                    p_item.font.bold = True
                    p_item.font.color.rgb = TEXT_WHITE
                    p_item.space_after = Pt(2)
                elif item.startswith("https://"):
                    p_item.space_after = Pt(custom_spacing) if custom_spacing is not None else Pt(6)
                    r = p_item.add_run()
                    r.text = item
                    r.font.name = 'Arial'
                    r.font.size = Pt(desc_font_size)
                    r.font.color.rgb = CYAN
                    r.font.underline = True
                    try:
                        r.hyperlink.address = item
                    except Exception:
                        pass
                elif len(raw_items) > 1 and idx == 0 and not item.startswith("•"):
                    p_item.text = item
                    p_item.font.size = Pt(desc_font_size)
                    p_item.font.bold = True
                    p_item.font.color.rgb = TEXT_WHITE
                    p_item.space_after = Pt(4)
                else:
                    p_item.text = item
                    p_item.font.size = Pt(desc_font_size)
                    p_item.font.color.rgb = TEXT_LAVENDER
                    p_item.space_after = Pt(custom_spacing) if custom_spacing is not None else Pt(4)

        return card

    # Standard 2x2 Grid Coordinates
    grid_positions = [
        (Inches(0.8), Inches(1.7)),
        (Inches(6.9), Inches(1.7)),
        (Inches(0.8), Inches(4.4)),
        (Inches(6.9), Inches(4.4))
    ]
    grid_w = Inches(5.633)
    grid_h = Inches(2.55)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = add_blank_slide()
    
    # Program Tag Pill
    tb_p = s1.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(11.333), Inches(0.4))
    p = tb_p.text_frame.paragraphs[0]
    p.text = "INFOSYS SPRINGBOARD VIRTUAL INTERNSHIP 7.0 – BATCH 3 · DATA VISUALIZATION"
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN

    # Main Project Title
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(1.1))
    p = tb_t.text_frame.paragraphs[0]
    p.text = "EduVision_DV"
    p.font.name = 'Arial'
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    # Project Subtitle
    tb_s = s1.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(11.333), Inches(0.7))
    p = tb_s.text_frame.paragraphs[0]
    p.text = "Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis"
    p.font.name = 'Arial'
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PURPLE

    # Brief Overview Description
    tb_d = s1.shapes.add_textbox(Inches(1.0), Inches(3.6), Inches(11.333), Inches(0.75))
    p = tb_d.text_frame.paragraphs[0]
    p.text = "A validated business intelligence platform integrating QS World University Rankings 2025 and Times Higher Education (THE) metrics into four interactive Tableau Desktop dashboards."
    p.font.name = 'Arial'
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_LAVENDER

    # Six Key Metric Cards
    metrics = [
        ("1,503", "Institutions"),
        ("106", "Countries"),
        ("195", "Matched Cohort"),
        ("6", "Core KPIs"),
        ("4", "Dashboards"),
        ("24", "Worksheets")
    ]
    card_w = Inches(1.75)
    gap = Inches(0.16)
    left_start = Inches(1.0)
    for i, (val, lbl) in enumerate(metrics):
        cx = left_start + i * (card_w + gap)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(4.7), card_w, Inches(1.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1.2)
        
        tb_m = s1.shapes.add_textbox(cx, Inches(4.8), card_w, Inches(1.1))
        tf_m = tb_m.text_frame
        p_val = tf_m.paragraphs[0]
        p_val.text = val
        p_val.alignment = PP_ALIGN.CENTER
        p_val.font.name = 'Arial'
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = CYAN

        p_lbl = tf_m.add_paragraph()
        p_lbl.text = lbl
        p_lbl.alignment = PP_ALIGN.CENTER
        p_lbl.font.name = 'Arial'
        p_lbl.font.size = Pt(11)
        p_lbl.font.color.rgb = TEXT_LAVENDER

    # Student Details Footer
    tb_f = s1.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.333), Inches(0.5))
    p = tb_f.text_frame.paragraphs[0]
    p.text = "Project Contributor: Kurapalli Sharmila  ·  Domain: Data Visualization & Analytics  ·  Tableau Desktop 2026.2"
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    s2 = add_blank_slide()
    add_header(s2, "Context & Challenges", "Problem Statement: Fragmented Higher Education Intelligence", 
               "Higher education ranking data is distributed across multiple ranking systems and difficult to analyze consistently.")
    
    cards_data_s2 = [
        ("Data Scattered Across Competing Systems", 
         "Institutions, students, and education policymakers must navigate disjointed publications across QS and Times Higher Education (THE), which maintain differing schemas, evaluation criteria, and coverage universes.", 
         "Challenge 01", AMBER),
        ("Incompatible Ranking Indicators", 
         "Direct university comparisons are hindered by competing methodological indicator weightings, contrasting scale ranges, and non-numeric rank bands ('15=', '1201-1400', '1401+') that prevent mathematical analysis.", 
         "Challenge 02", AMBER),
        ("Siloed Research & Student Analytics", 
         "Crucial institutional pillars—including teaching loads (faculty-to-student ratios), student diversity, and research depth—are evaluated in isolation without unified multidimensional business intelligence.", 
         "Challenge 03", AMBER),
        ("Raw League Tables Lack Executive BI", 
         "Static, tabular ranking reports provide zero dynamic cross-filtering, regional benchmarking, or drill-down visual exploration necessary for strategic institutional decision-making.", 
         "Challenge 04", AMBER)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(cards_data_s2, grid_positions):
        add_card(s2, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES
    # =========================================================================
    s3 = add_blank_slide()
    add_header(s3, "Mission & Scope", "Project Objectives: End-to-End Business Intelligence", 
               "Transform raw global ranking data into an executive, interactive decision-support analytics suite.")
    
    obj_data = [
        ("Integrate QS & THE Ranking Datasets", 
         "Ingest 1,503 institutions across 106 countries from QS 2025 and enrich top-tier universities with Times Higher Education ranking indicators while enforcing strict schema hygiene.", 
         "Objective 01", CYAN),
        ("Clean & Standardize University-Level Data", 
         "Resolve entity name discrepancies via 30 reviewed manual aliases, normalize 29 national jurisdictions, and mathematically parse rank bands to continuous midpoint floats.", 
         "Objective 02", CYAN),
        ("Engineer 6 Meaningful Education KPIs", 
         "Formulate and statistically validate 6 standardized higher education KPIs covering global ranks, academic reputation, citations, staffing ratios, diversity, and research productivity.", 
         "Objective 03", CYAN),
        ("Build 4 Interactive Tableau Dashboards", 
         "Architect four interconnected Tableau Desktop dashboards: University Overview, Research Analytics, Student Analytics, and Country Comparison with live cross-filtering.", 
         "Objective 04", CYAN)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(obj_data, grid_positions):
        add_card(s3, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 4: DATA SOURCES & PROJECT SCOPE
    # =========================================================================
    s4 = add_blank_slide()
    add_header(s4, "Data Foundation", "Data Sources & Project Scope: Two Global Authorities, One Master Table",
               "Harmonizing the world's most prestigious university ranking systems into a single verified master datastore.")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(5.633), Inches(3.3), 
             "Base Table: QS World University Rankings 2025", 
             "• Scope: 1,503 institutions across 106 countries.\n"
             "• Dimensions: 28 raw dimensions including ranks, overall scores, reputation scores, citations per faculty, region, size, and focus.\n"
             "• Preserved Universe: 100% of QS institutions retained as the master base table without dropping unranked rows.\n"
             "• Scored Subset: Overall scores published for top 600 institutions (range: 20.8 - 100.0, mean: 41.84).",
             "Primary Universe",
             custom_spacing=5,
             desc_font_size=10,
             badge_color=CYAN)

    add_card(s4, Inches(6.9), Inches(1.7), Inches(5.633), Inches(3.3), 
             "Enrichment: Times Higher Education (THE) Data", 
             "• Scope: 200 elite institutions across 29 jurisdictions.\n"
             "• Dimensions: 13 attributes including students-per-staff ratio, international student %, FTE student enrollment, and research environment.\n"
             "• Integration: Left join against QS based on standardized institution identity with 30 reviewed alias mappings.\n"
             "• Deliberate Exclusions: 5 THE entities excluded from matching (Karolinska, Charité, Pisa, UMass, Indiana) to prevent campus misattribution.",
             "Enrichment Universe",
             custom_spacing=5,
             desc_font_size=10,
             badge_color=PURPLE)

    add_card(s4, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.85),
             "Integrated Dataset Scope & Governed Missingness Policy",
             "• Master Schema: Exactly 1,503 institutions, 106 countries, and 52 final dimensions.\n"
             "• Match Outcome: 195 institutions successfully matched (97.5% of THE top 200). Exactly 1,308 unmatched institutions retain explicit nulls.\n"
             "• Analytical Honesty: THE-related nulls reflect source-coverage boundaries, NOT data errors. Zero synthetic imputation was applied.",
             "Governed Missingness",
             desc_font_size=10.5,
             badge_color=MINT)

    # =========================================================================
    # SLIDE 5: TECHNOLOGY STACK
    # =========================================================================
    s5 = add_blank_slide()
    add_header(s5, "Tools & Frameworks", "Technology Stack: Verified Production Tools & Libraries",
               "Every technology in the pipeline was selected for reproducibility, analytical rigor, and visual performance.")

    tech_cards = [
        ("Python, Pandas & NumPy", 
         "Python 3.10+, Pandas, NumPy, OpenPyXL.\nAutomated ETL pipeline, Latin-1 encoding correction, rank string midpoint parsing, 30-alias entity resolution, and KPI engineering.", 
         "Data Processing & ETL", CYAN),
        ("Jupyter Notebook & Google Colab", 
         "Jupyter Notebook, Google Colab, Matplotlib, Seaborn.\nSelf-contained 14-cell Milestone 1 cleaning notebook and 18-cell Colab notebook providing end-to-end reproducibility.", 
         "Exploration & Prototyping", PURPLE),
        ("Tableau Desktop & Tableau Public", 
         "Tableau Desktop 2026.2 (macOS Apple Silicon) & Tableau Public.\nFixed 1600 × 950 canvas, exactly 24 worksheets, 12 calculated fields, custom dark theme (#12161A), and Hyper packaged extract.", 
         "Visual Business Intelligence", CYAN),
        ("Excel, CSV & Version Control", 
         "Microsoft Excel (.xlsx), Flat CSV, Git, GitHub, Markdown.\nAutomated 36-point Python assertion suite, dual-pipeline MD5 hash verification, and structured 5-folder milestone deliverable repository.", 
         "Storage, Testing & Delivery", MINT)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(tech_cards, grid_positions):
        add_card(s5, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 6: METHODOLOGY & WORKFLOW
    # =========================================================================
    s6 = add_blank_slide()
    add_header(s6, "Pipeline Architecture", "Methodology & Workflow: Step-by-Step Analytical Pipeline",
               "A structured, eight-stage data engineering and visual analytics process ensuring complete reproducibility.")

    pipe_steps_1 = [
        ("1. Data Collection", "Ingest raw QS (1,503 rows) and THE (200 rows) with Latin-1 verification."),
        ("2. Data Cleaning", "Parse rank strings ('15=', '1401+'), normalize 29 national jurisdictions."),
        ("3. Name Standardization", "Standardize university identities; map 30 known alias variations."),
        ("4. QS–THE Integration", "Execute left join on standardized keys; preserve 100% of QS universe.")
    ]
    pipe_steps_2 = [
        ("5. KPI Engineering", "Derive 6 core indicators; formulate 3 tooltip display helper fields."),
        ("6. Data Validation", "Execute 36 automated Python assertions; verify dual-pipeline MD5 hash."),
        ("7. Tableau BI Build", "Develop 4 dashboards across 24 worksheets with interactive filter actions."),
        ("8. Testing & Docs", "Complete 62-point QA checklist, resolve 10 UI defects, deliver documentation.")
    ]
    card_pw = Inches(2.78)
    card_gap = Inches(0.2)
    left_start = Inches(0.8)

    for i, (stitle, sdesc) in enumerate(pipe_steps_1):
        sx = left_start + i * (card_pw + card_gap)
        add_card(s6, sx, Inches(1.7), card_pw, Inches(2.55), stitle, sdesc, f"Phase 0{i+1}", badge_color=CYAN, desc_font_size=10)

    for i, (stitle, sdesc) in enumerate(pipe_steps_2):
        sx = left_start + i * (card_pw + card_gap)
        add_card(s6, sx, Inches(4.4), card_pw, Inches(2.55), stitle, sdesc, f"Phase 0{i+5}", badge_color=PURPLE, desc_font_size=10)

    # =========================================================================
    # SLIDE 7: SIX KPI FRAMEWORK
    # =========================================================================
    s7 = add_blank_slide()
    add_header(s7, "Performance Metrics", "Six KPI Framework: Engineered Higher Education Metrics",
               "Standardized indicators evaluating institutional excellence across teaching, research impact, and reputation.")

    kpi_cards = [
        ("Global Ranking Score", 
         "• Source: QS Overall Score (Direct mapping)\n• Coverage: Top 600 ranked institutions\n• Statistical Mean: 41.84 (Range: 20.8 – 100.0)\n• Purpose: Composite institutional benchmark", 
         "KPI 01", CYAN),
        ("Academic Reputation Score", 
         "• Source: QS Academic Reputation (Direct mapping)\n• Coverage: All 1,503 institutions (100%)\n• Statistical Mean: 20.29 (Range: 1.3 – 100.0)\n• Purpose: Global peer survey standing", 
         "KPI 02", CYAN),
        ("Faculty-to-Student Ratio", 
         "• Source: THE No. of Students per Staff (Direct mapping)\n• Coverage: 195 matched institutions\n• Statistical Mean: 17.44 (Range: 3.8 – 58.0)\n• Purpose: Teaching capacity & workload", 
         "KPI 03", CYAN),
        ("International Student Percentage", 
         "• Source: THE International Students (%)\n• Coverage: 195 matched institutions\n• Statistical Mean: 25.48% (Range: 1.0% – 72.0%)\n• Purpose: Campus diversity & global attraction", 
         "KPI 04", PURPLE),
        ("Research Impact Score", 
         "• Source: QS Citations per Faculty (Direct mapping)\n• Coverage: All 1,503 institutions (100%)\n• Statistical Mean: 23.50 (Range: 1.0 – 100.0)\n• Purpose: Size-adjusted citation velocity", 
         "KPI 05", PURPLE),
        ("Research Productivity (Proxy)", 
         "• Source: THE Research Environment score\n• Coverage: 195 matched institutions\n• Statistical Mean: 61.23 (Range: 34.9 – 100.0)\n• Note: THE Research Environment used as an analytical proxy; not an official THE Research Productivity metric.", 
         "KPI 06", AMBER)
    ]
    card_kpi_w = Inches(3.78)
    card_kpi_h = Inches(2.45)
    kpi_positions = [
        (Inches(0.8), Inches(1.7)), (Inches(4.78), Inches(1.7)), (Inches(8.76), Inches(1.7)),
        (Inches(0.8), Inches(4.35)), (Inches(4.78), Inches(4.35)), (Inches(8.76), Inches(4.35))
    ]
    for (title, desc, badge, b_color), (x, y) in zip(kpi_cards, kpi_positions):
        add_card(s7, x, y, card_kpi_w, card_kpi_h, title, desc, badge, badge_color=b_color, desc_font_size=9.8)

    # Footnote on Slide 7
    tb_fn = s7.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
    p = tb_fn.text_frame.paragraphs[0]
    p.text = "Methodological Disclosure: Research Productivity (Proxy) is derived strictly from THE Research Environment and is clearly designated across all dashboards."
    p.font.name = 'Arial'
    p.font.size = Pt(10)
    p.font.italic = True
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: DATA VALIDATION & INTEGRATION
    # =========================================================================
    s8 = add_blank_slide()
    add_header(s8, "Data Hygiene & Quality", "Data Validation & Integration: Verified Coverage & Integrity",
               "Rigorous audit confirms high source completeness, zero synthetic imputation, and governed null preservation.")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(5.633), Inches(3.2),
             "Verified Cohort Dimensions & Universe Breakdown",
             "• 1,503 Total Institutions: 100% of the QS World University Rankings 2025 base table preserved.\n"
             "• 106 Countries Covered: Complete geographic distribution across all global territories.\n"
             "• 195 QS–THE Matched Institutions: 97.5% match rate against the THE top 200 universe.\n"
             "• 1,308 Unmatched QS Institutions: Explicitly retained with legitimate nulls for THE attributes.\n"
             "• 52 Final Master Columns: Encompassing ranks, raw indicators, engineered KPIs, and display strings.",
             "Cohort Scale", custom_spacing=4, desc_font_size=10, badge_color=CYAN)

    add_card(s8, Inches(6.9), Inches(1.7), Inches(5.633), Inches(3.2),
             "Milestone 1 Data Completeness Audit",
             "• QS Base Fields (Excl. Overall Score): 99.02% complete (0.98% missing), easily passing the < 2% evaluation threshold.\n"
             "• QS Base Fields (Incl. Overall Score): 96.98% complete (3.02% missing), exceeding the > 95% evaluation criterion.\n"
             "• THE Cleaned Dataset Completeness: 100.00% complete across all 200 elite institutions.\n"
             "• Zero Synthetic Imputation: Unranked institutions are never zero-filled or mean-imputed; missingness is governed by source availability.",
             "Completeness Audit", custom_spacing=4, desc_font_size=10, badge_color=MINT)

    add_card(s8, Inches(0.8), Inches(5.05), Inches(11.733), Inches(2.0),
             "Source-Coverage Limitations vs Data Errors",
             "• Governed Missingness: The 1,308 institutions without THE data reflect the inherent coverage boundary of THE's published top-200 league table, NOT data ingestion errors.\n"
             "• Analytical Honesty: Preserving true blanks eliminates synthetic bias in university benchmarks and ensures that all institutional comparisons remain statistically genuine.\n"
             "• Dual-Pipeline Verification: Standalone Python CLI scripts and Google Colab notebook produce byte-identical dataset exports (MD5 hash verified).",
             "Analytical Honesty", desc_font_size=10.2, badge_color=PURPLE)

    # =========================================================================
    # SLIDE 9: DASHBOARD SUITE OVERVIEW
    # =========================================================================
    s9 = add_blank_slide()
    add_header(s9, "Visual Architecture", "Dashboard Suite Overview: Four Interconnected Executive Views",
               "An integrated business intelligence system providing progressive drill-downs from global macro analysis to university deep-dives.")

    suite_cards = [
        ("Dashboard 1: University Overview", 
         "Macro-level directory providing institutional rankings, academic reputation scores, global geographic footprint across 106 countries, regional composition donut, and Rank Movement 2024–2025.", 
         "Macro Directory", CYAN),
        ("Dashboard 2: Research Analytics", 
         "Specialized research excellence view evaluating citation impact against the research productivity proxy, research intensity box plots (VH down to LO), and top 10 research institutions.", 
         "Research Excellence", PURPLE),
        ("Dashboard 3: Student Analytics", 
         "Institutional learning environment benchmarking analyzing students-per-staff staffing ratios, international student diversity %, regional divergence, and FTE student headcount volume.", 
         "Environment & Diversity", CYAN),
        ("Dashboard 4: Country Comparison", 
         "Macro national benchmarking heat table evaluating 106 nations across scores, reputation, and citations, coupled with an interactive world choropleth map via filter actions.", 
         "National Benchmarking", MINT)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(suite_cards, grid_positions):
        add_card(s9, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 10: UNIVERSITY OVERVIEW
    # =========================================================================
    s10 = add_blank_slide()
    add_header(s10, "Tableau Dashboard 1 of 4", "Dashboard 1: University Overview & Rank Movement",
               "Comprehensive institutional directory and temporal performance shift analysis.")

    img1_path = os.path.join(SCREENSHOTS_DIR, 'dash1_university_overview.png')
    if os.path.exists(img1_path):
        s10.shapes.add_picture(img1_path, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(s10, Inches(8.2), Inches(1.7), Inches(4.333), Inches(5.25),
             "Key Visualizations & Features",
             "• Dynamic KPI Cards: Top Ranked University (MIT #1), Total Universities (1,503), Dynamic Average Score (41.84).\n\n"
             "• Top 10 by Global Score: Horizontal bar chart with axis framed 85–100 to clearly separate elite scores.\n\n"
             "• Regional Distribution Donut: Dual-axis donut highlighting European (473) and Asian (511) institutional dominance.\n\n"
             "• Global Geographic Map: World map plotting global institutional footprint across 106 countries.\n\n"
             "• Rank Movement 2024–2025: Calculated as Rank Change = RANK_2024 - RANK_2025. Positive = improvement, Negative = decline. Caltech +5, Imperial +4, Cambridge -3, Stanford -1, 6 unchanged.",
             "Dashboard Features",
             custom_spacing=6,
             desc_font_size=9.5,
             badge_color=CYAN)

    # =========================================================================
    # SLIDE 11: RESEARCH ANALYTICS
    # =========================================================================
    s11 = add_blank_slide()
    add_header(s11, "Tableau Dashboard 2 of 4", "Dashboard 2: Research Analytics — Impact & Productivity",
               "Evaluating institutional citation velocity against research environment depth.")

    img2_path = os.path.join(SCREENSHOTS_DIR, 'dash2_research_analytics.png')
    if os.path.exists(img2_path):
        s11.shapes.add_picture(img2_path, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(s11, Inches(8.2), Inches(1.7), Inches(4.333), Inches(5.25),
             "Key Visualizations & Features",
             "• Research KPI Cards: Highest Research Impact (100.0), Avg Citations per Faculty (23.50), Avg Research Productivity Proxy (61.23).\n\n"
             "• Impact vs Productivity Scatter: Weak correlation demonstrates that publication volume environment does not guarantee citation impact.\n\n"
             "• Research Intensity Box Plots: Significant citation variance observed across Very High (1,021) down to Low (16).\n\n"
             "• Top 10 Research Institutions: Paired bars showing citation impact alongside productivity proxy score.\n\n"
             "• Publication-Volume Note: Publication-volume analysis was not implemented because the source data did not provide a comparable publication-count field.",
             "Dashboard Features",
             custom_spacing=6,
             desc_font_size=9.5,
             badge_color=PURPLE)

    # =========================================================================
    # SLIDE 12: STUDENT ANALYTICS
    # =========================================================================
    s12 = add_blank_slide()
    add_header(s12, "Tableau Dashboard 3 of 4", "Dashboard 3: Student Analytics — Ratios & Diversity",
               "Analyzing teaching workloads, campus internationalization, and total student enrollment.")

    img3_path = os.path.join(SCREENSHOTS_DIR, 'dash3_student_analytics.png')
    if os.path.exists(img3_path):
        s12.shapes.add_picture(img3_path, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(s12, Inches(8.2), Inches(1.7), Inches(4.333), Inches(5.25),
             "Key Visualizations & Features",
             "• Student KPI Cards: Avg Students per Staff (17.4), Avg International Student % (25.5%), Total FTE Student Headcount (5.46M across 195).\n\n"
             "• Regional Staffing Ratios: Average students per staff by region reveals massive divergence (Oceania 30.6 vs Africa 13.0).\n\n"
             "• Internationalization Scatter: Evaluates international student percentage against student-to-staff workload.\n\n"
             "• Top 10 by Enrollment: University of Toronto leads at 80,107 FTE students, followed by University of Bologna (76,955).\n\n"
             "• Interactive Cohort Benchmarking: Multi-dimensional filters (Region, Location, Size, Focus) allow dynamic cohort comparison.",
             "Dashboard Features",
             custom_spacing=6,
             desc_font_size=9.5,
             badge_color=CYAN)

    # =========================================================================
    # SLIDE 13: COUNTRY COMPARISON
    # =========================================================================
    s13 = add_blank_slide()
    add_header(s13, "Tableau Dashboard 4 of 4", "Dashboard 4: Country Comparison & Cross-Filtering",
               "Macro-level territorial benchmarking connecting national heat tables to global choropleth maps.")

    img4_path = os.path.join(SCREENSHOTS_DIR, 'dash4_country_comparison.png')
    if os.path.exists(img4_path):
        s13.shapes.add_picture(img4_path, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(s13, Inches(8.2), Inches(1.7), Inches(4.333), Inches(5.25),
             "Key Visualizations & Features",
             "• Country KPI Cards: Top Country by Avg Score (Hong Kong SAR, 79.9), Most Represented (United States, 197 unis), Total Ranked Countries (106).\n\n"
             "• Benchmarking Heat Table: Comprehensive evaluation of all 106 countries across institutions, scores, reputation, and citations.\n\n"
             "• Geographic Choropleth Map: Global gradient of national institutional representation.\n\n"
             "• Interactive Filter Action: Selecting a country in the benchmarking table filters the geographic map; clearing the selection restores all countries.\n\n"
             "• Top-N Reference Stability: Global reference cards remain stable without dropping out during cross-filtering.",
             "Dashboard Features",
             custom_spacing=6,
             desc_font_size=9.5,
             badge_color=MINT)

    # =========================================================================
    # SLIDE 14: KEY FINDINGS & INSIGHTS
    # =========================================================================
    s14 = add_blank_slide()
    add_header(s14, "Analytical Insights", "Key Findings & Insights: Educational Intelligence from Verified Data",
               "Concrete empirical observations derived from the harmonized QS and THE higher education dataset.")

    insights_data = [
        ("Peak Excellence vs System Depth", 
         "Hong Kong SAR achieves the highest average global score (79.9) across just 6 elite institutions. In contrast, the United States leads in sheer volume (197 institutions) with wider internal variance, demonstrating the difference between elite concentration and broad system depth.", 
         "Insight 01", CYAN),
        ("Productivity Decoupled from Citation Impact", 
         "High research environment scores do not automatically produce high citation impact. World-leading citations appear across varied productivity tiers, confirming that research quality and publishing environment represent distinct dimensions.", 
         "Insight 02", PURPLE),
        ("Structural Regional Staffing Divergence", 
         "Teaching loads diverge radically by continent: Oceania averages 30.6 students per staff member, while Africa averages 13.0, reflecting fundamental differences in funding structures and massification models.", 
         "Insight 03", CYAN),
        ("Coverage Discipline Prevents Misleading BI", 
         "Only 2 of the 6 KPIs cover the entire 1,503-institution universe. Surface-level averaging without explicit population tags would have produced misleading claims about unmeasured universities. Explicit scoping preserves analytical truth.", 
         "Insight 04", MINT)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(insights_data, grid_positions):
        add_card(s14, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 15: CHALLENGES & SOLUTIONS
    # =========================================================================
    s15 = add_blank_slide()
    add_header(s15, "Technical Solutions", "Challenges & Solutions: Engineering Robust Analytics",
               "Navigating complex data harmonization challenges with sound methodological resolutions.")

    challenges_data = [
        ("Different Schemas Across QS & THE", 
         "Challenge: Disparate column schemas and differing indicator scales prevented immediate joins.\nSolution: Standardized schemas with common dimension keys and mapped ranking indicators into unified types.", 
         "Resolution 01", CYAN),
        ("University-Name Mismatches", 
         "Challenge: Naming variations ('UC Berkeley' vs 'University of California, Berkeley') broke automated joins.\nSolution: String normalization plus 30 reviewed manual alias mappings achieved a 97.5% match rate.", 
         "Resolution 02", PURPLE),
        ("Partial THE Coverage (200 of 1,503)", 
         "Challenge: Standard tools often zero-fill or synthetically impute missing values, corrupting data integrity.\nSolution: Governed missingness policy strictly preserving true nulls with zero synthetic imputation.", 
         "Resolution 03", MINT),
        ("Missing Publication-Count Field", 
         "Challenge: Available source datasets lacked a direct comparable publication-count field.\nSolution: Avoided fabricated publication metrics; evaluated research via Citations per Faculty & Research Environment proxy.", 
         "Resolution 04", AMBER)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(challenges_data, grid_positions):
        add_card(s15, x, y, grid_w, grid_h, title, desc, badge, custom_spacing=4, desc_font_size=10, badge_color=b_color)

    # =========================================================================
    # SLIDE 16: TESTING & VALIDATION
    # =========================================================================
    s16 = add_blank_slide()
    add_header(s16, "Verification & Audit", "Testing & Validation: Conformance, Reproducibility & QA",
               "Multi-tier quality assurance covering the data layer, calculations, interactive filters, and visual rendering.")

    qa_cards = [
        ("36 Automated Data-Layer Assertions", 
         "Every KPI was validated against statistical boundaries, non-null counts, minimums, maximums, and theoretical distributions. 100% of assertion tests passed with zero data drift.", 
         "Data Layer QA", CYAN),
        ("Dual-Pipeline Reproducibility", 
         "Both the standalone Python CLI scripts and the Google Colab notebook execute independently and produce byte-identical dataset exports (MD5 checksum verified).", 
         "Reproducibility", PURPLE),
        ("62-Point Comprehensive QA Checklist", 
         "A rigorous audit covering dataset integrity, workbook architecture, filter constraints, rendering fidelity at 1600 × 950, and documentation completeness across all 4 milestones.", 
         "System Audit", MINT),
        ("100% Defect Remediation & 24 Worksheets", 
         "Ten specific UI and filter interaction defects were logged and remediated. The final authoritative workbook contains exactly 24 worksheets across the 4 dashboards.", 
         "Defect Resolution", CYAN)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(qa_cards, grid_positions):
        add_card(s16, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 17: PROJECT MILESTONES
    # =========================================================================
    s17 = add_blank_slide()
    add_header(s17, "Development Journey", "Project Milestones: Four Phases of Structured Delivery",
               "A disciplined eight-week engineering journey delivering verified milestone artifacts.")

    ms_data = [
        ("Milestone 1: Collection & Prep", 
         "Weeks 1–2 · Modules 1 & 2\n"
         "• Ingested 1,703 raw records across QS and THE universes.\n"
         "• Completeness: QS 96.87%, THE 100% (>95% criteria passed).\n"
         "• Delivered data_collection.py, education_cleaning.ipynb, university_cleaned.csv.", 
         "Milestone 01", CYAN),
        ("Milestone 2: KPI Engineering", 
         "Weeks 3–4 · Modules 3 & 4\n"
         "• Engineered 6 standardized higher education KPIs.\n"
         "• 36 automated assertions passed with zero drift.\n"
         "• Delivered generate_education_kpis.py, master datasets, and storyboard.", 
         "Milestone 02", PURPLE),
        ("Milestone 3: Dashboard Development", 
         "Weeks 5–6 · Modules 5 & 6\n"
         "• Built all 4 executive dashboards across exactly 24 worksheets.\n"
         "• Integrated Rank Movement 2024–2025 on University Overview.\n"
         "• Delivered eduvision_dashboard_v1.twbx and 4 retina-ready screenshots.", 
         "Milestone 03", CYAN),
        ("Milestone 4: Testing & Final Delivery", 
         "Weeks 7–8 · Modules 7 & 8\n"
         "• Executed comprehensive 62-point QA checklist.\n"
         "• Remediated 10 interaction defects logged during testing.\n"
         "• Delivered QA_Checklist.md, Testing Report, methodology, and user guide.", 
         "Milestone 04", MINT)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(ms_data, grid_positions):
        add_card(s17, x, y, grid_w, grid_h, title, desc, badge, custom_spacing=3, desc_font_size=9.8, badge_color=b_color)

    # =========================================================================
    # SLIDE 18: FINAL SYSTEM ARCHITECTURE
    # =========================================================================
    s18 = add_blank_slide()
    add_header(s18, "System Architecture", "Final System Architecture: End-to-End Pipeline & BI Suite",
               "The unified flow from heterogeneous raw sources to an executive, decision-grade visual intelligence system.")

    s18_layer1 = [
        "• Source Ingestion: QS 2025 (1,503 rows, 28 fields) + THE 2024 (200 rows, 13 fields).",
        "• Character Encoding: Strict Latin-1 decoding resolving special character glyphs.",
        "• Rank Midpoint Parsing: Converted non-numeric rank bands ('15=', '1401+') to continuous floats.",
        "• Geographic Alignment: Standardized 29 country and regional naming variations.",
        "• Milestone 1 Deliverables: university_raw_data.csv, university_cleaned.csv, data_collection.py, education_cleaning.ipynb."
    ]
    add_card(s18, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.25),
             "Data Ingestion & Hygiene",
             s18_layer1,
             "Layer 01 · Ingestion",
             custom_spacing=5,
             desc_font_size=9.8,
             badge_color=CYAN)

    s18_layer2 = [
        "• Left-Join Integration: Unified master schema retaining 100% of QS universe (1,503 rows × 52 cols).",
        "• Entity Resolution: 30 verified manual alias mappings yielding 97.5% match rate on THE top 200.",
        "• Governed Missingness: Explicit nulls for 1,308 unmatched institutions (zero synthetic imputation).",
        "• 6 Higher Education KPIs: Global Score, Reputation, Staffing Ratio, International %, Citations, Proxy.",
        "• Master Datastore: Byte-identical exports to university_final_dataset.csv and .xlsx."
    ]
    add_card(s18, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.25),
             "Integration & KPI Engine",
             s18_layer2,
             "Layer 02 · Processing",
             custom_spacing=5,
             desc_font_size=9.8,
             badge_color=PURPLE)

    s18_layer3 = [
        "• Tableau Engine: EduVision_DV.twbx Hyper packaged extract (MD5 verified).",
        "• Modular Architecture: Exactly 24 worksheets across 4 executive dashboards (1600 × 950 canvas).",
        "• Interactive Actions: Dashboard 4 country filter action connecting heat table and choropleth map.",
        "• Executive Design: Midnight navy palette (#12161A), high contrast, built for strategic insight.",
        "• Cloud Deployment: All 4 dashboards published live to Tableau Public with cloud interactivity."
    ]
    add_card(s18, Inches(8.8), Inches(1.7), Inches(3.733), Inches(5.25),
             "Tableau Visual BI Suite",
             s18_layer3,
             "Layer 03 · Analytics",
             custom_spacing=5,
             desc_font_size=9.8,
             badge_color=MINT)

    # =========================================================================
    # SLIDE 19: FUTURE ENHANCEMENTS
    # =========================================================================
    s19 = add_blank_slide()
    add_header(s19, "Project Roadmap", "Future Enhancements: Strategic Roadmap for Platform Scalability",
               "Planned evolution to expand analytical depth, automation, and predictive modeling capabilities.")

    future_data = [
        ("Multi-Ranking System Integration", 
         "Incorporate additional global league tables such as the Academic Ranking of World Universities (ARWU / Shanghai Ranking) and CWUR to build a multi-system consensus index.", 
         "Enhancement 01", CYAN),
        ("Automated Data Refresh API Pipeline", 
         "Develop scheduled REST API connectors and scraping pipelines to automatically ingest newly released annual ranking editions without manual ETL intervention.", 
         "Enhancement 02", PURPLE),
        ("Multi-Year Longitudinal Time-Series", 
         "Ingest historical ranking editions from 2020 through 2025 to visualize multi-year institutional trajectories, momentum vectors, and rank volatility over time.", 
         "Enhancement 03", CYAN),
        ("Predictive Machine Learning Analytics", 
         "Implement predictive regression and gradient boosting models to forecast next-cycle institutional ranks based on citation velocity, faculty hiring, and student ratios.", 
         "Enhancement 04", MINT)
    ]
    for (title, desc, badge, b_color), (x, y) in zip(future_data, grid_positions):
        add_card(s19, x, y, grid_w, grid_h, title, desc, badge, badge_color=b_color)

    # =========================================================================
    # SLIDE 20: FINAL SUBMISSION / Q&A
    # =========================================================================
    s20 = add_blank_slide()
    add_header(s20, "Project Delivery", "EduVision_DV: Final Submission & Live Tableau Public Suite",
               "Interactive dashboards deployed on Tableau Public · Open floor for evaluation and technical inquiry.")

    pub_links = [
        "Dashboard 1: University Overview",
        "https://public.tableau.com/app/profile/kurapalli.sharmila/viz/EduVision_DV_17913698181990/UniversityOverview",
        "Dashboard 2: Research Analytics",
        "https://public.tableau.com/app/profile/kurapalli.sharmila/viz/EduVision_DV_17913698181990/ResearchAnalytics",
        "Dashboard 3: Student Analytics",
        "https://public.tableau.com/app/profile/kurapalli.sharmila/viz/EduVision_DV_17913698181990/StudentAnalytics",
        "Dashboard 4: Country Comparison",
        "https://public.tableau.com/app/profile/kurapalli.sharmila/viz/EduVision_DV_17913698181990/CountryComparison"
    ]
    add_card(s20, Inches(0.8), Inches(1.7), Inches(6.6), Inches(5.25),
             "Tableau Public Interactive Dashboards",
             pub_links,
             "Live Deployments",
             custom_spacing=6,
             desc_font_size=9.2,
             badge_color=CYAN)

    qa_card_data = [
        "• Program: Infosys Springboard Virtual Internship 7.0 (Batch 3)",
        "• Project: EduVision_DV",
        "• Full Title: Higher Education Intelligence System",
        "• Contributor: Kurapalli Sharmila",
        "• Domain: Data Visualization & Analytics",
        "• Technology: Tableau Desktop 2026.2 & Python 3.10+",
        "• Authoritative Workbook: EduVision_DV.twbx (MD5: 133a10549295e4b3a1a2ab6640ae615d)",
        "• Final Delivery: 5-Folder Milestone Structure (All 4 Milestones + Final Project)",
        "• Verification: 36 Data Assertions & 62 QA Checks Passed",
        "Thank You!",
        "Questions & Answers: Open floor for mentor evaluation."
    ]
    add_card(s20, Inches(7.7), Inches(1.7), Inches(4.833), Inches(5.25),
             "Project Submission & Evaluation",
             qa_card_data,
             "Thank You & Q&A",
             custom_spacing=4,
             desc_font_size=10.0,
             badge_color=PURPLE)

    # Save presentation
    prs.save(OUTPUT_FINAL_PROJECT)
    print(f"Successfully generated: {OUTPUT_FINAL_PROJECT} ({os.path.getsize(OUTPUT_FINAL_PROJECT):,} bytes)")

if __name__ == '__main__':
    create_presentation()
