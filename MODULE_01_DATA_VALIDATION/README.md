# MODULE 01 – DATA VALIDATION

## Objective
The primary objective of Module 01 is to perform initial dataset inspection, structure profiling, and schema validation across all 4 raw institutional higher-education and macroeconomic data sources before applying downstream transformations.

## Input
- `data/raw/QS_Ranking/QS World University Rankings 2025 (Top global universities).csv`
- `data/raw/World_Ranking/World University Rankings 2023.csv`
- `data/raw/archive (8)/edstats-csv-zip-32-mb-/EdStatsData.csv`
- `data/raw/archive (8)/edstats-csv-zip-32-mb-/EdStatsCountry.csv`

## Process
1. Inspect row and column counts, dataset shapes, and column data types across all raw sources.
2. Profile missing value percentages, zero-value frequencies, and null distributions for ranking/research/student fields.
3. Verify available identifying attributes (`university_name`, `country`, `year`) and global ranking metrics.
4. Export comprehensive dataset profiling reports.

## Output
- `MODULE_01_DATA_VALIDATION/scripts/profile_data.py`
- `MODULE_01_DATA_VALIDATION/reports/dataset_validation_report.md`
- `MODULE_01_DATA_VALIDATION/reports/dataset_validation_report.csv`
- `MODULE_01_DATA_VALIDATION/outputs/dataset_profile.json`

## Validation
- Verified presence of all 4 expected primary datasets in raw storage.
- Verified column headers against expected metadata schemas.
- Profiled total rows: QS 2025 (1,503 rows), WUR 2023 (2,341 rows), THE 2024 (1,904 rows), World Bank EdStats (886,930 records).

## Judge Takeaway
Module 01 establishes baseline data integrity and profiling metrics for the entire pipeline. By understanding schema irregularities and missing value patterns upfront without mutating raw inputs, downstream modules can clean and standardize data deterministically.

---
MODULE 01
   ↓
MODULE 02 – DATA CLEANING
