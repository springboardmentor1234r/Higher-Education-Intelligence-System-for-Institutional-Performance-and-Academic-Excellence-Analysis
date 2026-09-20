# EduVision_DV: Relational Star Schema Data Dictionary

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Higher Education Data Modeling  
**Date:** September 2026  

---

## 1. Dimensional Architecture Overview

The **EduVision_DV** analytical model implements an audit-compliant **Star Schema** designed for high-performance Tableau querying, eliminate join ambiguity, and prevent row duplication.

```
                              +------------------------+
                              |     dim_university     |
                              +------------------------+
                              | PK: university_id      |
                              |     university_name    |
                              | FK: country_id         |
                              |     country_name       |
                              |     region             |
                              +-----------+------------+
                                          |
        +---------------------------------+---------------------------------+
        | 1:1                             | 1:1                             | 1:1
        v                                 v                                 v
+-------------------------------+ +-------------------------------+ +-------------------------------+
|  fact_university_performance  | |        fact_research          | |         fact_student          |
+-------------------------------+ +-------------------------------+ +-------------------------------+
| FK: university_id             | | FK: university_id             | | FK: university_id             |
|     year                      | |     year                      | |     year                      |
|     global_rank               | |     research_score            | |     total_students            |
|     overall_score             | |     citation_score            | |     students_per_staff        |
|     academic_reputation       | |     teaching_score            | |     intl_student_pct          |
|     employer_reputation       | |     industry_income_score     | |     female_male_ratio         |
|     citations_score           | |     intl_outlook_score        | |     intl_students_count       |
|     research_network_score    | |     research_productivity     | +-------------------------------+
+-------------------------------+ +-------------------------------+
                                          |
                                          | M:1
                                          v
                              +------------------------+
                              |      dim_country       |
                              +------------------------+
                              | PK: country_id         |
                              |     country_name       |
                              |     region             |
                              +-----------+------------+
                                          | 1:M
                                          v
                              +------------------------+
                              | fact_country_education |
                              +------------------------+
                              | FK: country_id         |
                              |     country_name       |
                              |     year               |
                              |     indicator          |
                              |     value              |
                              +------------------------+
```

---

## 2. Table Specifications

### 2.1 `dim_university` (Institutional Dimension Table)
- **Granularity:** One row per higher education institution.
- **Row Count:** 1,503 records.
- **Primary Key:** `university_id`.

| Column Name | Data Type | Constraint | Sample Value | Business Definition & Source Mapping |
|---|---|---|---|---|
| `university_id` | VARCHAR(10) | PRIMARY KEY, NOT NULL | `U0001` | Unique surrogate key formatted with leading zeros (`U0001`..`U1503`). |
| `university_name`| VARCHAR(255)| NOT NULL | `Massachusetts Institute of Technology (MIT)` | Canonical institution name after entity resolution and alias reconciliation. |
| `country_id` | VARCHAR(10) | FOREIGN KEY, NOT NULL | `C0001` | References `dim_country.country_id`. |
| `country_name` | VARCHAR(100)| NOT NULL | `United States` | Standardized sovereign country of institutional residence. |
| `region` | VARCHAR(50) | NOT NULL | `North America` | Continental geographic grouping (North America, Europe, Asia, Latin America, Oceania, Africa). |

---

### 2.2 `dim_country` (Geopolitical Dimension Table)
- **Granularity:** One row per sovereign country or territory.
- **Row Count:** 106 records.
- **Primary Key:** `country_id`.

| Column Name | Data Type | Constraint | Sample Value | Business Definition & Source Mapping |
|---|---|---|---|---|
| `country_id` | VARCHAR(10) | PRIMARY KEY, NOT NULL | `C0001` | Unique surrogate country key (`C0001`..`C0106`). |
| `country_name` | VARCHAR(100)| NOT NULL | `United States` | Harmonized geopolitical country name. |
| `region` | VARCHAR(50) | NOT NULL | `North America` | Continental macro-region for geographic aggregation. |

---

### 2.3 `fact_university_performance` (Core Rankings Fact Table)
- **Granularity:** One row per university per evaluation year.
- **Row Count:** 1,503 records.
- **Foreign Key:** `university_id` referencing `dim_university`.
- **Primary Source:** QS World University Rankings 2025.

| Column Name | Data Type | Nullable | Range / Format | Description & Business Logic |
|---|---|---|---|---|
| `university_id` | VARCHAR(10) | NO | `U0001`..`U1503` | Foreign key link to `dim_university`. |
| `year` | INTEGER | NO | `2025` | Assessment year. |
| `global_rank` | INTEGER | NO | `1` – `1503` | Official QS 2025 global institutional rank. |
| `overall_score` | FLOAT | NO | `0.07` – `100.0`| Published QS score for top 500; inverse percentile rank imputed for ranks > 500. |
| `academic_reputation` | FLOAT | YES | `0.0` – `100.0` | Global peer review academic survey score. |
| `employer_reputation` | FLOAT | YES | `0.0` – `100.0` | Global corporate recruiter survey score. |
| `faculty_student_score`| FLOAT | YES | `0.0` – `100.0`| QS academic staffing index (score, not raw ratio). |
| `citations_score` | FLOAT | YES | `0.0` – `100.0` | Normalized citations per faculty score. |
| `international_faculty`| FLOAT | YES | `0.0` – `100.0`| Cross-border faculty representation index. |
| `international_students`|FLOAT | YES | `0.0` – `100.0`| QS international student score index. |
| `research_network_score`|FLOAT| YES | `0.0` – `100.0`| International research collaboration network index. |
| `sustainability_score` | FLOAT | YES | `0.0` – `100.0` | Environmental and social sustainability index. |

---

### 2.4 `fact_research` (Research Productivity Fact Table)
- **Granularity:** One row per institution per evaluation year.
- **Row Count:** 849 records (verified exact entity matches).
- **Foreign Key:** `university_id` referencing `dim_university`.
- **Primary Source:** Times Higher Education (THE) World University Rankings 2024.

| Column Name | Data Type | Nullable | Range / Format | Description & Business Logic |
|---|---|---|---|---|
| `university_id` | VARCHAR(10) | NO | `U0001`..`U1503` | Foreign key link to `dim_university`. |
| `year` | INTEGER | NO | `2024` | Assessment year. |
| `research_score` | FLOAT | YES | `0.0` – `100.0` | THE research environment, volume, and funding score. |
| `citation_score` | FLOAT | YES | `0.0` – `100.0` | THE normalized citation impact score. |
| `teaching_score` | FLOAT | YES | `0.0` – `100.0` | THE teaching learning environment score. |
| `industry_income_score`| FLOAT | YES | `0.0` – `100.0`| THE knowledge transfer and commercial grant income score. |
| `international_outlook` | FLOAT | YES | `0.0` – `100.0`| THE international staff, students, and research co-authorship score. |
| `research_productivity` | FLOAT | NO | `10.5` – `99.87`| Composite KPI: $0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$. |

---

### 2.5 `fact_student` (Student Demographics Fact Table)
- **Granularity:** One row per institution per evaluation year.
- **Row Count:** 804 records (verified exact entity matches).
- **Foreign Key:** `university_id` referencing `dim_university`.
- **Primary Source:** World University Rankings (WUR) 2023.

| Column Name | Data Type | Nullable | Range / Format | Description & Business Logic |
|---|---|---|---|---|
| `university_id` | VARCHAR(10) | NO | `U0001`..`U1503` | Foreign key link to `dim_university`. |
| `year` | INTEGER | NO | `2023` | Assessment year. |
| `total_students` | FLOAT | YES | `513` – `414,438`| Full-time equivalent (FTE) student enrollment headcount. |
| `students_per_staff` | FLOAT | YES | `2.1` – `68.4` | Actual empirical ratio of students per academic staff member. |
| `intl_student_pct` | FLOAT | YES | `0.0%` – `87.0%`| True empirical percentage of international students. |
| `female_male_ratio` | VARCHAR(20)| YES | e.g. `48 : 52` | Institutional gender distribution ratio. |
| `intl_students_count` | FLOAT | YES | Calculated | Estimated international student headcount ($(\text{total} \times \text{pct}) / 100$). |

---

### 2.6 `fact_country_education` (Macroeconomic Fact Table)
- **Granularity:** One row per country per year per educational indicator.
- **Row Count:** 2,243 records.
- **Foreign Key:** `country_id` referencing `dim_country`.
- **Primary Source:** The World Bank Group (EdStats).

| Column Name | Data Type | Nullable | Sample Value | Description & Business Logic |
|---|---|---|---|---|
| `country_id` | VARCHAR(10) | NO | `C0001` | Foreign key link to `dim_country`. |
| `country_name` | VARCHAR(100)| NO | `United States` | Standardized sovereign country name. |
| `year` | INTEGER | NO | `2016` | Observation year (scoped to 2010–2023). |
| `indicator` | VARCHAR(255)| NO | `SE.XPD.TOTL.GD.ZS` | Educational or macroeconomic indicator code / description. |
| `value` | FLOAT | NO | `4.99` | Metric numeric value (e.g., % of GDP, enrollment percentage). |

---

### 2.7 `kpi_master` (Consolidated Analytical Master Table)
- **Granularity:** One row per institution (`university_id`).
- **Row Count:** 1,503 records.
- **Columns:** 16 pre-aggregated columns linking `dim_university`, `dim_country`, and all six core KPIs (`kpi_global_ranking_score`, `kpi_research_impact_score`, `kpi_faculty_student_ratio`, `kpi_international_student_pct`, `kpi_academic_reputation_score`, `kpi_research_productivity_index`) for immediate, responsive Tableau dashboard querying.

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**
