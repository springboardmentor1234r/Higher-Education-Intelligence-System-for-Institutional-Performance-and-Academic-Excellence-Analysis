from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# STEP 9.4 - QS 2025 RANKING ANALYSIS
# ============================================================

print("=" * 70)
print("STEP 9.4 - QS 2025 RANKING ANALYSIS")
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

qs = df[df["qs_present"] == True].copy()

print("QS 2025 data loaded.")
print(f"Universities with QS data: {len(qs)}")


# ============================================================
# 3. BASIC QS STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC QS 2025 STATISTICS")
print("=" * 70)

print(f"Universities             : {len(qs)}")
print(f"Countries represented    : {qs['country_name'].nunique()}")

print("\nQS Rank statistics:")

print(
    qs["qs_rank_2025"]
    .describe()
    .to_string()
)

print("\nQS Overall Score statistics:")

print(
    qs["qs_overall_score"]
    .describe()
    .to_string()
)


# ============================================================
# 4. TOP 20 QS UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("2. TOP 20 QS 2025 UNIVERSITIES")
print("=" * 70)

top20 = (
    qs.sort_values("qs_rank_2025")
    [
        [
            "qs_rank_2025",
            "university_name",
            "country_name",
            "qs_overall_score"
        ]
    ]
    .head(20)
)

print(top20.to_string(index=False))

top20.to_csv(
    EDA_DIR / "qs_2025_top_20_analysis.csv",
    index=False
)


# ============================================================
# 5. TOP 50 QS UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("3. TOP 50 QS 2025 UNIVERSITIES")
print("=" * 70)

top50 = (
    qs[
        qs["qs_rank_2025"] <= 50
    ]
    .sort_values("qs_rank_2025")
)

print(f"Universities ranked in top 50: {len(top50)}")

top50[
    [
        "qs_rank_2025",
        "university_name",
        "country_name",
        "qs_overall_score"
    ]
].to_csv(
    EDA_DIR / "qs_2025_top_50_analysis.csv",
    index=False
)


# ============================================================
# 6. QS RANKING TIERS
# ============================================================

print("\n" + "=" * 70)
print("4. QS 2025 RANKING TIERS")
print("=" * 70)


def rank_tier(rank):

    if pd.isna(rank):
        return "Unranked"

    if rank <= 50:
        return "Top 50"

    elif rank <= 100:
        return "51-100"

    elif rank <= 200:
        return "101-200"

    elif rank <= 500:
        return "201-500"

    else:
        return "501+"


qs["qs_rank_tier"] = qs["qs_rank_2025"].apply(rank_tier)

tier_summary = (
    qs["qs_rank_tier"]
    .value_counts()
    .reindex(
        [
            "Top 50",
            "51-100",
            "101-200",
            "201-500",
            "501+",
            "Unranked"
        ],
        fill_value=0
    )
    .reset_index()
)

tier_summary.columns = [
    "rank_tier",
    "university_count"
]

tier_summary["percentage"] = (
    tier_summary["university_count"]
    / len(qs)
    * 100
)

print(tier_summary.to_string(index=False))

tier_summary.to_csv(
    EDA_DIR / "qs_2025_rank_tiers.csv",
    index=False
)


# ============================================================
# 7. QS COUNTRY DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("5. QS 2025 UNIVERSITY DISTRIBUTION BY COUNTRY")
print("=" * 70)

country_qs = (
    qs.groupby("country_name")
    .agg(
        university_count=("university_id", "count"),
        average_score=("qs_overall_score", "mean"),
        best_rank=("qs_rank_2025", "min")
    )
    .reset_index()
    .sort_values(
        "university_count",
        ascending=False
    )
)

print(
    country_qs.head(20).to_string(index=False)
)

country_qs.to_csv(
    EDA_DIR / "qs_2025_country_distribution.csv",
    index=False
)


# ============================================================
# 8. QS COUNTRY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("6. QS 2025 COUNTRY PERFORMANCE")
print("=" * 70)

country_performance = country_qs[
    country_qs["university_count"] >= 5
].copy()

country_performance = country_performance.sort_values(
    "average_score",
    ascending=False
)

print(
    "Countries with at least 5 QS universities:"
)

print(
    country_performance.head(20).to_string(index=False)
)

country_performance.to_csv(
    EDA_DIR / "qs_2025_country_performance.csv",
    index=False
)


# ============================================================
# 9. QS REGION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("7. QS 2025 PERFORMANCE BY WORLD BANK REGION")
print("=" * 70)

region_qs = (
    qs.groupby("wb_region", dropna=False)
    .agg(
        university_count=("university_id", "count"),
        average_score=("qs_overall_score", "mean"),
        average_rank=("qs_rank_2025", "mean"),
        best_rank=("qs_rank_2025", "min")
    )
    .reset_index()
)

region_qs = region_qs.sort_values(
    "average_score",
    ascending=False
)

print(
    region_qs.to_string(index=False)
)

region_qs.to_csv(
    EDA_DIR / "qs_2025_region_analysis.csv",
    index=False
)


# ============================================================
# 10. QS INCOME GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. QS 2025 PERFORMANCE BY INCOME GROUP")
print("=" * 70)

income_qs = (
    qs.groupby("wb_income_group", dropna=False)
    .agg(
        university_count=("university_id", "count"),
        average_score=("qs_overall_score", "mean"),
        average_rank=("qs_rank_2025", "mean"),
        best_rank=("qs_rank_2025", "min")
    )
    .reset_index()
)

income_qs = income_qs.sort_values(
    "average_score",
    ascending=False
)

print(
    income_qs.to_string(index=False)
)

income_qs.to_csv(
    EDA_DIR / "qs_2025_income_group_analysis.csv",
    index=False
)


# ============================================================
# 11. QS INDICATOR ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("9. QS 2025 INDICATOR ANALYSIS")
print("=" * 70)

qs_indicators = [
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score"
]

indicator_summary = []

for column in qs_indicators:

    indicator_summary.append({
        "indicator": column,
        "available": qs[column].notna().sum(),
        "missing": qs[column].isna().sum(),
        "mean": qs[column].mean(),
        "median": qs[column].median(),
        "std": qs[column].std()
    })

indicator_summary = pd.DataFrame(indicator_summary)

print(
    indicator_summary.to_string(index=False)
)

indicator_summary.to_csv(
    EDA_DIR / "qs_2025_indicator_statistics.csv",
    index=False
)


# ============================================================
# 12. CORRELATION WITH QS OVERALL SCORE
# ============================================================

print("\n" + "=" * 70)
print("10. QS INDICATOR CORRELATION WITH OVERALL SCORE")
print("=" * 70)

correlations = []

for column in qs_indicators:

    valid = qs[
        [
            column,
            "qs_overall_score"
        ]
    ].dropna()

    correlation = valid[column].corr(
        valid["qs_overall_score"]
    )

    correlations.append({
        "indicator": column,
        "correlation_with_overall_score": correlation,
        "valid_observations": len(valid)
    })

correlations = pd.DataFrame(correlations)

correlations = correlations.sort_values(
    "correlation_with_overall_score",
    ascending=False
)

print(
    correlations.to_string(index=False)
)

correlations.to_csv(
    EDA_DIR / "qs_2025_indicator_correlations.csv",
    index=False
)


# ============================================================
# 13. TOP QS SCORE UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("11. UNIVERSITIES WITH HIGHEST QS OVERALL SCORES")
print("=" * 70)

top_score = (
    qs.sort_values(
        "qs_overall_score",
        ascending=False
    )
    [
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "qs_overall_score"
        ]
    ]
    .head(20)
)

print(
    top_score.to_string(index=False)
)

top_score.to_csv(
    EDA_DIR / "qs_2025_highest_scores.csv",
    index=False
)


# ============================================================
# 14. VISUALIZATION - QS SCORE DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("12. CREATING VISUALIZATIONS")
print("=" * 70)

plt.figure(figsize=(10, 6))

plt.hist(
    qs["qs_overall_score"].dropna(),
    bins=20
)

plt.xlabel("QS Overall Score")
plt.ylabel("Number of Universities")
plt.title("Distribution of QS 2025 Overall Scores")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "qs_2025_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "qs_2025_score_distribution.png"
)


# ============================================================
# 15. VISUALIZATION - RANK TIERS
# ============================================================

tier_plot = tier_summary[
    tier_summary["rank_tier"] != "Unranked"
]

plt.figure(figsize=(10, 6))

plt.bar(
    tier_plot["rank_tier"],
    tier_plot["university_count"]
)

plt.xlabel("QS Ranking Tier")
plt.ylabel("Number of Universities")
plt.title("QS 2025 Ranking Tier Distribution")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "qs_2025_rank_tiers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "qs_2025_rank_tiers.png"
)


# ============================================================
# 16. VISUALIZATION - TOP COUNTRIES
# ============================================================

country_plot = (
    country_qs
    .head(15)
    .sort_values("university_count")
)

plt.figure(figsize=(11, 7))

plt.barh(
    country_plot["country_name"],
    country_plot["university_count"]
)

plt.xlabel("Number of QS Universities")
plt.ylabel("Country")
plt.title("Top 15 Countries by QS 2025 University Count")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "qs_2025_top_countries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "qs_2025_top_countries.png"
)


# ============================================================
# 17. VISUALIZATION - INDICATOR CORRELATIONS
# ============================================================

correlation_plot = correlations.copy()

plt.figure(figsize=(11, 7))

plt.barh(
    correlation_plot["indicator"],
    correlation_plot["correlation_with_overall_score"]
)

plt.xlabel("Correlation")
plt.ylabel("QS Indicator")
plt.title(
    "Correlation Between QS Indicators and Overall Score"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "qs_2025_indicator_correlations.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved:",
    FIGURE_DIR / "qs_2025_indicator_correlations.png"
)


# ============================================================
# 18. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.4 SUMMARY")
print("=" * 70)

print(f"\nQS universities       : {len(qs)}")
print(f"Countries represented : {qs['country_name'].nunique()}")

print("\nTop QS university:")

print(
    qs.sort_values("qs_rank_2025")
    [
        [
            "qs_rank_2025",
            "university_name",
            "country_name",
            "qs_overall_score"
        ]
    ]
    .head(1)
    .to_string(index=False)
)

print("\nTop QS country by university count:")

print(
    country_qs.head(1).to_string(index=False)
)

print("\nHighest correlation with QS overall score:")

print(
    correlations.head(1).to_string(index=False)
)

print("\nOutput directory:")
print(EDA_DIR)

print("\nFigure directory:")
print(FIGURE_DIR)

print("\n" + "=" * 70)
print("STEP 9.4 COMPLETED")
print("=" * 70)