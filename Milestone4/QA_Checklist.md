# QA Checklist — Module 7: Testing & Validation

---

## 1. Project Information

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Module** | Module 7 — Testing & Validation |
| **Workbook** | `EduVision_DV.twbx` |
| **Dashboards** | University Overview · Research Analytics · Student Analytics · Country Comparison |
| **Testing Status** | Completed |
| **Overall Result** | ✅ PASS |

---

## 2. Module 7 Requirements

The project specification requires Module 7 to fulfil the following objectives:

- ☑ Validate KPI calculations
- ☑ Verify ranking calculations
- ☑ Test dashboard interactions
- ☑ Validate educational metrics
- ☑ Prepare a QA Checklist
- ☑ Prepare a Dashboard Testing Report

**Evaluation Target:** No major dashboard issues identified · KPI accuracy above 95%

---

## 3. KPI Validation Checklist

| # | KPI | Validation Performed | Result |
|---|-----|----------------------|--------|
| 1 | Global Ranking Score | Verified source/calculation and confirmed valid score range (0–100) | ✅ PASS |
| 2 | Research Impact Score | Verified source/calculation and confirmed valid score range (0–100) | ✅ PASS |
| 3 | Faculty-to-Student Ratio | Verified correct ratio field; validated values and missing data handling | ✅ PASS |
| 4 | International Student Percentage | Verified correct field and percentage representation | ✅ PASS |
| 5 | Academic Reputation Score | Verified KPI source and confirmed valid score range (0–100) | ✅ PASS |
| 6 | Research Productivity Index | Verified normalized composite calculation from available research indicators | ✅ PASS |

**KPI Validation Result:** 6 / 6 tested KPI checks passed — **100% pass rate**

> **Note:** Missing values in source KPI fields were treated as missing data and not substituted with zero values.

---

## 4. Ranking Validation Checklist

| Test | Expected Result | Result |
|------|-----------------|--------|
| Global rank ordering | Lower rank number represents a higher institutional position | ✅ PASS |
| Normalized rank consistency | `normalized_rank` is consistent with `global_rank` | ✅ PASS |
| Global ranking score directionality | Score decreases consistently as rank number increases | ✅ PASS |

### Sample Ranking Validation Data

*Source: `kpi_summary` sheet — sorted by `global_rank` ascending*

| Global Rank | Normalized Rank | Global Ranking Score |
|:-----------:|:---------------:|:--------------------:|
| 1 | 1 | 100.00 |
| 2 | 2 | 99.93 |
| 3 | 3 | 99.87 |
| 4 | 4 | 99.80 |
| 5 | 5 | 99.73 |
| 6 | 6 | 99.67 |
| 7 | 7 | 99.60 |
| 8 | 8 | 99.53 |

**Ranking Validation Result:** All 3 ranking checks passed — **100% pass rate**

---

## 5. Dashboard Interaction Testing

### 5.1 University Name Filter

- Selected a university on **University Overview**
- University-specific KPI cards and charts updated accordingly

**Result:** ✅ PASS

---

### 5.2 University Overview → Research Analytics (Cross-Dashboard Linking)

- Selected university was correctly passed to **Research Analytics**

**Result:** ✅ PASS

---

### 5.3 Research Analytics → Student Analytics (Cross-Dashboard Linking)

- Selected university was correctly passed to **Student Analytics**

**Result:** ✅ PASS

---

### 5.4 Student Analytics → Country Comparison (Cross-Dashboard Linking)

- The university's country was correctly passed to **Country Comparison**

**Result:** ✅ PASS

---

### 5.5 Ranking Year Filter

- Changed the **Ranking Year** filter on Country Comparison
- Dashboard visualizations updated correctly

**Result:** ✅ PASS

---

### 5.6 Country Filter

- Changed the **Country** filter on Country Comparison
- Dashboard visualizations updated correctly

**Result:** ✅ PASS

---

### 5.7 Region Filter

- Changed the **Region** filter on Country Comparison
- Dashboard visualizations updated correctly
- Regional Education Trends visual responded correctly

**Result:** ✅ PASS

---

### 5.8 Performance Metric Parameter

Tested the following parameter options:

| Parameter Option | Response |
|------------------|----------|
| Ranking Score | Country Ranking Comparison chart updated correctly |
| Overall Score | Country Ranking Comparison chart updated correctly |
| Research Impact Score | Country Ranking Comparison chart updated correctly |

**Result:** ✅ PASS

---

### 5.9 Dashboard Navigation

Tested the full navigation flow:

**University Overview → Research Analytics → Student Analytics → Country Comparison → University Overview**

All navigation buttons functioned correctly with no broken links or layout failures.

**Result:** ✅ PASS

---

### 5.10 Filter Clearing

- Cleared the selected university filter
- Research Analytics correctly reverted to displaying all universities rather than retaining the previous selection

**Result:** ✅ PASS

---

## 6. Educational Metric Validation

| Dashboard | Metric | Correct Field Used | Result |
|-----------|--------|--------------------|--------|
| Student Analytics | Faculty-to-Student Ratio | `Faculty To Student Ratio` | ✅ PASS |
| Student Analytics | International Student Percentage | `International Student Percentage` | ✅ PASS |
| Student Analytics | Student Diversity | `Female Percentage` | ✅ PASS |
| Research Analytics | Research Impact Score | `Research Impact Score` | ✅ PASS |
| Research Analytics | Citation Performance | `Citations Score` | ✅ PASS |
| Research Analytics | Research Productivity | `Research Productivity Index` | ✅ PASS |
| Country Comparison | Regional Education Trends | `Global Ranking Score` | ✅ PASS |

**Educational Metrics Result:** 7 / 7 checks passed — **100% pass rate**

---

## 7. Dashboard-Specific Visual Validation

### 7.1 University Overview

| Visual | Result |
|--------|--------|
| Top University Rankings | ✅ PASS |
| Global University Distribution | ✅ PASS |
| Academic Reputation Analysis | ✅ PASS |
| University Performance Trends | ✅ PASS |
| Institutional Comparison | ✅ PASS |
| KPI Cards | ✅ PASS |

---

### 7.2 Research Analytics

| Visual | Result |
|--------|--------|
| Top Research Institutions | ✅ PASS |
| Research Impact Comparison | ✅ PASS |
| Research Output Analysis | ✅ PASS |
| Citation Performance | ✅ PASS |
| Research Productivity Trends | ✅ PASS |
| KPI Cards | ✅ PASS |

---

### 7.3 Student Analytics

| Visual | Result |
|--------|--------|
| International Student Analysis | ✅ PASS |
| Faculty-to-Student Ratio Analysis | ✅ PASS |
| Student Diversity Trends | ✅ PASS |
| Enrollment Comparisons | ✅ PASS |
| Student Distribution Analysis | ✅ PASS |
| KPI Cards | ✅ PASS |

---

### 7.4 Country Comparison

| Visual | Result |
|--------|--------|
| Country Ranking Comparison | ✅ PASS |
| Education Performance Benchmarking | ✅ PASS |
| Regional Education Trends | ✅ PASS |
| Top Performing Countries | ✅ PASS |
| University Distribution | ✅ PASS |
| KPI Cards | ✅ PASS |

---

## 8. QA Summary

| Test Category | Tests Executed | Result |
|---------------|:--------------:|--------|
| KPI Validation | 6 | ✅ PASS |
| Ranking Validation | 3 | ✅ PASS |
| Dashboard Filters | 3 | ✅ PASS |
| Dashboard Cross-linking | 3 | ✅ PASS |
| Parameter Action | 3 | ✅ PASS |
| Navigation | 1 | ✅ PASS |
| Filter Clearing | 1 | ✅ PASS |
| Educational Metrics | 7 | ✅ PASS |
| Dashboard-Specific Visuals | 24 | ✅ PASS |
| **Total** | **51** | **✅ PASS** |

---

## 9. Final QA Status

| Field | Value |
|-------|-------|
| **Final Status** | ✅ **PASS** |
| **Major Issues Identified** | None |
| **KPI Checks Passed** | 6 / 6 (100%) |
| **Overall Test Pass Rate** | 100% |
| **Target (> 95% accuracy)** | ✅ Achieved |

No major dashboard issue was identified during the completed Module 7 testing. The KPI validation covered all six required KPI checks, with 6/6 tested checks passing (100%). All dashboard interactions, cross-linking, parameter actions, navigation flows, and educational metric fields were verified and confirmed correct.

---

*EduVision\_DV — Milestone 4 · Module 7 QA Checklist · Report Date: 2026-09-30*
