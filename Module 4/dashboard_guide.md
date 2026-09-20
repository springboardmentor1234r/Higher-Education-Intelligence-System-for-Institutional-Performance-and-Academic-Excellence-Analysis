# EduVision_DV: Tableau Dashboard Architecture & Comprehensive User Guide

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Higher Education Analytics & BI Dashboard Design  
**Workbook Deliverable:** `EduVision_DV.twbx` (Tableau Desktop 2026)  
**Date:** September 2026  

---

## 1. Overview & Visual Design System

The **EduVision_DV** dashboard suite is an integrated business intelligence system built in Tableau to provide multi-dimensional analysis of global higher education institutions. Rather than treating dashboards as disconnected worksheets, the workbook implements an interlinked 4-tier visual architecture connected via common master dimensions (`university_id`, `country_id`, `year`).

### 1.1 Visual Theme & Aesthetic Standard
- **Background & Canvas:** Dark slate / deep navy theme (`#0F172A`) providing maximum visual focus on chart marks while reducing eye fatigue during executive analysis.
- **Card Containers:** Elevated dark cards (`#1E293B`) with subtle borders (`#334155`) establishing clear visual hierarchy.
- **Typography:** Segoe UI / Arial sans-serif typography (`#F8FAFC` headers, `#94A3B8` secondary subtitles), calibrated for readability and WCAG AA contrast compliance.
- **Functional Metric Palette:**
  - **Emerald Green (`#10B981`):** Institutional Overall Scores, Global Ranks & Academic Reputation.
  - **Cyan (`#06B6D4`):** Research Environment Scores, Citations & Research Productivity.
  - **Amber / Gold (`#F59E0B`):** International Student Ratios & Campus Diversity.
  - **Purple (`#8B5CF6`):** Faculty Staffing, Student Mentorship & Class Size Ratios.

---

## 2. Target User Personas & Analytical Use Cases

The dashboard suite is engineered to serve three primary user groups:

### Persona 1: University Leadership & Academic Deans
- **Primary Need:** Benchmark institutional performance against global and regional peer competitors.
- **Key Questions:** Where does our university stand in peer reputation vs. citation impact? How does our faculty-to-student ratio compare with top-10 world institutions? What is our research productivity index?
- **Primary Dashboards:** `University Overview` -> `Research Analytics`.

### Persona 2: Prospective International Applicants & Academic Researchers
- **Primary Need:** Evaluate prospective institutions for graduate study, faculty mentorship, and international community.
- **Key Questions:** What is the actual class size and students per staff member? What percentage of students are international? How strong is research funding and citation influence in this university?
- **Primary Dashboards:** `University Overview` -> `Student Analytics`.

### Persona 3: Government Policymakers & Education Economists
- **Primary Need:** Evaluate how national public spending on education (% of GDP) translates into top-tier university capacity and tertiary participation.
- **Key Questions:** How many ranked world-class universities does our nation host? How does our public education expenditure compare with peer economies? What are our tertiary enrollment trajectories?
- **Primary Dashboards:** `Country Comparison` (cross-linked from individual university drill-downs).

---

## 3. Detailed Dashboard Specifications

```
+--------------------------------------------------------------------------------------------------+
|                                    TABLEAU WORKBOOK ARCHITECTURE                                 |
+------------------------------+------------------------------+------------------------------------+
| Dashboard Name               | Core Analytical Purpose      | Key Visual Elements & Charts       |
+------------------------------+------------------------------+------------------------------------+
| 1. University Overview       | Global ranking scorecard and | 6 KPI Cards, Top 10 Bar Chart,     |
|    (Landing View)            | institutional performance    | Reputation vs Score Scatter, Map   |
+------------------------------+------------------------------+------------------------------------+
| 2. Research Analytics        | Citation velocity, research  | Productivity Index Bar, Citations  |
|                              | environment, and networks    | vs Environment Scatter, Collab Map |
+------------------------------+------------------------------+------------------------------------+
| 3. Student Analytics         | Demographics, mentorship     | International Student % Histogram, |
|                              | ratios, and gender diversity | Student-Staff Ratio, Gender Bars   |
+------------------------------+------------------------------+------------------------------------+
| 4. Country Comparison        | National education capacity, | National Capacity Bar, Spend vs    |
|                              | public spending, enrollment  | Rank Scatter, Enrollment Trends    |
+------------------------------+------------------------------+------------------------------------+
```

### 3.1 Dashboard 1: University Overview (Landing Page)
- **Top Header Bar:** Contains project identity (`EduVision DV`), Global Filter dropdowns (`Region`, `Country`, `University`, `Year: 2025`), and Global Navigation Buttons.
- **Executive KPI Cards (Top Ribbon):**
  1. *Global Rank:* Displays institutional rank (`#1 MIT`, `#2 Imperial`, etc.).
  2. *Overall Score:* Displays QS composite score (`100.0 / 100`).
  3. *Academic Reputation:* Displays peer survey standing (`100.0 / 100`).
  4. *Research Impact:* Displays citations per faculty index (`100.0 / 100`).
  5. *Faculty-Student Ratio:* Displays actual student-to-staff ratio (`1 : 8.2`).
  6. *International Students:* Displays empirical international student share (`33.0%`).
- **Primary Visualizations:**
  - **Top 10 Global Universities (Horizontal Bar Chart):** Ranks universities by Overall Score with branded color accents. Clicking any institution triggers a filter action passing `university_id` to Dashboards 2 and 3.
  - **Academic Reputation vs. Overall Score (Scatter Plot):** Correlates peer perception against aggregate performance. Highlights institutions outperforming their reputation through research velocity.
  - **Global University Distribution (World Choropleth Map):** Displays geographic concentrations of world-class universities across North America, Europe, Asia-Pacific, and Latin America. Clicking any nation triggers country filter actions.
  - **Regional Share of Top Universities (Donut Chart):** Breaks down continental institutional representation.

### 3.2 Dashboard 2: Research Analytics & Output
- **Target Context:** Focuses on scholarly research environment, peer citation impact, and cross-border research networks.
- **Executive KPI Cards:**
  - *Research Environment Score:* Measures institutional research infrastructure and funding (THE standard).
  - *Citation Impact Score:* Normalized citation velocity per faculty.
  - *Research Productivity Index:* Composite KPI ($0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$).
  - *International Collaboration Network Score:* Cross-border collaborative co-authorship.
- **Primary Visualizations:**
  - **Research Productivity Index Ranking (Ranked Bar Chart):** Displays leading research hubs ordered by the derived composite KPI.
  - **Citation Impact vs. Research Score (Scatter Plot):** Evaluates institutional research ROI—identifying universities producing disproportionately high citation impact relative to internal research spending.
  - **Regional Research Impact Comparison (Benchmark Bar Chart):** Compares research output quality across global geographic regions.

### 3.3 Dashboard 3: Student Analytics & Diversity
- **Target Context:** Evaluates campus diversity, class sizes, and gender representation.
- **Executive KPI Cards:**
  - *Total FTE Student Enrollment:* Full-time equivalent student headcount.
  - *Students per Staff Member:* Actual empirical ratio (e.g., 8.2:1).
  - *International Student Percentage:* Proportion of foreign students (0.0%–100.0%).
  - *Female-to-Male Ratio:* Campus gender breakdown.
- **Primary Visualizations:**
  - **International Student Percentage Distribution (Histogram / Ranked Bar):** Benchmarks universities by cross-border attractiveness (e.g., Imperial College London leading at 61%, Oxford at 42%).
  - **Student-to-Staff Ratio Benchmarking (Bar Chart):** Evaluates instructional capacity. Top-tier institutions consistently maintain ratios below 12:1.
  - **Gender Diversity Breakdown (Stacked Bar Chart):** Displays Female:Male student proportions across institutions.
  - **Enrollment Scale vs. International Share (Bubble Plot):** Sizes circles by total student headcount and positions them by international percentage.

### 3.4 Dashboard 4: Country Comparison (Macro Education Policy)
- **Target Context:** Operates at the national level, linking university performance with World Bank EdStats macroeconomic indicators.
- **Executive KPI Cards:**
  - *National University Count:* Total ranked universities in selected country.
  - *Average National University Score:* Mean score across all national institutions.
  - *Government Education Spend (% GDP):* Public investment intensity.
  - *Gross Tertiary Enrollment Rate (%):* National higher education participation rate.
- **Primary Visualizations:**
  - **National University Capacity (Ranked Bar Chart):** Ranks nations by number of world-class institutions (USA: 197, UK: 90, China: 71, Germany: 49, India: 46).
  - **Public Education Spending (% GDP) vs. Institutional Performance (Scatter Plot):** Explores whether state spending correlates directly with elite university outcomes.
  - **Tertiary Enrollment Trajectories (2010–2023 Multi-Line Chart):** Compares historical enrollment growth across peer nations.

---

## 4. Dashboard Interlinking & Filter Action Architecture

In strict adherence to Sections 34–39 of the Project Guide, the dashboards are fully interlinked through three technical mechanisms:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DASHBOARD 1: UNIVERSITY OVERVIEW                     │
│  User selects University: "University of Oxford"                      │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
    Filter Action 1 │ (Passes university_id)         │ Filter Action 2 (Passes country_id)
                    ▼                                ▼
┌──────────────────────────────────────┐ ┌───────────────────────────────┐
│   DASHBOARD 2: RESEARCH ANALYTICS    │ │ DASHBOARD 4: COUNTRY          │
│   Pre-filtered for Oxford:           │ │ COMPARISON                    │
│   - Res Prod Index: 95.44            │ │ Pre-filtered for:             │
│   - Citations: 84.80                 │ │ - Country: United Kingdom     │
│   - Int'l Network: 97.80             │ │ - Ranked Universities: 90     │
└───────────────────┬──────────────────┘ │ - Tertiary Enrollment Trend   │
                    │                    └───────────────────────────────┘
    Navigation Link │ (Passes university_id)
                    ▼
┌──────────────────────────────────────┐
│    DASHBOARD 3: STUDENT ANALYTICS    │
│    Pre-filtered for Oxford:          │
│    - Students per Staff: 10.6 : 1    │
│    - International Students: 42.0%   │
│    - Total Enrollment: 20,700        │
└──────────────────────────────────────┘
```

### 4.1 Filter Action Specifications:
1. **Action 1 (University Drill-Down):**
   - *Source Sheet:* Top 10 Global Universities / Overview Table (`Dashboard 1`).
   - *Target Dashboards:* `Dashboard 2 (Research Analytics)` & `Dashboard 3 (Student Analytics)`.
   - *Passed Field:* `university_id`.
   - *Behavior:* Selecting an institution focuses child views specifically on that institution, overlaying peer benchmark reference lines.
2. **Action 2 (Geopolitical Drill-Down):**
   - *Source Sheet:* Global University Distribution Map (`Dashboard 1`).
   - *Target Dashboard:* `Dashboard 4 (Country Comparison)`.
   - *Passed Field:* `country_id`.
   - *Behavior:* Selecting any nation immediately navigates to Dashboard 4, displaying that country's macroeconomic education indicators.
3. **Action 3 (Persistent Top Navigation Bar):**
   - Every dashboard includes a standardized top navigation bar allowing one-click transitions between views while preserving active filter states.

---

## 5. Step-by-Step Scenario Walkthrough

### Scenario: Investigating the University of Oxford
1. **Initial Exploration (Dashboard 1):** The user opens `University Overview`. In the top ranking chart, the user locates **University of Oxford** (Rank 3, Overall Score 96.9). The KPI banner immediately shows an Academic Reputation score of 100.0 and Research Impact of 84.8.
2. **Deep-Dive into Research (Dashboard 2):** The user clicks Oxford and selects `Research Analytics`. Dashboard 2 displays Oxford's research environment (99.6), citation score (99.0), and calculated Research Productivity Index of **95.44**. The user notes that while Oxford has world-leading citations, its international research network score (97.8) reflects strong cross-border collaboration across Europe.
3. **Inspecting Teaching & Student Environment (Dashboard 3):** The user transitions to `Student Analytics`. Oxford's student profile displays an actual student-to-staff ratio of **10.6:1**, demonstrating small class mentorship, with **42.0%** international students representing over 150 nations.
4. **Contextualizing National Higher Education Policy (Dashboard 4):** The user clicks Oxford's country link (`United Kingdom`). Dashboard 4 opens pre-filtered for the UK, showing that the UK hosts 90 ranked world-class universities, spends approximately 5.2% of GDP on education, and has maintained a steady tertiary enrollment gross ratio exceeding 65%.

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**
