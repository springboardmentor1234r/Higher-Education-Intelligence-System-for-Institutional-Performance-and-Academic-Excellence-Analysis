# Milestone 2 — KPI Engineering and Dashboard Planning
### Weeks 3–4 · Modules 3 and 4

## Objective

Derive the six required education KPIs from the cleaned dataset, validate every one of them,
and produce the approved design specification the dashboards will be built against.

---

## Module 3 — Education KPI Engineering

### The six KPIs

| # | Specification name | Field in the dataset | Source measure | Coverage |
|---|---|---|---|---|
| 1 | Global Ranking Score | `KPI_Global_Ranking_Score` | QS Overall Score | 600 |
| 2 | Research Impact Score | `KPI_Research_Impact_Score` | QS Citations per Faculty | 1,503 |
| 3 | Faculty-to-Student Ratio | `KPI_Faculty_to_Student_Ratio` | THE Students per Staff | 195 |
| 4 | International Student Percentage | `KPI_International_Student_Pct` | THE International Students | 195 |
| 5 | Academic Reputation Score | `KPI_Academic_Reputation_Score` | QS Academic Reputation | 1,503 |
| 6 | Research Productivity Index | `KPI_Research_Productivity_Proxy` | THE Research Environment | 195 |

### KPI 6 — naming, stated plainly

The official specification calls this metric **Research Productivity Index**. In this project
it is implemented as `KPI_Research_Productivity_Proxy` and surfaced everywhere — dashboards,
legends, tooltips, documentation — as **"Research Productivity (Proxy)"**.

It is derived from the **THE Research Environment** score. It is **not** Times Higher
Education's official Research Productivity metric, which is not present in the source data.
The "(Proxy)" label is deliberate and is not removed to match the specification's wording.
Research Analytics carries a permanent on-dashboard footnote saying so.

### Coverage is not uniform, and the dashboards say so

Two KPIs describe all 1,503 institutions. Three describe the 195 matched to THE. One
describes the 600 QS actually scores. Every KPI card on the dashboards names its own
population, so no figure implies coverage it does not have.

### Deliverables

| File | Description |
|---|---|
| `generate_education_kpis.py` | Derives and validates all six KPIs; imports `scripts/kpi_engineering.py` so the milestone deliverable and the pipeline cannot diverge |
| `university_final_dataset.xlsx` | Tableau-ready master dataset — 1,503 × 52 |
| `university_final_dataset.csv` | Same dataset in CSV, the format the workbook connects to |

### Evaluation — all KPIs correctly calculated

36 assertions (non-null count, minimum, maximum and mean for each of the six KPIs) —
**36 passed, 0 failed**. Output verified byte-identical to the authoritative
`university_final_dataset.csv` at the project root.

### Evaluation — dataset optimized for Tableau

- Flat single-table structure, one row per institution, no joins required at report time.
- Numeric ranks pre-parsed; no string parsing in calculated fields.
- Three `Display_*` tooltip fields render an explicit "Sourced from THE (Data not available)"
  label instead of blank cells.
- Default number formats set on every KPI (decimal places, `%` suffix, Millions for FTE).

---

## Module 4 — Dashboard Planning & Prototyping

### Dashboards planned

| Dashboard | Accent | Purpose |
|---|---|---|
| University Overview | `#00D2C4` | Macro rankings, geographic spread, regional distribution, 2024–2025 rank movement |
| Research Analytics | `#FF9F1C` | Impact against productivity, research-intensity comparison, top research institutions |
| Student Analytics | `#2EC4B6` | Staffing ratios, internationalisation, enrolment scale |
| Country Comparison | `#00D2C4` | National benchmarking table, choropleth, cross-filter interaction |

### Defined in the storyboard

- **Filters** — Region, Location (Only Relevant Values), Size, Focus
- **Navigation** — four dashboard tabs at a fixed 1600 × 950 canvas
- **Dashboard action** — `Filter_Country_From_Benchmarking`: source Country Benchmarking
  Table, target Geographic Country Map, run on Select, clearing shows all values
- **Interactive comparisons** — country-level cross-filtering, region filtering applied
  simultaneously across every view on a tab

### Deliverables

| File | Description |
|---|---|
| `dashboard_storyboard.pdf` | Approved design specification — palette, canvas, KPI cards, chart types, filters, actions |
| `eduvision_prototype.twbx` | Prototype workbook — see the note below |

### ⚠ Note on `eduvision_prototype.twbx` — reconstructed artifact

**This workbook is a reconstruction, not a historical snapshot.**

The project was originally delivered in a single end-to-end build pass, so no separate
design-stage workbook was ever saved during Weeks 3–4. This file is a copy of the completed
workbook, provided as the structural reference for the four planned dashboards, their
filters, navigation and the cross-filter action.

It is **not** evidence of a prototype built before the final dashboards, and it is not
presented as such. The authoritative deliverable remains `EduVision_DV.twbx` at the project
root.

### Evaluation — prototype functionality verified

The workbook passes a ZIP integrity check and opens in Tableau Desktop 2026.2 with all four
dashboards, 24 worksheets and the `Filter_Country_From_Benchmarking` action present.

---

## How to run

```bash
python "Milestone 2/generate_education_kpis.py"
```

---

## Leads into Milestone 3

`university_final_dataset.csv` is the data source the Tableau workbook connects to, and
`dashboard_storyboard.pdf` is the specification Milestone 3 builds against.
