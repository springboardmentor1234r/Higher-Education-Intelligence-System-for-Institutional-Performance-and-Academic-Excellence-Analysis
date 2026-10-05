# EduVision_DV Dashboard Testing Report

## 1. Introduction

Testing was performed on the final EduVision_DV Tableau dashboard to
verify that the dashboards, filters, navigation, KPIs, charts, and
interactive features function correctly.

The testing focused on functionality, data display, navigation, and
general dashboard usability.

---

## 2. Dashboards Tested

The following dashboards were tested:

1. University Overview
2. Research Analytics Dashboard
3. Student Analytics Dashboard
4. Country Comparison Dashboard

---

## 3. Functional Testing

| Test ID | Test Case | Expected Result | Status |
|---|---|---|---|
| TC01 | Open University Overview | Dashboard loads correctly | Passed |
| TC02 | Open Research Analytics | Research dashboard opens correctly | Passed |
| TC03 | Open Student Analytics | Student dashboard opens correctly | Passed |
| TC04 | Open Country Comparison | Country dashboard opens correctly | Passed |
| TC05 | Apply University Name filter | Dashboard values update for selected university | Passed |
| TC06 | Apply Country Name filter | Relevant dashboard data updates | Passed |
| TC07 | Apply Region filter | Data is filtered according to selected region | Passed |
| TC08 | Apply Year filter | Data updates according to selected year | Passed |
| TC09 | Navigate between dashboards | Correct dashboard opens | Passed |
| TC10 | Verify University Name synchronization | Selected university remains applied across relevant dashboards | Passed |

---

## 4. KPI Testing

The KPI sections were checked to verify that values are displayed
correctly and respond to the selected filters.

The following KPIs were reviewed:

- Global Ranking Score
- Academic Reputation Score
- Research Impact Score
- Research Productivity Index
- Faculty-Student Ratio
- International Student Percentage

### Result

KPI values were displayed correctly and updated according to the
selected dashboard filters.

**Status: Passed**

---

## 5. Filter Testing

The following filters were tested:

- Region
- Country Name
- University Name
- Overview Year
- Research Year
- Student Year

### Result

The filters were checked to ensure that the relevant charts and KPI
values responded to the selected values.

**Status: Passed**

---

## 6. Dashboard Navigation Testing

Navigation buttons were tested between the four dashboards.

The following navigation paths were checked:

- University Overview → Research Analytics
- University Overview → Student Analytics
- University Overview → Country Comparison
- Research Analytics → University Overview
- Research Analytics → Student Analytics
- Research Analytics → Country Comparison
- Student Analytics → University Overview
- Student Analytics → Research Analytics
- Student Analytics → Country Comparison
- Country Comparison → University Overview
- Country Comparison → Research Analytics
- Country Comparison → Student Analytics

### Result

The navigation buttons opened the intended dashboards correctly.

**Status: Passed**

---

## 7. Cross-Dashboard Filter Testing

The University Name filter was specifically tested for
cross-dashboard synchronization.

A university was selected on the University Overview dashboard and the
Research Analytics dashboard was opened.

The selected university remained applied and the corresponding KPI
values changed according to the selected university.

The filter state was also retained when navigating back to the
University Overview dashboard.

### Result

Cross-dashboard filter synchronization worked correctly.

**Status: Passed**

---

## 8. Null Value Testing

The Research Analytics dashboard was reviewed for unwanted null values
in the research visualizations.

The identified null-value issue was investigated and cleared during
dashboard development.

### Result

The relevant research visualization was reviewed after the correction.

**Status: Passed**

---

## 9. Visual Testing

The final dashboards were reviewed for:

- Dashboard titles
- KPI visibility
- Chart visibility
- Filter placement
- Navigation button placement
- Layout consistency
- Text readability
- Overall dashboard appearance

### Result

The dashboards were visually reviewed after the final formatting and
layout adjustments.

**Status: Passed**

---

## 10. Final Workbook Testing

The final Tableau workbook was reviewed after completing the dashboard
development and formatting.

The workbook was saved as:

`EduVision_DV.twbx`

The final workbook contains all four completed dashboards.

**Status: Passed**

---

## 11. Overall Testing Result

All major functional and visual tests performed on the final
EduVision_DV dashboard were successful.

The dashboard was considered ready for final project submission after
completion of the testing and review process.
