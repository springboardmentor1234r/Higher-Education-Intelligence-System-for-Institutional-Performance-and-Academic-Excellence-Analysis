import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 70)
print("STEP 9.1 - EXPLORATORY DATA ANALYSIS OVERVIEW")
print("=" * 70)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank_education.csv"
)

EDA_DIR = BASE_DIR / "data" / "eda"

EDA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading final analytical dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")

# ============================================================
# 1. BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATASET INFORMATION")
print("=" * 70)

print("Rows       :", df.shape[0])
print("Columns    :", df.shape[1])
print("Countries  :", df["country_name"].nunique())
print("Universities:", df["university_name"].nunique())

# ============================================================
# 2. DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("2. DATA TYPES")
print("=" * 70)

dtype_summary = (
    df.dtypes
    .astype(str)
    .value_counts()
)

print(dtype_summary)

# ============================================================
# 3. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("3. MISSING VALUE ANALYSIS")
print("=" * 70)

missing_df = pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isna().sum(),
})

missing_df["missing_percentage"] = (
    missing_df["missing_count"]
    / len(df)
    * 100
)

missing_df = missing_df.sort_values(
    "missing_percentage",
    ascending=False
)

print(
    missing_df.to_string(index=False)
)

# Save missing-value report
missing_file = (
    EDA_DIR / "missing_value_summary.csv"
)

missing_df.to_csv(
    missing_file,
    index=False
)

print("\nSaved:")
print(missing_file)

# ============================================================
# 4. NUMERIC DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("4. NUMERIC DESCRIPTIVE STATISTICS")
print("=" * 70)

numeric_df = df.select_dtypes(
    include=np.number
)

statistics = numeric_df.describe().T

statistics["missing"] = (
    numeric_df.isna().sum()
)

statistics["missing_percentage"] = (
    numeric_df.isna().mean() * 100
)

print(
    statistics.to_string()
)

stats_file = (
    EDA_DIR / "numeric_descriptive_statistics.csv"
)

statistics.to_csv(
    stats_file
)

print("\nSaved:")
print(stats_file)

# ============================================================
# 5. COUNTRY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. UNIVERSITY COUNT BY COUNTRY")
print("=" * 70)

country_counts = (
    df["country_name"]
    .value_counts()
    .reset_index()
)

country_counts.columns = [
    "country_name",
    "university_count"
]

print(
    country_counts.head(20)
    .to_string(index=False)
)

country_file = (
    EDA_DIR / "university_count_by_country.csv"
)

country_counts.to_csv(
    country_file,
    index=False
)

print("\nSaved:")
print(country_file)

# ============================================================
# 6. REGION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("6. UNIVERSITY COUNT BY WORLD BANK REGION")
print("=" * 70)

region_counts = (
    df["wb_region"]
    .value_counts(dropna=False)
    .reset_index()
)

region_counts.columns = [
    "region",
    "university_count"
]

print(
    region_counts.to_string(index=False)
)

region_file = (
    EDA_DIR / "university_count_by_region.csv"
)

region_counts.to_csv(
    region_file,
    index=False
)

print("\nSaved:")
print(region_file)

# ============================================================
# 7. INCOME GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("7. UNIVERSITY COUNT BY INCOME GROUP")
print("=" * 70)

income_counts = (
    df["wb_income_group"]
    .value_counts(dropna=False)
    .reset_index()
)

income_counts.columns = [
    "income_group",
    "university_count"
]

print(
    income_counts.to_string(index=False)
)

income_file = (
    EDA_DIR / "university_count_by_income_group.csv"
)

income_counts.to_csv(
    income_file,
    index=False
)

print("\nSaved:")
print(income_file)

# ============================================================
# 8. RANKING COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("8. RANKING COVERAGE")
print("=" * 70)

ranking_coverage = pd.DataFrame({
    "ranking": [
        "QS 2025",
        "THE 2024",
        "THE 2023",
        "All Three"
    ],
    "university_count": [
        df["qs_present"].sum(),
        df["the24_present"].sum(),
        df["the23_present"].sum(),
        (
            (df["qs_present"] == True)
            & (df["the24_present"] == True)
            & (df["the23_present"] == True)
        ).sum()
    ]
})

ranking_coverage["percentage"] = (
    ranking_coverage["university_count"]
    / len(df)
    * 100
)

print(
    ranking_coverage.to_string(index=False)
)

ranking_file = (
    EDA_DIR / "ranking_coverage.csv"
)

ranking_coverage.to_csv(
    ranking_file,
    index=False
)

print("\nSaved:")
print(ranking_file)

# ============================================================
# 9. WORLD BANK EDUCATION COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("9. WORLD BANK EDUCATION COVERAGE")
print("=" * 70)

education_columns = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015"
]

education_coverage = []

for col in education_columns:

    available = df[col].notna().sum()

    missing = df[col].isna().sum()

    percentage = (
        available / len(df) * 100
    )

    education_coverage.append({
        "indicator": col,
        "available": available,
        "missing": missing,
        "coverage_percentage": percentage
    })

education_coverage = pd.DataFrame(
    education_coverage
)

print(
    education_coverage.to_string(index=False)
)

education_file = (
    EDA_DIR / "worldbank_education_coverage.csv"
)

education_coverage.to_csv(
    education_file,
    index=False
)

print("\nSaved:")
print(education_file)

# ============================================================
# 10. QS TOP UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("10. TOP 20 QS 2025 UNIVERSITIES")
print("=" * 70)

qs_top = (
    df[
        df["qs_rank_2025"].notna()
    ][
        [
            "qs_rank_2025",
            "university_name",
            "country_name",
            "qs_overall_score"
        ]
    ]
    .sort_values("qs_rank_2025")
    .head(20)
)

print(
    qs_top.to_string(index=False)
)

qs_top_file = (
    EDA_DIR / "top_20_qs_2025.csv"
)

qs_top.to_csv(
    qs_top_file,
    index=False
)

# ============================================================
# 11. TOP THE 2024 UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("11. TOP 20 THE 2024 UNIVERSITIES")
print("=" * 70)

the_top = (
    df[
        df["the_rank_2024"].notna()
    ][
        [
            "the_rank_2024",
            "university_name",
            "country_name",
            "the_overall_score_2024"
        ]
    ]
    .sort_values("the_rank_2024")
    .head(20)
)

print(
    the_top.to_string(index=False)
)

the_top_file = (
    EDA_DIR / "top_20_the_2024.csv"
)

the_top.to_csv(
    the_top_file,
    index=False
)

# ============================================================
# 12. MULTI-RANKING UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("12. UNIVERSITIES PRESENT IN ALL THREE RANKINGS")
print("=" * 70)

all_three_df = df[
    (df["qs_present"] == True)
    & (df["the24_present"] == True)
    & (df["the23_present"] == True)
].copy()

print(
    "Universities present in all three:",
    len(all_three_df)
)

print(
    all_three_df[
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "the_rank_2024",
            "the_rank_2023"
        ]
    ]
    .sort_values("qs_rank_2025")
    .head(20)
    .to_string(index=False)
)

all_three_file = (
    EDA_DIR / "universities_all_three_rankings.csv"
)

all_three_df[
    [
        "university_id",
        "university_name",
        "country_name",
        "qs_rank_2025",
        "the_rank_2024",
        "the_rank_2023"
    ]
].to_csv(
    all_three_file,
    index=False
)

# ============================================================
# 13. FINAL EDA OVERVIEW SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.1 SUMMARY")
print("=" * 70)

print("\nDataset:")
print("  Rows:", len(df))
print("  Columns:", len(df.columns))
print("  Countries:", df["country_name"].nunique())

print("\nRanking coverage:")
print("  QS 2025 :", int(df["qs_present"].sum()))
print("  THE 2024:", int(df["the24_present"].sum()))
print("  THE 2023:", int(df["the23_present"].sum()))
print("  All 3   :", len(all_three_df))

print("\nWorld Bank:")
print("  Metadata linked:", int(df["worldbank_linked"].sum()))
print(
    "  Education linked:",
    int(df["worldbank_education_2015_linked"].sum())
)

print("\nEDA output directory:")
print(EDA_DIR)

print("\n" + "=" * 70)
print("STEP 9.1 COMPLETED")
print("=" * 70)