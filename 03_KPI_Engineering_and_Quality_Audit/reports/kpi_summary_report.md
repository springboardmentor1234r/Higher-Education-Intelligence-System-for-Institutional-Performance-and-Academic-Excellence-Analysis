# EduVision_DV – KPI Engineering & Final Analytics Summary Report

## Executive Summary

Following user approval of the cross-dataset matching crosswalk, the final analytical data models and the **six core project KPIs** were engineered. All outputs are exported to `data/final/` and are fully prepared for direct import into Tableau.

--- 

## The Six Core Project KPIs

| KPI # & Name | Standardized Column | Mathematical & Methodological Formula | Target Tableau Dashboard |
| --- | --- | --- | --- |
| **KPI 1: Global Ranking Score** | `kpi_1_global_ranking_score` | Composite 0–100 overall score synthesizing QS 2025 and THE 2023 benchmark overall scores. | University Overview, Country Comparison |
| **KPI 2: Research Impact Score** | `kpi_2_research_impact_score` | Composite 0–100 citation influence score combining QS Citations per Faculty Score and THE Citations Score. | Research Analytics |
| **KPI 3: Faculty-to-Student Ratio** | `kpi_3_faculty_per_100_students` / `kpi_3_faculty_student_score` | Actual ratio of faculty per 100 students (derived from THE `student_staff_ratio`) alongside QS benchmark proxy score. | Student Analytics |
| **KPI 4: International Student Percentage** | `kpi_4_intl_student_pct` / `kpi_4_intl_student_score` | Actual percentage of international students enrolled (%) from THE alongside QS benchmark proxy score. | Student Analytics, Country Comparison |
| **KPI 5: Academic Reputation Score** | `kpi_5_academic_reputation_score` | 0–100 academic peer reputation survey score from QS 2025 (supplemented by THE teaching environment score). | University Overview, Research Analytics |
| **KPI 6: Research Productivity Index** | `kpi_6_research_productivity_index` | Composite 0–100 index combining QS International Research Network diversity score and THE Research volume score. | Research Analytics |

---

## Statistical Summary of Engineered KPIs

| KPI Column | Valid Count | Mean | Std Dev | Min | 25% | Median (50%) | 75% | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kpi_1_global_ranking_score` | 2,160 | 34.29 | 15.81 | 14.35 | 21.35 | 31.85 | 42.44 | 97.10 |
| `kpi_2_research_impact_score` | 2,496 | 37.65 | 27.79 | 1.00 | 13.30 | 32.70 | 58.42 | 100.00 |
| `kpi_3_faculty_per_100_students` | 2,533 | 7.18 | 8.19 | 0.43 | 4.50 | 6.02 | 7.87 | 250.00 |
| `kpi_4_intl_student_pct` | 2,531 | 10.04 | 13.21 | 0.00 | 1.00 | 5.00 | 14.00 | 100.00 |
| `kpi_5_academic_reputation_score` | 2,496 | 22.01 | 18.72 | 1.30 | 9.07 | 17.40 | 26.80 | 100.00 |
| `kpi_6_research_productivity_index` | 2,495 | 32.11 | 23.15 | 1.00 | 12.70 | 24.45 | 47.88 | 99.85 |

---

## Final Analytical Schemas in `data/final/`

1. **`dim_country.csv`** (130 records)

   - `country_id`, `country_name`, `region`


2. **`dim_university.csv`** (2,992 records)

   - `university_id`, `university_name`, `country_id`, `country_name`, `region`


3. **`university_crosswalk.csv`** (3,060 records)

   - `university_id`, `qs_name`, `the_name`, `wur_name`, `country_id`, `match_method`, `match_status`, `confidence`, `notes`


4. **`fact_university_rankings.csv`** (3,060 records)

   - Consolidated institutional rankings and 6 engineered KPIs.


5. **`fact_country_education.csv`** (130 records)

   - Macro-level country aggregates combining national higher education volume, average scores, and World Bank indicators.
