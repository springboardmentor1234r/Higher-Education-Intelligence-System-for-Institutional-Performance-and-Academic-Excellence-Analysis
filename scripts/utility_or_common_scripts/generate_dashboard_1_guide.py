import os

doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"
os.makedirs(doc_dir, exist_ok=True)

md = []
md.append("# EduVision_DV – Dashboard 1: University Overview Implementation Guide\n")
md.append("## Executive Overview\n")
md.append("This document provides **exact, step-by-step instructions** for building **Dashboard 1 – University Overview** in Tableau Desktop / Tableau Cloud. It incorporates executive KPI metric cards, six specialized analytical charts, interactive parameter filters, styled tooltips, and dashboard navigation.\n")

md.append("--- \n")
md.append("## 1. Tableau Data Model & Data Source Setup\n")
md.append("### Step-by-Step Data Connection:\n")
md.append("1. Open Tableau and click **Connect to Data** $\\rightarrow$ **Text File**.\n")
md.append("2. Select `../../data/final/dim_university.csv` as the central logical table.\n")
md.append("3. Drag and relate the following tables in the Tableau **Logical Layer**:\n")
md.append("   - Relate `dim_country.csv` on `country_id = country_id`\n")
md.append("   - Relate `fact_university_performance.csv` on `university_id = university_id`\n")
md.append("   - Relate `fact_research.csv` on `university_id = university_id`\n")
md.append("   - Relate `fact_student.csv` on `university_id = university_id`\n")
md.append("   - Relate `kpi_university.csv` on `university_id = university_id`\n")
md.append("4. Set Data Source name to: `EduVision_University_Overview`.\n\n")

md.append("--- \n")
md.append("## 2. Exact Calculated Fields to Create in Tableau\n")
md.append("In the Data Pane, click the dropdown menu and select **Create Calculated Field** for each formula below:\n\n")

calc_fields = [
    ("1. Global Ranking Score Display", "`[Global Ranking Score Display]`", 
     "IFNULL(AVG([kpi_1_global_ranking_score]), AVG([overall_score]))", 
     "Returns the composite global ranking score or raw overall score scaled 0–100."),
    
    ("2. Research Impact Score Display", "`[Research Impact Score Display]`", 
     "IFNULL(AVG([kpi_2_research_impact_score]), AVG([citation_score]))", 
     "Returns normalized citation impact score scaled 0–100."),
    
    ("3. Faculty-to-Student Ratio Display", "`[Faculty-to-Student Ratio Display]`", 
     "AVG([kpi_3_faculty_per_100_students])", 
     "Returns actual faculty members per 100 students enrolled."),
    
    ("4. International Student % Display", "`[International Student % Display]`", 
     "AVG([kpi_4_intl_student_pct]) / 100.0", 
     "Formatted as Percentage (`0.0%`). Returns true percentage of international students."),
    
    ("5. Academic Reputation Score Display", "`[Academic Reputation Score Display]`", 
     "IFNULL(AVG([kpi_5_academic_reputation_score]), AVG([academic_reputation]))", 
     "Returns academic peer survey reputation score scaled 0–100."),
    
    ("6. Rank Tier Category", "`[Rank Tier Category]`", 
     "IF [global_rank] <= 50 THEN 'Top 50'\nELSEIF [global_rank] <= 100 THEN 'Top 51–100'\nELSEIF [global_rank] <= 200 THEN 'Top 101–200'\nELSEIF [global_rank] <= 500 THEN 'Top 201–500'\nELSE 'Tier 500+' END", 
     "Categorizes institutions into standard analytical ranking bands."),
    
    ("7. Selected University Highlight", "`[Selected University Highlight]`", 
     "IF [university_name] = [Parameters].[Select Primary University] THEN 'Selected'\nELSEIF [university_name] = [Parameters].[Select Comparison University] THEN 'Comparison'\nELSE 'Other' END", 
     "Color highlighting calculation for side-by-side comparative analysis.")
]

md.append("| Calculation Name | Tableau Field Name | Tableau Calculated Field Formula | Purpose & Usage |")
md.append("| --- | --- | --- | --- |")
for name, field, formula, purpose in calc_fields:
    md.append(f"| **{name}** | {field} | `{formula}` | {purpose} |")

md.append("\n---\n")
md.append("## 3. Step-by-Step Worksheet Instructions\n\n")

# KPI Cards
md.append("### A. Building the 6 Executive KPI Metric Cards\n")
md.append("Create 6 individual worksheets in Tableau named `KPI_Global_Rank_Score`, `KPI_Overall_Score`, `KPI_Research_Impact`, `KPI_Faculty_Ratio`, `KPI_Intl_Student_Pct`, `KPI_Academic_Reputation`:\n\n")

md.append("1. **`KPI_Global_Rank_Score` Sheet**:\n")
md.append("   - Drag `[Global Ranking Score Display]` to **Text** on the Marks Card.\n")
md.append("   - Change Aggregation to `AVG`.\n")
md.append("   - Click **Text** $\\rightarrow$ Edit Text: Set font size to `28pt Bold`, color `#38BDF8` (Cyan).\n")
md.append("   - Add label subtext below: `GLOBAL RANKING SCORE (0–100)` in `9pt Regular`, color `#94A3B8` (Slate Gray).\n")
md.append("   - Set Format $\\rightarrow$ Background to Transparent (`None`).\n\n")

md.append("2. **`KPI_Overall_Score` Sheet**:\n")
md.append("   - Drag `[overall_score]` to **Text** on Marks Card (set to `AVG`, format `0.0`).\n")
md.append("   - Set Text size to `28pt Bold`, color `#818CF8` (Indigo).\n")
md.append("   - Add label: `BENCHMARK OVERALL SCORE`.\n\n")

md.append("3. **`KPI_Research_Impact` Sheet**:\n")
md.append("   - Drag `[Research Impact Score Display]` to **Text** (set to `AVG`, format `0.0`).\n")
md.append("   - Set Text size to `28pt Bold`, color `#34D399` (Emerald).\n")
md.append("   - Add label: `RESEARCH IMPACT SCORE (CITATIONS)`.\n\n")

md.append("4. **`KPI_Faculty_Ratio` Sheet**:\n")
md.append("   - Drag `[Faculty-to-Student Ratio Display]` to **Text** (format `0.0` Faculty / 100 Students).\n")
md.append("   - Set Text size to `28pt Bold`, color `#FBBF24` (Amber).\n")
md.append("   - Add label: `FACULTY PER 100 STUDENTS`.\n\n")

md.append("5. **`KPI_Intl_Student_Pct` Sheet**:\n")
md.append("   - Drag `[International Student % Display]` to **Text** (format Percentage `0.0%`).\n")
md.append("   - Set Text size to `28pt Bold`, color `#F472B6` (Pink).\n")
md.append("   - Add label: `INTL STUDENT PERCENTAGE (%)`.\n\n")

md.append("6. **`KPI_Academic_Reputation` Sheet**:\n")
md.append("   - Drag `[Academic Reputation Score Display]` to **Text** (format `0.0`).\n")
md.append("   - Set Text size to `28pt Bold`, color `#A78BFA` (Purple).\n")
md.append("   - Add label: `ACADEMIC REPUTATION SCORE`.\n\n")

# Visualizations
md.append("### B. Building the 6 Required Core Visualizations\n\n")

# Viz 1
md.append("#### Viz 1: University Ranking Leaderboard (`Viz_University_Ranking`)\n")
md.append("- **Chart Type**: Horizontal Bar Chart with Rank Labels.\n")
md.append("- **Columns**: `AVG(overall_score)`\n")
md.append("- **Rows**: `university_name` (Sorted in descending order by `AVG(overall_score)`)\n")
md.append("- **Marks Card**:\n")
md.append("  - Drag `[Rank Tier Category]` to **Color** (Palette: Custom Sequential Slate-to-Cyan).\n")
md.append("  - Drag `[global_rank]` and `AVG(overall_score)` to **Label**.\n")
md.append("- **Filters**: Add Top 20 filter on `university_name` by `AVG(overall_score)`.\n")
md.append("- **Tooltip**: Show Institution Name, Country, Rank, Overall Score.\n\n")

# Viz 2
md.append("#### Viz 2: Overall Performance Scatter Matrix (`Viz_Overall_Performance`)\n")
md.append("- **Chart Type**: Scatter Plot (Overall Score vs. Rank Position).\n")
md.append("- **Columns**: `AVG(global_rank)` (Reversed axis so Rank 1 is on the left)\n")
md.append("- **Rows**: `AVG(overall_score)`\n")
md.append("- **Detail**: `university_name`, `country_name`\n")
md.append("- **Color**: `region`\n")
md.append("- **Trend Line**: Add Linear Trend Line (Analysis $\\rightarrow$ Trend Lines $\\rightarrow$ Show Trend Lines).\n")
md.append("- **Tooltip**: Show exact rank position, score, country, and region.\n\n")

# Viz 3
md.append("#### Viz 3: Academic Reputation Heatmap (`Viz_Academic_Reputation`)\n")
md.append("- **Chart Type**: Highlight Table / Heatmap.\n")
md.append("- **Columns**: `region`\n")
md.append("- **Rows**: `[Rank Tier Category]`\n")
md.append("- **Color**: `AVG(academic_reputation_score)` (Palette: Purple Sequential).\n")
md.append("- **Label**: `AVG(academic_reputation_score)` (Formatted `0.0`).\n\n")

# Viz 4
md.append("#### Viz 4: Research Performance Quad-Plot (`Viz_Research_Performance`)\n")
md.append("- **Chart Type**: Quad Scatter Plot (Citation Impact vs. Research Productivity).\n")
md.append("- **Columns**: `AVG(kpi_2_research_impact_score)` (Citation Impact)\n")
md.append("- **Rows**: `AVG(kpi_6_research_productivity_index)` (Research Productivity)\n")
md.append("- **Detail**: `university_name`\n")
md.append("- **Color**: `region`\n")
md.append("- **Reference Lines**: Add Average Reference Lines on both X and Y axes to create 4 research performance quadrants (e.g. *High Impact / High Productivity*).\n\n")

# Viz 5
md.append("#### Viz 5: Internationalization Geographic Density (`Viz_Internationalization`)\n")
md.append("- **Chart Type**: Symbol Map / Choropleth Map.\n")
md.append("- **Detail**: `country_name`\n")
md.append("- **Color**: `AVG(kpi_4_intl_student_pct)` (Palette: Teal/Cyan Sequential).\n")
md.append("- **Size**: `COUNT(university_id)` (Number of ranked universities per country).\n")
md.append("- **Map Layers**: Modern Dark Map Style (Map $\\rightarrow$ Map Layers $\\rightarrow$ Style: Dark).\n\n")

# Viz 6
md.append("#### Viz 6: Side-by-Side University Comparison Radar/Bar (`Viz_University_Comparison`)\n")
md.append("- **Chart Type**: Side-by-Side Multi-Metric Bar Chart.\n")
md.append("- **Columns**: Measure Names (`[Global Ranking Score]`, `[Research Impact]`, `[Academic Reputation]`, `[Intl Student %]`)\n")
md.append("- **Rows**: Measure Values\n")
md.append("- **Color**: `[Selected University Highlight]` (Selected = `#38BDF8` Cyan, Comparison = `#F472B6` Pink).\n")
md.append("- **Parameters**: `Select Primary University` & `Select Comparison University`.\n\n")

md.append("---\n")
md.append("## 4. Dashboard Assembly, Formatting & Actions\n\n")

md.append("### A. Dashboard Layout & Canvas Settings\n")
md.append("- **Dashboard Size**: Fixed Size `1600 x 1000 pixels` (Desktop Browser Widescreen).\n")
md.append("- **Background Color**: Outer Container `#0F172A` (Slate Navy Dark Theme).\n")
md.append("- **Card Padding**: 8px inner padding per visualization container (`#1E293B` Slate Card background with 1px border `#334155`).\n\n")

md.append("### B. Header & Layout Container Hierarchy\n")
md.append("```\n")
md.append("Vertical Main Container (Background: #0F172A)\n")
md.append("├── Horizontal Header & Navigation Bar (Height: 70px)\n")
md.append("│   ├── Title: \"EduVision_DV – University Performance Intelligence\"\n")
md.append("│   └── Navigation Buttons: [Dashboard 1: Overview] [Dashboard 2: Research] [Dashboard 3: Student] [Dashboard 4: Country]\n")
md.append("├── Horizontal Filter Bar (Height: 50px)\n")
md.append("│   └── Filters: [Source Ranking / Year] [Region] [Country] [University]\n")
md.append("├── Horizontal KPI Container (Height: 110px)\n")
md.append("│   ├── [KPI_Global_Rank_Score] card\n")
md.append("│   ├── [KPI_Overall_Score] card\n")
md.append("│   ├── [KPI_Research_Impact] card\n")
md.append("│   ├── [KPI_Faculty_Ratio] card\n")
md.append("│   ├── [KPI_Intl_Student_Pct] card\n")
md.append("│   └── [KPI_Academic_Reputation] card\n")
md.append("└── Grid Visualization Container (2 x 3 Layout)\n")
md.append("    ├── Row 1: [Viz_University_Ranking]  | [Viz_Overall_Performance]   | [Viz_Academic_Reputation]\n")
md.append("    └── Row 2: [Viz_Research_Performance]| [Viz_Internationalization]  | [Viz_University_Comparison]\n")
md.append("```\n\n")

md.append("### C. Interactive Dashboard Actions\n")
md.append("1. **Filter Action 1 (Region Map Filter)**:\n")
md.append("   - Source: `Viz_Internationalization`\n")
md.append("   - Target: All other worksheets\n")
md.append("   - Run Action On: `Select` (Clearing selection shows all values).\n\n")

md.append("2. **Filter Action 2 (Leaderboard Drilldown)**:\n")
md.append("   - Source: `Viz_University_Ranking`\n")
md.append("   - Target: `Viz_University_Comparison` & `Viz_Research_Performance`\n")
md.append("   - Run Action On: `Select`.\n\n")

md.append("3. **Button Navigation Actions**:\n")
md.append("   - Add **Navigation Objects** in Tableau Dashboard toolbar linking seamlessly between Dashboard 1 (Overview), Dashboard 2 (Research), Dashboard 3 (Student), and Dashboard 4 (Country Comparison).\n")

doc_path = os.path.join(doc_dir, "tableau_dashboard_1_university_overview_guide.md")
with open(doc_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Exported {doc_path}")
