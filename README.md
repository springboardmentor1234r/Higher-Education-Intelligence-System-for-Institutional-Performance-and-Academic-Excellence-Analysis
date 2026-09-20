# EduVision_DV: Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Project Domain:** Higher Education Analytics & Business Intelligence  
**Core Technologies:** Python 3.11, Pandas, NumPy, Tableau Desktop 2026, OpenPyXL, ReportLab  
**Date:** September 2026  

---

## Project Overview

**EduVision_DV** is an end-to-end higher education business intelligence suite developed for the Infosys Springboard Internship 7.0. The platform integrates multi-source global university rankings and macroeconomic education datasets to deliver actionable decision support for university leadership, academic researchers, prospective international students, and national education policymakers.

Historically, higher education stakeholders have had to analyze fragmented datasets published by disparate ranking organizations (Quacquarelli Symonds, Times Higher Education, The World Bank). In this project, I engineered a robust, audit-compliant Python ETL pipeline, modeled the data into a relational Star Schema, derived six defensible Key Performance Indicators (KPIs), and developed a suite of four interconnected, interactive Tableau dashboards.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             EDUVISION_DV WORKFLOW                                │
│                                                                                  │
│   [QS 2025 Rankings]    [THE 2024 Rankings]   [WUR 2023]   [World Bank EdStats]  │
│           │                     │                  │                 │           │
│           └───────────────┬─────┴──────────────────┴─────────────────┘           │
│                           ▼                                                      │
│             [Python ETL & Cleaning Pipeline]                                     │
│             - Regex parenthetical acronym stripping                              │
│             - Deterministic entity resolution (849 research matches)             │
│             - Geopolitical country name harmonization                            │
│             - Category A/B/C missing value rules (no blind zero-fill)            │
│                           │                                                      │
│                           ▼                                                      │
│             [Relational Star Schema]                                             │
│             - Conformed Dimensions: dim_university (1,503), dim_country (106)    │
│             - Fact Tables: fact_performance, fact_research, fact_student,        │
│                            fact_country_education                                │
│                           │                                                      │
│                           ▼                                                      │
│             [Higher Education KPI Engineering]                                   │
│             1. Global Ranking Score (QS Overall + Percentile rank imputation)    │
│             2. Research Impact Score (Normalized Citations per Faculty)          │
│             3. Faculty-to-Student Ratio (Actual empirical ratio, not a score)    │
│             4. International Student % (True empirical percentage)               │
│             5. Academic Reputation Score (Global academic survey benchmark)      │
│             6. Research Productivity Index (Composite 0.50*Res+0.30*Cit+0.20*Net)│
│                           │                                                      │
│                           ▼                                                      │
│             [Unified Tableau Desktop Workbook (EduVision_DV.twbx)]               │
│             - Dashboard 1: University Overview (Global Scorecard & Rankings)     │
│             - Dashboard 2: Research Analytics (Citations & Productivity)         │
│             - Dashboard 3: Student Analytics (Staff Ratios & Diversity)          │
│             - Dashboard 4: Country Comparison (Macro Education Policy)           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure (5 Modules)

In accordance with project submission requirements, the repository is structured into exactly five functional module folders:

```
EduVision_DV/
├── Module 1/                    # Milestone 1 & 2: Data Collection, Ingestion & Cleaning
│   ├── 01_data_loading.ipynb    # Raw dataset loading & exploratory inspection
│   ├── 02_data_cleaning.ipynb   # Header sanitization & string normalization
│   ├── 03_data_standardization.ipynb # Star schema generation & join auditing
│   ├── data_collection.py       # Data ingestion script
│   ├── data_cleaning.py         # Complete cleaning & star schema export script
│   ├── education_cleaning.ipynb # Detailed interactive cleaning notebook
│   ├── dim_university.csv       # Master institutional dimension (1,503 rows)
│   ├── dim_country.csv          # Master country dimension (106 rows)
│   ├── fact_university_performance.csv # QS 2025 performance facts (1,503 rows)
│   ├── fact_research.csv        # THE 2024 research & citation facts (849 rows)
│   ├── fact_student.csv         # WUR 2023 student demographic facts (804 rows)
│   ├── fact_country_education.csv # World Bank macroeconomic indicators (2,243 rows)
│   ├── qs_2025_raw.csv, the_2024_raw.csv, wur_2023_raw.csv, world_bank_education_raw.csv
│   └── README.md
│
├── Module 2/                    # Milestone 3 & 4: KPI Engineering & Dashboard Planning
│   ├── 04_kpi_engineering.ipynb # KPI mathematical derivations & distribution analysis
│   ├── generate_education_kpis.py # Standalone Python KPI calculation script
│   ├── kpi_master.csv           # Pre-aggregated master table with all 6 KPIs
│   ├── university_final_dataset.xlsx # Multi-sheet Star Schema + KPI Excel workbook
│   ├── dashboard_storyboard.pdf # Visual UI wireframes, color palette & navigation plan
│   ├── eduvision_prototype.twbx # Milestone 2 Tableau prototype workbook
│   └── README.md
│
├── Module 3/                    # Milestone 5 & 6: Dashboard Development & Integration
│   ├── EduVision_DV.twbx        # Unified 4-dashboard interactive Tableau workbook
│   ├── eduvision_dashboard_v1.twbx # Iterative release (Dashboards 1 & 2)
│   ├── generate_tableau_workbooks.py # Tableau XML generation script
│   └── README.md
│
├── Module 4/                    # Milestone 7 & 8: Testing, QA & Technical Documentation
│   ├── final_documentation.md   # Master Comprehensive Project Report (11 sections)
│   ├── validate_and_test.py     # Automated validation test suite (100% pass)
│   ├── 05_validation.ipynb      # Interactive QA verification notebook
│   ├── qa_checklist.xlsx & qa_checklist.md # Quality assurance verification matrices
│   ├── dashboard_testing_report.md # Formal testing report with individual test logs
│   ├── cleaning_methodology.md  # Detailed guide to regex cleaning & entity resolution
│   ├── kpi_definitions.md       # Mathematical formulas and worked numerical examples
│   ├── dashboard_guide.md       # Comprehensive user manual & drill-down journeys
│   ├── data_dictionary.md       # Complete star schema table & column specifications
│   ├── dataset_sources.md       # Provenance, licensing, and raw data profiles
│   ├── dashboard_storyboard.pdf # Architecture & storyboard document
│   └── README.md
│
├── Module 5/                    # Tableau Workbooks & High-Resolution Dashboard Screenshots
│   ├── EduVision_DV.twbx        # Final packaged Tableau workbook
│   ├── eduvision_dashboard_v1.twbx
│   ├── eduvision_prototype.twbx
│   ├── dashboard_storyboard.pdf
│   ├── dashboard_1_university_overview.png # High-res screenshot: University Overview
│   ├── dashboard_2_research_analytics.png  # High-res screenshot: Research Analytics
│   ├── dashboard_3_student_analytics.png   # High-res screenshot: Student Analytics
│   ├── dashboard_4_country_comparison.png  # High-res screenshot: Country Comparison
│   └── README.md                # Visual walkthrough of the dashboard suite
│
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```

---

## The Six Key Performance Indicators (KPIs)

Every KPI is grounded in a defensible, mathematically validated formula adhering strictly to Sections 20–24 of the project guidelines:

| KPI # | KPI Name | Primary Data Source | Mathematical Formula / Derivation | Output Unit | Target / Scale |
|---|---|---|---|---|---|
| **KPI 1** | **Global Ranking Score** | QS World Rankings 2025 | $\text{QS Overall Score}$ (Inverse percentile rank imputed outside top 500) | Index | 0.0 – 100.0 |
| **KPI 2** | **Research Impact Score** | QS / THE Citations | $\text{QS Citations per Faculty Score} \parallel \text{THE Citations Score}$ | Index | 0.0 – 100.0 |
| **KPI 3** | **Faculty-to-Student Ratio** | WUR 2023 / THE 2024 | $\text{Students per Academic Staff Member (Actual Empirical Ratio)}$ | Ratio | Positive Float (X : 1) |
| **KPI 4** | **International Student %** | WUR 2023 | $\frac{\text{International FTE Students}}{\text{Total FTE Students}} \times 100$ | % | 0.0% – 100.0% |
| **KPI 5** | **Academic Reputation Score** | QS World Rankings 2025 | $\text{QS Academic Reputation Score}$ | Index | 0.0 – 100.0 |
| **KPI 6** | **Research Productivity Index** | Multi-Source Composite | $0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$ | Index | 0.0 – 100.0 |

### Worked Example: Top 5 Global Universities
```
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
| ID     | Institution Name                   | Rank | Global Score | Res Impact | Staff Ratio | Intl % | Acad Rep | Prod Index  |
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
| U0001  | Massachusetts Inst of Tech (MIT)   | 1    | 100.00       | 100.00     | 8.2 : 1     | 33.0%  | 100.00   | 97.30       |
| U0002  | Imperial College London            | 2    | 98.50        | 93.90      | 11.2 : 1    | 61.0%  | 98.50    | 95.40       |
| U0003  | University of Oxford               | 3    | 96.90        | 84.80      | 10.6 : 1    | 42.0%  | 100.00   | 95.44       |
| U0004  | Harvard University                 | 4    | 96.80        | 100.00     | 9.6 : 1     | 25.0%  | 100.00   | 99.87       |
| U0005  | University of Cambridge            | 5    | 96.70        | 84.60      | 11.3 : 1    | 39.0%  | 100.00   | 95.24       |
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
```

---

## Quality Assurance & Verification Summary

The project underwent rigorous testing through the automated test script `validate_and_test.py`:
- **Primary Key Uniqueness:** 100% unique surrogate keys across `dim_university` (1,503 rows) and `dim_country` (106 rows).
- **Referential Integrity:** 100% of records across all four fact tables link to valid dimension keys (**0 orphan records**).
- **Missing Value Threshold:** **0.0% missing** on all critical identifier columns.
- **Interlinking & Interactivity:** Cross-dashboard filter actions passing `university_id` and `country_id` operate seamlessly across all four dashboard views.
- **Automated Test Score:** **100.0% PASS (12 of 12 tests passed)**.

---

## Instructions for Running the Project

### 1. Environment Setup
```bash
# Clone the repository
git clone -b SUJAY_S https://github.com/springboardmentor1234r/Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis.git
cd Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis

# Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scriptsctivate  # Windows

# Install dependencies
pip install pandas numpy openpyxl reportlab matplotlib pillow
```

### 2. Execute Data Cleaning & Validation
```bash
# Run data cleaning and star schema generation
python "Module 1/data_cleaning.py"

# Generate KPIs and master dataset
python "Module 2/generate_education_kpis.py"

# Run automated quality assurance tests
python "Module 4/validate_and_test.py"
```

### 3. Open Tableau Dashboards
- Open `Module 3/EduVision_DV.twbx` or `Module 5/EduVision_DV.twbx` using **Tableau Desktop 2024.1+** or **Tableau Public**.
- Use the top navigation bar to switch between dashboards, or click any university on Dashboard 1 to drill down into its research and student demographic profiles.

---
**Project Author:** Sujay S  
**Internship Program:** Infosys Springboard Internship 7.0  
**Submission Date:** September 20, 2026
