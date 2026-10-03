import os
import pandas as pd
import numpy as np

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

os.makedirs(final_dir, exist_ok=True)
os.makedirs(doc_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# 1. Load Data
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_the = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)

dim_univ = pd.read_csv(os.path.join(final_dir, "dim_university.csv"))
crosswalk = pd.read_csv(os.path.join(final_dir, "university_crosswalk.csv"))

# Safe lookups
df_qs_unique = df_qs.drop_duplicates(subset=['university_name']).copy()
df_the_unique = df_the.drop_duplicates(subset=['university_name']).copy()

qs_lookup = df_qs_unique.set_index('university_name').to_dict(orient='index')
the_lookup = df_the_unique.set_index('university_name').to_dict(orient='index')

kpi_rows = []

for _, cw in crosswalk.iterrows():
    uid = cw['university_id']
    qs_name = cw['qs_name']
    the_name = cw['the_name']
    cid = cw['country_id']
    
    qs_data = qs_lookup.get(qs_name, {}) if pd.notna(qs_name) else {}
    the_data = the_lookup.get(the_name, {}) if pd.notna(the_name) else {}
    
    # Get institution name
    u_info = dim_univ[dim_univ['university_id'] == uid]
    u_name = u_info['university_name'].values[0] if len(u_info) > 0 else (qs_name if pd.notna(qs_name) else the_name)
    
    # Determine reference year (2025 if QS, 2023 if THE only)
    year = 2025 if pd.notna(qs_name) else 2023

    # Extract source fields
    qs_overall = qs_data.get('overall_score_numeric', np.nan)
    the_overall = the_data.get('overall_score_numeric', np.nan)
    
    qs_cit = qs_data.get('citations_per_faculty_score', np.nan)
    the_cit = the_data.get('citations_score', np.nan)
    
    the_stud_staff = the_data.get('student_staff_ratio', np.nan)
    the_pct_intl = the_data.get('pct_international_students', np.nan)
    
    qs_acad_rep = qs_data.get('academic_reputation_score', np.nan)
    the_teaching = the_data.get('teaching_score', np.nan)
    
    the_research = the_data.get('research_score', np.nan)
    qs_net = qs_data.get('international_research_network_score', np.nan)

    # -------------------------------------------------------------
    # KPI 1: Global Ranking Score
    # -------------------------------------------------------------
    overall_list = [s for s in [qs_overall, the_overall] if pd.notna(s)]
    global_ranking_score = round(float(np.mean(overall_list)), 2) if len(overall_list) > 0 else np.nan

    # -------------------------------------------------------------
    # KPI 2: Research Impact Score
    # -------------------------------------------------------------
    cit_list = [s for s in [qs_cit, the_cit] if pd.notna(s)]
    research_impact_score = round(float(np.mean(cit_list)), 2) if len(cit_list) > 0 else np.nan

    # -------------------------------------------------------------
    # KPI 3: Faculty-to-Student Ratio (Faculty per 100 students)
    # -------------------------------------------------------------
    if pd.notna(the_stud_staff) and float(the_stud_staff) > 0:
        faculty_student_ratio = round(100.0 / float(the_stud_staff), 2)
    else:
        faculty_student_ratio = np.nan

    # -------------------------------------------------------------
    # KPI 4: International Student Percentage (%)
    # -------------------------------------------------------------
    international_student_percentage = float(the_pct_intl) if pd.notna(the_pct_intl) else np.nan

    # -------------------------------------------------------------
    # KPI 5: Academic Reputation Score
    # -------------------------------------------------------------
    if pd.notna(qs_acad_rep):
        academic_reputation_score = float(qs_acad_rep)
    elif pd.notna(the_teaching):
        academic_reputation_score = float(the_teaching)
    else:
        academic_reputation_score = np.nan

    # -------------------------------------------------------------
    # KPI 6: Research Productivity Index (Approved Option 1 Formula)
    # Formula: 0.40 * S_citations + 0.35 * S_research + 0.25 * S_network
    # -------------------------------------------------------------
    s_citations = float(np.mean(cit_list)) if len(cit_list) > 0 else np.nan
    s_research = float(the_research) if pd.notna(the_research) else np.nan
    s_network = float(qs_net) if pd.notna(qs_net) else np.nan

    weights_sum = 0.0
    weighted_val = 0.0

    if pd.notna(s_citations):
        weighted_val += 0.40 * s_citations
        weights_sum += 0.40
    if pd.notna(s_research):
        weighted_val += 0.35 * s_research
        weights_sum += 0.35
    if pd.notna(s_network):
        weighted_val += 0.25 * s_network
        weights_sum += 0.25

    if weights_sum > 0:
        research_productivity_index = round(weighted_val / weights_sum, 2)
    else:
        research_productivity_index = np.nan

    kpi_rows.append({
        "university_id": uid,
        "university_name": u_name,
        "country_id": cid,
        "year": year,
        "global_ranking_score": global_ranking_score,
        "research_impact_score": research_impact_score,
        "faculty_student_ratio": faculty_student_ratio,
        "international_student_percentage": international_student_percentage,
        "academic_reputation_score": academic_reputation_score,
        "research_productivity_index": research_productivity_index
    })

df_kpi_univ = pd.DataFrame(kpi_rows)
kpi_univ_path = os.path.join(final_dir, "kpi_university.csv")
df_kpi_univ.to_csv(kpi_univ_path, index=False, encoding="utf-8")
print(f"Exported {kpi_univ_path} ({len(df_kpi_univ)} rows)")


# -------------------------------------------------------------
# Validation & Outlier Check
# -------------------------------------------------------------
val_kpi_records = []
kpi_cols = [
    "global_ranking_score",
    "research_impact_score",
    "faculty_student_ratio",
    "international_student_percentage",
    "academic_reputation_score",
    "research_productivity_index"
]

for col in kpi_cols:
    s = df_kpi_univ[col].dropna()
    total_cnt = len(df_kpi_univ)
    valid_cnt = len(s)
    missing_cnt = total_cnt - valid_cnt
    missing_pct = round((missing_cnt / total_cnt * 100), 2)
    
    c_min = round(float(s.min()), 2) if valid_cnt > 0 else np.nan
    c_max = round(float(s.max()), 2) if valid_cnt > 0 else np.nan
    c_mean = round(float(s.mean()), 2) if valid_cnt > 0 else np.nan
    c_std = round(float(s.std()), 2) if valid_cnt > 0 else np.nan
    
    # Outlier detection using IQR method (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
    if valid_cnt > 0:
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_cnt = int(((s < lower_bound) | (s > upper_bound)).sum())
    else:
        outlier_cnt = 0
        
    # Check impossible values (outside expected boundaries e.g. < 0 or > 100 for percentage/scores)
    if col in ["global_ranking_score", "research_impact_score", "international_student_percentage", "academic_reputation_score", "research_productivity_index"]:
        impossible_cnt = int(((s < 0) | (s > 100)).sum())
    elif col == "faculty_student_ratio":
        impossible_cnt = int((s <= 0).sum())
    else:
        impossible_cnt = 0

    val_kpi_records.append({
        "KPI Name": col,
        "Total Records": total_cnt,
        "Valid Count": valid_cnt,
        "Missing Count": missing_cnt,
        "Missing Percentage (%)": missing_pct,
        "Min": c_min,
        "Max": c_max,
        "Mean": c_mean,
        "Std Dev": c_std,
        "Outlier Count (IQR)": outlier_cnt,
        "Impossible Value Count": impossible_cnt,
        "Validation Status": "PASSED" if impossible_cnt == 0 else "WARNING"
    })

df_kpi_val = pd.DataFrame(val_kpi_records)
kpi_val_csv_path = os.path.join(reports_dir, "kpi_validation_report.csv")
df_kpi_val.to_csv(kpi_val_csv_path, index=False, encoding="utf-8")
print(f"Exported {kpi_val_csv_path}")


# -------------------------------------------------------------
# Documentation: kpi_calculation_methodology.md
# -------------------------------------------------------------
md = []
md.append("# EduVision_DV – KPI Calculation & Engineering Methodology\n")
md.append("## Executive Summary\n")
md.append("This technical document outlines the exact, step-by-step mathematical formulas, normalization schemes, and missing-value rules used to calculate the **six project KPIs** stored in `../data/final/kpi_university.csv`.\n")

md.append("--- \n")
md.append("## Master KPI Technical Specifications\n\n")

# KPI 1
md.append("### 1. Global Ranking Score (`global_ranking_score`)\n")
md.append("- **Purpose**: Measures total global academic standing.\n")
md.append("- **Source Fields**: `overall_score_numeric` (QS 2025), `overall_score_numeric` (THE 2023).\n")
md.append("- **Formula**:\n")
md.append("  $$\\text{global\\_ranking\\_score} = \\text{mean}(\\text{qs\\_overall}, \\text{the\\_overall})$$\n")
md.append("  If only one ranking body publishes an overall score for an institution, that available score is used.\n")
md.append("- **Scale & Unit**: `0.00` to `100.00` (Index Score).\n")
md.append("- **Missing Value Rule**: Preserved as `NaN`. Unranked institutions remain null.\n\n")

# KPI 2
md.append("### 2. Research Impact Score (`research_impact_score`)\n")
md.append("- **Purpose**: Evaluates scholarly citation density and research influence.\n")
md.append("- **Source Fields**: `citations_per_faculty_score` (QS 2025), `citations_score` (THE 2023).\n")
md.append("- **Formula**:\n")
md.append("  $$\\text{research\\_impact\\_score} = \\text{mean}(\\text{qs\\_citations\\_per\\_faculty}, \\text{the\\_citations})$$\n")
md.append("- **Scale & Unit**: `0.00` to `100.00` (Index Score).\n")
md.append("- **Missing Value Rule**: Preserved as `NaN`.\n\n")

# KPI 3
md.append("### 3. Faculty-to-Student Ratio (`faculty_student_ratio`)\n")
md.append("- **Purpose**: Quantifies academic staff headcount per student enrolled.\n")
md.append("- **Source Field**: `student_staff_ratio` (THE 2023).\n")
md.append("- **Formula**:\n")
md.append("  $$\\text{faculty\\_student\\_ratio} = \\frac{100.0}{\\text{student\\_staff\\_ratio}}$$\n")
md.append("- **Scale & Unit**: Ratio (Faculty members per 100 Students).\n")
md.append("- **Metric Direction**: Inverted so higher values indicate greater teaching capacity per student.\n")
md.append("- **Missing Value Rule**: Preserved as `NaN`.\n\n")

# KPI 4
md.append("### 4. International Student Percentage (`international_student_percentage`)\n")
md.append("- **Purpose**: Measures the proportion of international students in the student body.\n")
md.append("- **Source Field**: `pct_international_students` (THE 2023).\n")
md.append("- **Formula**:\n")
md.append("  $$\\text{international\\_student\\_percentage} = \\text{pct\\_international\\_students}$$\n")
md.append("- **Scale & Unit**: `0.0%` to `100.0%` (Percentage).\n")
md.append("- **Missing Value Rule**: Preserved as `NaN`.\n\n")

# KPI 5
md.append("### 5. Academic Reputation Score (`academic_reputation_score`)\n")
md.append("- **Purpose**: Captures international academic peer survey perception.\n")
md.append("- **Source Fields**: `academic_reputation_score` (QS 2025), `teaching_score` (THE 2023 proxy).\n")
md.append("- **Formula**:\n")
md.append("  $$\\text{academic\\_reputation\\_score} = \\text{Coalesce}(\\text{qs\\_academic\\_reputation}, \\text{the\\_teaching})$$\n")
md.append("- **Scale & Unit**: `0.00` to `100.00` (Index Score).\n")
md.append("- **Missing Value Rule**: Preserved as `NaN`.\n\n")

# KPI 6
md.append("### 6. Research Productivity Index (`research_productivity_index`)\n")
md.append("- **Purpose**: Synthesizes citation impact, research volume, and international network breadth.\n")
md.append("- **Approved Methodological Formula** (Option 1 Tri-Pillar Balanced Model):\n")
md.append("  $$\\text{research\\_productivity\\_index} = \\frac{0.40 \\cdot S_{\\text{citations}} + 0.35 \\cdot S_{\\text{research}} + 0.25 \\cdot S_{\\text{network}}}{W_{\\text{sum}}}$$\n")
md.append("  Where:\n")
md.append("  - $S_{\\text{citations}} = \\text{mean}(\\text{qs\\_citations}, \\text{the\\_citations})$\n")
md.append("  - $S_{\\text{research}} = \\text{the\\_research\\_score}$\n")
md.append("  - $S_{\\text{network}} = \\text{qs\\_international\\_research\\_network\\_score}$\n")
md.append("  - $W_{\\text{sum}}$ is the dynamic sum of weights for available non-null components.\n")
md.append("- **Scale & Unit**: `0.00` to `100.00` (Composite Index).\n")
md.append("- **Missing Value Rule**: Preserved as `NaN` if all components are missing.\n\n")

md.append("---\n")
md.append("## Validation Summary Table\n")
md.append("| KPI Name | Valid Count | Missing % | Min | Max | Mean | Outliers (IQR) | Impossible Values | Status |")
md.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")

for r in val_kpi_records:
    md.append(f"| `{r['KPI Name']}` | {r['Valid Count']:,} | {r['Missing Percentage (%)']}% | {r['Min']} | {r['Max']} | {r['Mean']} | {r['Outlier Count (IQR)']} | {r['Impossible Value Count']} | **{r['Validation Status']}** |")

methodology_doc_path = os.path.join(doc_dir, "kpi_calculation_methodology.md")
with open(methodology_doc_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Exported {methodology_doc_path}")

