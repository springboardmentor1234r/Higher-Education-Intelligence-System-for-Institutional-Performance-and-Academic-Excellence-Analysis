import os
import pandas as pd
import numpy as np

final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

fact_univ = pd.read_csv(os.path.join(final_dir, "fact_university_rankings.csv"))
fact_country = pd.read_csv(os.path.join(final_dir, "fact_country_education.csv"))

stats_df = fact_univ[[
    'kpi_1_global_ranking_score',
    'kpi_2_research_impact_score',
    'kpi_3_faculty_per_100_students',
    'kpi_4_intl_student_pct',
    'kpi_5_academic_reputation_score',
    'kpi_6_research_productivity_index'
]].describe().T

md = []
md.append("# EduVision_DV – KPI Engineering & Final Analytics Summary Report\n")
md.append("## Executive Summary\n")
md.append("Following user approval of the cross-dataset matching crosswalk, the final analytical data models and the **six core project KPIs** were engineered. All outputs are exported to `../../data/final/` and are fully prepared for direct import into Tableau.\n")

md.append("--- \n")
md.append("## The Six Core Project KPIs\n")

kpis_desc = [
    ("KPI 1: Global Ranking Score", "`kpi_1_global_ranking_score`", "Composite 0–100 overall score synthesizing QS 2025 and THE 2023 benchmark overall scores.", "University Overview, Country Comparison"),
    ("KPI 2: Research Impact Score", "`kpi_2_research_impact_score`", "Composite 0–100 citation influence score combining QS Citations per Faculty Score and THE Citations Score.", "Research Analytics"),
    ("KPI 3: Faculty-to-Student Ratio", "`kpi_3_faculty_per_100_students` / `kpi_3_faculty_student_score`", "Actual ratio of faculty per 100 students (derived from THE `student_staff_ratio`) alongside QS benchmark proxy score.", "Student Analytics"),
    ("KPI 4: International Student Percentage", "`kpi_4_intl_student_pct` / `kpi_4_intl_student_score`", "Actual percentage of international students enrolled (%) from THE alongside QS benchmark proxy score.", "Student Analytics, Country Comparison"),
    ("KPI 5: Academic Reputation Score", "`kpi_5_academic_reputation_score`", "0–100 academic peer reputation survey score from QS 2025 (supplemented by THE teaching environment score).", "University Overview, Research Analytics"),
    ("KPI 6: Research Productivity Index", "`kpi_6_research_productivity_index`", "Composite 0–100 index combining QS International Research Network diversity score and THE Research volume score.", "Research Analytics")
]

md.append("| KPI # & Name | Standardized Column | Mathematical & Methodological Formula | Target Tableau Dashboard |")
md.append("| --- | --- | --- | --- |")
for name, col, formula, dash in kpis_desc:
    md.append(f"| **{name}** | {col} | {formula} | {dash} |")

md.append("\n---\n")
md.append("## Statistical Summary of Engineered KPIs\n")
md.append("| KPI Column | Valid Count | Mean | Std Dev | Min | 25% | Median (50%) | 75% | Max |")
md.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")

for col, row in stats_df.iterrows():
    md.append(f"| `{col}` | {int(row['count']):,} | {row['mean']:.2f} | {row['std']:.2f} | {row['min']:.2f} | {row['25%']:.2f} | {row['50%']:.2f} | {row['75%']:.2f} | {row['max']:.2f} |")

md.append("\n---\n")
md.append("## Final Analytical Schemas in `../../data/final/`\n")

md.append("1. **`dim_country.csv`** (130 records)\n")
md.append("   - `country_id`, `country_name`, `region`\n\n")

md.append("2. **`dim_university.csv`** (2,992 records)\n")
md.append("   - `university_id`, `university_name`, `country_id`, `country_name`, `region`\n\n")

md.append("3. **`university_crosswalk.csv`** (3,060 records)\n")
md.append("   - `university_id`, `qs_name`, `the_name`, `wur_name`, `country_id`, `match_method`, `match_status`, `confidence`, `notes`\n\n")

md.append("4. **`fact_university_rankings.csv`** (3,060 records)\n")
md.append("   - Consolidated institutional rankings and 6 engineered KPIs.\n\n")

md.append("5. **`fact_country_education.csv`** (130 records)\n")
md.append("   - Macro-level country aggregates combining national higher education volume, average scores, and World Bank indicators.\n")

report_path = os.path.join(reports_dir, "kpi_summary_report.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Saved {report_path}")
