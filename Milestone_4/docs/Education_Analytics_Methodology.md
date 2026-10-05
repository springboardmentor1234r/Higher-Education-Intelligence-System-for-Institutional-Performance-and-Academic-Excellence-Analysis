# Education Analytics Methodology

## 1. Introduction

EduVision_DV is a Higher Education Intelligence System developed to
analyze university and education-related performance using multiple
publicly available datasets.

The methodology followed a structured process of data collection,
preparation, cleaning, normalization, validation, KPI development, and
dashboard visualization.

---

## 2. Overall Workflow

The project followed these major stages:

1. Data Collection
2. Data Inspection
3. Data Cleaning
4. Data Normalization
5. Data Validation
6. KPI Preparation
7. Tableau Integration
8. Dashboard Development
9. Dashboard Testing
10. Final Documentation

---

## 3. Data Collection

Data was collected from multiple higher education sources, including:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

The collected datasets were stored as raw data before processing.

---

## 4. Data Inspection

Each dataset was inspected to understand:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate records
- Unique values
- Ranking formats
- Score distributions

This stage helped identify potential data quality issues before cleaning.

---

## 5. Data Cleaning

The following cleaning operations were performed:

### 5.1 University Names

University names were cleaned and standardized to reduce inconsistencies
between datasets.

### 5.2 Country Names

Country names were standardized to support reliable country-level
filtering and comparison.

### 5.3 Ranking Values

Ranking fields containing ranges or special formats were processed into
appropriate forms for analysis.

Examples include:

- `621-630`
- `1401+`

### 5.4 Numeric Fields

Score and ranking fields were converted into suitable numeric formats
where required.

### 5.5 Missing Values

Missing values were identified and handled according to the requirements
of individual fields and visualizations.

---

## 6. Duplicate Checking

Datasets were checked for duplicate records.

Duplicate records were identified during data inspection and appropriate
cleaning steps were applied where required.

The objective was to avoid duplicate information affecting KPI calculations
and visualizations.

---

## 7. Data Normalization

After cleaning, the data was organized into structured datasets.

The project used normalized structures to separate information related to:

- Universities
- Countries
- University performance
- Research performance
- Student indicators
- Country education indicators

This organization supports efficient analysis and visualization.

---

## 8. Data Validation

The prepared datasets were validated before being connected to Tableau.

Validation included:

- Checking column names
- Checking data types
- Checking missing values
- Checking duplicate records
- Verifying university names
- Verifying country names
- Checking numerical values
- Checking year fields
- Reviewing calculated values

The validation process helped ensure that the prepared data was suitable
for dashboard development.

---

## 9. KPI Development

Key performance indicators were prepared to summarize important aspects
of higher education performance.

The major KPIs include:

- Global Ranking Score
- Academic Reputation Score
- Research Impact Score
- Research Productivity Index
- Faculty-Student Ratio
- International Student Percentage

The KPIs were incorporated into the Tableau dashboards to provide
quick performance summaries.

---

## 10. Tableau Integration

The cleaned and validated data was connected to Tableau.

The Tableau workbook was developed using:

- Worksheets
- Filters
- KPI views
- Charts
- Dashboard containers
- Navigation objects
- Interactive dashboard actions

The dashboards were designed to support interactive exploration of
university and country-level education data.

---

## 11. Dashboard Development

Four dashboards were developed.

### University Overview

Provides an overall view of university performance using KPIs and
university ranking comparisons.

### Research Analytics

Focuses on research productivity, research impact, and research-related
comparisons.

### Student Analytics

Focuses on student-related indicators including faculty-student ratio,
international student percentage, and academic reputation.

### Country Comparison

Provides country-level comparison using region, country, and year
filters.

---

## 12. Interactive Filtering

Interactive filters were implemented to allow users to analyze selected
subsets of the data.

Filters include:

- Region
- Country Name
- University Name
- Overview Year
- Research Year
- Student Year

The filters allow users to dynamically update the dashboard views.

---

## 13. Dashboard Navigation

Navigation buttons were implemented to allow users to move between the
four dashboards.

The navigation structure provides access to:

- University Overview
- Research Analytics
- Student Analytics
- Country Comparison

This creates a connected dashboard experience.

---

## 14. Final Validation

After dashboard development, the complete workbook was reviewed for:

- Correct KPI values
- Filter functionality
- Navigation functionality
- Chart rendering
- Layout consistency
- Null values
- Dashboard usability

The final Tableau workbook was saved as a packaged workbook:

`EduVision_DV.twbx`

---

## 15. Final Output

The final output of the methodology is an interactive Tableau-based
Higher Education Intelligence System that enables users to explore
university, research, student, and country-level education performance.
