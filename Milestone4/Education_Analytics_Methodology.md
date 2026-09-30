# EduVision\_DV — Education Analytics Methodology

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Document** | Education Analytics Methodology |
| **Report Date** | 2026-09-30 |
| **Document Version** | v1.0 |

---

## 1. Purpose

EduVision\_DV transforms publicly available higher-education datasets into an integrated analytical system for studying:

- University performance and global rankings
- Research output, impact, and productivity
- Student characteristics, diversity, and internationalization
- Country-level education trends and regional benchmarking

The methodology follows a structured project workflow across six phases:

| Phase | Activity |
|-------|----------|
| **Phase 1** | Data Collection |
| **Phase 2** | Dataset Validation |
| **Phase 3** | Data Cleaning |
| **Phase 4** | KPI Engineering |
| **Phase 5** | Tableau Dashboard Development |
| **Phase 6** | Testing & Validation |

---

## 2. End-to-End Workflow

```
Data Collection
      ↓
Dataset Validation
      ↓
Data Cleaning
      ↓
KPI Engineering
      ↓
Tableau Dashboard Development
      ↓
Testing & Validation (Module 7)
      ↓
Final Delivery
```

---

## 3. Phase 1 — Data Collection

### 3.1 Approach

Datasets are selected based on their analytical purpose. Each dataset is assigned to a specific analytical domain rather than being uniformly merged into a single flat table.

### 3.2 Datasets Used

| Dataset | Edition | Analytical Domain |
|---------|---------|-------------------|
| QS World University Rankings | 2025 | University performance, reputation, and ranking |
| Times Higher Education (THE) World University Rankings | 2024 | Research, teaching, citations, international outlook |
| World University Rankings | 2023 | Student enrolment, research, and citation indicators |
| World Bank Education Statistics | Country-level | Country-level education benchmarking |

### 3.3 Analytical Domain Mapping

| Domain | Primary Dataset(s) |
|--------|-------------------|
| University performance | QS 2025 |
| Research analytics | THE 2024 · World University Rankings 2023 |
| Student analytics | THE 2024 · World University Rankings 2023 |
| Country comparison | QS 2025 · World Bank Education Statistics |

---

## 4. Phase 2 — Dataset Validation

Before processing, each dataset is assessed across the following dimensions:

### 4.1 Structural Validation

| Check | Description |
|-------|-------------|
| Row count | Number of records in the dataset |
| Column count | Number of fields available |
| University name field | Presence and format of the primary institution identifier |
| Country field | Presence of country/location identifier |
| Year field | Presence of ranking year or data year field |

### 4.2 Content Validation

| Check | Description |
|-------|-------------|
| Key indicator availability | Presence of required KPI source fields |
| Missing value assessment | Volume and pattern of null values across critical fields |
| Duplicate rows | Identification of exact or near-duplicate records |
| Duplicate universities | Identification of the same institution appearing multiple times |
| Data types | Correct typing of numeric, string, and date fields |

### 4.3 University Match Rate

Dataset completeness and university match rate across datasets are treated as **separate concepts**.

> A low university match rate between two datasets does not automatically make a dataset unusable. Datasets are assessed on the quality and coverage of their own indicators independently.

---

## 5. Phase 3 — Data Cleaning

Data cleaning is completed prior to Tableau development to ensure a stable, validated analytical foundation.

### 5.1 Cleaning Pipeline

```
Raw Dataset
     ↓
Load Data
     ↓
Inspect Data (shape, types, sample rows)
     ↓
Remove Duplicate Rows
     ↓
Standardize Column Names (lowercase, underscores)
     ↓
Clean University Names (trim whitespace, normalize casing)
     ↓
Clean Country Names (standardize country spelling and codes)
     ↓
Handle Missing Values (preserve nulls — no zero-substitution)
     ↓
Convert Data Types (numeric fields to float/int, dates to datetime)
     ↓
Validate Cleaned Data (range checks, format checks)
     ↓
Save Cleaned Dataset
```

### 5.2 Missing Value Policy

Missing values in analytical fields are **preserved as null** throughout the cleaning pipeline.

| Rule | Detail |
|------|--------|
| No zero-substitution | Missing numeric values are not replaced with 0 |
| No mean/median imputation | KPI source fields are not statistically imputed |
| Null propagation | If a source field is null, the derived KPI remains null |

This policy ensures that institutions with incomplete data are not artificially penalized or inflated in any aggregation or ranking calculation.

### 5.3 Name Standardization

University and country name standardization is critical for cross-dataset joins. The cleaning process:

- Strips leading and trailing whitespace
- Normalizes capitalization (title case)
- Resolves common spelling variants (e.g., `USA` → `United States`)
- Removes special characters that may cause join failures

### 5.4 Output

| Output File | Description |
|-------------|-------------|
| `university_final_dataset.xlsx` | Consolidated, cleaned dataset used in Tableau and KPI calculations |
| Sheet: `kpi_summary` | KPI-level summary per university, used for all dashboard KPI cards and validation |

---

## 6. Phase 4 — KPI Engineering

### 6.1 Overview

Six KPIs are engineered from the cleaned dataset. Each KPI has a defined source, normalization method, and null-handling rule.

| # | KPI | Scale |
|---|-----|-------|
| 1 | Global Ranking Score | 0 – 100 |
| 2 | Research Impact Score | 0 – 100 |
| 3 | Faculty-to-Student Ratio | Ratio |
| 4 | International Student Percentage | % (0 – 100) |
| 5 | Academic Reputation Score | 0 – 100 |
| 6 | Research Productivity Index | 0 – 100 |

### 6.2 Normalization Method — Global Ranking Score

The raw global rank position is converted to a 0–100 score using min-max normalization:

```
global_ranking_score = 100 × (Max_Rank − global_rank) / (Max_Rank − Min_Rank)
```

- Rank 1 (best) → Score = 100
- Lowest rank → Score → 0
- Score decreases monotonically as rank number increases

### 6.3 Normalization Method — Research Productivity Index

The Research Productivity Index is computed as a normalized composite of available research performance indicators:

```
Research Productivity Index = Normalized mean of available research sub-indicators
                              (null indicators excluded from the mean)
```

If all contributing indicators are null for an institution, the index is null.

### 6.4 KPI Engineering Rules

| Rule | Description |
|------|-------------|
| Source fidelity | Each KPI uses only its defined source field(s) |
| No fabrication | No synthetic or estimated values are introduced |
| Null preservation | Null source fields yield null KPI values |
| Partial availability | Where multiple sources contribute to one KPI, available sources are used and null sources excluded |

---

## 7. Phase 5 — Tableau Dashboard Development

### 7.1 Dashboard Architecture

The four dashboards are developed as an integrated Tableau workbook (`EduVision_DV.twbx`), sharing common dimensions and connected through actions and navigation.

| Dashboard | Primary Analytical Focus |
|-----------|--------------------------|
| University Overview | Global rankings, reputation, and performance |
| Research Analytics | Research impact, citations, and productivity |
| Student Analytics | International students, faculty ratios, diversity |
| Country Comparison | Country benchmarking and regional trends |

### 7.2 Integration Mechanisms

| Mechanism | Purpose |
|-----------|---------|
| Dashboard Actions | Pass selected university or country between dashboards |
| Navigation Buttons | Move users through the dashboard sequence |
| Filters | Shared dimension filters (University, Country, Region, Ranking Year) |
| Parameter Actions | Allow users to switch the Performance Metric displayed in Country Comparison |

### 7.3 Development Principles

| Principle | Description |
|-----------|-------------|
| No data fabrication | Visuals only display fields that exist in the cleaned dataset |
| Field traceability | Every metric displayed in the workbook maps to a specific source field |
| Action-filter correctness | Clearing a selection resets dependent dashboards to the full dataset view |
| Parameter flexibility | The Performance Metric parameter allows user-controlled metric switching without dashboard duplication |

---

## 8. Phase 6 — Testing & Validation (Module 7)

### 8.1 Testing Scope

Module 7 validates the complete dashboard suite across five testing categories:

| Category | What Is Tested |
|----------|----------------|
| KPI Calculation Validation | All 6 KPIs verified against their source fields and expected ranges |
| Ranking Calculation Validation | `global_rank`, `normalized_rank`, and `global_ranking_score` consistency |
| Dashboard Interaction Testing | Filters, cross-dashboard linking, parameters, navigation, and filter clearing |
| Educational Metrics Validation | Source field mappings for all educational metrics across all dashboards |
| Dashboard-Specific Visual Validation | All 20 visuals across all 4 dashboards checked individually |

### 8.2 Testing Principles

| Principle | Description |
|-----------|-------------|
| No modification during testing | Dashboards are not changed during testing unless a confirmed error is found |
| Issue logging | Any issue found is documented with its correction before final validation |
| Evidence-based validation | Each test result is recorded with observed outcome, not assumed |

### 8.3 Evaluation Targets

| Target | Threshold | Result |
|--------|-----------|--------|
| KPI accuracy | > 95% of KPI checks pass | ✅ 6/6 (100%) |
| Major dashboard issues | Zero major issues in final tested state | ✅ None identified |
| Overall pass rate | > 95% | ✅ 100% |

### 8.4 Issues Identified and Resolved

Six issues were identified and corrected during the testing cycle prior to final validation:

| # | Issue | Correction |
|---|-------|------------|
| 1 | Research Impact Score aggregated as sum | Changed to average |
| 2 | Ranking chart axis set to fixed custom range | Changed to automatic range |
| 3 | Student Diversity Trends showing multiplied percentages | Percentage format corrected |
| 4 | Research Analytics retained previous selection after filter cleared | Action-filter clearing corrected |
| 5 | Charts contained excessive marks | Limited to Top 10 views where required |
| 6 | Regional Education Trends contained null region values and unnecessary labels | Null regions excluded; mark labels removed |

---

## 9. Final Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| `EduVision_DV.twbx` | Tableau workbook — 4 dashboards | Project root |
| `university_final_dataset.xlsx` | Cleaned and consolidated analytical dataset | `data/` |
| `QA_Checklist.md` | Module 7 QA checklist with all test results | `Milestone4/` |
| `Dashboard_Testing_Report.md` | Full dashboard testing report | `Milestone4/` |
| `KPI_Defination.md` | KPI definitions and calculation reference | `Milestone4/` |
| `Data_Sources.md` | Dataset sources and references | `Milestone4/` |
| `Dashboard_guide.md` | Dashboard user guide | `Milestone4/` |
| `Education_Analytics_Methodology.md` | This document — end-to-end methodology | `Milestone4/` |

---

## 10. Methodology Summary

| Phase | Input | Output | Status |
|-------|-------|--------|--------|
| Data Collection | Raw public datasets | 4 datasets selected | ✅ Complete |
| Dataset Validation | Raw datasets | Validation report per dataset | ✅ Complete |
| Data Cleaning | Raw datasets | `university_final_dataset.xlsx` | ✅ Complete |
| KPI Engineering | Cleaned dataset | `kpi_summary` sheet — 6 KPIs | ✅ Complete |
| Dashboard Development | Cleaned dataset + KPIs | `EduVision_DV.twbx` — 4 dashboards | ✅ Complete |
| Testing & Validation | Dashboard workbook | QA Checklist + Dashboard Testing Report | ✅ Complete |

---

*EduVision\_DV — Milestone 4 · Education Analytics Methodology · Report Date: 2026-09-30*
