import os
import pandas as pd
import numpy as np

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
doc_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\documentation"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

# 1. Load Cleaned Datasets & Crosswalk
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_the = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)
df_wb_ed = pd.read_csv(os.path.join(cleaned_dir, "world_bank_education_cleaned.csv"), low_memory=False)
df_wb_cntry = pd.read_csv(os.path.join(cleaned_dir, "world_bank_country_cleaned.csv"), low_memory=False)

dim_country = pd.read_csv(os.path.join(final_dir, "dim_country.csv"))
crosswalk = pd.read_csv(os.path.join(final_dir, "university_crosswalk.csv"))

print(f"Crosswalk records: {len(crosswalk)}")

# -------------------------------------------------------------
# 1. Build dim_university.csv directly from crosswalk
# -------------------------------------------------------------
dim_univ_rows = []
country_info_map = dim_country.set_index('country_id').to_dict(orient='index')

for _, r in crosswalk.iterrows():
    uid = r['university_id']
    qs_name = r['qs_name']
    the_name = r['the_name']
    cid = r['country_id']
    
    # Preferred display name: QS name if present, else THE name
    u_display_name = qs_name if pd.notna(qs_name) else the_name
    c_data = country_info_map.get(cid, {"country_name": "Unknown", "region": "Other / Global"})
    
    dim_univ_rows.append({
        "university_id": uid,
        "university_name": u_display_name,
        "country_id": cid,
        "country_name": c_data.get("country_name", "Unknown"),
        "region": c_data.get("region", "Other / Global")
    })

dim_univ_export = pd.DataFrame(dim_univ_rows).drop_duplicates(subset=['university_id']).reset_index(drop=True)
dim_univ_export.to_csv(os.path.join(final_dir, "dim_university.csv"), index=False, encoding="utf-8")
print(f"Exported dim_university.csv ({len(dim_univ_export)} rows)", flush=True)

dim_country_export = dim_country[['country_id', 'country_name', 'region']].copy()
dim_country_export.to_csv(os.path.join(final_dir, "dim_country.csv"), index=False, encoding="utf-8")
print(f"Exported dim_country.csv ({len(dim_country_export)} rows)", flush=True)

# Build lookups for facts
df_qs_unique = df_qs.drop_duplicates(subset=['university_name']).copy()
df_the_unique = df_the.drop_duplicates(subset=['university_name']).copy()

qs_lookup = df_qs_unique.set_index('university_name').to_dict(orient='index')
the_lookup = df_the_unique.set_index('university_name').to_dict(orient='index')

# -------------------------------------------------------------
# 3. Build fact_university_performance.csv
# -------------------------------------------------------------
perf_rows = []

for _, cw in crosswalk.iterrows():
    uid = cw['university_id']
    qs_name = cw['qs_name']
    the_name = cw['the_name']
    
    if pd.notna(qs_name) and qs_name in qs_lookup:
        q_data = qs_lookup[qs_name]
        perf_rows.append({
            "university_id": uid,
            "year": 2025,
            "source_ranking": "QS World University Rankings 2025",
            "global_rank": q_data.get('rank_2025_numeric', np.nan),
            "overall_score": q_data.get('overall_score_numeric', np.nan),
            "academic_reputation": q_data.get('academic_reputation_score', np.nan),
            "employer_reputation": q_data.get('employer_reputation_score', np.nan),
            "faculty_student_score": q_data.get('faculty_student_score', np.nan),
            "employment_outcomes_score": q_data.get('employment_outcomes_score', np.nan),
            "sustainability_score": q_data.get('sustainability_score', np.nan)
        })
        
    if pd.notna(the_name) and the_name in the_lookup:
        t_data = the_lookup[the_name]
        perf_rows.append({
            "university_id": uid,
            "year": 2023,
            "source_ranking": "THE World University Rankings 2023",
            "global_rank": t_data.get('world_rank_numeric', np.nan),
            "overall_score": t_data.get('overall_score_numeric', np.nan),
            "academic_reputation": t_data.get('teaching_score', np.nan),
            "employer_reputation": np.nan,
            "faculty_student_score": np.nan,
            "employment_outcomes_score": np.nan,
            "sustainability_score": np.nan
        })

df_fact_perf = pd.DataFrame(perf_rows).drop_duplicates(subset=['university_id', 'year', 'source_ranking'])
df_fact_perf.to_csv(os.path.join(final_dir, "fact_university_performance.csv"), index=False, encoding="utf-8")
print(f"Exported fact_university_performance.csv ({len(df_fact_perf)} rows)", flush=True)


# -------------------------------------------------------------
# 4. Build fact_research.csv
# -------------------------------------------------------------
research_rows = []

for _, cw in crosswalk.iterrows():
    uid = cw['university_id']
    qs_name = cw['qs_name']
    the_name = cw['the_name']
    
    if pd.notna(qs_name) and qs_name in qs_lookup:
        q_data = qs_lookup[qs_name]
        cit_score = q_data.get('citations_per_faculty_score', np.nan)
        prod_score = q_data.get('international_research_network_score', np.nan)
        
        research_rows.append({
            "university_id": uid,
            "year": 2025,
            "source_ranking": "QS World University Rankings 2025",
            "research_score": np.nan,
            "citation_score": cit_score,
            "research_impact": cit_score,
            "research_productivity": prod_score,
            "citations_per_faculty_score": cit_score,
            "international_research_network_score": prod_score,
            "industry_income_score": np.nan
        })
        
    if pd.notna(the_name) and the_name in the_lookup:
        t_data = the_lookup[the_name]
        r_score = t_data.get('research_score', np.nan)
        c_score = t_data.get('citations_score', np.nan)
        ind_score = t_data.get('industry_income_score', np.nan)
        
        research_rows.append({
            "university_id": uid,
            "year": 2023,
            "source_ranking": "THE World University Rankings 2023",
            "research_score": r_score,
            "citation_score": c_score,
            "research_impact": c_score,
            "research_productivity": r_score,
            "citations_per_faculty_score": np.nan,
            "international_research_network_score": np.nan,
            "industry_income_score": ind_score
        })

df_fact_research = pd.DataFrame(research_rows).drop_duplicates(subset=['university_id', 'year', 'source_ranking'])
df_fact_research.to_csv(os.path.join(final_dir, "fact_research.csv"), index=False, encoding="utf-8")
print(f"Exported fact_research.csv ({len(df_fact_research)} rows)", flush=True)


# -------------------------------------------------------------
# 5. Build fact_student.csv
# -------------------------------------------------------------
student_rows = []

for _, cw in crosswalk.iterrows():
    uid = cw['university_id']
    qs_name = cw['qs_name']
    the_name = cw['the_name']
    
    if pd.notna(qs_name) and qs_name in qs_lookup:
        q_data = qs_lookup[qs_name]
        student_rows.append({
            "university_id": uid,
            "year": 2025,
            "source_ranking": "QS World University Rankings 2025",
            "total_students": np.nan,
            "students_per_staff": np.nan,
            "international_students": np.nan,
            "international_student_percentage": np.nan,
            "gender_ratio": np.nan,
            "international_students_score": q_data.get('international_students_score', np.nan),
            "international_faculty_score": q_data.get('international_faculty_score', np.nan),
            "international_outlook_score": np.nan
        })
        
    if pd.notna(the_name) and the_name in the_lookup:
        t_data = the_lookup[the_name]
        tot_stud = t_data.get('num_students', np.nan)
        pct_intl = t_data.get('pct_international_students', np.nan)
        calc_intl_count = round(tot_stud * (pct_intl / 100.0)) if pd.notna(tot_stud) and pd.notna(pct_intl) else np.nan
        
        student_rows.append({
            "university_id": uid,
            "year": 2023,
            "source_ranking": "THE World University Rankings 2023",
            "total_students": tot_stud,
            "students_per_staff": t_data.get('student_staff_ratio', np.nan),
            "international_students": calc_intl_count,
            "international_student_percentage": pct_intl,
            "gender_ratio": t_data.get('female_male_ratio', np.nan),
            "international_students_score": np.nan,
            "international_faculty_score": np.nan,
            "international_outlook_score": t_data.get('international_outlook_score', np.nan)
        })

df_fact_student = pd.DataFrame(student_rows).drop_duplicates(subset=['university_id', 'year', 'source_ranking'])
df_fact_student.to_csv(os.path.join(final_dir, "fact_student.csv"), index=False, encoding="utf-8")
print(f"Exported fact_student.csv ({len(df_fact_student)} rows)", flush=True)


# -------------------------------------------------------------
# 6. Build fact_country_education.csv
# -------------------------------------------------------------
country_code_to_cid = {}
for _, r in dim_country.iterrows():
    match = df_wb_cntry[df_wb_cntry['table_name'].str.lower() == r['country_name'].lower()]
    if len(match) > 0:
        country_code_to_cid[match['country_code'].values[0]] = r['country_id']

year_cols = [c for c in df_wb_ed.columns if c.startswith('year_') and c[5:].isdigit()]
year_cols_valid = [c for c in year_cols if int(c[5:]) <= 2017]

tertiary_keywords = [
    'tertiary', 'expenditure', 'gdp', 'enrollment', 'enrolment', 'gross', 'net',
    'pupil', 'teacher', 'ratio', 'mobility', 'inbound', 'outbound', 'literacy'
]

df_ed_filtered = df_wb_ed[
    df_wb_ed['indicator_name'].astype(str).str.lower().apply(lambda x: any(k in x for k in tertiary_keywords))
].copy()

melted = pd.melt(
    df_ed_filtered,
    id_vars=['country_name', 'country_code', 'indicator_name', 'indicator_code'],
    value_vars=year_cols_valid,
    var_name='year_col',
    value_name='value'
).dropna(subset=['value'])

melted['year'] = melted['year_col'].str.replace('year_', '').astype(int)
melted['country_id'] = melted['country_code'].map(country_code_to_cid)

name_to_cid = dict(zip(dim_country['country_name'], dim_country['country_id']))
melted['country_id'] = melted['country_id'].fillna(melted['country_name'].map(name_to_cid))
melted = melted.dropna(subset=['country_id']).copy()

fact_country_ed = melted[['country_id', 'year', 'indicator_name', 'indicator_code', 'value']].rename(
    columns={'indicator_name': 'indicator'}
)

fact_country_ed.to_csv(os.path.join(final_dir, "fact_country_education.csv"), index=False, encoding="utf-8")
print(f"Exported fact_country_education.csv ({len(fact_country_ed):,} rows)", flush=True)

