# EduVision Data Quality and Final Validation Report

This report summarizes final automated data quality checks, referential integrity, schema verification, and completeness statistics.

## 1. Automated Quality Check Matrix

| Check Description | Observed Value | Status |
|---|---|---|
| dim_country Duplicate country_id Count | `0` | **PASSED** |
| dim_university Duplicate university_id Count | `0` | **PASSED** |
| fact_university_performance Unmatched university_id Count | `0` | **PASSED** |
| fact_research Unmatched university_id Count | `0` | **PASSED** |
| fact_student Unmatched university_id Count | `0` | **PASSED** |
| fact_country_education Unmatched country_id Count | `0` | **PASSED** |
| fact_university_performance Invalid global_rank Out of Bounds | `0` | **PASSED** |
| fact_university_performance Invalid overall_score Out of Bounds (0-100) | `0` | **PASSED** |
| fact_student Invalid intl_student_pct Out of Bounds (0-100) | `0` | **PASSED** |

**Overall Validation Result**: ALL CHECKS PASSED

## 2. Table Summary & Row Counts

- `dim_country`: 258 rows x 5 cols
- `dim_university`: 3,402 rows x 5 cols
- `fact_university_performance`: 6,223 rows x 6 cols
- `fact_research`: 6,223 rows x 6 cols
- `fact_student`: 6,223 rows x 6 cols
- `fact_country_education`: 55,541 rows x 6 cols
- `eduvision_final_dataset`: 6,241 rows x 24 cols
- `kpi_summary`: 6,241 rows x 11 cols

## 3. KPI Completeness Summary (% Non-Null)

| KPI Name | Non-Null Count | Total Rows | Completeness % |
|---|---|---|---|
| `kpi1_global_ranking_score` | 4,971 | 6,241 | 79.65% |
| `kpi2_research_impact_score` | 4,971 | 6,241 | 79.65% |
| `kpi3_faculty_student_ratio` | 4,731 | 6,241 | 75.81% |
| `kpi4_international_student_pct` | 4,726 | 6,241 | 75.73% |
| `kpi5_academic_reputation_score` | 4,971 | 6,241 | 79.65% |
| `kpi6_research_productivity_index` | 4,971 | 6,241 | 79.65% |
