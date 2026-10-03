# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education analytics project that integrates
university ranking, research, student, and country-level education data into
an interactive Tableau dashboard system.

The project uses data from:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

# Milestone 4 — Testing and Delivery

Milestone 4 consists of two modules:

- **Module 7 — Testing and Validation**
- **Module 8 — Documentation and Project Delivery**

The purpose of this milestone is to verify the correctness of the final
analytical model and Tableau dashboards and to prepare the complete project
for final submission and delivery.

---

# Module 7 — Testing and Validation

Module 7 focuses on validating the data model, KPI calculations, dashboard
functionality, dashboard interactions, and educational metrics.

## Testing Areas

The following areas were tested:

- Data integrity
- KPI calculations
- Ranking calculations
- Country-level educational metrics
- Dashboard availability
- Dashboard navigation
- Dashboard filters
- Dashboard linking
- Visual quality
- Documentation
- Final workbook delivery

The testing was performed using the final Excel analytical model and the
completed Tableau dashboards.

---

## Data Integrity Validation

The final analytical model was checked for:

- Duplicate university IDs
- Duplicate country IDs
- Duplicate fact-table composite keys
- Invalid university foreign keys
- Invalid country foreign keys
- Missing values and documented source limitations

### Validation Results

- **4,708** unique university IDs
- **136** unique country IDs
- **0** duplicate university IDs
- **0** duplicate country IDs
- **0** duplicate fact-table composite keys
- **0** invalid university foreign keys
- **0** invalid non-null country foreign keys

# Dashboard Validation

All four completed dashboards were tested:

1. University Overview
2. Research Analytics
3. Student Analytics
4. Country Comparison

### Dashboard Tests

The following dashboard functions were manually checked:

* Dashboard opening and rendering
* Left-side navigation
* Year filter
* University filter
* Country filter
* Dashboard linking
* Visual rendering
* Overall dashboard layout

All four dashboard interaction tests were manually verified as working.
No major broken visualization was identified in the supplied final dashboard
screenshots. 

---

# Ranking Validation

The University Overview ranking KPI was validated against the final
university performance fact table.

The minimum global rank in the final data was:

```text
1
```

The Tableau dashboard displayed:

```text
1.000
```

The ranking calculation therefore matched the final analytical model.


---

# Educational Metric Validation

The country-level educational metrics were validated against the
`fact_country_education` dataset.

Validated metrics include:

* Average Adult Literacy
* Average Tertiary Enrollment
* Number of Education Countries

The final model contains:

* **119 countries** with education records
* **87.9667%** average adult literacy
* **44.3255%** average tertiary enrollment

These values match the displayed Tableau KPI values of **87.97** and
**44.33** after rounding. 

---

# QA Checklist

A total of **30 QA test cases** were recorded.

### QA Summary

| Result         |  Count |
| -------------- | -----: |
| PASS           |     26 |
| PASS WITH NOTE |      2 |
| MANUAL         |      2 |
| **Total**      | **30** |

The two PASS WITH NOTE items document known source/data limitations,
including missing values and remaining Null categories/scrollbars.

The two MANUAL items concern:

* Dashboard action click-through verification
* Final `.twbx` delivery verification

The final manual interaction verification confirmed that navigation, Year
filter, University/Country filters, and dashboard linking were working.

# Module 7 Deliverables

The following documents were prepared for testing and validation:

```text
Milestone 4/
│
└── Module 7/
    └── Delivarables/
        ├── Dashboard_Testing_Report.pdf
        └── QA_Checklist.pdf
```

### Dashboard Testing Report

The Dashboard Testing Report documents:

* Testing objective
* Test basis
* Data integrity validation
* KPI validation
* Dashboard functional testing
* Ranking validation
* Educational metric validation
* Final QA conclusion

The report confirms that the final analytical model is internally
consistent for identifiers, composite keys, referential integrity, and
tested KPI calculations. 

### QA Checklist

The QA Checklist contains all 30 test cases covering data, KPI,
dashboard, documentation, and delivery validation. 

---

# Module 8 — Documentation and Project Delivery

Module 8 focuses on preparing the final project documentation and
organising the complete project for delivery.

The final documentation consolidates the work completed across Milestones
1 to 4.

It covers:

* Project overview
* Data sources
* Data model
* KPI definitions
* KPI methodology
* Dashboard architecture
* Dashboard guides
* Filters and navigation
* Testing and quality assurance
* Project structure
* Delivery information
* Milestone summary
* Technical stack

The final documentation is intended to allow a new reader to understand the
completed project without needing to open the earlier milestone files.


---

# Final Documentation

The final documentation is provided as:

```text
Module 8/
└── Deliverables/
    └── EduVision_Final_Documentation.pdf
```

The document provides the consolidated final record of the project,
including the data model, KPI methodology, four dashboards, testing,
quality assurance, and delivery structure. 

---

# GitHub Repository

The completed project is organised into milestone-based folders and a
working directory containing the data, notebooks, and supporting
documentation.

The repository contains:

* Milestone 1
* Milestone 2
* Milestone 3
* Milestone 4
* Working data
* Jupyter notebooks
* Documentation
* Final Tableau workbook

The final documentation records the GitHub repository as part of the
Module 8 project delivery. 

---

# Project Structure

```text
EduVision_DV/
│
├── Milestone 1/
│
├── Milestone 2/
│
├── Milestone 3/
│
├── Milestone 4/
│   │
│   ├── Milestone4_README.md
│   │
│   ├── Module 7/
│   │   └── Delivarables/
│   │       ├── Dashboard_Testing_Report.pdf
│   │       └── QA_Checklist.pdf
│   │
│   └── Module 8/
│       ├── Deliverables/
│       │   ├── EduVision_Final_Documentation.pdf
│       │   ├── Git_Repository.md
│       │   └── Tableau_Public.md
│       │
│       └── Tableau/
│           ├── 4_Dashboards.pdf
│           └── EduVision_Dashboard.twbx
│
└── working/
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

# Technology Stack

The project uses:

* **Python**
* **Pandas**
* **Jupyter Notebook**
* **Microsoft Excel**
* **Tableau**
* **Git**
* **GitHub**

Python was used for data preparation, standardisation, KPI engineering,
and validation. Tableau was used for dashboard development and
visualisation.

---
# Final Deliverables

The final Milestone 4 submission contains:

### Module 7 — Testing and Validation

* `Dashboard_Testing_Report.pdf`
* `QA_Checklist.pdf`

### Module 8 — Documentation and Project Delivery

* `EduVision_Final_Documentation.pdf`
* `Git_Repository.md`
* `Tableau_Public.md`

### Tableau

* `4_Dashboards.pdf`
* `EduVision_Dashboard.twbx`

---
**EduVision_DV Milestone 4 is complete.**
