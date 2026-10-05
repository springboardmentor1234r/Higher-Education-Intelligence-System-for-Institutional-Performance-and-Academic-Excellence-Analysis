# EduVision_DV Dataset Sources

## 1. Introduction

The EduVision_DV project uses multiple higher education and university
ranking datasets to analyze university performance, research performance,
student-related indicators, and country-level education characteristics.

The major datasets used in the project are listed below.

---

## 2. QS World University Rankings 2025

### Dataset Name

QS World University Rankings 2025

### Description

The QS World University Rankings dataset provides information about
universities worldwide and includes indicators related to academic
reputation, research, internationalization, and overall university
performance.

### Usage in EduVision_DV

The QS 2025 dataset was used as one of the major sources for university
performance analysis.

Relevant information includes:

- University name
- Country
- Ranking information
- Overall score
- Academic reputation
- Research-related indicators
- International indicators

### Source

QS World University Rankings:

https://www.topuniversities.com/world-university-rankings/2025

---

## 3. Times Higher Education World University Rankings 2024

### Dataset Name

Times Higher Education World University Rankings 2024

### Description

The Times Higher Education World University Rankings dataset provides
comparative information about universities based on teaching, research,
international outlook, and industry-related performance.

### Usage in EduVision_DV

The dataset was used to support university and research-related analysis
and to provide additional ranking information for the project.

### Source

Times Higher Education:

https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking

---

## 4. World University Rankings 2023

### Dataset Name

World University Rankings 2023

### Description

The World University Rankings 2023 dataset provides historical university
ranking and performance information.

### Usage in EduVision_DV

The dataset was used to provide historical university performance data and
support comparison and analysis across ranking information.

---

## 5. World Bank Education Statistics

### Dataset Name

World Bank Education Statistics

### Description

The World Bank Education Statistics database provides internationally
comparable education indicators for countries around the world.

The indicators cover areas such as education access, participation,
completion, teachers, and education expenditure.

### Usage in EduVision_DV

World Bank education information was used to support country-level
education analysis and provide additional context for higher education
performance.

### Source

World Bank Education Statistics:

https://databank.worldbank.org/source/education-statistics

---

## 6. Data Preparation

The collected datasets were prepared before being used for dashboard
development.

The preparation process included:

1. Loading the raw datasets.
2. Inspecting rows and columns.
3. Identifying missing values.
4. Checking duplicate records.
5. Cleaning university and country names.
6. Converting ranking and score fields into appropriate formats.
7. Standardizing relevant fields.
8. Combining required information from different sources.
9. Creating cleaned and structured datasets.
10. Validating the prepared data before Tableau integration.

---

## 7. Data Quality Considerations

During data preparation, attention was given to:

- Missing values
- Duplicate records
- Different ranking formats
- Non-numeric ranking values
- Inconsistent university names
- Inconsistent country names
- Different years represented by different datasets
- Numeric conversion of score and ranking fields

For example, ranking values such as `621-630` and `1401+` required
appropriate preprocessing before numerical analysis.

---

## 8. Prepared Data

After cleaning and normalization, the project data was organized into
structured datasets suitable for visualization and analysis.

The prepared data supports:

- University-level analysis
- Research analysis
- Student-related analysis
- Country-level comparison
- KPI calculations
- Interactive Tableau filtering

---

## 9. Data Usage and Attribution

The datasets were used for academic and educational project purposes as
part of the EduVision_DV higher education intelligence system.

The original data sources remain the property of their respective
organizations. Users should refer to the original sources for complete
dataset definitions, methodology, licensing, and attribution requirements.
