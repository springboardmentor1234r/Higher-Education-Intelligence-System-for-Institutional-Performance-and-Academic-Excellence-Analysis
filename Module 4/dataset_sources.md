# EduVision_DV: Dataset Sources & Provenance

This document details the provenance, scope, licensing, and schema characteristics of the four primary data sources integrated into the EduVision_DV Higher Education Performance Dashboard.

---

## 1. QS World University Rankings 2025
- **Source:** Quacquarelli Symonds (QS) / Kaggle
- **Coverage:** 1,503 world-class institutions across 106 educational systems/countries
- **Temporal Granularity:** Year 2025
- **Primary Use:** University Overview Dashboard, Institutional Master Dimension (`dim_university`), Global Ranking KPIs
- **Key Columns Utilized:**
  - `RANK_2025`: Official global institutional ranking
  - `Institution_Name`: Official university name
  - `Location` & `Region`: National sovereignty and continental geographic grouping
  - `Academic_Reputation_Score`: Global survey of academics (0–100)
  - `Employer_Reputation_Score`: Global survey of corporate graduate recruiters (0–100)
  - `Faculty_Student_Score`: Academic staffing capacity index (0–100)
  - `Citations_per_Faculty_Score`: Citations per faculty member benchmark (0–100)
  - `International_Faculty_Score` & `International_Students_Score`: Institutional internationalization indices (0–100)
  - `International_Research_Network_Score`: Cross-border collaborative co-authorship index (0–100)
  - `Overall_Score`: Aggregate institutional composite score (0–100)

---

## 2. Times Higher Education (THE) World University Rankings 2024
- **Source:** Times Higher Education / Kaggle
- **Coverage:** 2,673 universities globally
- **Temporal Granularity:** Year 2024
- **Primary Use:** Research Analytics Dashboard (`fact_research`), Research Productivity Index engineering
- **Key Columns Utilized:**
  - `scores_research`: Institutional research environment and reputation (0–100)
  - `scores_citations`: Normalized research citation impact (0–100)
  - `scores_teaching`: Teaching environment and student-staff indicators (0–100)
  - `scores_international_outlook`: Cross-border student, staff, and publication share (0–100)
  - `scores_industry_income`: Commercialization and industry research grant funding (0–100)

---

## 3. World University Rankings (WUR) 2023
- **Source:** Times Higher Education 2023 Edition / Kaggle
- **Coverage:** 2,341 universities
- **Temporal Granularity:** Year 2023
- **Primary Use:** Student Analytics Dashboard (`fact_student`), Demographic & Faculty capacity analysis
- **Key Columns Utilized:**
  - `No of student`: Full-time equivalent (FTE) student headcount
  - `No of student per staff`: True numeric ratio of students per academic staff member
  - `International Student`: Actual percentage of international students (%)
  - `Female:Male Ratio`: Institutional gender demographic distribution

---

## 4. World Bank Education Statistics (EdStats)
- **Source:** The World Bank Group / Kaggle
- **Coverage:** 242 countries and territories over historical and modern horizons
- **Temporal Granularity:** Filtered to 2010–2023 for contemporary policy alignment
- **Primary Use:** Country Comparison Dashboard (`fact_country_education`), Macro-level education economics
- **Selected Key Indicators:**
  - `SE.XPD.TOTL.GD.ZS`: Government expenditure on education (% of GDP)
  - `SE.TER.ENRR`: Gross enrolment ratio, tertiary (both sexes) (%)
  - `SE.TER.ENRR.FE` & `SE.TER.ENRR.MA`: Gross tertiary enrolment by gender (%)
  - `SE.ADT.LITR.ZS`: Adult literacy rate (% aged 15 and older)
  - `SE.TER.TCHR.RS`: Pupil-teacher ratio in tertiary education
