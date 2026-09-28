# EduVision DV – QA Checklist

## Milestone 4: Testing and Validation

**Project:** EduVision_DV – Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis  
**Workbook:** `EduVision_DV.twbx`  
**Tester:** Mohammad Saad  
**Date:** 26 September 2026

### Scope

This checklist follows the mentor's Milestone 4 requirements:
- Validate KPI calculations
- Verify ranking calculations
- Test dashboard interactions
- Validate educational metrics
- Check for major dashboard issues

---

## 1. Workbook Structure Validation

| Test ID | Check | Result | Status |
|---|---|---|---|
| STR-01 | Four required dashboards exist | University Overview, Research Analytics, Students Analytics, Country Comparison | PASS |
| STR-02 | University Overview worksheets present | KPI cards and required analytical visuals are present | PASS |
| STR-03 | Research Analytics worksheets present | Research, citation, teaching, outlook and student-staff visuals are present | PASS |
| STR-04 | Students Analytics worksheets present | Student population, diversity and ratio visuals are present | PASS |
| STR-05 | Country Comparison worksheets present | Country education indicators and comparison visuals are present | PASS |
| STR-06 | Workbook opens as packaged `.twbx` | Packaged Tableau workbook inspected successfully | PASS |

---

## 2. KPI Calculation / Definition Validation

The workbook was structurally inspected to confirm that KPI worksheets use the intended fields.

| Test ID | Dashboard | KPI / Measure | Source field found | Status |
|---|---|---|---|---|
| KPI-01 | University Overview | Overall Score | `Overall Score` | PASS |
| KPI-02 | University Overview | Academic Reputation Score | `Academic Reputation` | PASS |
| KPI-03 | University Overview | Research Impact Score | `Citations Per Faculty Score` | PASS |
| KPI-04 | University Overview | Student Per Staff Ratio | `Student Staff Ratio` | PASS |
| KPI-05 | University Overview | International Student Percentage | `International Students Percentage` | PASS |
| KPI-06 | University Overview | Global Ranking | `Rank 2025 Numeric` | PASS |
| KPI-07 | Research Analytics | Research Score | `Scores Research` | PASS |
| KPI-08 | Research Analytics | Citations Score | `Scores Citations` | PASS |
| KPI-09 | Research Analytics | Student–Staff Ratio | `Student Staff Ratio` | PASS |
| KPI-10 | Research Analytics | International Students % | `International Students Percentage` | PASS |
| KPI-11 | Students Analytics | Total Students | `Total Students` | PASS |
| KPI-12 | Students Analytics | Student Staff Ratio | `Student Staff Ratio` | PASS |
| KPI-13 | Students Analytics | International Students Percentage | `International Students Percentage` | PASS |
| KPI-14 | Students Analytics | Female Students % | `Female Pct` | PASS |
| KPI-15 | Country Comparison | Education Expenditure % GDP | Country `Value` for indicator | PASS |
| KPI-16 | Country Comparison | Tertiary Enrollment | Country `Value` for indicator | PASS |
| KPI-17 | Country Comparison | Adult Literacy Rate | Country `Value` for indicator | PASS |
| KPI-18 | Country Comparison | Primary Completion Rate | Country `Value` for indicator | PASS |
| KPI-19 | Country Comparison | Tertiary Teachers | Country `Value` for indicator | PASS |
| KPI-20 | Country Comparison | GDP per Capita | Country `Value` for indicator | PASS |

**Important:** Structural verification confirms the configured fields and worksheet definitions. A numerical accuracy percentage against the original source rows was not independently recomputed from the packaged Hyper extracts in this environment, so no unsupported “>95% accuracy” claim is made here.

---

## 3. Ranking Validation

| Test ID | Check | Result | Status |
|---|---|---|---|
| RANK-01 | University ranking uses `Rank 2025 Numeric` | Confirmed in ranking worksheets | PASS |
| RANK-02 | Top University Rankings worksheet exists | Confirmed | PASS |
| RANK-03 | Country ranking worksheets exist | Six country ranking/comparison worksheets confirmed | PASS |
| RANK-04 | Ranking visuals contain university/country dimensions | Confirmed | PASS |
| RANK-05 | Ranking values are available as numeric fields where required | Confirmed for QS numeric rank | PASS |

---

## 4. Dashboard Navigation Validation

| Test ID | Check | Result | Status |
|---|---|---|---|
| NAV-01 | University Overview navigation buttons | Four dashboard navigation buttons configured | PASS |
| NAV-02 | Research Analytics navigation buttons | Four dashboard navigation buttons configured | PASS |
| NAV-03 | Students Analytics navigation buttons | Four dashboard navigation buttons configured | PASS |
| NAV-04 | Country Comparison navigation buttons | Four dashboard navigation buttons configured | PASS |

The workbook contains dashboard navigation button actions connecting the four dashboard destinations.

---

## 5. Dashboard Interaction Validation

The workbook contains generated filter actions for the analytical sheets.

| Test ID | Check | Result | Status |
|---|---|---|---|
| INT-01 | University Overview visual selection actions | Configured | PASS |
| INT-02 | Research Analytics visual selection actions | Configured | PASS |
| INT-03 | Students Analytics visual selection actions | Configured | PASS |
| INT-04 | Country Comparison visual/filter structure | Configured | PASS |
| INT-05 | Filter actions have automatic clear behavior | Confirmed in workbook action definitions | PASS |

### Known interaction note

The current workbook contains generated **“Use as Filter”** actions whose target is the dashboard. Such actions can cause KPI cards to become blank when a visual selection removes all records represented by a KPI. This behavior has already been observed during project testing.

This should be treated as a **known interaction limitation** and reviewed in Tableau before claiming a completely issue-free final release. The workbook's navigation itself has been confirmed working during project testing.

---

## 6. Educational Metrics Validation

| Test ID | Metric area | Result | Status |
|---|---|---|---|
| EDU-01 | Education expenditure | Country Comparison worksheet present | PASS |
| EDU-02 | Tertiary enrollment | Country Comparison worksheet present | PASS |
| EDU-03 | Adult literacy | Country Comparison worksheet present | PASS |
| EDU-04 | Primary completion | Country Comparison worksheet present | PASS |
| EDU-05 | Tertiary teachers | Country Comparison worksheet present | PASS |
| EDU-06 | GDP per capita | Country Comparison worksheet present | PASS |
| EDU-07 | Total students | Students Analytics worksheet present | PASS |
| EDU-08 | Student-staff ratio | Student/Research worksheets present | PASS |
| EDU-09 | International student percentage | Student/Research worksheets present | PASS |
| EDU-10 | Female student percentage | Students Analytics worksheet present | PASS |

---

## 7. Visual / Layout QA

| Test ID | Check | Status |
|---|---|---|
| QA-01 | Four dashboard titles present | PASS |
| QA-02 | KPI cards present | PASS |
| QA-03 | Required analytical visuals present | PASS |
| QA-04 | Navigation controls present | PASS |
| QA-05 | Dashboard background/branding assets packaged | PASS |
| QA-06 | Workbook contains no missing dashboard definition | PASS |
| QA-07 | Workbook is packaged as `.twbx` | PASS |

---

## QA Summary

**Structural workbook validation:** PASS  
**KPI field/definition validation:** PASS  
**Ranking structure validation:** PASS  
**Navigation configuration:** PASS  
**Educational metric coverage:** PASS  
**Known interaction issue:** KPI cards can become blank under some dashboard-level visual filter selections.

### Final QA status

**CONDITIONAL PASS – one interaction behavior requires final Tableau review before declaring the workbook completely issue-free.**

This status is intentionally conservative and does not claim a numerical KPI accuracy percentage that was not independently recomputed from the packaged Hyper data.
