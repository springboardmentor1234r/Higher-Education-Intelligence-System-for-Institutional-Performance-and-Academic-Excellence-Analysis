# EduVision KPI Definitions, Formulas & Normalization Logic

This document defines the six core Key Performance Indicators (KPIs) engineered for the EduVision Higher Education Intelligence System.

---

## 1. Global Ranking Score (`kpi1_global_ranking_score`)
- **Description**: Quantifies the overall institutional standing of a university on a normalized 0-100 scale.
- **Source Columns**: `Overall_Score` (QS 2025), `scores_overall` (THE 2024), `OverAll Score` (WUR 2023).
- **Formula**:
  $$\text{Global Ranking Score} = \begin{cases} \text{overall\_score} & \text{if overall\_score is not null} \\ \max\left(10, 100 - (\text{global\_rank} - 1) \times 0.05\right) & \text{otherwise} \end{cases}$$
- **Unit**: Score (0-100 scale).
- **Missing Value Treatment**: Calculated from rank if overall score is missing; NaN if both rank and score are absent.
- **Interpretation**: Higher score indicates superior overall global standing and performance.

---

## 2. Research Impact Score (`kpi2_research_impact_score`)
- **Description**: Measures the influence, reach, and citation intensity of an institution's scholarly output per faculty member.
- **Source Columns**: `Citations_per_Faculty_Score` (QS 2025), `scores_citations` (THE 2024), `Citations Score` (WUR 2023).
- **Formula**:
  $$\text{Research Impact Score} = \text{citation\_score}$$
- **Unit**: Score (0-100 scale).
- **Missing Value Treatment**: Preserved as NaN if unavailable.
- **Interpretation**: Higher score reflects greater academic citation volume and international research influence.

---

## 3. Faculty-to-Student Ratio (`kpi3_faculty_student_ratio`)
- **Description**: Represents institutional teaching capacity and individual student attention, measured as student headcount per staff member.
- **Source Columns**: `stats_student_staff_ratio` (THE 2024), `No of student per staff` (WUR 2023).
- **Formula**:
  $$\text{Faculty-to-Student Ratio} = \text{students\_per\_staff}$$
- **Unit**: Ratio (Number of Students per 1 Staff Member).
- **Missing Value Treatment**: NaN for QS 2025 (as QS publishes a faculty/student score index rather than raw ratio).
- **Interpretation**: Lower ratio indicates fewer students per faculty member (higher institutional teaching focus).

---

## 4. International Student Percentage (`kpi4_international_student_pct`)
- **Description**: Measures student body diversity and global attractiveness.
- **Source Columns**: `stats_pc_intl_students` (THE 2024), `International Student` (WUR 2023).
- **Formula**:
  $$\text{International Student Percentage} = \text{intl\_student\_pct}$$
- **Unit**: Percentage (`%`).
- **Missing Value Treatment**: NaN for QS 2025 (QS provides international student score index, not raw percentage).
- **Interpretation**: Higher percentage indicates a more globally diverse student population.

---

## 5. Academic Reputation Score (`kpi5_academic_reputation_score`)
- **Description**: Gauges global peer perception of academic excellence and teaching quality.
- **Source Columns**: `Academic_Reputation_Score` (QS 2025), `scores_teaching` (THE 2024), `Teaching Score` (WUR 2023).
- **Formula**:
  $$\text{Academic Reputation Score} = \text{academic\_reputation}$$
- **Unit**: Score (0-100 scale).
- **Missing Value Treatment**: Preserved as NaN.
- **Interpretation**: Reflects global survey reputation among academics and scholarly peers.

---

## 6. Research Productivity Index (`kpi6_research_productivity_index`)
- **Description**: Derived composite metric reflecting combined research quality, citation density, and scholarly output.
- **Source Columns**: Combination of `research_score` and `citation_score`.
- **Formula**:
  $$\text{Research Productivity Index} = 0.50 \times \text{research\_score} + 0.50 \times \text{citation\_score}$$
  *(Excludes Sustainability Score per explicit brief rules)*
- **Unit**: Composite Score (0-100 scale).
- **Missing Value Treatment**: Evaluated on available component score if one is absent; NaN if both absent.
- **Interpretation**: Comprehensive evaluation of research volume and scientific influence.
