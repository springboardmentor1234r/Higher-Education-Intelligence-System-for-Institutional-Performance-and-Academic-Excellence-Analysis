# EduVision_DV: Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

**Author:** Sujay S  
**Internship Track:** Infosys Springboard Internship 7.0  
**Domain:** Data Visualization - Higher Education Analytics & Business Intelligence  
**Core Technologies:** Python 3.11, Pandas, NumPy, Tableau Desktop 2026, OpenPyXL, ReportLab, python-pptx  
**Date:** September 2026  

---

## Project Overview

**EduVision_DV** is an end-to-end higher education business intelligence suite developed for the Infosys Springboard Internship 7.0. The platform integrates multi-source global university rankings and macroeconomic education datasets to deliver actionable decision support for university leadership, academic researchers, prospective international students, and national education policymakers.

The project transforms fragmented data from Quacquarelli Symonds (QS), Times Higher Education (THE), and The World Bank into a standardized, audit-compliant relational Star Schema, engineers six defensible Higher Education Key Performance Indicators (KPIs), and delivers four seamlessly interconnected Tableau dashboards.

---

## Project Organization (Nested Milestones & Modules)

In strict accordance with the official project specification document, the repository is organized into **4 Milestones** comprising **8 Modules**, plus a dedicated **Screenshots** asset folder:

```
EduVision_DV/
├── Milestone 1/                                  # Weeks 1–2: Data Collection & Preparation
│   ├── Module 1/                                 # University Data Collection
│   │   ├── data_collection.py                    # Official deliverable (Data collection script)
│   │   ├── university_raw_data.csv               # Official deliverable (Consolidated raw data)
│   │   ├── qs_2025_raw.csv, the_2024_raw.csv, wur_2023_raw.csv, world_bank_education_raw.csv
│   │   ├── 01_data_loading.ipynb                 # Raw data exploration notebook
│   │   └── README.md
│   │
│   └── Module 2/                                 # Data Cleaning & Transformation
│       ├── education_cleaning.ipynb              # Official deliverable (Cleaning notebook)
│       ├── university_cleaned.csv                # Official deliverable (Consolidated clean data)
│       ├── data_cleaning.py                      # Complete Python ETL script
│       ├── 02_data_cleaning.ipynb, 03_data_standardization.ipynb
│       ├── dim_university.csv, dim_country.csv   # Conformed Star Schema dimensions
│       ├── fact_university_performance.csv, fact_research.csv, fact_student.csv, fact_country_education.csv
│       └── README.md
│
├── Milestone 2/                                  # Weeks 3–4: KPI Engineering & Prototyping
│   ├── Module 3/                                 # Education KPI Engineering
│   │   ├── university_final_dataset.xlsx         # Official deliverable (Multi-sheet Star Schema model)
│   │   ├── generate_education_kpis.py            # Official deliverable (KPI calculation script)
│   │   ├── kpi_master.csv                        # Analytical master table (1,503 rows)
│   │   ├── 04_kpi_engineering.ipynb              # KPI distribution analysis notebook
│   │   └── README.md
│   │
│   └── Module 4/                                 # Dashboard Planning & Prototyping
│       ├── dashboard_storyboard.pdf              # Official deliverable (Visual wireframes & layout)
│       ├── eduvision_prototype.twbx              # Official deliverable (Tableau prototype)
│       └── README.md
│
├── Milestone 3/                                  # Weeks 5–6: Dashboard Development
│   ├── Module 5/                                 # University Overview & Research Dashboards
│   │   ├── eduvision_dashboard_v1.twbx           # Official deliverable (Dashboards 1 & 2)
│   │   └── README.md
│   │
│   └── Module 6/                                 # Student Analytics & Country Comparison Dashboards
│       ├── EduVision_DV.twbx                     # Official deliverable (Unified 4-Dashboard Suite)
│       ├── generate_tableau_workbooks.py         # Tableau XML workbook generator
│       └── README.md
│
├── Milestone 4/                                  # Weeks 7–8: Testing & Project Delivery
│   ├── Module 7/                                 # Testing and Validation
│   │   ├── qa_checklist.xlsx & qa_checklist.md   # Official deliverable (QA Checklist)
│   │   ├── dashboard_testing_report.md           # Official deliverable (Testing Report)
│   │   ├── validate_and_test.py                  # Automated test suite (12 assertions, 100% pass)
│   │   ├── 05_validation.ipynb                   # Interactive verification notebook
│   │   └── README.md
│   │
│   └── Module 8/                                 # Documentation and Project Delivery
│       ├── final_documentation.md & .pdf         # Official deliverable (Master Project Report)
│       ├── EduVision_DV_Project_Presentation.pptx# Official presentation slide deck
│       ├── cleaning_methodology.md, kpi_definitions.md, dashboard_guide.md
│       ├── data_dictionary.md, dataset_sources.md, dashboard_storyboard.pdf
│       └── README.md
│
├── Milestone 5/                                  # Final Deliverables, Dashboards & Presentation
│   ├── EduVision_DV.twbx                         # Unified Production Tableau Workbook
│   ├── dashboard_1_university_overview.png       # University Overview Screenshot
│   ├── dashboard_2_research_analytics.png        # Research Analytics Screenshot
│   ├── dashboard_3_student_analytics.png         # Student Analytics Screenshot
│   ├── dashboard_4_country_comparison.png        # Country Comparison Screenshot
│   ├── final_documentation.pdf & .md             # Master Technical Report
│   ├── dashboard_storyboard.pdf                  # Visual Storyboard Specification
│   ├── EduVision_DV_Project_Presentation.pptx    # Executive Presentation Deck
│   ├── eduvision_dashboard_v1.twbx, eduvision_prototype.twbx
│   ├── cleaning_methodology.md, kpi_definitions.md, dashboard_guide.md
│   ├── data_dictionary.md, dataset_sources.md
│   └── README.md
│
├── Screenshots/                                  # Tableau Dashboards & Visual Assets
│   ├── dashboard_1_university_overview.png       # Screenshot: University Overview
│   ├── dashboard_2_research_analytics.png        # Screenshot: Research Analytics
│   ├── dashboard_3_student_analytics.png         # Screenshot: Student Analytics
│   ├── dashboard_4_country_comparison.png        # Screenshot: Country Comparison
│   ├── EduVision_DV.twbx                         # Final packaged Tableau workbook
│   ├── eduvision_dashboard_v1.twbx, eduvision_prototype.twbx
│   ├── dashboard_storyboard.pdf, final_documentation.pdf
│   ├── EduVision_DV_Project_Presentation.pptx
│   └── README.md
│
├── EduVision_DV_Project_Presentation.pptx        # Root copy of the presentation
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```

---

## The Six Key Performance Indicators (KPIs)

Every KPI is formulated with a defensible, mathematically validated formula:

| KPI # | KPI Name | Primary Source | Mathematical Derivation / Formula | Output Unit | Target Scale |
|---|---|---|---|---|---|
| **KPI 1** | **Global Ranking Score** | QS World Rankings 2025 | $\text{QS Overall Score}$ (Inverse percentile rank imputed for rank > 500) | Index | 0.0 – 100.0 |
| **KPI 2** | **Research Impact Score** | QS / THE Citations | $\text{QS Citations per Faculty Score} \parallel \text{THE Citations Score}$ | Index | 0.0 – 100.0 |
| **KPI 3** | **Faculty-to-Student Ratio** | WUR 2023 / THE 2024 | $\text{Students per Academic Staff Member (Actual Empirical Ratio)}$ | Ratio | Positive Float (X : 1) |
| **KPI 4** | **International Student %** | WUR 2023 | $\frac{\text{International FTE Students}}{\text{Total FTE Students}} \times 100$ | % | 0.0% – 100.0% |
| **KPI 5** | **Academic Reputation Score** | QS World Rankings 2025 | $\text{QS Academic Reputation Score}$ | Index | 0.0 – 100.0 |
| **KPI 6** | **Research Productivity Index** | Derived Composite | $0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$ | Index | 0.0 – 100.0 |

---

## Quality Assurance & Verification Results

The project underwent automated testing via `validate_and_test.py`:
- **Primary Key Uniqueness:** 100% unique surrogate keys across `dim_university` (1,503 rows) and `dim_country` (106 rows).
- **Referential Integrity:** 100% of records across all four fact tables link to valid dimension keys (**0 orphan records**).
- **Missing Value Threshold:** **0.0% missing** on all critical identifier columns.
- **Interlinking & Interactivity:** Cross-dashboard filter actions passing `university_id` and `country_id` operate seamlessly across all four dashboard views.
- **Automated Test Score:** **100.0% PASS (12 of 12 tests passed)**.

---

## Instructions for Running the Project

```bash
# Clone the repository
git clone -b SUJAY_S https://github.com/springboardmentor1234r/Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis.git
cd Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis

# Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows

# Install dependencies
pip install pandas numpy openpyxl reportlab matplotlib pillow python-pptx

# Run data cleaning and star schema generation
python "Milestone 1/Module 2/data_cleaning.py"

# Generate KPIs and master dataset
python "Milestone 2/Module 3/generate_education_kpis.py"

# Run automated quality assurance tests
python "Milestone 4/Module 7/validate_and_test.py"
```

---
**Project Author:** Sujay S  
**Internship Program:** Infosys Springboard Internship 7.0  
**Submission Date:** September 20, 2026
