# EduVision_DV — Higher Education Intelligence System

**Submitted by:** Priyanjal Yadav

Higher Education Performance Analytics project covering data collection, cleaning, standardization, KPI engineering, analytical data modelling, dashboard planning/presentation, validation, and documentation.

## Project scope

The project follows the supplied EduVision_DV requirements and organizes the analysis into four linked areas:

1. **University Overview** — ranking and academic performance
2. **Research Analytics** — research, citation and research productivity indicators
3. **Student Analytics** — students, students-per-staff and international student indicators
4. **Country Comparison** — country-level education indicators linked through `country_id`

The model uses `university_id`, `country_id`, `year`, and source-aware fact tables rather than blindly merging all datasets into one many-to-many table.

## Data sources

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- `world-education-data.csv` for country-level education indicators

> **Source note:** The supplied project brief specifies World Bank Education Statistics for the country-level dataset. The submitted package uses the provided `world-education-data.csv` replacement. If the evaluator requires the original World Bank EdStats file specifically, that source must be substituted before final submission.

## KPIs

The analytical model documents six KPIs:

- Global Ranking Score
- Research Impact Score
- Faculty-to-Student Ratio (students per staff, where available)
- International Student Percentage
- Academic Reputation Score
- Research Productivity Index

The Research Productivity Index is explicitly treated as a **derived analytical KPI**, not an official publisher metric. Missing components are not replaced with zero; available weights are renormalized.

## Repository contents

- `data_final/` — raw, cleaned, dimensional and fact tables
- `notebooks/` — loading, cleaning, standardization, KPI engineering and validation notebooks
- `scripts/` — reproducibility/validation scripts
- `Milestone_1/` through `Milestone_4/` — milestone evidence
- `Milestone_3/EduVision_DV_Dashboard.html` — interactive dashboard presentation
- `Milestone_2/university_final_dataset.xlsx` — analytical workbook
- `documentation/` — methods, model, dashboard plan and submission checklist

## Dashboard status

The package contains a four-dashboard interactive HTML presentation and Tableau-ready data tables. A native Tableau `.twbx` is **not** included because Tableau Desktop was not available in the preparation environment. If `.twbx` is mandatory, it must be created/saved in Tableau Desktop.

## Data-quality principles

- Raw datasets are retained separately from cleaned datasets.
- Duplicate rows are checked and removed where appropriate.
- University matching uses conservative normalized-name matching; aggressive fuzzy matching is not used to inflate match rates.
- Missing values are retained where the source does not provide a value.
- University-level and country-level data remain at their appropriate grains.

## AI-assisted development note

AI tools were used as development assistance for portions of data-processing code, documentation, structuring and review. The project is submitted by **Priyanjal Yadav**, who is responsible for reviewing the outputs, understanding the methodology, and validating the final submission. No claim is made that the project was produced entirely without AI assistance.

## License

See `LICENSE` in the repository.
