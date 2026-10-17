# EduVision_DV: Tableau Build Steps (Dashboards 3 & 4 + Integration)

Run `prepare_eduvision_data.py` first. You will use these files from `output/`:

| File | Used for |
|---|---|
| `university_final_dataset.csv` | Main data source for all sheets |
| `country_radar.csv` | Radar chart only (Dashboard 4) |
| `expected_kpis.csv` | QA: compare with your Tableau KPI cards |

---

## PART A: Reconnect your data

1. Open your workbook. **Data → New Data Source → Text file** and pick `university_final_dataset.csv`.
2. In the old data source, right-click it → **Replace Data Source** → choose the new one. Your Dashboard 1 and 2 sheets keep their fields if names match (the script keeps your names).
3. Fix any red `!` fields by right-clicking → **Replace References**.
4. In the data pane: right-click **Country** → **Geographic Role → Country/Region**.
5. Check types: `Year` should be a **Discrete** dimension (right-click → Convert to Discrete). `Total Students`, `International Students`, `International Student %` should be measures.
6. If names look wrong, confirm the CSV was written as UTF-8 (the script uses `utf-8-sig`).

## PART B: Shared calculated fields and parameters

Create via **Analysis → Create Calculated Field**.

**1. Latest Year Flag** (for KPI cards)
```
[Year] = { FIXED : MAX([Year]) }
```

**2. Intl % Weighted**
```
SUM([International Students]) / SUM([Total Students])
```
Format as Percentage, 1 decimal.

**3. Domestic Students**
```
SUM([Total Students]) - SUM([International Students])
```

**4. Top N parameter**: right-click data pane → **Create Parameter**
- Name: `Top N`, Data type: Integer, Allowable values: List → 5, 10, 15. Current value: 10.
- Right-click → **Show Parameter**.

**5. Country Rank**
```
RANK(AVG([Global Ranking Score]))
```
Right-click this pill in a view → **Compute Using → Country**.

**6. Metric Selector parameter**
- Name: `Metric Selector`, Data type: String, List:
  Global Ranking Score, Academic Reputation Score, Research Impact Score, Research Productivity Index.

**7. Selected Metric Value**
```
CASE [Metric Selector]
WHEN "Global Ranking Score" THEN AVG([Global Ranking Score])
WHEN "Academic Reputation Score" THEN AVG([Academic Reputation Score])
WHEN "Research Impact Score" THEN AVG([Research Impact Score])
WHEN "Research Productivity Index" THEN AVG([Research Productivity Index])
END
```

## PART C: Dashboard 3, Student Analytics

Create each as a **new sheet**. Name them exactly as shown so they are easy to find.

### KPI cards (4 sheets, each with Text mark)

| Sheet name | Put on Text | Filter |
|---|---|---|
| `S3_KPI_TotalStudents` | `SUM([Total Students])` | Latest Year Flag = True |
| `S3_KPI_IntlStudents` | `SUM([International Students])` | Latest Year Flag = True |
| `S3_KPI_IntlPct` | `Intl % Weighted` | Latest Year Flag = True |
| `S3_KPI_FSR` | `AVG([Faculty Student Ratio])` | Latest Year Flag = True |

For each: Marks → Text → click `...` to edit the label. Use a larger bold font for the number and a small grey title. Hide the sheet title and set **Fit → Entire View**.

### Chart 1: Student Distribution (Bar), `S3_Distribution`
1. Rows: `Country`. Columns: `SUM([Total Students])`.
2. Sort descending (click the sort icon on the toolbar).
3. Drag `Country` to Filters → **Top** tab → By field → Top `[Top N]` by `SUM(Total Students)`.
4. Colour: `Region`. Add `SUM(Total Students)` to Label.

### Chart 2: International Students by Country (Filled Map), `S3_IntlMap`
1. Double-click `Country` (creates the map). Marks → **Map** (filled).
2. Drag `Intl % Weighted` to Color. Edit colors → sequential, 2-stop.
3. Drag `Country` and `SUM(International Students)` to Tooltip.
4. Map menu → **Background Layers** → set Dark/Light to match your theme.

### Chart 3: Student Diversity (Donut), `S3_Donut`
1. Drag `Measure Names` to Filters → keep only `Domestic Students` and `International Students`.
2. Marks → **Pie**. Measure Names → Color, Measure Values → Angle.
3. Donut hole: on Columns, drag **`MIN(0)`** twice (type it into the Columns shelf: double-click and enter `MIN(0)`).
4. The second `MIN(0)` marks card: set to **Circle**, remove all fields from it, colour white or your background colour, Size smaller.
5. Right-click the second `MIN(0)` pill → **Dual Axis**. Hide both axes (right-click → uncheck Show Header).
6. Add `Intl % Weighted` as a Label on the second mark (text in the hole).

### Chart 4: Faculty-to-Student Ratio (Column chart), `S3_FSR`
1. Columns: `Region`. Rows: `AVG([Faculty Student Ratio])`.
2. Sort descending. Colour by Region. Add value labels.
3. Optional: make it drillable by adding `Country` to Columns, with Region as a **hierarchy** (drag Country onto Region in the data pane).

### Chart 5: Enrollment Comparison (Scatter), `S3_Scatter`
1. Columns: `SUM([Total Students])`. Rows: `AVG([International Student %])`.
2. `University Name` → Detail (this disaggregates to one point per university).
3. `Region` → Color. `AVG([Faculty Student Ratio])` → Size.
4. Analysis → **Trend Lines → Show Trend Lines** (optional).
5. If points bunch at the left, right-click the X axis → **Edit Axis → Scale: Logarithmic**.

### Assemble Dashboard 3
1. **New Dashboard** → Size: **Fixed, 1600 × 900** (use the same as Dashboards 1 and 2).
2. Drag a **Horizontal container** to the top: logo image, title text "Student Analytics", then the navigation buttons later.
3. Row 2: the four KPI sheets, evenly distributed (set each to **Fit Entire View**).
4. Row 3: Distribution + Map + Donut. Row 4: FSR + Scatter.
5. Right side: filter panel with `University Name`, `Country`, `Year`. Each filter's dropdown → **Apply to Worksheets → All Using This Data Source**.
6. Footer: text object "Source: QS World University Rankings | Times Higher Education | Last updated: <date>".

## PART D: Dashboard 4, Country Comparison

### KPI cards (4 sheets)

| Sheet name | Put on Text |
|---|---|
| `S4_KPI_NumUnis` | `COUNTD([University Id])` |
| `S4_KPI_AvgRank` | `AVG([Global Ranking Score])` (title: "Avg Global Ranking Score") |
| `S4_KPI_AvgResearch` | `AVG([Research Impact Score])` |
| `S4_KPI_Intl` | `AVG([International Student %])` |

All filtered with Latest Year Flag = True.

### Chart 1: Country Ranking Comparison (Horizontal bar), `S4_CountryRank`
1. Rows: `Country`. Columns: `AVG([Global Ranking Score])`.
2. Sort descending. Filter: `Country Rank` ≤ `[Top N]` (drag `Country Rank` to Filters → At most → type `[Top N]` via parameter).
3. Colour: `Region`. Label: value.

### Chart 2: Education Benchmarking (Radar), `S4_Radar`
This uses the **pre-computed polygon coordinates** in `country_radar.csv`.
1. **Data → New Data Source → Text file** → `country_radar.csv`.
2. Columns: `SUM([X])`. Rows: `SUM([Y])`.
3. Marks → **Polygon**. `Path` → **Path**. `Country` → **Color** and **Detail**.
4. Filter `Country` and select 3 to 5 countries (show filter, set to Multiple values dropdown).
5. Hide both axes (uncheck Show Header). Right-click axes → Edit Axis → **Fixed**: -100 to 100 for both X and Y (keeps the pentagon centred).
6. Set Marks opacity ~35%. Add a Border on Color.
7. Put a **Tooltip** with `Metric` and `Value`. Add a second layer if you want axis labels: put `Metric` on Label for the first 5 points only (filter `Path` ≤ 5).
8. If it takes too long, fall back to a clustered bar: `Measure Names` on Columns/Color, `Measure Values` on Rows, with the five `(Norm)` fields. This is acceptable for the rubric.

### Chart 3: Regional Education Trends (Line), `S4_RegionTrend`
1. Columns: `Year` (Discrete). Rows: `Selected Metric Value`.
2. Colour: `Region`. Show the `Metric Selector` parameter.
3. If you only have one year, replace with a bar by Region and note that in the README.

### Chart 4: Top Performing Countries (Bar), `S4_TopCountries`
1. Rows: `Country`. Columns: `Selected Metric Value`.
2. Filter `Country Rank` ≤ `[Top N]`. (Compute Using Country; you may need to use `RANK(AVG(...))` on the metric you plot.)
3. Sort descending. Colour by Region.

### Chart 5: Country-to-Country (Scatter), `S4_CountryScatter`
1. Columns: `AVG([Research Impact Score])`. Rows: `AVG([Academic Reputation Score])`.
2. `Country` → Detail and Label. `COUNTD([University Id])` → Size. `Region` → Color.

### Assemble Dashboard 4
Same layout as Dashboard 3: header, KPI row, 2 rows of charts, filter panel (`Country`, `Region`, `Year`), footer. Fixed 1600 × 900.

## PART E: Integration

### E1. Navigation buttons (on all four dashboards)
1. In the dashboard, drag a **Navigation** object (Objects pane) into the header container.
2. Click the object's dropdown → **Edit Button**:
   - **Navigate to:** pick the target dashboard (Overview, Research Analytics, Student Analytics, Country Comparison).
   - **Title:** text such as "Student Analytics".
3. Repeat for each button. Skip the button for the page you are on, or style it highlighted.
4. For Home: point it to your University Overview, or build a small "Home" dashboard if you want.
5. Copy the header container (Ctrl+C / V) between dashboards and just change the buttons.

### E2. Common filters
For every filter on every dashboard:
1. Filter dropdown → **Apply to Worksheets → Selected Worksheets…**
2. Tick **all** sheets across all dashboards that use the main data source → OK.
3. The `country_radar.csv` source is separate. Relate it: **Data → Edit Blend Relationships** on `Country`, then use **Apply to Worksheets → All Using Related Data Sources** for the Country filter.

Check: change Year on Dashboard 3 and see the Dashboard 4 values change.

### E3. Filter actions (Dashboard → Actions → Add Action → Filter)

| Name | Source sheet (Dashboard 1) | Target dashboard | Run on | Target filters (Selected Fields) | On clear |
|---|---|---|---|---|---|
| Overview → Research | the university bar/scatter | Research Analytics | Select | Source `University Id` → Target `University Id` | Show all values |
| Overview → Student | the university bar/scatter | Student Analytics | Select | `University Id` → `University Id` | Show all values |
| Overview → Country | the university bar/scatter | Country Comparison | Select | `Country` → `Country` | Show all values |

This gives "IIT Delhi selected → Country Comparison filters to India."

### E4. "Opens with the university selected" (Go to Sheet actions)
A filter action only filters. To also **jump** to the dashboard, add:
- **Dashboard → Actions → Add Action → Go to Sheet**
- Source: the university chart on Dashboard 1. Target: `Research Analytics` dashboard.
- Run action on: **Menu** (not Select, because three Select-jump actions would conflict).
- Name it "Open Research Analytics for <University Name>" (click the `>` to insert the field).
- Repeat for Student Analytics and Country Comparison.

Result: click a university → its tooltip shows three links → clicking one opens that dashboard already filtered.

### E5. Parameter action (Top N)
1. **Dashboard → Actions → Add Action → Change Parameter**.
2. Source: `S4_CountryRank`. Target parameter: `Top N` … or better, create a string parameter `Selected Country` (default "All") and use it to highlight. A simple version: Source field = `Country`, Target Parameter = `Selected Country`, Aggregation: none.
3. Use `Selected Country` in a highlight calculation: `IF [Country] = [Selected Country] THEN "Selected" ELSE "Other" END` on Color.

## PART F: Test (see QA_Checklist.md)

1. Open `output/expected_kpis.csv`. Compare each KPI card with the matching value.
2. Click every navigation button and every filter.

## PART G: Save and deliver

1. **File → Save As → Tableau Packaged Workbook** → `EduVision_DV.twbx`.
2. (Optional) **Server → Tableau Public → Save to Tableau Public** and copy the link.
3. Create the repo folders and push:
```bash
mkdir -p EduVision_DV/{scripts,data,dashboard,docs}
cp prepare_eduvision_data.py EduVision_DV/scripts/
cp -r output/* EduVision_DV/data/
cp EduVision_DV.twbx EduVision_DV/dashboard/
cp README.md QA_Checklist.md tableau_build_steps.md EduVision_DV/docs/
cd EduVision_DV
git init
git add .
git commit -m "EduVision_DV: Higher Education Performance Dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/EduVision_DV.git
git push -u origin main
```
4. Take screenshots of each dashboard into `docs/screenshots/` and link them in the README.
