# EduVision_DV: Dashboard Testing & Data Validation Report

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Milestone:** Milestone 4 / Module 7 (Testing and Validation)  
**Evaluation Date:** September 20, 2026  
**Test Suite Script:** `validate_and_test.py`  
**Overall Validation Result:** **100.0% PASS (12 of 12 Automated Tests Passed)**  
**Certification Status:** **VERIFIED & PORTFOLIO READY**  

---

## 1. Executive Summary & Testing Objectives

The **EduVision_DV** higher education analytics suite underwent formal automated and manual verification prior to final deployment. The purpose of this quality assurance cycle was to verify:
1. **Relational Integrity:** Ensure 100% uniqueness of primary dimension keys and zero orphan records across fact tables.
2. **Mathematical Accuracy:** Validate that all engineered Key Performance Indicators (KPIs) conform to defined mathematical formulas and empirical boundaries.
3. **Data Completeness:** Confirm that missing values in critical identifier fields are strictly 0.0%.
4. **Tableau Interactivity & UX:** Test bidirectional filter actions, navigation controls, and cross-dashboard data passing in `EduVision_DV.twbx`.

---

## 2. Testing Environment & Tools
- **Operating System:** Windows 11 Enterprise
- **Programming Language:** Python 3.11.9
- **Libraries:** Pandas 3.0.6, NumPy 2.2.3, OpenPyXL 3.1.5
- **BI Platform:** Tableau Desktop 2026.1
- **Automated Test Harness:** Custom Python assertion suite (`validate_and_test.py`)

---

## 3. Automated Test Suite Results

```
+-------------------------------------------------------------------------------------------------------------------+
|                                            AUTOMATED QA TEST EXECUTION LOG                                        |
+-------+-----------------------------+------------------------------------+---------------+----------------+-------+
| Test  | Test Category               | Target Component                   | Expected      | Observed       | Status|
+-------+-----------------------------+------------------------------------+---------------+----------------+-------+
| TC-01 | Primary Key Uniqueness      | dim_university.university_id       | 1,503 unique  | 1,503 unique   | PASS  |
| TC-02 | Primary Key Uniqueness      | dim_country.country_id             | 106 unique    | 106 unique     | PASS  |
| TC-03 | Referential Integrity       | dim_university -> dim_country      | 0 orphans     | 0 orphans      | PASS  |
| TC-04 | Referential Integrity       | fact_performance -> dim_university | 0 orphans     | 0 orphans      | PASS  |
| TC-05 | Referential Integrity       | fact_research -> dim_university    | 0 orphans     | 0 orphans      | PASS  |
| TC-06 | Referential Integrity       | fact_student -> dim_university     | 0 orphans     | 0 orphans      | PASS  |
| TC-07 | Referential Integrity       | fact_country_ed -> dim_country     | 0 orphans     | 0 orphans      | PASS  |
| TC-08 | KPI Boundary Validation     | kpi_global_ranking_score           | [0.0, 100.0]  | Min:0.07,Max:100| PASS |
| TC-09 | KPI Boundary Validation     | kpi_research_impact_score          | [0.0, 100.0]  | Min:1.0,Max:100| PASS  |
| TC-10 | KPI Boundary Validation     | kpi_faculty_student_ratio          | Real ratio >0 | Min:2.1,Max:68.4| PASS|
| TC-11 | KPI Boundary Validation     | kpi_international_student_pct      | [0.0%, 100.0%]| Min:0.0%,Max:87%| PASS|
| TC-12 | KPI Boundary Validation     | kpi_research_productivity_index   | [0.0, 100.0]  | Min:10.5,Max:99.87|PASS|
+-------+-----------------------------+------------------------------------+---------------+----------------+-------+
```

### Detailed Breakdown of Test Cases:

#### TC-01: Primary Key Uniqueness (`dim_university`)
- *Procedure:* Counted unique `university_id` values and compared against total record count.
- *Assertion:* `len(dim_u['university_id'].unique()) == len(dim_u) == 1503`.
- *Result:* **PASS**. 1,503 unique keys, 0 duplicates.

#### TC-02: Primary Key Uniqueness (`dim_country`)
- *Procedure:* Counted unique `country_id` values and compared against total record count.
- *Assertion:* `len(dim_c['country_id'].unique()) == len(dim_c) == 106`.
- *Result:* **PASS**. 106 unique keys, 0 duplicates.

#### TC-03 to TC-07: Referential Integrity (Foreign Key Resolution)
- *Procedure:* Performed left outer joins between child fact tables and parent dimension tables, counting records with null parent keys.
- *Observed Orphan Count:*
  - `dim_university` to `dim_country`: **0 orphans** (100% resolution).
  - `fact_university_performance` to `dim_university`: **0 orphans** (1,503 / 1,503 matched).
  - `fact_research` to `dim_university`: **0 orphans** (849 / 849 matched).
  - `fact_student` to `dim_university`: **0 orphans** (804 / 804 matched).
  - `fact_country_education` to `dim_country`: **0 orphans** (2,243 / 2,243 matched).
- *Result:* **PASS**.

#### TC-08 to TC-12: KPI Range & Boundary Checks
- *Procedure:* Evaluated minimum, maximum, and mean values of all calculated KPIs in `kpi_master.csv`.
- *Findings:*
  - `kpi_global_ranking_score`: Minimum value is 0.07 (institution #1503), maximum is 100.0 (MIT). All values lie strictly within $[0, 100]$.
  - `kpi_research_impact_score`: Minimum value is 1.0, maximum is 100.0. No negative values or values exceeding 100.
  - `kpi_faculty_student_ratio`: Minimum is 2.1 students per staff, maximum is 68.4. All values are strictly positive real numbers.
  - `kpi_international_student_pct`: Minimum is 0.0%, maximum is 87.0%.
  - `kpi_research_productivity_index`: Minimum is 10.5, maximum is 99.87 (Harvard University).
- *Result:* **PASS**.

---

## 4. Tableau Interactive Functionality Testing

In addition to automated data tests, manual testing was performed on the packaged Tableau workbook (`EduVision_DV.twbx`) across all four dashboards:

| Test ID | Interaction Tested | Test Procedure | Expected UX Behavior | Observed Outcome | Status |
|---|---|---|---|---|---|
| **UX-01** | University Filter Action | Click 'University of Oxford' on Dashboard 1 | Dashboards 2 & 3 open pre-filtered for Oxford | Pre-filtered correctly; displays Oxford metrics | **PASS** |
| **UX-02** | Country Filter Action | Click 'United Kingdom' on Dashboard 1 map | Dashboard 4 opens pre-filtered for UK | Dashboard 4 displays UK capacity & spend stats | **PASS** |
| **UX-03** | Top Navigation Bar | Click 'Research Analytics' button on header | Navigates directly to Dashboard 2 | Instantaneous transition; retains active filters | **PASS** |
| **UX-04** | Global Region Filter | Select 'Asia' from top filter dropdown | All chart marks update to Asian institutions | Charts refresh smoothly; renders Asian peers | **PASS** |
| **UX-05** | Reset / Clear Filter | Click in empty space on bar chart | Resets active selection to all universities | View restores full global ranking list | **PASS** |

---

## 5. Quality Assurance Sign-Off & Certification

- **Target Completeness:** >95% (Achieved: **100% on all dimension keys**).
- **Target Missing Rate:** <2% on critical primary identifiers (Achieved: **0.0%**).
- **Target Interlinking:** 4 of 4 dashboards fully interlinked (Achieved: **100%**).
- **Automated Test Score:** **100% (12 / 12 passed)**.

**Final Certification Decision:** **APPROVED FOR FINAL DEPLOYMENT AND SUBMISSION**

---
**QA Engineer / Author:** Sujay S  
**Infosys Springboard Internship 7.0**
