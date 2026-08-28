=======
# Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis
=======


## Milestone 2 – KPI Engineering and Tableau Dashboard Planning

This milestone focuses on transforming the cleaned higher-education dataset into meaningful education KPIs and developing interactive Tableau dashboards for institutional, research, country, and student analysis.

---

## Module 3: Education KPI Engineering

The following KPIs were calculated as part of Milestone 2:

- Global Ranking Score
- Research Impact Score
- Faculty-to-Student Ratio
- International Student Percentage
- Academic Reputation Score
- Research Productivity Index

The final dataset was prepared and optimized for visualization and analysis in Tableau.

### KPI Engineering Script

The KPI calculations are implemented in:

`scripts/generate_education_kpis.py`

### Final Dataset

The processed dataset is available at:

`data/university_final_dataset.xlsx`



## Module 4: Tableau Dashboards

Four interactive Tableau dashboards were created to analyze university performance from different perspectives.

### 1. University Overview Dashboard

Provides an overall view of university performance using key indicators such as:

- Global Ranking
- Research Impact
- Academic Reputation
- Faculty-to-Student Ratio
- International Students
- Universities by Country
- Research Impact by University
- Research Productivity by University
- Research Citations Analysis



### 2. Research Analytics Dashboard

Focuses on research performance and includes:

- Research Impact KPI
- Research Productivity KPI
- Academic Reputation KPI
- Research Impact by University
- Research Productivity by University
- Research Citations Analysis

A university filter is included to allow interactive analysis.


### 3. Country Analysis Dashboard

Provides country-level comparison of university performance using:

- Global Ranking
- Academic Reputation
- Research Impact
- Universities by Country
- Average Ranking Score by Country
- Research Impact by Country

The dashboard includes an interactive university filter.



### 4. Student Analytics Dashboard

Focuses on student-related indicators, including:

- Faculty / Student Ratio
- International Students
- Female / Male Student Ratio
- International Students by University
- Student Staff Ratio by University
- Female Male Student Analysis

The dashboard includes an interactive university filter.



## Interactive Features

The Tableau dashboards include:

- University filtering
- Interactive charts
- KPI summary cards
- University-level comparisons
- Country-level comparisons
- Research performance analysis
- Student analytics



## Tableau Workbook

The final Tableau workbook containing the dashboards and supporting worksheets is:

`University_Analytics_Final.twbx`

The workbook contains the four completed dashboards along with their supporting worksheets.



## Project Structure

Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis/
│
├── data/
│   --- university_final_dataset.xlsx
│
├── scripts/
│   --- generate_education_kpis.py
│
├── University_Analytics_Final.twbx
│
├── README.md
│
├── LICENSE
│
└── .gitignore


