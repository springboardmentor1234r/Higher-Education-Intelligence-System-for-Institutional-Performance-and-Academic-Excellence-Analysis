# EduVision_DV Data Dictionary

## Final Dataset

File:

`data/final/university_kpi_dataset.csv`

Number of universities:

822

---

## University Identification

| Field | Description |
|---|---|
| University_ID | Unique identifier assigned to each matched university |
| University_Name | Standard university name |
| Match_Key | Normalized matching key |
| Match_Method | Method used to establish the university match |
| Country_Standard | Standardized country name |

---

## Source Data

### QS World University Rankings 2025

| Field | Description |
|---|---|
| QS_RANK_2025 | QS 2025 ranking |
| QS_RANK_2024 | QS 2024 ranking |
| QS_Academic_Reputation_Score | Academic reputation indicator |
| QS_Faculty_Student_Score | Faculty/student indicator |
| QS_International_Students_Score | International student indicator |

### Times Higher Education 2024

| Field | Description |
|---|---|
| THE_Rank | THE 2024 ranking |
| THE_Student_Population | Student population |
| THE_Students_to_Staff_Ratio | Students-to-staff ratio |
| THE_International_Students | International student percentage |
| THE_Overall_Score | Overall THE score |
| THE_Teaching | Teaching indicator |
| THE_Research_Environment | Research environment indicator |
| THE_Research_Quality | Research quality indicator |
| THE_Industry_Impact | Industry impact indicator |
| THE_International_Outlook | International outlook indicator |

### World University Ranking 2023

| Field | Description |
|---|---|
| WUR_No_of_student | Number of students |
| WUR_No_of_student_per_staff | Students per staff |
| WUR_International_Student | International student percentage |
| WUR_Female_Male_Ratio | Female-to-male ratio |
| WUR_OverAll_Score | Overall WUR score |
| WUR_Teaching_Score | Teaching score |
| WUR_Research_Score | Research score |
| WUR_Citations_Score | Citation score |
| WUR_Industry_Income_Score | Industry income score |
| WUR_International_Outlook_Score | International outlook score |

---

# KPI Definitions

## 1. Global Ranking Score

Derived from QS 2025 ranking.

Higher score indicates a stronger position within the matched dataset.

Ranking bands such as `661-670` are represented using their midpoint before normalization.

---

## 2. Research Impact Score

Calculated as the mean of available:

- THE Research Quality
- WUR Citations Score

Only available components are included.

---

## 3. Faculty-to-Student Ratio

Uses:

1. THE Students-to-Staff Ratio
2. WUR Students-per-Staff as fallback

---

## 4. International Student Percentage

Uses:

1. THE International Students percentage
2. WUR International Student percentage as fallback

---

## 5. Academic Reputation Score

Directly derived from:

`QS_Academic_Reputation_Score`

---

## 6. Research Productivity Index

Calculated as the mean of available:

- THE Research Environment
- WUR Research Score

Only available components are included.

---

# Data Quality

Total matched universities:

**822**

QS coverage:

**822 / 822**

THE coverage:

**822 / 822**

WUR coverage:

**815 / 822**

Final KPI completeness:

**100%**

Duplicate University IDs:

**0**

Invalid KPI values detected:

**0**

---

# Important Data Handling Rules

- Raw datasets are never modified.
- Missing source values are preserved.
- Missing values are not replaced with artificial zeroes.
- WUR data is unavailable for seven matched universities.
- Those universities remain in the master dataset.
- KPI calculations use available source components.
- Source-specific fields are retained for traceability.