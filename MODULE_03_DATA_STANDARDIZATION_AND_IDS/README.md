# MODULE 03 – DATA STANDARDIZATION AND IDS

## Objective
Module 03 establishes unified, global surrogate identifiers (`university_id` and `country_id`) across disparate university rankings and macroeconomic datasets. It builds a rigorous institutional crosswalk using a multi-tiered matching workflow.

## Input
- Cleaned datasets from `data/cleaned/` (`qs_2025_cleaned.csv`, `the_2024_cleaned.csv`, `wur_2023_cleaned.csv`, `world_bank_country_cleaned.csv`).

## Process
1. **Tier 1 - Exact Standardized Match**: Join institutions on 100% identical normalized name and country.
2. **Tier 2 - Deterministic Mapping**: Apply a curated crosswalk dictionary for known abbreviations and historical naming variations (e.g., `MIT` ↔ `Massachusetts Institute of Technology`).
3. **Tier 3 - Country Consistency Guardrail**: Enforce strict country matching so institutions with similar names across different nations (e.g., `University of Delhi` vs `Delhi Technological University`) are never merged.
4. **Tier 4 - Controlled Fuzzy Matching**: Use token-set ratio scoring purely as candidate identification; manual audit rules classify matches into `APPROVED`, `REVIEW_REQUIRED`, or `NOT_MATCHED`.

## Output
- `MODULE_03_DATA_STANDARDIZATION_AND_IDS/notebooks/03_standardization_and_ids.ipynb`
- `MODULE_03_DATA_STANDARDIZATION_AND_IDS/scripts/build_standardization_pipeline.py`
- `MODULE_03_DATA_STANDARDIZATION_AND_IDS/scripts/build_university_crosswalk.py`
- `MODULE_03_DATA_STANDARDIZATION_AND_IDS/reports/university_matching_report.md`
- `MODULE_03_DATA_STANDARDIZATION_AND_IDS/reports/university_matching_candidates.csv`
- Output Mappings: `data/final/dim_country.csv`, `data/final/dim_university.csv`, `data/final/university_crosswalk.csv`

## Validation
- Verified unique primary key constraint on `university_id` in `dim_university.csv` (2,735 unique global institutions).
- Verified unique primary key constraint on `country_id` in `dim_country.csv` (152 countries).
- Audited candidate matches: 1,072 APPROVED institutional crosswalk links verified with 0 false-positive auto-merges.

## Judge Takeaway
Module 03 resolves institutional identity fragmentation across global rankings. By relying on deterministic crosswalks and strict country guards rather than blind fuzzy matching, it ensures relational integrity for multi-dataset performance tracking.

---
MODULE 03
   ↓
MODULE 04 – DATA INTEGRATION AND DATA MODEL
