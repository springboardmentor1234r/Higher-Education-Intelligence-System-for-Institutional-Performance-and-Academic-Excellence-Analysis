# Milestone 3 — Dashboard Development
### Weeks 5–6 · Modules 5 and 6

## Objective

Build all four dashboards in Tableau Desktop against the Milestone 2 storyboard, then
integrate them into one workbook with working filters, navigation and cross-filtering.

---

## Module 5 — University Overview and Research Analytics

### University Overview

| Required coverage | How it is delivered | Status |
|---|---|---|
| Top university rankings | Top 10 Universities by Global Score, axis framed 85–100 | ✅ |
| Global university distribution | Geographic Distribution map, all 1,503 institutions | ✅ |
| Academic reputation analysis | Average Global Score KPI card, computed over the 600 scored institutions | ✅ |
| University performance trends | **Rank Movement 2024-2025** — see below | ✅ |
| Institutional comparison | Top 10 bar chart plus the Region donut over all 1,503 | ✅ |

#### Rank Movement 2024-2025 — how the trend requirement is met

The dataset is a single QS edition, so multi-year trend analysis is not possible from it.
The one genuine temporal signal available is `RANK_2024` alongside `RANK_2025`, both
published in the same source file.

Two calculated fields were added to the workbook:

```
Rank 2024 Numeric =
  IF ISNULL([Rank 2024]) THEN NULL
  ELSEIF CONTAINS([Rank 2024], "+") THEN FLOAT(REPLACE([Rank 2024], "+", ""))
  ELSEIF CONTAINS([Rank 2024], "-") THEN
     (FLOAT(SPLIT([Rank 2024], "-", 1)) + FLOAT(SPLIT([Rank 2024], "-", 2))) / 2
  ELSE FLOAT(REPLACE([Rank 2024], "=", ""))
  END

Rank Change 2024-2025 = [Rank 2024 Numeric] - [Rank 2025 Numeric]
```

**Interpretation:** positive = improved, negative = declined, zero = no change.

Computable for **1,482 of 1,503** institutions (98.6%); 21 have no 2024 rank.
Across the full dataset: **461 improved, 610 declined, 411 unchanged.**

The published view is scoped to the QS top 10, all of which carry exact ranks in both
editions, so no band-midpoint artefacts appear. It shows Caltech +5 and Imperial College
London +4 as the risers, Cambridge −3 and Stanford −1 as the fallers, with six unchanged.

No historical data was fabricated. Only `RANK_2024` and `RANK_2025`, both already in the
source dataset, were used.

### Research Analytics

| Required coverage | How it is delivered | Status |
|---|---|---|
| Publications analysis | **Not delivered** — see limitations | ❌ |
| Citation performance | Average Citation Score KPI plus Top 10 by research impact | ✅ |
| Research productivity trends | Research Impact vs Productivity scatter, 195 matched institutions | ✅ |
| Top research institutions | Top 10 Research Institutions, paired impact/productivity bars | ✅ |
| Research impact comparison | Research Intensity Comparison box plots across VH / HI / MD / LO | ✅ |

### Deliverable

| File | Description |
|---|---|
| `eduvision_dashboard_v1.twbx` | University Overview + Research Analytics only |

### ⚠ Note on `eduvision_dashboard_v1.twbx` — reconstructed artifact

**This workbook is a reconstruction, not a historical snapshot.**

The project was delivered in a single end-to-end build pass, so no two-dashboard interim
workbook was saved during Weeks 5–6. This file was produced from the completed workbook by
removing the Student Analytics and Country Comparison dashboards, leaving exactly the two
dashboards Module 5 calls for.

The dashboards inside it are the genuine, finished dashboards — nothing was re-built or
simplified — but the file itself did not exist at the time Module 5 describes. It is not
presented as evidence of staged development.

Because Country Comparison is absent from this copy, the
`Filter_Country_From_Benchmarking` action is not present in it either. That action lives in
the Module 6 deliverable.

---

## Module 6 — Student Analytics, Country Comparison, and integration

### Student Analytics

| Required coverage | How it is delivered | Status |
|---|---|---|
| International student analysis | Average International Student % KPI, 195 matched | ✅ |
| Faculty-to-student ratio analysis | Avg Students per Staff by Region — Oceania 30.6 vs Africa 13.0 | ✅ |
| Student diversity trends | Internationalization Scatter — intl % against staffing ratio | ⚠ single-edition |
| Enrollment comparisons | Top 10 Universities by Enrollment — Toronto 80,107 FTE | ✅ |
| Student distribution analysis | Total FTE Student Headcount — 5.46M across 195 | ✅ |

### Country Comparison

| Required coverage | How it is delivered | Status |
|---|---|---|
| Country ranking comparison | Country Benchmarking Table — all 106 countries on 4 measures | ✅ |
| Education performance benchmarking | Colour-graded heat table for outlier detection | ✅ |
| Regional education trends | Region filter applied across the tab | ⚠ single-edition |
| Top performing countries | Top Country by Avg QS Score (Hong Kong SAR) and Most Represented (US, 197) | ✅ |

### Dashboard integration

| Requirement | Implementation | Status |
|---|---|---|
| Global filters | Region, Location, Size, Focus applied across each tab's views | ✅ |
| Navigation controls | Four dashboard tabs, fixed 1600 × 950 canvas | ✅ |
| Parameter actions | `Filter_Country_From_Benchmarking` — filter action on Select, Show all values on clear | ✅ |
| Dashboard linking | Benchmarking table → choropleth + ranked-country count | ✅ |

### Deliverables

| File | Description |
|---|---|
| `EduVision_DV.twbx` | *(at the project root)* — the authoritative final workbook: 4 dashboards, 24 worksheets, 10 calculated fields, 1 cross-filter action |
| `screenshots/` | Four dashboard exports at 3200 × 1900 |

The final workbook is kept at the project root rather than duplicated here, so there is
exactly one authoritative copy.

### Evaluation

- **Interactive visualizations operational** — cross-filter tested in both directions; see
  `Milestone 4/Dashboard_Testing_Report.md` §2.
- **Ranking metrics validated** — 36 of 36 KPI assertions passed.
- **All dashboards integrated** — 4 dashboards verified present in the packaged workbook.
- **Navigation and filters functioning** — 10 defects found during testing, all fixed and
  retested.

---

## Limitations, stated rather than worked around

**Publications analysis cannot be delivered.** Publication-volume analysis was not implemented because the available QS/THE source data does not provide a directly comparable publication-count field. In strict adherence to analytical honesty, no publication metric was fabricated. The available research measures are citation impact (QS Citations per Faculty) and research environment (THE Research Environment proxy).

**Trend analysis is limited to one year-on-year comparison.** The dataset is a single QS
edition. `RANK_2024` versus `RANK_2025` is the only genuine temporal dimension available,
and it is now shown on University Overview.

---

## Leads into Milestone 4

The integrated workbook is the object under test in Milestone 4, which validates KPI
calculations, verifies rank calculations and tests every dashboard interaction.
