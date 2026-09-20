# Module 2: Data Cleaning & Transformation

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Phase:** Milestone 1 / Weeks 1–2  

---

## Deliverables in this Module
- `data_cleaning.py`: Complete Python ETL script executing regex entity resolution and Star Schema generation.
- `education_cleaning.ipynb`: Interactive cleaning notebook detailing string parsing and join validation.
- `02_data_cleaning.ipynb`: Header standardization and text sanitization notebook.
- `03_data_standardization.ipynb`: Star Schema relational model validation notebook.
- `university_cleaned.csv`: Consolidated clean university dataset.
- Star Schema Fact & Dimension CSVs:
  - `dim_university.csv`: 1,503 institutions with unique surrogate keys (`U0001`..`U1503`).
  - `dim_country.csv`: 106 sovereign nations with conformed keys (`C0001`..`C0106`).
  - `fact_university_performance.csv`: QS ranking facts (1,503 rows).
  - `fact_research.csv`: THE research and citation impact facts (849 rows).
  - `fact_student.csv`: WUR student demographic facts (804 rows).
  - `fact_country_education.csv`: Scoped World Bank macroeconomic indicators (2,243 rows).

---
**Evaluation Result:** Zero duplicate keys, zero orphan records, 0.0% missing on primary identifiers.
