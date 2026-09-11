# EduVision_DV — Higher Education Performance Analytics

## Project Overview

**EduVision_DV** is a higher education data analytics project focused on integrating, cleaning, standardizing, and preparing university ranking and education datasets for further KPI engineering and Tableau dashboard development.

The project uses publicly available higher education datasets, including:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

The overall project is intended to transform raw educational data into structured, analysis-ready datasets that can later be used to develop interactive Tableau dashboards for university and country-level analysis.

The planned dashboard suite includes:

1. University Overview
2. Research Analytics
3. Student Analytics
4. Country Comparison

---

## Current Progress

### Milestone 1 — Data Collection and Preparation

Milestone 1 consists of:

- **Module 1 — University Data Collection**
- **Module 2 — Data Cleaning & Transformation**

### Module 1

Module 1 focuses on collecting and validating the raw datasets.

The raw datasets include:

- `qs_2025_raw.csv`
- `the_2024_raw.csv`
- `world_bank_education_subset.csv` — a reduced subset of the original World Bank dataset, included to keep the repository GitHub-compatible
- `wur_2023_raw.csv`

The data-loading notebook performs initial validation of the datasets, including checks for:

- Number of rows and columns
- Duplicate rows
- Duplicate university names
- Important indicator columns
- Missing values
- Data types
- Dataset-specific validation

### Module 2

Module 2 focuses on cleaning, standardizing, and integrating the collected datasets.

The main tasks completed are:

- Removing exact duplicate rows
- Removing records without university names where applicable
- Standardizing column names
- Cleaning university names
- Standardizing country names
- Converting numerical fields into appropriate numeric types
- Handling ranking bands
- Preserving missing values rather than incorrectly replacing them with zero
- Matching universities across different ranking datasets
- Creating standardized university and country dimensions
- Preparing World Bank education data for integration

---

## Important: `working` vs `Milestone 1`

The project contains two copies of the project files for different purposes.

### `Milestone 1/`

This folder contains the **final submission files for Milestone 1**.

> **These files are submission copies and must not be modified after submission.**

They are organized according to the required milestone deliverable structure.

### `working/`

This folder contains the **active, runnable version of the project**.

It maintains the complete directory structure required by the notebooks, including:

- Raw datasets
- Cleaned datasets
- Documentation
- Notebooks

> **Run and modify the project from the `working/` folder.**

The notebooks use relative paths based on this structure, so the copies inside `Milestone 1/` are **not intended to be run directly**.

### In short

```text
Milestone 1/  →  Final submission / DO NOT MODIFY
working/      →  Runnable development version / MODIFY HERE
````

---

## Running the Project

To run the notebooks, use the files inside:

```text
working/notebooks/
```

Run them in this order:

```text
01_data_loading.ipynb
        ↓
02_data_cleaning.ipynb
        ↓
03_data_standardization.ipynb
```

The required datasets are already located under:

```text
working/data/
```

The project uses Python with:

* Pandas
* NumPy
* RapidFuzz
* Jupyter Notebook

---

## Project Structure

```text
EduVision_DV/
│
├── Milestone 1/        # Frozen submission files
│
└── working/            # Active, runnable project
    ├── data/
    │   ├── raw/
    │   └── cleaned/
    ├── docs/
    └── notebooks/
```

**Note:** Any future changes should be made in `working/`. Once a milestone is finalized, the required files can be copied into the corresponding `Milestone` folder as the final submission snapshot.
