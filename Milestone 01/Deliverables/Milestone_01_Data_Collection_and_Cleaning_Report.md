# Milestone 01: Data Collection & Cleaning Report

## Project Overview
**Project Name:** Higher Education Intelligence System for Institutional Performance and Academic Excellence Analysis (EduVision_DV)  
**Deliverable:** Milestone 01 — Data Collection, Ingestion, Auditing & Standardization Report  
**Author / Contributor:** Banka Charishma  

---

## 1. Raw Datasets Ingested
The raw higher education universe combines four authoritative ranking and socio-economic databases:

| Dataset | Source Provider | Year / Edition | Raw Shape | Primary Content |
| :--- | :--- | :--- | :--- | :--- |
| **QS World University Rankings** | Quacquarelli Symonds | 2025 | 1,503 rows × 19 cols | Master institution ranking, academic & employer reputation, faculty-student ratio |
| **Times Higher Education (THE)** | Times Higher Education | 2024 | 867 rows × 27 cols | Research quality, research environment, industry income, international outlook |
| **World University Rankings (WUR)** | Center for WUR / Kaggle | 2023 | 812 rows × 25 cols | Citations, publications, student population, female/male gender ratio |
| **World Bank Education Statistics** | The World Bank | Historical / Multi-year | 55,918 rows × 8 cols | Country-level tertiary education expenditures, literacy rates, enrollment indicators |

---

## 2. Ingestion & Quality Auditing Workflow
1. **Schema Inspection & Encoding Standardization:**
   - Evaluated character encodings across all CSV source files; standardized to `UTF-8`.
   - Stripped trailing and leading whitespace across all string and institution name columns.
2. **Master Universe Anchor (QS 2025):**
   - Treated the QS 2025 ranking table as the primary dimensional anchor (`DIM_UNIVERSITY`).
   - Cleaned invalid geographic region entries (e.g., `U0206 Eastern Mediterranean University`, reclassified from `Not Classified` to `Asia` to harmonize with Cyprus).
   - Confirmed zero duplicate `University_ID` keys in the master entity table.
3. **Filtering & Synchronization:**
   - Filtered secondary ranking tables (`THE 2024`, `WUR 2023`) against the master universe to eliminate phantom entities.
   - Synchronized Country Comparison dataset down to countries validated within the master university scope.

---

## 3. Data Cleaning Pipeline Architecture
```
Raw CSV Sources (QS 2025, THE 2024, WUR 2023, World Bank)
                  │
                  ▼
          [data_collection.py]
   • Null Audit & Data Type Casting
   • Removal of corrupt / unmapped rows
                  │
                  ▼
      [build_university_master.py]
   • Institutional Entity Resolution
   • Alias Dictionary Matching
                  │
                  ▼
         Cleaned Datasets (data/cleaned/)
```

---

## 4. Summary of Output Deliverables
- `Milestone 01/Raw Datasets/`: Exact raw CSV input files.
- `Milestone 01/Script/data_collection.py`: Python ingestion and pre-processing script.
- `Milestone 01/Deliverables/`: Auditing documentation and schema dictionaries.
