# EduVision_DV: Tableau Dashboard Architecture & User Guide

The **EduVision_DV** workbook (`EduVision_DV.twbx`) contains four interconnected dashboards designed for interactive exploration and drill-down analysis.

---

## Dashboard 1: University Overview (Landing Page)
- **Purpose:** Institutional performance scorecard and global standing.
- **Components:**
  - **KPI Cards:** Top Global Rank, Overall Score, Academic Reputation, Research Impact, Faculty-to-Student Ratio, International Students.
  - **Top 10 Global Universities Bar Chart:** Ranks institutions by Overall Score. Clicking any institution filters Dashboard 2 & 3.
  - **Global University Distribution Map:** Geographic view of top universities worldwide.
  - **Academic Reputation vs. Overall Score:** Evaluates peer survey perceptions against aggregate institutional performance.
  - **Institutional Comparison Table:** Tabular inspection of top universities.

---

## Dashboard 2: Research Analytics
- **Purpose:** Deep dive into research productivity, citations, and international collaboration.
- **Components:**
  - **Research Productivity Index Ranking:** Displays top universities ordered by the composite Research Productivity KPI.
  - **Citations vs. Research Score Scatter:** Analyzes the relationship between research environment and citation impact.
  - **Regional Research Impact Comparison:** Compares citation impact across world regions.

---

## Dashboard 3: Student Analytics
- **Purpose:** Student demographics, staffing ratios, and international diversity.
- **Components:**
  - **International Student Percentage Distribution:** Institutional benchmark of cross-border enrollment.
  - **Student-to-Staff Ratio Benchmark:** Staffing capacity across universities.
  - **Regional Student Diversity:** Donut and bar charts analyzing continental student mobility.

---

## Dashboard 4: Country Comparison
- **Purpose:** National education benchmarking using World Bank EdStats indicators.
- **Components:**
  - **Ranked Universities by Nation:** Identifies countries with the highest concentration of top institutions.
  - **Average National University Score:** Evaluates average institutional quality per nation.
  - **Education Expenditure vs. Performance:** Analyzes public expenditure (% of GDP) in relation to world-class university outcomes.

---

## Interlinking Workflow & Filter Actions
1. **Selecting a University:** Clicking an institution on Dashboard 1 automatically filters Dashboards 2 and 3 for that university's profile.
2. **Selecting a Country:** Clicking a country on the map navigates to Dashboard 4 pre-filtered for that nation.
3. **Global Navigation Bar:** Quick navigation buttons at the top of each dashboard enable direct transitions between views while maintaining active filter selections.
