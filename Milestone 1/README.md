# Milestone 1 — Data Collection and Preparation
### Weeks 1–2 · Modules 1 and 2

## Objective

Collect the two source university ranking datasets, audit their completeness, and produce a
single cleaned and integrated table that the KPI stage can build on without further repair.

---

## Module 1 — University Data Collection

### Tasks completed

| Task | How it was done |
|---|---|
| Download QS Ranking dataset | QS World University Rankings 2025 export — 1,503 institutions × 28 columns |
| Download World University Ranking dataset | Times Higher Education export — 200 institutions × 13 columns |
| Collect university performance indicators | 9 QS score indicators and 6 THE performance pillars retained verbatim |
| Merge ranking datasets into a common structure | Both sources unioned into one long table tagged by `Source_Ranking_System` |

### Why a union, not a join, at this stage

Entity matching between QS and THE depends on standardised institution names, and
standardisation is a *cleaning* operation. Joining before cleaning would force name-matching
decisions on raw, inconsistently-spelled data. Module 1 therefore stacks both sources into a
common schema and leaves the join to Module 2, where a reliable key exists.

Ranks are kept as published strings at this stage (`15`, `621-630`, `1401+`).

### Deliverables

| File | Description |
|---|---|
| `data_collection.py` | Loads both sources, audits completeness, writes the merged raw structure |
| `university_raw_data.csv` | 1,703 rows × 39 columns — 1,503 QS + 200 THE in a common schema |

### Evaluation — dataset completeness above 95%

| Source | Completeness | Result |
|---|---|---|
| QS World University Rankings 2025 | **96.87%** | PASS |
| Times Higher Education Rankings | **100.00%** | PASS |

Completeness is reported per source universe. The QS figure includes `Overall_Score`, which
QS itself publishes only for its top 600 institutions.

---

## Module 2 — Data Cleaning & Transformation

### Tasks completed

| Task | Result |
|---|---|
| Remove duplicates | 0 found — QS publishes each institution once (verified, not assumed) |
| Standardize university names | Reviewed mapping table of 30 QS↔THE name pairs |
| Standardize country names | THE locations normalised onto the QS country vocabulary — 29 jurisdictions |
| Normalize ranking metrics | 4 published rank formats parsed to a single comparable numeric |
| Create Tableau-ready dataset | `university_cleaned.csv` — 1,503 × 43 |

### Rank normalisation rules

| Published | Parsed | Rule |
|---|---|---|
| `15` | 15.0 | plain integer |
| `15=` | 15.0 | tied rank, `=` stripped |
| `1201-1400` | 1300.5 | band midpoint |
| `1401+` | 1401.0 | open band floor |

### Integration outcome

- QS is the **base table**; all 1,503 rows survive a left join.
- **195** QS institutions matched to THE.
- **1,308** unmatched — THE-derived fields left strictly null.
- **5** THE institutions deliberately unmatched:
  - Karolinska Institute, Charité – Universitätsmedizin Berlin and Scuola Normale Superiore
    di Pisa are absent from the QS table.
  - University of Massachusetts and Indiana University are multi-campus systems that QS
    lists by campus; choosing one would invent a data point.

### Deliverables

| File | Description |
|---|---|
| `education_cleaning.ipynb` | Executed notebook — 14 code cells, zero errors, outputs saved |
| `university_cleaned.csv` | 1,503 × 43 cleaned and integrated dataset |

> The notebook contains the project's production cleaning and integration functions,
> extracted verbatim from `scripts/data_cleaning.py` and `scripts/data_integration.py`,
> so the milestone deliverable and the pipeline cannot drift apart.

### Evaluation — less than 2% missing values

| Measurement | Missing | Result |
|---|---|---|
| QS base fields, excluding `Overall_Score` | **0.98%** | PASS |
| QS base fields, including `Overall_Score` | 3.02% | QS publishes it for 600 institutions only |
| Whole joined rectangle | 30.37% | By design — see below |

The joined rectangle is 30% empty because 1,308 institutions legitimately have no THE
counterpart. Filling those cells would have met the criterion numerically while destroying
the dataset's honesty. Completeness is therefore measured on the universe the project
actually controls, and the THE coverage gap is stated openly everywhere it matters.

### Evaluation — consistent ranking indicators

All four published rank formats resolve to one numeric scale, verified across all 1,503 rows.

---

## Reproducibility

`education_cleaning.ipynb` was executed end to end and produced a `university_cleaned.csv`
**byte-identical** to the script pipeline's output (MD5 `08170c7dd4c1c4842d54f8fc9882328c`).

---

## How to run

```bash
python "Milestone 1/data_collection.py"          # → university_raw_data.csv
jupyter notebook "Milestone 1/education_cleaning.ipynb"   # → university_cleaned.csv
```

---

## Leads into Milestone 2

`university_cleaned.csv` is the direct input to `Milestone 2/generate_education_kpis.py`,
which derives the six education KPIs and exports the Tableau-ready master dataset.
