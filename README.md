=======
# Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis
=======

# EduVision_DV — Module 1: University Data Collection

## Overview

This module focuses on collecting and integrating university ranking data
from the QS World University Rankings 2025 and the Times Higher Education
(THE) World University Rankings 2024.

The collected datasets are used to create a common raw university dataset
containing ranking information and relevant university performance
indicators.

---

## Objectives

The objectives of Module 1 are:

- Download the QS World University Rankings dataset.
- Download the Times Higher Education World University Rankings dataset.
- Collect relevant university performance indicators.
- Integrate the QS and THE ranking datasets into a common structure.
- Generate the raw integrated university dataset.

---

## Data Sources

### QS World University Rankings 2025

Source:

QS World University Rankings

Dataset:

`qs-world-rankings-2025.csv`

The dataset contains university ranking information and performance
indicators such as:

- QS Rank
- QS Overall Score
- Academic Reputation
- Employer Reputation
- Faculty/Student
- Citations per Faculty
- International Faculty
- International Students
- International Research Network
- Employment Outcomes
- Sustainability

### Times Higher Education World University Rankings 2024

Source:

Times Higher Education World University Rankings

Dataset:

`TIMES_WorldUniversityRankings_2024.csv`

The dataset contains university ranking information and performance
indicators such as:

- THE Rank
- THE Overall Score
- Teaching
- Research
- Citations
- Industry Income
- International Outlook
- Number of Students
- Student/Staff Ratio
- International Students
- Female/Male Ratio

---

## Data Collection Process

The Module 1 workflow is:

```text
QS World University Rankings 2025
              +
THE World University Rankings 2024
              ↓
Select relevant performance indicators
              ↓
Create standardized university matching key
              ↓
Merge QS and THE datasets
              ↓
Validate dataset integration
              ↓
Generate university_raw_data.csv

