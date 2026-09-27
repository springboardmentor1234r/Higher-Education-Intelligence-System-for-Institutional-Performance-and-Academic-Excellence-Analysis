# EduVision Tableau Desktop Build Guide

This comprehensive guide details how to build and complete the **EduVision Higher Education Intelligence System** in **Tableau Desktop**, incorporating the existing starter workbook at [`exisitng/University Overview.twb`](file:///c:/Users/Sonia/Downloads/EduVision_DV/exisitng/University%20Overview.twb).

---

## 1. Audit of Existing Workbook (`exisitng/University Overview.twb`)

The existing workbook already establishes data source connections, 16 pre-built worksheets, and initial dashboard layouts. 

### Data Source Connections Defined
1. **`university_final_dataset (1)`** (Primary University Performance Data):
   - Connects to [`data/final/eduvision_final_dataset.xlsx`](file:///c:/Users/Sonia/Downloads/EduVision_DV/data/final/eduvision_final_dataset.xlsx) (or `.csv`).
   - Contains pre-calculated KPI metrics and source indicators (`kpi1_global_ranking_score`, `kpi2_research_impact_score`, `kpi3_faculty_student_ratio`, `kpi3_qs_score_only_NOT_a_ratio`, `kpi4_intl_student_pct`, `kpi4_qs_score_only_NOT_a_percentage`, `kpi5_academic_reputation_score`, `kpi6_research_productivity_index`).
2. **`dim_country+`** (World Bank Country & Education Stats):
   - Connects to [`data/cleaned/fact_country_education.xlsx`](file:///c:/Users/Sonia/Downloads/EduVision_DV/data/cleaned/fact_country_education.xlsx) related with [`data/cleaned/dim_country.xlsx`](file:///c:/Users/Sonia/Downloads/EduVision_DV/data/cleaned/dim_country.xlsx) on `[country_id]`.

---

## 2. Existing Worksheets vs. Still Need to Build

The table below maps all 16 existing worksheets to their target dashboards and highlights what remains to be built from scratch.

| Dashboard View | Already Built Worksheets (Just Format/Place) | Worksheets to Build from Scratch |
|---|---|---|
| **1. University Overview** | • `KPI1 Card` (`kpi1_global_ranking_score`)<br>• `KPI2 Card` (`kpi2_research_impact_score`)<br>• `KPI3 Card` (`kpi3_qs_score_only_NOT_a_ratio`)<br>• `Student KPI4` (`kpi4_intl_student_pct`)<br>• `KPI5 Card` (`kpi5_academic_reputation_score`)<br>• `KPI6 Card` (`kpi6_research_productivity_index`)<br>• `Top Universities` (`university_name` vs `kpi1`) | • `Regional Distribution`: Donut / Bar chart showing ranking scores by region. |
| **2. Research Analytics** | • `Research KPI2`: BAN Card for Research Impact<br>• `Research KPI6`: BAN Card for Productivity<br>• `Top Research`: Bar chart of `kpi2_research_impact_score`<br>• `Research Productivity`: Bar chart of `kpi6_research_productivity_index` | • `Research Score vs Citation Impact`: Scatter plot (`research_score` vs `citation_score`).<br>• `Multi-Year Research Trend`: Line chart (`year` vs `citation_score`). |
| **3. Student Analytics** | • `Student KPI3`: BAN Card for Student-Staff Ratio<br>• `Student KPI4`: BAN Card for Intl Student %<br>• `Top Intl Students`: Bar chart of `kpi4_intl_student_pct`<br>• `Faculty Ratio`: Bar chart of `kpi3_faculty_student_ratio` | • `Total Headcount vs Intl Students`: Scatter / Grouped Bar (`total_students` vs `international_students`). |
| **4. Country Comparison** | • `Tertiary Enrollment by Country`: Bar chart (`country_name` vs `value` filtered by Tertiary Enrolment)<br>• `Education Spend by Country`: Bar chart (`country_name` vs `value` filtered by Spend % GDP) | • `Country Education Performance Map`: Map of university density & avg ranking.<br>• `University Count by Income Group`: Bar chart by World Bank Income Group. |

---

## 3. Exact Field Names & Formulas

To ensure total compatibility with `University Overview.twb` and `eduvision_final_dataset.xlsx`, reuse the **exact field names** defined in the workbook:

### Core Metric & KPI Fields (Direct from Dataset)
- `[kpi1_global_ranking_score]`: Overall / rank-derived ranking score (0–100 scale).
- `[kpi1_source]`: Source ranking dataset (`QS 2025`, `THE 2024`, `WUR 2023`).
- `[kpi2_research_impact_score]`: Citations per faculty / citation impact score (0–100 scale).
- `[kpi2_source]`: Source column description.
- `[kpi3_faculty_student_ratio]`: Actual student-to-staff headcount ratio (students per 1 staff member).
- `[kpi3_qs_score_only_NOT_a_ratio]`: QS faculty-student score index (for QS rows where raw headcount ratio is not published).
- `[kpi4_intl_student_pct]`: Actual percentage of international students (0–100%).
- `[kpi4_qs_score_only_NOT_a_percentage]`: QS international student score index.
- `[kpi5_academic_reputation_score]`: Academic reputation / teaching quality score (0–100 scale).
- `[kpi6_research_productivity_index]`: Derived composite research index ($0.50 \times \text{research\_score} + 0.50 \times \text{citation\_score}$).

### Calculated Fields to Add (If Needed in Tableau)
Create these supplementary calculated fields in Tableau (`Analysis -> Create Calculated Field...`):

1. **`[Rank Tier]`**
   ```tableau
   IF [global_rank] <= 10 THEN "Top 10"
   ELSEIF [global_rank] <= 50 THEN "Top 50"
   ELSEIF [global_rank] <= 100 THEN "Top 100"
   ELSEIF [global_rank] <= 500 THEN "Top 500"
   ELSE "501+"
   END
   ```

2. **`[Is QS Score Only]`**
   ```tableau
   ISNULL([kpi3_faculty_student_ratio]) AND NOT ISNULL([kpi3_qs_score_only_NOT_a_ratio])
   ```

---

## 4. Step-by-Step Build Instructions

### Step 1: Place and Format Existing Worksheets
1. Open [`exisitng/University Overview.twb`](file:///c:/Users/Sonia/Downloads/EduVision_DV/exisitng/University%20Overview.twb) in Tableau Desktop.
2. Go to **Dashboard: University Overview**:
   - Arrange BAN cards (`KPI1 Card`, `KPI2 Card`, `KPI3 Card`, `Student KPI4`, `KPI5 Card`, `KPI6 Card`) across the top KPI container.
   - Place `Top Universities` in the main view container.
3. Go to **Dashboard: Research Analytics**:
   - Place BAN cards (`Research KPI2`, `Research KPI6`) at the top.
   - Place `Top Research` and `Research Productivity` side by side.
4. Go to **Dashboard: Student Analytics**:
   - Place BAN cards (`Student KPI3`, `Student KPI4`) at the top.
   - Place `Top Intl Students` and `Faculty Ratio` side by side.
5. Go to **Dashboard: Country Comparison**:
   - Place `Tertiary Enrollment by Country` and `Education Spend by Country` side by side.

---

### Step 2: Build the 5 Missing Worksheets from Scratch

#### 1. `Regional Distribution` (for Dashboard 1: University Overview)
- **Data Source**: `university_final_dataset (1)`
- **Columns**: `AVG([kpi1_global_ranking_score])`
- **Rows**: `[region]`
- **Color**: `[region]`
- **Mark Type**: Horizontal Bar Chart or Donut Chart.

#### 2. `Research Score vs Citation Impact` (for Dashboard 2: Research Analytics)
- **Data Source**: `university_final_dataset (1)`
- **Columns**: `AVG([research_score])`
- **Rows**: `AVG([citation_score])`
- **Detail**: `[university_name]`
- **Size**: `AVG([kpi6_research_productivity_index])`
- **Color**: `[region]`
- **Mark Type**: Circle / Scatter Plot.

#### 3. `Multi-Year Research Trend` (for Dashboard 2: Research Analytics)
- **Data Source**: `university_final_dataset (1)`
- **Columns**: `[year]` (Discrete)
- **Rows**: `AVG([kpi2_research_impact_score])`
- **Color**: `[region]`
- **Mark Type**: Line Chart with Data Points.

#### 4. `Total Headcount vs Intl Students` (for Dashboard 3: Student Analytics)
- **Data Source**: `university_final_dataset (1)`
- **Columns**: `SUM([total_students])`
- **Rows**: `SUM([international_students])`
- **Detail**: `[university_name]`
- **Color**: `[region]`
- **Mark Type**: Scatter Plot.

#### 5. `Country Education Performance Map` (for Dashboard 4: Country Comparison)
- **Data Source**: `dim_country+`
- **Detail**: `[country_name]` (Geographic Role: Country)
- **Color**: `COUNTD([university_id])`
- **Tooltip**: `AVG([value])`
- **Mark Type**: Filled Map / Symbol Map.

---

### Step 3: Configure Dashboard Actions & Interlinking

Set up the following **Dashboard Actions** (`Dashboard -> Actions...`):

1. **Filter Action: University Selection Carry-Forward**
   - **Name**: `Filter by Selected University`
   - **Source Dashboard**: `University Overview` (Sheet: `Top Universities`)
   - **Run Action on**: `Select`
   - **Target Dashboards**: `Research Analytics`, `Student Analytics`
   - **Target Fields**: `university_id` = `university_id`
   - **Clearing Selection**: `Leave filter`

2. **Filter Action: Country Selection Carry-Forward**
   - **Name**: `Filter by Selected Country`
   - **Source Dashboard**: `University Overview` / `Student Analytics`
   - **Run Action on**: `Select`
   - **Target Dashboards**: `Country Comparison`
   - **Target Fields**: `country_id` = `country_id`

3. **Navigation Actions**:
   - Add Navigation Button objects on each dashboard header linking seamlessly between `University Overview` ↔ `Research Analytics` ↔ `Student Analytics` ↔ `Country Comparison`.
