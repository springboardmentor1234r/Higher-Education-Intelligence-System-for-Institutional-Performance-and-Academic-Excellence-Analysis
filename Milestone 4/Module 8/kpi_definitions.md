# EduVision_DV: Higher Education KPI Engineering & Mathematical Formulations

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Domain:** Higher Education Analytics & Performance Metrics  
**Date:** September 2026  

---

## 1. KPI Engineering Principles & Guidelines

In accordance with Sections 20–24 of the Project Guide, Key Performance Indicators (KPIs) in **EduVision_DV** are engineered following strict analytical principles:
1. **Defensibility:** Every KPI represents a genuine educational construct. Arbitrary column mapping (such as equating Sustainability Score to Research Productivity) is strictly prohibited.
2. **Transparency & Reproducibility:** Every KPI formula is mathematically defined, documented, and reproducible in Python and Tableau.
3. **Metric Integrity:** Scores (scaled 0–100) are never confused with actual empirical ratios (e.g., students per staff member) or empirical percentages (e.g., international student share).
4. **Statistical Authenticity:** Missing scores are handled through principled statistical transformations rather than arbitrary zero-imputation.

---

## 2. Summary Matrix of the Six Core KPIs

| KPI # | KPI Name | Primary Data Source | Mathematical Formula / Derivation | Unit | Allowable Scale |
|---|---|---|---|---|---|
| **KPI 1** | **Global Ranking Score** | QS World University Rankings 2025 | $\text{QS Overall Score}$ (Percentile imputed for ranks > 500) | Index Score | 0.0 – 100.0 |
| **KPI 2** | **Research Impact Score** | QS Citations / THE Citations | $\text{QS Citations per Faculty Score} \parallel \text{THE Citations Score}$ | Index Score | 0.0 – 100.0 |
| **KPI 3** | **Faculty-to-Student Ratio** | WUR 2023 / THE 2024 | $\text{Students per Academic Staff Member (Actual Empirical Ratio)}$ | Ratio | Positive Float (X : 1) |
| **KPI 4** | **International Student %** | WUR 2023 | $\frac{\text{International FTE Students}}{\text{Total FTE Students}} \times 100$ | Percentage | 0.0% – 100.0% |
| **KPI 5** | **Academic Reputation Score** | QS World University Rankings 2025 | $\text{QS Academic Reputation Score}$ | Index Score | 0.0 – 100.0 |
| **KPI 6** | **Research Productivity Index**| Multi-Source Derived Composite | $0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$ | Composite Index | 0.0 – 100.0 |

---

## 3. In-Depth KPI Specifications

### KPI 1: Global Ranking Score
- **Conceptual Definition:** Measures overall institutional excellence, academic standing, and global competitive positioning.
- **Source Indicator:** QS 2025 `Overall_Score`.
- **Handling Rank Bands (Ranks 501–1503):** QS explicitly publishes composite scores only for the top 500 universities; institutions ranked 501 to 1503 are published in rank intervals (e.g., 501-510, 801-850). To ensure a continuous, defensible score for all institutions without artificial step-jumps or zero-filling, an inverse percentile rank formula was applied:
  $$\text{Global Ranking Score} = \left( \frac{\text{Max Rank} - \text{Global Rank} + 1}{\text{Max Rank}} \right) \times 100$$
  *Where $\text{Max Rank} = 1503$.*
- **Interpretation:** Top-ranked institutions score near 100.0 (MIT: 100.0, Imperial College: 98.5), while institution #1503 scores 0.07.

### KPI 2: Research Impact Score
- **Conceptual Definition:** Quantifies the average citation influence and academic velocity of scientific papers published by institutional faculty members.
- **Source Indicator:** QS 2025 `Citations_per_Faculty_Score`, supplemented by THE 2024 `scores_citations`.
- **Methodological Value:** Normalizing citations per faculty member prevents institutional size bias. Large state universities with tens of thousands of faculty members naturally produce more total raw citations than specialized technical institutes; dividing citations by faculty size isolates true per-capita research impact.
- **Interpretation:** Scaled 0.0 to 100.0. A score of 100.0 indicates world-leading citation density (e.g., MIT, Harvard).

### KPI 3: Faculty-to-Student Ratio
- **Conceptual Definition:** Evaluates teaching capacity, class size environment, and individual faculty mentorship availability.
- **Source Indicator:** WUR 2023 `No of student per staff`.
- **Critical Methodological Rule:** Adhering strictly to Section 22 of the Project Guide: *A score reflecting the faculty/student ratio should not be presented as though it were the actual ratio.* 
  - The QS `Faculty_Student_Score` (0–100 index) is maintained separately.
  - KPI 3 strictly represents the **actual empirical ratio** of students per staff member (e.g., 8.2:1 for MIT, 10.6:1 for Oxford, 12.0:1 for Stanford).
- **Interpretation:** Lower ratios denote smaller class sizes and more individualized instruction.

### KPI 4: International Student Percentage
- **Conceptual Definition:** Measures campus global diversity, international attractiveness, and cross-border student recruitment.
- **Source Indicator:** WUR 2023 `International Student` percentage parsed to float.
- **Critical Methodological Rule:** Strictly reports actual empirical percentages (e.g., 33.0% for MIT, 61.0% for Imperial College London), rather than an abstract survey score.
- **Interpretation:** Values range from 0.0% to 100.0%. High values reflect strong cross-border educational appeal.

### KPI 5: Academic Reputation Score
- **Conceptual Definition:** Evaluates institutional academic prestige and scholarly recognition based on peer review surveys.
- **Source Indicator:** QS 2025 `Academic_Reputation_Score`.
- **Methodology:** Based on survey responses from over 100,000 active university academics worldwide.
- **Interpretation:** Scaled 0.0 to 100.0. Institutions with established historical prestige (MIT, Oxford, Cambridge, Harvard) achieve top ratings of 100.0.

### KPI 6: Research Productivity Index (Composite KPI)
- **Conceptual Definition:** A multi-dimensional composite index capturing institutional research capacity, peer citation quality, and cross-border collaborative research networks.
- **Formula:**
  $$\text{Research Productivity Index} = (0.50 \times \text{Research Score}) + (0.30 \times \text{Citations Score}) + (0.20 \times \text{International Research Network Score})$$
- **Weighting Rationale:**
  - **0.50 on Research Score (THE):** Measures internal research environment, grant funding, and publication volume.
  - **0.30 on Citation Score (THE / QS):** Measures external scholarly validation and scientific impact.
  - **0.20 on International Research Network (QS):** Measures breadth and diversity of international co-authorship.
- **Anti-Pattern Prohibited:** Section 22 explicitly warns: *Do not map Sustainability Score to Research Productivity.* Sustainability measures carbon emissions, green campus operations, and environmental governance. It has no conceptual relationship to scholarly research velocity.

---

## 4. Worked Calculation Case Studies

The table below details the step-by-step calculated KPIs for top-performing global institutions:

```
+------------------------------------------------------------------------------------------------------------------------------+
|                                             TOP INSTITUTION KPI BENCHMARK MATRIX                                             |
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
| ID     | Institution Name                   | Rank | Global Score | Res Impact | Staff Ratio | Intl % | Acad Rep | Prod Index  |
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
| U0001  | Massachusetts Inst of Tech (MIT)   | 1    | 100.00       | 100.00     | 8.2 : 1     | 33.0%  | 100.00   | 97.30       |
| U0002  | Imperial College London            | 2    | 98.50        | 93.90      | 11.2 : 1    | 61.0%  | 98.50    | 95.40       |
| U0003  | University of Oxford               | 3    | 96.90        | 84.80      | 10.6 : 1    | 42.0%  | 100.00   | 95.44       |
| U0004  | Harvard University                 | 4    | 96.80        | 100.00     | 9.6 : 1     | 25.0%  | 100.00   | 99.87       |
| U0005  | University of Cambridge            | 5    | 96.70        | 84.60      | 11.3 : 1    | 39.0%  | 100.00   | 95.24       |
| U0006  | Stanford University                | 6    | 96.10        | 99.90      | 12.0 : 1    | 24.0%  | 100.00   | 98.20       |
| U0007  | ETH Zurich                         | 7    | 93.90        | 98.80      | 14.8 : 1    | 41.0%  | 98.90    | 94.10       |
| U0008  | National Univ of Singapore (NUS)   | 8    | 93.70        | 89.20      | 16.5 : 1    | 34.0%  | 99.50    | 93.80       |
+--------+------------------------------------+------+--------------+------------+-------------+--------+----------+-------------+
```

### Detailed Calculation for University of Oxford (U0003):
- **Global Rank:** 3
- **QS Overall Score:** 96.9 -> **KPI 1 = 96.9**
- **Citations per Faculty:** 84.8 -> **KPI 2 = 84.8**
- **Students per Staff:** 10.6 -> **KPI 3 = 10.6 : 1**
- **International Student Share:** 42.0% -> **KPI 4 = 42.0%**
- **Academic Reputation:** 100.0 -> **KPI 5 = 100.0**
- **Research Productivity Index Calculation:**
  $$\text{Res Score} = 99.6, \quad \text{Cit Score} = 99.0, \quad \text{Net Score} = 79.7$$
  $$\text{KPI 6} = (0.50 \times 99.6) + (0.30 \times 99.0) + (0.20 \times 79.7) = 49.8 + 29.7 + 15.94 = \mathbf{95.44}$$

---
**Author:** Sujay S  
**Infosys Springboard Internship 7.0**
