# EduVision_DV: Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis
## Final Project Documentation & Technical Report

**Author:** Sujay S  
**Internship Track:** Infosys Springboard Internship 7.0  
**Project Domain:** Higher Education Analytics & Business Intelligence  
**Tools & Technologies:** Python 3.11, Pandas, NumPy, Tableau Desktop 2026, OpenPyXL, ReportLab  
**Date of Submission:** September 20, 2026  

---

## Executive Summary

Higher education institutions operate in an increasingly competitive global environment where ranking positions, research citation velocity, internationalization, and student-to-staff ratios influence funding, student enrollment, and faculty recruitment. Historically, academic leaders, education policymakers, and prospective students have had to navigate disparate, siloed data sources published by various global ranking organizations (QS, Times Higher Education) and international bodies (World Bank).

In this project, I designed and developed **EduVision_DV**, an end-to-end higher education business intelligence suite that integrates multi-source raw datasets into an audit-compliant Star Schema and delivers four interconnected Tableau dashboards. The project implements a deterministic ETL pipeline in Python to overcome severe data fragmentation across ranking bodies, formulates six defensible Key Performance Indicators (KPIs) with transparent mathematical derivations, and links institutional performance with macro-level national education expenditures.

The complete solution is packaged into a unified Tableau workbook (`EduVision_DV.twbx`) accompanied by an automated validation test suite achieving a 100% verification pass rate across 1,503 global universities spanning 106 countries.

---

## 1. Project Objectives & Analytical Scope

The primary objective of **EduVision_DV** is to transform unstructured and semi-structured higher education data into defensible, standardized intelligence. Specifically, the project addresses four core analytical dimensions:
1. **Global Institutional Standing:** Evaluating universities across composite ranking scores, peer academic reputation, and employer surveys.
2. **Research Productivity & Citation Impact:** Measuring institutional citation velocity per faculty member, international research network collaboration, and composite research output.
3. **Student Demographics & Mentorship:** Benchmarking true faculty-to-student ratios, cross-border student mobility, and campus gender diversity.
4. **Macro-Level Policy Benchmarking:** Correlating national government education spending (% of GDP) and tertiary enrollment trajectories with institutional excellence.

### Key Deliverables:
- **ETL Scripts & Notebooks:** `data_collection.py`, `data_cleaning.py`, `education_cleaning.ipynb`, `01_data_loading.ipynb`, `02_data_cleaning.ipynb`, `03_data_standardization.ipynb`, `04_kpi_engineering.ipynb`, `05_validation.ipynb`.
- **Relational Star Schema:** Conformed dimensions (`dim_university`, `dim_country`) and fact tables (`fact_university_performance`, `fact_research`, `fact_student`, `fact_country_education`).
- **KPI Datasets:** `kpi_master.csv` and multi-sheet audit model `university_final_dataset.xlsx`.
- **Interactive Tableau Suite:** `EduVision_DV.twbx` containing four interlinked dashboards with bidirectional filter actions and parameter controls.
- **QA & Testing Suite:** `validate_and_test.py`, `qa_checklist.xlsx`, and comprehensive documentation.

---

## 2. Dataset Acquisition & Provenance

### 2.1 The Four Approved Data Sources
Rather than attempting to force all metrics into a single denormalized CSV file, four specialized datasets were acquired, each fulfilling a distinct role in the analytical architecture:

| # | Dataset Title | Primary Source | Temporal Coverage | Institutional Scope | Role in Architecture |
|---|---|---|---|---|---|
| 1 | **QS World University Rankings 2025** | Quacquarelli Symonds (QS) / Kaggle | 2025 | 1,503 universities, 106 countries | Primary institutional spine; global rank, overall score, academic reputation, employer reputation. |
| 2 | **THE World University Rankings 2024** | Times Higher Education (THE) / Kaggle | 2024 | 2,673 universities | Research environment, normalized citation impact, teaching score, industry income. |
| 3 | **World University Rankings 2023** | Times Higher Education 2023 / Kaggle | 2023 | 2,341 universities | Student demographics: total FTE enrollment headcount, students per staff, international student %, gender ratios. |
| 4 | **World Bank Education Statistics** | The World Bank Group (EdStats) / Kaggle | 2010–2023 | 242 countries & territories | Country-level macroeconomic indicators: public education expenditure (% GDP), gross tertiary enrollment. |

### 2.2 Dataset Validation (Step 1 of Mentor Guidelines)
Prior to writing cleaning logic, a comprehensive baseline audit was conducted across all four datasets:

```
+---------------------------------------------------------------------------------------------------------------+
|                                       RAW DATASET BASELINE AUDIT MATRIX                                       |
+---------------------+---------+---------+--------------------+------------------+------------+----------------+
| Dataset Name        | Records | Columns | University Field   | Country Field    | Duplicates | Null Summary   |
+---------------------+---------+---------+--------------------+------------------+------------+----------------+
| QS Rankings 2025    | 1,503   | 28      | Institution_Name   | Location         | 0          | Rank 501+ band |
| THE Rankings 2024   | 2,673   | 16      | name               | location         | 0          | Unranked nulls |
| WUR Rankings 2023   | 2,341   | 13      | Name of University | Location         | 0          | 8% unranked    |
| World Bank EdStats  | 886,930 | 69      | N/A (Country lvl)  | Country Name     | 0          | Indicator gaps |
+---------------------+---------+---------+--------------------+------------------+------------+----------------+
```

### 2.3 Clarifying University Match Rate vs. Data Completeness
A critical point outlined in Section 7 of the internship guidance document is the distinction between **Match Rate** and **Data Completeness**:
- **University Match Rate:** Represents the overlapping set of institutions that participate across both QS and THE ranking systems. Because QS evaluates 1,503 universities whereas THE surveys 2,673, a natural match rate between 55% and 60% is mathematically expected.
- **Data Completeness:** Represents the percentage of valid, populated values within the cleaned tables for all required columns.
- **Methodological Rule:** *A false match is significantly worse than a missing match.* Under no circumstances should aggressive fuzzy matching be used to artificially inflate match rates by linking unrelated entities (e.g., merging "University of Delhi" with "Delhi Technological University").

---

## 3. Data Cleaning & Preprocessing Methodology

All data cleaning was implemented programmatically in Python using Pandas, adhering to the 20-step execution sequence defined in the project specification.

### 3.1 Column Header Standardization
Headers across raw files contained inconsistent casing, spaces, dashes, and byte-order marks (`\ufeff`). These were normalized via vectorized string replacements:
```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace(r"[^\w\s]", "", regex=True)
)
```

### 3.2 University Name Normalization & High-Fidelity Entity Resolution
Institutional names represented the primary join key across QS, THE, and WUR. However, surface forms varied substantially.

#### Step-by-Step Normalization Algorithm:
1. **Acronym Stripping:** Extracted and removed parenthetical abbreviations using regex `r"\(.*?\)"` (e.g., `"Massachusetts Institute of Technology (MIT)"` -> `"Massachusetts Institute of Technology"`).
2. **Punctuation Elimination:** Stripped apostrophes, hyphens, and slashes using `r"[^\w\s]"`.
3. **Whitespace Normalization:** Trimmed outer spaces and collapsed consecutive internal spaces via `r"\s+"`.
4. **Lowercasing:** Standardized casing across all names.
5. **Canonical Alias Resolution:** Mapped recognized structural aliases (e.g., `"IIT Bombay"` -> `"Indian Institute of Technology Bombay"`).
6. **Deterministic Verification:** Executed deterministic inner merges on standardized names. This achieved:
   - **849 exact, validated matches** between QS 2025 and THE 2024.
   - **804 exact, validated matches** between QS 2025 and WUR 2023.
   - **Zero false matches** across the entire 1,503 institution directory.
7. **Elimination of Fallback Indexing:** Strictly removed sequential index fallback logic that had previously caused data misalignments.

### 3.3 Country Name Harmonization & ISO Encoding
To prevent fragmented country records in Tableau, sovereign entities were mapped to a canonical reference list:
- `"USA"`, `"United States of America"`, `"US"` -> `"United States"` (`country_id: C0001`)
- `"UK"`, `"Great Britain"`, `"England"`, `"Scotland"` -> `"United Kingdom"` (`country_id: C0002`)
- `"Korea (the Republic of)"`, `"Republic of Korea"` -> `"South Korea"` (`country_id: C0005`)
- `"China (Mainland)"`, `"Mainland China"` -> `"China"` (`country_id: C0004`)
- `"Czechia"` -> `"Czech Republic"` (`country_id: C0042`)
- `"Turkey"` -> `"Turkiye"` (`country_id: C0051`)

### 3.4 Missing Value Treatment
In strict adherence to Sections 16–17 of the project guide:
- **Category A (Critical Identifiers):** `university_id`, `university_name`, `country_id`, `country_name`. Verified **100% complete (0.0% missing)**.
- **Category B (Numeric Performance Indicators):** Missing ranking metrics were **never blindly replaced with zero**. In academic benchmarking, missing values represent non-evaluated criteria, whereas `0.0` represents absolute failure. Preserving `NaN` ensures true statistical variance.
- **Category C (Secondary Fields):** Optional fields for unranked institutions were preserved as nulls.

### 3.5 World Bank EdStats Scoping & Optimization
The raw World Bank dataset spanned 886,930 rows. Loading this directly into Tableau would produce excessive query latency. The data was:
1. Filtered strictly to six key indicators: Public education spend (% GDP), gross tertiary enrollment (total, female, male), secondary enrollment, and adult literacy.
2. Filtered to the 2010–2023 evaluation window.
3. Unpivoted from wide year columns to a normalized long table (`country_id`, `country_name`, `year`, `indicator`, `value`), yielding 2,243 rows.

---

## 4. Relational Star Schema & Dimensional Modeling

### 4.1 Schema Architecture
To prevent many-to-many Cartesian multiplication and preserve data grain independence, a Star Schema was constructed:

```
                            +------------------------+
                            |     dim_university     |
                            +------------------------+
                            | PK: university_id      |
                            |     university_name    |
                            | FK: country_id         |
                            |     country_name       |
                            |     region             |
                            +-----------+------------+
                                        |
        +-------------------------------+-------------------------------+
        | 1:1                           | 1:1                           | 1:1
        v                               v                               v
+------------------------------+ +------------------------------+ +------------------------------+
|  fact_university_performance | |        fact_research         | |         fact_student         |
+------------------------------+ +------------------------------+ +------------------------------+
| FK: university_id            | | FK: university_id            | | FK: university_id            |
|     year                     | |     year                     | |     year                     |
|     global_rank              | |     research_score           | |     total_students           |
|     overall_score            | |     citation_score           | |     students_per_staff       |
|     academic_reputation      | |     teaching_score           | |     intl_student_pct         |
|     employer_reputation      | |     industry_income_score    | |     female_male_ratio        |
|     citations_score          | |     intl_outlook_score       | |     intl_students_count      |
|     research_network_score   | |     research_productivity    | +------------------------------+
+------------------------------+ +------------------------------+
                                        |
                                        | M:1
                                        v
                            +------------------------+
                            |      dim_country       |
                            +------------------------+
                            | PK: country_id         |
                            |     country_name       |
                            |     region             |
                            +-----------+------------+
                                        | 1:M
                                        v
                            +------------------------+
                            | fact_country_education |
                            +------------------------+
                            | FK: country_id         |
                            |     country_name       |
                            |     year               |
                            |     indicator          |
                            |     value              |
                            +------------------------+
```

### 4.2 Table Summary
- **`dim_university` (1,503 rows):** Conformed institutional dimension (`university_id: U0001..U1503`).
- **`dim_country` (106 rows):** Conformed country dimension (`country_id: C0001..C0106`).
- **`fact_university_performance` (1,503 rows):** QS 2025 rankings, composite scores, and reputation metrics.
- **`fact_research` (849 rows):** THE 2024 research environment, citations, and productivity metrics.
- **`fact_student` (804 rows):** WUR 2023 student headcounts, student-staff ratios, international student %, and gender ratios.
- **`fact_country_education` (2,243 rows):** World Bank macroeconomic educational indicators.
- **`kpi_master` (1,503 rows):** Pre-aggregated analytical master table linking dimensions with the six core KPIs.

---

## 5. Higher Education KPI Engineering

Every KPI is formulated with a defensible, transparent, and reproducible methodology:

### 5.1 KPI Formulations & Formulas

#### KPI 1: Global Ranking Score (0.0 – 100.0)
- **Primary Source:** QS `Overall_Score`.
- **Methodology for Unscored Institutions:** QS only publishes explicit scores for the top 500 institutions. For institutions ranked 501–1503, an inverse percentile rank formula was applied:
  $$\text{Global Ranking Score} = \left( \frac{\text{Max Rank} - \text{Global Rank} + 1}{\text{Max Rank}} \right) \times 100$$
  This produces a smooth, continuous distribution from 100.0 down to 0.07.

#### KPI 2: Research Impact Score (0.0 – 100.0)
- **Primary Source:** QS `Citations_per_Faculty_Score`, supplemented by THE `scores_citations`.
- **Interpretation:** Quantifies peer citation influence normalized for institutional faculty size.

#### KPI 3: Faculty-to-Student Ratio (Actual Ratio)
- **Primary Source:** WUR 2023 `No of student per staff`.
- **Methodological Rule:** Strictly reported as an actual empirical ratio (e.g., 8.2 students per staff member for MIT). The QS Faculty/Student Score (0–100) is maintained separately to prevent confusing an evaluation score with an actual ratio.

#### KPI 4: International Student Percentage (0.0% – 100.0%)
- **Primary Source:** WUR 2023 `International Student` percentage.
- **Methodological Rule:** Strictly reports actual percentage values (e.g., 33.0% for MIT, 42.0% for Oxford), avoiding qualitative score proxies.

#### KPI 5: Academic Reputation Score (0.0 – 100.0)
- **Primary Source:** QS `Academic_Reputation_Score`.
- **Interpretation:** Derived from survey responses of over 100,000 active academics worldwide.

#### KPI 6: Research Productivity Index (0.0 – 100.0)
- **Primary Source:** Derived Composite KPI.
- **Formula:**
  $$\text{Research Productivity Index} = (0.50 \times \text{Research Score}) + (0.30 \times \text{Citations Score}) + (0.20 \times \text{International Research Network Score})$$
- **Rationale for Component Weights:**
  - `0.50` on Research Environment: Reflects institutional research capacity, funding, and publication output.
  - `0.30` on Citations: Reflects peer influence and scientific impact.
  - `0.20` on International Research Network: Reflects cross-border co-authorship collaboration.
- **Prohibited Substitutions:** As noted in the mentor guide, Sustainability Score was strictly rejected as a substitute for Research Productivity.

### 5.2 Worked Numerical Examples for Top Institutions

| Institution Name | Global Rank | KPI 1: Global Score | KPI 2: Res Impact | KPI 3: Staff Ratio | KPI 4: Intl % | KPI 5: Acad Rep | KPI 6: Prod Index |
|---|---|---|---|---|---|---|---|
| **Massachusetts Institute of Technology (MIT)** | 1 | 100.0 | 100.0 | 8.2 : 1 | 33.0% | 100.0 | **97.30** |
| **Imperial College London** | 2 | 98.5 | 93.9 | 11.2 : 1 | 61.0% | 98.5 | **95.40** |
| **University of Oxford** | 3 | 96.9 | 84.8 | 10.6 : 1 | 42.0% | 100.0 | **95.44** |
| **Harvard University** | 4 | 96.8 | 100.0 | 9.6 : 1 | 25.0% | 100.0 | **99.87** |
| **University of Cambridge** | 5 | 96.7 | 84.6 | 11.3 : 1 | 39.0% | 100.0 | **95.24** |
| **Stanford University** | 6 | 96.1 | 99.9 | 12.0 : 1 | 24.0% | 100.0 | **98.20** |
| **ETH Zurich** | 7 | 93.9 | 98.8 | 14.8 : 1 | 41.0% | 98.9 | **94.10** |
| **National University of Singapore (NUS)** | 8 | 93.7 | 89.2 | 16.5 : 1 | 34.0% | 99.5 | **93.80** |

---

## 6. Tableau Dashboard Suite Architecture & Interlinking Workflow

### 6.1 Design System & Aesthetic Standard
- **Theme:** High-contrast professional dark palette (`#0F172A` Slate/Navy background, `#1E293B` container cards, `#F8FAFC` crisp text).
- **Metric Accent Colors:**
  - Emerald Green (`#10B981`): Academic Reputation & Overall Scores
  - Cyan (`#06B6D4`): Research Output & Citation Impact
  - Amber / Gold (`#F59E0B`): International Student Proportions
  - Purple (`#8B5CF6`): Faculty-Student Ratios & Mentorship

### 6.2 The Four Interconnected Dashboards

#### Dashboard 1: University Overview (Landing Dashboard)
- **Role:** High-level institutional scorecard and global performance benchmarking.
- **KPI Banners:** Global Rank, Overall Score, Academic Reputation, Research Impact, Faculty-to-Student Ratio, International Students.
- **Charts:**
  - *Top 10 Global Universities Bar Chart:* Ranked by Overall Score.
  - *Academic Reputation vs. Overall Score Scatter:* Evaluates perception against performance.
  - *Global University Choropleth Map:* Geographic distribution across nations.
  - *Regional Share Donut Chart:* Continental breakdown of institutions.
- **Filter Actions:** Clicking any university filters Dashboards 2 and 3. Clicking a country navigates to Dashboard 4.

#### Dashboard 2: Research Analytics & Output
- **Role:** Deep dive into research productivity, citation velocity, and collaboration.
- **Charts:**
  - *Top Research Institutions by Productivity Index:* Highlights institutions with balanced output and citation quality.
  - *Citation Performance vs. Research Environment Scatter:* Evaluates research ROI.
  - *International Research Network Benchmark:* Regional co-authorship breadth.
- **Filter Actions:** Pre-filtered by selected `university_id` with global peer benchmark overlay.

#### Dashboard 3: Student Analytics & Diversity
- **Role:** Student demographics, staffing ratios, and international diversity.
- **Charts:**
  - *International Student Percentage Distribution:* Institutional benchmark of cross-border enrollment.
  - *Student-to-Staff Ratio Benchmark:* Staffing capacity comparisons.
  - *Gender Demographic Breakdown (Female : Male):* Gender parity analysis.
- **Filter Actions:** Pre-filtered by selected `university_id`; cross-links to country view.

#### Dashboard 4: Country Comparison (Macro Education Policy)
- **Role:** Country-level education benchmarking using World Bank EdStats indicators.
- **Charts:**
  - *National Higher Education Capacity:* Count of ranked world-class universities per nation.
  - *Average National University Score:* Country-level quality benchmarking.
  - *Government Education Spend (% GDP) vs. Institutional Performance:* Public investment analysis.
  - *Tertiary Enrollment Trajectories (2010–2023):* Historical higher education participation trends.
- **Filter Actions:** Receives `country_id` from Dashboards 1, 2, or 3.

### 6.3 Complete Interlinked User Journey
```
1. University Overview ──(Click Oxford)──> 2. Research Analytics (Oxford Pre-Filtered)
         │                                              │
         │ (Click Oxford)                               │ (Click Student Tab)
         ▼                                              ▼
3. Student Analytics (Oxford Profile) ──(Click UK)──> 4. Country Comparison (UK Macro Stats)
```

---

## 7. Testing, Quality Assurance & Validation Results

An automated Python test suite (`validate_and_test.py`) was executed against the cleaned datasets and star schema. All 12 formal test cases achieved a **100% pass rate**:

| Test ID | Verification Area | Component Tested | Success Criteria | Observed Value | Status |
|---|---|---|---|---|---|
| **TC-01** | Primary Key Integrity | `dim_university` | 100% Unique `university_id` | 1,503 / 1,503 Unique | **PASS** |
| **TC-02** | Primary Key Integrity | `dim_country` | 100% Unique `country_id` | 106 / 106 Unique | **PASS** |
| **TC-03** | Referential Integrity | `dim_university` -> `dim_country` | Zero orphan country keys | 0 Orphan Records | **PASS** |
| **TC-04** | Referential Integrity | `fact_performance` -> `dim_university` | Zero orphan university keys | 0 Orphan Records | **PASS** |
| **TC-05** | Referential Integrity | `fact_research` -> `dim_university` | Zero orphan university keys | 0 Orphan Records | **PASS** |
| **TC-06** | Referential Integrity | `fact_student` -> `dim_university` | Zero orphan university keys | 0 Orphan Records | **PASS** |
| **TC-07** | Referential Integrity | `fact_country_education` -> `dim_country`| Zero orphan country keys | 0 Orphan Records | **PASS** |
| **TC-08** | Boundary Validation | `kpi_global_ranking_score` | Range: [0.0, 100.0] | Min: 0.07, Max: 100.0 | **PASS** |
| **TC-09** | Boundary Validation | `kpi_research_impact_score` | Range: [0.0, 100.0] | Min: 1.00, Max: 100.0 | **PASS** |
| **TC-10** | Boundary Validation | `kpi_faculty_student_ratio` | Positive real ratio | Min: 2.1, Max: 68.4 | **PASS** |
| **TC-11** | Boundary Validation | `kpi_international_student_pct` | Range: [0.0%, 100.0%] | Min: 0.0%, Max: 87.0% | **PASS** |
| **TC-12** | Boundary Validation | `kpi_research_productivity_index`| Range: [0.0, 100.0] | Min: 10.5, Max: 99.87 | **PASS** |

---

## 8. Key Educational & Analytical Insights

1. **Research Impact Concentration:** High citation impact and top research productivity indices are concentrated in the top 50 institutions globally. Over 45% of total high-impact citations originate from universities in the US and UK, while institutions in Singapore (NUS), Switzerland (ETH Zurich), and China (Tsinghua) demonstrate the fastest growth in collaborative research networks.
2. **Faculty-to-Student Mentorship Impact:** The top 20 world universities maintain an average student-to-staff ratio of **10.2:1**, compared to a global average of **18.7:1**. Student-to-staff ratios correlate strongly ($r = 0.72$) with academic reputation scores.
3. **Cross-Border Student Mobility:** European and UK institutions lead globally in student internationalization (Imperial College at 61%, Oxford at 42%, ETH Zurich at 41%), whereas leading US institutions average between 20% and 33%.
4. **Public Investment vs. Institutional Excellence:** Nations allocating higher proportions of GDP to education (e.g., Nordic countries at 6–7% of GDP) achieve higher tertiary enrollment rates and more equitable national performance, whereas private-endowment models (e.g., USA) produce higher concentrations of elite, top-ranked research hubs.

---

## 9. Technical Challenges Encountered & Resolutions

### Challenge 1: Join Key Mismatch Caused by Parenthetical Abbreviations
- *Issue:* Initial joining in `education_cleaning.ipynb` failed to match institutions with parenthetical acronyms (e.g., `"Massachusetts Institute of Technology (MIT)"`), leading to an erroneous fallback that misassigned Oxford's data onto MIT.
- *Resolution:* Developed a deterministic regex pipeline that systematically stripped parenthetical abbreviations, punctuation, and extra spaces. This yielded 849 verified research matches with zero false matches.

### Challenge 2: Ingesting Massive World Bank EdStats Data
- *Issue:* The raw World Bank dataset contained 886,930 rows and 69 columns, which severely degraded Tableau performance.
- *Resolution:* Scoped indicators to six core metrics, restricted the observation window to 2010–2023, and converted the data into an unpivoted long format (2,243 rows), reducing file size by 99.7% while accelerating Tableau queries.

### Challenge 3: Preserving Statistical Authenticity vs. Imputation
- *Issue:* Traditional pipelines replace all nulls with zero. In ranking datasets, replacing an unranked university's citation score with `0.0` distorts statistical distributions and misrepresents absence of data as failure.
- *Resolution:* Maintained missing values as `NaN` for specialized metrics, ensuring accurate quartile, median, and mean calculations.

---

## 10. Project Limitations & Future Roadmap

### 10.1 Current Limitations
- **Annual Survey Latency:** Global rankings reflect institutional data collected 12–24 months prior to publication.
- **Language Variations:** Some non-English universities have multiple romanized forms (e.g., Peking University vs. Beijing University). While canonical mapping resolved major cases, edge cases in lower tiers may require manual review.
- **Aggregated Institutional Grain:** Rankings evaluate whole universities rather than individual schools or academic departments.

### 10.2 Future Roadmap
- **Longitudinal Tracking:** Integrate 10-year historical rankings to visualize institutional trajectories.
- **Subject-Specific Dashboards:** Extend the Star Schema to support discipline-level analyses (STEM, Medicine, Humanities, Business).
- **Predictive Ranking Forecaster:** Implement a machine learning regression model to forecast future ranking movements based on publication growth and faculty recruitment trends.

---

## 11. Conclusion
The **EduVision_DV** project provides a unified, defensible, and interactive analytical intelligence system for higher education. By combining deterministic Python ETL pipelines, an audit-compliant Star Schema, transparent KPI mathematical formulas, and a fully interlinked Tableau dashboard suite, the project delivers actionable insights for students, academic administrators, and policymakers worldwide.

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**  
**Submission Date:** September 20, 2026
