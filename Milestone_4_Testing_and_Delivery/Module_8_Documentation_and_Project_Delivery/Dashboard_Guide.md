# EduVision – Dashboard Guide

## 1. Overview

EduVision contains four integrated Tableau dashboards designed to analyze university performance, research performance, student characteristics, and country-level education indicators.

The four dashboards are:

1. University Overview
2. Research Analytics
3. Student Analytics
4. Country Comparison

---

## 2. University Overview

### Purpose

The University Overview dashboard provides an overall view of university performance and ranking indicators.

### Main Components

- University Count
- Average Global Ranking Score
- Average Research Impact Score
- Average Academic Reputation Score
- Top Universities by Global Ranking Score
- University Distribution by Country
- Top Universities by Academic Reputation
- University Performance Trends
- Institutional Performance Comparison

### Main Filters

- Country
- Region
- Income Group
- University Name
- Year

### Usage

Users can select a country from the map to filter related university views.

Users can also select individual universities to examine their performance indicators.

The dashboard provides navigation to Research Analytics.

---

## 3. Research Analytics

### Purpose

The Research Analytics dashboard evaluates research performance and research-related indicators.

### Main Components

- Average Research Productivity Index
- Average Research Impact Score
- THE Research Score
- THE Citation Score
- Research Productivity vs Research Impact
- Top Universities by QS Citations per Faculty
- THE Research Score vs Citation Score
- Research Score Trends

### Main Filters

- Country
- Region
- Income Group
- University Name
- Year

### Usage

Users can compare research productivity and research impact.

The scatter plot can be used to examine relationships between research productivity and research impact.

The ranking view displays universities according to QS Citations per Faculty.

The dashboard provides navigation to Student Analytics.

---

### Publications Analysis

The Research Analytics dashboard includes publication analysis based on validated OpenAlex institution matches.

#### Publication Trends
Shows publication-count trends for validated universities across 2023, 2024, and 2025.

#### Top Universities by Publications
Shows universities with the highest validated publication counts for the selected year.

#### Publication Data Coverage

The OpenAlex publication analysis currently covers 60 validated universities out of the 3,530 universities in the integrated dataset, representing approximately 1.70% validated coverage.

Only reliable institution matches were included. Ambiguous or unmatched institutions were excluded to avoid incorrect publication attribution.

Therefore, the publication visualizations should be interpreted as a validated OpenAlex subset analysis rather than complete publication coverage of all universities.

## 4. Student Analytics

### Purpose

The Student Analytics dashboard examines student-related indicators available in the integrated dataset.

### Main Components

- Average International Student Percentage
- Average Students per Staff
- Average Faculty-to-Student Ratio Score
- International Students vs Students per Staff
- Top Universities by International Student Percentage
- Universities with Lowest Students per Staff Ratio
- Top Universities by Faculty-to-Student Ratio Score

### Main Filters

- Country
- Region
- Income Group
- University Name
- Year

### Parameter

The dashboard includes a `Selected Year` parameter.

Available years:

- 2023
- 2024
- 2025

A Year Selector worksheet is used to change the selected year through a Tableau parameter action.

### Usage

Users can select a year to update the student analytics views.

The dashboard provides navigation to Country Comparison.

---

## 5. Country Comparison

### Purpose

The Country Comparison dashboard combines university performance with country-level World Bank education indicators.

### University Performance Views

- Country University Count
- Country Average Ranking
- Country Research Productivity

### Education Indicators

- Tertiary Enrollment Ratio
- Tertiary Graduation Ratio
- Female Tertiary Students Percentage
- Tertiary Pupil-Teacher Ratio
- Youth Literacy 15–24 Percentage
- Tertiary Graduates

### Regional Comparison

The Regional Youth Literacy Comparison provides a comparison of youth literacy values across World Bank regions.

### Usage

Users can compare countries based on university performance and education indicators.

Country selections can filter related dashboard views.

The dashboard provides navigation back to University Overview.

---

## 6. Dashboard Navigation

The four dashboards are connected using Tableau navigation controls.

```text
University Overview
        ↓
Research Analytics
        ↓
Student Analytics
        ↓
Country Comparison
        ↓
University Overview