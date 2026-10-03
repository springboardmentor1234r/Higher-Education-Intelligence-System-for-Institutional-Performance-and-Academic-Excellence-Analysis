import os
import pandas as pd
import numpy as np

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

# 1. Load Cleaned Datasets & Crosswalk
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_the = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)
df_wb_ed = pd.read_csv(os.path.join(cleaned_dir, "world_bank_education_cleaned.csv"), low_memory=False)
df_wb_cntry = pd.read_csv(os.path.join(cleaned_dir, "world_bank_country_cleaned.csv"), low_memory=False)

dim_country = pd.read_csv(os.path.join(final_dir, "dim_country.csv"))
dim_univ = pd.read_csv(os.path.join(final_dir, "dim_university.csv"))
crosswalk = pd.read_csv(os.path.join(final_dir, "university_crosswalk.csv"))

print(f"Crosswalk records: {len(crosswalk)}")

# Build lookup dicts safely handling non-unique indexes
df_qs_unique = df_qs.drop_duplicates(subset=['university_name']).copy()
df_the_unique = df_the.drop_duplicates(subset=['university_name']).copy()

qs_lookup = df_qs_unique.set_index('university_name').to_dict(orient='index')
the_lookup = df_the_unique.set_index('university_name').to_dict(orient='index')

fact_rows = []

for _, cw in crosswalk.iterrows():
    uid = cw['university_id']
    qs_name = cw['qs_name']
    the_name = cw['the_name']
    cid = cw['country_id']
    match_status = cw['match_status']
    
    qs_data = qs_lookup.get(qs_name, {}) if pd.notna(qs_name) else {}
    the_data = the_lookup.get(the_name, {}) if pd.notna(the_name) else {}
    
    u_info = dim_univ[dim_univ['university_id'] == uid]
    u_name = u_info['university_name'].values[0] if len(u_info) > 0 else (qs_name if pd.notna(qs_name) else the_name)
    c_info = dim_country[dim_country['country_id'] == cid]
    c_name = c_info['country_name'].values[0] if len(c_info) > 0 else "Unknown"
    region = c_info['region'].values[0] if len(c_info) > 0 else "Other / Global"

    # Extract Scores & Ranks
    qs_rank_2025 = qs_data.get('rank_2025_numeric', np.nan)
    the_rank_2023 = the_data.get('world_rank_numeric', np.nan)
    
    qs_overall_score = qs_data.get('overall_score_numeric', np.nan)
    the_overall_score = the_data.get('overall_score_numeric', np.nan)
    
    qs_cit_score = qs_data.get('citations_per_faculty_score', np.nan)
    the_cit_score = the_data.get('citations_score', np.nan)
    
    qs_acad_rep = qs_data.get('academic_reputation_score', np.nan)
    the_teaching_score = the_data.get('teaching_score', np.nan)
    
    qs_intl_net = qs_data.get('international_research_network_score', np.nan)
    the_research_score = the_data.get('research_score', np.nan)
    
    qs_fac_stud_score = qs_data.get('faculty_student_score', np.nan)
    the_stud_staff_ratio = the_data.get('student_staff_ratio', np.nan)
    
    qs_intl_stud_score = qs_data.get('international_students_score', np.nan)
    the_pct_intl_stud = the_data.get('pct_international_students', np.nan)
    the_num_students = the_data.get('num_students', np.nan)

    # Calculate 6 Project KPIs
    
    # 1. Global Ranking Score (Composite 0-100)
    scores_for_global = [s for s in [qs_overall_score, the_overall_score] if pd.notna(s)]
    kpi_1_global_ranking_score = round(float(np.mean(scores_for_global)), 2) if scores_for_global else np.nan
    
    # 2. Research Impact Score (Composite 0-100)
    scores_for_research = [s for s in [qs_cit_score, the_cit_score] if pd.notna(s)]
    kpi_2_research_impact_score = round(float(np.mean(scores_for_research)), 2) if scores_for_research else np.nan
    
    # 3. Faculty-to-Student Ratio (Actual Ratio & Score)
    kpi_3_faculty_per_100_students = round(100.0 / float(the_stud_staff_ratio), 2) if pd.notna(the_stud_staff_ratio) and the_stud_staff_ratio > 0 else np.nan
    kpi_3_faculty_student_score = qs_fac_stud_score if pd.notna(qs_fac_stud_score) else np.nan
    
    # 4. International Student Percentage (Actual % & Score)
    kpi_4_intl_student_pct = float(the_pct_intl_stud) if pd.notna(the_pct_intl_stud) else np.nan
    kpi_4_intl_student_score = qs_intl_stud_score if pd.notna(qs_intl_stud_score) else np.nan
    
    # 5. Academic Reputation Score (0-100)
    kpi_5_academic_reputation_score = float(qs_acad_rep) if pd.notna(qs_acad_rep) else (float(the_teaching_score) if pd.notna(the_teaching_score) else np.nan)
    
    # 6. Research Productivity Index (Composite 0-100)
    scores_for_prod = [s for s in [qs_intl_net, the_research_score] if pd.notna(s)]
    kpi_6_research_productivity_index = round(float(np.mean(scores_for_prod)), 2) if scores_for_prod else np.nan

    fact_rows.append({
        "university_id": uid,
        "university_name": u_name,
        "country_id": cid,
        "country_name": c_name,
        "region": region,
        "match_status": match_status,
        
        # Raw Ranks & Scores
        "qs_rank_2025": qs_rank_2025,
        "the_rank_2023": the_rank_2023,
        "qs_overall_score": qs_overall_score,
        "the_overall_score": the_overall_score,
        
        # 6 Project KPIs
        "kpi_1_global_ranking_score": kpi_1_global_ranking_score,
        "kpi_2_research_impact_score": kpi_2_research_impact_score,
        "kpi_3_faculty_per_100_students": kpi_3_faculty_per_100_students,
        "kpi_3_faculty_student_score": kpi_3_faculty_student_score,
        "kpi_4_intl_student_pct": kpi_4_intl_student_pct,
        "kpi_4_intl_student_score": kpi_4_intl_student_score,
        "kpi_5_academic_reputation_score": kpi_5_academic_reputation_score,
        "kpi_6_research_productivity_index": kpi_6_research_productivity_index,
        
        # Supporting Institutional Volume Attributes
        "total_students": the_num_students,
        "student_staff_ratio": the_stud_staff_ratio
    })

fact_univ_df = pd.DataFrame(fact_rows)
fact_univ_path = os.path.join(final_dir, "fact_university_rankings.csv")
fact_univ_df.to_csv(fact_univ_path, index=False, encoding="utf-8")
print(f"Saved fact_university_rankings.csv ({len(fact_univ_df)} rows)")

# Build fact_country_education.csv
country_agg = fact_univ_df.groupby('country_id').agg({
    'university_id': 'count',
    'kpi_1_global_ranking_score': 'mean',
    'kpi_2_research_impact_score': 'mean',
    'kpi_4_intl_student_pct': 'mean',
    'kpi_5_academic_reputation_score': 'mean',
    'kpi_6_research_productivity_index': 'mean'
}).reset_index()

country_agg.rename(columns={
    'university_id': 'ranked_university_count',
    'kpi_1_global_ranking_score': 'avg_global_ranking_score',
    'kpi_2_research_impact_score': 'avg_research_impact_score',
    'kpi_4_intl_student_pct': 'avg_intl_student_pct',
    'kpi_5_academic_reputation_score': 'avg_academic_reputation_score',
    'kpi_6_research_productivity_index': 'avg_research_productivity_index'
}, inplace=True)

fact_country_df = pd.merge(dim_country, country_agg, on='country_id', how='left')
fact_country_df['ranked_university_count'] = fact_country_df['ranked_university_count'].fillna(0).astype(int)

for col in ['avg_global_ranking_score', 'avg_research_impact_score', 'avg_intl_student_pct', 'avg_academic_reputation_score', 'avg_research_productivity_index']:
    fact_country_df[col] = fact_country_df[col].round(2)

fact_country_path = os.path.join(final_dir, "fact_country_education.csv")
fact_country_df.to_csv(fact_country_path, index=False, encoding="utf-8")
print(f"Saved fact_country_education.csv ({len(fact_country_df)} rows)")

