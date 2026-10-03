# Module 01 – Data Ingestion and Cleaning

## Overview
Module 01 handles the initial data pipeline stages: validating raw institutional and macroeconomic datasets, inspecting schemas, profiling null distributions, and performing comprehensive data cleaning and standardization.

## Key Objectives
1. **Raw Data Inspection & Profiling**: Validate raw data schemas, column counts, data types, and null distributions across 4 public sources (QS 2025, THE 2024, WUR 2023, World Bank EdStats).
2. **Text Hygiene & Parsing**: Standardize headers to `snake_case`, clean string encodings, strip whitespace, and parse text-encoded numeric ranges (e.g., `"601-800"` → `600.5`).
3. **Country Name Alignment**: Normalize regional and country naming variations across multi-source datasets (e.g., `"USA"` vs `"United States"`).
4. **Data Integrity Logging**: Track pre- and post-cleaning missing value rates without altering original raw source files.

## Module Structure
```text
01_Data_Ingestion_and_Cleaning/
├── notebooks/
│   └── 02_data_cleaning.ipynb
├── reports/
│   ├── dataset_validation_report.csv
│   ├── dataset_validation_report.md
│   ├── dataset_profile.json
│   ├── post_cleaning_validation.csv
│   └── cleaning_log.md
├── scripts/
│   ├── profile_data.py
│   └── clean_datasets.py
└── README.md
```

## Inputs & Outputs

### Inputs (`Data/raw/`)
- `QS World University Rankings 2025 (Top global universities).csv` (1,503 rows x 19 cols)
- `World University Rankings 2023.csv` (2,341 rows x 25 cols)
- `THE 2024 / WUR Data` (1,904 rows x 27 cols)
- `World Bank EdStats` (886,930 records)

### Outputs (`Data/cleaned/`)
- `qs_2025_cleaned.csv`
- `the_2024_cleaned.csv`
- `wur_2023_cleaned.csv`
- `world_bank_education_cleaned.csv`
- `world_bank_country_cleaned.csv`

## How to Run
```bash
python 01_Data_Ingestion_and_Cleaning/scripts/profile_data.py
python 01_Data_Ingestion_and_Cleaning/scripts/clean_datasets.py
```
