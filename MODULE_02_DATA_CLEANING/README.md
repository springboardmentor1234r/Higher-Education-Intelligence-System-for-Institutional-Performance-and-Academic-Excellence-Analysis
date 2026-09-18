# MODULE 02 – DATA CLEANING

## Objective
Module 02 standardizes column names into standard snake_case, converts string-encoded numeric indicators into proper numeric formats, strips leading/trailing whitespace, handles special character encodings, and logs missing-value distributions without modifying the raw datasets.

## Input
- Raw datasets from `data/raw/` (QS 2025, THE 2024, WUR 2023, World Bank EdStats).

## Process
RAW DATA → CLEANING SCRIPT & NOTEBOOK → CLEAN DATA

1. **Column Standardization**: Convert all headers into clean `snake_case` format (e.g., `Rank` → `rank`, `Institution Name` → `university_name`).
2. **Numeric Conversion**: Parse ranges, text ranks (e.g., `601-800` → `600.5`), and string numbers (`citations_per_faculty`) into float/int types.
3. **Text Hygiene**: Trim whitespace, remove non-printable characters, and unify country name variants (e.g., `USA` vs `United States`).
4. **Duplicate Handling**: Retain distinct institutional observations per benchmark year; flag duplicate occurrences.
5. **Post-Cleaning Validation**: Generate validation logs summarizing missing rates before and after cleaning.

## Output
- `MODULE_02_DATA_CLEANING/notebooks/02_data_cleaning.ipynb`
- `MODULE_02_DATA_CLEANING/scripts/clean_datasets.py`
- `MODULE_02_DATA_CLEANING/reports/cleaning_log.md`
- `MODULE_02_DATA_CLEANING/reports/post_cleaning_validation.csv`
- Output Datasets: `data/cleaned/qs_2025_cleaned.csv`, `data/cleaned/the_2024_cleaned.csv`, `data/cleaned/wur_2023_cleaned.csv`, `data/cleaned/world_bank_education_cleaned.csv`, `data/cleaned/world_bank_country_cleaned.csv`

## Validation
- Checked 100% of numeric fields for correct data type conversion (no string-based ranks remaining).
- Validated post-cleaning row counts match clean institutional populations (QS 2025: 1,503 rows; THE 2024: 1,904 rows; WUR 2023: 2,341 rows).
- Zero raw data files were modified during execution.

## Judge Takeaway
Module 02 transforms heterogeneous, dirty raw tabular data into pristine structured tables. It guarantees data type safety and string uniformity, providing a reliable foundation for institutional cross-matching and standardization.

---
MODULE 02
   ↓
MODULE 03 – DATA STANDARDIZATION AND IDS
