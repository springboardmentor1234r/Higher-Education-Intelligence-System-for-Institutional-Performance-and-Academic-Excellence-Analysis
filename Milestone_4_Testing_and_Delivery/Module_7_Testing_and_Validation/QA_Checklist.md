# EduVision – QA Checklist

## Module 7: Testing and Validation

### Project
Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

---

## 1. KPI Calculation Validation

| Test ID | KPI | Validation Method | Expected Result | Status |
|---|---|---|---|---|
| T01.1 | Global Ranking Score | Compare Tableau value with Python calculation | 41.84 average | PASS |
| T01.2 | Research Impact Score | Compare Tableau value with Python calculation | 23.50 average | PASS |
| T01.3 | Academic Reputation Score | Compare Tableau value with Python calculation | 20.29 average | PASS |
| T01.4 | Faculty-to-Student Ratio Score | Verify derived percentile calculation | Valid 0–100 score | PASS |
| T01.5 | International Student Percentage | Verify source values and range | 0–100% | PASS |
| T01.6 | Research Productivity Index | Verify weighted calculation | Valid 0–100 score | PASS |

---

## 2. Ranking Calculation Validation

| Test ID | Test | Expected Result | Status |
|---|---|---|---|
| T02.1 | Top Universities by Global Ranking Score | Universities ordered by descending score | PASS |
| T02.2 | Top Universities by Academic Reputation | Universities ordered by descending academic reputation score | PASS |
| T02.3 | Top Universities by QS Citations per Faculty | Universities ordered by descending citation score | PASS |
| T02.4 | Ranking values compared with source data | Values match source dataset | PASS |
| T02.5 | Ranking filters | Ranking updates when filters are applied | PASS |

---

## 3. Dashboard Interaction Testing

| Test ID | Test | Expected Result | Status |
|---|---|---|---|
| T03.1 | Country filter | Dashboard updates for selected country | PASS |
| T03.2 | Region filter | Dashboard updates for selected region | PASS |
| T03.3 | Income Group filter | Dashboard updates for selected income group | PASS |
| T03.4 | University filter | Dashboard updates for selected university | PASS |
| T03.5 | Year filter | Dashboard updates for selected year | PASS |
| T03.6 | University Overview → Research Analytics | Navigation works | PASS |
| T03.7 | Research Analytics → Student Analytics | Navigation works | PASS |
| T03.8 | Student Analytics → Country Comparison | Navigation works | PASS|
| T03.9 | Country Comparison → University Overview | Navigation works | PASS |
| T03.10 | Country map/dashboard action | Selecting country filters related views | PASS |
| T03.11 | Student Year Parameter Action | Selecting year changes Selected Year parameter | PASS |
| T03.12 | Clear filters | Dashboard returns to all values | PASS |

---

## 4. Educational Metrics Validation

| Test ID | Metric | Expected Result | Status |
|---|---|---|---|
| T04.1 | Tertiary Enrollment Ratio | Values displayed correctly | PASS |
| T04.2 | Tertiary Graduation Ratio | Values displayed correctly | PASS |
| T04.3 | Female Tertiary Students % | Values displayed correctly | PASS |
| T04.4 | Tertiary Pupil-Teacher Ratio | Values displayed correctly | PASS |
| T04.5 | Youth Literacy 15–24 % | Values displayed correctly | PASS |
| T04.6 | Tertiary Graduates | Values displayed correctly | PASS |
| T04.7 | Country linkage | World Bank values linked to correct countries | PASS |
| T04.8 | Regional comparison | Regional education comparison displays correctly | PASS |

---

## 5. Data Quality Checks

| Test ID | Check | Expected Result | Status |
|---|---|---|---|
| T05.1 | Duplicate university IDs | No duplicates | PASS |
| T05.2 | Missing university IDs | No missing IDs | PASS |
| T05.3 | Row count preservation | 3,530 university records maintained | PASS |
| T05.4 | World Bank linkage | 98.19% linked | PASS |
| T05.5 | Invalid international student percentages | No invalid values | PASS |

---

## 6. Final QA Result

**Overall Status:** PASS

### Testing Summary

- KPI calculation validation: PASS
- Ranking calculation validation: PASS
- Dashboard interaction testing: PASS
- Educational metrics validation: PASS
- Data quality checks: PASS

### Overall Result

All Module 7 testing and validation checks have been completed successfully.

No major dashboard issues were identified during testing. KPI values were validated against the Python-generated KPI dataset, dashboard interactions were tested, and educational metrics were verified in the Country Comparison dashboard.