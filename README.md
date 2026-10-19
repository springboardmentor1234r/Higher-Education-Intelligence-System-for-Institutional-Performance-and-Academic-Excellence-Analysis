# EduVision — Higher Education Intelligence System

An end-to-end data engineering pipeline and interactive analytics dashboard suite built to analyze institutional performance, research impact, student demographics, and macro-level education indicators across top global universities.

---

## 1. Project Overview

The **EduVision Higher Education Intelligence System** integrates multi-year global university rankings (QS 2025, THE 2024, WUR 2023) with World Bank Education Statistics (EdStats). The system standardizes heterogeneous data structures into a clean star-schema dimensional model, engineers six core academic KPIs, and delivers four interlinked interactive dashboards available both as a native Tableau workbook (`dashboard/EduVision_DV.twbx`) and a standalone interactive web application (`dashboard/index.html`).

---

## 2. Data Sources

| Dataset Name | Source File | Record Scope | Primary Metrics / Attributes |
|---|---|---|---|
| **QS World University Rankings 2025** | `data/raw/qs_2025.csv` | ~1,500 institutions | Academic reputation, employer reputation, faculty/student score, citations per faculty, international faculty/student scores, overall score & rank. |
| **THE World University Rankings 2024** | `data/raw/the_2024.csv` | ~1,900 institutions | Teaching, research environment, research quality/citations, international outlook, industry income, student/staff ratio, % international students. |
| **World University Rankings 2023** | `data/raw/wur_2023.csv` | ~1,800 institutions (104 countries) | Overall rank, total headcount, student-per-staff ratio, female:male ratio, international student %, teaching/research/citation scores. |
| **World Bank Education Statistics** | `data/raw/world_bank_edstats/` | 240+ countries & territories | Primary to tertiary enrollment rates, government education expenditure (% GDP), literacy rates, completion indicators. |

---

## 3. Data Pipeline & Dimensional Architecture

The pipeline executes five automated Python modules sequentially (`notebooks_or_scripts/`):

```
raw/ (Original CSVs) 
  ├── 01_data_loading.py        --> Audit shapes, missingness, schema types
  ├── 02_data_cleaning.py       --> Strip whitespace, parse numericals, handle nulls
  ├── 03_standardization.py     --> Normalize country/university names, generate PKs (university_id, country_id)
  ├── 04_kpi_engineering.py     --> Build star schema fact tables & calculate 6 KPIs
  └── 05_validation.py          --> Automated QA checks (0 duplicate PKs, 100% referential integrity)
```

### Star Schema Data Model
- **`dim_country`**: `country_id` (PK), `country_name`, `region`, `income_group`, `iso_code`
- **`dim_university`**: `university_id` (PK), `university_name`, `country_id` (FK), `country_name`, `region`
- **`fact_university_performance`**: `university_id` (FK), `year`, `global_rank`, `overall_score`, `academic_reputation`, `employer_reputation`
- **`fact_research`**: `university_id` (FK), `year`, `research_score`, `citation_score`, `research_impact`, `research_productivity`
- **`fact_student`**: `university_id` (FK), `year`, `total_students`, `students_per_staff`, `international_students`, `international_student_percentage`
- **`fact_country_education`**: `country_id` (FK), `year`, `indicator_code`, `indicator_name`, `value`

---

## 4. Key Performance Indicators (KPIs)

The system engineers six standardized KPIs (`docs/kpi_definitions_and_formulas.md`):

1. **Global Ranking Score (`kpi1_global_ranking_score`)**
   - *Formula*: Direct `overall_score` (0–100); rank-decay formula $\max(10, 100 - (\text{global\_rank} - 1) \times 0.05)$ applied when score is unpublished.
2. **Research Impact Score (`kpi2_research_impact_score`)**
   - *Formula*: Citations per faculty / citation score index (0–100 scale).
3. **Faculty-to-Student Ratio (`kpi3_faculty_student_ratio`)**
   - *Formula*: Direct `students_per_staff` headcount ratio.
4. **International Student Percentage (`kpi4_international_student_pct`)**
   - *Formula*: Direct percentage of international students (`%`).
5. **Academic Reputation Score (`kpi5_academic_reputation_score`)**
   - *Formula*: Survey-based academic peer reputation score (0–100 scale).
6. **Research Productivity Index (`kpi6_research_productivity_index`)**
   - *Formula*: Weighted composite score: $0.50 \times \text{research\_score} + 0.50 \times \text{citation\_score}$. *(QS Sustainability Score excluded per specifications)*.

---

## 5. Dashboards & Interlinking Features

The suite contains four interactive dashboard views:

1. **University Overview** (Landing View): Executive KPI summary cards, ranked university data table, regional distribution chart, and multi-parameter filters.
2. **Research Analytics**: Deep-dive into institutional research scores, citation impact scatter plot, productivity index, and multi-year research trends.
3. **Student Analytics**: Analysis of total enrollment headcounts vs international students, faculty-to-student ratios, and institutional diversity.
4. **Country Comparison**: Macro-level country map, public education expenditure (% GDP), and gross tertiary enrollment rates.

**Interlinking Action Filters**: Selecting an institution in the `University Overview` table dynamically filters `Student Analytics`, `Research Analytics`, and `Country Comparison` views to the selected institution and its host country.

---

## 6. How to Reproduce the Data Pipeline

### Prerequisites
- Python 3.9+ with `pandas`, `numpy`, `openpyxl`

### Execution Steps
1. Place raw source CSV files in `data/raw/` (including `world_bank_edstats/` folder).
2. Execute pipeline scripts sequentially:
   ```bash
   python notebooks_or_scripts/01_data_loading.py
   python notebooks_or_scripts/02_data_cleaning.py
   python notebooks_or_scripts/03_standardization.py
   python notebooks_or_scripts/04_kpi_engineering.py
   python notebooks_or_scripts/05_validation.py
   ```
3. Cleaned dimensions and fact tables will be output to `data/cleaned/` and final datasets to `data/final/`.
4. Open `dashboard/index.html` in any modern web browser or launch `dashboard/EduVision_DV.twbx` in Tableau Desktop / Reader.

---

## 7. Known Limitations & Technical Decisions

- **Strict Entity Resolution**: Matching across QS, THE, and WUR required exact token-set name alignment within canonical countries to eliminate false-positive joins. Unmatched institutions were assigned unique `university_id`s.
- **Null Value Governance**: Missing scores in raw sources were kept as `NaN`/null values rather than zero-filled, preventing artificial distortion of regional averages.
- **World Bank EdStats Alignment**: Rank datasets cover 2023–2025; World Bank EdStats indicators use the latest available reported country baseline.
- **Known Tableau Action Filter Quirk**: During workbook development in Tableau Desktop, action filters created via GUI omitted the explicit source dashboard reference (`dashboard="University Overview"`), defaulting to sheet-level scope (`<source worksheet="Top Universities" />`). This prevented cross-dashboard filter propagation upon navigation. The `.twb` XML was hand-edited under `<actions>` to add explicit `dashboard="University Overview"` tags, restoring interlinking. If rebuilding the workbook from scratch in Tableau Desktop, verify that filter actions specify the source dashboard explicitly.

---

## 8. Repository Structure

```
EduVision_DV/
├── data/
│   ├── raw/                      # Original raw CSVs (EdStatsData.csv excluded from git)
│   ├── cleaned/                  # Dimension and fact tables (dim_*, fact_*)
│   └── final/                    # Merged final dataset and KPI summary tables
├── notebooks_or_scripts/          # Data processing pipeline scripts (01 to 05)
├── dashboard/
│   ├── EduVision_DV.twbx          # Tableau Packaged Workbook
│   ├── index.html                # Standalone Interactive Web Dashboard
│   └── data/                     # JSON/JS datasets powering web app
├── docs/                         # Complete documentation
│   ├── data_dictionary.md
│   ├── data_model.md
│   ├── kpi_definitions_and_formulas.md
│   ├── cleaning_and_matching_methodology.md
│   ├── raw_data_validation_report.md
│   ├── data_quality_report.md
│   ├── dashboard_testing_report.md
│   ├── qa_checklist.md
│   ├── limitations.md
│   └── tableau_build_guide.md
├── project_brief.md
├── README.md
└── .gitignore
```
