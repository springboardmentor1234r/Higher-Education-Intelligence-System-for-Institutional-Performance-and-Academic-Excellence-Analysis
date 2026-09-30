# Dashboard Testing Report — Module 7: Testing & Validation

---

## 1. Executive Summary

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Module** | Module 7 — Testing & Validation |
| **Workbook** | `EduVision_DV.twbx` |
| **Report Date** | 2026-09-30 |
| **Prepared By** | EduVision QA Team |
| **Document Version** | v1.0 |
| **Final Status** | ✅ PASS |

Module 7 focused on systematic testing and validation of the EduVision\_DV higher education dashboard suite. Testing was conducted across the integrated Tableau workbook, covering all four interconnected dashboards as a unified system rather than as independent components.

**Testing scope covered:**

- ☑ KPI calculations
- ☑ Ranking calculations
- ☑ Dashboard filters and interactions
- ☑ Dashboard-to-dashboard linking
- ☑ Parameter actions
- ☑ Navigation
- ☑ Filter clearing
- ☑ Educational metric field correctness
- ☑ Dashboard-specific visualizations

All completed tests passed. No major dashboard issue was identified.

---

## 2. Dashboard Suite Tested

The following four interconnected dashboards were tested as an integrated workbook:

| # | Dashboard | Purpose |
|---|-----------|---------|
| 1 | **University Overview** | Institutional rankings, reputation, and performance trends |
| 2 | **Research Analytics** | Research impact, citation performance, and productivity |
| 3 | **Student Analytics** | International students, faculty ratios, and diversity |
| 4 | **Country Comparison** | Country-level benchmarking and regional education trends |

---

## 3. KPI Testing

### 3.1 KPIs Validated

| # | KPI | Result |
|---|-----|--------|
| 1 | Global Ranking Score | ✅ PASS |
| 2 | Research Impact Score | ✅ PASS |
| 3 | Faculty-to-Student Ratio | ✅ PASS |
| 4 | International Student Percentage | ✅ PASS |
| 5 | Academic Reputation Score | ✅ PASS |
| 6 | Research Productivity Index | ✅ PASS |

**KPI Test Coverage:** 6 / 6 tested KPI checks passed — **100% pass rate**

### 3.2 Key Observation

> Missing KPI values are correctly preserved as null and are **not** incorrectly converted to zero values. This was confirmed during source field inspection.

---

## 4. Ranking Testing

Ranking data was validated using three fields from the `kpi_summary` sheet:

- `global_rank`
- `normalized_rank`
- `global_ranking_score`

### 4.1 Validation Criteria

| Check | Expected Behaviour |
|-------|--------------------|
| Rank ordering | Lower rank number = higher institutional position |
| Normalized rank | Consistent and aligned with `global_rank` |
| Score directionality | `global_ranking_score` decreases as rank number increases |

### 4.2 Sample Ranking Validation Data

| Global Rank | Normalized Rank | Global Ranking Score |
|:-----------:|:---------------:|:--------------------:|
| 1 | 1 | 100.00 |
| 2 | 2 | 99.93 |
| 3 | 3 | 99.87 |
| 4 | 4 | 99.80 |
| 5 | 5 | 99.73 |

All tested records demonstrated the expected relationship between rank position and ranking score.

**Ranking Validation Result:** ✅ PASS

---

## 5. Dashboard Interaction Testing

### 5.1 Filters

The following filters were tested individually on their respective dashboards:

| Filter | Dashboard | Behaviour Verified | Result |
|--------|-----------|--------------------|--------|
| University Name | University Overview | KPI cards and charts updated to selected university | ✅ PASS |
| Country | Country Comparison | Visualizations updated to selected country | ✅ PASS |
| Region | Country Comparison | Regional Education Trends responded correctly | ✅ PASS |
| Ranking Year | Country Comparison | Visualizations updated to selected year | ✅ PASS |

---

### 5.2 Dashboard-to-Dashboard Linking

The following cross-dashboard linking sequence was tested:

**University Overview → Research Analytics → Student Analytics → Country Comparison**

| Link | Data Passed | Result |
|------|-------------|--------|
| University Overview → Research Analytics | Selected university | ✅ PASS |
| Research Analytics → Student Analytics | Selected university | ✅ PASS |
| Student Analytics → Country Comparison | University's country | ✅ PASS |

---

### 5.3 Parameter Action — Performance Metric

The **Performance Metric** parameter was tested with all three available options:

| Parameter Value | Effect on Country Ranking Comparison Chart | Result |
|-----------------|---------------------------------------------|--------|
| Ranking Score | Chart updated correctly | ✅ PASS |
| Overall Score | Chart updated correctly | ✅ PASS |
| Research Impact Score | Chart updated correctly | ✅ PASS |

---

### 5.4 Navigation

The full navigation loop was tested:

**University Overview → Research Analytics → Student Analytics → Country Comparison → University Overview**

All navigation controls functioned correctly. No broken links or layout failures were encountered.

**Result:** ✅ PASS

---

### 5.5 Filter Clearing

- University selection was cleared on University Overview
- Research Analytics correctly reverted to displaying **all universities** rather than retaining the previously selected university

**Result:** ✅ PASS

---

## 6. Educational Metric Validation

Field mappings were verified to confirm each dashboard metric references the correct source field.

| Dashboard | Metric | Verified Source Field | Result |
|-----------|--------|-----------------------|--------|
| Student Analytics | Faculty-to-Student Ratio | `Faculty To Student Ratio` | ✅ PASS |
| Student Analytics | International Student Percentage | `International Student Percentage` | ✅ PASS |
| Student Analytics | Student Diversity | `Female Percentage` | ✅ PASS |
| Research Analytics | Research Impact | `Research Impact Score` | ✅ PASS |
| Research Analytics | Citation Performance | `Citations Score` | ✅ PASS |
| Research Analytics | Research Productivity | `Research Productivity Index` | ✅ PASS |
| Country Comparison | Regional Education Trends | `Global Ranking Score` | ✅ PASS |
| Country Comparison | Top Performing Countries | `Overall Score` | ✅ PASS |

**Educational Metrics Result:** 8 / 8 field mappings verified — **100% pass rate**

---

## 7. Dashboard Visual Validation Results

### 7.1 University Overview

| Visual | Result |
|--------|--------|
| Top University Rankings | ✅ PASS |
| Global University Distribution | ✅ PASS |
| Academic Reputation Analysis | ✅ PASS |
| University Performance Trends | ✅ PASS |
| Institutional Comparison | ✅ PASS |
| KPI Cards | ✅ PASS |

**Dashboard Result:** ✅ PASS

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

**Dashboard Result:** ✅ PASS

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

**Dashboard Result:** ✅ PASS

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

**Dashboard Result:** ✅ PASS

---

## 8. Issues Identified and Resolved During Testing

The following issues were identified during the development and testing process and corrected prior to final validation. All corresponding tests passed after corrections were applied.

| # | Issue | Correction Applied | Status |
|---|-------|--------------------|--------|
| 1 | Research Impact Score was being aggregated as a **sum** | Aggregation changed to **average** | ✅ Resolved |
| 2 | Ranking chart axis was set to a fixed custom range | Axis changed to **automatic range** | ✅ Resolved |
| 3 | Student Diversity Trends displayed percentage values as multiplied (e.g. 45 as 4500%) | Percentage format corrected | ✅ Resolved |
| 4 | Research Analytics retained previous university selection after filter was cleared | Action-filter clearing behaviour corrected to show all universities | ✅ Resolved |
| 5 | Dashboard charts contained excessive marks causing performance issues | Charts limited to appropriate **Top 10** views where required | ✅ Resolved |
| 6 | Regional Education Trends contained unnecessary mark labels and null region values | Mark labels removed; null regions excluded | ✅ Resolved |

> No issues remained unresolved at the time of final validation.

---

## 9. Final Test Results Summary

| Test Area | Tests Executed | Result |
|-----------|:--------------:|--------|
| KPI Calculations | 6 | ✅ PASS |
| Ranking Calculations | 3 | ✅ PASS |
| Dashboard Filters | 4 | ✅ PASS |
| Dashboard Linking | 3 | ✅ PASS |
| Parameter Actions | 3 | ✅ PASS |
| Navigation | 1 | ✅ PASS |
| Filter Clearing | 1 | ✅ PASS |
| Educational Metrics | 8 | ✅ PASS |
| Dashboard Visuals | 24 | ✅ PASS |
| **Total** | **53** | **✅ PASS** |

---

## 10. Conclusion

| Field | Value |
|-------|-------|
| **Final Module 7 Status** | ✅ **PASS** |
| **Major Issues Identified** | None |
| **KPI Checks Passed** | 6 / 6 (100%) |
| **Overall Test Pass Rate** | 100% |
| **Evaluation Target (> 95%)** | ✅ Achieved |

The EduVision\_DV Tableau dashboard suite successfully completed all Module 7 testing activities. All four dashboards are correctly integrated, navigation is fully functional, filters and cross-dashboard links performed as expected, the parameter action was verified across all options, and all required educational metric field mappings were confirmed correct.

Six issues identified during the development and testing cycle were corrected prior to final validation, none of which constituted a major dashboard failure in the final tested state.

**Final Module 7 Status: PASS**
**KPI Validation: 6 / 6 tested checks passed (100%)**

---

*EduVision\_DV — Milestone 4 · Module 7 Dashboard Testing Report · Report Date: 2026-09-30*
