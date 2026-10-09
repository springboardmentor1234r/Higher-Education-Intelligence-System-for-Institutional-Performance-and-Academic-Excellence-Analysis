# EduVision_DV — QA Checklist
### Milestone 4 · Module 7 · Testing and Validation
### Infosys Springboard Virtual Internship Project

**Workbook under test:** `EduVision_DV.twbx`
**Dataset under test:** `university_final_dataset.csv` — 1,503 rows × 52 columns
**Verification date:** 29 September 2026

Every item below was executed against the project as it stands. Items are marked
**PASS**, **FAIL**, or **N/A — documented**. Nothing is marked PASS on the basis of
intention; where a requirement could not be met, it says so and says why.

---

## A. Source data integrity

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| A1 | QS source loads without error | 1,503 × 28 | 1,503 × 28 | **PASS** |
| A2 | THE source loads without error | 200 × 13 | 200 × 13 | **PASS** |
| A3 | Raw files unmodified by the pipeline | byte-identical | byte-identical | **PASS** |
| A4 | QS source completeness | > 95% | 96.87% | **PASS** |
| A5 | THE source completeness | > 95% | 100.00% | **PASS** |
| A6 | Duplicate institution names in QS | 0 | 0 | **PASS** |
| A7 | Duplicate institution names in final dataset | 0 | 0 | **PASS** |

## B. Cleaning and transformation

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| B1 | Plain integer ranks parsed | `15` → 15.0 | as expected | **PASS** |
| B2 | Tied ranks parsed | `15=` → 15.0 | as expected | **PASS** |
| B3 | Banded ranks parsed to midpoint | `1201-1400` → 1300.5 | as expected | **PASS** |
| B4 | Open bands parsed to floor | `1401+` → 1401.0 | as expected | **PASS** |
| B5 | THE country names normalised onto QS vocabulary | 29 jurisdictions | 29 | **PASS** |
| B6 | Missing values, QS base fields excl. `Overall_Score` | < 2% | 0.98% | **PASS** |
| B7 | Missing values, whole joined rectangle | — | 30.37% | **N/A — documented** (see note 1) |

> **Note 1.** The joined rectangle is 30.37% empty because 1,308 QS institutions have no THE
> counterpart and their THE-derived columns are deliberately null. The `< 2%` criterion is
> therefore measured on the QS base universe, where the project controls completeness.
> `Overall_Score` is excluded because QS publishes it for its top 600 institutions only.

## C. Integration and matching

| # | Check | Expected | Actual | Result |
|---|---|---|---|---|
| C1 | Base universe preserved | 1,503 rows | 1,503 | **PASS** |
| C2 | QS institutions matched to THE | 195 | 195 | **PASS** |
| C3 | Unmatched institutions left null | 1,308 | 1,308 | **PASS** |
| C4 | THE institutions deliberately unmatched | 5 | 5 | **PASS** |
| C5 | Zero-filling of unmatched THE fields | none | none | **PASS** |
| C6 | Mean or regression imputation | none | none | **PASS** |
| C7 | Distinct countries | 106 | 106 | **PASS** |
| C8 | United States institution count | 197 | 197 | **PASS** |

## D. KPI accuracy — evaluation criterion: above 95%

All six KPIs were verified on non-null count, minimum, maximum and mean.
**36 of 36 assertions passed — 100%.**

| # | KPI | Coverage | Min | Max | Mean | Result |
|---|---|---|---|---|---|---|
| D1 | Global Ranking Score | 600 | 20.8 | 100.0 | 41.84 | **PASS** |
| D2 | Academic Reputation Score | 1,503 | 1.3 | 100.0 | 20.29 | **PASS** |
| D3 | Research Impact Score | 1,503 | 1.0 | 100.0 | 23.50 | **PASS** |
| D4 | Faculty-to-Student Ratio | 195 | 3.8 | 58.0 | 17.44 | **PASS** |
| D5 | International Student % | 195 | 1.0% | 72.0% | 25.48% | **PASS** |
| D6 | Research Productivity Index (Proxy) | 195 | 34.9 | 100.0 | 61.23 | **PASS** |

| # | Check | Result |
|---|---|---|
| D7 | Research intensity split VH 1021 / HI 362 / MD 104 / LO 16 | **PASS** |
| D8 | KPI 6 labelled "(Proxy)" in every dashboard, legend and tooltip | **PASS** |
| D9 | KPI 6 never presented as THE's official Research Productivity metric | **PASS** |
| D10 | Faculty ratio displayed as `17.4 students/staff`, not `1:17.4` | **PASS** |

## E. Reproducibility

| # | Check | Result |
|---|---|---|
| E1 | `data_cleaning.py` → `data_integration.py` → `kpi_engineering.py` re-run end to end | **PASS** |
| E2 | Re-run produced byte-identical `university_final_dataset.csv` | **PASS** |
| E3 | Re-run produced byte-identical processed CSVs | **PASS** |
| E4 | `EduVision_DV_Colab.ipynb` executed — 18/18 code cells, zero errors | **PASS** |
| E5 | Notebook export identical to script pipeline output | **PASS** |
| E6 | `education_cleaning.ipynb` executed — 14/14 code cells, zero errors | **PASS** |
| E7 | `education_cleaning.ipynb` reproduced `university_cleaned.csv` byte-identically (MD5 `08170c7d…`) | **PASS** |
| E8 | `generate_education_kpis.py` output identical to the authoritative dataset | **PASS** |

## F. Dashboard build

| # | Check | Result |
|---|---|---|
| F1 | Four dashboards present in `EduVision_DV.twbx` | **PASS** |
| F2 | 24 worksheets present | **PASS** |
| F3 | Canvas fixed at 1600 × 950 on all four | **PASS** |
| F4 | Dark theme `#12161A` canvas / `#1B2026` cards applied | **PASS** |
| F5 | Gridlines and borders set to `#28323D` workbook-wide | **PASS** |
| F6 | Dashboard titles white and consistent across all four tabs | **PASS** |
| F7 | KPI cards fill their tiles uniformly | **PASS** |
| F8 | Top 10 axis framed 85–100 per the storyboard | **PASS** |
| F9 | Mandatory proxy footnote pinned to Research Analytics | **PASS** |
| F10 | Null indicators visible in-view rather than suppressed | **PASS** |

## G. Dashboard interactions

| # | Check | Result |
|---|---|---|
| G1 | `Filter_Country_From_Benchmarking` fires on select | **PASS** |
| G2 | Selecting a country filters the choropleth | **PASS** |
| G3 | Selecting a country updates Total Ranked Countries | **PASS** |
| G4 | Clearing the selection restores all 106 countries | **PASS** |
| G5 | Top-N reference KPI cards remain stable during cross-filter | **PASS** (see Testing Report §4) |
| G6 | Region / Location / Size / Focus filters present on all tabs | **PASS** |
| G7 | Colour legends render without stray measure entries | **PASS** |

## H. Deliverables and structure

| # | Check | Result |
|---|---|---|
| H1 | `/scripts`, `/data`, `/docs`, `/notebooks` present | **PASS** |
| H2 | Milestone 1 – Milestone 4 and Final Project folders present with READMEs/docs | **PASS** |
| H3 | `EduVision_DV.twbx` opens and remains the authoritative workbook | **PASS** |
| H4 | All three workbooks pass ZIP integrity check | **PASS** |
| H5 | Full backup taken before restructuring | **PASS** |
| H6 | Off-brief files excluded from the repository | **PASS** |

---

## Items NOT passed

| Requirement | Status | Reason |
|---|---|---|
| Publications analysis (M3 Module 5) | **NOT DELIVERED** | Neither source file contains a publications count. Only citation impact and research environment are available. Documented, not substituted. |
| Multi-year trend analysis | **PARTIAL** | The dataset is a single QS edition. Trend analysis is limited to the 2024→2025 rank comparison now shown on University Overview. |
| Tableau Public deployment | **NOT DONE** | Optional in the specification. Publishing requires an extract-based data source; not attempted. |

**Summary: 62 checks executed — 59 PASS, 0 FAIL, 3 documented limitations.**
