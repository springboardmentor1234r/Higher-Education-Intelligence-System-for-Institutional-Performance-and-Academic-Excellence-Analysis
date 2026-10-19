# Folder Organization Notes — EduVision_DV Branch Structure

This document details the milestone categorization and file organization applied to the `sonia_vinod` branch in accordance with project guidelines.

## 1. Top-Level Folder Structure Overview

```
.
├── Milestone 1/          # Data Collection & Raw Preparation
├── Milestone 2/          # KPI Engineering & Dashboard Planning
├── Milestone 3/          # Dashboard Development & Data Modeling
├── Milestone 4/          # QA Testing & Delivery Verification
├── Final Project/        # Final PowerPoint Presentation & Public Links
└── docs/                 # Overarching documentation & folder organization notes
```

## 2. Milestone File Categorization Rationale

### Milestone 1: Data Collection & Preparation
- **Contents**: `data_collection.py`, `raw_data_validation_report.md`, `data_quality_report.md`, `raw_data_notes.md`, and `data/raw/` CSV files (`qs_2025.csv`, `the_2024.csv`, `wur_2023.csv`, `world_bank_edstats/`).
- **Rationale**: Captures all initial ingestion script routines, raw dataset validations, quality reports, and raw source datasets.
- **Git Handling**: Oversized dataset `EdStatsData.csv` (~326MB) is excluded via `.gitignore` to prevent git push errors, with full path and ingestion details documented in `raw_data_notes.md`.

### Milestone 2: KPI Engineering & Dashboard Planning
- **Contents**: `generate_education_kpis.py`, `kpi_definitions_and_formulas.md`, `data_dictionary.md`, `dashboard_storyboard.md`, `kpi_summary.csv`, `kpi_summary.xlsx`.
- **Rationale**: Encompasses mathematical KPI formulation, composite score logic, target dashboard visual planning/storyboarding, and generated KPI data summaries.

### Milestone 3: Dashboard Development & Data Modeling
- **Contents**: `02_data_cleaning.py`, `03_standardization.py`, `export_dashboard_json.py`, `cleaning_and_matching_methodology.md`, `data_model.md`, `tableau_build_guide.md`, `xml_dashboard_reference_fix.md`, `data/cleaned/` (star schema tables), `data/final/` (final integrated dataset), and `dashboard/` (`EduVision_DV.twbx`, `index.html`, `dashboard_data.json`).
- **Rationale**: Groups all core ETL cleaning scripts, country/university fuzzy entity resolution logic, relational star schema dimension/fact tables, Tableau build guides, interactive HTML/JS dashboard files, `.twbx` workbook, and the critical XML action interlinking bug fix report.

### Milestone 4: QA Testing & Delivery Verification
- **Contents**: `qa_checklist.md`, `dashboard_testing_report.md`, `05_validation.py`, `limitations.md`, `validation_results.md`.
- **Rationale**: Contains all testing routines, quality sign-offs, data boundary checks, validation scripts, edge-case limitations, and final delivery audit reports.

### Final Project: Internship Deliverables
- **Contents**: `EduVision_DV_Final_Presentation.pptx` and `README.md` (with live Tableau Public URL).
- **Rationale**: Dedicated exclusively to the final presentation slides and public deployment links for mentor review.

---
*Organized by Sonia Vinod for EduVision_DV Project Review.*
