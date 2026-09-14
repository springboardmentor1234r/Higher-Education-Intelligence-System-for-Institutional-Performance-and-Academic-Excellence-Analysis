import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("STEP 9.6 - QS 2025 VS THE 2024 COMPARISON")
print("=" * 70)

# ==============================================================
# PATHS
# ==============================================================

INPUT_FILE = Path(
    "data/processed/university_integrated_worldbank_education.csv"
)

OUTPUT_DIR = Path("data/eda")
FIGURE_DIR = Path("reports/figures")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================
# LOAD DATA
# ==============================================================

print("\nLoading final analytical dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Rows       : {len(df)}")
print(f"Columns    : {len(df.columns)}")


# ==============================================================
# NUMERIC CONVERSION
# ==============================================================

df["qs_rank_2025"] = pd.to_numeric(
    df["qs_rank_2025"], errors="coerce"
)

df["the_rank_2024"] = pd.to_numeric(
    df["the_rank_2024"], errors="coerce"
)

df["qs_overall_score"] = pd.to_numeric(
    df["qs_overall_score"], errors="coerce"
)

df["the_overall_score_2024"] = pd.to_numeric(
    df["the_overall_score_2024"], errors="coerce"
)


# ==============================================================
# 1. BASIC OVERLAP
# ==============================================================

print("\n" + "=" * 70)
print("1. QS VS THE BASIC OVERLAP")
print("=" * 70)

qs_rank_count = df["qs_rank_2025"].notna().sum()
the_rank_count = df["the_rank_2024"].notna().sum()

qs_score_count = df["qs_overall_score"].notna().sum()
the_score_count = df["the_overall_score_2024"].notna().sum()

rank_overlap = df[
    df["qs_rank_2025"].notna()
    & df["the_rank_2024"].notna()
].copy()

score_overlap = df[
    df["qs_overall_score"].notna()
    & df["the_overall_score_2024"].notna()
].copy()

print(f"Universities with QS numeric rank       : {qs_rank_count}")
print(f"Universities with THE numeric rank      : {the_rank_count}")
print(f"Universities with both numeric ranks    : {len(rank_overlap)}")

print(f"\nUniversities with QS overall score       : {qs_score_count}")
print(f"Universities with THE overall score      : {the_score_count}")
print(f"Universities with both overall scores   : {len(score_overlap)}")


# ==============================================================
# 2. RANK CORRELATION
# ==============================================================

print("\n" + "=" * 70)
print("2. QS RANK VS THE RANK CORRELATION")
print("=" * 70)

if len(rank_overlap) >= 2:

    pearson_rank_corr = rank_overlap[
        ["qs_rank_2025", "the_rank_2024"]
    ].corr(method="pearson").iloc[0, 1]

    spearman_rank_corr = rank_overlap[
        ["qs_rank_2025", "the_rank_2024"]
    ].corr(method="spearman").iloc[0, 1]

    print(
        f"Pearson correlation  : {pearson_rank_corr:.4f}"
    )

    print(
        f"Spearman correlation : {spearman_rank_corr:.4f}"
    )

    print(
        "\nSpearman correlation is preferred here because "
        "ranking positions are ordinal."
    )

else:
    pearson_rank_corr = np.nan
    spearman_rank_corr = np.nan

    print("Not enough overlapping universities.")


# ==============================================================
# 3. OVERALL SCORE CORRELATION
# ==============================================================

print("\n" + "=" * 70)
print("3. QS OVERALL SCORE VS THE OVERALL SCORE")
print("=" * 70)

if len(score_overlap) >= 2:

    pearson_score_corr = score_overlap[
        ["qs_overall_score", "the_overall_score_2024"]
    ].corr(method="pearson").iloc[0, 1]

    spearman_score_corr = score_overlap[
        ["qs_overall_score", "the_overall_score_2024"]
    ].corr(method="spearman").iloc[0, 1]

    print(
        f"Pearson correlation  : {pearson_score_corr:.4f}"
    )

    print(
        f"Spearman correlation : {spearman_score_corr:.4f}"
    )

else:
    pearson_score_corr = np.nan
    spearman_score_corr = np.nan

    print("Not enough overlapping universities.")


# ==============================================================
# 4. RANK DIFFERENCE
# ==============================================================

print("\n" + "=" * 70)
print("4. RANK DIFFERENCE ANALYSIS")
print("=" * 70)

if len(rank_overlap) > 0:

    # Positive value:
    # QS rank number is greater than THE rank number
    # Therefore THE ranks the university better.
    rank_overlap["rank_difference"] = (
        rank_overlap["qs_rank_2025"]
        - rank_overlap["the_rank_2024"]
    )

    rank_overlap["absolute_rank_difference"] = (
        rank_overlap["rank_difference"].abs()
    )

    print(
        f"Average QS rank       : "
        f"{rank_overlap['qs_rank_2025'].mean():.2f}"
    )

    print(
        f"Average THE rank      : "
        f"{rank_overlap['the_rank_2024'].mean():.2f}"
    )

    print(
        f"Average rank difference: "
        f"{rank_overlap['rank_difference'].mean():.2f}"
    )

    print(
        f"Median absolute difference: "
        f"{rank_overlap['absolute_rank_difference'].median():.2f}"
    )

    print(
        f"Mean absolute difference: "
        f"{rank_overlap['absolute_rank_difference'].mean():.2f}"
    )


# ==============================================================
# 5. QS RANKS BETTER THAN THE
# ==============================================================

print("\n" + "=" * 70)
print("5. UNIVERSITIES RANKED BETTER BY QS")
print("=" * 70)

qs_better = rank_overlap[
    rank_overlap["rank_difference"] < 0
].copy()

qs_better = qs_better.sort_values(
    "rank_difference"
)

print(
    f"Universities ranked better by QS: {len(qs_better)}"
)

print("\nTop 20 largest QS advantages:")

print(
    qs_better[
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "the_rank_2024",
            "rank_difference"
        ]
    ].head(20).to_string(index=False)
)


# ==============================================================
# 6. THE RANKS BETTER THAN QS
# ==============================================================

print("\n" + "=" * 70)
print("6. UNIVERSITIES RANKED BETTER BY THE")
print("=" * 70)

the_better = rank_overlap[
    rank_overlap["rank_difference"] > 0
].copy()

the_better = the_better.sort_values(
    "rank_difference",
    ascending=False
)

print(
    f"Universities ranked better by THE: {len(the_better)}"
)

print("\nTop 20 largest THE advantages:")

print(
    the_better[
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "the_rank_2024",
            "rank_difference"
        ]
    ].head(20).to_string(index=False)
)


# ==============================================================
# 7. UNIVERSITIES WITH CLOSE RANKINGS
# ==============================================================

print("\n" + "=" * 70)
print("7. UNIVERSITIES WITH CLOSE QS AND THE RANKINGS")
print("=" * 70)

close_rankings = rank_overlap[
    rank_overlap["absolute_rank_difference"] <= 10
].copy()

close_rankings = close_rankings.sort_values(
    "absolute_rank_difference"
)

print(
    f"Universities with rank difference <= 10: "
    f"{len(close_rankings)}"
)

print(
    close_rankings[
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "the_rank_2024",
            "rank_difference",
            "absolute_rank_difference"
        ]
    ].head(20).to_string(index=False)
)


# ==============================================================
# 8. TOP UNIVERSITIES IN BOTH RANKINGS
# ==============================================================

print("\n" + "=" * 70)
print("8. TOP UNIVERSITIES IN BOTH RANKINGS")
print("=" * 70)

top_both = rank_overlap[
    (rank_overlap["qs_rank_2025"] <= 50)
    & (rank_overlap["the_rank_2024"] <= 50)
].copy()

top_both = top_both.sort_values(
    ["qs_rank_2025", "the_rank_2024"]
)

print(
    f"Universities in top 50 of both rankings: "
    f"{len(top_both)}"
)

print(
    top_both[
        [
            "university_name",
            "country_name",
            "qs_rank_2025",
            "the_rank_2024",
            "qs_overall_score",
            "the_overall_score_2024"
        ]
    ].to_string(index=False)
)


# ==============================================================
# 9. COUNTRY-LEVEL COMPARISON
# ==============================================================

print("\n" + "=" * 70)
print("9. COUNTRY-LEVEL QS VS THE COMPARISON")
print("=" * 70)

if len(rank_overlap) > 0:

    country_comparison = (
        rank_overlap
        .groupby("country_name")
        .agg(
            overlapping_universities=("university_id", "count"),
            average_qs_rank=("qs_rank_2025", "mean"),
            average_the_rank=("the_rank_2024", "mean"),
            average_rank_difference=("rank_difference", "mean"),
            median_rank_difference=("rank_difference", "median"),
            average_absolute_difference=(
                "absolute_rank_difference",
                "mean"
            )
        )
        .reset_index()
    )

    country_comparison = country_comparison[
        country_comparison["overlapping_universities"] >= 3
    ].copy()

    country_comparison = country_comparison.sort_values(
        "average_absolute_difference"
    )

    print(
        "\nCountries with at least 3 overlapping universities:"
    )

    print(
        country_comparison.head(20).to_string(index=False)
    )

else:
    country_comparison = pd.DataFrame()


# ==============================================================
# 10. REGION-LEVEL COMPARISON
# ==============================================================

print("\n" + "=" * 70)
print("10. WORLD BANK REGION COMPARISON")
print("=" * 70)

if len(rank_overlap) > 0:

    region_comparison = (
        rank_overlap
        .groupby("wb_region")
        .agg(
            overlapping_universities=("university_id", "count"),
            average_qs_rank=("qs_rank_2025", "mean"),
            average_the_rank=("the_rank_2024", "mean"),
            average_rank_difference=("rank_difference", "mean"),
            average_absolute_difference=(
                "absolute_rank_difference",
                "mean"
            )
        )
        .reset_index()
    )

    print(
        region_comparison.to_string(index=False)
    )

else:
    region_comparison = pd.DataFrame()


# ==============================================================
# 11. INCOME GROUP COMPARISON
# ==============================================================

print("\n" + "=" * 70)
print("11. INCOME GROUP COMPARISON")
print("=" * 70)

if len(rank_overlap) > 0:

    income_comparison = (
        rank_overlap
        .groupby("wb_income_group")
        .agg(
            overlapping_universities=("university_id", "count"),
            average_qs_rank=("qs_rank_2025", "mean"),
            average_the_rank=("the_rank_2024", "mean"),
            average_rank_difference=("rank_difference", "mean"),
            average_absolute_difference=(
                "absolute_rank_difference",
                "mean"
            )
        )
        .reset_index()
    )

    print(
        income_comparison.to_string(index=False)
    )

else:
    income_comparison = pd.DataFrame()


# ==============================================================
# 12. SCORE DIFFERENCE
# ==============================================================

print("\n" + "=" * 70)
print("12. OVERALL SCORE DIFFERENCE")
print("=" * 70)

if len(score_overlap) > 0:

    score_overlap["score_difference"] = (
        score_overlap["qs_overall_score"]
        - score_overlap["the_overall_score_2024"]
    )

    score_overlap["absolute_score_difference"] = (
        score_overlap["score_difference"].abs()
    )

    print(
        f"Average QS score       : "
        f"{score_overlap['qs_overall_score'].mean():.2f}"
    )

    print(
        f"Average THE score      : "
        f"{score_overlap['the_overall_score_2024'].mean():.2f}"
    )

    print(
        f"Average score difference: "
        f"{score_overlap['score_difference'].mean():.2f}"
    )

    print(
        f"Average absolute score difference: "
        f"{score_overlap['absolute_score_difference'].mean():.2f}"
    )


# ==============================================================
# 13. SAVE CSV FILES
# ==============================================================

print("\n" + "=" * 70)
print("13. SAVING COMPARISON DATA")
print("=" * 70)

rank_overlap_output = OUTPUT_DIR / "qs_2025_the_2024_rank_overlap.csv"
score_overlap_output = OUTPUT_DIR / "qs_2025_the_2024_score_overlap.csv"
qs_better_output = OUTPUT_DIR / "qs_better_than_the.csv"
the_better_output = OUTPUT_DIR / "the_better_than_qs.csv"
close_output = OUTPUT_DIR / "qs_the_close_rankings.csv"
top_both_output = OUTPUT_DIR / "top_universities_both_rankings.csv"
country_output = OUTPUT_DIR / "qs_the_country_comparison.csv"
region_output = OUTPUT_DIR / "qs_the_region_comparison.csv"
income_output = OUTPUT_DIR / "qs_the_income_comparison.csv"

rank_overlap.to_csv(
    rank_overlap_output,
    index=False
)

score_overlap.to_csv(
    score_overlap_output,
    index=False
)

qs_better.to_csv(
    qs_better_output,
    index=False
)

the_better.to_csv(
    the_better_output,
    index=False
)

close_rankings.to_csv(
    close_output,
    index=False
)

top_both.to_csv(
    top_both_output,
    index=False
)

if not country_comparison.empty:
    country_comparison.to_csv(
        country_output,
        index=False
    )

if not region_comparison.empty:
    region_comparison.to_csv(
        region_output,
        index=False
    )

if not income_comparison.empty:
    income_comparison.to_csv(
        income_output,
        index=False
    )

print("Saved comparison CSV files.")


# ==============================================================
# 14. VISUALIZATION - RANK SCATTER
# ==============================================================

print("\n" + "=" * 70)
print("14. CREATING VISUALIZATIONS")
print("=" * 70)

if len(rank_overlap) >= 2:

    plt.figure(figsize=(10, 7))

    plt.scatter(
        rank_overlap["qs_rank_2025"],
        rank_overlap["the_rank_2024"],
        alpha=0.7
    )

    max_rank = max(
        rank_overlap["qs_rank_2025"].max(),
        rank_overlap["the_rank_2024"].max()
    )

    plt.plot(
        [1, max_rank],
        [1, max_rank],
        linestyle="--"
    )

    plt.xlabel("QS 2025 Rank")
    plt.ylabel("THE 2024 Rank")
    plt.title("QS 2025 vs THE 2024 University Rankings")

    plt.tight_layout()

    rank_scatter_file = (
        FIGURE_DIR / "qs_vs_the_rank_scatter.png"
    )

    plt.savefig(
        rank_scatter_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {rank_scatter_file}")


# ==============================================================
# 15. RANK DIFFERENCE DISTRIBUTION
# ==============================================================

if len(rank_overlap) > 0:

    plt.figure(figsize=(10, 6))

    plt.hist(
        rank_overlap["rank_difference"],
        bins=20
    )

    plt.axvline(
        0,
        linestyle="--"
    )

    plt.xlabel("QS Rank - THE Rank")
    plt.ylabel("Number of Universities")
    plt.title("Distribution of QS vs THE Rank Differences")

    plt.tight_layout()

    difference_file = (
        FIGURE_DIR / "qs_the_rank_difference_distribution.png"
    )

    plt.savefig(
        difference_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {difference_file}")


# ==============================================================
# 16. SCORE SCATTER
# ==============================================================

if len(score_overlap) >= 2:

    plt.figure(figsize=(10, 7))

    plt.scatter(
        score_overlap["qs_overall_score"],
        score_overlap["the_overall_score_2024"],
        alpha=0.6
    )

    plt.xlabel("QS 2025 Overall Score")
    plt.ylabel("THE 2024 Overall Score")
    plt.title("QS 2025 vs THE 2024 Overall Scores")

    plt.tight_layout()

    score_scatter_file = (
        FIGURE_DIR / "qs_vs_the_score_scatter.png"
    )

    plt.savefig(
        score_scatter_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {score_scatter_file}")


# ==============================================================
# 17. SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("STEP 9.6 SUMMARY")
print("=" * 70)

print(f"\nQS numeric ranks          : {qs_rank_count}")
print(f"THE numeric ranks         : {the_rank_count}")
print(f"Both numeric ranks        : {len(rank_overlap)}")

print(f"\nQS overall scores         : {qs_score_count}")
print(f"THE overall scores        : {the_score_count}")
print(f"Both overall scores       : {len(score_overlap)}")

if len(rank_overlap) >= 2:
    print(
        f"\nSpearman rank correlation : "
        f"{spearman_rank_corr:.4f}"
    )

if len(score_overlap) >= 2:
    print(
        f"Spearman score correlation: "
        f"{spearman_score_corr:.4f}"
    )

print(
    f"\nQS ranks better            : {len(qs_better)}"
)

print(
    f"THE ranks better           : {len(the_better)}"
)

print(
    f"Close rankings (<=10)     : {len(close_rankings)}"
)

print(
    f"Top 50 in both             : {len(top_both)}"
)

print("\nOutput directory:")
print(OUTPUT_DIR.resolve())

print("\nFigure directory:")
print(FIGURE_DIR.resolve())

print("\n" + "=" * 70)
print("STEP 9.6 COMPLETED")
print("=" * 70)