import os
import pandas as pd
import numpy as np
import json

BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
FINAL_DIR = os.path.join(BASE_DIR, "data", "final")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
DASHBOARD_DATA_DIR = os.path.join(BASE_DIR, "dashboard", "data")
os.makedirs(DASHBOARD_DATA_DIR, exist_ok=True)

# Load cleaned/final tables
dim_country = pd.read_csv(os.path.join(CLEANED_DIR, "dim_country.csv"))
dim_university = pd.read_csv(os.path.join(CLEANED_DIR, "dim_university.csv"))
m_df = pd.read_csv(os.path.join(FINAL_DIR, "eduvision_final_dataset.csv"))
f_country_ed = pd.read_csv(os.path.join(CLEANED_DIR, "fact_country_education.csv"))

def clean_df(df):
    df = df.replace({np.nan: None})
    records = df.to_dict(orient='records')
    # double check any float nan remaining
    for r in records:
        for k, v in r.items():
            if isinstance(v, float) and np.isnan(v):
                r[k] = None
    return records

data_bundle = {
    'dim_country': clean_df(dim_country),
    'dim_university': clean_df(dim_university[['university_id', 'university_name', 'country_id', 'country_name', 'region']]),
    'university_performance': clean_df(m_df[[
        'university_id', 'university_name', 'country_id', 'country_name', 'region', 'year',
        'global_rank', 'overall_score', 'academic_reputation', 'employer_reputation',
        'citation_score', 'research_score', 'research_productivity',
        'total_students', 'students_per_staff', 'international_students', 'international_student_percentage',
        'kpi1_global_ranking_score', 'kpi2_research_impact_score', 'kpi3_faculty_student_ratio',
        'kpi4_international_student_pct', 'kpi5_academic_reputation_score', 'kpi6_research_productivity_index'
    ]]),
    'country_education': clean_df(f_country_ed)
}

json_path = os.path.join(DASHBOARD_DATA_DIR, "dashboard_data.json")

# Serialize with standard json dumps (ensure_ascii=False)
json_str = json.dumps(data_bundle, allow_nan=False)

with open(json_path, "w", encoding="utf-8") as f:
    f.write(json_str)

print(f"Exported valid JSON: {os.path.getsize(json_path):,} bytes to {json_path}")
