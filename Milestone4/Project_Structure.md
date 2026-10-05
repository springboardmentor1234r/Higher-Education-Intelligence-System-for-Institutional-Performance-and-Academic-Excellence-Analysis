# EduVision\_DV — Project Structure

| Item | Details |
|------|---------|
| **Project** | EduVision\_DV — Higher Education Performance Dashboard |
| **Document** | Project Folder Structure Reference |
| **Report Date** | 2026-09-30 |
| **Document Version** | v1.0 |

---

## 1. Overview

EduVision\_DV is organized into **four milestone folders** representing the complete project development lifecycle — from raw data collection through cleaning, KPI engineering, Tableau dashboard development, and final testing and documentation.

The project uses a milestone-based structure without separate sub-module folders. All files for a given phase are stored directly within the corresponding milestone directory.

---

## 2. Milestone Summary

| Milestone | Phase | Primary Deliverables |
|-----------|-------|----------------------|
| **Milestone 1** | Data Collection & Cleaning | Raw data, cleaning script, cleaned dataset |
| **Milestone 2** | KPI Engineering & Prototype | KPI generation script, final dataset, prototype workbook |
| **Milestone 3** | Dashboard Development | Production Tableau workbook |
| **Milestone 4** | Testing, Validation & Documentation | QA checklist, testing report, all reference documents |

---

## 3. Complete Folder Structure

```text
EduVision_DV/
│
├── data/
│   └── raw/
│       ├── QS World University Rankings 2025 (Top global universities).csv
│       ├── TIMES_WorldUniversityRankings_2024.csv
│       ├── World University Rankings 2023.csv
│       └── world_bank_education/
│           ├── EdStatsCountry-Series.csv
│           ├── EdStatsCountry.csv
│           ├── EdStatsData.csv
│           ├── EdStatsFootNote.csv
│           └── EdStatsSeries.csv
│
├── Milestone1/
│   ├── data_collection.py
│   ├── education_cleaning.ipynb
│   ├── university_raw_data.csv
│   └── university_cleaned.csv
│
├── Milestone2/
│   ├── generate_education_kpis.py
│   ├── university_final_dataset.xlsx
│   ├── dashboard_storyboard.pdf
│   ├── eduvision_prototype.twb
│   └── eduvision_prototype.twbx
│
├── Milestone3/
│   ├── EduVision_DV_1.twbx
│   └── eduvision_prototype_v1.twbx
│
├── Milestone4/
│   ├── QA_Checklist.md
│   ├── Dashboard_Testing_Report.md
│   ├── KPI_Defination.md
│   ├── Data_Sources.md
│   ├── Dashboard_guide.md
│   ├── Education_Analytics_Methodology.md
│   └── Project_Structure.md
│
├── Final Project/
│   └── Tableau_Public_Link.md
│
├── .gitignore
└── README.md
```

---

## 4. Data Folder

The `data/` folder holds all raw source datasets used in the project.

### 4.1 `data/raw/`

| File | Dataset | Size |
|------|---------|------|
| `QS World University Rankings 2025 (Top global universities).csv` | QS World University Rankings 2025 | 226 KB |
| `TIMES_WorldUniversityRankings_2024.csv` | Times Higher Education Rankings 2024 | 1.79 MB |
| `World University Rankings 2023.csv` | World University Rankings 2023 | 234 KB |

### 4.2 `data/raw/world_bank_education/`

The World Bank Education Statistics dataset is stored in its own sub-folder due to its multi-file structure.

| File | Description | Size |
|------|-------------|------|
| `EdStatsData.csv` | Main education indicators data (all countries, multi-year) | 311 MB |
| `EdStatsSeries.csv` | Series/indicator definitions and metadata | 3.5 MB |
| `EdStatsCountry.csv` | Country reference data | 136 KB |
| `EdStatsCountry-Series.csv` | Country-to-series mapping | 48 KB |
| `EdStatsFootNote.csv` | Data footnotes and source notes | 37.9 MB |

---

## 5. Milestone 1 — Data Collection & Cleaning

**Phase:** Raw data ingestion and preprocessing

| File | Type | Description |
|------|------|-------------|
| `data_collection.py` | Python script | Collects and downloads source datasets |
| `education_cleaning.ipynb` | Jupyter Notebook | Full data cleaning pipeline — deduplication, standardization, missing value handling, type conversion |
| `university_raw_data.csv` | CSV | Combined raw university data before cleaning (752 KB) |
| `university_cleaned.csv` | CSV | Cleaned and standardized university dataset, ready for KPI engineering (714 KB) |

**Key Outputs:**
- `university_cleaned.csv` — the primary input for Milestone 2

---

## 6. Milestone 2 — KPI Engineering & Prototype

**Phase:** KPI calculation, dataset finalization, and prototype dashboard

| File | Type | Description |
|------|------|-------------|
| `generate_education_kpis.py` | Python script | Computes all six KPIs from the cleaned dataset and produces the final analytical dataset |
| `university_final_dataset.xlsx` | Excel Workbook | Final consolidated dataset including the `kpi_summary` sheet — primary data source for all Tableau dashboards (1.06 MB) |
| `dashboard_storyboard.pdf` | PDF | Dashboard layout storyboard and wireframes produced during design planning (247 KB) |
| `eduvision_prototype.twb` | Tableau Workbook | Unpackaged Tableau prototype (XML format) (342 KB) |
| `eduvision_prototype.twbx` | Tableau Packaged Workbook | Packaged Tableau prototype including embedded data (352 KB) |

**Key Outputs:**
- `university_final_dataset.xlsx` with `kpi_summary` sheet — used by all four dashboards

---

## 7. Milestone 3 — Dashboard Development

**Phase:** Production dashboard build in Tableau

| File | Type | Description |
|------|------|-------------|
| `EduVision_DV_1.twbx` | Tableau Packaged Workbook | **Production workbook** — the final four-dashboard suite (University Overview · Research Analytics · Student Analytics · Country Comparison) |
| `eduvision_prototype_v1.twbx` | Tableau Packaged Workbook | Intermediate dashboard version retained for reference (690 KB) |

**Key Output:**
- `EduVision_DV_1.twbx` — the primary deliverable of the project, submitted for final evaluation

---

## 8. Milestone 4 — Testing, Validation & Documentation

**Phase:** Module 7 QA testing and full project documentation

| File | Type | Description |
|------|------|-------------|
| `QA_Checklist.md` | Markdown | Module 7 QA checklist — KPI validation, ranking validation, dashboard interaction tests, educational metric tests, and visual validation results |
| `Dashboard_Testing_Report.md` | Markdown | Full dashboard testing report — detailed test results, issues identified and resolved, final QA status |
| `KPI_Defination.md` | Markdown | KPI definitions and calculation reference — source fields, normalization methods, interpretation, and missing value policy for all 6 KPIs |
| `Data_Sources.md` | Markdown | Dataset sources — origin, Kaggle URLs, local file names, field descriptions, and analytical domain mapping |
| `Dashboard_guide.md` | Markdown | Dashboard user guide — purpose, KPI cards, visualizations, filters, navigation, and cross-dashboard linking for all 4 dashboards |
| `Education_Analytics_Methodology.md` | Markdown | End-to-end analytics methodology — data collection through testing, covering all six project phases |
| `Project_Structure.md` | Markdown | This document — complete project folder structure reference |

---

## 9. Root-Level Files

| File | Description |
|------|-------------|
| `README.md` | Project overview and quick-start reference |
| `.gitignore` | Git ignore rules — excludes virtual environments, cache files, and temporary Tableau files |

---

## 10. Key File Relationships

```
data/raw/                          ← Source datasets (4 datasets)
      ↓
Milestone1/data_collection.py      ← Collects raw data
Milestone1/education_cleaning.ipynb← Cleans raw data
      ↓
Milestone1/university_cleaned.csv  ← Cleaned dataset
      ↓
Milestone2/generate_education_kpis.py ← Computes 6 KPIs
      ↓
Milestone2/university_final_dataset.xlsx (kpi_summary sheet)
      ↓
Milestone3/EduVision_DV_1.twbx     ← Production dashboards (4 dashboards)
      ↓
Milestone4/QA_Checklist.md         ← Module 7 test results
Milestone4/Dashboard_Testing_Report.md
```

---

## 11. Module 7 Documentation Index (Milestone 4)

| Document | Purpose | Status |
|----------|---------|--------|
| [`QA_Checklist.md`](QA_Checklist.md) | QA test results across all testing categories | ✅ Complete |
| [`Dashboard_Testing_Report.md`](Dashboard_Testing_Report.md) | Detailed dashboard testing report | ✅ Complete |
| [`KPI_Defination.md`](KPI_Defination.md) | KPI definitions and calculation reference | ✅ Complete |
| [`Data_Sources.md`](Data_Sources.md) | Dataset sources and field reference | ✅ Complete |
| [`Dashboard_guide.md`](Dashboard_guide.md) | Dashboard user and navigation guide | ✅ Complete |
| [`Education_Analytics_Methodology.md`](Education_Analytics_Methodology.md) | End-to-end project methodology | ✅ Complete |
| [`Project_Structure.md`](Project_Structure.md) | Project folder structure (this document) | ✅ Complete |

---

*EduVision\_DV — Milestone 4 · Project Structure · Report Date: 2026-09-30*
