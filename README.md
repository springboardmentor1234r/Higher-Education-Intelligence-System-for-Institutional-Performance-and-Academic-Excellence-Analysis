# EduVision_DV: Higher Education Performance Dashboard

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Data Visualization & Educational Analytics  
**Tools Used:** Python (Pandas, NumPy), Tableau Desktop 2026, OpenPyXL  

---

## Project Overview

In this project, I developed an end-to-end higher education analytics dashboard suite called **EduVision_DV**. The project analyses university rankings, research productivity, faculty-student ratios, international student diversity, and national education indicators using publicly available global datasets.

The final outcome is an integrated Tableau workbook (`EduVision_DV.twbx`) containing four interconnected dashboards:
1. **University Overview** – Global ranking scorecard, top university performance, and geographic distribution.
2. **Research Analytics** – Institutional research scores, citation impact, and research productivity benchmarking.
3. **Student Analytics** – International student share, students per staff ratios, and gender diversity trends.
4. **Country Comparison** – National higher education capacity, public education spending (% of GDP), and tertiary enrollment trajectories.

---

## Project Organization

The repository is organized into five module folders matching the internship submission guidelines:

```
EduVision_DV/
├── Module 1/                    # Milestone 1 & Milestone 2 (Data Collection & Cleaning)
│   ├── data_collection.py       # Data loading & ingestion script
│   ├── data_cleaning.py         # Cleaning & star schema generation script
│   ├── education_cleaning.ipynb # Jupyter notebook for cleaning steps
│   ├── 01_data_loading.ipynb    # Raw data exploration notebook
│   ├── 02_data_cleaning.ipynb   # String standardization notebook
│   ├── 03_data_standardization.ipynb # Star schema verification notebook
│   ├── university_raw_data.csv  # Consolidated raw dataset
│   ├── university_cleaned.csv   # Consolidated cleaned dataset
│   ├── qs_2025_raw.csv, the_2024_raw.csv, wur_2023_raw.csv, world_bank_education_raw.csv
│   └── dim_university.csv, dim_country.csv, fact_university_performance.csv, fact_research.csv, fact_student.csv, fact_country_education.csv
│
├── Module 2/                    # Milestone 3 & Milestone 4 (KPI Engineering & Dashboard Planning)
│   ├── generate_education_kpis.py # KPI calculation script
│   ├── 04_kpi_engineering.ipynb   # KPI distribution & formula notebook
│   ├── university_final_dataset.xlsx # Star Schema + KPI master Excel workbook
│   ├── kpi_master.csv           # Flat master KPI table
│   ├── dashboard_storyboard.pdf # Storyboard & wireframe document
│   └── eduvision_prototype.twbx # Tableau prototype workbook
│
├── Module 3/                    # Milestone 5 & Milestone 6 (Dashboard Development & Integration)
│   ├── EduVision_DV.twbx        # Unified 4-dashboard Tableau workbook
│   ├── eduvision_dashboard_v1.twbx # Milestone 3 v1 dashboard workbook
│   └── generate_tableau_workbooks.py # Tableau XML workbook generation script
│
├── Module 4/                    # Milestone 7 & Milestone 8 (Testing, Validation & Documentation)
│   ├── validate_and_test.py     # Data validation & QA test script
│   ├── 05_validation.ipynb      # Verification notebook
│   ├── qa_checklist.xlsx & qa_checklist.md
│   ├── dashboard_testing_report.md
│   └── dataset_sources.md, data_dictionary.md, cleaning_methodology.md, kpi_definitions.md, dashboard_guide.md, dashboard_storyboard.pdf
│
└── Module 5/                    # Tableau Dashboard Screenshots & Tableau Files
    ├── EduVision_DV.twbx        # Final packaged Tableau workbook
    ├── eduvision_dashboard_v1.twbx
    ├── eduvision_prototype.twbx
    ├── dashboard_storyboard.pdf
    ├── dashboard_1_university_overview.png # Screenshot: University Overview
    ├── dashboard_2_research_analytics.png  # Screenshot: Research Analytics
    ├── dashboard_3_student_analytics.png   # Screenshot: Student Analytics
    ├── dashboard_4_country_comparison.png  # Screenshot: Country Comparison
    └── README.md                # Dashboard walkthrough with screenshots
```

---

## The Six Key Performance Indicators (KPIs)

Every KPI is calculated with a transparent, documented formula:
1. **Global Ranking Score (0–100):** Sourced from the QS Overall Score. For institutions ranked outside the published top 500 score band, an inverse percentile rank formula was applied.
2. **Research Impact Score (0–100):** Sourced from the QS Citations per Faculty Score and supported by THE Citation Score.
3. **Faculty-to-Student Ratio:** Sourced as the actual ratio of students per academic staff member from WUR 2023 / THE 2024 (e.g. 8.2:1 for MIT, 10.6:1 for Oxford).
4. **International Student Percentage (0–100%):** True percentage of international students from WUR 2023 (e.g. 33.0% for MIT, 42.0% for Oxford).
5. **Academic Reputation Score (0–100):** Sourced from the QS Academic Reputation Score.
6. **Research Productivity Index (0–100):** Derived composite index combining research volume, citations, and international collaboration:
   $$\text{Research Productivity Index} = 0.50 \times \text{Research Score} + 0.30 \times \text{Citations Score} + 0.20 \times \text{International Research Network Score}$$

---

## Summary of Results & Quality Checks
- **Data Completeness:** 100% completeness on required university and country dimensions (target: >95%).
- **Key Uniqueness:** Zero duplicate IDs in `dim_university` and `dim_country`.
- **Referential Integrity:** 100% of rows in all fact tables link directly to valid dimension keys (0 orphan records).
- **Interlinking:** Filter actions passing `university_id` and `country_id` allow users to drill from high-level university rankings down into research output, student profiles, and country-level education benchmarks.
