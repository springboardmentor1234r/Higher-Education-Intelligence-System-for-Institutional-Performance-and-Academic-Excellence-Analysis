import os
import pandas as pd
import numpy as np

BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
FINAL_DIR = os.path.join(BASE_DIR, "data", "final")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

def run_validation():
    # Load all cleaned and final datasets
    dim_country = pd.read_csv(os.path.join(CLEANED_DIR, "dim_country.csv"))
    dim_university = pd.read_csv(os.path.join(CLEANED_DIR, "dim_university.csv"))
    f_perf = pd.read_csv(os.path.join(CLEANED_DIR, "fact_university_performance.csv"))
    f_research = pd.read_csv(os.path.join(CLEANED_DIR, "fact_research.csv"))
    f_stud = pd.read_csv(os.path.join(CLEANED_DIR, "fact_student.csv"))
    f_country_ed = pd.read_csv(os.path.join(CLEANED_DIR, "fact_country_education.csv"))
    
    m_df = pd.read_csv(os.path.join(FINAL_DIR, "eduvision_final_dataset.csv"))
    kpi_summary = pd.read_csv(os.path.join(FINAL_DIR, "kpi_summary.csv"))
    
    # Validation checks
    checks = []
    
    # 1. Primary Key Uniqueness
    dup_c_id = dim_country.duplicated(subset=['country_id']).sum()
    checks.append(('dim_country Duplicate country_id Count', dup_c_id, dup_c_id == 0))
    
    dup_u_id = dim_university.duplicated(subset=['university_id']).sum()
    checks.append(('dim_university Duplicate university_id Count', dup_u_id, dup_u_id == 0))
    
    # 2. Referential Integrity
    valid_uids = set(dim_university['university_id'])
    valid_cids = set(dim_country['country_id'])
    
    unmatched_u_perf = set(f_perf['university_id']) - valid_uids
    checks.append(('fact_university_performance Unmatched university_id Count', len(unmatched_u_perf), len(unmatched_u_perf) == 0))
    
    unmatched_u_res = set(f_research['university_id']) - valid_uids
    checks.append(('fact_research Unmatched university_id Count', len(unmatched_u_res), len(unmatched_u_res) == 0))
    
    unmatched_u_stud = set(f_stud['university_id']) - valid_uids
    checks.append(('fact_student Unmatched university_id Count', len(unmatched_u_stud), len(unmatched_u_stud) == 0))
    
    unmatched_c_ed = set(f_country_ed['country_id']) - valid_cids
    checks.append(('fact_country_education Unmatched country_id Count', len(unmatched_c_ed), len(unmatched_c_ed) == 0))
    
    # 3. Numeric Range Validation
    invalid_ranks = f_perf[(f_perf['global_rank'] <= 0) | (f_perf['global_rank'] > 3000)]['global_rank'].count()
    checks.append(('fact_university_performance Invalid global_rank Out of Bounds', invalid_ranks, invalid_ranks == 0))
    
    invalid_scores = f_perf[(f_perf['overall_score'] < 0) | (f_perf['overall_score'] > 100)]['overall_score'].count()
    checks.append(('fact_university_performance Invalid overall_score Out of Bounds (0-100)', invalid_scores, invalid_scores == 0))
    
    invalid_pcts = f_stud[(f_stud['international_student_percentage'] < 0) | (f_stud['international_student_percentage'] > 100)]['international_student_percentage'].count()
    checks.append(('fact_student Invalid intl_student_pct Out of Bounds (0-100)', invalid_pcts, invalid_pcts == 0))
    
    # Generate Markdown Report
    md = "# EduVision Data Quality and Final Validation Report\n\n"
    md += "This report summarizes final automated data quality checks, referential integrity, schema verification, and completeness statistics.\n\n"
    md += "## 1. Automated Quality Check Matrix\n\n"
    md += "| Check Description | Observed Value | Status |\n"
    md += "|---|---|---|\n"
    
    all_passed = True
    for desc, val, status in checks:
        st_str = "PASSED" if status else "FAILED"
        if not status:
            all_passed = False
        md += f"| {desc} | `{val}` | **{st_str}** |\n"
        
    md += "\n"
    md += f"**Overall Validation Result**: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED'}\n\n"
    
    md += "## 2. Table Summary & Row Counts\n\n"
    md += f"- `dim_country`: {len(dim_country):,} rows x {len(dim_country.columns)} cols\n"
    md += f"- `dim_university`: {len(dim_university):,} rows x {len(dim_university.columns)} cols\n"
    md += f"- `fact_university_performance`: {len(f_perf):,} rows x {len(f_perf.columns)} cols\n"
    md += f"- `fact_research`: {len(f_research):,} rows x {len(f_research.columns)} cols\n"
    md += f"- `fact_student`: {len(f_stud):,} rows x {len(f_stud.columns)} cols\n"
    md += f"- `fact_country_education`: {len(f_country_ed):,} rows x {len(f_country_ed.columns)} cols\n"
    md += f"- `eduvision_final_dataset`: {len(m_df):,} rows x {len(m_df.columns)} cols\n"
    md += f"- `kpi_summary`: {len(kpi_summary):,} rows x {len(kpi_summary.columns)} cols\n\n"
    
    md += "## 3. KPI Completeness Summary (% Non-Null)\n\n"
    md += "| KPI Name | Non-Null Count | Total Rows | Completeness % |\n"
    md += "|---|---|---|---|\n"
    kpi_cols = ['kpi1_global_ranking_score', 'kpi2_research_impact_score', 'kpi3_faculty_student_ratio', 'kpi4_international_student_pct', 'kpi5_academic_reputation_score', 'kpi6_research_productivity_index']
    for kcol in kpi_cols:
        non_null = m_df[kcol].notnull().sum()
        total = len(m_df)
        pct = round(non_null / total * 100, 2)
        md += f"| `{kcol}` | {non_null:,} | {total:,} | {pct}% |\n"
        
    report_path = os.path.join(DOCS_DIR, "data_quality_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Final data quality report saved to {report_path}")
    return all_passed

if __name__ == "__main__":
    run_validation()
