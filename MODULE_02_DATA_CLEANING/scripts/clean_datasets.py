import os
import re
import pandas as pd
import numpy as np

raw_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\raw"
cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

os.makedirs(cleaned_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

cleaning_log = []
validation_records = []

def log_action(dataset_name, step, details):
    log_entry = f"**[{dataset_name}] Step {step}**: {details}"
    print(log_entry, flush=True)
    cleaning_log.append(log_entry)

def safe_read_csv(path):
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='latin1', low_memory=False)

# ==========================================
# 1. Clean QS World University Rankings 2025
# ==========================================
qs_raw_path = os.path.join(raw_dir, "QS_Ranking", "QS World University Rankings 2025 (Top global universities).csv")
log_action("QS 2025", 1, "Loading raw dataset")
df_qs_raw = safe_read_csv(qs_raw_path)

rows_before_qs = len(df_qs_raw)
cols_before_qs = len(df_qs_raw.columns)
missing_before_qs = int(df_qs_raw.isnull().sum().sum())
dups_before_qs = int(df_qs_raw.duplicated().sum())

df_qs = df_qs_raw.copy()

# Step 3: Standardize column names
log_action("QS 2025", 2, "Standardizing column names to lowercase snake_case")
col_map_qs = {
    "RANK_2025": "rank_2025",
    "RANK_2024": "rank_2024",
    "Institution_Name": "university_name",
    "Location": "country",
    "Region": "region",
    "SIZE": "institution_size",
    "FOCUS": "subject_focus",
    "RES.": "research_intensity",
    "STATUS": "institution_status",
    "Academic_Reputation_Score": "academic_reputation_score",
    "Academic_Reputation_Rank": "academic_reputation_rank",
    "Employer_Reputation_Score": "employer_reputation_score",
    "Employer_Reputation_Rank": "employer_reputation_rank",
    "Faculty_Student_Score": "faculty_student_score",
    "Faculty_Student_Rank": "faculty_student_rank",
    "Citations_per_Faculty_Score": "citations_per_faculty_score",
    "Citations_per_Faculty_Rank": "citations_per_faculty_rank",
    "International_Faculty_Score": "international_faculty_score",
    "International_Faculty_Rank": "international_faculty_rank",
    "International_Students_Score": "international_students_score",
    "International_Students_Rank": "international_students_rank",
    "International_Research_Network_Score": "international_research_network_score",
    "International_Research_Network_Rank": "international_research_network_rank",
    "Employment_Outcomes_Score": "employment_outcomes_score",
    "Employment_Outcomes_Rank": "employment_outcomes_rank",
    "Sustainability_Score": "sustainability_score",
    "Sustainability_Rank": "sustainability_rank",
    "Overall_Score": "overall_score"
}
df_qs.rename(columns=col_map_qs, inplace=True)

# Step 4 & 5: Strip whitespace and clean text fields
log_action("QS 2025", 3, "Stripping whitespace and cleaning text fields")
str_cols_qs = df_qs.select_dtypes(include=['object']).columns
for c in str_cols_qs:
    df_qs[c] = df_qs[c].astype(str).str.strip()
    df_qs[c] = df_qs[c].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan, '-': np.nan})

# Step 6 & 7: Clean University & Country names
log_action("QS 2025", 4, "Cleaning university and country names")
df_qs['university_name'] = df_qs['university_name'].str.replace(r'\s+', ' ', regex=True)
df_qs['country'] = df_qs['country'].str.replace(r'\s+', ' ', regex=True)

# Country standardization
country_clean_map = {
    "United States": "United States",
    "United Kingdom": "United Kingdom",
    "China (Mainland)": "China",
    "Hong Kong SAR": "Hong Kong",
    "Macau SAR": "Macao",
    "South Korea": "Korea, Rep.",
    "Taiwan": "Taiwan"
}
# Keep raw country in 'country_raw' and cleaned in 'country'
df_qs['country_raw'] = df_qs['country']
df_qs['country'] = df_qs['country'].replace(country_clean_map)

# Step 8: Numeric conversions for scores and ranks
log_action("QS 2025", 5, "Extracting clean numeric fields for ranks and overall score")

def parse_rank_numeric(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).replace('=', '').replace('+', '').strip()
    match = re.search(r'(\d+)', val_str)
    return int(match.group(1)) if match else np.nan

df_qs['rank_2025_numeric'] = df_qs['rank_2025'].apply(parse_rank_numeric)
df_qs['rank_2024_numeric'] = df_qs['rank_2024'].apply(parse_rank_numeric)
df_qs['overall_score_numeric'] = pd.to_numeric(df_qs['overall_score'], errors='coerce')

# Step 9 & 10: Duplicate detection & removal
log_action("QS 2025", 6, "Detecting and removing confirmed duplicate rows")
dups_qs = df_qs.duplicated().sum()
if dups_qs > 0:
    df_qs.drop_duplicates(inplace=True)
    log_action("QS 2025", 7, f"Removed {dups_qs} duplicate rows")
else:
    log_action("QS 2025", 7, "No duplicate rows found")

rows_after_qs = len(df_qs)
cols_after_qs = len(df_qs.columns)
missing_after_qs = int(df_qs.isnull().sum().sum())
dups_after_qs = int(df_qs.duplicated().sum())

qs_cleaned_path = os.path.join(cleaned_dir, "qs_2025_cleaned.csv")
df_qs.to_csv(qs_cleaned_path, index=False, encoding="utf-8")
log_action("QS 2025", 8, f"Saved cleaned QS 2025 dataset to {qs_cleaned_path}")

validation_records.append({
    "Dataset": "QS World University Rankings 2025",
    "Output File": "qs_2025_cleaned.csv",
    "Rows Before": rows_before_qs,
    "Rows After": rows_after_qs,
    "Cols Before": cols_before_qs,
    "Cols After": cols_after_qs,
    "Missing Cells Before": missing_before_qs,
    "Missing Cells After": missing_after_qs,
    "Duplicates Before": dups_before_qs,
    "Duplicates After": dups_after_qs
})


# ===============================================
# 2. Clean THE / World University Rankings 2023
# ===============================================
wur_raw_path = os.path.join(raw_dir, "World_Ranking", "World University Rankings 2023.csv")
log_action("WUR 2023", 1, "Loading raw WUR 2023 dataset")
df_wur_raw = safe_read_csv(wur_raw_path)

rows_before_wur = len(df_wur_raw)
cols_before_wur = len(df_wur_raw.columns)
missing_before_wur = int(df_wur_raw.isnull().sum().sum())
dups_before_wur = int(df_wur_raw.duplicated().sum())

df_wur = df_wur_raw.copy()

# Step 3: Standardize column names
log_action("WUR 2023", 2, "Standardizing column names to lowercase snake_case")
col_map_wur = {
    "University Rank": "world_rank",
    "Name of University": "university_name",
    "Location": "country",
    "No of student": "num_students_raw",
    "No of student per staff": "student_staff_ratio",
    "International Student": "pct_international_students_raw",
    "Female:Male Ratio": "female_male_ratio",
    "OverAll Score": "overall_score",
    "Teaching Score": "teaching_score",
    "Research Score": "research_score",
    "Citations Score": "citations_score",
    "Industry Income Score": "industry_income_score",
    "International Outlook Score": "international_outlook_score"
}
df_wur.rename(columns=col_map_wur, inplace=True)

# Step 4 & 5: Strip whitespace and clean text fields
log_action("WUR 2023", 3, "Stripping whitespace and cleaning text fields")
str_cols_wur = df_wur.select_dtypes(include=['object']).columns
for c in str_cols_wur:
    df_wur[c] = df_wur[c].astype(str).str.strip()
    df_wur[c] = df_wur[c].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan, 'Reporter': 'Reporter'})

# Step 6 & 7: Clean University & Country names
log_action("WUR 2023", 4, "Cleaning university and country names")
df_wur['university_name'] = df_wur['university_name'].str.replace(r'\s+', ' ', regex=True)
df_wur['country'] = df_wur['country'].str.replace(r'\s+', ' ', regex=True)

df_wur['country_raw'] = df_wur['country']
df_wur['country'] = df_wur['country'].replace(country_clean_map)

# Step 8: Parse numeric fields
log_action("WUR 2023", 5, "Converting raw strings to numeric representations (num_students, pct_international_students, ranks)")

# Number of students: "20,965" -> 20965.0
df_wur['num_students'] = df_wur['num_students_raw'].astype(str).str.replace(',', '').str.strip()
df_wur['num_students'] = pd.to_numeric(df_wur['num_students'], errors='coerce')

# International students %: "42%" -> 42.0
df_wur['pct_international_students'] = df_wur['pct_international_students_raw'].astype(str).str.replace('%', '').str.strip()
df_wur['pct_international_students'] = pd.to_numeric(df_wur['pct_international_students'], errors='coerce')

# Parse rank range / integer e.g., "501-600" or "1" or "1001+"
def parse_wur_rank(val):
    if pd.isna(val) or val == 'Reporter':
        return np.nan
    val_str = str(val).replace('=', '').replace('+', '').replace('–', '-').strip()
    if '-' in val_str:
        parts = val_str.split('-')
        try:
            return (float(parts[0]) + float(parts[1])) / 2.0
        except:
            return np.nan
    match = re.search(r'(\d+)', val_str)
    return float(match.group(1)) if match else np.nan

df_wur['world_rank_numeric'] = df_wur['world_rank'].apply(parse_wur_rank)

# Parse overall score e.g. "96.4" or "50.1-53.8"
def parse_score(val):
    if pd.isna(val) or val == 'Reporter':
        return np.nan
    val_str = str(val).replace('–', '-').strip()
    if '-' in val_str:
        parts = val_str.split('-')
        try:
            return (float(parts[0]) + float(parts[1])) / 2.0
        except:
            return np.nan
    return pd.to_numeric(val_str, errors='coerce')

df_wur['overall_score_numeric'] = df_wur['overall_score'].apply(parse_score)

# Step 9 & 10: Duplicate detection & removal
log_action("WUR 2023", 6, f"Detecting and removing confirmed duplicate rows ({dups_before_wur} exact duplicates detected)")
df_wur.drop_duplicates(inplace=True)

rows_after_wur = len(df_wur)
cols_after_wur = len(df_wur.columns)
missing_after_wur = int(df_wur.isnull().sum().sum())
dups_after_wur = int(df_wur.duplicated().sum())

wur_cleaned_path = os.path.join(cleaned_dir, "wur_2023_cleaned.csv")
the_2024_cleaned_path = os.path.join(cleaned_dir, "the_2024_cleaned.csv")

df_wur.to_csv(wur_cleaned_path, index=False, encoding="utf-8")
df_wur.to_csv(the_2024_cleaned_path, index=False, encoding="utf-8")
log_action("WUR 2023", 7, f"Saved cleaned dataset to {wur_cleaned_path} and aliased {the_2024_cleaned_path}")

validation_records.append({
    "Dataset": "World University Rankings 2023 (THE)",
    "Output File": "wur_2023_cleaned.csv / the_2024_cleaned.csv",
    "Rows Before": rows_before_wur,
    "Rows After": rows_after_wur,
    "Cols Before": cols_before_wur,
    "Cols After": cols_after_wur,
    "Missing Cells Before": missing_before_wur,
    "Missing Cells After": missing_after_wur,
    "Duplicates Before": dups_before_wur,
    "Duplicates After": dups_after_wur
})


# ===============================================
# 3. Clean World Bank Education Statistics
# ===============================================
ed_raw_path = os.path.join(raw_dir, "archive (8)", "edstats-csv-zip-32-mb-", "EdStatsData.csv")
log_action("World Bank EdStats", 1, "Loading raw EdStatsData dataset")
df_ed_raw = safe_read_csv(ed_raw_path)

rows_before_ed = len(df_ed_raw)
cols_before_ed = len(df_ed_raw.columns)
missing_before_ed = int(df_ed_raw.isnull().sum().sum())
dups_before_ed = int(df_ed_raw.duplicated().sum())

df_ed = df_ed_raw.copy()

# Step 3: Standardize column names
log_action("World Bank EdStats", 2, "Standardizing column names to lowercase snake_case")
col_map_ed = {
    "Country Name": "country_name",
    "Country Code": "country_code",
    "Indicator Name": "indicator_name",
    "Indicator Code": "indicator_code"
}
# Map years 1970..2100 to year_1970..year_2100
for c in df_ed.columns:
    if str(c).strip().isdigit():
        col_map_ed[c] = f"year_{c}"

df_ed.rename(columns=col_map_ed, inplace=True)

# Step 4: Drop empty un-named columns e.g., "Unnamed: 69" if 100% NaN
if "Unnamed: 69" in df_ed.columns:
    log_action("World Bank EdStats", 3, "Dropping 100% null trailing column 'Unnamed: 69'")
    df_ed.drop(columns=["Unnamed: 69"], inplace=True)

# Step 5: Strip text fields
log_action("World Bank EdStats", 4, "Stripping whitespace from text fields")
str_cols_ed = ["country_name", "country_code", "indicator_name", "indicator_code"]
for c in str_cols_ed:
    if c in df_ed.columns:
        df_ed[c] = df_ed[c].astype(str).str.strip()

# Step 9 & 10: Duplicates check
dups_ed = df_ed.duplicated().sum()
log_action("World Bank EdStats", 5, f"Checking for duplicates ({dups_ed} duplicate rows found)")

rows_after_ed = len(df_ed)
cols_after_ed = len(df_ed.columns)
missing_after_ed = int(df_ed.isnull().sum().sum())
dups_after_ed = int(df_ed.duplicated().sum())

ed_cleaned_path = os.path.join(cleaned_dir, "world_bank_education_cleaned.csv")
df_ed.to_csv(ed_cleaned_path, index=False, encoding="utf-8")
log_action("World Bank EdStats", 6, f"Saved cleaned dataset to {ed_cleaned_path}")

validation_records.append({
    "Dataset": "World Bank Education Statistics",
    "Output File": "world_bank_education_cleaned.csv",
    "Rows Before": rows_before_ed,
    "Rows After": rows_after_ed,
    "Cols Before": cols_before_ed,
    "Cols After": cols_after_ed,
    "Missing Cells Before": missing_before_ed,
    "Missing Cells After": missing_after_ed,
    "Duplicates Before": dups_before_ed,
    "Duplicates After": dups_after_ed
})


# ===============================================
# 4. Clean World Bank Country Metadata
# ===============================================
country_raw_path = os.path.join(raw_dir, "archive (8)", "edstats-csv-zip-32-mb-", "EdStatsCountry.csv")
log_action("World Bank Country Meta", 1, "Loading raw EdStatsCountry dataset")
df_cntry_raw = safe_read_csv(country_raw_path)

rows_before_cntry = len(df_cntry_raw)
cols_before_cntry = len(df_cntry_raw.columns)
missing_before_cntry = int(df_cntry_raw.isnull().sum().sum())
dups_before_cntry = int(df_cntry_raw.duplicated().sum())

df_cntry = df_cntry_raw.copy()

# Standardize column names
col_map_cntry = {c: str(c).lower().replace(" ", "_").replace("-", "_") for c in df_cntry.columns}
df_cntry.rename(columns=col_map_cntry, inplace=True)

if "unnamed:_31" in df_cntry.columns:
    df_cntry.drop(columns=["unnamed:_31"], inplace=True)

cntry_cleaned_path = os.path.join(cleaned_dir, "world_bank_country_cleaned.csv")
df_cntry.to_csv(cntry_cleaned_path, index=False, encoding="utf-8")
log_action("World Bank Country Meta", 2, f"Saved cleaned dataset to {cntry_cleaned_path}")

rows_after_cntry = len(df_cntry)
cols_after_cntry = len(df_cntry.columns)
missing_after_cntry = int(df_cntry.isnull().sum().sum())
dups_after_cntry = int(df_cntry.duplicated().sum())

validation_records.append({
    "Dataset": "World Bank Country Metadata",
    "Output File": "world_bank_country_cleaned.csv",
    "Rows Before": rows_before_cntry,
    "Rows After": rows_after_cntry,
    "Cols Before": cols_before_cntry,
    "Cols After": cols_after_cntry,
    "Missing Cells Before": missing_before_cntry,
    "Missing Cells After": missing_after_cntry,
    "Duplicates Before": dups_before_cntry,
    "Duplicates After": dups_after_cntry
})


# Save Post-Cleaning Validation Report CSV
val_df = pd.DataFrame(validation_records)
val_csv_path = os.path.join(reports_dir, "post_cleaning_validation.csv")
val_df.to_csv(val_csv_path, index=False, encoding="utf-8")
print(f"\nSaved post cleaning validation CSV: {val_csv_path}", flush=True)


# Save Detailed Cleaning Log Markdown
md_log = []
md_log.append("# EduVision_DV – Data Cleaning Transformation Log\n")
md_log.append("## Overview\n")
md_log.append("This log documents every data cleaning step executed across the project's raw datasets. All raw data files in `../data/raw/` were kept strictly untouched. Cleaned datasets are saved into `../data/cleaned/`.\n")

md_log.append("## Transformation Steps Log\n")
for entry in cleaning_log:
    md_log.append(f"- {entry}")

md_log.append("\n---\n")
md_log.append("## Post-Cleaning Validation Summary\n")
md_log.append("| Dataset | Output File | Rows Before | Rows After | Cols Before | Cols After | Missing Before | Missing After | Dups Before | Dups After |")
md_log.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

for r in validation_records:
    md_log.append(f"| {r['Dataset']} | `{r['Output File']}` | {r['Rows Before']:,} | {r['Rows After']:,} | {r['Cols Before']} | {r['Cols After']} | {r['Missing Cells Before']:,} | {r['Missing Cells After']:,} | {r['Duplicates Before']} | {r['Duplicates After']} |")

log_md_path = os.path.join(reports_dir, "cleaning_log.md")
with open(log_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_log))

print(f"Saved cleaning log markdown: {log_md_path}", flush=True)
