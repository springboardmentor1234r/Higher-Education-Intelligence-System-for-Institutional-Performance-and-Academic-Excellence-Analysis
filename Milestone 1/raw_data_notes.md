# Raw Data & Collection Notes — Milestone 1

## Overview
Milestone 1 encompasses raw data collection, ingestion, initial validation, and quality assessment across international higher education and global macroeconomic/educational datasets.

## Datasets Ingested
1. **QS World University Rankings 2025 (`qs_2025.csv`)**: 1,500+ university rankings with scores for academic reputation, citations, and international metrics.
2. **Times Higher Education 2024 (`the_2024.csv`)**: 1,900+ institutions with metrics across teaching, research environment, research quality, industry impact, and international outlook.
3. **World University Rankings 2023 (`wur_2023.csv`)**: Supplementary international university indicators.
4. **World Bank EdStats Database (`world_bank_edstats/`)**: Country-level educational indicator series including tertiary enrollment rates (`SE.TER.ENRR`) and government expenditure on education as % of GDP (`SE.XPD.TOTL.GD.ZS`).

> [!NOTE]
> Large raw data file `EdStatsData.csv` (~326MB) exceeds GitHub single file limits and is gitignored per `.gitignore`. It is ingested locally via `data_collection.py`.

## Files Included in Milestone 1
- `data_collection.py`: Python script for automated multi-source dataset loading and schema audit.
- `raw_data_validation_report.md`: Complete audit of column types, null counts, and candidate key candidate integrity.
- `data_quality_report.md`: Quality metrics, outlier detection, and initial dataset readiness evaluation.
- `data/raw/`: Raw CSV files and World Bank metadata series.
