# EduVision_DV – Dashboard 1: University Overview Implementation Guide

## Executive Overview

This document provides **exact, step-by-step instructions** for building **Dashboard 1 – University Overview** in Tableau Desktop / Tableau Cloud. It incorporates executive KPI metric cards, six specialized analytical charts, interactive parameter filters, styled tooltips, and dashboard navigation.

--- 

## 1. Tableau Data Model & Data Source Setup

### Step-by-Step Data Connection:

1. Open Tableau and click **Connect to Data** $\rightarrow$ **Text File**.

2. Select `../../data/final/dim_university.csv` as the central logical table.

3. Drag and relate the following tables in the Tableau **Logical Layer**:

   - Relate `dim_country.csv` on `country_id = country_id`

   - Relate `fact_university_performance.csv` on `university_id = university_id`

   - Relate `fact_research.csv` on `university_id = university_id`

   - Relate `fact_student.csv` on `university_id = university_id`

   - Relate `kpi_university.csv` on `university_id = university_id`

4. Set Data Source name to: `EduVision_University_Overview`.


--- 

## 2. Exact Calculated Fields to Create in Tableau

In the Data Pane, click the dropdown menu and select **Create Calculated Field** for each formula below:


| Calculation Name | Tableau Field Name | Tableau Calculated Field Formula | Purpose & Usage |
| --- | --- | --- | --- |
| **1. Global Ranking Score Display** | `[Global Ranking Score Display]` | `IFNULL(AVG([kpi_1_global_ranking_score]), AVG([overall_score]))` | Returns the composite global ranking score or raw overall score scaled 0–100. |
| **2. Research Impact Score Display** | `[Research Impact Score Display]` | `IFNULL(AVG([kpi_2_research_impact_score]), AVG([citation_score]))` | Returns normalized citation impact score scaled 0–100. |
| **3. Faculty-to-Student Ratio Display** | `[Faculty-to-Student Ratio Display]` | `AVG([kpi_3_faculty_per_100_students])` | Returns actual faculty members per 100 students enrolled. |
| **4. International Student % Display** | `[International Student % Display]` | `AVG([kpi_4_intl_student_pct]) / 100.0` | Formatted as Percentage (`0.0%`). Returns true percentage of international students. |
| **5. Academic Reputation Score Display** | `[Academic Reputation Score Display]` | `IFNULL(AVG([kpi_5_academic_reputation_score]), AVG([academic_reputation]))` | Returns academic peer survey reputation score scaled 0–100. |
| **6. Rank Tier Category** | `[Rank Tier Category]` | `IF [global_rank] <= 50 THEN 'Top 50'
ELSEIF [global_rank] <= 100 THEN 'Top 51–100'
ELSEIF [global_rank] <= 200 THEN 'Top 101–200'
ELSEIF [global_rank] <= 500 THEN 'Top 201–500'
ELSE 'Tier 500+' END` | Categorizes institutions into standard analytical ranking bands. |
| **7. Selected University Highlight** | `[Selected University Highlight]` | `IF [university_name] = [Parameters].[Select Primary University] THEN 'Selected'
ELSEIF [university_name] = [Parameters].[Select Comparison University] THEN 'Comparison'
ELSE 'Other' END` | Color highlighting calculation for side-by-side comparative analysis. |

---

## 3. Step-by-Step Worksheet Instructions


### A. Building the 6 Executive KPI Metric Cards

Create 6 individual worksheets in Tableau named `KPI_Global_Rank_Score`, `KPI_Overall_Score`, `KPI_Research_Impact`, `KPI_Faculty_Ratio`, `KPI_Intl_Student_Pct`, `KPI_Academic_Reputation`:


1. **`KPI_Global_Rank_Score` Sheet**:

   - Drag `[Global Ranking Score Display]` to **Text** on the Marks Card.

   - Change Aggregation to `AVG`.

   - Click **Text** $\rightarrow$ Edit Text: Set font size to `28pt Bold`, color `#38BDF8` (Cyan).

   - Add label subtext below: `GLOBAL RANKING SCORE (0–100)` in `9pt Regular`, color `#94A3B8` (Slate Gray).

   - Set Format $\rightarrow$ Background to Transparent (`None`).


2. **`KPI_Overall_Score` Sheet**:

   - Drag `[overall_score]` to **Text** on Marks Card (set to `AVG`, format `0.0`).

   - Set Text size to `28pt Bold`, color `#818CF8` (Indigo).

   - Add label: `BENCHMARK OVERALL SCORE`.


3. **`KPI_Research_Impact` Sheet**:

   - Drag `[Research Impact Score Display]` to **Text** (set to `AVG`, format `0.0`).

   - Set Text size to `28pt Bold`, color `#34D399` (Emerald).

   - Add label: `RESEARCH IMPACT SCORE (CITATIONS)`.


4. **`KPI_Faculty_Ratio` Sheet**:

   - Drag `[Faculty-to-Student Ratio Display]` to **Text** (format `0.0` Faculty / 100 Students).

   - Set Text size to `28pt Bold`, color `#FBBF24` (Amber).

   - Add label: `FACULTY PER 100 STUDENTS`.


5. **`KPI_Intl_Student_Pct` Sheet**:

   - Drag `[International Student % Display]` to **Text** (format Percentage `0.0%`).

   - Set Text size to `28pt Bold`, color `#F472B6` (Pink).

   - Add label: `INTL STUDENT PERCENTAGE (%)`.


6. **`KPI_Academic_Reputation` Sheet**:

   - Drag `[Academic Reputation Score Display]` to **Text** (format `0.0`).

   - Set Text size to `28pt Bold`, color `#A78BFA` (Purple).

   - Add label: `ACADEMIC REPUTATION SCORE`.


### B. Building the 6 Required Core Visualizations


#### Viz 1: University Ranking Leaderboard (`Viz_University_Ranking`)

- **Chart Type**: Horizontal Bar Chart with Rank Labels.

- **Columns**: `AVG(overall_score)`

- **Rows**: `university_name` (Sorted in descending order by `AVG(overall_score)`)

- **Marks Card**:

  - Drag `[Rank Tier Category]` to **Color** (Palette: Custom Sequential Slate-to-Cyan).

  - Drag `[global_rank]` and `AVG(overall_score)` to **Label**.

- **Filters**: Add Top 20 filter on `university_name` by `AVG(overall_score)`.

- **Tooltip**: Show Institution Name, Country, Rank, Overall Score.


#### Viz 2: Overall Performance Scatter Matrix (`Viz_Overall_Performance`)

- **Chart Type**: Scatter Plot (Overall Score vs. Rank Position).

- **Columns**: `AVG(global_rank)` (Reversed axis so Rank 1 is on the left)

- **Rows**: `AVG(overall_score)`

- **Detail**: `university_name`, `country_name`

- **Color**: `region`

- **Trend Line**: Add Linear Trend Line (Analysis $\rightarrow$ Trend Lines $\rightarrow$ Show Trend Lines).

- **Tooltip**: Show exact rank position, score, country, and region.


#### Viz 3: Academic Reputation Heatmap (`Viz_Academic_Reputation`)

- **Chart Type**: Highlight Table / Heatmap.

- **Columns**: `region`

- **Rows**: `[Rank Tier Category]`

- **Color**: `AVG(academic_reputation_score)` (Palette: Purple Sequential).

- **Label**: `AVG(academic_reputation_score)` (Formatted `0.0`).


#### Viz 4: Research Performance Quad-Plot (`Viz_Research_Performance`)

- **Chart Type**: Quad Scatter Plot (Citation Impact vs. Research Productivity).

- **Columns**: `AVG(kpi_2_research_impact_score)` (Citation Impact)

- **Rows**: `AVG(kpi_6_research_productivity_index)` (Research Productivity)

- **Detail**: `university_name`

- **Color**: `region`

- **Reference Lines**: Add Average Reference Lines on both X and Y axes to create 4 research performance quadrants (e.g. *High Impact / High Productivity*).


#### Viz 5: Internationalization Geographic Density (`Viz_Internationalization`)

- **Chart Type**: Symbol Map / Choropleth Map.

- **Detail**: `country_name`

- **Color**: `AVG(kpi_4_intl_student_pct)` (Palette: Teal/Cyan Sequential).

- **Size**: `COUNT(university_id)` (Number of ranked universities per country).

- **Map Layers**: Modern Dark Map Style (Map $\rightarrow$ Map Layers $\rightarrow$ Style: Dark).


#### Viz 6: Side-by-Side University Comparison Radar/Bar (`Viz_University_Comparison`)

- **Chart Type**: Side-by-Side Multi-Metric Bar Chart.

- **Columns**: Measure Names (`[Global Ranking Score]`, `[Research Impact]`, `[Academic Reputation]`, `[Intl Student %]`)

- **Rows**: Measure Values

- **Color**: `[Selected University Highlight]` (Selected = `#38BDF8` Cyan, Comparison = `#F472B6` Pink).

- **Parameters**: `Select Primary University` & `Select Comparison University`.


---

## 4. Dashboard Assembly, Formatting & Actions


### A. Dashboard Layout & Canvas Settings

- **Dashboard Size**: Fixed Size `1600 x 1000 pixels` (Desktop Browser Widescreen).

- **Background Color**: Outer Container `#0F172A` (Slate Navy Dark Theme).

- **Card Padding**: 8px inner padding per visualization container (`#1E293B` Slate Card background with 1px border `#334155`).


### B. Header & Layout Container Hierarchy

```

Vertical Main Container (Background: #0F172A)

├── Horizontal Header & Navigation Bar (Height: 70px)

│   ├── Title: "EduVision_DV – University Performance Intelligence"

│   └── Navigation Buttons: [Dashboard 1: Overview] [Dashboard 2: Research] [Dashboard 3: Student] [Dashboard 4: Country]

├── Horizontal Filter Bar (Height: 50px)

│   └── Filters: [Source Ranking / Year] [Region] [Country] [University]

├── Horizontal KPI Container (Height: 110px)

│   ├── [KPI_Global_Rank_Score] card

│   ├── [KPI_Overall_Score] card

│   ├── [KPI_Research_Impact] card

│   ├── [KPI_Faculty_Ratio] card

│   ├── [KPI_Intl_Student_Pct] card

│   └── [KPI_Academic_Reputation] card

└── Grid Visualization Container (2 x 3 Layout)

    ├── Row 1: [Viz_University_Ranking]  | [Viz_Overall_Performance]   | [Viz_Academic_Reputation]

    └── Row 2: [Viz_Research_Performance]| [Viz_Internationalization]  | [Viz_University_Comparison]

```


### C. Interactive Dashboard Actions

1. **Filter Action 1 (Region Map Filter)**:

   - Source: `Viz_Internationalization`

   - Target: All other worksheets

   - Run Action On: `Select` (Clearing selection shows all values).


2. **Filter Action 2 (Leaderboard Drilldown)**:

   - Source: `Viz_University_Ranking`

   - Target: `Viz_University_Comparison` & `Viz_Research_Performance`

   - Run Action On: `Select`.


3. **Button Navigation Actions**:

   - Add **Navigation Objects** in Tableau Dashboard toolbar linking seamlessly between Dashboard 1 (Overview), Dashboard 2 (Research), Dashboard 3 (Student), and Dashboard 4 (Country Comparison).
