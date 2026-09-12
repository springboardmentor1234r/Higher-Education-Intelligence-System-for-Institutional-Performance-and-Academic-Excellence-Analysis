"""
data_cleaning.py — REAL DATA EDITION
--------------------------------------
STAGE 2. Cleans each of the 7 real sources independently. These are public
datasets that have already been through some curation, but still carry the
normal messiness of any real multi-year, multi-publisher export:
  - percentage strings ("42%"), thousands separators ("20,152"), ratio
    strings ("48 : 52") stored as text instead of numbers
  - inconsistent country naming ("United States of America" vs "USA" vs
    "United States")
  - duplicate (university, year) rows within a source
  - wide-format supplementary tables (one column per year) that need
    reshaping before they're usable in a BI tool
"""
import os
import re
import pandas as pd
import numpy as np

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(OUT_DIR, exist_ok=True)
LOG = []


def log(stage, msg):
    LOG.append(f"[{stage}] {msg}")
    print(f"[{stage}] {msg}")


# ---- shared helpers -------------------------------------------------------
COUNTRY_ALIASES = {
    "United States of America": "United States", "USA": "United States", "US": "United States",
    "UK": "United Kingdom", "Britain": "United Kingdom",
    "Russian Federation": "Russia", "South Korea": "South Korea", "Korea, South": "South Korea",
    "Republic of Korea": "South Korea", "Hong Kong": "Hong Kong SAR", "China (Hong Kong)": "Hong Kong SAR",
    "Iran, Islamic Rep.": "Iran", "Egypt, Arab Rep.": "Egypt", "Czechia": "Czech Republic",
}


def std_country(name):
    if pd.isna(name):
        return None
    n = str(name).strip()
    return COUNTRY_ALIASES.get(n, n)


def std_name(name):
    if pd.isna(name):
        return None
    return " ".join(str(name).strip().split())


def pct_to_float(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip().replace("%", "")
    try:
        return float(s)
    except ValueError:
        return np.nan


def commas_to_int(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return np.nan


def ratio_first_half(s):
    """'48 : 52' -> 48.0 (female share) — also handles '25%' style already-numeric input."""
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if ":" in s:
        try:
            return float(s.split(":")[0].strip())
        except ValueError:
            return np.nan
    return pct_to_float(s)


# ---- per-source cleaners ---------------------------------------------------
def clean_times():
    df = pd.read_csv(os.path.join(RAW_DIR, "timesData.csv"))
    before = len(df)
    df["university_name"] = df["university_name"].apply(std_name)
    df["country"] = df["country"].apply(std_country)
    df["num_students"] = df["num_students"].apply(commas_to_int)
    df["international_students"] = df["international_students"].apply(pct_to_float)
    df["international"] = pd.to_numeric(df["international"], errors="coerce")
    df["income"] = pd.to_numeric(df["income"], errors="coerce")
    df["total_score"] = pd.to_numeric(df["total_score"], errors="coerce")
    df["world_rank"] = df["world_rank"].astype(str).str.extract(r"(\d+)").astype(float)  # some ranks like "201-250"
    dupes = df.duplicated(subset=["university_name", "year"]).sum()
    df = df.drop_duplicates(subset=["university_name", "year"])
    missing_score = df["total_score"].isna().sum()
    log("clean_times", f"{before} -> {len(df)} rows | {dupes} dupes removed | "
                        f"{missing_score} missing total_score (kept null) | numeric coercion applied to "
                        f"num_students, international_students, income, world_rank")
    df.to_csv(os.path.join(OUT_DIR, "clean_times.csv"), index=False)
    return df


def clean_cwur():
    df = pd.read_csv(os.path.join(RAW_DIR, "cwurData.csv"))
    before = len(df)
    df["institution"] = df["institution"].apply(std_name)
    df["country"] = df["country"].apply(std_country)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    dupes = df.duplicated(subset=["institution", "year"]).sum()
    df = df.drop_duplicates(subset=["institution", "year"])
    missing_broad_impact = df["broad_impact"].isna().sum()
    log("clean_cwur", f"{before} -> {len(df)} rows | {dupes} dupes removed | "
                       f"{missing_broad_impact} rows missing broad_impact (not reported before 2014, kept null)")
    df.to_csv(os.path.join(OUT_DIR, "clean_cwur.csv"), index=False)
    return df


def clean_shanghai():
    df = pd.read_csv(os.path.join(RAW_DIR, "shanghaiData.csv"))
    before = len(df)
    df["university_name"] = df["university_name"].apply(std_name)
    df["world_rank"] = df["world_rank"].astype(str).str.extract(r"(\d+)").astype(float)
    for col in ["total_score", "alumni", "award", "hici", "ns", "pub", "pcp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    dupes = df.duplicated(subset=["university_name", "year"]).sum()
    df = df.drop_duplicates(subset=["university_name", "year"])
    missing_total = df["total_score"].isna().sum()
    log("clean_shanghai", f"{before} -> {len(df)} rows | {dupes} dupes removed | "
                           f"{missing_total} rows missing total_score (kept null — ARWU doesn't publish a "
                           f"composite score below the top tier)")
    df.to_csv(os.path.join(OUT_DIR, "clean_shanghai.csv"), index=False)
    return df


def clean_qs2023():
    df = pd.read_csv(os.path.join(RAW_DIR, "WorldUniversityRankings2023.csv"))
    before = len(df)
    df = df.rename(columns={
        "University Rank": "world_rank", "Name of University": "university_name", "Location": "country",
        "No of student": "num_students", "No of student per staff": "student_staff_ratio",
        "International Student": "international_students", "Female:Male Ratio": "female_ratio",
        "OverAll Score": "overall_score", "Teaching Score": "teaching_score", "Research Score": "research_score",
        "Citations Score": "citations_score", "Industry Income Score": "industry_income_score",
        "International Outlook Score": "international_outlook_score",
    })
    df["university_name"] = df["university_name"].apply(std_name)
    df["country"] = df["country"].apply(std_country)
    df["num_students"] = df["num_students"].apply(commas_to_int)
    df["international_students"] = df["international_students"].apply(pct_to_float)
    df["female_ratio"] = df["female_ratio"].apply(ratio_first_half)
    for col in ["world_rank", "overall_score", "teaching_score", "research_score", "citations_score",
                "industry_income_score", "international_outlook_score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["year"] = 2023
    dupes = df.duplicated(subset=["university_name"]).sum()
    df = df.drop_duplicates(subset=["university_name"])
    log("clean_qs2023", f"{before} -> {len(df)} rows | {dupes} dupes removed | "
                         f"parsed '%' / 'a : b' ratio / comma-thousands text fields to numeric")
    df.to_csv(os.path.join(OUT_DIR, "clean_qs2023.csv"), index=False)
    return df


def clean_school_country():
    df = pd.read_csv(os.path.join(RAW_DIR, "school_and_country_table.csv"))
    before = len(df)
    df["school_name"] = df["school_name"].apply(std_name)
    df["country"] = df["country"].apply(std_country)
    dupes = df.duplicated(subset=["school_name"]).sum()
    df = df.drop_duplicates(subset=["school_name"])
    log("clean_school_country", f"{before} -> {len(df)} rows | {dupes} dupes removed")
    df.to_csv(os.path.join(OUT_DIR, "clean_school_country.csv"), index=False)
    return df


def clean_expenditure():
    """Wide (one column per year) -> long (country, year, indicator, value)."""
    df = pd.read_csv(os.path.join(RAW_DIR, "education_expenditure_supplementary_data.csv"), engine="python")
    before = len(df)
    df["country"] = df["country"].apply(std_country)
    year_cols = [c for c in df.columns if c.isdigit()]
    long_df = df.melt(id_vars=["country", "institute_type", "direct_expenditure_type"],
                       value_vars=year_cols, var_name="year", value_name="expenditure_pct_gdp")
    long_df["year"] = long_df["year"].astype(int)
    long_df = long_df.dropna(subset=["expenditure_pct_gdp"])
    log("clean_expenditure", f"{before} wide rows -> {len(long_df)} long (country, year) observations "
                              f"after melting {len(year_cols)} year columns and dropping empty cells")
    long_df.to_csv(os.path.join(OUT_DIR, "clean_expenditure.csv"), index=False)
    return long_df


def clean_attainment():
    """Wide (one column per year) -> long. This file is large (79k rows x 29 cols) so we filter
    to tertiary-education-relevant series only, which is what EduVision_DV actually visualizes."""
    df = pd.read_csv(os.path.join(RAW_DIR, "educational_attainment_supplementary_data.csv"), engine="python")
    before = len(df)
    df["country_name"] = df["country_name"].apply(std_country)
    tertiary_mask = df["series_name"].str.contains("tertiary", case=False, na=False)
    tertiary = df[tertiary_mask].copy()
    year_cols = [c for c in df.columns if c.isdigit()]
    long_df = tertiary.melt(id_vars=["country_name", "series_name"], value_vars=year_cols,
                             var_name="year", value_name="value")
    long_df["year"] = long_df["year"].astype(int)
    long_df = long_df.dropna(subset=["value"])
    log("clean_attainment", f"{before} wide rows ({df['series_name'].nunique()} series) -> filtered to "
                             f"{tertiary['series_name'].nunique()} tertiary-education series -> "
                             f"{len(long_df)} long observations after melting")
    long_df.to_csv(os.path.join(OUT_DIR, "clean_attainment.csv"), index=False)
    return long_df


if __name__ == "__main__":
    clean_times()
    clean_cwur()
    clean_shanghai()
    clean_qs2023()
    clean_school_country()
    clean_expenditure()
    clean_attainment()
    with open(os.path.join(OUT_DIR, "cleaning_log.txt"), "w") as f:
        f.write("\n".join(LOG))
    print("\nCleaning complete: 7 clean sources in data/processed/ (see cleaning_log.txt)")
