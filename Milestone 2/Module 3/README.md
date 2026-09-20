# Module 3: Education KPI Engineering

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  
**Phase:** Milestone 2 / Weeks 3–4  

---

## The Six Engineered KPIs
1. **Global Ranking Score (0.0 – 100.0):** QS Overall Score, with inverse percentile rank imputation for ranks > 500.
2. **Research Impact Score (0.0 – 100.0):** Citations per faculty member normalized for institutional size.
3. **Faculty-to-Student Ratio (Real Ratio):** Actual ratio of students per academic staff member (e.g. 8.2:1 for MIT).
4. **International Student Percentage (0.0% – 100.0%):** Empirical proportion of cross-border enrolled students.
5. **Academic Reputation Score (0.0 – 100.0):** Peer survey score from over 100,000 global academics.
6. **Research Productivity Index (0.0 – 100.0):** Derived composite metric ($0.50 \times \text{Res} + 0.30 \times \text{Cit} + 0.20 \times \text{Net}$).

## Deliverables in this Module
- `generate_education_kpis.py`: Script calculating all 6 KPIs and generating `kpi_master.csv`.
- `university_final_dataset.xlsx`: Multi-sheet Excel workbook containing `KPI_Master`, `Dim_University`, `Dim_Country`, and all Fact tables.
- `kpi_master.csv`: Clean tabular master table ready for Tableau ingestion.
- `04_kpi_engineering.ipynb`: Analytical distribution and validation notebook.
