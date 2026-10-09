# Milestone 4 — Testing and Delivery
### Weeks 7–8 · Modules 7 and 8

## Objective

Validate every KPI and ranking calculation, test all dashboard interactions, and deliver a
fully documented, portfolio-ready project.

---

## Module 7 — Testing and Validation

### Tasks completed

| Task | Evidence |
|---|---|
| Validate KPI calculations | 36 assertions across 6 KPIs — `QA_Checklist.md` §D |
| Verify ranking calculations | 4 rank formats parsed and verified — `QA_Checklist.md` §B |
| Test dashboard interactions | 6 interaction tests, 10 defects found and fixed — `Dashboard_Testing_Report.md` |
| Validate educational metrics | Coverage, country and cohort audits — `QA_Checklist.md` §C |

### Deliverables

| File | Description |
|---|---|
| `QA_Checklist.md` | 62 checks across data integrity, cleaning, integration, KPIs, reproducibility, build, interactions and structure |
| `Dashboard_Testing_Report.md` | Dashboard interaction testing, the defect log, and known behaviour |

### Evaluation — KPI accuracy above 95%

**36 of 36 assertions passed — 100%.**

| KPI | Coverage | Mean | Range | Result |
|---|---|---|---|---|
| Global Ranking Score | 600 | 41.84 | 20.8 – 100.0 | PASS |
| Academic Reputation Score | 1,503 | 20.29 | 1.3 – 100.0 | PASS |
| Research Impact Score | 1,503 | 23.50 | 1.0 – 100.0 | PASS |
| Faculty-to-Student Ratio | 195 | 17.44 | 3.8 – 58.0 | PASS |
| International Student % | 195 | 25.48% | 1% – 72% | PASS |
| Research Productivity Index (Proxy) | 195 | 61.23 | 34.9 – 100.0 | PASS |

### Evaluation — no major dashboard issues

Ten defects were found during interaction testing. All ten were fixed and retested; none
remain open. The defect log is in `Dashboard_Testing_Report.md` §3 — including the two
most instructive: a filter-merge bug that made a KPI card show the wrong country, and a
cross-filter that blanked two Top-N cards because a Top-1 calculation intersected with a
single-country filter returns nothing.

### Reproducibility evidence

| Check | Result |
|---|---|
| Python pipeline re-run end to end | Byte-identical dataset |
| `EduVision_DV_Colab.ipynb` executed | 18/18 cells, zero errors, identical export |
| `education_cleaning.ipynb` executed | 14/14 cells, identical `university_cleaned.csv` |

Two independent implementations producing the same bytes is the strongest available evidence
that the dashboard figures are not an artefact of one particular run.

---

## Module 8 — Documentation and Project Delivery

### Documentation

| Requirement | File |
|---|---|
| Dataset sources | `methodology.md` §2 · `Milestone 1/README.md` |
| KPI definitions | `methodology.md` §5 · `Milestone 2/README.md` |
| Dashboard guide | `dashboard_guide.md` · `Milestone 2/dashboard_storyboard.pdf` |
| Education analytics methodology | `methodology.md` |

### Required project organization

| Folder | Present | Contents |
|---|---|---|
| `/scripts` | ✅ | Cleaning, integration, KPI engineering, presentation builder |
| `/data` | ✅ | `raw/` sources and `processed/` intermediates |
| `/dashboard` | ✅ | Satisfied by `Milestone 3/` and the root workbook — see note |
| `/docs` | ✅ | Methodology, dashboard guide, testing report |

> **On `/dashboard`.** Rather than an extraneous top-level folder duplicating the workbook, the
> dashboard deliverables live in `Milestone 3/` (v1 workbook, screenshots) with the
> authoritative `EduVision_DV.twbx` at the project root. This keeps exactly one copy of the
> final workbook rather than two that can drift apart.

### Deployment

| Target | Status |
|---|---|
| GitHub Repository | Structure prepared; **not yet pushed** |
| Tableau Public | Documented in `Final Project/Dashboard_Link.txt` — manual publishing required |

### Deliverables

| File | Description |
|---|---|
| `methodology.md` | Technical methodology, join rules, KPI formulas |
| `dashboard_guide.md` | Tableau construction guide and design system |
| `../Final Project/Final_Presentation.pptx` | 20-slide project presentation with all four dashboards (and root sync copy) |
| `QA_Checklist.md` | Full QA record |
| `Dashboard_Testing_Report.md` | Dashboard testing record |

### Evaluation — fully documented project

Every KPI has a stated formula, source measure and coverage figure. Every data-handling
decision that could have been made differently — the base table choice, the five unmatched
institutions, the null policy, the proxy naming — is documented with its reasoning.

### Evaluation — portfolio-ready dashboard suite

Four dashboards at 1600 × 950 on a consistent dark theme, with working global filters and a
cross-filter action, exported at 3200 × 1900 for presentation use.

---

## Open items

| Item | Status |
|---|---|
| Publications analysis | Not deliverable — no source data. Documented, not substituted. |
| Multi-year trends | Partial — single-edition dataset; 2024→2025 rank comparison delivered |
| Tableau Public | Not attempted — optional |
| GitHub push | Pending your action |
