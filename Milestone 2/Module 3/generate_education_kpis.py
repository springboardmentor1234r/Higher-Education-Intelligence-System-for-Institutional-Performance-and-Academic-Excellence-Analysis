"""
EduVision_DV - Milestone 2 / Module 3: Education KPI Engineering
Author: Sujay S
Date: 2026-09-20

Purpose:
Engineers the 6 core Higher Education KPIs in accordance with Section 20-24 of the Project Guide:
1. Global Ranking Score (QS Overall Score / normalized ranking score)
2. Research Impact Score (QS Citations per Faculty / THE Citation Score)
3. Faculty-to-Student Ratio (Students per staff actual ratio)
4. International Student Percentage (True percentage of international students)
5. Academic Reputation Score (QS Academic Reputation Score)
6. Research Productivity Index (Composite: 0.50*Research + 0.30*Citations + 0.20*Research Collaboration)

Deliverables:
- scripts/generate_education_kpis.py
- 04_kpi_dataset/university_final_dataset.xlsx
- 04_kpi_dataset/kpi_master.csv
- data/Module_3/university_final_dataset.xlsx
- 04_kpi_engineering.ipynb
"""

import os
import pandas as pd
import numpy as np

def main():
    print("================================================================================")
    print("   EduVision_DV - Module 3: Education KPI Engineering Pipeline")
    print("================================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_dir = os.path.join(base_dir, "03_final_data_model")
    kpi_dir = os.path.join(base_dir, "04_kpi_dataset")
    mod3_dir = os.path.join(base_dir, "data", "Module_3")
    
    os.makedirs(kpi_dir, exist_ok=True)
    os.makedirs(mod3_dir, exist_ok=True)

    # 1. Load Star Schema Tables
    print("\n[1] Loading Star Schema Data Model...")
    dim_uni = pd.read_csv(os.path.join(model_dir, "dim_university.csv"))
    dim_country = pd.read_csv(os.path.join(model_dir, "dim_country.csv"))
    fact_perf = pd.read_csv(os.path.join(model_dir, "fact_university_performance.csv"))
    fact_res = pd.read_csv(os.path.join(model_dir, "fact_research.csv"))
    fact_stud = pd.read_csv(os.path.join(model_dir, "fact_student.csv"))
    fact_ed = pd.read_csv(os.path.join(model_dir, "fact_country_education.csv"))

    # 2. Engineer KPIs per University
    print("\n[2] Computing Six Defensible Educational KPIs...")
    
    # Merge performance, research, and student facts on university_id
    m1 = dim_uni.merge(fact_perf, on="university_id", how="left")
    m2 = m1.merge(fact_res.drop(columns=["year"], errors="ignore"), on="university_id", how="left")
    master = m2.merge(fact_stud.drop(columns=["year"], errors="ignore"), on="university_id", how="left")

    # KPI 1: Global Ranking Score (0-100 scale)
    # Source: QS Overall Score; if NaN for ranked universities outside top 500, calculate percentile score
    max_rank = master["global_rank"].max()
    rank_score_imputed = ((max_rank - master["global_rank"] + 1) / max_rank) * 100.0
    master["kpi_global_ranking_score"] = master["overall_score"].combine_first(rank_score_imputed).round(2)

    # KPI 2: Research Impact Score (0-100 scale)
    # Source: QS Citations per Faculty Score / THE Citation Score
    master["kpi_research_impact_score"] = master["citations_score"].combine_first(master["citation_score"]).round(2)

    # KPI 3: Faculty-to-Student Ratio (Actual Ratio: Students per Staff)
    # Source: WUR / THE actual ratio
    master["kpi_faculty_student_ratio"] = master["students_per_staff"].round(1)

    # KPI 4: International Student Percentage (True Percentage: 0 - 100%)
    # Source: WUR actual international student percentage
    master["kpi_international_student_pct"] = master["international_student_percentage"].round(1)

    # KPI 5: Academic Reputation Score (0-100 scale)
    # Source: QS Academic Reputation Score
    master["kpi_academic_reputation_score"] = master["academic_reputation"].round(2)

    # KPI 6: Research Productivity Index (Composite: 0-100 scale)
    # Formula: 0.50 * Research Score + 0.30 * Citation Score + 0.20 * International Research Network Score
    # We normalize each available component to 0-100 scale
    res_score = master["research_score"].combine_first(master["academic_reputation"])
    cit_score = master["kpi_research_impact_score"]
    net_score = master["research_network_score"].fillna(50.0)

    # Calculate transparent composite index
    master["kpi_research_productivity_index"] = (
        0.50 * res_score +
        0.30 * cit_score +
        0.20 * net_score
    ).round(2)

    print("    - All 6 KPIs calculated successfully!")
    print(master[[
        "university_id",
        "university_name",
        "kpi_global_ranking_score",
        "kpi_research_impact_score",
        "kpi_faculty_student_ratio",
        "kpi_international_student_pct",
        "kpi_academic_reputation_score",
        "kpi_research_productivity_index"
    ]].head(5))

    # 3. Create Clean KPI Master Table
    intl_count = master["international_students_y"] if "international_students_y" in master.columns else master.get("international_students", np.nan)
    intl_score = master["international_students_x"] if "international_students_x" in master.columns else np.nan

    kpi_master = pd.DataFrame({
        "university_id": master["university_id"],
        "university_name": master["university_name"],
        "country_id": master["country_id"],
        "country_name": master["country_name"],
        "region": master["region"],
        "global_rank": master["global_rank"],
        "kpi_global_ranking_score": master["kpi_global_ranking_score"],
        "kpi_research_impact_score": master["kpi_research_impact_score"],
        "kpi_faculty_student_ratio": master["kpi_faculty_student_ratio"],
        "kpi_international_student_pct": master["kpi_international_student_pct"],
        "kpi_academic_reputation_score": master["kpi_academic_reputation_score"],
        "kpi_research_productivity_index": master["kpi_research_productivity_index"],
        "total_students": master.get("total_students", np.nan),
        "international_students_count": intl_count,
        "international_students_score": intl_score,
        "female_male_ratio": master.get("female_male_ratio", "Unknown")
    })

    # 4. Export Deliverables
    print("\n[3] Exporting Analytical Deliverables...")
    
    # Export CSVs
    kpi_csv_path1 = os.path.join(kpi_dir, "kpi_master.csv")
    kpi_csv_path2 = os.path.join(model_dir, "kpi_master.csv")
    kpi_master.to_csv(kpi_csv_path1, index=False)
    kpi_master.to_csv(kpi_csv_path2, index=False)
    print(f"    - Exported: {kpi_csv_path1}")

    # Export multi-tab Excel workbook: university_final_dataset.xlsx
    excel_path1 = os.path.join(kpi_dir, "university_final_dataset.xlsx")
    excel_path2 = os.path.join(mod3_dir, "university_final_dataset.xlsx")
    excel_path3 = os.path.join(base_dir, "university_final_dataset.xlsx")

    with pd.ExcelWriter(excel_path1, engine="openpyxl") as writer:
        kpi_master.to_excel(writer, sheet_name="KPI_Master", index=False)
        dim_uni.to_excel(writer, sheet_name="Dim_University", index=False)
        dim_country.to_excel(writer, sheet_name="Dim_Country", index=False)
        fact_perf.to_excel(writer, sheet_name="Fact_Performance", index=False)
        fact_res.to_excel(writer, sheet_name="Fact_Research", index=False)
        fact_stud.to_excel(writer, sheet_name="Fact_Student", index=False)
        fact_ed.head(50000).to_excel(writer, sheet_name="Fact_Country_Ed", index=False)

    import shutil
    shutil.copy2(excel_path1, excel_path2)
    shutil.copy2(excel_path1, excel_path3)
    print(f"    - Multi-sheet Excel exported: {excel_path1}")
    print(f"    - Multi-sheet Excel exported: {excel_path2}")

    print("\n[SUCCESS] Module 3 KPI Engineering completed successfully!")

if __name__ == "__main__":
    main()
