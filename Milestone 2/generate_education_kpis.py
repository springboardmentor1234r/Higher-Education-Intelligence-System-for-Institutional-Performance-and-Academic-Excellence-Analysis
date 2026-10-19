import os
import sys
import pandas as pd
import numpy as np
import importlib.util

BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
RAW_DIR = os.path.join(BASE_DIR, "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
FINAL_DIR = os.path.join(BASE_DIR, "data", "final")
SCRIPTS_DIR = os.path.join(BASE_DIR, "notebooks_or_scripts")
os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# Helper to import files with numbers in names
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

dc = load_module("data_cleaning", os.path.join(SCRIPTS_DIR, "02_data_cleaning.py"))
std = load_module("standardization", os.path.join(SCRIPTS_DIR, "03_standardization.py"))

def run_kpi_engineering():
    # Load dimensions
    dim_country = pd.read_csv(os.path.join(CLEANED_DIR, "dim_country.csv"))
    dim_university = pd.read_csv(os.path.join(CLEANED_DIR, "dim_university.csv"))
    
    country_lookup = dict(zip(dim_country['country_name'], dim_country['country_id']))
    
    # Load raw datasets
    df_qs = pd.read_csv(os.path.join(RAW_DIR, "qs_2025.csv"), encoding='latin1')
    df_the = pd.read_csv(os.path.join(RAW_DIR, "the_2024.csv"), encoding='latin1')
    df_wur = pd.read_csv(os.path.join(RAW_DIR, "wur_2023.csv"), encoding='latin1')
    
    c_qs = dc.clean_qs(df_qs)
    c_the = dc.clean_the(df_the)
    c_wur = dc.clean_wur(df_wur)
    
    # Add standardized country name and token key for matching
    for df, name_col, country_col in [(c_qs, 'Institution_Name', 'Location'),
                                      (c_the, 'name', 'location'),
                                      (c_wur, 'Name of University', 'Location')]:
        df['country_name'] = df[country_col].apply(std.clean_country_name)
        df['country_id'] = df['country_name'].map(country_lookup)
        df['clean_name'] = df[name_col].apply(std.clean_uni_string)
        df['token_key'] = df['clean_name'].apply(std.uni_token_key)
        
    # Match against dim_university lookup (country_id, token_key) -> university_id
    uni_lookup = dict(zip(zip(dim_university['country_id'], dim_university['university_name'].apply(std.clean_uni_string).apply(std.uni_token_key)),
                           dim_university['university_id']))
    
    # Fallback lookup directly on university_name if token_key differs
    uni_name_lookup = dict(zip(zip(dim_university['country_id'], dim_university['university_name'].apply(std.clean_uni_string)),
                                dim_university['university_id']))
    
    def get_uni_id(row):
        cid = row['country_id']
        tkey = row['token_key']
        cname = row['clean_name']
        if (cid, tkey) in uni_lookup:
            return uni_lookup[(cid, tkey)]
        if (cid, cname) in uni_name_lookup:
            return uni_name_lookup[(cid, cname)]
        return np.nan
        
    c_qs['university_id'] = c_qs.apply(get_uni_id, axis=1)
    c_the['university_id'] = c_the.apply(get_uni_id, axis=1)
    c_wur['university_id'] = c_wur.apply(get_uni_id, axis=1)
    
    # 1. Build fact_university_performance
    perf_cols = ['university_id', 'year', 'global_rank', 'overall_score', 'academic_reputation', 'employer_reputation']
    f_perf = pd.concat([
        c_qs[perf_cols],
        c_the[perf_cols],
        c_wur[perf_cols]
    ], ignore_index=True).dropna(subset=['university_id'])
    
    # 2. Build fact_research
    # research_impact = citation_score, research_productivity = calculated composite
    def calc_res_prod(row):
        r_score = row['research_score']
        c_score = row['citation_score']
        if pd.notnull(r_score) and pd.notnull(c_score):
            return round(0.5 * r_score + 0.5 * c_score, 2)
        elif pd.notnull(c_score):
            return round(c_score, 2)
        elif pd.notnull(r_score):
            return round(r_score, 2)
        return np.nan

    f_res_list = []
    for df in [c_qs, c_the, c_wur]:
        df_r = df[['university_id', 'year', 'research_score', 'citation_score']].copy()
        df_r['research_impact'] = df_r['citation_score']
        df_r['research_productivity'] = df_r.apply(calc_res_prod, axis=1)
        f_res_list.append(df_r)
    f_research = pd.concat(f_res_list, ignore_index=True).dropna(subset=['university_id'])
    
    # 3. Build fact_student
    stud_cols = ['university_id', 'year', 'total_students', 'students_per_staff', 'international_students', 'intl_student_pct']
    f_stud = pd.concat([
        c_qs[stud_cols].rename(columns={'intl_student_pct': 'international_student_percentage'}),
        c_the[stud_cols].rename(columns={'intl_student_pct': 'international_student_percentage'}),
        c_wur[stud_cols].rename(columns={'intl_student_pct': 'international_student_percentage'})
    ], ignore_index=True).dropna(subset=['university_id'])
    
    # 4. Build fact_country_education from EdStats
    ed_dir = os.path.join(RAW_DIR, "world_bank_edstats")
    df_ed_data = pd.read_csv(os.path.join(ed_dir, "EdStatsData.csv"), low_memory=False)
    df_ed_data.columns = [c.replace('﻿', '').replace('"', '').strip() for c in df_ed_data.columns]
    
    # Key indicators to select for country analytics
    target_indicators = {
        'SE.TER.ENRR': 'Gross enrolment ratio, tertiary (%)',
        'SE.XPD.TOTL.GD.ZS': 'Government expenditure on education (% of GDP)',
        'SE.XPD.TERT.ZS': 'Expenditure on tertiary education (% of ed spend)',
        'SE.TER.ENRL.FE.ZS': 'Tertiary students female (%)',
        'SE.ADT.LITR.ZS': 'Adult literacy rate (%)',
        'SE.PRM.ENRL.TC.ZS': 'Pupil-teacher ratio, primary',
        'SE.SEC.ENRL.TC.ZS': 'Pupil-teacher ratio, secondary',
        'SE.SCH.LIFE': 'School life expectancy (years)',
        'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        'SP.POP.TOTL': 'Total population'
    }
    
    ed_filtered = df_ed_data[df_ed_data['Indicator Code'].isin(target_indicators.keys())].copy()
    ed_filtered['country_name'] = ed_filtered['Country Name'].apply(std.clean_country_name)
    ed_filtered['country_id'] = ed_filtered['country_name'].map(country_lookup)
    ed_filtered = ed_filtered.dropna(subset=['country_id'])
    
    year_cols = [c for c in ed_filtered.columns if c.isdigit()]
    
    # Melt year columns to long format
    f_country_ed = pd.melt(
        ed_filtered,
        id_vars=['country_id', 'Indicator Code', 'Indicator Name'],
        value_vars=year_cols,
        var_name='year',
        value_name='value'
    )
    f_country_ed['year'] = f_country_ed['year'].astype(int)
    f_country_ed['value'] = pd.to_numeric(f_country_ed['value'], errors='coerce')
    f_country_ed = f_country_ed.dropna(subset=['value'])
    f_country_ed['indicator_short'] = f_country_ed['Indicator Code'].map(target_indicators)
    f_country_ed = f_country_ed.rename(columns={'Indicator Code': 'indicator_code', 'Indicator Name': 'indicator_name'})
    
    # 5. Build Master KPI Table (eduvision_final_dataset)
    # Join dim_university, fact_university_performance, fact_research, fact_student
    m_df = dim_university.merge(f_perf, on='university_id', how='inner')
    m_df = m_df.merge(f_research, on=['university_id', 'year'], how='left')
    m_df = m_df.merge(f_stud, on=['university_id', 'year'], how='left')
    
    # Calculate 6 KPIs
    m_df['kpi1_global_ranking_score'] = m_df['overall_score']
    # If overall score is NaN, compute derived score from rank: max(10, 100 - (rank - 1) * 0.05)
    m_df['kpi1_global_ranking_score'] = np.where(
        m_df['kpi1_global_ranking_score'].isnull() & m_df['global_rank'].notnull(),
        np.maximum(10.0, (100.0 - (m_df['global_rank'] - 1) * 0.05)).round(1),
        m_df['kpi1_global_ranking_score']
    )
    
    m_df['kpi2_research_impact_score'] = m_df['citation_score']
    m_df['kpi3_faculty_student_ratio'] = m_df['students_per_staff']
    m_df['kpi4_international_student_pct'] = m_df['international_student_percentage']
    m_df['kpi5_academic_reputation_score'] = m_df['academic_reputation']
    m_df['kpi6_research_productivity_index'] = m_df['research_productivity']
    
    # Save cleaned tables
    f_perf.to_csv(os.path.join(CLEANED_DIR, "fact_university_performance.csv"), index=False)
    f_research.to_csv(os.path.join(CLEANED_DIR, "fact_research.csv"), index=False)
    f_stud.to_csv(os.path.join(CLEANED_DIR, "fact_student.csv"), index=False)
    f_country_ed.to_csv(os.path.join(CLEANED_DIR, "fact_country_education.csv"), index=False)
    
    f_perf.to_excel(os.path.join(CLEANED_DIR, "fact_university_performance.xlsx"), index=False)
    f_research.to_excel(os.path.join(CLEANED_DIR, "fact_research.xlsx"), index=False)
    f_stud.to_excel(os.path.join(CLEANED_DIR, "fact_student.xlsx"), index=False)
    f_country_ed.to_excel(os.path.join(CLEANED_DIR, "fact_country_education.xlsx"), index=False)
    
    # Save final tables
    m_df.to_csv(os.path.join(FINAL_DIR, "eduvision_final_dataset.csv"), index=False)
    m_df.to_excel(os.path.join(FINAL_DIR, "eduvision_final_dataset.xlsx"), index=False)
    
    kpi_summary = m_df[['university_id', 'university_name', 'country_name', 'region', 'year',
                        'kpi1_global_ranking_score', 'kpi2_research_impact_score',
                        'kpi3_faculty_student_ratio', 'kpi4_international_student_pct',
                        'kpi5_academic_reputation_score', 'kpi6_research_productivity_index']]
    
    kpi_summary.to_csv(os.path.join(FINAL_DIR, "kpi_summary.csv"), index=False)
    kpi_summary.to_excel(os.path.join(FINAL_DIR, "kpi_summary.xlsx"), index=False)
    
    print(f"Master final dataset saved: {len(m_df)} rows")
    print("KPI summary saved successfully!")
    return m_df, f_perf, f_research, f_stud, f_country_ed

if __name__ == "__main__":
    run_kpi_engineering()
