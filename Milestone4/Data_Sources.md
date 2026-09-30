# EduVision\_DV — Dataset Sources

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Document** | Dataset Sources & References |
| **Report Date** | 2026-09-30 |
| **Document Version** | v1.0 |

---

## 1. Overview

EduVision\_DV is built on publicly available higher-education datasets to analyse university rankings, research performance, student indicators, and country-level education trends.

The project integrates **four primary datasets**, each selected for a distinct analytical purpose rather than being uniformly merged into a single flat table:

| # | Dataset | Edition |
|---|---------|---------|
| 1 | QS World University Rankings | 2025 |
| 2 | Times Higher Education (THE) World University Rankings | 2024 |
| 3 | World University Rankings | 2023 |
| 4 | World Bank Education Statistics | Country-level (multi-year) |

---

## 2. Dataset Summary

| Dataset | Edition | Primary Analytical Purpose |
|---------|---------|---------------------------|
| QS World University Rankings | 2025 | University performance, rankings, and reputation indicators |
| Times Higher Education World University Rankings | 2024 | Research, teaching, citations, and international outlook |
| World University Rankings | 2023 | Student enrolment, research output, and citation indicators |
| World Bank Education Statistics | Country-level | Country-level education benchmarking and regional trends |

---

## 3. QS World University Rankings 2025

### 3.1 Source

| Field | Detail |
|-------|--------|
| **Publisher** | QS Quacquarelli Symonds |
| **Edition** | 2025 |
| **Access** | Kaggle — Public Dataset |
| **URL** | [QS World University Rankings 2025 — Kaggle](https://www.kaggle.com/datasets/melissamonfared/qs-world-university-rankings-2025) |
| **Local File** | `QS World University Rankings 2025 (Top global universities).csv` |

### 3.2 Dataset Dimensions

| Attribute | Value |
|-----------|-------|
| Rows | 1,503 |
| Columns | 28 |

### 3.3 Key Fields Used

| Field | Description |
|-------|-------------|
| `RANK_2025` | Current global ranking position |
| `RANK_2024` | Previous year ranking position |
| `Institution_Name` | University name |
| `Location` | Country of institution |
| `Region` | Geographic region |
| `Academic_Reputation_Score` | Score from QS academic reputation survey |
| `Employer_Reputation_Score` | Score from QS employer reputation survey |
| `Faculty_Student_Score` | Faculty-to-student ratio score |
| `Citations_per_Faculty_Score` | Research citation score per faculty |
| `International_Faculty_Score` | Proportion of international faculty |
| `International_Students_Score` | Proportion of international students |
| `International_Research_Network_Score` | Research collaboration network score |
| `Employment_Outcomes_Score` | Graduate employability score |
| `Sustainability_Score` | Sustainability indicator score |
| `Overall_Score` | Composite QS overall score |

### 3.4 Primary Use in EduVision\_DV

The QS dataset is the principal source for:
- **University Overview** — global rankings, reputation, and overall performance
- Academic reputation analysis
- International student and faculty indicators
- Overall institutional performance benchmarking

---

## 4. Times Higher Education World University Rankings 2024

### 4.1 Source

| Field | Detail |
|-------|--------|
| **Publisher** | Times Higher Education (THE) |
| **Edition** | 2024 |
| **Access** | Public dataset |
| **Local File** | `TIMES_WorldUniversityRankings_2024.csv` |

### 4.2 Dataset Dimensions

| Attribute | Value |
|-----------|-------|
| Rows | 2,673 |
| Columns | 29 |

### 4.3 Key Fields Used

| Field | Description |
|-------|-------------|
| `rank` | THE global ranking position |
| `name` | University name |
| `scores_overall` | THE composite overall score |
| `scores_teaching` | Teaching quality score |
| `scores_research` | Research environment score |
| `scores_citations` | Research influence (citation) score |
| `scores_industry_income` | Knowledge transfer and industry income score |
| `scores_international_outlook` | International diversity score |
| `stats_number_students` | Total student enrolment |
| `stats_student_staff_ratio` | Student-to-staff ratio |
| `stats_pc_intl_students` | Percentage of international students |
| `stats_female_male_ratio` | Gender ratio among students |
| `location` | Country of institution |

### 4.4 Primary Use in EduVision\_DV

The THE dataset provides complementary performance indicators for:
- **Research Analytics** — research performance, citation performance, and research output
- Teaching quality analysis
- International outlook metrics
- Student and staff ratio indicators

---

## 5. World University Rankings 2023

### 5.1 Source

| Field | Detail |
|-------|--------|
| **Publisher** | Center for World University Rankings (CWUR) |
| **Edition** | 2023 |
| **Access** | Kaggle — Public Dataset |
| **URL** | [World University Rankings 2023 — Kaggle](https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023) |
| **Local File** | `World University Rankings 2023.csv` |

### 5.2 Dataset Dimensions

| Attribute | Value |
|-----------|-------|
| Rows | 2,341 |
| Columns | 13 |

### 5.3 Primary Use in EduVision\_DV

This dataset provides supplementary university-level indicators covering:

| Indicator | Dashboard |
|-----------|-----------|
| Number of students | Student Analytics |
| Students per staff | Student Analytics |
| International students percentage | Student Analytics |
| Research performance score | Research Analytics |
| Citation performance score | Research Analytics |
| Teaching performance score | Research Analytics |
| Overall university performance | University Overview |

---

## 6. World Bank Education Statistics

### 6.1 Source

| Field | Detail |
|-------|--------|
| **Publisher** | The World Bank |
| **Coverage** | Country-level, multi-year |
| **Access** | Kaggle — Public Dataset |
| **URL** | [World Bank Education Statistics — Kaggle](https://www.kaggle.com/datasets/theworldbank/education-statistics) |

### 6.2 Primary Use in EduVision\_DV

The World Bank Education Statistics dataset provides country-level education indicators and is treated separately from university-level datasets. It is the primary source for the **Country Comparison** dashboard.

It supports:
- Country-level education benchmarking
- Regional education trend analysis
- Top performing countries comparison

### 6.3 Dataset Integration Model

The relationship between university-level and country-level data in EduVision\_DV follows this hierarchy:

```
University Data  (QS · THE · CWUR 2023)
       ↓
  Country Level
       ↓
Country Education Indicators  (World Bank)
```

University records are linked to their respective countries, allowing cross-dataset analysis between institutional performance and national education statistics.

---

## 7. Data Source Reference Table

| Dataset | Edition | URL | Local File |
|---------|---------|-----|------------|
| QS World University Rankings | 2025 | [Kaggle](https://www.kaggle.com/datasets/melissamonfared/qs-world-university-rankings-2025) | `QS World University Rankings 2025 (Top global universities).csv` |
| THE World University Rankings | 2024 | Public dataset | `TIMES_WorldUniversityRankings_2024.csv` |
| World University Rankings | 2023 | [Kaggle](https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023) | `World University Rankings 2023.csv` |
| World Bank Education Statistics | Country-level | [Kaggle](https://www.kaggle.com/datasets/theworldbank/education-statistics) | World Bank export |

---

*EduVision\_DV — Milestone 4 · Dataset Sources Document · Report Date: 2026-09-30*
