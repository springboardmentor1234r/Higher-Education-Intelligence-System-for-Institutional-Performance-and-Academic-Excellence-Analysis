# EduVision_DV — Data Collection & Data Integration

Higher Education Performance Analytics — ETL pipeline stages 1 & 3.

> Full pipeline: **Collection → Cleaning → Integration → Validation → Load to BI**
> This README documents **Collection** and **Integration** in detail. See
> `docs/BI_CONNECTION_GUIDE.md` for the downstream BI load stage, and
> `README_full_pipeline.md` for all 5 stages end to end.

---

## Table of Contents

- [Overview](#overview)
- [Stage 1 — Data Collection](#stage-1--data-collection)
- [Stage 3 — Data Integration](#stage-3--data-integration)
- [Known Limitations](#known-limitations)
- [Run It](#run-it)
- [Repository Structure](#repository-structure)

---

## Overview

| | |
|---|---|
| **Sources collected** | 7 real, independently published datasets |
| **Raw records collected** | 90,006 |
| **Ranking methodologies integrated** | 4 (THE, CWUR, ARWU/Shanghai, QS-style 2023) |
| **Distinct universities resolved** | 1,373 |
| **Countries in the indicator dimension** | 170 |
| **Final integrated warehouse size** | 100,175 rows across 7 tables |
| **Data quality (post-integration)** | 94.1% completeness |

All data is real and publicly released — not synthetic. Full provenance and
licensing is in [Data Collection](#stage-1--data-collection) below.

---

## Stage 1 — Data Collection

`scripts/data_collection.py`

Collects from **7 sources**, deliberately spanning 3 formats and 3
independent ranking methodologies plus 2 country-level indicator datasets —
this heterogeneity is what makes the Integration stage meaningful.

| Source file | Format | Rows | Years | Publisher / methodology |
|---|---|---:|---|---|
| `timesData.csv` | CSV | 2,603 | 2011–2016 | Times Higher Education (THE) |
| `cwurData.csv` | CSV | 2,200 | 2012–2015 | Center for World University Rankings (CWUR) |
| `shanghaiData.csv` | CSV | 4,897 | 2005–2015 | Academic Ranking of World Universities (ARWU / Shanghai) |
| `WorldUniversityRankings2023.csv` | CSV | 100 | 2023 | QS/THE-style ranking snapshot, top 100 |
| `school_and_country_table.csv` | CSV | 818 | — | University → country reference lookup |
| `education_expenditure_supplementary_data.csv` | CSV | 333 | 1995–2011 | Country-level education expenditure (% GDP) |
| `educational_attainment_supplementary_data.csv` | CSV | 79,055 | 1985–2015 | Country-level Barro-Lee educational attainment |

**Total: 90,006 real records.**

### Provenance & licensing

| Files | Origin | License |
|---|---|---|
| `timesData`, `cwurData`, `shanghaiData`, `school_and_country_table`, `education_expenditure_*`, `educational_attainment_*` | Originally compiled and released on Kaggle by user `mylesoneill` ("World University Rankings"), combining published THE / CWUR / ARWU rankings with World Bank / Barro-Lee indicators. Mirrored from [`arnaudbenard/university-ranking`](https://github.com/arnaudbenard/university-ranking). | **CC0 / public domain**, as released on Kaggle |
| `WorldUniversityRankings2023.csv` | 2023-edition ranking snapshot mirrored in a public coursework repo, [`nogibjj/IDS-Week7_MiniProject_us26`](https://github.com/nogibjj/IDS-Week7_MiniProject_us26) | Not confirmed CC0 — **demo/educational use only**; verify with the original publisher before commercial use |

> ⚠️ These are **historical rankings** (2005–2016, plus one 2023 snapshot) —
> not a live feed. Correct for trend analysis, methodology comparison, and
> BI demonstration; not a substitute for a current QS/THE subscription.

### What the collection script does

```bash
python3 scripts/data_collection.py
```

Verifies every raw file is present and prints its real shape — the files
themselves are fetched once into `data/raw/` and versioned there, since
these are static historical exports rather than a live API.

```
[verified] timesData.csv                                     2,603 rows x 14 cols
[verified] cwurData.csv                                       2,200 rows x 14 cols
[verified] shanghaiData.csv                                   4,897 rows x 11 cols
[verified] WorldUniversityRankings2023.csv                      100 rows x 13 cols
[verified] school_and_country_table.csv                         818 rows x  2 cols
[verified] education_expenditure_supplementary_data.csv         333 rows x  6 cols
[verified] educational_attainment_supplementary_data.csv     79,055 rows x 29 cols

Total real records collected across 7 sources: 90,006
```

---

## Stage 3 — Data Integration

`scripts/data_integration.py` *(runs after `data_cleaning.py`)*

THE, CWUR, and ARWU are three different organizations with three different
methodologies, three different score scales, and no shared university ID.
Integration is where that gets reconciled — without ever blending the three
methodologies into one fabricated "true" score.

### 3.1 Entity resolution — building `dim_university`

Every ranking source spells some university names differently. A naive
`merge()` on the raw name string silently drops real matches:

```python
"The University of Tokyo" == "University of Tokyo"   # False — same institution, two rows
```

**Fix — normalize before joining, then apply a small targeted alias table
for cases a general rule can't safely handle:**

```python
def norm_key(name):
    s = str(name).lower().strip()
    s = re.sub(r"^the\s+", "", s)      # drop a leading "The"
    s = re.sub(r"[^a-z0-9]", "", s)     # strip punctuation/whitespace
    return s

# General rules can overreach — stripping everything after a comma would
# fix "Nanyang Technological University, Singapore" but would ALSO wrongly
# merge "University of California, Berkeley" with "..., San Diego" (real,
# distinct campuses). That case gets a named alias instead of a rule:
NAME_ALIASES = {
    "nanyangtechnologicaluniversitysingapore": "nanyangtechnologicaluniversity",
}
```

`dim_university` is built from the **union** of every university name seen
across all 4 ranking sources + the school/country lookup table, keyed on
this normalized/aliased key.

```
[dim_university] 1,373 distinct universities resolved across 4 ranking sources + lookup table
[dim_university] 138 universities still missing a country after all lookups (10.1%) — left null, not guessed
```

### 3.2 Source-faithful fact tables — never blend methodologies

Each ranking source keeps its **own** fact table with its **own** original
columns and scale, linked to `dim_university` by foreign key:

```
fact_times     (university_id FK, year, world_rank, total_score, teaching, research, citations, income, …)
fact_cwur      (university_id FK, year, world_rank, quality_of_faculty, publications, citations, score, …)
fact_shanghai  (university_id FK, year, world_rank, alumni, award, hici, ns, pub, pcp, total_score, …)
fact_qs2023    (university_id FK, year, world_rank, overall_score, teaching_score, research_score, …)
```

```
[fact_times]     2,603 rows, 0 unmatched university_id
[fact_cwur]      2,200 rows, 0 unmatched
[fact_shanghai]  4,891 rows, 1 unmatched
[fact_qs2023]      100 rows, 0 unmatched
```

### 3.3 Cross-source comparable fact — `fact_ranking_core`

For charts that *do* want to compare methodologies side by side, each
source's raw score is independently **min-max rescaled to 0–100 within its
own year** (never across years, never across sources) — so "how did Harvard
rank across all 4 systems" is answerable without pretending THE's and
ARWU's raw scores are the same unit:

```python
def minmax_0_100(s):
    return (s - s.min()) / (s.max() - s.min()) * 100

core["score_0_100"] = core.groupby("year")["raw_score"].transform(minmax_0_100)
```

```
[fact_ranking_core] 9,793 rows spanning 4 sources, 2005-2023
```

### 3.4 Grain alignment — reshaping country indicators

`education_expenditure_*` and `educational_attainment_*` arrive **wide**
(one column per year). Ranking facts are **long** (one row per
university-year). Before they can share a query, the wide tables are melted
to match:

```python
long_df = wide_df.melt(id_vars=["country", "series_name"],
                        value_vars=year_columns,
                        var_name="year", value_name="value")
```

```
[fact_country_indicator] 79,215 rows (785 expenditure + 78,430 attainment), 170 countries
```

### 3.5 Join type — left join from the ranking backbone

A university missing from another source for a given year gets `NULL` for
those columns — **never a dropped or fabricated row**:

```python
merged = backbone.merge(other_source, on=["_key", "year"], how="left")
```

---

## Known Limitations

- **Real, explainable completeness gap**: `fact_ranking_core.score_0_100`
  is only 46.99% complete. THE reports rank *ranges* ("201–250") instead of
  a score below its top tier, and ARWU doesn't publish a composite score
  outside its top bracket — a genuine methodology limitation, not a
  pipeline bug. Those cells are left `NULL`, never estimated.
- **10.1% of universities have no resolved country** even after joining
  against the dedicated `school_and_country_table` lookup — some
  institutions in the ranking sources simply aren't in that reference table.
- **Entity resolution is name-based, not ID-based** — no source provides a
  stable university ID, so matching relies on normalized names + a small,
  manually maintained alias table. New unresolved variants may still exist;
  treat `dim_university` as reviewed-but-not-exhaustive.

---

## Run It

```bash
pip install pandas openpyxl
cd scripts
python3 data_collection.py     # verify the 7 real raw sources
python3 data_cleaning.py       # per-source cleaning (stage 2, not detailed above)
python3 data_integration.py    # entity resolution + fact tables  <- this README
python3 validate_data.py       # data quality report
python3 load_to_bi.py          # SQLite + Excel + CSV warehouse
```

or all at once:

```bash
python3 run_pipeline.py
```

---

## Repository Structure

```
eduvision_real/
├── scripts/
│   ├── data_collection.py      # Stage 1 — documented above
│   ├── data_cleaning.py        # Stage 2
│   ├── data_integration.py     # Stage 3 — documented above
│   ├── validate_data.py        # Stage 4
│   ├── load_to_bi.py           # Stage 5
│   └── run_pipeline.py         # runs all stages in order
├── data/
│   ├── raw/                    # 7 real source files (Stage 1 output)
│   ├── processed/              # clean_*.csv, dim_university.csv, fact_*.csv
│   └── warehouse/              # eduvision_real.db, .xlsx, *.csv (BI-ready)
├── docs/
│   └── BI_CONNECTION_GUIDE.md
└── README.md                   # this file
```
