# Dashboard Testing & Verification Report

## 1. Executive Summary

This report documents the end-to-end testing and verification executed on the **EduVision Higher Education Intelligence System** dashboards. Testing was conducted on both the native Tableau workbook (`EduVision_DV.twbx`) and the interactive standalone web application (`dashboard/index.html`).

The test suite covers:
- Visual accuracy and KPI alignment against dataset specifications.
- Filter responsiveness and global control state propagation.
- Cross-dashboard interlinking action filters.
- Data integrity, null value rendering, and formatting.

**Overall Test Result**: **PASSED** (All 4 dashboards and interlinking actions validated successfully).

---

## 2. Test Environment & Scope

- **Tableau Workbook**: `dashboard/EduVision_DV.twbx` (Tableau 2024.x XML format)
- **Web Application**: `dashboard/index.html` (HTML5 / Vanilla JavaScript / CSS3)
- **Target Dashboards**:
  1. `University Overview` (Landing / Executive View)
  2. `Research Analytics` (Institutional Research & Productivity)
  3. `Student Analytics` (Demographics, Ratios & Diversity)
  4. `Country Comparison` (Macro-level Education Indicators)

---

## 3. Dashboard-by-Dashboard Test Execution

### 3.1 University Overview
| Test Item | Specification | Expected Behavior | Result |
|---|---|---|---|
| KPI Cards | Display Global Rank, Overall Score, Academic Rep, Research Impact, Faculty/Student Ratio, Intl Student % | Render aggregation values dynamically based on selected filters | **PASS** |
| Top Universities Table | Ranked list of institutions sorted by Global Rank | Row selection triggers cross-dashboard interlinking actions | **PASS** |
| Regional Distribution | Categorical breakdown across world regions | Slice click filters university table and KPI cards | **PASS** |
| Global Filters | Region, Country, University Name, Year dropdowns | Updates all sheet zones on `University Overview` | **PASS** |

### 3.2 Research Analytics
| Test Item | Specification | Expected Behavior | Result |
|---|---|---|---|
| KPI2 Card | Research Impact Score metric | Shows average/selected Research Impact | **PASS** |
| KPI6 Card | Research Productivity Index metric | Shows weighted composite index | **PASS** |
| Research Score vs Citation Impact | Scatter plot comparing research & citation metrics | Hover tooltips display institution details and exact scores | **PASS** |
| Multi-Year Research Trend | Time-series line chart | Reflects multi-year performance across QS 2025 and THE 2024 | **PASS** |

### 3.3 Student Analytics
| Test Item | Specification | Expected Behavior | Result |
|---|---|---|---|
| KPI3 Card | Faculty-to-Student Ratio | Displays students per staff count accurately | **PASS** |
| KPI4 Card | International Student Percentage | Displays % of international student body | **PASS** |
| Headcount vs Intl Students | Stacked / Dual-axis metric visualization | Visualizes total enrollment alongside international headcount | **PASS** |

### 3.4 Country Comparison
| Test Item | Specification | Expected Behavior | Result |
|---|---|---|---|
| Performance Map | Choropleth / Symbol map of country education performance | Map hover shows country ISO code and average rank/score | **PASS** |
| Education Spend | Bar chart of Expenditure on Education (% GDP) | Ranks countries by World Bank EdStats spend indicator | **PASS** |
| Tertiary Enrollment | Bar/Line chart of Gross Tertiary Enrollment Rate | Displays higher education participation by country | **PASS** |

---

## 4. Action Filter & Interlinking Tests

### 4.1 Cross-Dashboard Interlinking Verification
The core interlinking requirement dictates that selecting a university on `University Overview` carries that active filter forward to `Student Analytics`, `Research Analytics`, and `Country Comparison`.

| Action Name | Source View | Target View | Filter Field | Status |
|---|---|---|---|---|
| `Filter Student by University` | `University Overview` (`Top Universities`) | `Student Analytics` | `University Id` / `University Name` | **PASS** |
| `Filter Research by University v2` | `University Overview` (`Top Universities`) | `Research Analytics` | `University Id` / `University Name` | **PASS** |
| `Filter Country Comparison by Country` | `University Overview` (`Top Universities`) | `Country Comparison` | `Country Id` / `Country Name` | **PASS** |

### 4.2 Known Tableau Quirk & Manual XML Resolution
During Tableau development, action filters created via the Desktop GUI omitted the explicit source dashboard reference (`dashboard="University Overview"`), defaulting to `<source worksheet="Top Universities" />`. In Tableau Desktop, this caused action filters to register only within the local sheet scope, failing to pass parameters across dashboards upon navigation.

**Fix Applied**: Hand-edited `EduVision_DV.twb` XML under the `<actions>` block to explicitly define source dashboard scope:
```xml
<action caption="Filter Student by University" name="[Action2_DF27BB10602D47BEAC0D6C0D046B3A1B]">
  <activation type="on-select" />
  <source dashboard="University Overview" type="sheet" worksheet="Top Universities" />
  <command command="tsc:tsl-filter">
    <param name="special-fields" value="all" />
    <param name="target" value="Student Analytics" />
  </command>
</action>
```
Post-edit validation confirmed seamless cross-dashboard filter propagation.

---

## 5. Data Integrity & Formatting Verification

- **Null Handling**: Missing scores and indicators are explicitly preserved as `NULL` / blank rather than zero-filled, preventing distorted averages.
- **Data Types**: Ranks and headcounts render as integers; scores and ratios render as formatted floats (`0.0`).
- **Referential Integrity**: 100% of fact table records link to valid `dim_university` and `dim_country` dimension keys.
