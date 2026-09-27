# EduVision_DV — Higher Education Intelligence System
## Project Brief for Agent Execution

## 0. Objective
Build a complete, reproducible analytics pipeline and an interactive dashboard suite from four public higher-education datasets. Output: cleaned data model, six documented KPIs, and four interlinked dashboards (University Overview, Research Analytics, Student Analytics, Country Comparison), plus full documentation.

Since native Tableau automation isn't available to an AI agent, build the working dashboard as a **self-contained interactive web app** (HTML/CSS/JS, e.g. using Plotly, D3, or Chart.js) that replicates everything a Tableau workbook would do: KPI cards, charts, cross-filters, and dashboard-to-dashboard navigation that carries the selected university/country forward. Also produce a **Tableau build guide** (calculated field formulas, chart specs, filter/action setup) so the same data can be rebuilt in Tableau Desktop manually if needed.

## 1. Inputs (already in raw/)
- `qs_2025.csv` — QS World University Rankings 2025 (~1,500 universities): institution name, location/region, academic reputation score, employer reputation score, faculty/student score, citations-per-faculty score, international faculty/student scores, international research network score, employment outcomes score, sustainability score, overall score, rank.
- `the_2024.csv` — THE World University Rankings 2024: teaching, research, citations, international outlook, industry income, student/staff ratio, international students.
- `wur_2023.csv` — World University Rankings 2023 (~1,800 universities, 104 countries): rank, name, location, no. of students, students per staff, international students %, female:male ratio, overall/teaching/research/citations/industry income/international outlook scores.
- `world_bank_edstats/` — World Bank Education Statistics (EdStats), delivered as a folder of related files rather than one CSV. Load and join these together rather than treating any single file as the whole dataset:
  - `EdStatsData.csv` — the main file: country x year x indicator values, long format, 4,000+ indicators. This is the primary source for fact_country_education.
  - `EdStatsCountry.csv` — country metadata (region, income group, country codes). Use this to help build/validate dim_country, not just the raw country strings in EdStatsData.csv.
  - `EdStatsSeries.csv` — indicator metadata: what each indicator_code in EdStatsData.csv actually means (full name, definition, source). Use this to pick and label the specific indicators for Country Comparison (expenditure, enrollment, literacy, completion, tertiary education, teacher indicators) rather than guessing from indicator codes alone.
  - `EdStatsCountry-Series.csv` — cross-reference of which series apply to which countries. Optional, use if useful for filtering.
  - `EdStatsFootNote.csv` — footnotes/caveats on specific data points. Optional, document if a chosen indicator has a relevant footnote.
  - Do not use `EdStatsEXCEL.xlsx` if present — it duplicates `EdStatsData.csv`.

## 2. Non-negotiable rules
- Do not force-match universities across datasets to inflate match rate. Fuzzy matching is for candidate identification only; final merges need logic/manual validation. A false match is worse than a missing match.
- Do not fabricate or zero-fill missing scores. Missing ≠ zero. Document what's missing and why, rather than inventing values.
- Do not map an unrelated field to a KPI because the name looks similar (e.g., never map Sustainability Score → Research Productivity Index).
- Do not treat a "score" as if it were an actual percentage or ratio unless the source dataset actually provides that percentage/ratio.
- Keep raw files untouched. Write all cleaned output to separate files.
- A university belongs to a country; country-level data joins via country_id, not by re-matching every university row against the country dataset.
- No giant many-to-many join across all four datasets — build a dimensional model instead (see below).

## 3. Data model
```
dim_university (university_id, university_name, country_id, country_name, region)
dim_country (country_id, country_name)
fact_university_performance (university_id, year, global_rank, overall_score, academic_reputation, employer_reputation)
fact_research (university_id, year, research_score, citation_score, research_impact, research_productivity)
fact_student (university_id, year, total_students, students_per_staff, international_students, international_student_percentage)
fact_country_education (country_id, year, indicator, value)
```
- `university_id` and `country_id` are the join keys everywhere — never join on raw name strings alone.
- Standardize university names (lowercase, strip punctuation, collapse whitespace) before matching; standardize country names to one canonical form (e.g. collapse "USA"/"United States"/"United States of America"/"US" into one row).

## 4. Six KPIs — each needs a documented source, formula, unit, normalization, missing-value treatment, and interpretation
1. **Global Ranking Score** — from QS/THE overall score or rank.
2. **Research Impact Score** — from citations-per-faculty / citation-related fields (document exact source columns used).
3. **Faculty-to-Student Ratio** — prefer the actual ratio (e.g., students-per-staff) over a proxy "score"; label clearly if only a score is available.
4. **International Student Percentage** — use only if the source gives an actual percentage; otherwise label it a "score," not a percentage.
5. **Academic Reputation Score** — from QS Academic Reputation Score.
6. **Research Productivity Index** — a derived, documented composite (e.g., weighted normalization of research score + citation performance + a size/output measure). Do not use Sustainability Score. Finalize and document the exact weights used.

## 5. Pipeline order
1. Load and inspect each raw file (shape, dtypes, missing %, duplicates) — write a validation report per dataset.
2. Standardize column names, university names, country names.
3. Build `dim_university` and `dim_country` with generated IDs.
4. Check duplicate universities/countries before removing anything.
5. Convert numeric fields with `pd.to_numeric(..., errors="coerce")`.
6. Build fact tables, joining only on IDs.
7. Calculate the six KPIs into a KPI table (one row per university).
8. Run a final validation pass (row counts, null checks, duplicate ID checks) and write a short data-quality report.
9. Export cleaned/final files (CSV or XLSX) to a `cleaned/` and `final/` folder — never overwrite raw/.

## 6. Dashboards (build as one interactive web app with 4 linked views + a home/nav layer)
- **University Overview** (landing): KPI cards (global rank, overall score, academic reputation, research impact, faculty/student ratio, international students), ranking table, distribution by region, filters for University/Country/Region/Year.
- **Research Analytics**: research score, citations, research impact, research productivity index, top research institutions, trends. Filters: University/Country/Year.
- **Student Analytics**: total students, international students %, students-per-staff, diversity/gender ratio, comparisons. Filters: University/Country/Year.
- **Country Comparison**: country-level aggregates (# universities, avg ranking, avg research performance, education indicators, trends). Filters: Country/Region/Year.

**Interlinking requirement**: selecting a university on one dashboard and navigating to another should carry that university (and its country, for Country Comparison) forward as the active filter — this is the core "interlinked" requirement, not just four separate charts in one file.

## 7. Deliverables to produce
```
data/
  raw/                  (untouched originals)
  cleaned/              (dim_*, fact_* tables)
  final/                (eduvision_final_dataset + kpi table)
notebooks_or_scripts/
  01_data_loading
  02_data_cleaning
  03_standardization
  04_kpi_engineering
  05_validation
dashboard/
  index.html (+ assets)  — the interactive web dashboard
docs/
  data_dictionary.md
  cleaning_and_matching_methodology.md
  kpi_definitions_and_formulas.md
  data_model.md
  tableau_build_guide.md   — field-by-field instructions + calculated-field formulas to rebuild this in Tableau Desktop
  limitations.md
```

## 8. Definition of done
- All 6 KPIs calculated, each with source/formula documented.
- No fabricated values anywhere; missing data is labeled, not filled.
- Dashboard runs standalone in a browser with working filters and cross-dashboard navigation.
- Validation report shows 0 duplicate IDs, numeric fields properly typed, referential integrity between fact tables and dim_university/dim_country.
- Tableau build guide is complete enough that someone could reproduce the same dashboards manually in Tableau Desktop.
