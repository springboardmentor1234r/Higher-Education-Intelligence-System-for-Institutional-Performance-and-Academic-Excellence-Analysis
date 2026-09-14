from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# STEP 9.3 - UNIVERSITY & COUNTRY ANALYSIS
# ============================================================

print("=" * 70)
print("STEP 9.3 - UNIVERSITY & COUNTRY ANALYSIS")
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
print(f"Rows       : {len(df)}")
print(f"Countries  : {df['country_name'].nunique()}")


# ============================================================
# 3. TOP COUNTRIES BY UNIVERSITY COUNT
# ============================================================

print("\n" + "=" * 70)
print("1. TOP COUNTRIES BY UNIVERSITY COUNT")
print("=" * 70)

country_count = (
    df.groupby("country_name")
    .size()
    .reset_index(name="university_count")
    .sort_values("university_count", ascending=False)
)

print(country_count.head(30).to_string(index=False))

country_count.to_csv(
    EDA_DIR / "country_university_distribution.csv",
    index=False
)


# ============================================================
# 4. WORLD BANK REGION DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("2. UNIVERSITY DISTRIBUTION BY WORLD BANK REGION")
print("=" * 70)

region_count = (
    df.groupby("wb_region", dropna=False)
    .size()
    .reset_index(name="university_count")
    .sort_values("university_count", ascending=False)
)

region_count["percentage"] = (
    region_count["university_count"]
    / len(df)
    * 100
)

print(region_count.to_string(index=False))

region_count.to_csv(
    EDA_DIR / "country_analysis_region.csv",
    index=False
)


# ============================================================
# 5. INCOME GROUP DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("3. UNIVERSITY DISTRIBUTION BY INCOME GROUP")
print("=" * 70)

income_count = (
    df.groupby("wb_income_group", dropna=False)
    .size()
    .reset_index(name="university_count")
    .sort_values("university_count", ascending=False)
)

income_count["percentage"] = (
    income_count["university_count"]
    / len(df)
    * 100
)

print(income_count.to_string(index=False))

income_count.to_csv(
    EDA_DIR / "country_analysis_income_group.csv",
    index=False
)


# ============================================================
# 6. QS 2025 COUNTRY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("4. QS 2025 COUNTRY ANALYSIS")
print("=" * 70)

qs_df = df[df["qs_present"] == True].copy()

qs_country = (
    qs_df.groupby("country_name")
    .agg(
        university_count=("university_id", "count"),
        average_qs_score=("qs_overall_score", "mean"),
        average_qs_rank=("qs_rank_2025", "mean"),
        best_qs_rank=("qs_rank_2025", "min")
    )
    .reset_index()
)

qs_country = qs_country.sort_values(
    "university_count",
    ascending=False
)

print(qs_country.head(30).to_string(index=False))

qs_country.to_csv(
    EDA_DIR / "qs_2025_country_analysis.csv",
    index=False
)


# ============================================================
# 7. THE 2024 COUNTRY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. THE 2024 COUNTRY ANALYSIS")
print("=" * 70)

the24_df = df[df["the24_present"] == True].copy()

the24_country = (
    the24_df.groupby("country_name")
    .agg(
        university_count=("university_id", "count"),
        average_overall_score=("the_overall_score_2024", "mean"),
        average_student_staff_ratio=("the_student_staff_ratio_2024", "mean"),
        average_international_students=(
            "the_international_students_pct_2024",
            "mean"
        ),
        average_female_percentage=(
            "the_female_percentage_2024",
            "mean"
        )
    )
    .reset_index()
)

the24_country = the24_country.sort_values(
    "university_count",
    ascending=False
)

print(the24_country.head(30).to_string(index=False))

the24_country.to_csv(
    EDA_DIR / "the_2024_country_analysis.csv",
    index=False
)


# ============================================================
# 8. THE 2023 COUNTRY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("6. THE 2023 COUNTRY ANALYSIS")
print("=" * 70)

the23_df = df[df["the23_present"] == True].copy()

the23_country = (
    the23_df.groupby("country_name")
    .agg(
        university_count=("university_id", "count"),
        average_overall_score=("the_overall_score_2023", "mean"),
        average_student_staff_ratio=("the_student_staff_ratio_2023", "mean"),
        average_international_students=(
            "the_international_students_pct_2023",
            "mean"
        ),
        average_female_percentage=(
            "the_female_percentage_2023",
            "mean"
        )
    )
    .reset_index()
)

the23_country = the23_country.sort_values(
    "university_count",
    ascending=False
)

print(the23_country.head(30).to_string(index=False))

the23_country.to_csv(
    EDA_DIR / "the_2023_country_analysis.csv",
    index=False
)


# ============================================================
# 9. TOP COUNTRIES BY QS PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("7. TOP COUNTRIES BY QS 2025 AVERAGE SCORE")
print("=" * 70)

qs_performance = (
    qs_df.groupby("country_name")
    .agg(
        university_count=("university_id", "count"),
        average_score=("qs_overall_score", "mean"),
        best_rank=("qs_rank_2025", "min")
    )
    .reset_index()
)

# Only countries with at least 5 QS universities
qs_performance_5plus = qs_performance[
    qs_performance["university_count"] >= 5
].copy()

qs_performance_5plus = qs_performance_5plus.sort_values(
    "average_score",
    ascending=False
)

print(
    qs_performance_5plus.head(20).to_string(index=False)
)

qs_performance_5plus.to_csv(
    EDA_DIR / "top_qs_countries_5plus_universities.csv",
    index=False
)


# ============================================================
# 10. INDIA ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. INDIA ANALYSIS")
print("=" * 70)

india = df[
    df["country_name"].str.lower().str.contains(
        "india",
        na=False
    )
].copy()

print(f"Indian universities in dataset: {len(india)}")

print(
    "\nIndian universities by ranking presence:"
)

print(
    india[
        [
            "university_name",
            "qs_present",
            "the24_present",
            "the23_present"
        ]
    ].head(20).to_string(index=False)
)

india_qs = india[
    india["qs_present"] == True
].copy()

if len(india_qs) > 0:

    india_qs = india_qs.sort_values(
        "qs_rank_2025"
    )

    print("\nTop Indian universities in QS 2025:")

    print(
        india_qs[
            [
                "university_name",
                "qs_rank_2025",
                "qs_overall_score"
            ]
        ].head(20).to_string(index=False)
    )

    india_qs[
        [
            "university_name",
            "qs_rank_2025",
            "qs_overall_score"
        ]
    ].to_csv(
        EDA_DIR / "india_qs_2025_analysis.csv",
        index=False
    )


# ============================================================
# 11. COUNTRY CONCENTRATION
# ============================================================

print("\n" + "=" * 70)
print("9. COUNTRY CONCENTRATION")
print("=" * 70)

top_10_count = country_count.head(10)["university_count"].sum()

top_20_count = country_count.head(20)["university_count"].sum()

top_10_percentage = (
    top_10_count / len(df) * 100
)

top_20_percentage = (
    top_20_count / len(df) * 100
)

print(
    f"Top 10 countries: {top_10_count} universities "
    f"({top_10_percentage:.2f}%)"
)

print(
    f"Top 20 countries: {top_20_count} universities "
    f"({top_20_percentage:.2f}%)"
)


concentration = pd.DataFrame({
    "group": ["Top 10 countries", "Top 20 countries"],
    "university_count": [top_10_count, top_20_count],
    "percentage": [
        top_10_percentage,
        top_20_percentage
    ]
})

concentration.to_csv(
    EDA_DIR / "country_concentration.csv",
    index=False
)


# ============================================================
# 12. VISUALIZATION - TOP 20 COUNTRIES
# ============================================================

print("\n" + "=" * 70)
print("10. CREATING VISUALIZATIONS")
print("=" * 70)

top20 = country_count.head(20).sort_values(
    "university_count"
)

plt.figure(figsize=(12, 8))

plt.barh(
    top20["country_name"],
    top20["university_count"]
)

plt.xlabel("Number of Universities")
plt.ylabel("Country")
plt.title("Top 20 Countries by Number of Universities")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "top_20_countries_universities.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "top_20_countries_universities.png"
)


# ============================================================
# 13. VISUALIZATION - WORLD BANK REGIONS
# ============================================================

region_plot = region_count.dropna(
    subset=["wb_region"]
)

plt.figure(figsize=(10, 6))

plt.bar(
    region_plot["wb_region"],
    region_plot["university_count"]
)

plt.xlabel("World Bank Region")
plt.ylabel("Number of Universities")
plt.title("University Distribution by World Bank Region")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "universities_by_world_bank_region.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "universities_by_world_bank_region.png"
)


# ============================================================
# 14. VISUALIZATION - INCOME GROUP
# ============================================================

income_plot = income_count.dropna(
    subset=["wb_income_group"]
)

plt.figure(figsize=(10, 6))

plt.bar(
    income_plot["wb_income_group"],
    income_plot["university_count"]
)

plt.xlabel("Income Group")
plt.ylabel("Number of Universities")
plt.title("University Distribution by World Bank Income Group")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "universities_by_income_group.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "universities_by_income_group.png"
)


# ============================================================
# 15. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.3 SUMMARY")
print("=" * 70)

print(f"\nTotal universities : {len(df)}")
print(f"Total countries    : {df['country_name'].nunique()}")

print("\nTop 5 countries by university count:")

print(
    country_count.head(5).to_string(index=False)
)

print("\nWorld Bank region with most universities:")

print(
    region_count.dropna(
        subset=["wb_region"]
    ).iloc[0].to_string()
)

print("\nLargest income group:")

print(
    income_count.dropna(
        subset=["wb_income_group"]
    ).iloc[0].to_string()
)

print("\nOutput directory:")
print(EDA_DIR)

print("\nFigure directory:")
print(FIGURE_DIR)

print("\n" + "=" * 70)
print("STEP 9.3 COMPLETED")
print("=" * 70)