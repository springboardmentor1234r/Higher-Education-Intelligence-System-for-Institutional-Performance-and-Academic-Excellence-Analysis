# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education data analytics project focused on collecting, cleaning, standardizing, and transforming university ranking and education data into analysis-ready datasets for Tableau dashboard development.

The project integrates data from:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

The project follows a structured data pipeline from raw data collection through data cleaning, standardization, KPI engineering, validation, and dashboard planning.

---

## Project Progress

### Milestone 1 — Data Collection & Preparation

**Module 1 — Data Collection**
- Collected university ranking and education datasets
- Stored original datasets as raw files

**Module 2 — Data Cleaning & Standardization**
- Cleaned source datasets
- Standardized university and country names
- Created normalized dimension tables
- Matched World Bank education data with university/country information

### Milestone 2 — KPI Engineering & Dashboard Planning

**Module 3 — KPI Engineering & Validation**
- Created star-schema fact and dimension tables
- Engineered analytical KPIs
- Created the final integrated dataset
- Performed data validation
- Generated the final Excel dataset

**Module 4 — Dashboard Planning & Prototyping**
- Created dashboard storyboard
- Created Tableau dashboard prototype
- Dashboard development is currently in progress

---

## Working Version vs Milestone Folders

The repository contains both **milestone submission copies** and an **active working version**.

### `Milestone 1/`

Contains the files submitted for **Milestone 1 — Data Collection & Preparation**.

### `Milestone 2/`

Contains the files submitted for **Milestone 2 — KPI Engineering & Dashboard Planning**.

### `working/`

Contains the **active development version** of the project.

All notebook execution and ongoing development should be performed inside `working/`.

The `working/` directory contains:

- Raw datasets
- Cleaned datasets
- Final datasets
- Documentation
- Notebooks

## Project Workflow

The complete data workflow is:

```text
Raw Data
   ↓
Data Loading
   ↓
Data Cleaning
   ↓
Data Standardization
   ↓
KPI Engineering
   ↓
Data Validation
   ↓
Final Dataset
   ↓
Dashboard Planning
   ↓
Tableau Dashboard Development
```

---

## Running the Project

The active notebooks are located in:

```text
working/notebooks/
```

Run them in the following order:

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

The notebooks use relative paths, so the `working/` directory structure should be preserved.

### Input Data

Raw datasets are stored in:

```text
working/data/raw/
```

### Processed Data

Cleaned and standardized datasets are stored in:

```text
working/data/cleaned/
```

### Final Dataset

The final integrated Excel dataset is stored in:

```text
working/data/final/eduvision_final_dataset.xlsx
```

---

## Data Model

The project uses a star-schema structure for analytical reporting.

The main tables include:

```text
dim_country
dim_university

fact_university_performance
fact_research
fact_student
fact_country_education
```

Additional matching information is maintained through:

```text
matches_for_manual_review.csv
world_bank_matched.csv
```

These tables support KPI analysis and Tableau dashboard development.

---

## Project Structure

```text
EduVision_DV/
│
├── Milestone 1/
│   ├── Milestone1_README.md
│   ├── Module 1/
│   │   ├── 01_data_loading.ipynb
│   │   └── raw/
│   │
│   └── Module 2/
│       ├── cleaned/
│       └── notebooks/
│           ├── 02_data_cleaning.ipynb
│           └── 03_data_standardization.ipynb
│
├── Milestone 2/
│   ├── Milestone2_README.md
│   │
│   ├── Module 3/
│   │   ├── deliverables/
│   │   │   ├── eduvision_final_dataset.xlsx
│   │   │   └── star_data_model/
│   │   │
│   │   └── notebooks/
│   │       ├── 04_kpi_engineering.ipynb
│   │       └── 05_validation.ipynb
│   │
│   └── Module 4/
│       ├── dashboard_storyboard.pdf
│       └── prototype.twb
│
├── working/
│   ├── data/
│   │   ├── raw/
│   │   ├── cleaned/
│   │   └── final/
│   │
│   ├── docs/
│   │   ├── 01_dataset_validation_report.md
│   │   ├── 02_matching_methodology.md
│   │   └── 04_final_validation_checklist.csv
│   │
│   └── notebooks/
│       ├── 01_data_loading.ipynb
│       ├── 02_data_cleaning.ipynb
│       ├── 03_data_standardization.ipynb
│       ├── 04_kpi_engineering.ipynb
│       └── 05_validation.ipynb
│
├── .gitignore
├── LICENSE
└── README.md
```

