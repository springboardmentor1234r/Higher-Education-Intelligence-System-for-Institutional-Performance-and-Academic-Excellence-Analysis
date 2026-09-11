# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education data analytics project focused on collecting, cleaning, standardizing, and transforming university ranking and education data into analysis-ready datasets for Tableau dashboard development.

The project uses:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

---

## Current Progress

### Milestone 1 — Data Collection & Preparation
- Module 1 — University Data Collection 
- Module 2 — Data Cleaning & Transformation 

### Milestone 2 — KPI Engineering & Dashboard Planning
- Module 3 — KPI Engineering & Validation 
- Module 4 — Dashboard Planning & Prototyping *(In Progress)*

Module 3 includes:

- Star-schema fact tables
- KPI engineering
- Final Excel dataset
- Data validation

The engineered dataset contains university performance, research, student, and country-level education data.

---

## Important: `working/` vs `Milestone` Folders

The repository contains two versions of the project for different purposes.

### `Milestone 1/` and `Milestone 2/`

These folders contain the **final submission files for each milestone**.

> **These are frozen submission copies and must not be modified after submission.**

They are organized according to the required deliverable structure.

### `working/`

This folder contains the **active and directly runnable version of the project**.

It contains the complete directory structure required by the notebooks, including:

- Raw datasets
- Cleaned datasets
- Final datasets
- Documentation
- Notebooks

> **All development and notebook execution should be done from `working/`.**

### In short

```text
Milestone 1/ → Frozen Milestone 1 submission
Milestone 2/ → Frozen Milestone 2 submission
working/     → Active, runnable development version
````

---

## Running the Project

Use the notebooks inside:

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

The required raw datasets are located in:

```text
working/data/raw/
```

The processed datasets are generated under:

```text
working/data/cleaned/
```

The final Excel dataset is generated under:

```text
working/data/final/
```

---

## Requirements

Python 3 with the following libraries:

* Pandas
* NumPy
* RapidFuzz
* OpenPyXL
* Jupyter Notebook

Install using:

```bash
pip install pandas numpy rapidfuzz openpyxl jupyter
```

---

## Project Structure

```text
EduVision_DV/
│
├── Milestone 1/       # Frozen submission files
│
├── Milestone 2/       # Frozen submission files
│
└── working/           # Active, runnable project
    ├── data/
    │   ├── raw/
    │   ├── cleaned/
    │   └── final/
    ├── docs/
    └── notebooks/
```