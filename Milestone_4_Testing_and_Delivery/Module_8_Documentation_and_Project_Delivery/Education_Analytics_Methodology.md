# EduVision – Education Analytics Methodology

## 1. Overview

EduVision combines university ranking information with country-level education indicators to provide a broader view of higher education performance.

The methodology connects:

- University rankings
- Research performance
- Student indicators
- Country-level education statistics
- Regional education indicators

---

## 2. Data Sources

The analysis uses:

- QS World University Rankings 2025
- Times Higher Education World University Rankings 2024
- World University Rankings 2023
- World Bank Education Statistics

The World Bank education indicators used in the final analytical model are based on 2015 data.

---

## 3. University-Level Analysis

University-level analysis is performed using ranking and performance data.

The main university-level measures include:

- Global Ranking Score
- Research Impact Score
- Academic Reputation Score
- Research Productivity Index
- Students per Staff
- International Student Percentage
- Faculty-to-Student Ratio Score

These indicators are used to compare institutional performance.

---

## 4. Research Analytics Methodology

Research performance is analyzed using:

- QS Citations per Faculty
- THE Research Score
- THE Citation Score
- Research Productivity Index

The Research Productivity Index combines available research indicators using weighted scoring.

When sufficient components are available:

```text
RPI =
0.40 × QS Citations per Faculty
+
0.35 × THE Research Score
+
0.25 × THE Citations Score