````
# Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis

---

# Milestone 1: Data Collection and Preparation

## Overview

**Milestone 1** focuses on collecting, cleaning, standardizing, and integrating higher-education ranking datasets required for the **Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis**.

The objective of this milestone is to create a reliable and consistent data foundation for university performance analysis, KPI development, research analytics, student analytics, country-level education analysis, and Tableau dashboard development.

---

# Module 1: University Data Collection

## Objectives

- Collect university ranking datasets from **QS World University Rankings**.
- Collect university ranking datasets from **Times Higher Education (THE)**.
- Collect relevant university performance indicators.
- Identify common fields such as university name and country.
- Prepare datasets for integration.
- Create a common structure across different ranking sources.

## Datasets Collected

The following datasets were collected and prepared for the project:

| Dataset | Year | Purpose |
|---|---:|---|
| QS World University Rankings | 2025 | University rankings and performance indicators |
| Times Higher Education World University Rankings | 2024 | Teaching, research, citations and international outlook |
| Times Higher Education World University Rankings | 2023 | Historical ranking and performance comparison |
| World Bank Education Statistics | 2015 | Supporting country-level education indicators |

> **Note:** World Bank Education Statistics are country-level data and are used as supporting education indicators rather than university-level ranking data.

---

## Major QS Indicators

The QS dataset contains indicators including:

- Global Ranking
- Overall Score
- Academic Reputation
- Employer Reputation
- Faculty-to-Student related indicator
- Citations per Faculty
- International Students
- International Faculty
- Employment Outcomes
- Sustainability

---

## Major THE Indicators

The THE datasets contain indicators including:

- World Ranking
- Overall Score
- Teaching Score
- Research Score
- Citations Score
- Industry Income
- International Outlook
- Student-to-Staff Ratio
- International Students Percentage
- Female Percentage

---

# Module 2: Data Cleaning and Transformation

## Objectives

The collected datasets were cleaned and transformed to make them consistent and suitable for further analysis and visualization.

## Data Cleaning Activities

### 1. Duplicate Removal

- Checked for duplicate rows.
- Checked for duplicate university records.
- Removed duplicate records where applicable.

### 2. Column Standardization

- Standardized column names.
- Converted column names into a consistent format.
- Selected relevant analytical fields.

### 3. University Name Standardization

- Standardized university names across different datasets.
- Created common university identifiers.
- Improved university matching between ranking sources.

### 4. Country Name Standardization

- Identified country-name differences between datasets.
- Created a country mapping to establish consistent country names.
- Used standardized country names for cross-dataset matching.

### 5. Ranking Metric Standardization

- Converted ranking datasets into a common analytical structure.
- Preserved original ranking indicators and scores.
- Prepared datasets for integration and comparison.

### 6. University ID Assignment

- Created a unique `university_id` for each university.
- Used `university_id` to connect university records across different datasets.

---

# Data Integration

After cleaning the individual datasets, the university ranking data was integrated into a common structure.

## Common University Structure

````markdown
```text
University
    │
    ├── University ID
    ├── University Name
    ├── Country
    ├── QS Ranking 2025
    ├── THE Ranking 2024
    └── THE Ranking 2023
````

A country mapping layer was also created to improve consistency between university datasets and country-level education information.

---

# Data Quality and Validation

Several validation checks were performed during Milestone 1.

## Validation Checks

* ✅ Duplicate rows checked
* ✅ Duplicate universities checked
* ✅ University names standardized
* ✅ Country names standardized
* ✅ University IDs generated
* ✅ Ranking datasets converted to common structures
* ✅ Dataset integration verified
* ✅ Missing values analyzed
* ✅ University overlap between datasets analyzed
* ✅ Country mapping validated
* ✅ University ID overlap validated

## QS 2025 Dataset Validation

The QS 2025 dataset contained:

| Metric                 | Value |
| ---------------------- | ----: |
| Rows                   | 1,503 |
| Columns                |    28 |
| Countries              |   106 |
| Duplicate Rows         |     0 |
| Duplicate Universities |     0 |

Missing values in ranking fields were analyzed rather than automatically replaced with zero because a missing value does not necessarily indicate poor university performance.

---

# Milestone 1 Deliverables

## Cleaned Data

```text
data/cleaned/
├── edstats_country_cleaned.csv
├── qs_world_university_rankings_2025_cleaned.csv
├── the_world_university_rankings_2023_cleaned.csv
└── the_world_university_rankings_2024_cleaned.csv
```

## Processed Data

```text
data/processed/
├── country_mapping.csv
├── qs_2025_common.csv
├── qs_2025_with_id.csv
├── the_2023_common.csv
├── the_2023_with_id.csv
├── the_2024_common.csv
├── the_2024_with_id.csv
├── university_master.csv
└── university_overlap_summary.csv
```

## Data Processing Scripts

```text
scripts/
├── analyze_university_overlap.py
├── assign_university_ids.py
├── clean_edstats_country.py
├── clean_qs_2025.py
├── clean_the_2023.py
├── clean_the_2024.py
├── create_country_mapping.py
├── create_university_master.py
├── diagnose_id_merge.py
├── diagnose_university_matching.py
├── inspect_country_matching.py
├── integrate_university_data.py
├── prepare_university_data.py
└── validate_id_overlap.py
```

---

# Technology Stack

| Technology       | Purpose                                      |
| ---------------- | -------------------------------------------- |
| Python           | Data collection, cleaning and transformation |
| Pandas           | Data manipulation and preprocessing          |
| Jupyter Notebook | Data analysis and experimentation            |
| Git              | Version control                              |
| GitHub           | Repository management and collaboration      |

---

# Project Data Flow

```text
Raw Datasets
     │
     ▼
Data Collection
     │
     ▼
Data Inspection
     │
     ▼
Duplicate Detection
     │
     ▼
Column Standardization
     │
     ▼
University Name Standardization
     │
     ▼
Country Name Standardization
     │
     ▼
University ID Assignment
     │
     ▼
Ranking Dataset Integration
     │
     ▼
Validation and Quality Checks
     │
     ▼
Cleaned and Processed Datasets
```

---

# Repository Structure

```text
EduVision/
│
├── data/
│   ├── cleaned/
│   ├── processed/
│   └── raw/
│
├── scripts/
│   ├── Data cleaning scripts
│   ├── Data integration scripts
│   ├── University matching scripts
│   └── Validation scripts
│
├── reports/
│
├── .gitignore
├── README.md
└── LICENSE
```

> **Note:** Original raw datasets are excluded from the GitHub repository using `.gitignore` to avoid uploading large source files.

---

# Outcome

At the end of **Milestone 1**, the project has a structured and validated foundation for higher-education analysis.

The prepared datasets provide the foundation for:

* University performance analysis
* QS and THE ranking comparison
* Research analytics
* Student analytics
* KPI development
* World Bank education integration
* Data modeling
* Tableau dashboard development

---

# Milestone 1 Status

**Milestone 1: ✅ COMPLETED**

## Completed Modules

* ✅ Module 1: University Data Collection
* ✅ Module 2: Data Cleaning and Transformation
* ✅ University Name Standardization
* ✅ Country Name Standardization
* ✅ University ID Assignment
* ✅ Ranking Dataset Integration
* ✅ Data Quality Validation

The completed Milestone 1 work has been committed and pushed to the **`Lekhana_B_M`** branch.

```

 
