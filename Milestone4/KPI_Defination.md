# EduVision\_DV — KPI Definitions

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Document** | KPI Definitions & Calculation Reference |
| **Report Date** | 2026-09-30 |
| **Document Version** | v1.0 |

---

## 1. Overview

EduVision\_DV uses six Key Performance Indicators (KPIs) to evaluate university performance across four dimensions: ranking strength, research output, student characteristics, and internationalization.

| Dimension | KPIs |
|-----------|------|
| **Ranking** | Global Ranking Score |
| **Research** | Research Impact Score · Research Productivity Index |
| **Academic Reputation** | Academic Reputation Score |
| **Students & Faculty** | Faculty-to-Student Ratio · International Student Percentage |

Each KPI has a defined source, scale, normalization method, interpretation, and rule for handling missing values.

---

## 2. KPI Summary Reference

| # | KPI | Source Field(s) | Scale / Unit | Direction |
|---|-----|-----------------|-------------|-----------|
| 1 | Global Ranking Score | `global_rank` | 0 – 100 | Higher = Better |
| 2 | Research Impact Score | Citations per faculty / research impact indicator | 0 – 100 | Higher = Better |
| 3 | Faculty-to-Student Ratio | Student count / faculty count | Ratio | Context-dependent |
| 4 | International Student Percentage | International student enrollment field | % (0 – 100) | Higher = More international |
| 5 | Academic Reputation Score | QS Academic Reputation indicator | 0 – 100 | Higher = Better |
| 6 | Research Productivity Index | Normalized composite of research indicators | 0 – 100 | Higher = Better |

> **Missing Value Policy (All KPIs):** Missing source values are preserved as null. They are never substituted with zero. KPIs are computed only from available data.

---

## 3. KPI 1 — Global Ranking Score

### 3.1 Definition

The **Global Ranking Score** is a normalized score representing an institution's global ranking position on a 0–100 scale.

A higher score indicates a better (lower-numbered) global rank. The top-ranked institution receives a score of 100.

### 3.2 Source Fields

| Field | Description |
|-------|-------------|
| `global_rank` | Raw global ranking position (integer, 1 = best) |
| `normalized_rank` | Rank position after normalization |
| `global_ranking_score` | Final 0–100 score derived from rank position |

### 3.3 Normalization

The raw ranking position is converted to a 0–100 score using min-max normalization so that:

```
Rank 1 (best position)   →   Score = 100.00
Rank N (worst position)  →   Score → 0
```

The score decreases monotonically as rank number increases. In the validated dataset, the score decrements at approximately **−0.067 per rank step** from the top, confirming a consistent linear normalization formula.

### 3.4 Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 95 – 100 | Elite global institutions (Top tier) |
| 80 – 94 | High-performing universities |
| 50 – 79 | Mid-range global standing |
| Below 50 | Lower global ranking position |

### 3.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| University Overview | Primary ranking KPI card and ranking charts |
| Country Comparison | Regional Education Trends |

### 3.6 Missing Value Treatment

If `global_rank` is missing for an institution, `global_ranking_score` is recorded as null and excluded from ranking aggregations.

---

## 4. KPI 2 — Research Impact Score

### 4.1 Definition

The **Research Impact Score** measures the citation-based research influence of an institution, normalized to a 0–100 scale.

It captures how frequently an institution's research output is cited relative to peers, reflecting the quality and reach of its academic contributions.

### 4.2 Source Fields

| Field | Description |
|-------|-------------|
| `Citations_per_Faculty_Score` | QS citations per faculty score |
| `scores_citations` | THE citation impact score |
| `research_impact_score` | Derived normalized score in final dataset |

### 4.3 Normalization

The score is normalized to a 0–100 scale from the citation-based source indicators. Higher citation frequency per faculty relative to the dataset range produces a higher score.

```
High citation frequency relative to peers  →  Score closer to 100
Low citation frequency                     →  Score closer to 0
```

### 4.4 Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 80 – 100 | Very high research citation impact |
| 50 – 79 | Moderate to strong research impact |
| Below 50 | Lower citation-based research influence |

### 4.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| Research Analytics | Research Impact Score KPI card · Research Impact Comparison chart |

### 4.6 Missing Value Treatment

If citation source fields are null for an institution, `research_impact_score` is recorded as null and excluded from averages. The field is never imputed to zero.

---

## 5. KPI 3 — Faculty-to-Student Ratio

### 5.1 Definition

The **Faculty-to-Student Ratio** measures the number of students per academic staff member at an institution.

It is an indicator of teaching resource intensity and instructional capacity.

### 5.2 Source Fields

| Field | Description |
|-------|-------------|
| `Faculty_Student_Score` | QS faculty-to-student ratio score |
| `stats_student_staff_ratio` | THE student-to-staff ratio statistic |
| `faculty_to_student_ratio` | Derived ratio field in final dataset |

### 5.3 Calculation

```
Faculty-to-Student Ratio = Total Students / Total Academic Staff
```

A **lower ratio** generally indicates more teaching resources per student. A **higher ratio** indicates larger class sizes relative to staff.

> **Note:** This KPI is reported as a raw ratio, not normalized to 0–100.

### 5.4 Interpretation

| Ratio | Interpretation |
|-------|----------------|
| Below 10 | High staffing intensity — low student-to-staff ratio |
| 10 – 20 | Moderate staffing levels |
| Above 20 | High student load per staff member |

### 5.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| Student Analytics | Faculty-to-Student Ratio KPI card · Faculty-to-Student Ratio Analysis chart |

### 5.6 Missing Value Treatment

If student count or staff count is missing, the ratio is recorded as null. No synthetic ratio values are calculated from partial data.

---

## 6. KPI 4 — International Student Percentage

### 6.1 Definition

The **International Student Percentage** represents the proportion of an institution's enrolled student body that consists of international (non-domestic) students.

It is a direct measure of institutional internationalization and global student attraction.

### 6.2 Source Fields

| Field | Description |
|-------|-------------|
| `International_Students_Score` | QS international students indicator |
| `stats_pc_intl_students` | THE percentage of international students |
| `international_student_percentage` | Derived percentage field in final dataset |

### 6.3 Calculation

```
International Student Percentage = (International Students / Total Students) × 100
```

Values are expressed as a percentage between 0 and 100. No value should exceed 100%.

### 6.4 Interpretation

| Percentage | Interpretation |
|------------|----------------|
| Above 30% | Highly international student body |
| 15 – 30% | Moderately international |
| Below 15% | Predominantly domestic student population |

### 6.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| Student Analytics | International Student Percentage KPI card · International Student Analysis chart |

### 6.6 Missing Value Treatment

If the source international student field is null, the percentage is recorded as null and excluded from aggregations.

---

## 7. KPI 5 — Academic Reputation Score

### 7.1 Definition

The **Academic Reputation Score** reflects the perceived academic prestige of an institution as measured by the QS Academic Reputation survey — one of the largest surveys of academic opinion globally.

The score aggregates views from academics worldwide on the quality of research and teaching at each institution.

### 7.2 Source Fields

| Field | Description |
|-------|-------------|
| `Academic_Reputation_Score` | QS Academic Reputation survey score (0–100) |
| `academic_reputation_score` | Field name in final consolidated dataset |

### 7.3 Scale

This KPI is used directly from the QS source without further transformation. Values are already expressed on a 0–100 scale.

```
Score = 100  →  Maximum academic reputation (top globally recognized institutions)
Score = 0    →  Lowest observed academic reputation in the dataset
```

### 7.4 Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 90 – 100 | World-leading academic reputation |
| 70 – 89 | Highly reputable institution |
| 40 – 69 | Regionally or nationally recognized |
| Below 40 | Limited global academic recognition |

### 7.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| University Overview | Academic Reputation Score KPI card · Academic Reputation Analysis chart |

### 7.6 Missing Value Treatment

If the QS Academic Reputation field is null (institution not included in QS survey), the score is recorded as null.

---

## 8. KPI 6 — Research Productivity Index

### 8.1 Definition

The **Research Productivity Index** is a normalized composite score (0–100) that measures the overall research output and productivity of an institution.

Unlike the Research Impact Score (which focuses on citation influence), the Research Productivity Index reflects the breadth and volume of research activity across multiple research performance indicators.

### 8.2 Source Fields

The index is computed from a combination of available normalized research performance indicators, including:

| Indicator | Source Dataset |
|-----------|---------------|
| Research environment / output score | THE (`scores_research`) |
| Research performance score | World University Rankings 2023 |
| Overall research-related sub-scores | QS research indicators |

### 8.3 Calculation

```
Research Productivity Index = Normalized composite of available research indicators
                              (computed only from non-null indicator values)
```

The index is calculated from whichever research indicators are available for a given institution. If some indicators are missing, the index is computed from the remaining available indicators. If all indicators are missing, the index is null.

> **Important:** The index is never calculated by treating missing indicators as zero. Partial availability is handled gracefully.

### 8.4 Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 80 – 100 | Very high research productivity |
| 50 – 79 | Moderate to strong research output |
| Below 50 | Lower research productivity relative to dataset |

### 8.5 Dashboard Usage

| Dashboard | Usage |
|-----------|-------|
| Research Analytics | Research Productivity Index KPI card · Research Productivity Trends chart |

### 8.6 Missing Value Treatment

Missing source indicators are excluded from the composite calculation. The index is null only when all contributing source fields are null for an institution.

---

## 9. KPI Cross-Reference by Dashboard

| KPI | University Overview | Research Analytics | Student Analytics | Country Comparison |
|-----|:------------------:|:-----------------:|:----------------:|:-----------------:|
| Global Ranking Score | ✅ | | | ✅ |
| Research Impact Score | | ✅ | | |
| Faculty-to-Student Ratio | | | ✅ | |
| International Student Percentage | | | ✅ | |
| Academic Reputation Score | ✅ | | | |
| Research Productivity Index | | ✅ | | |

---

## 10. Missing Value Policy Summary

| KPI | If Source is Null |
|-----|------------------|
| Global Ranking Score | Recorded as null — excluded from ranking aggregations |
| Research Impact Score | Recorded as null — excluded from citation averages |
| Faculty-to-Student Ratio | Recorded as null — ratio not calculated from partial data |
| International Student Percentage | Recorded as null — excluded from percentage aggregations |
| Academic Reputation Score | Recorded as null — institution not included in QS survey |
| Research Productivity Index | Null only if all contributing research indicators are null |

> **Global Policy:** No KPI field uses zero-substitution for missing values. This ensures that institutions with missing data are not artificially penalized or inflated in comparisons.

---

*EduVision\_DV — Milestone 4 · KPI Definitions Document · Report Date: 2026-09-30*
