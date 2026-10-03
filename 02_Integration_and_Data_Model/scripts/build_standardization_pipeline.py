import os
import re
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

os.makedirs(final_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# 1. Load Cleaned Data
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_wur = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)

df_qs = df_qs.dropna(subset=['university_name']).copy()
df_wur = df_wur.dropna(subset=['university_name']).copy()

# 2. Country Canonical Mapping
country_canonical_map = {
    "United States": ("United States", "USA", "North America"),
    "US": ("United States", "USA", "North America"),
    "USA": ("United States", "USA", "North America"),
    "United States of America": ("United States", "USA", "North America"),
    "United Kingdom": ("United Kingdom", "GBR", "Europe"),
    "UK": ("United Kingdom", "GBR", "Europe"),
    "China": ("China", "CHN", "Asia"),
    "China (Mainland)": ("China", "CHN", "Asia"),
    "Hong Kong": ("Hong Kong", "HKG", "Asia"),
    "Hong Kong SAR": ("Hong Kong", "HKG", "Asia"),
    "Macau": ("Macao", "MAC", "Asia"),
    "Macao": ("Macao", "MAC", "Asia"),
    "Macau SAR": ("Macao", "MAC", "Asia"),
    "South Korea": ("South Korea", "KOR", "Asia"),
    "Korea, Rep.": ("South Korea", "KOR", "Asia"),
    "Republic of Korea": ("South Korea", "KOR", "Asia"),
    "Taiwan": ("Taiwan", "TWN", "Asia"),
    "Taiwan, Province of China": ("Taiwan", "TWN", "Asia"),
    "Russia": ("Russian Federation", "RUS", "Europe"),
    "Russian Federation": ("Russian Federation", "RUS", "Europe"),
    "Iran": ("Iran", "IRN", "Middle East"),
    "Iran (Islamic Republic of)": ("Iran", "IRN", "Middle East"),
    "Iran, Islamic Rep.": ("Iran", "IRN", "Middle East"),
    "Viet Nam": ("Vietnam", "VNM", "Asia"),
    "Vietnam": ("Vietnam", "VNM", "Asia"),
    "Egypt": ("Egypt", "EGY", "Africa"),
    "Egypt, Arab Rep.": ("Egypt", "EGY", "Africa"),
    "Turkey": ("Türkiye", "TUR", "Europe"),
    "Türkiye": ("Türkiye", "TUR", "Europe"),
    "Czech Republic": ("Czechia", "CZE", "Europe"),
    "Czechia": ("Czechia", "CZE", "Europe"),
    "Slovakia": ("Slovak Republic", "SVK", "Europe"),
    "Slovak Republic": ("Slovak Republic", "SVK", "Europe")
}

qs_countries = df_qs['country'].dropna().unique()
wur_countries = df_wur['country'].dropna().unique()
all_raw_countries = sorted(list(set(qs_countries).union(set(wur_countries))))

country_report_rows = []
assigned_country_ids = {}
country_id_counter = 1

for c_raw in all_raw_countries:
    c_clean = str(c_raw).strip()
    if c_clean in country_canonical_map:
        c_name, c_iso, c_region = country_canonical_map[c_clean]
    else:
        c_name = c_clean
        c_iso = c_clean[:3].upper() if len(c_clean)>=3 else "OTH"
        c_region = "Other / Global"
        
    if c_name not in assigned_country_ids:
        cid = f"C{country_id_counter:03d}"
        country_id_counter += 1
        assigned_country_ids[c_name] = (cid, c_iso, c_region)
    else:
        cid, c_iso, c_region = assigned_country_ids[c_name]
        
    country_report_rows.append({
        "raw_country_name": c_raw,
        "canonical_country_name": c_name,
        "country_id": cid,
        "iso_code": c_iso,
        "region": c_region
    })

# Add C999 explicitly to assigned_country_ids for Unknown countries
assigned_country_ids["Unknown"] = ("C999", "UNK", "Other / Global")

# Save dim_country.csv
dim_country_df = pd.DataFrame([
    {"country_id": cid, "country_name": cname, "region": cregion}
    for cname, (cid, ciso, cregion) in assigned_country_ids.items()
]).sort_values("country_id").reset_index(drop=True)

dim_country_df.to_csv(os.path.join(final_dir, "dim_country.csv"), index=False, encoding="utf-8")
print(f"Saved dim_country.csv ({len(dim_country_df)} countries)")

# Save country_standardization_report.csv
country_report_df = pd.DataFrame(country_report_rows)
country_report_df.to_csv(os.path.join(reports_dir, "country_standardization_report.csv"), index=False, encoding="utf-8")

# 3. Deterministic University Name Cleaning Function
def clean_university_name_deterministic(name):
    if pd.isna(name):
        return ""
    text = str(name).lower()
    text = re.sub(r'\s*\([^)]*\)\s*$', '', text)
    if text.startswith("the "):
        text = text[4:]
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_canonical_country(c_raw):
    if pd.isna(c_raw):
        return ("Unknown", "C999", "Other / Global")
    c_clean = str(c_raw).strip()
    if c_clean in country_canonical_map:
        c_name = country_canonical_map[c_clean][0]
    else:
        c_name = c_clean
    if c_name in assigned_country_ids:
        cid, ciso, cregion = assigned_country_ids[c_name]
        return (c_name, cid, cregion)
    return ("Unknown", "C999", "Other / Global")

# Standardize QS & WUR Universities
qs_univ_list = []
for idx, row in df_qs.iterrows():
    u_raw = row['university_name']
    u_clean = clean_university_name_deterministic(u_raw)
    c_name, cid, cregion = get_canonical_country(row['country'])
    qs_univ_list.append({
        "dataset": "QS 2025",
        "raw_university_name": u_raw,
        "clean_university_name": u_clean,
        "raw_country": row['country'],
        "country_name": c_name,
        "country_id": cid,
        "region": cregion
    })

wur_univ_list = []
for idx, row in df_wur.iterrows():
    u_raw = row['university_name']
    u_clean = clean_university_name_deterministic(u_raw)
    c_name, cid, cregion = get_canonical_country(row['country'])
    wur_univ_list.append({
        "dataset": "THE / WUR 2023",
        "raw_university_name": u_raw,
        "clean_university_name": u_clean,
        "raw_country": row['country'],
        "country_name": c_name,
        "country_id": cid,
        "region": cregion
    })

df_qs_univ = pd.DataFrame(qs_univ_list)
df_wur_univ = pd.DataFrame(wur_univ_list)

univ_std_report = pd.concat([df_qs_univ, df_wur_univ], ignore_index=True)
univ_std_report.to_csv(os.path.join(reports_dir, "university_standardization_report.csv"), index=False, encoding="utf-8")
print(f"Saved university_standardization_report.csv ({len(univ_std_report)} total university rows)")

