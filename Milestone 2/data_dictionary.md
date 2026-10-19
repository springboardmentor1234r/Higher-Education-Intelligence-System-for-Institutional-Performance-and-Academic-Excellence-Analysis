# EduVision Master Data Dictionary

This data dictionary describes all attributes in `eduvision_final_dataset.csv`, `dim_country`, `dim_university`, and fact tables.

---

## 1. `dim_country`

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| `country_id` | STRING | Primary Key (`CTY_xxx`) | `CTY_001` |
| `country_name` | STRING | Canonical country name | `United States` |
| `country_code` | STRING | ISO 3-letter code | `USA` |
| `region` | STRING | World Bank macro region | `North America` |
| `income_group` | STRING | World Bank income group | `High income: OECD` |

---

## 2. `dim_university`

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| `university_id` | STRING | Primary Key (`UNI_xxxx`) | `UNI_0001` |
| `university_name` | STRING | Canonical university name | `Massachusetts Institute of Technology (MIT)` |
| `country_id` | STRING | Foreign Key to `dim_country` | `CTY_243` |
| `country_name` | STRING | Country name | `United States` |
| `region` | STRING | Macro region | `North America` |

---

## 3. `eduvision_final_dataset` & Fact Tables

| Field Name | Data Type | Source Table | Description |
|---|---|---|---|
| `university_id` | STRING | `dim_university` | Unique university surrogate key |
| `university_name` | STRING | `dim_university` | Canonical university display name |
| `country_id` | STRING | `dim_country` | Unique country surrogate key |
| `country_name` | STRING | `dim_country` | Canonical country display name |
| `region` | STRING | `dim_country` | Macro-region classification |
| `year` | INTEGER | Fact Tables | Ranking year (2023, 2024, 2025) |
| `global_rank` | FLOAT | `fact_university_performance` | Global ranking position |
| `overall_score` | FLOAT | `fact_university_performance` | Publisher overall score (0-100) |
| `academic_reputation` | FLOAT | `fact_university_performance` | Academic reputation / teaching score |
| `employer_reputation` | FLOAT | `fact_university_performance` | Employer reputation / industry income score |
| `citation_score` | FLOAT | `fact_research` | Citations per faculty / citation score |
| `research_score` | FLOAT | `fact_research` | Research quality score |
| `research_productivity` | FLOAT | `fact_research` | Composite research productivity score |
| `total_students` | FLOAT | `fact_student` | Total student headcount |
| `students_per_staff` | FLOAT | `fact_student` | Student to faculty ratio |
| `international_students` | FLOAT | `fact_student` | International student headcount |
| `international_student_percentage` | FLOAT | `fact_student` | Percentage of international students (%) |
| `kpi1_global_ranking_score` | FLOAT | KPI Calculated | KPI 1: Global Ranking Score (0-100) |
| `kpi2_research_impact_score` | FLOAT | KPI Calculated | KPI 2: Research Impact Score (0-100) |
| `kpi3_faculty_student_ratio` | FLOAT | KPI Calculated | KPI 3: Faculty-to-Student Ratio |
| `kpi4_international_student_pct` | FLOAT | KPI Calculated | KPI 4: International Student % (0-100) |
| `kpi5_academic_reputation_score` | FLOAT | KPI Calculated | KPI 5: Academic Reputation Score (0-100) |
| `kpi6_research_productivity_index` | FLOAT | KPI Calculated | KPI 6: Research Productivity Index (0-100) |
