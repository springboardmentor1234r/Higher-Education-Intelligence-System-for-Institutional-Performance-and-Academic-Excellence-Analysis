# EduVision_DV: Dataset Sources, Provenance & Licensing

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Higher Education Data Analytics  
**Date:** September 2026  

---

## 1. Overview of Data Architecture

The **EduVision_DV** higher education intelligence suite integrates four distinct, authoritative open datasets. Rather than forcing all data into an unnormalized single flat file, each dataset was selected to address a specific analytical layer:
1. **QS 2025:** Institutional global ranking, overall academic prestige, and employer surveys.
2. **THE 2024:** Research environment, normalized citation impact, and cross-border research networks.
3. **WUR 2023:** Student demographic profiles, empirical student-to-staff ratios, and gender breakdowns.
4. **World Bank EdStats:** Country-level macroeconomic educational investment and tertiary enrollment.

---

## 2. Detailed Dataset Profiles

### 2.1 Dataset 1: QS World University Rankings 2025
- **Publisher / Authority:** Quacquarelli Symonds (QS)
- **Distribution Platform:** Kaggle (`qs_world_rankings_2025.csv`)
- **Temporal Horizon:** Assessment Year 2025 (Published June 2024)
- **Coverage:** 1,503 universities across 106 countries and territories
- **Role in Project:** Primary institutional dimension (`dim_university`), institutional performance fact table (`fact_university_performance`), and master spine for surrogate key generation (`U0001`..`U1503`).
- **Key Columns Ingested:**
  - `RANK_2025`: Official global institutional rank.
  - `Institution_Name`: Official institutional name.
  - `Location`: Sovereign country of operation.
  - `Region`: Continental macro-region.
  - `Academic_Reputation_Score`: Global survey of over 100,000 academics (0–100).
  - `Employer_Reputation_Score`: Global survey of corporate graduate recruiters (0–100).
  - `Faculty_Student_Score`: Academic staffing capacity index (0–100).
  - `Citations_per_Faculty_Score`: Citations per faculty member benchmark (0–100).
  - `International_Faculty_Score`: Cross-border faculty representation index (0–100).
  - `International_Students_Score`: International student representation index (0–100).
  - `International_Research_Network_Score`: Cross-border collaborative co-authorship index (0–100).
  - `Overall_Score`: QS composite institutional score (0–100).

---

### 2.2 Dataset 2: Times Higher Education (THE) World University Rankings 2024
- **Publisher / Authority:** Times Higher Education
- **Distribution Platform:** Kaggle (`the_world_university_rankings_2024.csv`)
- **Temporal Horizon:** Assessment Year 2024
- **Coverage:** 2,673 universities globally
- **Role in Project:** Research analytics fact table (`fact_research`) and primary input for KPI 6 (Research Productivity Index).
- **Key Columns Ingested:**
  - `name`: Institutional name.
  - `scores_research`: Institutional research environment, volume, and income (0–100).
  - `scores_citations`: Normalized research citation impact (0–100).
  - `scores_teaching`: Learning and teaching environment score (0–100).
  - `scores_international_outlook`: International staff, student, and co-authorship score (0–100).
  - `scores_industry_income`: Commercialization and industry research grant funding (0–100).

---

### 2.3 Dataset 3: World University Rankings (WUR) 2023
- **Publisher / Authority:** Times Higher Education 2023 Edition
- **Distribution Platform:** Kaggle (`world_university_rankings_2023.csv`)
- **Temporal Horizon:** Assessment Year 2023
- **Coverage:** 2,341 universities across 104 countries
- **Role in Project:** Student demographics fact table (`fact_student`), supporting KPI 3 (Faculty-to-Student Ratio) and KPI 4 (International Student Percentage).
- **Key Columns Ingested:**
  - `Name of University`: Institutional name.
  - `No of student`: Full-time equivalent (FTE) student enrollment headcount.
  - `No of student per staff`: Actual empirical ratio of students per academic staff member.
  - `International Student`: Actual percentage of international students (%).
  - `Female : Male Ratio`: Institutional student gender distribution.

---

### 2.4 Dataset 4: World Bank Education Statistics (EdStats)
- **Publisher / Authority:** The World Bank Group
- **Distribution Platform:** World Bank Open Data / Kaggle
- **Temporal Horizon:** Longitudinal historical coverage scoped to 2010–2023
- **Coverage:** 242 sovereign countries and regional groups
- **Role in Project:** Country comparison fact table (`fact_country_education`) for macroeconomic policy analysis on Dashboard 4.
- **Key Indicators Scoped:**
  - `SE.XPD.TOTL.GD.ZS`: Government expenditure on education (% of GDP)
  - `SE.TER.ENRR`: Gross enrolment ratio, tertiary (both sexes) (%)
  - `SE.TER.ENRR.FE`: Gross enrolment ratio, tertiary (female) (%)
  - `SE.TER.ENRR.MA`: Gross enrolment ratio, tertiary (male) (%)
  - `SE.SEC.ENRR`: Gross enrolment ratio, secondary (both sexes) (%)
  - `SE.ADT.LITR.ZS`: Adult literacy rate (% aged 15 and older)

---

## 3. Data Governance, Integrity & Ethical Use

1. **Public Domain & Academic Research Use:** All datasets utilized in this project are publicly available data assets distributed under open data licenses for academic research, education, and benchmark analysis.
2. **Provenance Preservation:** Original raw CSV files are preserved unchanged in the repository archive. All data cleaning, filtering, and normalization operations are performed programmatically in Python, creating transparent, reproducible transformation steps.
3. **No Artificial Data Generation:** Missing values are handled through principled statistical rules (e.g., preserving `NaN` for non-evaluated indicators, inverse percentile ranking for published rank bands), completely avoiding synthetic data generation or arbitrary field mapping.

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**
