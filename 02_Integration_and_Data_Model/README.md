# Module 02 – Integration and Data Model

## Overview
Module 02 establishes unified institutional surrogate identifiers (`university_id`, `country_id`), builds a multi-tier entity crosswalk across ranking systems, and constructs an enterprise Star Schema relational data model.

## Key Objectives
1. **Entity Resolution & Crosswalk**: Execute a 4-tiered matching workflow (Exact Name match, Deterministic mapping, Country guardrail checks, and Controlled token-set fuzzy matching with audit rules) to link institutions across QS, THE, WUR, and World Bank datasets.
2. **Surrogate Key Assignment**: Generate unique global primary keys (`university_id` like `U0001`, `country_id` like `C001`).
3. **Dimensional Modeling**: Construct `dim_university` (2,735 unique institutions) and `dim_country` (152 countries).
4. **Fact Table Generation**: Construct normalized Star Schema fact tables with composite primary keys (`university_id`, `year`):
   - `fact_university_performance`: Overall ranks, scores, and reputation.
   - `fact_research`: Citation counts, research scores, collaboration indices.
   - `fact_student`: Total enrollment, international student ratios, staff ratios.
   - `fact_country_education`: World Bank education indicators by country and year.

## Module Structure
```text
02_Integration_and_Data_Model/
├── notebooks/
│   ├── 03_standardization_and_ids.ipynb
│   └── 04_kpi_engineering_and_final_data.ipynb
├── reports/
│   ├── university_matching_candidates.csv
│   ├── university_matching_report.md
│   └── final_data_model_validation.csv
├── scripts/
│   ├── build_standardization_pipeline.py
│   ├── build_university_crosswalk.py
│   ├── build_analytical_data_model.py
│   └── build_final_fact_tables.py
└── README.md
```

## Inputs & Outputs

### Inputs
- Cleaned CSV datasets from `Data/cleaned/`

### Outputs (`Data/final/`)
- `dim_university.csv`
- `dim_country.csv`
- `university_crosswalk.csv`
- `fact_university_performance.csv`
- `fact_research.csv`
- `fact_student.csv`
- `fact_country_education.csv`

## How to Run
```bash
python 02_Integration_and_Data_Model/scripts/build_standardization_pipeline.py
python 02_Integration_and_Data_Model/scripts/build_university_crosswalk.py
python 02_Integration_and_Data_Model/scripts/build_analytical_data_model.py
python 02_Integration_and_Data_Model/scripts/build_final_fact_tables.py
```
