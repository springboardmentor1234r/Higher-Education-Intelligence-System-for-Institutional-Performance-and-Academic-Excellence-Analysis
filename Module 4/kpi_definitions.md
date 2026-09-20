# EduVision_DV: KPI Definitions & Mathematical Formulas

Per Sections 20–24 of the Project Guide, every KPI is engineered with a defensible, transparent, and reproducible methodology. Arbitrary field substitutions (such as equating Sustainability Score to Research Productivity) are strictly avoided.

---

## Summary Matrix of the Six Project KPIs

| KPI # | KPI Name | Primary Data Source | Mathematical Formula / Derivation | Unit | Target / Scale |
|---|---|---|---|---|---|
| **KPI 1** | **Global Ranking Score** | QS World Rankings 2025 | $\text{QS Overall Score}$ (Rank-percentile imputed outside top 500) | Index | 0.0 – 100.0 |
| **KPI 2** | **Research Impact Score** | QS / THE Citations | $\text{QS Citations per Faculty Score} \parallel \text{THE Citations Score}$ | Index | 0.0 – 100.0 |
| **KPI 3** | **Faculty-to-Student Ratio** | WUR 2023 / THE 2024 | $\text{Students per Academic Staff Member (Actual Ratio)}$ | Ratio | Positive numeric (e.g. 8.2:1) |
| **KPI 4** | **International Student %** | WUR 2023 | $\frac{\text{International FTE Students}}{\text{Total FTE Students}} \times 100$ | % | 0.0% – 100.0% |
| **KPI 5** | **Academic Reputation Score** | QS World Rankings 2025 | $\text{QS Academic Reputation Score}$ | Index | 0.0 – 100.0 |
| **KPI 6** | **Research Productivity Index** | Multi-source Composite | $0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Network}$ | Index | 0.0 – 100.0 |

---

## In-Depth KPI Formulations

### KPI 1: Global Ranking Score
- **Definition:** Represents an institution's comprehensive academic standing on the global stage.
- **Source:** QS `Overall_Score`.
- **Handling Missing Values:** For universities positioned outside the published top 500 score bracket, a standard inverse percentile transformation based on verified global rank is applied:
  $$\text{Imputed Score} = \left( \frac{\text{Max Rank} - \text{Global Rank} + 1}{\text{Max Rank}} \right) \times 100$$
- **Interpretation:** Higher values denote higher international competitiveness.

### KPI 2: Research Impact Score
- **Definition:** Quantifies the relative citation influence and academic reach of research produced by institutional faculty.
- **Source:** QS `Citations_per_Faculty_Score`, complemented by THE `scores_citations`.
- **Interpretation:** Reflects paper citation velocity normalized for faculty body size.

### KPI 3: Faculty-to-Student Ratio
- **Definition:** Measures academic teaching capacity and individualized mentorship potential.
- **Source:** WUR `No of student per staff` / THE `stats_student_staff_ratio`.
- **Methodology Rule:** Strictly presented as a real ratio (e.g., 8.2 students per staff member). The QS Faculty/Student *Score* is retained separately as an evaluation index to avoid confusing a score with an actual ratio.

### KPI 4: International Student Percentage
- **Definition:** The proportion of international students enrolled in degree programs.
- **Source:** WUR `International Student` (%) parsed into a continuous float.
- **Methodology Rule:** Strictly reports empirical percentages, rather than qualitative internationalization scores.

### KPI 5: Academic Reputation Score
- **Definition:** The institutional reputation benchmark derived from global survey responses of over 100,000 active academics worldwide.
- **Source:** QS `Academic_Reputation_Score`.
- **Interpretation:** Directly measures scholarly esteem and institutional prestige.

### KPI 6: Research Productivity Index (Composite KPI)
- **Definition:** A multi-dimensional composite index capturing both research output volume, citation quality, and cross-border collaborative research networks.
- **Formula:**
  $$\text{Research Productivity Index} = (0.50 \times \text{Research Score}) + (0.30 \times \text{Citations Score}) + (0.20 \times \text{International Research Network Score})$$
- **Rationale:** Ensures that high research output is balanced against peer impact and international partnership breadth.
