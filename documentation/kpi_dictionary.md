# EduVision_DV – Master KPI Specification Dictionary

## Overview

This document establishes the official technical specifications for the **six core project KPIs**. All KPI definitions, formulas, and data types are derived strictly from the actual fields available in the finalized data models (`../../data/final/`).

--- 

## KPI Classification & Availability Summary Table

Per analytical rigor rules, metrics are distinguished between **DIRECT** (raw field directly represents the target metric), **DERIVED** (engineered from underlying raw metrics), and **NOT DIRECTLY AVAILABLE** (proxy required):


| KPI # | KPI Name | Availability Status | Primary Source Field | Unit | Classification Rule |
| --- | --- | --- | --- | --- | --- |
| 1 | **Global Ranking Score** | **DIRECT / DERIVED** | `overall_score` (QS / THE) | Index Score (0–100) | Direct score in single-source; derived mean in cross-dataset. |
| 2 | **Research Impact Score** | **DIRECT / DERIVED** | `citations_per_faculty_score` / `citations_score` | Index Score (0–100) | Direct citation score in single-source; derived mean in cross-dataset. |
| 3 | **Faculty-to-Student Ratio** | **DIRECT (THE) / DERIVED** | `students_per_staff` (THE) / `faculty_student_score` (QS) | Faculty / 100 Students (THE) / Score (QS) | Direct actual ratio in THE (`100 / students_per_staff`); QS provides score proxy. |
| 4 | **International Student Percentage** | **DIRECT (THE) / DERIVED** | `pct_international_students` (THE) / `international_students_score` (QS) | Percentage (%) (THE) / Score (QS) | Direct actual percentage in THE (e.g. `42%`); QS provides score proxy. |
| 5 | **Academic Reputation Score** | **DIRECT (QS) / DERIVED** | `academic_reputation_score` (QS) / `teaching_score` (THE) | Index Score (0–100) | Direct survey score in QS; proxy teaching environment score in THE. |
| 6 | **Research Productivity Index** | **DERIVED** | `international_research_network_score` + `research_score` | Composite Index (0–100) | Derived composite index combining research volume & international network breadth. |

---

## Detailed Specifications for Every KPI

### KPI 1: Global Ranking Score

- **Availability Status**: `DIRECT / DERIVED`
- **Definition**: Quantitative overall institutional benchmark score representing global academic standing and performance.
- **Source Dataset**: QS World University Rankings 2025 / THE World University Rankings 2023
- **Source Field(s)**: `overall_score (QS 2025), overall_score (THE 2023)`
- **Formula**: `Single Source: overall_score. Composite: mean(qs_overall_score, the_overall_score).`
- **Unit**: Index Score (0–100 scale)
- **Normalization Method**: Pre-normalized by ranking bodies (0–100 scale based on weighted indicator components).
- **Missing-Value Treatment**: Preserve NaN. Unranked / unassigned institutions remain null; no zero-imputation.
- **Interpretation**: Higher score signifies superior overall global institutional standing and excellence.
- **Limitations**: QS and THE use distinct weighting methodologies (QS weights employer reputation; THE weights research environment).

### KPI 2: Research Impact Score

- **Availability Status**: `DIRECT / DERIVED`
- **Definition**: Measure of scholarly citation volume and research influence per faculty member.
- **Source Dataset**: QS World University Rankings 2025 / THE World University Rankings 2023
- **Source Field(s)**: `citations_per_faculty_score (QS 2025), citations_score (THE 2023)`
- **Formula**: `Single Source: citations_per_faculty_score (QS) or citations_score (THE). Composite: mean(qs_citations_score, the_citations_score).`
- **Unit**: Index Score (0–100 scale)
- **Normalization Method**: Pre-normalized by ranking bodies using field-adjusted citation impact scaling.
- **Missing-Value Treatment**: Preserve NaN; do not impute with zero.
- **Interpretation**: Higher score indicates greater global academic research influence and citation density per staff.
- **Limitations**: Measures normalized citation impact per paper/faculty, not absolute institutional citation volume.

### KPI 3: Faculty-to-Student Ratio

- **Availability Status**: `DIRECT (THE) / DERIVED`
- **Definition**: Number of academic staff members relative to enrolled students, indicating teaching capacity and individualized attention.
- **Source Dataset**: THE World University Rankings 2023 (Actual Ratio) / QS World University Rankings 2025 (Benchmark Score)
- **Source Field(s)**: `students_per_staff (THE 2023), faculty_student_score (QS 2025)`
- **Formula**: `Actual Ratio (per 100 students) = 100 / students_per_staff. QS Benchmark Score = faculty_student_score.`
- **Unit**: Faculty per 100 Students (Actual Ratio) / Index Score (0–100 for QS)
- **Normalization Method**: Mathematical inversion (100 / students_per_staff) for actual ratio; none needed for QS score.
- **Missing-Value Treatment**: Preserve NaN; do not impute.
- **Interpretation**: Higher ratio value (Faculty per 100 students) indicates smaller student-to-faculty ratios and higher teaching support capacity.
- **Limitations**: THE provides actual headcount ratio (Students:Staff); QS provides a relative 0–100 benchmark score. Score must not be confused with actual ratio.

### KPI 4: International Student Percentage

- **Availability Status**: `DIRECT (THE) / DERIVED`
- **Definition**: Proportion of total student enrollment comprised of international (foreign national) students.
- **Source Dataset**: THE World University Rankings 2023 (Actual %) / QS World University Rankings 2025 (Score)
- **Source Field(s)**: `pct_international_students (THE 2023), international_students_score (QS 2025)`
- **Formula**: `Actual Percentage = pct_international_students (THE). QS Benchmark Score = international_students_score.`
- **Unit**: Percentage (%) for actual metric / Index Score (0–100) for QS score
- **Normalization Method**: Direct numeric percentage (%) for THE; 0–100 normalized score for QS.
- **Missing-Value Treatment**: Preserve NaN; do not fill missing values with 0%.
- **Interpretation**: Higher percentage reflects a highly globalized campus student body and strong international attraction.
- **Limitations**: QS publishes a relative 0–100 benchmark score, NOT the raw percentage of international students.

### KPI 5: Academic Reputation Score

- **Availability Status**: `DIRECT (QS) / DERIVED (THE)`
- **Definition**: Academic peer perception of institutional research quality and academic excellence.
- **Source Dataset**: QS World University Rankings 2025 / THE World University Rankings 2023
- **Source Field(s)**: `academic_reputation_score (QS 2025), teaching_score (THE 2023 proxy)`
- **Formula**: `Direct Score: academic_reputation_score (QS). Proxy Score: teaching_score (THE).`
- **Unit**: Index Score (0–100 scale)
- **Normalization Method**: Standardized 0–100 survey score based on international academic peer survey returns.
- **Missing-Value Treatment**: Preserve NaN; do not impute.
- **Interpretation**: Higher score indicates stronger global recognition and peer prestige among academic scholars.
- **Limitations**: Subject to academic survey sample distribution and brand familiarity.

### KPI 6: Research Productivity Index

- **Availability Status**: `DERIVED`
- **Definition**: Synthetic index measuring global research collaboration breadth and institutional research output volume.
- **Source Dataset**: QS World University Rankings 2025 / THE World University Rankings 2023
- **Source Field(s)**: `international_research_network_score (QS 2025), research_score (THE 2023)`
- **Formula**: `Research Productivity Index = mean(international_research_network_score, research_score).`
- **Unit**: Composite Index Score (0–100 scale)
- **Normalization Method**: Arithmetic mean of pre-normalized 0–100 research volume and international collaboration scores.
- **Missing-Value Treatment**: Preserve NaN if neither component score is available.
- **Interpretation**: Higher index reflects broader international research networks and stronger institutional research productivity.
- **Limitations**: Raw publication counts per faculty are NOT directly available in raw files; this derived index relies on normalized indicator proxies.
