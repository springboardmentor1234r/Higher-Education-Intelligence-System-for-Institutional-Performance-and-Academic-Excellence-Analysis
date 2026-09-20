# Module 2: Milestone 3 & Milestone 4 (KPI Engineering & Dashboard Planning)

**Author:** Sujay S  
**Internship:** Infosys Springboard Internship 7.0  

---

## 1. Description of Work
In this module, I completed both **Milestone 2 / Module 3 (Education KPI Engineering)** and **Milestone 2 / Module 4 (Dashboard Planning & Prototyping)**:
- Developed the mathematical logic and calculated the six required higher education KPIs.
- Built a multi-sheet Excel analytical model (`university_final_dataset.xlsx`) containing the KPI master table alongside all dimension and fact tables.
- Designed the UI wireframes, visual hierarchy, dark navy theme (#0F172A), and color palette in a comprehensive storyboard PDF document (`dashboard_storyboard.pdf`).
- Created the initial Tableau prototype workbook (`eduvision_prototype.twbx`).

---

## 2. The Six Engineered KPIs
1. **Global Ranking Score (0–100):** Primary institutional performance score from QS.
2. **Research Impact Score (0–100):** Citations per faculty score.
3. **Faculty-to-Student Ratio:** Real ratio of students per staff member (e.g. 8.2:1 for MIT).
4. **International Student Percentage (0–100%):** Actual proportion of international degree students.
5. **Academic Reputation Score (0–100):** Academic survey reputation score.
6. **Research Productivity Index (0–100):** Composite metric:
   $$\text{Research Productivity Index} = 0.50 \times \text{Research Score} + 0.30 \times \text{Citations Score} + 0.20 \times \text{International Research Network Score}$$

---

## 3. Deliverables in this Folder
- `generate_education_kpis.py`: Script computing all 6 KPIs and exporting the final dataset.
- `04_kpi_engineering.ipynb`: Analysis notebook documenting KPI distributions.
- `university_final_dataset.xlsx`: Multi-tab Excel workbook containing `KPI_Master`, `Dim_University`, `Dim_Country`, `Fact_Performance`, `Fact_Research`, `Fact_Student`, and `Fact_Country_Ed`.
- `kpi_master.csv`: Master KPI table.
- `dashboard_storyboard.pdf`: Detailed visual storyboard and layout specification.
- `eduvision_prototype.twbx`: Tableau prototype workbook.
