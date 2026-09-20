# Module 1: Milestone 1 & Milestone 2 (Data Collection & Cleaning)

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  

---

## 1. Description of Work
In this module, I completed both **Milestone 1 (University Data Collection)** and **Milestone 2 (Data Cleaning & Transformation)**:
- Loaded and validated four global higher education datasets: QS World University Rankings 2025, Times Higher Education 2024, World University Rankings 2023, and World Bank EdStats.
- Standardized all column names into lowercase snake_case.
- Cleaned university names by removing parenthetical abbreviations (e.g. `(MIT)`) and non-alphanumeric punctuation.
- Standardized country names against a common geopolitical dictionary (`USA` -> `United States`, `UK` -> `United Kingdom`, etc.).
- Created unique master identifiers: `university_id` (`U0001` .. `U1503`) and `country_id` (`C0001` .. `C0106`).
- Created a clean Star Schema relational model consisting of two dimension tables and four fact tables.
- Filtered the World Bank dataset from 5+ million raw rows down to 2,243 relevant records covering key education indicators (expenditure, tertiary enrollment, completion, pupil-teacher ratios) for 2010–2023.

---

## 2. Deliverables in this Folder
- `data_collection.py`: Script to load and validate all raw datasets.
- `data_cleaning.py`: Script executing the full cleaning and star schema transformation.
- `education_cleaning.ipynb`: Interactive cleaning notebook.
- `01_data_loading.ipynb`: Data exploration notebook.
- `02_data_cleaning.ipynb`: Entity cleaning notebook.
- `03_data_standardization.ipynb`: Star schema verification notebook.
- `university_raw_data.csv`: Master consolidated raw dataset.
- `university_cleaned.csv`: Consolidated cleaned dataset.
- Raw CSV files: `qs_2025_raw.csv`, `the_2024_raw.csv`, `wur_2023_raw.csv`, `world_bank_education_raw.csv`.
- Star Schema CSV files: `dim_university.csv`, `dim_country.csv`, `fact_university_performance.csv`, `fact_research.csv`, `fact_student.csv`, `fact_country_education.csv`.
