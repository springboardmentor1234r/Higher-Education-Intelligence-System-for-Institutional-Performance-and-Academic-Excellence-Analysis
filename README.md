# EduVision_DV — Higher Education Intelligence System

[![Tableau](https://img.shields.io/badge/Tableau-2024.1+-E97627?style=for-the-badge&logo=Tableau&logoColor=white)](https://public.tableau.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Project%20Status-Complete-success?style=for-the-badge)]()

An enterprise-grade, four-dashboard analytical suite designed to synthesize global university rankings into actionable strategic intelligence. EduVision_DV integrates data from **QS World University Rankings 2025**, **Times Higher Education World University Rankings 2024**, **World University Rankings 2023**, and the **World Bank EdStats** to enable university administrators, academic researchers, policymakers, and students to evaluate institutional performance, compare universities globally, analyze research output, and identify worldwide education trends.

---

## Interactive Dashboard Suite

### 1. University Overview
*Global university ranking landscape, institutional volume by country, and academic reputation correlation.*

![Dashboard 1: University Overview](Milestone%203/Screenshots/dashboard_1_university_overview.png)

---

### 2. Research Analytics
*Executive tri-panel bar layout evaluating QS Research Impact Score, QS Citations per Faculty, and Research Productivity Index with single-university enlargement (`entire-view`).*

![Dashboard 2: Research Analytics](Milestone%203/Screenshots/dashboard_2_research_analytics.png)

---

### 3. Student Analytics
*International student mobility, total student enrollment distribution across top countries, and faculty-to-student capacity ratios.*

![Dashboard 3: Student Analytics](Milestone%203/Screenshots/dashboard_3_student_analytics.png)

---

### 4. Country Comparison
*National education benchmarking, top performing nations, country ranking comparisons, and single-country isolation on click.*

![Dashboard 4: Country Comparison](Milestone%203/Screenshots/dashboard_4_country_comparison.png)

---

## Project Structure

The project is strictly organized into five standard milestone folders:

```
├── Milestone 1/                       # Data Collection & Preparation (Weeks 1–2)
│   ├── Module 1/                      # University Data Collection
│   │   ├── raw/                       # Approved raw datasets (QS 2025, THE 2024)
│   │   ├── data_collection.py         # Automated data ingestion & schema validation script
│   │   └── university_raw_data.csv    # Consolidated raw ranking dataset
│   └── Module 2/                      # Data Cleaning & Transformation
│       ├── education_cleaning.ipynb   # Cleaning, deduplication & normalization notebook
│       └── university_cleaned.csv     # Tableau-ready cleaned dataset
│
├── Milestone 2/                       # KPI Engineering & Dashboard Planning (Weeks 3–4)
│   ├── Module 3/                      # Education KPI Engineering
│   │   ├── generate_education_kpis.py # Python script computing the 6 standardized KPIs
│   │   └── university_final_dataset.xlsx # Optimized Excel data model for Tableau
│   └── Module 4/                      # Dashboard Planning & Prototyping
│       ├── dashboard_storyboard.pdf   # Complete wireframe designs and storyboard layouts
│       └── eduvision_prototype.twbx   # Interactive prototype workbook
│
├── Milestone 3/                       # Dashboard Development & Integration (Weeks 5–6)
│   ├── Screenshots/                   # Full-resolution screenshots of all 4 dashboards
│   ├── Module 5/                      # University Overview & Research Analytics
│   │   └── eduvision_dashboard_v1.twbx
│   └── Module 6/                      # Student Analytics, Country Comparison & Full Integration
│       ├── EduVision_DV.twbx          # Complete, fully interlinked Tableau workbook
│       └── Book2.twb                  # Tableau workbook with schema-compliant XML
│
├── Milestone 4/                       # Testing, Quality Assurance & Delivery (Weeks 7–8)
│   ├── Module 7/                      # Testing and Validation
│   │   ├── QA_Checklist_and_Validation_Report.md
│   │   └── Dashboard_Testing_Report.md
│   └── Module 8/                      # Project Documentation and User Guide
│       └── Project_Documentation_and_User_Guide.md
│
└── Final Project/                     # Final Deliverables
    ├── Final PPT/                     # Executive Presentations
    │   ├── Final_PPT.pptx             # 10-slide executive PowerPoint with embedded dashboard screenshots
    │   └── EduVision_DV_Project_Presentation.pdf
    ├── Complete Tableau Dashboard Link/
    │   ├── Complete_Tableau_Dashboard_Link.md
    │   └── Tableau_Dashboard_Link.txt
    └── Screenshots/                   # Project visual showcase assets
```

---

## Standardized Higher Education KPIs

| KPI | Name | Description & Formula | Source |
| :---: | :--- | :--- | :--- |
| **KPI 1** | **Global Ranking Score** | Overall institutional score (0–100 scale) based on academic performance. | QS World Rankings |
| **KPI 2** | **Research Impact Score** | Citations per faculty member reflecting global scholarly influence. | QS World Rankings |
| **KPI 3** | **Faculty-to-Student Ratio** | Ratio of student enrollment to academic teaching staff (e.g. 1 : 17.3). | WUR / THE Rankings |
| **KPI 4** | **International Student %** | Share of international students enrolled in the university body. | WUR / THE Rankings |
| **KPI 5** | **Academic Reputation Score** | Survey-based peer review metric across 100,000+ academics worldwide. | QS World Rankings |
| **KPI 6** | **Research Productivity Index** | Composite index combining publication volume, citations, and collaboration. | Composite Derived |

---

## Technical Features & Highlights

1. **Uniform Navigation Bar**: Mathematically aligned 4-button header across all dashboards spanning full canvas ($w = 98,828$, identical heights and hover states).
2. **Context Filter Pipeline**: Implemented `context="true"` across university and country action filters, ensuring top-10 sort filters never yield blank charts.
3. **Single-University Cross-Enlargement**: In Research Analytics, selecting any university on one bar chart filters the other two charts to that university only, using `<zoom type="entire-view" />` to expand the single bar across the entire panel.
4. **Stable KPI Card Styling**: Solid `#ffffff` text styling and eliminated highlight brush actions so KPI cards never dim or fade during interactive filtering.
5. **Strict Tableau XML Compliance**: 100% conforming to Tableau DTD with 0 schema violations.
