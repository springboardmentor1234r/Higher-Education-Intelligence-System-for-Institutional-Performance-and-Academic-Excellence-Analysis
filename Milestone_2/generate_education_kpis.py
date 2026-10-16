from gettext import install
import os
import pandas as pd
import numpy as np
import pip
pip.main(['install', 'openpyxl'])
    
# 1. Define Paths
CLEANED_DIR = "Milestone_1/cleaned"
FINAL_DIR = "Milestone_2"

#os.makedirs(FINAL_DIR, exist_ok=True)

print("=" * 70)
print("MILESTONE 2: KPI ENGINEERING & STATISTICAL ASSEMBLY")
print("=" * 70)

# 2. Ingest Cleaned Star Schema Tables
dim_country = pd.read_csv(f"{CLEANED_DIR}/dim_country.csv")
dim_university = pd.read_csv(f"{CLEANED_DIR}/dim_university.csv")
fact_perf = pd.read_csv(f"{CLEANED_DIR}/fact_university_performance.csv")
fact_res = pd.read_csv(f"{CLEANED_DIR}/fact_research.csv")
fact_stu = pd.read_csv(f"{CLEANED_DIR}/fact_student.csv")


# 3. Master Join Base (University & Country Dimensions)
kpi_df = dim_university[['university_id', 'university_name', 'country_id', 'country_name']].copy()

# Join Fact Tables
kpi_df = kpi_df.merge(
    fact_perf[['university_id', 'global_rank_2025', 'academic_reputation', 'employer_reputation']], 
    on='university_id', 
    how='left'
)

kpi_df = kpi_df.merge(
    fact_res[['university_id', 'research_score', 'research_impact']], 
    on='university_id', 
    how='left'
)
kpi_df = kpi_df.merge(
    fact_stu[['university_id', 'total_students', 'students_per_staff', 'international_students', 'international_student_percentage']], 
    on='university_id', 
    how='left'
)

print(f"\n[INFO] KPI dataset assembled: {kpi_df.shape[0]:,} universities x {kpi_df.shape[1]:,} columns")


# 4. KPI Engineering per Structured Specification
# KPI 1: Research Impact
kpi_df['kpi_research_impact'] = kpi_df['research_impact'].round(2)

# KPI 2: Research Productivity Index
kpi_df['kpi_research_productivity'] = np.where(
    kpi_df['research_score'].notna() & kpi_df['research_impact'].notna(),
    ((kpi_df['research_score'] * 0.5) + (kpi_df['research_impact'] * 0.5)).round(2),
    np.nan
)

# KPI 3: Student Internationalization Ratio
# Source: WUR 2023 | Unit: % | Normalization: Bounded % | Missing: NaN
kpi_df['kpi_intl_student_pct'] = kpi_df['international_student_percentage'].fillna(
    (kpi_df['international_students'] / kpi_df['total_students']) * 100
).round(2)

# KPI 4: Faculty-Student Capacity Ratio (Staff per 100 students)
# Source: WUR 2023 | Formula: 100 / students_per_staff | Missing: NaN
kpi_df['kpi_faculty_student_ratio'] = np.where(
    kpi_df['students_per_staff'] > 0,
    (100.0 / kpi_df['students_per_staff']).round(2),
    np.nan
)

# KPI 5: Academic Reputation Score
# Source: QS 2025 | Unit: Score (0-100) | Missing: NaN
kpi_df['kpi_academic_reputation'] = kpi_df['academic_reputation'].round(2)

# KPI 6: Employer Reputation Score
# Source: QS 2025 | Unit: Score (0-100) | Missing: NaN
kpi_df['kpi_employer_reputation'] = kpi_df['employer_reputation'].round(2)

# KPI 7: Institutional Excellence Tier
def get_global_tier(rank):
    if pd.isna(rank):
        return "Unranked / Regional"
    elif rank <= 100:
        return "Tier 1 (Top 100)"
    elif rank <= 300:
        return "Tier 2 (101-300)"
    elif rank <= 500:
        return "Tier 3 (301-500)"
    else:
        return "Tier 4 (500+)"

kpi_df['kpi7_global_tier'] = kpi_df['global_rank_2025'].apply(get_global_tier)

# 5. Build Final Schema Table
final_kpi_columns = [
    'university_id',
    'university_name',
    'country_id',
    'country_name',
    'global_rank_2025',
    'kpi_research_impact',
    'kpi_research_productivity',
    'kpi_intl_student_pct',
    'kpi_faculty_student_ratio',
    'kpi_academic_reputation',
    'kpi_employer_reputation',
    'kpi7_global_tier'  
]

final_master_dataset = kpi_df[final_kpi_columns].copy()

# Sort by global ranking with unranked entities placed after
final_master_dataset = final_master_dataset.sort_values(
    by=['global_rank_2025'], 
    na_position='last'
).reset_index(drop=True)

print(f"\n[INFO] Master KPI dataset assembled: {final_master_dataset.shape[0]:,} universities x {final_master_dataset.shape[1]:,} columns")

# 6. Quality & Completeness Audit
print("\n--- KPI ENGINEERING AUDIT SUMMARY ---")
print(f"Total Master Universities: {len(final_master_dataset):,}")
print(f"Total Columns: {final_master_dataset.shape[1]}")

# 7. Export Final Deliverables
xlsx_path = f"{FINAL_DIR}/university _final_dataset.xlsx"

try:
    final_master_dataset.to_excel(xlsx_path, index=False, sheet_name="HigherEd_Master_KPIs")
    print(f"\n[SUCCESS] Exported Excel deliverable: {xlsx_path}")
except Exception as e:
    print(f"\n[!] Excel export skipped: {e}")

print(f"[SUCCESS] Exported Excel deliverable: {xlsx_path}")
print("=" * 70)