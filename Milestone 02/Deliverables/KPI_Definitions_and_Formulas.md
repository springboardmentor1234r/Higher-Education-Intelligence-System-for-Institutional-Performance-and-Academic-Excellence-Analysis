# Milestone 02: KPI Definitions & Engineering Specifications

## 1. Executive Summary
Milestone 02 focuses on engineering actionable higher education key performance indicators (KPIs) from the cleaned institutional datasets, harmonizing entity names, computing derived metrics, and structuring the analytical dimensional model.

---

## 2. Core KPI Matrix

| Metric Name | Calculation / Source Formula | Scale | Analytical Purpose |
| :--- | :--- | :--- | :--- |
| **Global Ranking Score** | Normalized score inverted from global rank: `(1 - (Rank - 1)/(Max_Rank - 1)) * 100` | 0 – 100 | Standardized comparative global standing |
| **Overall Score** | Multi-pillar composite institutional performance from QS & THE | 0 – 100 | Hollistic institutional excellence score |
| **Academic Reputation Score** | Survey-based peer academic reputation evaluation | 0 – 100 | International academic perception & prestige |
| **Research Impact Score** | Citations and normalized research impact composite | 0 – 100 | Scientific authority and scholarly influence |
| **Faculty-to-Student Ratio** | Derived ratio: Total FTE Students / Total Faculty Staff | Ratio (Float) | Teaching capacity and learning environment |
| **Research Productivity Index** | Scholarly output normalized by faculty volume | 0 – 100 | Volume efficiency of research production |

---

## 3. Student Diversity & Demographics Engineering
To address the critical diversity analytics requirements:
1. **Female & Male Student Percentage:**
   - Extracted from WUR ratio strings (e.g. `"52 : 48"`).
   - Parsed into `Female_Percentage` and `Male_Percentage` continuous numeric float fields (`[0.0, 100.0]`).
2. **International Student Percentage:**
   - Parsed from percentage string representations (e.g. `"14%"`) into continuous numeric float fields (`International_Student_Percentage`).
3. **International Outlook:**
   - Direct Times Higher Education score benchmarking international staff, students, and global co-authorship.

---

## 4. Dimensional Modeling (Star Schema)
```
          ┌─────────────────────────┐
          │     DIM_UNIVERSITY      │
          │  University_ID (PK)     │
          │  University_Name        │
          │  Country_Standard       │
          │  Region                 │
          └────────────┬────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
  ┌─────────────┐┌─────────────┐┌─────────────┐
  │FACT_PERFORM ││FACT_RESEARCH││FACT_STUDENT │
  │University_ID││University_ID││University_ID│
  │Overall_Score││Impact_Score ││Student_Pop  │
  │Rank_Score   ││Citation_Sc  ││Female_Pct   │
  │Acad_Rep     ││Productivity ││Male_Pct     │
  └─────────────┘└─────────────┘└─────────────┘
```
