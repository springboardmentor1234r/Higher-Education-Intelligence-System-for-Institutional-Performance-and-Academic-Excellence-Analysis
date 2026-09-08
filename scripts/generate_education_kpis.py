"""
generate_education_kpis.py
EduVision_DV - Higher Education Performance Dashboard
Milestone 2 / Module 3: Education KPI Engineering
"""

import pandas as pd
import numpy as np
import os

def min_max_norm(s: pd.Series) -> pd.Series:
    v = s.dropna()
    if v.empty or v.max() == v.min():
        return s
    return ((s - v.min()) / (v.max() - v.min())) * 100

def generate_kpis(cleaned_csv_path: str, output_excel_path: str):
    print('Loading cleaned dataset...')
    df = pd.read_csv(cleaned_csv_path)

    # 1. Master IDs
    if 'university_id' not in df.columns:
        df['university_id'] = [f'U{i+1:04d}' for i in range(len(df))]
    if 'country_id' not in df.columns:
        df['country_id'] = df['Country'].astype(str).str.strip().str[:2].str.upper()

    # 2. KPI 1: Global Ranking Score
    if 'QS_Overall_Score' in df.columns:
        df['kpi1_global_ranking_score'] = pd.to_numeric(df['QS_Overall_Score'], errors='coerce')
        if 'THE_Overall_Score_Numeric' in df.columns:
            df['kpi1_global_ranking_score'] = df['kpi1_global_ranking_score'].fillna(df['THE_Overall_Score_Numeric'])

    # 3. KPI 2: Research Impact Score
    if 'QS_Citations_Per_Faculty' in df.columns:
        df['kpi2_research_impact_score'] = pd.to_numeric(df['QS_Citations_Per_Faculty'], errors='coerce')
        if 'THE_Citations' in df.columns:
            df['kpi2_research_impact_score'] = df['kpi2_research_impact_score'].fillna(df['THE_Citations'])

    # 4. KPI 3: Faculty-to-Student Ratio
    if 'THE_Student_Staff_Ratio' in df.columns:
        s = pd.to_numeric(df['THE_Student_Staff_Ratio'], errors='coerce')
        df['kpi3_students_per_staff_num'] = s
        df['kpi3_faculty_to_student_ratio'] = s.apply(lambda x: f'1:{x:.1f}' if pd.notnull(x) else np.nan)

    # 5. KPI 4: International Student %
    if 'THE_International_Students' in df.columns:
        df['kpi4_international_student_pct'] = pd.to_numeric(df['THE_International_Students'], errors='coerce')

    # 6. KPI 5: Academic Reputation Score
    if 'QS_Academic_Reputation' in df.columns:
        df['kpi5_academic_reputation_score'] = pd.to_numeric(df['QS_Academic_Reputation'], errors='coerce')

    # 7. KPI 6: Research Productivity Index
    r_n = min_max_norm(pd.to_numeric(df.get('THE_Research', 0), errors='coerce'))
    c_n = min_max_norm(pd.to_numeric(df.get('kpi2_research_impact_score', 0), errors='coerce'))
    o_n = min_max_norm(pd.to_numeric(df.get('THE_International_Outlook', 0), errors='coerce'))

    df['kpi6_research_productivity_index'] = (
        0.50 * r_n.fillna(r_n.median()) + 
        0.30 * c_n.fillna(c_n.median()) + 
        0.20 * o_n.fillna(o_n.median())
    ).round(2)

    os.makedirs(os.path.dirname(output_excel_path) or '.', exist_ok=True)
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='final_kpi_dataset', index=False)
        dim_uni = df[['university_id', 'University', 'country_id', 'Country']].drop_duplicates()
        dim_uni.to_excel(writer, sheet_name='dim_university', index=False)
        dim_country = df[['country_id', 'Country']].drop_duplicates()
        dim_country.to_excel(writer, sheet_name='dim_country', index=False)

    print('Finished exporting university_final_dataset.xlsx!')

if __name__ == '__main__':
    generate_kpis('data/processed/university_cleaned.csv', 'data/processed/university_final_dataset.xlsx')
