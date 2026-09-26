# Milestone 3 -- Dashboard Development

## Project

**EduVision_DV -- Higher Education Intelligence System for Institutional
Performance and Academic Excellence Analysis**

Milestone 3 covers the development and integration of the Tableau
dashboard suite for higher education performance analysis.

## Objective

The objective of this milestone is to transform the prepared analytical
datasets and KPI definitions into a unified, interactive Tableau
dashboard suite.

The project requires four interconnected dashboards:

1.  University Overview
2.  Research Analytics
3.  Student Analytics
4.  Country Comparison

## Dashboard Development

### 1. University Overview

The University Overview dashboard provides a high-level view of
university performance.

Key areas include:

-   University rankings
-   University distribution by country
-   Overall score analysis
-   Academic reputation
-   Research performance
-   International student indicators
-   KPI cards
-   Country filtering and dashboard navigation

### 2. Research Analytics

The Research Analytics dashboard focuses on research and academic
performance.

Key areas include:

-   Research score
-   Citation performance
-   Research score distribution
-   Teaching versus research performance
-   International outlook
-   Student-staff ratio
-   Top research-performing universities

### 3. Student Analytics

The Student Analytics dashboard focuses on student population and
diversity.

Key areas include:

-   Total students
-   Student-staff ratio
-   International student percentage
-   Female student percentage
-   University-level student comparisons
-   Student distribution
-   Teaching, research and citation indicators

### 4. Country Comparison

The Country Comparison dashboard operates primarily at country level.

Key areas include:

-   Education expenditure
-   Tertiary enrollment
-   Adult literacy
-   Primary completion
-   Total population
-   Government expenditure on education
-   Country-level KPI cards
-   Top-country comparisons

## Dashboard Integration

The four dashboards are integrated within a single Tableau workbook.

The dashboard suite includes:

-   Navigation buttons between dashboards
-   Filter interactions
-   Dashboard actions
-   University and country analysis
-   Common identifiers such as `university_id`, `country_id`, and `year`
    where applicable

The intended dashboard flow is:

**University Overview → Research Analytics → Student Analytics → Country
Comparison**

The project guide requires the dashboards to be interconnected rather
than functioning as four unrelated dashboards.

## Data Sources

The dashboard suite uses the project's prepared analytical datasets:

-   QS World University Rankings 2025 -- University Overview
-   THE World University Rankings 2024 -- Research Analytics
-   World University Rankings 2023 -- Student Analytics
-   World Bank Education Statistics -- Country Comparison

The datasets have different analytical grains and are therefore used for
their intended dashboard purposes rather than being blindly merged into
one large table.

## KPI Approach

The project defines six major KPIs:

1.  Global Ranking Score
2.  Research Impact Score
3.  Faculty-to-Student Ratio
4.  International Student Percentage
5.  Academic Reputation Score
6.  Research Productivity Index

KPI definitions and formulas should remain consistent with the approved
project methodology. Scores should not be treated as actual percentages
or ratios unless the underlying field represents that measure.

## Tableau Workbook

The completed integrated Tableau workbook for this milestone is:

`EduVision_DV.twbx`

It contains all four required dashboards:

-   University Overview
-   Research Analytics
-   Student Analytics
-   Country Comparison

## Milestone 3 Deliverable

The primary deliverable for this milestone is the integrated Tableau
workbook:

`EduVision_DV.twbx`

The workbook is stored in the `dashboard` folder of this milestone.

## Quality Focus

Before final submission, the dashboard suite should be checked for:

-   Correct KPI calculations
-   Correct ranking calculations
-   Working filters
-   Working navigation buttons
-   Working dashboard actions
-   Correct university and country filtering
-   Proper dashboard interlinking
-   Clear KPI units
-   Consistent dashboard formatting
-   No major dashboard errors

## Repository Structure

``` text
Milestone_3/
├── README.md
└── dashboard/
    └── EduVision_DV.twbx
```

## Next Milestone

**Milestone 4 -- Testing and Delivery**

The next milestone covers:

-   KPI validation
-   Ranking validation
-   Dashboard interaction testing
-   Educational metric validation
-   QA Checklist
-   Dashboard Testing Report
-   Final documentation
-   Final project delivery
