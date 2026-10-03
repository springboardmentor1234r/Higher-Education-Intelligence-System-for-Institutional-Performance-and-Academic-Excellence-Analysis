# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education analytics project that integrates university ranking, research, student, and country-level education data into an interactive Tableau dashboard system.

The project follows a complete data analytics workflow from raw data collection and preprocessing to KPI engineering, dashboard development, testing, documentation, and final delivery.

---

## Data Sources

The project uses data from the following sources:

- **QS World University Rankings 2025**
- **Times Higher Education World University Rankings 2024**
- **World University Rankings 2023**
- **World Bank Education Statistics**

---

## Project Objectives

- Collect and prepare higher education datasets from multiple sources.
- Clean and standardize university and country data.
- Create a structured analytical data model.
- Engineer higher education performance KPIs.
- Validate the analytical data and KPI calculations.
- Develop interactive Tableau dashboards.
- Integrate the dashboards into a single dashboard system.
- Test dashboard functionality and data accuracy.
- Prepare complete project documentation and final deliverables.

---

## Project Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Data Standardization
      ↓
University & Country Matching
      ↓
Data Modeling
      ↓
KPI Engineering
      ↓
Data Validation
      ↓
Dashboard Planning
      ↓
Tableau Dashboard Development
      ↓
Dashboard Integration
      ↓
Testing & Quality Assurance
      ↓
Final Documentation
      ↓
Project Delivery
````

---

# Milestones

## Milestone 1 — Data Collection & Preparation

### Module 1 — Data Collection

* Loaded and inspected the source datasets.
* Stored the original datasets as raw files.
* Prepared the datasets for further processing.

### Module 2 — Data Cleaning & Standardization

* Cleaned the source datasets.
* Standardized university and country names.
* Created university and country dimensions.
* Matched World Bank country information.
* Recorded uncertain matches for manual review.

---

## Milestone 2 — KPI Engineering & Dashboard Planning

### Module 3 — KPI Engineering & Validation

* Created the analytical star-schema data model.
* Created fact and dimension tables.
* Engineered the required KPIs.
* Created the final analytical dataset.
* Performed data validation.

### Module 4 — Dashboard Planning & Prototyping

* Created the dashboard storyboard.
* Planned dashboard layouts and visualizations.
* Created the Tableau prototype.

---

## Milestone 3 — Dashboard Development & Integration

### Module 5

* University Overview
* Research Analytics

### Module 6

* Student Analytics
* Country Comparison
* Dashboard integration

The four dashboards were developed using the final analytical dataset and integrated into a single Tableau workbook.

---

## Milestone 4 — Testing & Delivery

### Module 7 — Testing & Validation

* Data integrity testing
* KPI validation
* Ranking validation
* Educational metric validation
* Dashboard functional testing
* Navigation testing
* Filter testing
* Dashboard interaction testing
* Visual quality validation
* Quality assurance

### Module 8 — Documentation & Project Delivery

* Final project documentation
* GitHub repository organization
* Final Tableau workbook
* Final dashboard PDF
* Project delivery documentation

---

# Dashboards

The final project contains four integrated Tableau dashboards.

## 1. University Overview

Provides an overview of:

* Global ranking
* Overall score
* Academic reputation
* Research impact
* Faculty-student ratio
* International students

## 2. Research Analytics

Provides analysis of:

* Research score
* Citation score
* Research impact
* Research productivity
* Research institutions
* Research performance by region

## 3. Student Analytics

Provides analysis of:

* Total students
* International students
* Faculty-student ratio
* Student diversity
* Enrollment
* Student distribution

## 4. Country Comparison

Provides country-level analysis of:

* Total countries
* Education countries
* Adult literacy
* Tertiary enrollment
* Country ranking
* Education performance

---

# Key Performance Indicators

The project includes six core engineered KPIs:

1. **Global Ranking Score**
2. **Research Impact Score**
3. **Faculty-to-Student Ratio**
4. **International Student Percentage**
5. **Academic Reputation Score**
6. **Research Productivity Index**

---

# Data Model

The project uses a **star-schema analytical model** consisting of university and country dimensions with multiple analytical fact tables.

```text
                 dim_university
                       │
                       ├── fact_university_performance
                       ├── fact_research
                       └── fact_student

                 dim_country
                       │
                       └── fact_country_education
```

The final analytical dataset is:

```text
working/data/final/eduvision_final_dataset.xlsx
```

---

# Project Structure

```text
Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── Milestone 1/
│   ├── Milestone1_README.md
│   │
│   ├── Module 1/
│   │   ├── 01_data_loading.ipynb
│   │   └── raw/
│   │       ├── qs_2025_raw.csv
│   │       ├── the_2024_raw.csv
│   │       ├── world_bank_education_subset.csv
│   │       └── wur_2023_raw.csv
│   │
│   └── Module 2/
│       ├── notebooks/
│       │   ├── 02_data_cleaning.ipynb
│       │   └── 03_data_standardization.ipynb
│       │
│       └── cleaned/
│           ├── qs_2025_clean.csv
│           ├── the_2024_clean.csv
│           ├── world_bank_education_clean.csv
│           ├── wur_2023_clean.csv
│           │
│           └── Normalized/
│               ├── dim_country.csv
│               ├── dim_university.csv
│               ├── matches_for_manual_review.csv
│               └── world_bank_matched.csv
│
├── Milestone 2/
│   ├── Milestone2_README.md
│   │
│   ├── Module 3/
│   │   ├── notebooks/
│   │   │   ├── 04_kpi_engineering.ipynb
│   │   │   └── 05_validation.ipynb
│   │   │
│   │   └── deliverables/
│   │       ├── eduvision_final_dataset.xlsx
│   │       └── star_data_model/
│   │           ├── dim_country.csv
│   │           ├── dim_university.csv
│   │           ├── fact_country_education.csv
│   │           ├── fact_research.csv
│   │           ├── fact_student.csv
│   │           ├── fact_university_performance.csv
│   │           ├── matches_for_manual_review.csv
│   │           └── world_bank_matched.csv
│   │
│   └── Module 4/
│       ├── dashboard_storyboard.pdf
│       └── prototype.twb
│
├── Milestone 3/
│   ├── Milestone3_README.md
│   │
│   ├── Module 5/
│   │   ├── 1_University Overview.pdf
│   │   └── 2_Research Analytics.pdf
│   │
│   ├── Module 6/
│   │   ├── 3_Student Analytics.pdf
│   │   └── 4_Country Comparison.pdf
│   │
│   └── Final Integrated Dashboard/
│       └── EduVision_Dashboard.twbx
│
├── Milestone 4/
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
    │   ├── 01_dataset_validation_report.md
    │   ├── 02_matching_methodology.md
    │   └── 04_final_validation_checklist.csv
    │
    └── notebooks/
        ├── 01_data_loading.ipynb
        ├── 02_data_cleaning.ipynb
        ├── 03_data_standardization.ipynb
        ├── 04_kpi_engineering.ipynb
        └── 05_validation.ipynb
```

---

# Working Directory

The `working/` directory contains the active development version of the project.

### Raw Data

```text
working/data/raw/
```

Contains the original source datasets.

### Cleaned Data

```text
working/data/cleaned/
```

Contains cleaned, standardized, matched, and structured datasets.

### Final Dataset

```text
working/data/final/
```

Contains:

```text
eduvision_final_dataset.xlsx
```

### Notebooks

```text
working/notebooks/
```

The notebooks are organized in the following workflow:

```text
01_data_loading.ipynb
        ↓
02_data_cleaning.ipynb
        ↓
03_data_standardization.ipynb
        ↓
04_kpi_engineering.ipynb
        ↓
05_validation.ipynb
```

---

# Final Deliverables

## Tableau

```text
EduVision_Dashboard.twbx
4_Dashboards.pdf
```

## Testing

```text
Dashboard_Testing_Report.pdf
QA_Checklist.pdf
```

## Documentation

```text
EduVision_Final_Documentation.pdf
Git_Repository.md
Tableau_Public.md
```

## Analytical Dataset

```text
eduvision_final_dataset.xlsx
```

---

# Technology Stack

* **Python**
* **Pandas**
* **Jupyter Notebook**
* **Microsoft Excel**
* **Tableau**
* **Git**
* **GitHub**

---

# Final Outcome

EduVision_DV provides a complete higher education analytics workflow that combines multiple university ranking and education datasets into a structured analytical model and an integrated Tableau dashboard system.

The final solution includes:

* Standardized analytical data model
* Six core KPIs
* Four Tableau dashboards
* Dashboard navigation and interactions
* Testing and QA documentation
* Final project documentation
* Final Tableau workbook
* Complete project repository

---
