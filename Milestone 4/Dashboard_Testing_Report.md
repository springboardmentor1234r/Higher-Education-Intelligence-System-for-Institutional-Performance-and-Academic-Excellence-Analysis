# EduVision_DV — Dashboard Testing Report
### Milestone 4 · Module 7 · Testing and Validation
### Infosys Springboard Virtual Internship Project

**Workbook:** `EduVision_DV.twbx` (Tableau Desktop 2026.2, macOS Apple silicon)
**Test date:** 29 September 2026
**Method:** manual interaction testing in Tableau Desktop, plus programmatic
verification of the packaged workbook and the underlying dataset.

This report covers **dashboard behaviour**. Data-layer validation — the 36 KPI
assertions, match audit and null-policy audit — is recorded separately in
`docs/testing_report.md` and summarised in `QA_Checklist.md`.

---

## 1. Scope

| Dashboard | Canvas | Worksheets | Filters | Actions |
|---|---|---|---|---|
| University Overview | 1600 × 950 | 7 | Region, Location, Size, Focus | — |
| Research Analytics | 1600 × 950 | 6 | Region, Location | — |
| Student Analytics | 1600 × 950 | 6 | Region, Location, Size, Focus | — |
| Country Comparison | 1600 × 950 | 5 | — | `Filter_Country_From_Benchmarking` |

Workbook totals verified programmatically from the packaged `.twb`:
**4 dashboards, 24 worksheets, 2 actions** (one authored, one Tableau-generated).

---

## 2. Cross-filter action test — `Filter_Country_From_Benchmarking`

**Requirement:** selecting a country row in the benchmarking table filters the
choropleth and the associated country KPIs; clearing restores all values.

| Step | Action | Expected | Observed | Result |
|---|---|---|---|---|
| 2.1 | Click the Kazakhstan row | Map filters to Kazakhstan | Map zoomed to Kazakhstan only | **PASS** |
| 2.2 | — | Total Ranked Countries updates | Dropped 106 → 1 | **PASS** |
| 2.3 | Click the same row again | Selection clears | Selection cleared | **PASS** |
| 2.4 | — | All countries restored | Map returned to 106 countries | **PASS** |
| 2.5 | — | KPI restored | Total Ranked Countries returned to 106 | **PASS** |
| 2.6 | Repeat with Paraguay | Same behaviour | Same behaviour | **PASS** |

Action configuration verified: **Run on Select**, **Clearing the selection → Show all values**.

---

## 3. Defects found and fixed

All defects below were found during testing and corrected in the workbook. They are
recorded because a testing report that finds nothing is not a testing report.

| # | Defect | Root cause | Fix | Retest |
|---|---|---|---|---|
| 3.1 | "Most Represented Country" card showed a wrong country when filters were applied | Tableau merges filters on the same field, so the shared `Location` filter overrode the card's own Top-1 filter | Created a separate `Country` field and rebuilt both country KPI cards on it with their own Top-1 filters | Shows United States / 197 and Hong Kong SAR consistently — **PASS** |
| 3.2 | Two KPI cards went blank when a country was selected | Action applied a `Location` filter to cards whose Top-1 calculation is computed over the whole dataset, so the intersection returned no rows | Retargeted the action to the map and the ranked-country count only | Cards remain populated throughout the interaction — **PASS** |
| 3.3 | Region donut rendered as a solid pie on the dashboard | Inner "hole" mark was a Circle (fixed point size) while the outer mark was a Pie (scales with cell size) | Converted the inner mark to Pie | Donut renders correctly at dashboard scale — **PASS** |
| 3.4 | Top 10 Research Institutions showed only 4 rows | Sheet fit mode plus a visible Measure Names row header consumed vertical space | Set Fit → Entire View and hid the Measure Names header | All 10 institutions visible — **PASS** |
| 3.5 | A stray full-canvas world map bled through Student Analytics | An unused tiled container held a duplicate Geographic Distribution sheet | Removed the container | Dashboard renders cleanly — **PASS** |
| 3.6 | Country benchmarking table values unreadable | White text on a light heat-map gradient | Set pane font to `#12161A` | All values legible across the gradient — **PASS** |
| 3.7 | Dashboard titles on three tabs rendered nearly invisible | Title text objects sat at 0% background opacity | Gave each a `#12161A` fill at 100% opacity | Titles legible and consistent — **PASS** |
| 3.8 | KPI cards filled their tiles unevenly | Cards left on Standard fit | Set Fit → Entire View on each | Uniform card widths on all four tabs — **PASS** |
| 3.9 | Top 10 bar chart showed no visible separation | Axis auto-ranged from zero | Applied the storyboard's 85–100 range | Differences between MIT 100.0 and Caltech 90.9 now readable — **PASS** |
| 3.10 | Region colour legend read "Africa, MIN(1)" | `Measure Names` was on the Colour shelf of the dual-axis donut | Removed it from Colour | Legend reads as a plain Region legend — **PASS** |

---

## 4. Known behaviour — not a defect

**Top-N reference cards do not respond to the cross-filter.** "Top Country by Avg QS Score"
and "Most Represented Country" are global reference values. They are deliberately excluded
from `Filter_Country_From_Benchmarking` because a Top-1 calculation intersected with a
single-country filter returns an empty result (defect 3.2). They stay stable as a benchmark
while the map and the country count respond to the selection.

**"Highest Research Impact" shows Amirkabir University of Technology.** Nine institutions
tie at exactly 100.0 on `KPI_Research_Impact_Score`; Tableau surfaces the alphabetically
first. This is a tie, not a ranking artefact, and not an error.

**Band-derived rank movement.** `Rank Change 2024-2025` uses band midpoints for institutions
published in ranges (for example `1201-1400` → 1300.5). Movement figures for banded
institutions are therefore approximate. The Rank Movement view on University Overview is
scoped to the QS top 10, all of which carry exact ranks in both editions, so no band
artefacts appear in the published view.

---

## 5. Rendering and export verification

| # | Check | Result |
|---|---|---|
| 5.1 | All four dashboards render at 1600 × 950 without scrollbars | **PASS** |
| 5.2 | Dashboards exported to PNG at 3200 × 1900 (2× retina) | **PASS** |
| 5.3 | Exported images free of authoring artefacts (selection highlights) | **PASS** — one export repeated after selection highlights were found on Country Comparison |
| 5.4 | Dark theme consistent across all four tabs | **PASS** |
| 5.5 | Null indicators ("1 null", "5 nulls", ">1K nulls") visible in-view | **PASS** |

---

## 6. Workbook integrity

| # | Check | Result |
|---|---|---|
| 6.1 | `EduVision_DV.twbx` passes ZIP integrity check | **PASS** |
| 6.2 | Packaged extract present (`university_final_dataset.hyper`) | **PASS** |
| 6.3 | Workbook reopens after save with all four dashboards intact | **PASS** |
| 6.4 | `eduvision_prototype.twbx` passes integrity check, 4 dashboards | **PASS** |
| 6.5 | `eduvision_dashboard_v1.twbx` passes integrity check, 2 dashboards | **PASS** |

---

## 7. Conclusion

No major dashboard issues remain open. Ten defects were found during testing and all ten
were fixed and retested. The cross-filter action behaves to specification in both directions.
KPI accuracy is 100% against the 36 data-layer assertions, above the 95% criterion.

Three requirements from the official specification are not met and are documented rather
than worked around: publications analysis (no source data), multi-year trend analysis
(single-edition dataset, addressed in part by the 2024–2025 rank comparison), and Tableau
Public deployment (optional).
