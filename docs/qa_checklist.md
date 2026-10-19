# Quality Assurance (QA) Checklist & Definition of Done

This document provides the formal QA checklist verifying that the **EduVision Higher Education Intelligence System** meets all technical, data engineering, and dashboard requirements outlined in `project_brief.md`.

---

## 1. Definition of Done Checklist

| Item # | Verification Task | Standard / Rule | Observed Value / Finding | Status |
|---|---|---|---|---|
| **QA-01** | Primary Key Uniqueness (`dim_country`) | `country_id` must be unique (0 duplicates) | 0 duplicate IDs across 258 rows | **PASSED** |
| **QA-02** | Primary Key Uniqueness (`dim_university`) | `university_id` must be unique (0 duplicates) | 0 duplicate IDs across 3,402 rows | **PASSED** |
| **QA-03** | Referential Integrity (`fact_university_performance`) | 100% of `university_id` keys exist in `dim_university` | 0 unmatched keys across 6,223 rows | **PASSED** |
| **QA-04** | Referential Integrity (`fact_research`) | 100% of `university_id` keys exist in `dim_university` | 0 unmatched keys across 6,223 rows | **PASSED** |
| **QA-05** | Referential Integrity (`fact_student`) | 100% of `university_id` keys exist in `dim_university` | 0 unmatched keys across 6,223 rows | **PASSED** |
| **QA-06** | Referential Integrity (`fact_country_education`) | 100% of `country_id` keys exist in `dim_country` | 0 unmatched keys across 55,541 rows | **PASSED** |
| **QA-07** | Numeric Coercion & Data Typing | All numeric fields converted via `pd.to_numeric(..., errors='coerce')` | No string corruption in numeric fields | **PASSED** |
| **QA-08** | Out-of-Bounds Check (`global_rank`) | `global_rank` must be > 0 and within valid bounds | 0 invalid rank values | **PASSED** |
| **QA-09** | Out-of-Bounds Check (`overall_score`) | `overall_score` must be between 0.0 and 100.0 | 0 out-of-bounds score values | **PASSED** |
| **QA-10** | Out-of-Bounds Check (`intl_student_pct`) | `international_student_percentage` must be between 0 and 100 | 0 out-of-bounds percentage values | **PASSED** |
| **QA-11** | Zero-Filling Prevention Rule | Missing values must remain `NaN`/`NULL`, never zero-filled | Missing values preserved and documented | **PASSED** |
| **QA-12** | KPI Engineering | All 6 KPIs calculated according to documented formulas | KPI 1–6 present in `final/` dataset | **PASSED** |
| **QA-13** | Dashboard Interlinking | Selection on landing dashboard carries active filters across views | Verified in `.twbx` XML & Web app | **PASSED** |
| **QA-14** | Deliverables Organization | Clean directory layout (`data/`, `notebooks_or_scripts/`, `dashboard/`, `docs/`) | Scratch/temp files purged | **PASSED** |
| **QA-15** | File Size & Git Exclusion | Raw datasets > 100MB (`EdStatsData.csv`) excluded via `.gitignore` | `.gitignore` rules active | **PASSED** |

---

## 2. Table Summary & Record Counts

| Table Name | File Location | Row Count | Column Count | Primary Key |
|---|---|---|---|---|
| `dim_country` | `data/cleaned/dim_country.csv` | 258 | 5 | `country_id` |
| `dim_university` | `data/cleaned/dim_university.csv` | 3,402 | 5 | `university_id` |
| `fact_university_performance` | `data/cleaned/fact_university_performance.csv` | 6,223 | 6 | (`university_id`, `year`) |
| `fact_research` | `data/cleaned/fact_research.csv` | 6,223 | 6 | (`university_id`, `year`) |
| `fact_student` | `data/cleaned/fact_student.csv` | 6,223 | 6 | (`university_id`, `year`) |
| `fact_country_education` | `data/cleaned/fact_country_education.csv` | 55,541 | 6 | (`country_id`, `year`, `indicator_code`) |
| `eduvision_final_dataset` | `data/final/eduvision_final_dataset.csv` | 6,241 | 24 | (`university_id`, `year`) |
| `kpi_summary` | `data/final/kpi_summary.csv` | 6,241 | 11 | (`university_id`, `year`) |

---

## 3. KPI Completeness Audit

| KPI Code | KPI Description | Non-Null Rows | Total Rows | Completeness % |
|---|---|---|---|---|
| `kpi1_global_ranking_score` | Global Ranking Score | 4,971 | 6,241 | 79.65% |
| `kpi2_research_impact_score` | Research Impact Score | 4,971 | 6,241 | 79.65% |
| `kpi3_faculty_student_ratio` | Faculty-to-Student Ratio | 4,731 | 6,241 | 75.81% |
| `kpi4_international_student_pct` | International Student Percentage | 4,726 | 6,241 | 75.73% |
| `kpi5_academic_reputation_score` | Academic Reputation Score | 4,971 | 6,241 | 79.65% |
| `kpi6_research_productivity_index` | Research Productivity Index | 4,971 | 6,241 | 79.65% |

---

## 4. Final Sign-off

- **Data Engineering Lead**: Sonia Vinod
- **Validation Run Status**: 100% Passed
- **Sign-off Date**: September 27, 2026
