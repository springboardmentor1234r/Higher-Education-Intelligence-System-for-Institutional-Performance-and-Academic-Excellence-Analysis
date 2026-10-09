# EduVision_DV — Global Higher Education Performance Analytics
### Infosys Springboard Virtual Internship Project
### Kurapalli Sharmila

---

## 1. Project overview

**EduVision_DV** integrates two independent global university ranking systems — the **QS
World University Rankings 2025** and the **Times Higher Education (THE) World University
Rankings** — into a single validated dataset, and delivers four interactive Tableau Desktop
dashboards built on it.

The dataset covers **1,503 institutions across 106 countries**, measured on **six KPIs**.

## 2. Objective

Produce an end-to-end business intelligence pipeline — from raw, inconsistently-formatted
ranking exports to a reproducible master dataset to an executive dashboard suite — while
preserving analytical honesty about what the source data does and does not measure.

The project's governing rule: **no gap is ever filled with a guess.** Where a measurement
does not exist, it stays null, and the dashboards say so.

## 3. Data sources

| Source | Institutions | Columns | Role |
|---|---|---|---|
| QS World University Rankings 2025 | 1,503 | 28 | Base table — all rows preserved |
| Times Higher Education Rankings | 200 | 13 | Enrichment — 195 matched |

**Integration outcome:** 195 matched, 1,308 unmatched with THE fields left null, 5 THE
institutions deliberately excluded from matching (three absent from QS; two ambiguous
multi-campus systems).

## 4. Technology stack

| Layer | Tools |
|---|---|
| Data processing | Python 3.10+, pandas, numpy, openpyxl |
| Exploration | Jupyter / Google Colab, matplotlib, seaborn |
| Visualisation | **Tableau Desktop 2026.2** (macOS Apple silicon) |
| Formats | CSV, XLSX, TWBX, PNG, PDF, PPTX |

---

## 5. Milestones

### Milestone 1 — Data Collection and Preparation *(Weeks 1–2)*

Collects both ranking sources, audits completeness, then cleans, standardises and integrates
them into one table.

| Deliverable | File |
|---|---|
| Collection script | `Milestone 1/data_collection.py` |
| Merged raw structure | `Milestone 1/university_raw_data.csv` — 1,703 × 39 |
| Cleaning notebook | `Milestone 1/education_cleaning.ipynb` — executed, 14 cells |
| Cleaned dataset | `Milestone 1/university_cleaned.csv` — 1,503 × 43 |

**Evaluation:** QS completeness 96.87%, THE 100% (criterion > 95% ✅). Missing values on the
QS base fields 0.98% (criterion < 2% ✅).

### Milestone 2 — KPI Engineering and Dashboard Planning *(Weeks 3–4)*

Derives and validates the six KPIs, and specifies the four dashboards.

| Deliverable | File |
|---|---|
| KPI script | `Milestone 2/generate_education_kpis.py` |
| Master dataset | `Milestone 2/university_final_dataset.xlsx` — 1,503 × 52 |
| Design specification | `Milestone 2/dashboard_storyboard.pdf` |
| Prototype workbook | `Milestone 2/eduvision_prototype.twbx` *(reconstructed — see §11)* |

**Evaluation:** 36 of 36 KPI assertions passed ✅.

### Milestone 3 — Dashboard Development *(Weeks 5–6)*

Builds all four dashboards and integrates them with filters, navigation and cross-filtering.

| Deliverable | File |
|---|---|
| Module 5 workbook | `Milestone 3/eduvision_dashboard_v1.twbx` *(reconstructed — see §11)* |
| Final workbook | `EduVision_DV.twbx` *(project root)* |
| Screenshots | `Milestone 3/screenshots/` — 4 exports at 3200 × 1900 |

**Evaluation:** 4 dashboards, 24 worksheets, cross-filter action verified in both directions ✅.

### Milestone 4 — Testing and Delivery *(Weeks 7–8)*

Validates every calculation, tests every interaction, and documents the project.

| Deliverable | File |
|---|---|
| QA checklist | `Milestone 4/QA_Checklist.md` — 62 checks |
| Testing report | `Milestone 4/Dashboard_Testing_Report.md` |
| Methodology | `Milestone 4/methodology.md` |
| Dashboard guide | `Milestone 4/dashboard_guide.md` |
| Presentation | `Final Project/Final_Presentation.pptx` & `EduVision_DV_Presentation.pptx` |

**Evaluation:** 59 PASS, 0 FAIL, 3 documented limitations ✅.

### Final Project *(Final Submission Folder)*

Dedicated final submission package containing only the final presentation and dashboard link.

| Deliverable | File |
|---|---|
| Final Presentation | `Final Project/Final_Presentation.pptx` — 20-slide comprehensive deck |
| Dashboard Link | `Final Project/Dashboard_Link.txt` — instructions for manual Tableau Public publishing |

---

## 6. Final dashboards

| # | Dashboard | Accent | Contents |
|---|---|---|---|
| 1 | **University Overview** | `#00D2C4` | Top 10 by global score, region donut, world map, **Rank Movement 2024-2025** |
| 2 | **Research Analytics** | `#FF9F1C` | Impact vs productivity scatter, research-intensity box plots, top 10 research institutions |
| 3 | **Student Analytics** | `#2EC4B6` | Staffing ratio by region, internationalisation scatter, top 10 by enrolment |
| 4 | **Country Comparison** | `#00D2C4` | 106-country benchmarking table, choropleth, cross-filter action |

All four: fixed 1600 × 950 canvas, dark theme (`#12161A` canvas, `#1B2026` cards,
`#28323D` gridlines).

**Dashboard action:** `Filter_Country_From_Benchmarking` — selecting a country row filters
the map and the ranked-country count; clearing restores all 106.

---

## 7. KPI definitions

| # | KPI | Field | Source | Coverage | Mean |
|---|---|---|---|---|---|
| 1 | Global Ranking Score | `KPI_Global_Ranking_Score` | QS Overall Score | 600 | 41.84 |
| 2 | Academic Reputation Score | `KPI_Academic_Reputation_Score` | QS Academic Reputation | 1,503 | 20.29 |
| 3 | Research Impact Score | `KPI_Research_Impact_Score` | QS Citations per Faculty | 1,503 | 23.50 |
| 4 | Faculty-to-Student Ratio | `KPI_Faculty_to_Student_Ratio` | THE Students per Staff | 195 | 17.44 |
| 5 | International Student % | `KPI_International_Student_Pct` | THE International Students | 195 | 25.48% |
| 6 | Research Productivity Index **(Proxy)** | `KPI_Research_Productivity_Proxy` | THE Research Environment | 195 | 61.23 |

### ⚠ On KPI 6

The official specification calls this **Research Productivity Index**. This project
implements it as a **proxy** derived from the **THE Research Environment** score and labels
it **"Research Productivity (Proxy)"** everywhere it appears.

It is **not** THE's official Research Productivity metric, which is not present in the source
data. The label is deliberate and is not removed to match the specification's wording.

### Coverage is not uniform

Only two of the six KPIs describe all 1,503 institutions. Three describe the 195 matched to
THE; one describes the 600 QS actually scores. Every KPI card names its own population.

---

## 8. Testing and validation

| Layer | Result |
|---|---|
| KPI assertions | 36 / 36 passed (criterion > 95%) |
| Full QA checklist | 62 checks — 59 PASS, 0 FAIL, 3 documented limitations |
| Dashboard interactions | 6 tests; 10 defects found, fixed and retested |
| Pipeline reproducibility | Re-run produces byte-identical outputs |
| Notebook reproducibility | Two notebooks execute cleanly and reproduce the datasets exactly |

Full records: `Milestone 4/QA_Checklist.md` and `Milestone 4/Dashboard_Testing_Report.md`.

---

## 9. How to run

### Python pipeline

```bash
pip install -r requirements.txt

python scripts/data_cleaning.py       # raw → data/processed/*.csv
python scripts/data_integration.py    # → qs_the_integrated.csv
python scripts/kpi_engineering.py     # → university_final_dataset.csv / .xlsx
```

### Milestone scripts

```bash
python "Milestone 1/data_collection.py"
python "Milestone 2/generate_education_kpis.py"
```

### Notebooks

```bash
jupyter notebook "Milestone 1/education_cleaning.ipynb"
jupyter notebook notebooks/EduVision_DV_Colab.ipynb
```

In Google Colab: upload the notebook, then upload `infosys_dataset.csv` and
`Top_Universities_THE.xlsx` when prompted, and Run all.

### Dashboards

Open `EduVision_DV.twbx` in **Tableau Desktop 2026.2 or later**. The dataset is packaged
inside the workbook — no separate data connection is required.

---

## 10. Repository structure

```
EduVision_DV/
├── Milestone 1/                     Data collection and preparation
│   ├── data_collection.py
│   ├── university_raw_data.csv
│   ├── education_cleaning.ipynb
│   ├── university_cleaned.csv
│   └── README.md
├── Milestone 2/                     KPI engineering and dashboard planning
│   ├── generate_education_kpis.py
│   ├── university_final_dataset.xlsx / .csv
│   ├── dashboard_storyboard.pdf
│   ├── eduvision_prototype.twbx
│   └── README.md
├── Milestone 3/                     Dashboard development
│   ├── eduvision_dashboard_v1.twbx
│   ├── screenshots/                 4 dashboard exports
│   └── README.md
├── Milestone 4/                     Testing and delivery
│   ├── QA_Checklist.md
│   ├── Dashboard_Testing_Report.md
│   ├── methodology.md
│   ├── dashboard_guide.md
│   └── README.md
├── Final Project/                   Final delivery folder (submission only)
│   ├── Final_Presentation.pptx      20-slide executive presentation
│   └── Dashboard_Link.txt           Tableau Public publishing instructions
├── data/
│   ├── raw/                         QS and THE source exports
│   └── processed/                   Cleaned and integrated intermediates
├── scripts/                         Production pipeline & PPT builder
├── notebooks/                       Google Colab notebook
├── docs/                            Methodology, dashboard guide, testing report
├── EduVision_DV.twbx                ★ authoritative final workbook
├── EduVision_DV_Presentation.pptx    Final presentation (root copy)
├── university_final_dataset.csv / .xlsx
├── requirements.txt
└── README.md
```

---

## 11. Note on the milestone structure

This project was originally completed **end to end in a single build pass**. The milestone
folders above were assembled afterwards, from the real work and its real outputs, so the
repository reads against the official Week 1–8 milestone structure.

Two files are **reconstructions rather than historical snapshots**, and are labelled as such
in their milestone READMEs:

| File | What it actually is |
|---|---|
| `Milestone 2/eduvision_prototype.twbx` | A copy of the completed workbook, provided as the structural reference for the planned dashboards. No design-stage workbook was ever saved. |
| `Milestone 3/eduvision_dashboard_v1.twbx` | The completed workbook with Student Analytics and Country Comparison removed, leaving the two dashboards Module 5 specifies. The dashboards inside are genuine; the file did not exist during Weeks 5–6. |

Everything else in every milestone folder is an original project artifact or is derived
directly from one. No results, validation figures, screenshots or dashboards were fabricated.

---

## 12. Documented limitations

| Limitation | Why |
|---|---|
| **Publications analysis not delivered** | Neither source file contains a publications count. Only citation impact and research environment are available. Not substituted. |
| **Trend analysis limited to one year** | Single QS edition. `RANK_2024` vs `RANK_2025` is the only genuine temporal signal, and it is now on University Overview. |
| **Overall Score covers 600, not 1,503** | QS publishes it for its top 600 institutions only. |
| **Three KPIs cover 195 institutions** | They are THE-derived and only 195 QS institutions match THE. Never extrapolated. |
| **"Highest Research Impact" is a tie** | Nine institutions tie at exactly 100.0; Tableau surfaces the alphabetically first. |
| **Tableau Public not deployed** | Optional in the specification. |
