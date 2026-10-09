# EduVision_DV: Tableau Desktop Construction & Dashboard Guide
### Infosys Springboard Virtual Internship Project

---

## 1. Executive Summary & Design System

This guide provides the complete blueprint for constructing the 4 interactive dashboards in **Tableau Desktop** using the finalized dataset (`university_final_dataset.csv` or `university_final_dataset.xlsx`).

### 1.1 Color Palette & Theme Specifications
The visual theme follows a modern, high-contrast dark aesthetic optimized for executive reporting:

| Element | Hex Code | Purpose / Visual Role |
| :--- | :--- | :--- |
| **Canvas Background** | `#12161A` | Deep charcoal dashboard background |
| **Card / Container Fill** | `#1B2026` | Elevated tile background for KPI blocks and charts |
| **Primary Typography** | `#FFFFFF` | Headers, KPI numerals, primary titles |
| **Secondary Typography** | `#CFD6DF` | Subtitles, axis labels, field captions, footers |
| **Gridlines & Borders** | `#28323D` | Subtle divider lines with low visual noise |
| **Primary Accent** | `#00D2C4` | Teal / Cyan (Dashboard 1 & 4 - Overview & Benchmarking) |
| **Research Accent** | `#FF9F1C` | Amber / Orange (Dashboard 2 - Research Analytics) |
| **Student Accent** | `#2EC4B6` | Mint / Emerald (Dashboard 3 - Student Analytics) |
| **Highlight / Alert** | `#E71D36` | Coral Red (Reference lines, maximum highlights) |

---

## 2. Calculated Fields & Data Prep in Tableau

Before constructing worksheets, create the following calculated fields in Tableau Desktop:

### 2.1 Display Tooltip Fields
1. **`Display_Students_per_Staff`**:
   ```sql
   IF ISNULL([KPI_Faculty_to_Student_Ratio]) THEN
       "Sourced from THE (Data not available)"
   ELSE
       STR(ROUND([KPI_Faculty_to_Student_Ratio], 1)) + " students/staff"
   END
   ```
2. **`Display_Int_Student_Pct`**:
   ```sql
   IF ISNULL([KPI_International_Student_Pct]) THEN
       "Sourced from THE (Data not available)"
   ELSE
       STR(ROUND([KPI_International_Student_Pct], 1)) + "%"
   END
   ```
3. **`Display_Research_Productivity`**:
   ```sql
   IF ISNULL([KPI_Research_Productivity_Proxy]) THEN
       "THE Environment Proxy (Data not available)"
   ELSE
       STR(ROUND([KPI_Research_Productivity_Proxy], 1)) + " pts"
   END
   ```

### 2.2 Aggregation & KPI Helper Fields
- **`Total_Universities_Count`**:
  ```sql
  COUNTD([Institution_Name])
  ```
- **`Avg_Global_Score`**:
  ```sql
  AVG([KPI_Global_Ranking_Score])
  ```
- **`Avg_Academic_Reputation`**:
  ```sql
  AVG([KPI_Academic_Reputation_Score])
  ```
- **`Avg_Research_Impact`**:
  ```sql
  AVG([KPI_Research_Impact_Score])
  ```
- **`Avg_Students_per_Staff`**:
  ```sql
  AVG([KPI_Faculty_to_Student_Ratio])
  ```
- **`Avg_Intl_Student_Pct`**:
  ```sql
  AVG([KPI_International_Student_Pct])
  ```
- **`Avg_Research_Productivity`**:
  ```sql
  AVG([KPI_Research_Productivity_Proxy])
  ```
- **`Total_FTE_Enrollment`**:
  ```sql
  SUM([THE_No_of_FTE_Students])
  ```

---

## 3. Dashboard 1: University Overview

### Purpose:
Provides macro-level institutional rankings, geographical spread, and structural distributions across 1,503 institutions.

### Layout Dimensions:
- Fixed Size: `1600 x 950` pixels (or Automatic responsive).
- Canvas Background: `#12161A`.

### Top KPI Summary Cards (Container: 3 Cards across top):
1. **Top Ranked University:**
   - **Main Value:** `MIT` (or `Massachusetts Institute of Technology (MIT)`)
   - **Subtitle:** `#1 in World Rankings 2025`
   - **Accent:** `#00D2C4`
2. **Total Universities:**
   - **Calculation:** `COUNTD([Institution_Name])`
   - **Main Value:** `1,503`
   - **Subtitle:** `106 Countries Covered`
3. **Average Global Score:**
   - **Calculation:** `AVG([KPI_Global_Ranking_Score])`
   - **Main Value:** `41.84`
   - **Subtitle:** `Avg. of Top 600 Scored Institutions` (Do NOT hard-code 41.84; use aggregation).

### Visualizations:
1. **Chart 1: Top 10 Universities by Global Score**
   - **Type:** Horizontal Bar Chart (descending).
   - **Rows:** `Institution_Name` (Filtered to Top 10 by `AVG(KPI_Global_Ranking_Score)`).
   - **Columns:** `AVG(KPI_Global_Ranking_Score)` (Axis range: 85 to 100).
   - **Color:** Single Accent `#00D2C4`.
   - **Labels:** Value on end of bar (`ROUND([KPI_Global_Ranking_Score], 1)`).
2. **Chart 2: Universities by Region**
   - **Type:** Donut Chart (Dual Axis Pie Chart).
   - **Color / Slice:** `Region`.
   - **Angle / Size:** `COUNTD(Institution_Name)`.
   - **Inner Hole:** Shaded `#1B2026` with center label displaying Total `1,503`.
3. **Chart 3: Geographic Distribution**
   - **Type:** Filled World Map / Symbol Density Map.
   - **Location:** Geographic role `Location` (Country).
   - **Size / Color:** `COUNTD(Institution_Name)`.
   - **Map Theme:** Dark map layer (`#12161A`).

### Interactive Filters:
- `Region` (Multiple values dropdown / buttons)
- `Location` (Dropdown, set to **"Only Relevant Values"**)
- `SIZE` (Category filter: S, M, L, XL)
- `FOCUS` (Category filter: FC, FO, CO, SP)

---

## 4. Dashboard 2: Research Analytics

### Purpose:
Analyzes research productivity, citations per faculty, and institutional research intensity.

### Accent Color:
`#FF9F1C` (Amber / Orange)

### Top KPI Cards:
1. **Highest Research Impact:**
   - Institution with highest `Citations_per_Faculty_Score` (Score: `100.0`).
2. **Average Citation Score:**
   - **Calculation:** `AVG([KPI_Research_Impact_Score])`
   - **Value:** `23.5`
   - **Subtitle:** `Citations per Faculty (All 1,503)`
3. **Average Research Productivity (Proxy):**
   - **Calculation:** `AVG([KPI_Research_Productivity_Proxy])`
   - **Value:** `61.2`
   - **Subtitle:** `THE Environment Metric (195 Matched)`

### Visualizations:
1. **Chart 1: Research Impact vs Research Productivity (Proxy)**
   - **Type:** Scatter Plot.
   - **Columns (X-axis):** `KPI_Research_Productivity_Proxy`.
   - **Rows (Y-axis):** `KPI_Research_Impact_Score`.
   - **Color:** `Region`.
   - **Detail / Marks:** `Institution_Name`.
   - **Trend Line:** Linear trendline showing correlation between environment and citation output.
2. **Chart 2: Research Intensity Comparison**
   - **Type:** Box Plot.
   - **Columns:** `RES.` (Ordered: `VH`, `HI`, `MD`, `LO`).
   - **Rows:** `KPI_Research_Impact_Score`.
   - **Visual Rationale:** Demonstrates how Citation Scores distribute systematically higher in Very High (VH) vs Medium (MD) institutions.
3. **Chart 3: Top 10 Research Institutions**
   - **Type:** Grouped Bar Chart / Side-by-Side Bars.
   - **Filter:** Top 10 filtered strictly by `KPI_Research_Impact_Score`.
   - **Measures:** `KPI_Research_Impact_Score` and `KPI_Research_Productivity_Proxy`.
   - **Colors:** Impact (`#FF9F1C`), Productivity (`#48CAE4`).

### Filters & Mandatory Notice:
- Filters: `Region`, `Location` (Only Relevant Values).
- **Mandatory Dashboard Footer / Annotation:**
  > *"Research Productivity (Proxy) uses THE Research Environment and is available only for matched QS-THE institutions."*
- **Note on Publication Volume Analysis:** Publication-volume analysis was not implemented because the available QS/THE source data does not provide a directly comparable publication-count field. Do not fabricate a publication metric; research performance is legitimately analyzed via QS Citations per Faculty alongside the THE Research Environment proxy.

---

## 5. Dashboard 3: Student Analytics

### Purpose:
Explores learning environment indicators including student-to-faculty ratios, internationalization, and total enrollment volume.

### Accent Color:
`#2EC4B6` (Teal / Mint)

### Top KPI Cards:
1. **Average Students per Staff:**
   - **Calculation:** `AVG([KPI_Faculty_to_Student_Ratio])`
   - **Value:** `17.4`
   - **Label:** `Average Students per Staff` (Do **NOT** format as `1:17.4`).
2. **Average International Student %:**
   - **Calculation:** `AVG([KPI_International_Student_Pct])`
   - **Value:** `25.5%`
   - **Subtitle:** `Global Student Mobility`
3. **Total FTE Student Headcount:**
   - **Calculation:** `SUM([THE_No_of_FTE_Students])`
   - **Value:** Displayed as formatted `M` (e.g. `5.46M` across all 195 matched universities).

### Visualizations:
1. **Chart 1: Average Students per Staff by Region**
   - **Type:** Horizontal Bar Chart.
   - **Rows:** `Region`.
   - **Columns:** `AVG([KPI_Faculty_to_Student_Ratio])`.
   - **Label:** `STR(ROUND(AVG([KPI_Faculty_to_Student_Ratio]), 1)) + " students/staff"`.
2. **Chart 2: Internationalization Scatter**
   - **Type:** Scatter Plot.
   - **Columns (X-axis):** `KPI_Faculty_to_Student_Ratio` (Students per Staff).
   - **Rows (Y-axis):** `KPI_International_Student_Pct`.
   - **Color:** `Region`.
   - **Detail:** `Institution_Name`.
   - **Tooltip:** Uses `Display_Students_per_Staff` and `Display_Int_Student_Pct`.
3. **Chart 3: Top 10 Universities by Enrollment**
   - **Type:** Horizontal Bar Chart.
   - **Filter:** Top 10 by `THE_No_of_FTE_Students`.
   - **Rows:** `Institution_Name`.
   - **Columns:** `THE_No_of_FTE_Students`.
   - **Strict Data Handling:** Unmatched institutions have `Null` enrollment and must remain omitted (never coerced to 0).

### Filters:
- `Region`, `Location` (Only Relevant Values), `SIZE`, `FOCUS`.

---

## 6. Dashboard 4: Country Comparison & Benchmarking

### Purpose:
Facilitates national-level performance comparisons with dynamic visual cross-filtering.

### Accent Color:
`#00D2C4`

### Top KPI Cards:
1. **Top Country by Average QS Global Score:**
   - Country with highest mean score among institutions with valid `KPI_Global_Ranking_Score`.
2. **Total Ranked Countries:**
   - **Calculation:** `COUNTD([Location])`
   - **Value:** `106`
3. **Most Represented Country:**
   - **Value:** `United States`
   - **Subtitle:** `197 Ranked Universities`

### Visualizations:
1. **Chart 1: Country Benchmarking Heatmap / Summary Table**
   - **Rows:** `Location` (Country).
   - **Columns (Measures):**
     1. `AVG([KPI_Global_Ranking_Score])`
     2. `AVG([KPI_Academic_Reputation_Score])`
     3. `AVG([KPI_Research_Impact_Score])`
     4. `COUNTD([Institution_Name])` (University Count)
   - **Formatting:** Color highlight table / gradient background for quick visual outlier detection.
2. **Chart 2: Geographic Country Map**
   - **Type:** Choropleth World Map.
   - **Dimension:** `Location`.
   - **Color Measure:** `COUNTD([Institution_Name])` or `AVG([KPI_Academic_Reputation_Score])`.

### Dynamic Dashboard Action (Critical Requirement):
- **Action Name:** `Filter_Country_From_Benchmarking`
- **Source Sheet:** `Country Benchmarking Table`
- **Target Sheet:** `Geographic Country Map` (and associated KPI cards)
- **Run Action on:** `Select`
- **Clearing Selection:** `Show all values`
- **Effect:** Clicking any country row in the benchmarking table instantly zooms/highlights the corresponding nation on the world map and filters country performance.

---

## 7. Step-by-Step Tableau Desktop Workflow

Follow these exact steps inside **Tableau Desktop**:

1. **Connect to Data:**
   - Launch Tableau Desktop.
   - Under *Connect*, select **Text File** and choose `university_final_dataset.csv` (or **Microsoft Excel** and choose `university_final_dataset.xlsx`).
   - Verify that 1,503 rows are loaded.
2. **Verify Data Types:**
   - Ensure `Rank_2025_Numeric`, `KPI_Global_Ranking_Score`, `KPI_Academic_Reputation_Score`, `KPI_Faculty_to_Student_Ratio`, `KPI_International_Student_Pct`, `KPI_Research_Impact_Score`, and `KPI_Research_Productivity_Proxy` are detected as **Number (decimal)**.
   - Ensure `Location` has Geographic Role $\rightarrow$ **Country/Region**.
3. **Create Dashboard Sheets:**
   - Build individual worksheets as detailed in Sections 3 through 6.
   - Apply dark background formatting (`Format` $\rightarrow$ `Shading` $\rightarrow$ `Worksheet: #1B2026`, `Font: #FFFFFF`).
4. **Assemble Dashboards:**
   - Create 4 separate Dashboard tabs:
     1. `University Overview`
     2. `Research Analytics`
     3. `Student Analytics`
     4. `Country Comparison`
   - Place horizontal/vertical layout containers.
   - Apply dashboard background color `#12161A`.
5. **Configure Filters & Interactivity:**
   - Add filters to container headers.
   - Set `Location` filter to **Only Relevant Values**.
   - Under `Dashboard` $\rightarrow$ `Actions`, add the filter action for Dashboard 4 connecting table to map.
6. **Save & Publish:**
   - Save workbook as `EduVision_DV.twbx` (Tableau Packaged Workbook).
