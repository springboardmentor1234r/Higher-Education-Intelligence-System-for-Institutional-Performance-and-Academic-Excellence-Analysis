# EduVision – Dataset Sources

## Project

Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

---

## 1. Overview

EduVision integrates university ranking datasets with country-level World Bank education indicators to analyze institutional performance, research performance, student characteristics, and national education conditions.

The project uses four primary data sources.

---

## 2. QS World University Rankings 2025

**Dataset:** QS World University Rankings 2025

**Year:** 2025

**Purpose:**
- Global university ranking
- Overall ranking score
- Academic reputation
- Employer reputation
- Faculty-related indicators
- Citations per faculty
- Internationalization
- Sustainability

**Primary use in EduVision:**
- University Overview
- Global Ranking Score
- Academic Reputation Score
- Research Impact Score
- University ranking analysis

---

## 3. Times Higher Education World University Rankings 2024

**Dataset:** The World University Rankings 2024

**Year:** 2024

**Purpose:**
- Overall university performance
- Teaching
- Research
- Citations
- Industry income
- International outlook
- Student/staff ratio
- International student percentage

**Primary use in EduVision:**
- Research Analytics
- Student Analytics
- University performance comparison
- Research score and citation analysis

---

## 4. World University Rankings 2023

**Dataset:** World University Rankings 2023

**Year:** 2023

**Purpose:**
- Historical university performance
- Research indicators
- Citation indicators
- Student/staff indicators
- International student indicators

**Primary use in EduVision:**
- Historical research analysis
- Student analytics
- Performance comparison across years

---

## 5. World Bank Education Statistics

**Dataset:** World Bank Education Statistics

**Primary files:**
- EdStatsData.csv
- EdStatsCountry.csv

**Year used for selected education indicators:** 2015

**Purpose:**
Country-level education analysis including:

- Tertiary enrollment
- Tertiary graduation
- Female tertiary participation
- Pupil-teacher ratio
- Youth literacy
- Tertiary graduates

**Primary use in EduVision:**
- Country Comparison dashboard
- Education performance benchmarking
- Regional education comparison

---

## 6. Data Integration

The datasets were processed using Python and Pandas.

The integrated model uses:

- `dim_university`
- `fact_university_performance`
- `fact_research`
- `fact_student`
- `fact_university_kpi`
- `fact_country_education`

University records are identified using `university_id`.

World Bank education data is maintained at country level and linked using standardized country codes.

---

## 7. Data Quality

The final integrated dataset contains:

**3,530 university records**

World Bank country linkage:

**3,466 linked records**

**98.19% linkage**

The project does not treat missing ranking values as zero. Missing values are retained where source data is unavailable.

---

## 8. Important Data Handling Notes

Country names can differ between datasets. Country standardization was therefore performed before integration.

Examples include:

- Russia / Russian Federation
- China / China (Mainland)
- Taiwan naming differences
- Hong Kong naming differences

The raw datasets are preserved separately from cleaned and processed datasets.

---

## 9. Data Processing Tools

| Activity | Technology |
|---|---|
| Data collection | CSV datasets |
| Data cleaning | Python |
| Data transformation | Pandas |
| Numerical processing | NumPy |
| KPI engineering | Python |
| Visualization | Tableau |
| Documentation | Markdown |
| Version control | Git and GitHub |

## OpenAlex Publication Data

**Source:** OpenAlex

OpenAlex was used to add university-level publication analysis to the Research Analytics dashboard.

Publication counts were obtained from OpenAlex institution-level yearly work counts using the `counts_by_year` data for:

- 2023
- 2024
- 2025

A conservative institution-matching process was used to avoid incorrectly assigning publication counts to universities. Matching considered university name similarity and country consistency.

### Validated Coverage

- Total universities in the integrated dataset: 3,530
- Universities with validated OpenAlex institution matches: 60
- Validated coverage: 1.70%
- Publication counts available for 2023: 60
- Publication counts available for 2024: 60
- Publication counts available for 2025: 60

The validated publication dataset is stored in:

`data/publications/processed/openalex_publications_validated.csv`

The Tableau-ready publication dataset is stored in:

`data/publications/processed/university_publications_tableau.csv`

### Publication Analysis Limitation

OpenAlex publication analysis currently covers only the universities for which a reliable institution match was validated. The publication counts are therefore presented as a validated subset analysis and are not interpreted as complete publication coverage for all 3,530 universities.

Unmatched or ambiguous institutions were excluded rather than assigning potentially incorrect publication counts.