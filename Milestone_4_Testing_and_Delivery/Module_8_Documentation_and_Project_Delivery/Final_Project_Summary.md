# EduVision – Final Project Summary

## Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis

---

## 1. Project Overview

EduVision is a higher education analytics system that integrates university ranking datasets with country-level education indicators.

The system provides interactive Tableau dashboards for analyzing:

- University performance
- Research performance
- Student characteristics
- Country-level education performance
- Regional education comparisons

---

## 2. Project Objectives

The main objectives are:

1. Collect university ranking and education datasets.
2. Clean and standardize the source data.
3. Integrate university-level and country-level information.
4. Engineer six education-related KPIs.
5. Build an analytical data model.
6. Develop four interactive Tableau dashboards.
7. Validate calculations and dashboard interactions.
8. Prepare complete project documentation.

---

## 3. Data Sources

The project uses:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

Selected World Bank education indicators are based on 2015 data.

---

## 4. Data Processing

Python was used for:

- Data cleaning
- Data transformation
- Country standardization
- Dataset integration
- KPI engineering
- Data validation
- Exploratory data analysis

Main technologies:

- Python
- Pandas
- NumPy
- Tableau
- Git
- GitHub

---

## 5. Analytical Dataset

The final integrated analytical dataset contains:

**3,530 university records**

World Bank linkage:

**3,466 linked records**

**98.19% linkage**

The project preserves missing values where source information is unavailable.

---

## 6. Six KPIs

The project contains six KPIs:

1. Global Ranking Score
2. Research Impact Score
3. Faculty-to-Student Ratio Score
4. International Student Percentage
5. Academic Reputation Score
6. Research Productivity Index

The KPIs were generated using Python and validated in Tableau.

---

## 7. Tableau Dashboards

Four integrated dashboards were developed.

### University Overview

Analyzes:

- University rankings
- Global ranking score
- Academic reputation
- Research impact
- University distribution
- Performance trends

### Research Analytics

Analyzes:

- Research productivity
- Research impact
- THE research score
- Citation score
- QS citations per faculty
- Research trends

### Student Analytics

Analyzes:

- International student percentage
- Students per staff
- Faculty-to-student ratio score
- Student-related university comparisons

### Country Comparison

Analyzes:

- Country university performance
- Country ranking comparison
- Research productivity
- World Bank education indicators
- Regional education comparison

---

## 8. Dashboard Integration

The Tableau dashboards use:

- Filters
- Parameters
- Parameter actions
- Dashboard actions
- Navigation controls

Navigation flow:

```text
University Overview
        ↓
Research Analytics
        ↓
Student Analytics
        ↓
Country Comparison
        ↓
University Overview