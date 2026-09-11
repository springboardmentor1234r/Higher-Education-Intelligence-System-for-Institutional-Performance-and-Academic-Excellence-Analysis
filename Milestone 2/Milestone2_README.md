# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education data analytics project focused on
collecting, cleaning, standardizing, transforming, and analyzing university
ranking and education datasets for KPI engineering and Tableau dashboard development.

The project uses:

* QS World University Rankings 2025
* Times Higher Education World University Rankings 2024
* World University Rankings 2023
* World Bank Education Statistics

The project develops four interlinked Tableau dashboards:

1. University Overview
2. Research Analytics
3. Student Analytics
4. Country Comparison

---

## Current Progress

### Milestone 2 — KPI Engineering and Dashboard Development

Completed modules:

* Module 3 — KPI Engineering & Validation
* Module 4 — Dashboard Planning & Prototyping


## Module 3 — KPI Engineering & Validation

Module 3 focuses on converting the cleaned datasets into analysis-ready
data structures and engineering the required KPIs.

### Data Model

The analytical model contains:

* University dimension
* Country dimension
* University performance data
* Research data
* Student data
* Country education data

Common identifiers include:

* `university_id`
* `country_id`
* `year`

### KPIs

The project includes six major KPIs:

1. Global Ranking Score
2. Research Impact Score
3. Faculty-to-Student Ratio
4. International Student Percentage
5. Academic Reputation Score
6. Research Productivity Index

KPI values are mapped to appropriate source fields or derived using
documented calculations.

### Final Dataset

The final analytical dataset is generated as:

```text
working/data/final/
└── eduvision_final_dataset.xlsx
```

The final dataset contains the required university, research, student,
KPI, and country-level education information.

### Validation

Validation includes:

* Duplicate university checks
* Duplicate country checks
* University-country relationship checks
* Year validation
* Numeric KPI validation
* Missing-value analysis
* KPI availability checks
* Data consistency checks

---

## Module 4 — Dashboard Planning & Prototyping

Module 4 focuses on designing and prototyping the four Tableau dashboards.

The dashboard storyboard serves as the **design specification** for the
Tableau implementation.

### Dashboard 1 — University Overview

Purpose: University landscape and ranking performance.

Includes:

* Total Universities
* Average Rank
* Overall Score
* Top Universities 2025
* University Map

Filters:

* Country
* Region
* Source

University selections can filter or highlight related dashboard views.

### Dashboard 2 — Research Analytics

Purpose: Research performance and university comparison.

Includes:

* Research Impact
* Academic Reputation
* Research comparison
* Research Productivity / Citation comparison

Filters:

* University
* Country
* Region
* Year
* Source

University selection highlights research metrics.

### Dashboard 3 — Student Analytics

Purpose: Student scale, internationalization, and faculty-student analysis.

Includes:

* Faculty-Student Ratio
* International Students
* Student comparison
* International Student Percentage comparison

Filters:

* University
* Country
* Region
* Year
* Source

University selection highlights student metrics.

### Dashboard 4 — Country Comparison

Purpose: Country-level education comparison.

Includes:

* Country ranking
* Tertiary Enrollment
* Adult Literacy
* Government Education Expenditure

Filters:

* Country
* Region

Country selection highlights the comparison views.

---

## Dashboard Interlinking

The four dashboards are designed as one interconnected system.

Navigation connects:

```text
University Overview
        ↓
Research Analytics
        ↓
Student Analytics
        ↓
Country Comparison
```

Users can select a university and carry the selection into related
dashboard views.

Country information can also be used to move from university-level
analysis to country-level comparison.

---

## `working/` vs `Milestone` Folders

The repository contains separate folders for development and submission.

### `Milestone 1/`

Contains the final Milestone 1 submission files.

> These files are frozen and must not be modified.

### `Milestone 2/`

Contains the final Milestone 2 submission files.

> These files are frozen and must not be modified.

Milestone 2 contains the completed Module 3 and Module 4 work.

### `working/`

Contains the active and runnable version of the project.

All development and notebook execution should be performed from `working/`.

## Project Structure

```text
EduVision_DV/
│
├── Milestone 1/
│   └── Frozen submission files
│
├── Milestone 2/
│   └── Frozen submission files
│
└── working/
    │
    ├── data/
    │   ├── raw/
    │   ├── cleaned/
    │   └── final/
    │
    ├── docs/
    │
    └── notebooks/
        ├── 01_data_loading.ipynb
        ├── 02_data_cleaning.ipynb
        ├── 03_data_standardization.ipynb
        ├── 04_kpi_engineering.ipynb
        └── 05_validation.ipynb
```

---

## Final Statement

This storyboard serves as the **design specification** for the EduVision dashboard.
The Tableau **`.twbx` workbook should implement the four dashboards, defined filters,
navigation, and inter-dashboard actions using the **final dataset**.

**EduVision_DV Milestone 2 is complete.**
