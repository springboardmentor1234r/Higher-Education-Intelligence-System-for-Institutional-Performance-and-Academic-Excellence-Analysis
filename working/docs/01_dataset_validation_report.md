# EduVision_DV - Dataset Validation Report
Generated before any cleaning step, per project reference guide Section 8.

### QS World University Rankings 2025
- **Source:** QS Quacquarelli Symonds (Kaggle mirror)
- **URL:** https://www.kaggle.com/datasets/joebeachcapital/qs-world-university-rankings-2025
- **Year:** 2025
- **Rows:** 1503
- **Columns:** 28
- **University Name Column:** `Institution_Name`
- **Country Column:** `Location`
- **Important Indicators:** Academic_Reputation_Score, Employer_Reputation_Score, Faculty_Student_Score, Citations_per_Faculty_Score, International_Students_Score, Overall_Score
- **Duplicate rows:** 0
- **Duplicate university names:** 0
- **Top missing-value columns (%):**
  - `Overall_Score`: 60.0%
  - `International_Faculty_Rank`: 6.7%
  - `International_Faculty_Score`: 6.7%
  - `International_Students_Score`: 3.9%
  - `International_Students_Rank`: 3.9%
  - `STATUS`: 2.5%
  - `RANK_2024`: 1.4%
  - `Sustainability_Score`: 1.3%
- **Data types:** {'object': np.int64(19), 'float64': np.int64(9)}

### Times Higher Education World University Rankings 2024
- **Source:** Times Higher Education (Kaggle mirror)
- **URL:** https://www.kaggle.com/datasets/thedevastator/2024-university-world-rankings
- **Year:** 2024
- **Rows:** 2673
- **Columns:** 29
- **University Name Column:** `name`
- **Country Column:** `location`
- **Important Indicators:** scores_overall, scores_teaching, scores_research, scores_citations, stats_student_staff_ratio, stats_pc_intl_students
- **Duplicate rows:** 0
- **Duplicate university names:** 0
- **Top missing-value columns (%):**
  - `website_url`: 87.1%
  - `scores_teaching`: 28.8%
  - `scores_international_outlook`: 28.8%
  - `scores_citations`: 28.8%
  - `scores_overall`: 28.8%
  - `scores_industry_income`: 28.8%
  - `scores_research`: 28.8%
  - `stats_female_male_ratio`: 3.5%
- **Data types:** {'object': np.int64(12), 'int64': np.int64(8), 'float64': np.int64(6), 'bool': np.int64(3)}

### World University Rankings 2023
- **Source:** Times Higher Education, via alitaqi000 (Kaggle mirror)
- **URL:** https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023
- **Year:** 2023
- **Rows:** 2341
- **Columns:** 13
- **University Name Column:** `Name of University`
- **Country Column:** `Location`
- **Important Indicators:** OverAll Score, Teaching Score, Research Score, Citations Score, No of student per staff, International Student
- **Duplicate rows:** 29
- **Duplicate university names:** 107
- **Reference row-count check:** REVIEW (reference: 1799 rows; actual: 2341 rows)
- **Top missing-value columns (%):**
  - `Industry Income Score`: 23.2%
  - `Research Score`: 23.2%
  - `Citations Score`: 23.2%
  - `OverAll Score`: 23.2%
  - `Teaching Score`: 23.2%
  - `International Outlook Score`: 23.2%
  - `Location`: 12.6%
  - `Female:Male Ratio`: 9.1%
- **Data types:** {'object': np.int64(7), 'float64': np.int64(6)}

### World Bank Education Statistics
- **Source:** World Bank EdStats (Kaggle: theworldbank/education-statistics)
- **URL:** https://www.kaggle.com/datasets/theworldbank/education-statistics
- **Year:** multi-year panel (1970-2020s)
- **Rows (full file):** 1210
- **Columns:** 70 (65 year columns)
- **University Name Column:** n/a (country-level dataset)
- **Country Column:** `Country Name`
- **Important Indicators (of 5 total in file):** SE.XPD.TOTL.GD.ZS, SE.TER.ENRR, SE.ADT.LITR.ZS, SE.XPD.TOTL.GB.ZS, SE.PRM.ENRR
- **Rows matching our 5 selected indicators:** 1210
- **Countries covered by selected indicators:** 242
- **Duplicate rows:** 0
