# Module 03 – KPI Engineering and Quality Audit

## Overview
Module 03 engineers six core higher-education Key Performance Indicators (KPIs) and executes automated data quality audits to guarantee structural integrity, constraint compliance, and BI readiness.

## Core KPIs Specification
1. **Global Ranking Score**: Direct overall institutional ranking score [0–100].
2. **Research Impact Score**: Citation influence and global research footprint [0–100].
3. **Faculty-to-Student Ratio**: Direct staff capacity ratio (students per staff member).
4. **International Student Percentage**: Campus diversity percentage ($(\text{International Students} / \text{Total Students}) \times 100$).
5. **Academic Reputation Score**: Peer academic survey reputation metric [0–100].
6. **Research Productivity Index (Tri-Pillar Model)**: Composite metric combining research score, citation impact, and international collaboration ($0.40 \cdot \text{Research} + 0.40 \cdot \text{Citations} + 0.20 \cdot \text{Network}$).

## Data Quality & Validation Suite
Automated execution of 21 integrity checks:
- **Primary Key Uniqueness**: `dim_university` and `dim_country`.
- **Foreign Key Integrity**: 100% match of fact records to dimension primary keys.
- **Metric Range Boundaries**: Scores constrained within [0–100], percentages within [0–100%].
- **Readiness Signal**: Generates `ready_for_tableau.txt` upon successful pass of all checks.

## Module Structure
```text
03_KPI_Engineering_and_Quality_Audit/
├── notebooks/
│   └── 04_kpi_engineering.ipynb
├── reports/
│   ├── kpi_summary_report.md
│   ├── kpi_validation_report.csv
│   ├── final_data_quality_report.csv
│   ├── final_data_quality_report.md
│   └── ready_for_tableau.txt
├── scripts/
│   ├── engineer_kpis.py
│   └── audit_data_quality.py
└── README.md
```

## Inputs & Outputs

### Inputs
- Star Schema tables from `Data/final/` (`dim_university`, `fact_university_performance`, `fact_research`, `fact_student`, `fact_country_education`)

### Outputs (`Data/final/` & `03_KPI_Engineering_and_Quality_Audit/reports/`)
- `kpi_university.csv`
- `kpi_validation_report.csv`
- `final_data_quality_report.md`
- `ready_for_tableau.txt`

## How to Run
```bash
python 03_KPI_Engineering_and_Quality_Audit/scripts/engineer_kpis.py
python 03_KPI_Engineering_and_Quality_Audit/scripts/audit_data_quality.py
```
