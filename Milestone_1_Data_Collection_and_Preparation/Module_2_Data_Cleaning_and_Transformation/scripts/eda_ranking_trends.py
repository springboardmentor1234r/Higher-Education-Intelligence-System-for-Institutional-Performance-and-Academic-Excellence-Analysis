import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# STEP 9.7 - RANKING TREND ANALYSIS
# THE 2023 -> THE 2024
# ============================================================

print("=" * 70)
print("STEP 9.7 - RANKING TREND ANALYSIS")
print("THE 2023 -> THE 2024")
print("=" * 70)


# ============================================================
# PATHS
# ============================================================

INPUT_FILE = Path(
    "data/processed/university_integrated_worldbank_education.csv"
)

EDA_DIR = Path("data/eda")
FIG_DIR = Path("reports/figures")

EDA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING FINAL ANALYTICAL DATASET")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "university_id",
    "university_name",
    "country_name",
    "wb_region",
    "wb_income_group",
    "the_rank_2023",
    "the_rank_2024",
    "the_overall_score_2023",
    "the_overall_score_2024",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nERROR: Missing required columns:")
    for col in missing_columns:
        print(f"  - {col}")
    raise SystemExit(1)

print("Required columns: PASS")


# ============================================================
# CONVERT RANKS AND SCORES TO NUMERIC
# ============================================================

df["the_rank_2023_num"] = pd.to_numeric(
    df["the_rank_2023"],
    errors="coerce"
)

df["the_rank_2024_num"] = pd.to_numeric(
    df["the_rank_2024"],
    errors="coerce"
)

df["the_score_2023_num"] = pd.to_numeric(
    df["the_overall_score_2023"],
    errors="coerce"
)

df["the_score_2024_num"] = pd.to_numeric(
    df["the_overall_score_2024"],
    errors="coerce"
)


# ============================================================
# 1. BASIC COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("1. THE 2023 -> 2024 COVERAGE")
print("=" * 70)

rank_2023_count = df["the_rank_2023_num"].notna().sum()
rank_2024_count = df["the_rank_2024_num"].notna().sum()

rank_overlap = df[
    df["the_rank_2023_num"].notna()
    & df["the_rank_2024_num"].notna()
].copy()

score_2023_count = df["the_score_2023_num"].notna().sum()
score_2024_count = df["the_score_2024_num"].notna().sum()

score_overlap = df[
    df["the_score_2023_num"].notna()
    & df["the_score_2024_num"].notna()
].copy()

print(f"Universities with numeric THE 2023 rank: {rank_2023_count}")
print(f"Universities with numeric THE 2024 rank: {rank_2024_count}")
print(f"Universities with numeric ranks in BOTH years: {len(rank_overlap)}")

print()

print(f"Universities with THE 2023 score: {score_2023_count}")
print(f"Universities with THE 2024 score: {score_2024_count}")
print(f"Universities with scores in BOTH years: {len(score_overlap)}")


# ============================================================
# 2. RANK OVERLAP
# ============================================================

print("\n" + "=" * 70)
print("2. THE 2023 -> 2024 RANK OVERLAP")
print("=" * 70)

rank_overlap["rank_change"] = (
    rank_overlap["the_rank_2023_num"]
    - rank_overlap["the_rank_2024_num"]
)

rank_overlap["absolute_rank_change"] = (
    rank_overlap["rank_change"].abs()
)

rank_overlap["rank_status"] = np.select(
    [
        rank_overlap["rank_change"] > 0,
        rank_overlap["rank_change"] < 0,
        rank_overlap["rank_change"] == 0,
    ],
    [
        "Improved",
        "Declined",
        "Stable",
    ],
    default="Unknown"
)

print(
    f"Average 2023 rank: "
    f"{rank_overlap['the_rank_2023_num'].mean():.2f}"
)

print(
    f"Average 2024 rank: "
    f"{rank_overlap['the_rank_2024_num'].mean():.2f}"
)

print(
    f"Average rank change: "
    f"{rank_overlap['rank_change'].mean():.2f}"
)

print(
    f"Median absolute rank change: "
    f"{rank_overlap['absolute_rank_change'].median():.2f}"
)

print(
    f"Mean absolute rank change: "
    f"{rank_overlap['absolute_rank_change'].mean():.2f}"
)


# ============================================================
# STATUS COUNTS
# ============================================================

status_counts = (
    rank_overlap["rank_status"]
    .value_counts()
)

print("\nRank status:")

for status, count in status_counts.items():
    percentage = count / len(rank_overlap) * 100

    print(
        f"{status:10s}: "
        f"{count:4d} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# SAVE RANK OVERLAP
# ============================================================

rank_overlap_output = rank_overlap[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_region",
        "wb_income_group",
        "the_rank_2023_num",
        "the_rank_2024_num",
        "rank_change",
        "absolute_rank_change",
        "rank_status",
    ]
].sort_values(
    "rank_change",
    ascending=False
)

rank_overlap_output.to_csv(
    EDA_DIR / "the_2023_2024_rank_overlap.csv",
    index=False
)


# ============================================================
# 3. TOP RANK IMPROVEMENTS
# ============================================================

print("\n" + "=" * 70)
print("3. TOP RANK IMPROVEMENTS")
print("=" * 70)

improvements = rank_overlap[
    rank_overlap["rank_change"] > 0
].sort_values(
    "rank_change",
    ascending=False
)

print(
    f"Universities that improved: "
    f"{len(improvements)}"
)

if len(improvements) > 0:

    print("\nTop 20 improvements:")

    print(
        improvements[
            [
                "university_name",
                "country_name",
                "the_rank_2023_num",
                "the_rank_2024_num",
                "rank_change",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


improvements_output = improvements[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_region",
        "wb_income_group",
        "the_rank_2023_num",
        "the_rank_2024_num",
        "rank_change",
        "absolute_rank_change",
    ]
]

improvements_output.to_csv(
    EDA_DIR / "the_rank_improvements.csv",
    index=False
)


# ============================================================
# 4. TOP RANK DECLINES
# ============================================================

print("\n" + "=" * 70)
print("4. TOP RANK DECLINES")
print("=" * 70)

declines = rank_overlap[
    rank_overlap["rank_change"] < 0
].sort_values(
    "rank_change",
    ascending=True
)

print(
    f"Universities that declined: "
    f"{len(declines)}"
)

if len(declines) > 0:

    print("\nTop 20 declines:")

    print(
        declines[
            [
                "university_name",
                "country_name",
                "the_rank_2023_num",
                "the_rank_2024_num",
                "rank_change",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


declines_output = declines[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_region",
        "wb_income_group",
        "the_rank_2023_num",
        "the_rank_2024_num",
        "rank_change",
        "absolute_rank_change",
    ]
]

declines_output.to_csv(
    EDA_DIR / "the_rank_declines.csv",
    index=False
)


# ============================================================
# 5. STABLE UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("5. STABLE UNIVERSITIES")
print("=" * 70)

stable = rank_overlap[
    rank_overlap["rank_change"] == 0
].copy()

print(
    f"Universities with unchanged numeric rank: "
    f"{len(stable)}"
)

stable_output = stable[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_region",
        "wb_income_group",
        "the_rank_2023_num",
        "the_rank_2024_num",
    ]
].sort_values(
    "the_rank_2024_num"
)

stable_output.to_csv(
    EDA_DIR / "the_stable_universities.csv",
    index=False
)


# ============================================================
# 6. TOP STABLE UNIVERSITIES
# ============================================================

print("\n" + "=" * 70)
print("6. TOP STABLE UNIVERSITIES")
print("=" * 70)

top_stable = stable_output.head(20)

if len(top_stable) > 0:

    print(
        top_stable.to_string(index=False)
    )

top_stable.to_csv(
    EDA_DIR / "the_top_stable_universities.csv",
    index=False
)


# ============================================================
# 7. SCORE CHANGES
# ============================================================

print("\n" + "=" * 70)
print("7. THE OVERALL SCORE CHANGES")
print("=" * 70)

score_overlap["score_change"] = (
    score_overlap["the_score_2024_num"]
    - score_overlap["the_score_2023_num"]
)

score_overlap["absolute_score_change"] = (
    score_overlap["score_change"].abs()
)

print(
    f"Average 2023 score: "
    f"{score_overlap['the_score_2023_num'].mean():.2f}"
)

print(
    f"Average 2024 score: "
    f"{score_overlap['the_score_2024_num'].mean():.2f}"
)

print(
    f"Average score change: "
    f"{score_overlap['score_change'].mean():.2f}"
)

print(
    f"Median score change: "
    f"{score_overlap['score_change'].median():.2f}"
)

print(
    f"Mean absolute score change: "
    f"{score_overlap['absolute_score_change'].mean():.2f}"
)


score_overlap_output = score_overlap[
    [
        "university_id",
        "university_name",
        "country_name",
        "wb_region",
        "wb_income_group",
        "the_score_2023_num",
        "the_score_2024_num",
        "score_change",
        "absolute_score_change",
    ]
].sort_values(
    "score_change",
    ascending=False
)

score_overlap_output.to_csv(
    EDA_DIR / "the_2023_2024_score_overlap.csv",
    index=False
)


# ============================================================
# 8. COUNTRY-LEVEL TREND
# ============================================================

print("\n" + "=" * 70)
print("8. COUNTRY-LEVEL RANKING TREND")
print("=" * 70)

country_trend = (
    rank_overlap
    .groupby("country_name")
    .agg(
        universities=("university_id", "count"),
        avg_rank_2023=("the_rank_2023_num", "mean"),
        avg_rank_2024=("the_rank_2024_num", "mean"),
        avg_rank_change=("rank_change", "mean"),
        avg_absolute_rank_change=(
            "absolute_rank_change",
            "mean"
        ),
    )
    .reset_index()
)

# Minimum overlap of 3 universities
country_trend = country_trend[
    country_trend["universities"] >= 3
].copy()

country_trend = country_trend.sort_values(
    "avg_rank_change",
    ascending=False
)

print(
    "\nCountries with at least 3 universities "
    "having numeric ranks in both years:"
)

print(
    country_trend.head(20).to_string(index=False)
)

country_trend.to_csv(
    EDA_DIR / "the_country_trends.csv",
    index=False
)


# ============================================================
# 9. REGION-LEVEL TREND
# ============================================================

print("\n" + "=" * 70)
print("9. REGION-LEVEL RANKING TREND")
print("=" * 70)

region_trend = (
    rank_overlap
    .dropna(subset=["wb_region"])
    .groupby("wb_region")
    .agg(
        universities=("university_id", "count"),
        avg_rank_2023=("the_rank_2023_num", "mean"),
        avg_rank_2024=("the_rank_2024_num", "mean"),
        avg_rank_change=("rank_change", "mean"),
        avg_absolute_rank_change=(
            "absolute_rank_change",
            "mean"
        ),
    )
    .reset_index()
)

region_trend = region_trend.sort_values(
    "avg_rank_change",
    ascending=False
)

print(
    region_trend.to_string(index=False)
)

region_trend.to_csv(
    EDA_DIR / "the_region_trends.csv",
    index=False
)


# ============================================================
# 10. INCOME-GROUP TREND
# ============================================================

print("\n" + "=" * 70)
print("10. INCOME-GROUP RANKING TREND")
print("=" * 70)

income_trend = (
    rank_overlap
    .dropna(subset=["wb_income_group"])
    .groupby("wb_income_group")
    .agg(
        universities=("university_id", "count"),
        avg_rank_2023=("the_rank_2023_num", "mean"),
        avg_rank_2024=("the_rank_2024_num", "mean"),
        avg_rank_change=("rank_change", "mean"),
        avg_absolute_rank_change=(
            "absolute_rank_change",
            "mean"
        ),
    )
    .reset_index()
)

income_trend = income_trend.sort_values(
    "avg_rank_change",
    ascending=False
)

print(
    income_trend.to_string(index=False)
)

income_trend.to_csv(
    EDA_DIR / "the_income_trends.csv",
    index=False
)


# ============================================================
# 11. FIGURE 1 - RANK SCATTER
# ============================================================

print("\n" + "=" * 70)
print("11. CREATING VISUALIZATIONS")
print("=" * 70)

plt.figure(figsize=(9, 7))

plt.scatter(
    rank_overlap["the_rank_2023_num"],
    rank_overlap["the_rank_2024_num"],
    alpha=0.65
)

max_rank = max(
    rank_overlap["the_rank_2023_num"].max(),
    rank_overlap["the_rank_2024_num"].max()
)

plt.plot(
    [1, max_rank],
    [1, max_rank],
    linestyle="--"
)

plt.xlabel("THE 2023 Rank")
plt.ylabel("THE 2024 Rank")
plt.title("THE 2023 vs THE 2024 University Rankings")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "the_2023_vs_2024_rank_scatter.png",
    dpi=300
)

plt.close()


# ============================================================
# 12. FIGURE 2 - RANK CHANGE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    rank_overlap["rank_change"],
    bins=25
)

plt.axvline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Rank Change (2023 Rank - 2024 Rank)"
)

plt.ylabel("Number of Universities")

plt.title(
    "Distribution of THE Rank Changes: 2023 → 2024"
)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "the_rank_change_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 13. FIGURE 3 - SCORE CHANGE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    score_overlap["score_change"],
    bins=30
)

plt.axvline(
    0,
    linestyle="--"
)

plt.xlabel(
    "THE Overall Score Change (2024 - 2023)"
)

plt.ylabel("Number of Universities")

plt.title(
    "Distribution of THE Overall Score Changes: 2023 → 2024"
)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "the_score_change_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 14. FIGURE 4 - TOP RANK CHANGES
# ============================================================

top_improvements = improvements.head(10).copy()

top_declines = declines.head(10).copy()

combined_changes = pd.concat(
    [
        top_improvements,
        top_declines
    ],
    ignore_index=True
)

if len(combined_changes) > 0:

    combined_changes = combined_changes.sort_values(
        "rank_change"
    )

    plt.figure(figsize=(10, 8))

    plt.barh(
        combined_changes["university_name"],
        combined_changes["rank_change"]
    )

    plt.axvline(
        0,
        linestyle="--"
    )

    plt.xlabel(
        "Rank Change (Positive = Improvement)"
    )

    plt.ylabel("University")

    plt.title(
        "Largest THE Ranking Changes: 2023 → 2024"
    )

    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "the_top_rank_changes.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 15. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.7 SUMMARY")
print("=" * 70)

print(f"Total universities: {len(df)}")

print(
    f"Numeric rank overlap: "
    f"{len(rank_overlap)}"
)

print(
    f"Improved: "
    f"{(rank_overlap['rank_change'] > 0).sum()}"
)

print(
    f"Declined: "
    f"{(rank_overlap['rank_change'] < 0).sum()}"
)

print(
    f"Stable: "
    f"{(rank_overlap['rank_change'] == 0).sum()}"
)

print(
    f"Average rank change: "
    f"{rank_overlap['rank_change'].mean():.2f}"
)

print(
    f"Score overlap: "
    f"{len(score_overlap)}"
)

print(
    f"Average score change: "
    f"{score_overlap['score_change'].mean():.2f}"
)


# ============================================================
# OUTPUT FILES
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

output_files = [
    "the_2023_2024_rank_overlap.csv",
    "the_2023_2024_score_overlap.csv",
    "the_rank_improvements.csv",
    "the_rank_declines.csv",
    "the_stable_universities.csv",
    "the_top_stable_universities.csv",
    "the_country_trends.csv",
    "the_region_trends.csv",
    "the_income_trends.csv",
]

for file_name in output_files:
    print(f"data/eda/{file_name}")

print()

figure_files = [
    "the_2023_vs_2024_rank_scatter.png",
    "the_rank_change_distribution.png",
    "the_score_change_distribution.png",
    "the_top_rank_changes.png",
]

for file_name in figure_files:
    print(f"reports/figures/{file_name}")


print("\n" + "=" * 70)
print("STEP 9.7 COMPLETED SUCCESSFULLY")
print("=" * 70)