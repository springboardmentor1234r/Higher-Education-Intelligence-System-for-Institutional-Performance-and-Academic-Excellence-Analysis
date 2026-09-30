# EduVision\_DV — Dashboard Guide

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Document** | Dashboard Guide & User Reference |
| **Workbook** | `EduVision_DV.twbx` |
| **Report Date** | 2026-09-30 |
| **Document Version** | v1.0 |

---

## 1. Overview

EduVision\_DV is a unified Tableau dashboard suite for analysing higher-education performance across institutions, research output, student indicators, and country-level education trends.

The workbook contains **four interconnected dashboards**:

| # | Dashboard | Primary Focus |
|---|-----------|---------------|
| 1 | **University Overview** | Institutional rankings, reputation, and overall performance |
| 2 | **Research Analytics** | Research impact, citations, and productivity |
| 3 | **Student Analytics** | Internationalization, faculty ratios, diversity, and enrolment |
| 4 | **Country Comparison** | Country-level benchmarking and regional education trends |

The dashboards share common dimensions — **University**, **Country**, **Region**, and **Ranking Year** — and are connected through Tableau navigation buttons, dashboard actions, filters, and parameters, forming a cohesive analytical experience.

---

## 2. Dashboard Navigation Map

```
┌─────────────────────┐
│  University Overview │  ← Main landing dashboard
└────────┬────────────┘
         │ Navigate + pass university selection
    ┌────▼─────────────┐
    │ Research Analytics│
    └────┬──────────────┘
         │ Navigate + pass university selection
    ┌────▼─────────────┐
    │ Student Analytics │
    └────┬──────────────┘
         │ Navigate + pass country
    ┌────▼──────────────┐
    │ Country Comparison │
    └────┬───────────────┘
         │ Navigate back
    ┌────▼─────────────┐
    │ University Overview│
    └───────────────────┘
```

---

## 3. University Overview

### 3.1 Purpose

**University Overview** is the main landing dashboard of the EduVision\_DV workbook. It provides a high-level view of global university rankings, academic reputation, overall performance scores, and geographic distribution across countries.

### 3.2 KPI Cards

| KPI Card | Metric Displayed |
|----------|-----------------|
| Total Universities | Count of universities in the current filter context |
| Average Global Ranking Score | Mean normalized ranking score (0–100) |
| Average Overall Score | Mean composite overall performance score |
| Total Countries | Count of distinct countries in the current filter context |

### 3.3 Visualizations

| Visual | Description |
|--------|-------------|
| **Top University Rankings** | Ranked list or bar chart of top universities by Global Ranking Score |
| **Global University Distribution** | Geographic map or chart showing university distribution across countries |
| **Academic Reputation Analysis** | Comparison of Academic Reputation Scores across institutions |
| **University Performance Trends** | Overall performance score trends across ranking years |
| **Institutional Comparison** | Side-by-side comparison of overall performance across universities |

### 3.4 Filters

| Filter | Scope |
|--------|-------|
| University | Filter to a specific institution |
| Country | Filter to a specific country |
| Region | Filter to a geographic region |
| Ranking Year | Filter to a specific ranking year |

### 3.5 Navigation & Linking

| Action | Destination | Data Passed |
|--------|-------------|-------------|
| Navigate to Research Analytics | Research Analytics | Selected university |
| Navigate to Student Analytics | Student Analytics | — |
| Navigate to Country Comparison | Country Comparison | — |

---

## 4. Research Analytics

### 4.1 Purpose

**Research Analytics** focuses on university research performance — citation influence, research impact, and research productivity. It enables users to identify the strongest research institutions and track research trends over time.

### 4.2 KPI Cards

| KPI Card | Metric Displayed |
|----------|-----------------|
| Average Research Impact Score | Mean Research Impact Score (0–100) |
| Average Citations Score | Mean citation performance score |
| Average Research Productivity | Mean Research Productivity Index (0–100) |
| Average Research Score | Mean overall research environment score |

### 4.3 Visualizations

| Visual | Description |
|--------|-------------|
| **Top Research Institutions** | Universities ranked by research performance |
| **Research Impact Comparison** | Comparison of Research Impact Score across institutions |
| **Research Output Analysis** | Research Score used as the research-output analytical measure. No publication-count field exists in the source data; publication counts are not fabricated |
| **Citation Performance** | Citation performance using Citations Score |
| **Research Productivity Trends** | Research Productivity Index tracked across ranking years |

### 4.4 Filters

| Filter | Scope |
|--------|-------|
| University | Filter to a specific institution |
| Country | Filter to a specific country |
| Ranking Year | Filter to a specific ranking year |

### 4.5 Navigation & Linking

| Action | Destination | Data Passed |
|--------|-------------|-------------|
| Receives university from University Overview | — | Selected university (passed in) |
| Navigate to Student Analytics | Student Analytics | Selected university |
| Navigate to University Overview | University Overview | — |

---

## 5. Student Analytics

### 5.1 Purpose

**Student Analytics** focuses on student population characteristics — international student share, faculty-to-student ratios, gender diversity, enrolment size, and student geographic distribution.

### 5.2 KPI Cards

| KPI Card | Metric Displayed |
|----------|-----------------|
| Average International Student Percentage | Mean % of international students enrolled |
| Average Faculty-to-Student Ratio | Mean students per academic staff member |
| Average Female Percentage | Mean % of female students |
| Average Number of Students | Mean total student enrolment |

### 5.3 Visualizations

| Visual | Description |
|--------|-------------|
| **International Student Analysis** | Percentage of international students across institutions |
| **Faculty-to-Student Ratio Analysis** | Actual Faculty-to-Student Ratio comparison across institutions |
| **Student Diversity Trends** | Female student percentage trends across ranking years |
| **Enrollment Comparisons** | Total student enrolment comparison across universities |
| **Student Distribution Analysis** | Student distribution across countries |

### 5.4 Filters

| Filter | Scope |
|--------|-------|
| University | Filter to a specific institution |
| Country | Filter to a specific country |
| Ranking Year | Filter to a specific ranking year |

### 5.5 Navigation & Linking

| Action | Destination | Data Passed |
|--------|-------------|-------------|
| Receives university from Research Analytics | — | Selected university (passed in) |
| Navigate to Country Comparison | Country Comparison | University's country |
| Navigate to University Overview | University Overview | — |

---

## 6. Country Comparison

### 6.1 Purpose

**Country Comparison** operates at the **country level** rather than the institution level. It benchmarks countries against each other using aggregated university performance indicators and regional education trends.

### 6.2 KPI Cards

| KPI Card | Metric Displayed |
|----------|-----------------|
| Average Global Ranking Score | Mean normalized ranking score for universities in the selected country |
| Average Overall Score | Mean overall composite score |
| Average Research Impact Score | Mean Research Impact Score |
| Average International Student Percentage | Mean % of international students |

### 6.3 Visualizations

| Visual | Description |
|--------|-------------|
| **Country Ranking Comparison** | Compares countries using a user-selected performance metric (controlled by the Performance Metric parameter) |
| **Education Performance Benchmarking** | Country comparison using Research Impact Score |
| **Regional Education Trends** | Global Ranking Score trends by geographic region across ranking years |
| **Top Performing Countries** | Countries with the highest Overall Score |
| **University Distribution** | Number or distribution of universities per selected country |

### 6.4 Filters

| Filter | Scope |
|--------|-------|
| Country | Filter to a specific country |
| Region | Filter to a geographic region |
| Ranking Year | Filter to a specific ranking year |
| University | Filter to a specific institution |

### 6.5 Parameter — Performance Metric

The **Performance Metric** parameter allows users to dynamically change the metric displayed in the **Country Ranking Comparison** chart without modifying the dashboard.

| Parameter Value | Effect |
|-----------------|--------|
| Ranking Score | Country Ranking Comparison displays Global Ranking Score |
| Overall Score | Country Ranking Comparison displays Overall Score |
| Research Impact Score | Country Ranking Comparison displays Research Impact Score |

### 6.6 Navigation & Linking

| Action | Destination | Data Passed |
|--------|-------------|-------------|
| Receives country from Student Analytics | — | University's country (passed in) |
| Navigate to University Overview | University Overview | — |

---

## 7. Cross-Dashboard Linking Summary

The dashboards form an integrated analytical journey through a consistent linking chain:

| From | To | Trigger | Data Passed |
|------|----|---------|-------------|
| University Overview | Research Analytics | Navigation button + university selection | Selected university |
| Research Analytics | Student Analytics | Navigation button + university selection | Selected university |
| Student Analytics | Country Comparison | Navigation button | University's country |
| Any dashboard | University Overview | Navigation button | — |

### Filter Clearing Behaviour

When the university selection is cleared on **University Overview**, the **Research Analytics** dashboard resets to display all universities rather than retaining the previously selected institution.

---

## 8. Shared Dimensions

All four dashboards operate on a common set of dimensions:

| Dimension | Description |
|-----------|-------------|
| **University** | Institution name — primary identifier |
| **Country** | Country of institution |
| **Region** | Geographic region grouping |
| **Ranking Year** | Year of the ranking data record |

---

## 9. Dashboard × KPI Reference

| KPI | University Overview | Research Analytics | Student Analytics | Country Comparison |
|-----|:------------------:|:-----------------:|:----------------:|:-----------------:|
| Global Ranking Score | ✅ | | | ✅ |
| Research Impact Score | | ✅ | | ✅ |
| Faculty-to-Student Ratio | | | ✅ | |
| International Student Percentage | | | ✅ | ✅ |
| Academic Reputation Score | ✅ | | | |
| Research Productivity Index | | ✅ | | |

---

## 10. Dashboard × Visualization Reference

| Visual | University Overview | Research Analytics | Student Analytics | Country Comparison |
|--------|:------------------:|:-----------------:|:----------------:|:-----------------:|
| Top University Rankings | ✅ | | | |
| Global University Distribution | ✅ | | | |
| Academic Reputation Analysis | ✅ | | | |
| University Performance Trends | ✅ | | | |
| Institutional Comparison | ✅ | | | |
| Top Research Institutions | | ✅ | | |
| Research Impact Comparison | | ✅ | | |
| Research Output Analysis | | ✅ | | |
| Citation Performance | | ✅ | | |
| Research Productivity Trends | | ✅ | | |
| International Student Analysis | | | ✅ | |
| Faculty-to-Student Ratio Analysis | | | ✅ | |
| Student Diversity Trends | | | ✅ | |
| Enrollment Comparisons | | | ✅ | |
| Student Distribution Analysis | | | ✅ | |
| Country Ranking Comparison | | | | ✅ |
| Education Performance Benchmarking | | | | ✅ |
| Regional Education Trends | | | | ✅ |
| Top Performing Countries | | | | ✅ |
| University Distribution | | | | ✅ |

---

*EduVision\_DV — Milestone 4 · Dashboard Guide · Report Date: 2026-09-30*
