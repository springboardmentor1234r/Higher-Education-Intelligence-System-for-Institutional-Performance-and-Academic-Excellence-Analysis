# EduVision – Dashboard Testing Report

## Module 7: Testing and Validation

### Project

Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

---

## 1. Testing Objective

The objective of Module 7 testing was to verify the correctness, functionality, and reliability of the EduVision analytical system.

The testing covered:

- KPI calculations
- Ranking calculations
- Dashboard filters
- Dashboard navigation
- Dashboard actions
- Parameter actions
- Educational metrics
- Country-level World Bank linkage
- Data quality

---

## 2. Testing Environment

| Component | Technology |
|---|---|
| Data Processing | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Tableau Desktop |
| Dashboard Integration | Tableau Filters, Parameters and Actions |
| Primary Analytical Dataset | University KPI Dataset |
| Country Education Data | World Bank Education Statistics |
| Operating System | Windows |

---

## 3. KPI Calculation Validation

Six KPIs were validated during testing.

| KPI | Validation Result |
|---|---|
| Global Ranking Score | PASS |
| Research Impact Score | PASS |
| Faculty-to-Student Ratio Score | PASS |
| International Student Percentage | PASS |
| Academic Reputation Score | PASS |
| Research Productivity Index | PASS |

### KPI Average Validation

The Python-generated KPI dataset produced:

| KPI | Average |
|---|---:|
| Global Ranking Score | 41.84 |
| Research Impact Score | 23.50 |
| Academic Reputation Score | 20.29 |

These values matched the corresponding Tableau dashboard KPI values.

Additional KPI checks confirmed valid ranges for the derived scores and international student percentage.

---

## 4. Ranking Calculation Validation

The ranking worksheets were checked against the Python-generated KPI dataset.

### Global Ranking Score

The Tableau ranking was verified against the descending Python calculation.

The top results included:

1. Massachusetts Institute of Technology (MIT) – 100.0
2. Imperial College London – 98.5
3. University of Oxford – 96.9
4. Harvard University – 96.8
5. University of Cambridge – 96.7
6. Stanford University – 96.1
7. ETH Zurich – 93.9
8. National University of Singapore (NUS) – 93.7
9. UCL – 91.6
10. California Institute of Technology (Caltech) – 90.9

### Other Ranking Tests

The following were also validated:

- Top Universities by Academic Reputation
- Top Universities by QS Citations per Faculty
- Ranking values against source data
- Ranking response to dashboard filters

All ranking tests passed.

---

## 5. Dashboard Interaction Testing

All 12 dashboard interaction tests passed.

| Test | Result |
|---|---|
| Country filter | PASS |
| Region filter | PASS |
| Income Group filter | PASS |
| University filter | PASS |
| Year filter | PASS |
| University Overview → Research Analytics | PASS |
| Research Analytics → Student Analytics | PASS |
| Student Analytics → Country Comparison | PASS |
| Country Comparison → University Overview | PASS |
| Country map/dashboard action | PASS |
| Student Year Parameter Action | PASS |
| Clear filters | PASS |

The dashboard navigation and interaction mechanisms were tested successfully across the four integrated dashboards.

---

## 6. Educational Metrics Validation

The Country Comparison dashboard was tested for the following World Bank education indicators:

| Educational Metric | Result |
|---|---|
| Tertiary Enrollment Ratio | PASS |
| Tertiary Graduation Ratio | PASS |
| Female Tertiary Students % | PASS |
| Tertiary Pupil-Teacher Ratio | PASS |
| Youth Literacy 15–24 % | PASS |
| Tertiary Graduates | PASS |
| Country Linkage | PASS |
| Regional Comparison | PASS |

The dashboard displayed populated country-level values for the World Bank education indicators.

The World Bank country linkage achieved 98.19% linkage, with 3,466 of 3,530 university records linked.

---

## 7. Data Quality Validation

The following data-quality checks were completed:

| Check | Result |
|---|---|
| Duplicate university IDs | PASS |
| Missing university IDs | PASS |
| Row count preservation | PASS |
| World Bank linkage | PASS |
| Invalid international student percentages | PASS |

The final integrated dataset maintained 3,530 university records and contained no duplicate or missing university IDs.

---

## 8. Issues Identified and Resolved

### Issue 1 – Country Relationship

Initially, the World Bank country charts displayed Null values because the Tableau relationship used the incorrect country-code field.

**Resolution:**  
The relationship was corrected to:

`dim_university.Wb Country Code → fact_country_education.Country Code`

After correction, the World Bank country values appeared correctly.

### Issue 2 – Ranking Sort

The Global Ranking Score worksheet initially did not display the intended descending ranking order.

**Resolution:**  
The worksheet was configured to sort by:

`Global Ranking Score → Average → Descending`

### Issue 3 – Academic Reputation Worksheet

The Academic Reputation ranking worksheet initially contained leftover filtering conditions.

**Resolution:**  
The filters were cleared and the Top 10 filter was applied correctly.

### Issue 4 – Research Ranking Field

The research ranking worksheet initially used an incorrect citation field.

**Resolution:**  
The worksheet was corrected to use:

`Research Impact Score`

with descending average aggregation.

### Issue 5 – Country Filter Visibility

The Country Name filter existed at worksheet level but was initially not visible on the dashboard.

**Resolution:**  
The Country Name filter was added to the University Overview dashboard and successfully tested.

---

## 9. Testing Limitations

### Publications Analysis

Publications Analysis was not directly implemented because the integrated research dataset does not contain a publication-count metric.

Research performance is instead analyzed using research score, citation score, citations per faculty, and research productivity indicators.

### Enrollment Comparisons

Total student enrollment and international student counts were not available in the integrated dataset.

Therefore, Student Analytics uses the available indicators such as international student percentage and students per staff.

### Regional Education Trends

Regional education analysis uses World Bank 2015 education indicators.

Therefore, the regional comparison represents a cross-region comparison rather than a temporal trend.

### Ranking Data Completeness

Some QS and THE ranking datasets contain missing or banded ranking values. Missing ranking values were not treated as zero or as poor performance.

---

## 10. Final QA Result

**Overall Status: PASS**

All planned Module 7 testing activities were completed.

The testing confirmed:

- KPI calculations are consistent with the generated analytical dataset.
- Ranking calculations and sorting operate correctly.
- Dashboard filters and interactions work correctly.
- Navigation between the four dashboards works correctly.
- Parameter actions work correctly.
- World Bank educational metrics are displayed in the Country Comparison dashboard.
- Data-quality checks passed.
- No major dashboard issues remained after testing.

---

## 11. Conclusion

Module 7 successfully validated the EduVision dashboard suite and its underlying analytical outputs.

The system is ready to proceed to **Module 8: Documentation and Project Delivery**.