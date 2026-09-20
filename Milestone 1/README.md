# Milestone 1: Data Collection & Preparation (Weeks 1–2)

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Track:** Higher Education Analytics & Business Intelligence  

---

## Milestone Overview
Milestone 1 encompasses the initial data engineering phase of the **EduVision_DV** project, structured into two dedicated modules:
- **Module 1: University Data Collection:** Ingesting, profiling, and archiving multi-source higher education datasets (QS 2025, THE 2024, WUR 2023, World Bank EdStats).
- **Module 2: Data Cleaning & Transformation:** Executing deterministic entity resolution via regex, harmonizing geopolitical nomenclature, eliminating duplicates, enforcing missing value audit rules, and generating an audit-compliant relational Star Schema.

---

## Directory Structure
```
Milestone 1/
├── Module 1/                  # University Data Collection
│   ├── data_collection.py     # Data ingestion & baseline profiling script
│   ├── university_raw_data.csv# Consolidated raw dataset
│   ├── qs_2025_raw.csv, the_2024_raw.csv, wur_2023_raw.csv, world_bank_education_raw.csv
│   ├── 01_data_loading.ipynb  # Interactive data loading notebook
│   └── README.md
│
└── Module 2/                  # Data Cleaning & Transformation
    ├── data_cleaning.py       # Deterministic cleaning & star schema generator
    ├── education_cleaning.ipynb # Interactive cleaning notebook
    ├── 02_data_cleaning.ipynb # String normalization notebook
    ├── 03_data_standardization.ipynb # Schema join verification notebook
    ├── university_cleaned.csv # Consolidated cleaned dataset
    ├── dim_university.csv     # Master university dimension (1,503 rows)
    ├── dim_country.csv        # Master country dimension (106 rows)
    ├── fact_university_performance.csv # QS ranking facts (1,503 rows)
    ├── fact_research.csv      # THE research & citation facts (849 rows)
    ├── fact_student.csv       # WUR student demographic facts (804 rows)
    ├── fact_country_education.csv # World Bank macroeconomic indicators (2,243 rows)
    └── README.md
```
