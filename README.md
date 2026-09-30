# EduVision_DV – Higher Education Intelligence System

## Higher Education Performance and Academic Excellence Analysis

EduVision_DV is a higher education analytics and business intelligence project designed to analyze university performance, research impact, student characteristics, and country-level education indicators.

The project integrates multiple higher education datasets and transforms them into an interactive Tableau dashboard suite supporting comparative analysis of universities, research performance, student analytics, and country-level education indicators.

---

## Project Objective

The objective of EduVision_DV is to build a comprehensive Higher Education Intelligence System that enables users to:

- Analyze university rankings and institutional performance
- Evaluate academic reputation and research impact
- Analyze research and citation performance
- Understand student population and student-staff ratios
- Analyze international student participation and student diversity
- Compare education indicators across countries
- Explore relationships between institutional and country-level education metrics
- Present the results through an interactive Tableau dashboard suite

---

# Project Journey

The project was completed through four major milestones followed by final project delivery.

```text
Data Collection & Preparation
            ↓
KPI Engineering & Data Modeling
            ↓
Tableau Dashboard Development
            ↓
Testing, Validation & Documentation
            ↓
Final Project Presentation & Dashboard
```

---

# Milestone 1 – Data Collection & Preparation

### Objective

The first milestone focused on collecting, cleaning, standardizing, and preparing the datasets required for the higher education analytics project.

### Major datasets

- QS World University Rankings 2025
- Times Higher Education (THE) World University Rankings 2024
- World University Rankings (WUR) 2023
- World Bank Education Statistics

### Major activities

- Collected the required datasets
- Audited raw datasets
- Identified missing values
- Identified duplicate records
- Standardized column names
- Standardized data types
- Cleaned university and country names
- Created standardized country mappings
- Created university mappings
- Prepared common identifiers such as University_ID and Country_ID
- Documented data quality observations

### Deliverables

The cleaned datasets and supporting documentation are available inside:

`Milestone_1/`

---

# Milestone 2 – KPI Engineering & Analytical Data Model

### Objective

The second milestone focused on transforming the cleaned datasets into an analytical structure suitable for dashboard development.

### Major activities

- Designed the analytical data model
- Prepared university-level analytical data
- Prepared research-related analytical data
- Prepared student-related analytical data
- Prepared country-level education data
- Created KPI-related calculations
- Standardized analytical fields
- Prepared data for Tableau visualization

### Major analytical concepts

The project uses common identifiers such as:

- University_ID
- Country_ID
- Year

The analytical structure separates university, research, student, and country-level information to avoid inappropriate many-to-many joins.

### Deliverables

Milestone 2 files are available inside:

`Milestone_2/`

---

# Milestone 3 – Tableau Dashboard Development

### Objective

The third milestone focused on developing the interactive Tableau dashboard suite.

## Four interconnected dashboards

### 1. University Overview

Provides an overview of university rankings and institutional performance.

Key analysis includes:

- Overall Score
- Academic Reputation
- Research Impact
- Student/Staff Ratio
- International Student Percentage
- Global Ranking
- Top University Rankings
- University distribution by country
- Overall score distribution
- Academic reputation
- Research performance
- International student indicators

### 2. Research Analytics

Provides analysis of research and academic performance.

Key analysis includes:

- Research Score
- Citations Score
- Student/Staff Ratio
- International Student Percentage
- Top universities by research performance
- Top universities by citation performance
- Research score distribution
- Teaching vs Research performance
- International outlook
- Student/staff ratio by university

### 3. Students Analytics

Provides analysis of student population, participation, and diversity.

Key analysis includes:

- Total Students
- Student/Staff Ratio
- International Student Percentage
- Female Student Percentage
- Universities by total student population
- International student participation
- Student/staff ratios
- Female vs Male student analysis
- Teaching, Research and Citation comparison
- Student population distribution

### 4. Country Comparison

Provides country-level education and development analysis.

Key analysis includes:

- Education Expenditure (% of GDP)
- Tertiary Enrollment
- Adult Literacy Rate
- Primary Completion Rate
- Tertiary Teachers
- GDP per Capita
- Country-level comparisons
- Top countries across education indicators

## Dashboard Navigation

The dashboard suite contains navigation between the four analytical perspectives:

```text
University Overview
        ↓
Research Analytics
        ↓
Students Analytics
        ↓
Country Comparison
```

Users can move between the different analytical perspectives using the dashboard navigation controls.

### Deliverables

The Tableau workbook is available inside:

`Milestone_3/dashboard/`

---

# Milestone 4 – Testing, Validation & Documentation

### Objective

The fourth milestone focused on validating the dashboard, documenting the analytical methodology, and preparing the project for final delivery.

### Testing activities

- KPI calculation validation
- Ranking validation
- Dashboard interaction testing
- Educational metric validation
- Visual and layout validation
- Navigation testing
- Data consistency checks
- Dashboard structure verification

### Documentation created

Milestone 4 contains:

- QA Checklist
- Dashboard Testing Report
- Dataset Sources
- KPI Definitions
- Dashboard Guide
- Education Analytics Methodology

### Deliverables

All Milestone 4 documentation and the Tableau workbook are available inside:

`Milestone_4/`

---

# Final Project

The Final Project folder is intended to contain the final internship presentation and the public dashboard link.

## Final Presentation

The final presentation summarizes the complete internship journey:

- Project objective
- Data collection and preparation
- KPI engineering
- Data modeling
- Tableau dashboard development
- Research analytics
- Student analytics
- Country comparison
- Testing and validation
- Project insights
- Business value
- Future scope

## Tableau Public Dashboard

The final public Tableau dashboard link will be maintained inside:

`Final_Project/Tableau_Public_Link.md`

## Final Presentation File

The final presentation will be maintained inside:

`Final_Project/Final_Presentation.pptx`

---

# Key KPIs

| KPI | Purpose |
|---|---|
| Global Ranking | University ranking position |
| Overall Score | Overall institutional performance |
| Academic Reputation | Academic reputation performance |
| Research Impact | Research/citation impact |
| Student/Staff Ratio | Student-to-staff relationship |
| International Student Percentage | International participation |
| Research Score | Research performance |
| Citations Score | Citation performance |
| Total Students | Student population |
| Female Student Percentage | Student gender distribution |
| Education Expenditure | Country education investment |
| Tertiary Enrollment | Higher education participation |
| Adult Literacy Rate | Literacy indicator |
| Primary Completion Rate | Primary education completion |
| GDP per Capita | Country economic context |

---

# Data Sources

The project uses the following major sources:

1. QS World University Rankings 2025
2. Times Higher Education World University Rankings 2024
3. World University Rankings 2023
4. World Bank Education Statistics

Detailed source information is documented in the Milestone 4 documentation.

---

# Technology Stack

### Data Preparation

- Python
- Pandas
- NumPy

### Data Analysis

- Python
- Data validation
- Data standardization
- KPI engineering

### Visualization & Business Intelligence

- Tableau
- Interactive dashboards
- Dashboard actions
- Filters
- Navigation
- KPI cards
- Comparative visualizations

### Project Management & Delivery

- GitHub
- GitHub Branches
- GitHub Pull Requests
- Markdown Documentation

---

# Project Architecture

```text
                    DATA SOURCES
                         │
          ┌──────────────┼──────────────┐
          │              │              │
         QS             THE            WUR
          │              │              │
          └──────────────┼──────────────┘
                         │
                  WORLD BANK DATA
                         │
                         ↓
                 DATA PREPARATION
                         │
                         ↓
                DATA STANDARDIZATION
                         │
                         ↓
                  KPI ENGINEERING
                         │
                         ↓
                  ANALYTICAL MODEL
                         │
              ┌──────────┼──────────┐
              │          │          │
              ↓          ↓          ↓
          University   Research   Students
           Analytics   Analytics  Analytics
              │          │          │
              └──────────┼──────────┘
                         ↓
                 Country Comparison
                         │
                         ↓
                  TABLEAU DASHBOARD
```

---

# Repository Structure

```text
EduVision_DV/
│
├── Milestone_1/
│   └── Data Collection & Preparation
│
├── Milestone_2/
│   └── KPI Engineering & Data Model
│
├── Milestone_3/
│   └── Tableau Dashboard Development
│
├── Milestone_4/
│   └── Testing, Validation & Documentation
│
├── Final_Project/
│   ├── Final_Presentation.pptx
│   └── Tableau_Public_Link.md
│
├── data/
├── docs/
├── scripts/
├── README.md
├── README_full_pipeline.md
└── LICENSE
```

---

# Project Outcome

EduVision_DV provides an integrated higher education analytics solution combining university-level, research-level, student-level, and country-level information.

The final Tableau dashboard suite allows users to move from institutional performance analysis to research analysis, student analysis, and country-level education comparison within one connected analytical experience.

---

# Future Scope

Potential future enhancements include:

- Real-time education data integration
- Additional university ranking sources
- Advanced predictive analytics
- University performance forecasting
- Automated data refresh pipelines
- Advanced geographic analysis
- Machine learning-based institutional performance prediction
- Additional country-level socioeconomic indicators

---

# Final Deliverables

The completed internship project includes:

- Cleaned datasets
- Data preparation documentation
- Analytical data model
- KPI engineering
- Tableau dashboard suite
- Testing and validation documentation
- Final project documentation
- Final presentation
- Public Tableau dashboard

---

## Author

**Mohammad Saad**

Higher Education Intelligence System  
**EduVision_DV**

---

## Repository

**GitHub Branch:** `Mohammad_Saad`

**Project Repository:**  
Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis

**Screenshots**
<img width="1891" height="1022" alt="University Overview Dashboard" src="https://github.com/user-attachments/assets/017b867c-35f6-40e4-b931-1923a5509698" />

<img width="1897" height="1022" alt="Research Analytics Dashboard" src="https://github.com/user-attachments/assets/cbb5a200-fc2c-407e-835e-d550ac8fb149" />

<img width="1904" height="1023" alt="Students Analytics Dashboard" src="https://github.com/user-attachments/assets/74c96262-7c7d-4e9a-a6f8-8770278aee45" />

<img width="1894" height="1018" alt="Country Comparison Dashboard" src="https://github.com/user-attachments/assets/ee008602-7bd7-4c6f-9832-b743f1bda5f0" />



