from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# STEP 9.5 - THE 2024 RANKING ANALYSIS
# ============================================================

print("=" * 70)
print("STEP 9.5 - THE 2024 RANKING ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# PATHS
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
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading final analytical dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")


# ------------------------------------------------------------
# THE 2024 DATA
# ------------------------------------------------------------

the = df[df["the24_present"] == True].copy()

print(f"\nUniversities with THE 2024 data: {len(the)}")


# ------------------------------------------------------------
# 1. BASIC THE 2024 STATISTICS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. BASIC THE 2024 STATISTICS")
print("=" * 70)

print(f"Universities             : {len(the)}")
print(f"Countries represented    : {the['country_name'].nunique()}")

print("\nTHE 2024 Rank statistics:")

print(the["the_rank_2024"].describe())


print("\nTHE 2024 Overall Score statistics:")

print(the["the_overall_score_2024"].describe())


# ------------------------------------------------------------
# 2. TOP 20 UNIVERSITIES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. TOP 20 THE 2024 UNIVERSITIES")
print("=" * 70)

top20 = (
    the[
        [
            "the_rank_2024",
            "university_name",
            "country_name",
            "the_overall_score_2024",
        ]
    ]
    .dropna(subset=["the_rank_2024"])
    .sort_values("the_rank_2024")
    .head(20)
)

print(top20.to_string(index=False))

top20.to_csv(
    EDA_DIR / "top_20_the_2024_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 3. RANKING TIERS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. THE 2024 RANKING TIERS")
print("=" * 70)


def rank_tier(rank):
    if pd.isna(rank):
        return "Unranked"
    elif rank <= 50:
        return "Top 50"
    elif rank <= 100:
        return "51-100"
    elif rank <= 200:
        return "101-200"
    elif rank <= 500:
        return "201-500"
    else:
        return "501+"


the["rank_tier"] = the["the_rank_2024"].apply(rank_tier)

tier_order = [
    "Top 50",
    "51-100",
    "101-200",
    "201-500",
    "501+",
    "Unranked",
]

tier_counts = (
    the["rank_tier"]
    .value_counts()
    .reindex(tier_order, fill_value=0)
    .reset_index()
)

tier_counts.columns = [
    "rank_tier",
    "university_count"
]

tier_counts["percentage"] = (
    tier_counts["university_count"]
    / len(the)
    * 100
)

print(tier_counts.to_string(index=False))

tier_counts.to_csv(
    EDA_DIR / "the_2024_ranking_tiers.csv",
    index=False
)


# ------------------------------------------------------------
# 4. COUNTRY DISTRIBUTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. THE 2024 UNIVERSITY DISTRIBUTION BY COUNTRY")
print("=" * 70)

country_distribution = (
    the.groupby("country_name")
    .agg(
        university_count=("university_name", "count"),
        average_score=("the_overall_score_2024", "mean"),
        average_rank=("the_rank_2024", "mean"),
        best_rank=("the_rank_2024", "min"),
    )
    .sort_values(
        "university_count",
        ascending=False
    )
)

print(country_distribution.head(30).to_string())

country_distribution.to_csv(
    EDA_DIR / "the_2024_country_distribution.csv"
)


# ------------------------------------------------------------
# 5. COUNTRY PERFORMANCE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. THE 2024 COUNTRY PERFORMANCE")
print("=" * 70)

country_performance = (
    the.groupby("country_name")
    .agg(
        university_count=("university_name", "count"),
        average_score=("the_overall_score_2024", "mean"),
        average_rank=("the_rank_2024", "mean"),
        best_rank=("the_rank_2024", "min"),
    )
    .reset_index()
)

# Consider only countries with at least 5 universities
country_performance_5 = (
    country_performance[
        country_performance["university_count"] >= 5
    ]
    .sort_values(
        "average_score",
        ascending=False
    )
)

print(
    country_performance_5.head(20)
    .to_string(index=False)
)

country_performance_5.to_csv(
    EDA_DIR / "the_2024_country_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 6. WORLD BANK REGION PERFORMANCE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. THE 2024 PERFORMANCE BY WORLD BANK REGION")
print("=" * 70)

region_performance = (
    the.groupby("wb_region", dropna=False)
    .agg(
        university_count=("university_name", "count"),
        average_score=("the_overall_score_2024", "mean"),
        average_rank=("the_rank_2024", "mean"),
        best_rank=("the_rank_2024", "min"),
    )
    .reset_index()
    .sort_values(
        "average_score",
        ascending=False
    )
)

print(region_performance.to_string(index=False))

region_performance.to_csv(
    EDA_DIR / "the_2024_region_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 7. INCOME GROUP PERFORMANCE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. THE 2024 PERFORMANCE BY INCOME GROUP")
print("=" * 70)

income_performance = (
    the.groupby("wb_income_group", dropna=False)
    .agg(
        university_count=("university_name", "count"),
        average_score=("the_overall_score_2024", "mean"),
        average_rank=("the_rank_2024", "mean"),
        best_rank=("the_rank_2024", "min"),
    )
    .reset_index()
    .sort_values(
        "average_score",
        ascending=False
    )
)

print(income_performance.to_string(index=False))

income_performance.to_csv(
    EDA_DIR / "the_2024_income_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 8. THE INDICATOR ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. THE 2024 INDICATOR ANALYSIS")
print("=" * 70)

indicators = [
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "the_female_percentage_2024",
]

indicator_rows = []

for col in indicators:

    available = the[col].notna().sum()
    missing = the[col].isna().sum()

    indicator_rows.append(
        {
            "indicator": col,
            "available": available,
            "missing": missing,
            "mean": the[col].mean(),
            "median": the[col].median(),
            "std": the[col].std(),
        }
    )

indicator_summary = pd.DataFrame(indicator_rows)

print(
    indicator_summary.to_string(index=False)
)

indicator_summary.to_csv(
    EDA_DIR / "the_2024_indicator_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 9. CORRELATION WITH OVERALL SCORE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. THE INDICATOR CORRELATION WITH OVERALL SCORE")
print("=" * 70)

correlation_rows = []

for col in indicators:

    temp = the[
        [
            col,
            "the_overall_score_2024"
        ]
    ].dropna()

    if len(temp) > 1:

        correlation = (
            temp[col]
            .corr(temp["the_overall_score_2024"])
        )

    else:
        correlation = np.nan

    correlation_rows.append(
        {
            "indicator": col,
            "correlation_with_overall_score": correlation,
            "valid_observations": len(temp),
        }
    )

correlation_df = pd.DataFrame(
    correlation_rows
).sort_values(
    "correlation_with_overall_score",
    ascending=False
)

print(
    correlation_df.to_string(index=False)
)

correlation_df.to_csv(
    EDA_DIR / "the_2024_indicator_correlations.csv",
    index=False
)


# ------------------------------------------------------------
# 10. TOP UNIVERSITIES BY OVERALL SCORE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. UNIVERSITIES WITH HIGHEST THE 2024 OVERALL SCORES")
print("=" * 70)

top_scores = (
    the[
        [
            "university_name",
            "country_name",
            "the_rank_2024",
            "the_overall_score_2024",
        ]
    ]
    .dropna(subset=["the_overall_score_2024"])
    .sort_values(
        "the_overall_score_2024",
        ascending=False
    )
    .head(20)
)

print(top_scores.to_string(index=False))


# ------------------------------------------------------------
# 11. INDIA ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. INDIA ANALYSIS")
print("=" * 70)

india = the[
    the["country_name"]
    .str.lower()
    .eq("india")
].copy()

print(
    f"Indian universities with THE 2024 data: {len(india)}"
)

if len(india) > 0:

    india_top = (
        india[
            [
                "university_name",
                "the_rank_2024",
                "the_overall_score_2024",
            ]
        ]
        .sort_values(
            "the_rank_2024",
            na_position="last"
        )
        .head(20)
    )

    print("\nTop Indian universities in THE 2024:")

    print(
        india_top.to_string(index=False)
    )

    india_top.to_csv(
        EDA_DIR / "the_2024_india_top_universities.csv",
        index=False
    )


# ------------------------------------------------------------
# 12. VISUALIZATIONS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. CREATING VISUALIZATIONS")
print("=" * 70)


# Score distribution

plt.figure(figsize=(10, 6))

plt.hist(
    the["the_overall_score_2024"].dropna(),
    bins=25
)

plt.xlabel("THE 2024 Overall Score")
plt.ylabel("Number of Universities")
plt.title("THE 2024 Overall Score Distribution")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "the_2024_score_distribution.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {FIGURE_DIR / 'the_2024_score_distribution.png'}"
)


# Ranking tiers

plt.figure(figsize=(10, 6))

tier_plot = tier_counts[
    tier_counts["rank_tier"] != "Unranked"
]

plt.bar(
    tier_plot["rank_tier"],
    tier_plot["university_count"]
)

plt.xlabel("THE 2024 Ranking Tier")
plt.ylabel("Number of Universities")
plt.title("THE 2024 Ranking Tier Distribution")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "the_2024_rank_tiers.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {FIGURE_DIR / 'the_2024_rank_tiers.png'}"
)


# Top countries by university count

top_countries = (
    country_distribution
    .head(20)
    .sort_values("university_count")
)

plt.figure(figsize=(10, 8))

plt.barh(
    top_countries.index,
    top_countries["university_count"]
)

plt.xlabel("Number of Universities")
plt.ylabel("Country")
plt.title(
    "Top 20 Countries by THE 2024 University Count"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "the_2024_top_countries.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {FIGURE_DIR / 'the_2024_top_countries.png'}"
)


# Indicator correlations

plt.figure(figsize=(10, 6))

corr_plot = correlation_df.dropna(
    subset=["correlation_with_overall_score"]
)

plt.barh(
    corr_plot["indicator"],
    corr_plot["correlation_with_overall_score"]
)

plt.xlabel("Correlation with THE 2024 Overall Score")
plt.ylabel("Indicator")
plt.title(
    "THE 2024 Indicator Correlations with Overall Score"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "the_2024_indicator_correlations.png",
    dpi=300
)

plt.close()

print(
    f"Saved: {FIGURE_DIR / 'the_2024_indicator_correlations.png'}"
)


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 9.5 SUMMARY")
print("=" * 70)

print(f"\nTHE 2024 universities : {len(the)}")
print(
    f"Countries represented : {the['country_name'].nunique()}"
)

if len(top20) > 0:

    print("\nTop THE 2024 university:")

    print(
        top20.head(1).to_string(index=False)
    )

if len(country_distribution) > 0:

    print("\nTop country by university count:")

    print(
        country_distribution
        .head(1)
        .to_string()
    )

if len(correlation_df) > 0:

    print("\nHighest correlation with THE overall score:")

    print(
        correlation_df
        .head(1)
        .to_string(index=False)
    )

print("\nOutput directory:")
print(EDA_DIR)

print("\nFigure directory:")
print(FIGURE_DIR)

print("\n" + "=" * 70)
print("STEP 9.5 COMPLETED")
print("=" * 70)