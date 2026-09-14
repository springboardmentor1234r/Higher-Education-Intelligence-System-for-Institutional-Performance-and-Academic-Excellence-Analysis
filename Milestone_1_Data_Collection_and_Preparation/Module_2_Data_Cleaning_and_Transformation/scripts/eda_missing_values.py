from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# STEP 9.2 - MISSING VALUE & DATA QUALITY ANALYSIS
# ============================================================

print("=" * 70)
print("STEP 9.2 - MISSING VALUE & DATA QUALITY ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "university_integrated_worldbank_education.csv"
)

EDA_DIR = BASE_DIR / "data" / "eda"
FIGURE_DIR = BASE_DIR / "reports" / "figures"

EDA_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

print("\nLoading final analytical dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# ------------------------------------------------------------
# 3. OVERALL MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. OVERALL MISSING VALUE ANALYSIS")
print("=" * 70)

missing = pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isna().sum(),
    "missing_percentage": (df.isna().mean() * 100)
})

missing = missing.sort_values(
    by="missing_percentage",
    ascending=False
)

print(missing.to_string(index=False))

missing.to_csv(
    EDA_DIR / "missing_value_analysis_9_2.csv",
    index=False
)

print("\nSaved:")
print(EDA_DIR / "missing_value_analysis_9_2.csv")


# ------------------------------------------------------------
# 4. DATA QUALITY CATEGORIES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. DATA QUALITY CATEGORIES")
print("=" * 70)

def classify_missing(row):
    pct = row["missing_percentage"]

    if pct == 0:
        return "Complete"

    elif pct < 20:
        return "Low Missingness"

    elif pct < 50:
        return "Moderate Missingness"

    elif pct < 80:
        return "High Missingness"

    else:
        return "Very High Missingness"


missing["missing_category"] = missing.apply(
    classify_missing,
    axis=1
)

print(
    missing[
        [
            "column",
            "missing_count",
            "missing_percentage",
            "missing_category"
        ]
    ].to_string(index=False)
)

missing.to_csv(
    EDA_DIR / "missing_value_categories.csv",
    index=False
)


# ------------------------------------------------------------
# 5. RANKING MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. RANKING MISSING VALUE ANALYSIS")
print("=" * 70)

ranking_columns = [
    "qs_rank_2025",
    "qs_overall_score",
    "the_rank_2024",
    "the_overall_score_2024",
    "the_rank_2023",
    "the_overall_score_2023"
]

ranking_missing = []

for column in ranking_columns:

    total = len(df)
    missing_count = df[column].isna().sum()
    available = total - missing_count

    ranking_missing.append({
        "column": column,
        "available": available,
        "missing": missing_count,
        "missing_percentage": missing_count / total * 100
    })

ranking_missing = pd.DataFrame(ranking_missing)

print(ranking_missing.to_string(index=False))

ranking_missing.to_csv(
    EDA_DIR / "ranking_missing_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 6. RANKING PRESENCE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. RANKING PRESENCE ANALYSIS")
print("=" * 70)

ranking_presence = pd.DataFrame({
    "QS_2025": df["qs_present"],
    "THE_2024": df["the24_present"],
    "THE_2023": df["the23_present"]
})

ranking_presence["ranking_count"] = ranking_presence.sum(axis=1)

presence_summary = (
    ranking_presence["ranking_count"]
    .value_counts()
    .sort_index()
    .reset_index()
)

presence_summary.columns = [
    "number_of_rankings",
    "university_count"
]

presence_summary["percentage"] = (
    presence_summary["university_count"]
    / len(df)
    * 100
)

print(presence_summary.to_string(index=False))

presence_summary.to_csv(
    EDA_DIR / "ranking_presence_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 7. WORLD BANK EDUCATION MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. WORLD BANK EDUCATION MISSING VALUE ANALYSIS")
print("=" * 70)

education_columns = [
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015"
]

education_analysis = []

for column in education_columns:

    total = len(df)

    available = df[column].notna().sum()
    missing_count = df[column].isna().sum()

    education_analysis.append({
        "indicator": column,
        "available": available,
        "missing": missing_count,
        "coverage_percentage": available / total * 100,
        "missing_percentage": missing_count / total * 100
    })

education_analysis = pd.DataFrame(education_analysis)

print(
    education_analysis.to_string(index=False)
)

education_analysis.to_csv(
    EDA_DIR / "education_missing_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 8. MISSING EDUCATION INDICATORS PER UNIVERSITY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. MISSING EDUCATION INDICATORS PER UNIVERSITY")
print("=" * 70)

df["education_missing_count"] = (
    df[education_columns].isna().sum(axis=1)
)

education_missing_distribution = (
    df["education_missing_count"]
    .value_counts()
    .sort_index()
    .reset_index()
)

education_missing_distribution.columns = [
    "missing_indicator_count",
    "university_count"
]

education_missing_distribution["percentage"] = (
    education_missing_distribution["university_count"]
    / len(df)
    * 100
)

print(
    education_missing_distribution.to_string(index=False)
)

education_missing_distribution.to_csv(
    EDA_DIR / "education_missing_distribution.csv",
    index=False
)


# ------------------------------------------------------------
# 9. UNIVERSITIES WITH NO EDUCATION DATA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. UNIVERSITIES WITH NO WORLD BANK EDUCATION DATA")
print("=" * 70)

no_education = df[
    df["education_missing_count"] == len(education_columns)
].copy()

print(
    f"Universities with no education indicators: {len(no_education)}"
)

no_education_output = no_education[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_country_code",
        "wb_region",
        "wb_income_group"
    ]
]

no_education_output.to_csv(
    EDA_DIR / "universities_without_education_data.csv",
    index=False
)

print(
    "Saved:",
    EDA_DIR / "universities_without_education_data.csv"
)


# ------------------------------------------------------------
# 10. MISSING VALUES BY WORLD BANK REGION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. MISSING EDUCATION DATA BY REGION")
print("=" * 70)

region_analysis = []

for region, group in df.groupby(
    "wb_region",
    dropna=False
):

    row = {
        "region": region,
        "university_count": len(group)
    }

    for column in education_columns:

        row[column + "_missing_percentage"] = (
            group[column].isna().mean() * 100
        )

    region_analysis.append(row)

region_analysis = pd.DataFrame(region_analysis)

print(
    region_analysis.to_string(index=False)
)

region_analysis.to_csv(
    EDA_DIR / "education_missing_by_region.csv",
    index=False
)


# ------------------------------------------------------------
# 11. VISUALIZATION - OVERALL MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. CREATING MISSING VALUE VISUALIZATION")
print("=" * 70)

plot_df = missing[
    missing["missing_percentage"] > 0
].head(20)

plt.figure(figsize=(12, 8))

plt.barh(
    plot_df["column"][::-1],
    plot_df["missing_percentage"][::-1]
)

plt.xlabel("Missing Values (%)")
plt.ylabel("Column")
plt.title("Top 20 Columns by Missing Values")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "missing_values_overview.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "missing_values_overview.png"
)


# ------------------------------------------------------------
# 12. VISUALIZATION - RANKING MISSING VALUES
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    ranking_missing["column"],
    ranking_missing["missing_percentage"]
)

plt.ylabel("Missing Values (%)")
plt.xlabel("Ranking Variable")
plt.title("Missing Values in Ranking Variables")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "ranking_missing_values.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "ranking_missing_values.png"
)


# ------------------------------------------------------------
# 13. VISUALIZATION - WORLD BANK EDUCATION
# ------------------------------------------------------------

plt.figure(figsize=(11, 6))

plt.bar(
    education_analysis["indicator"],
    education_analysis["missing_percentage"]
)

plt.ylabel("Missing Values (%)")
plt.xlabel("Education Indicator")
plt.title("Missing Values in World Bank Education Indicators")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "worldbank_education_missing_values.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "worldbank_education_missing_values.png"
)


# ------------------------------------------------------------
# 14. REMOVE TEMPORARY COLUMN FROM DATAFRAME
# ------------------------------------------------------------

df.drop(
    columns=["education_missing_count"],
    inplace=True
)


# ------------------------------------------------------------
# 15. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 9.2 SUMMARY")
print("=" * 70)

print(f"\nTotal universities       : {len(df)}")
print(f"Total columns            : {len(df.columns)}")

print(
    f"\nUniversities with NO "
    f"World Bank education data: {len(no_education)}"
)

print("\nHighest missing ranking field:")

highest_ranking_missing = ranking_missing.loc[
    ranking_missing["missing_percentage"].idxmax()
]

print(
    f"  {highest_ranking_missing['column']} : "
    f"{highest_ranking_missing['missing_percentage']:.2f}%"
)

print("\nHighest missing education indicator:")

highest_education_missing = education_analysis.loc[
    education_analysis["missing_percentage"].idxmax()
]

print(
    f"  {highest_education_missing['indicator']} : "
    f"{highest_education_missing['missing_percentage']:.2f}%"
)

print("\nOutput directory:")
print(EDA_DIR)

print("\nFigure directory:")
print(FIGURE_DIR)

print("\n" + "=" * 70)
print("STEP 9.2 COMPLETED")
print("=" * 70)