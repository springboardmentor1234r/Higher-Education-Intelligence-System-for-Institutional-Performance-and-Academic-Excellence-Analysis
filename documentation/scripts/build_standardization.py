import os
import re
import pandas as pd
import numpy as np

cleaned_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\cleaned"
final_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\data\final"
reports_dir = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\reports"

os.makedirs(final_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# Load cleaned datasets
df_qs = pd.read_csv(os.path.join(cleaned_dir, "qs_2025_cleaned.csv"), low_memory=False)
df_wur = pd.read_csv(os.path.join(cleaned_dir, "wur_2023_cleaned.csv"), low_memory=False)
df_wb_cntry = pd.read_csv(os.path.join(cleaned_dir, "world_bank_country_cleaned.csv"), low_memory=False)

# Collect all country values
qs_countries = df_qs['country'].dropna().unique()
wur_countries = df_wur['country'].dropna().unique()

print(f"QS Unique Countries: {len(qs_countries)}")
print(f"WUR Unique Countries: {len(wur_countries)}")

# Build Canonical Country Mapping Dictionary
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

# Process all unique country names from raw datasets
all_raw_countries = sorted(list(set(qs_countries).union(set(wur_countries))))

country_rows = []
country_id_counter = 1
assigned_country_ids = {}

# Map World Bank Country Meta for regions
wb_country_region = {}
if 'country_code' in df_wb_cntry.columns and 'region' in df_wb_cntry.columns:
    for _, r in df_wb_cntry.iterrows():
        wb_country_region[r['country_code']] = r['region']

for c_raw in all_raw_countries:
    c_clean = str(c_raw).strip()
    if c_clean in country_canonical_map:
        c_name, c_iso, c_region = country_canonical_map[c_clean]
    else:
        c_name = c_clean
        # Generate 3-letter code if unknown
        c_iso = c_clean[:3].upper()
        c_region = "Other / Unclassified"
        
    if c_name not in assigned_country_ids:
        cid = f"C{country_id_counter:03d}"
        country_id_counter += 1
        assigned_country_ids[c_name] = (cid, c_iso, c_region)
    else:
        cid, c_iso, c_region = assigned_country_ids[c_name]
        
    country_rows.append({
        "raw_country_name": c_raw,
        "canonical_country_name": c_name,
        "country_id": cid,
        "iso_code": c_iso,
        "region": c_region
    })

# Create dim_country.csv
dim_country_df = pd.DataFrame([
    {"country_id": cid, "country_name": cname, "region": cregion, "iso_code": ciso}
    for cname, (cid, ciso, cregion) in assigned_country_ids.items()
]).sort_values("country_id").reset_index(drop=True)

dim_country_df[['country_id', 'country_name', 'region']].to_csv(
    os.path.join(final_dir, "dim_country.csv"), index=False, encoding="utf-8"
)
print(f"Created dim_country.csv with {len(dim_country_df)} countries.")

# Save country standardization report
country_report_df = pd.DataFrame(country_rows)
country_report_df.to_csv(os.path.join(reports_dir, "country_standardization_report.csv"), index=False, encoding="utf-8")
print(f"Saved country_standardization_report.csv with {len(country_report_df)} mapped entries.")

