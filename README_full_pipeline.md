# EduVision_DV — Real Data Pipeline

Unlike the earlier synthetic demo, every number in this pipeline is **real,
publicly released** higher-education data — collected from 7 sources across
3 independent university-ranking methodologies (Times Higher Education,
CWUR, ARWU/Shanghai) plus a 2023 snapshot and 2 country-level UNESCO/World
Bank-style supplementary indicator sets.

**~90,000 real records collected → 100,216 rows loaded to BI** (integration
resolves 1,414 distinct universities and reshapes wide country tables to
long form, which increases row count while making the data queryable).

## Provenance & licensing — read this before reusing the data

| File | Origin | License |
|---|---|---|
| `timesData.csv`, `cwurData.csv`, `shanghaiData.csv`, `school_and_country_table.csv`, `education_expenditure_supplementary_data.csv`, `educational_attainment_supplementary_data.csv` | Originally compiled & released on Kaggle by user `mylesoneill` ("World University Rankings"), combining published THE / CWUR / ARWU rankings + World Bank/Barro-Lee indicators. Mirrored from [arnaudbenard/university-ranking](https://github.com/arnaudbenard/university-ranking) on GitHub. | CC0 / public domain as released on Kaggle |
| `WorldUniversityRankings2023.csv` | 2023-edition ranking snapshot mirrored in a public coursework repo, [nogibjj/IDS-Week7_MiniProject_us26](https://github.com/nogibjj/IDS-Week7_MiniProject_us26) | Not confirmed CC0 — treat as demo/educational use; verify with the original publisher before commercial use |

**These are historical rankings (2005–2016), plus one 2023 snapshot — not a
live feed.** That's fine for BI demonstration, trend analysis, and comparing
how the three methodologies (dis)agree, which is genuinely interesting
analytically. It is not current QS 2025/THE 2025 data.

## Run it

```bash
pip install pandas openpyxl
cd scripts
python3 data_collection.py      # verifies the 7 real raw files (data/raw/)
python3 data_cleaning.py        # per-source cleaning -> data/processed/clean_*.csv
python3 data_integration.py     # entity resolution + fact tables -> data/processed/
python3 validate_data.py        # -> data/processed/data_quality_report.(json|csv)
python3 load_to_bi.py           # -> data/warehouse/ (SQLite + Excel + CSV, 7 tables)
```

## What makes this "integration" real work

THE, CWUR, and ARWU are three different organizations with three different
methodologies and three different score scales. `data_integration.py`:

1. **Resolves university identity** across all 4 ranking sources + the
   school/country lookup table using a normalized join key — "Massachusetts
   Institute of Technology" in one source and slightly different formatting
   in another still resolve to the same `university_id`.
2. **Keeps each source's own numbers untouched** in its own fact table
   (`fact_times`, `fact_cwur`, `fact_shanghai`, `fact_qs2023`) — never blends
   methodologies into one fabricated "true" score.
3. **Builds one cross-source comparable table** (`fact_ranking_core`) by
   independently min-max rescaling each source's score to 0–100 *within its
   own year*, so you can chart "how did Harvard rank across all 4 systems"
   without pretending THE's and ARWU's raw scores are the same unit.
4. **Reshapes two wide country-level tables** (one column per year) into a
   single long `fact_country_indicator` table, joinable to `dim_university`
   by country name.

## Known real data-quality result

Actual validation run: **94.07% overall completeness.** The gap is a real,
explainable data limitation, not a pipeline bug: THE reports rank *ranges*
("201–250") instead of a score below the top tier, and ARWU doesn't publish
a composite score outside its top bracket. `fact_ranking_core.score_0_100`
is null for those rows rather than estimated.

## Warehouse output (`data/warehouse/`)

- `eduvision_real.db` — SQLite, 7 tables, indexed on university/year/source/country
- `EduVision_Real_BI_Workbook.xlsx` — same 7 tables as sheets
- `*.csv` — flat files, one per table

See `docs/BI_CONNECTION_GUIDE.md` for Power BI / Tableau / Looker Studio /
Metabase connection steps — identical process to the synthetic build, just
point at `eduvision_real.db` instead.

## Suggested visualizations this data actually supports

- **Cross-methodology agreement**: `fact_ranking_core` scatter — THE score
  vs. ARWU score for the same university/year, colored by country
  (do the rankings agree?)
- **Ranking volatility over time**: line chart of `world_rank` per
  university across 2011–2016 (THE) or 2005–2015 (ARWU)
- **Country-level context**: `fact_country_indicator` — tertiary education
  attainment or government expenditure trend, filterable by country, next
  to that country's average university ranking
- **Methodology spread**: for universities covered by all 4 sources, a box
  plot of `score_0_100` shows how much a university's apparent standing
  depends on which ranking you trust
