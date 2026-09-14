import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("STEP 9.7 V2 - CORRECTED THE 2023 -> 2024 RANKING TREND")
print("=" * 70)

# ==============================================================
# PATHS
# ==============================================================

INPUT_FILE = "data/processed/university_integrated_worldbank_education.csv"

EDA_DIR = "data/eda"
FIG_DIR = "reports/figures"

os.makedirs(EDA_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# ==============================================================
# LOAD DATA
# ==============================================================

print("\n" + "=" * 70)
print("LOADING FINAL ANALYTICAL DATASET")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")

required_columns = [
    "university_id",
    "university_name",
    "country_name",
    "the_rank_2023",
    "the_rank_2024",
    "the_overall_score_2023",
    "the_overall_score_2024"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nERROR - Missing required columns:")
    print(missing_columns)
    raise SystemExit

print("Required columns: PASS")

# ==============================================================
# NUMERIC CONVERSION
# ==============================================================

df["the_rank_2023_numeric"] = pd.to_numeric(
    df["the_rank_2023"],
    errors="coerce"
)

df["the_rank_2024_numeric"] = pd.to_numeric(
    df["the_rank_2024"],
    errors="coerce"
)

df["the_score_2023_numeric"] = pd.to_numeric(
    df["the_overall_score_2023"],
    errors="coerce"
)

df["the_score_2024_numeric"] = pd.to_numeric(
    df["the_overall_score_2024"],
    errors="coerce"
)

# ==============================================================
# STEP 1 - IDENTIFY EXACT VS BANDED THE 2023 RANKS
# ==============================================================

print("\n" + "=" * 70)
print("1. THE 2023 RANK REPRESENTATION")
print("=" * 70)

# Known lower bounds used for THE ranking bands
band_lower_bounds = [
    201,
    251,
    301,
    351,
    401,
    501,
    601,
    801,
    1001,
    1201,
    1501
]

df["the_2023_is_banded"] = (
    df["the_rank_2023_numeric"]
    .isin(band_lower_bounds)
)

df["the_2023_rank_type"] = np.where(
    df["the_rank_2023_numeric"].isna(),
    "Missing",
    np.where(
        df["the_2023_is_banded"],
        "Banded",
        "Exact"
    )
)

print("\nTHE 2023 rank representation:")

print(
    df["the_2023_rank_type"]
    .value_counts(dropna=False)
)

# ==============================================================
# SAVE RANK REPRESENTATION
# ==============================================================

rank_representation = (
    df[
        [
            "university_id",
            "university_name",
            "the_rank_2023",
            "the_rank_2023_numeric",
            "the_2023_rank_type"
        ]
    ]
    .sort_values(
        ["the_2023_rank_type", "the_rank_2023_numeric"]
    )
)

rank_representation_file = os.path.join(
    EDA_DIR,
    "the_2023_rank_representation_v2.csv"
)

rank_representation.to_csv(
    rank_representation_file,
    index=False
)

print(
    f"\nSaved: {rank_representation_file}"
)

# ==============================================================
# STEP 2 - EXACT RANK OVERLAP
# ==============================================================

print("\n" + "=" * 70)
print("2. EXACT THE 2023 -> 2024 RANK OVERLAP")
print("=" * 70)

exact_rank_df = df[
    (df["the_rank_2023_numeric"].notna()) &
    (df["the_rank_2024_numeric"].notna()) &
    (~df["the_2023_is_banded"])
].copy()

print(
    f"Universities with exact THE 2023 rank: "
    f"{(~df['the_2023_is_banded'] & df['the_rank_2023_numeric'].notna()).sum()}"
)

print(
    f"Universities with exact THE 2024 rank: "
    f"{df['the_rank_2024_numeric'].notna().sum()}"
)

print(
    f"Universities with exact ranks in BOTH years: "
    f"{len(exact_rank_df)}"
)

# ==============================================================
# STEP 3 - CALCULATE EXACT RANK CHANGE
# ==============================================================

print("\n" + "=" * 70)
print("3. EXACT RANK CHANGE")
print("=" * 70)

# Positive = improvement
# Negative = decline

exact_rank_df["rank_change"] = (
    exact_rank_df["the_rank_2023_numeric"]
    - exact_rank_df["the_rank_2024_numeric"]
)

exact_rank_df["absolute_rank_change"] = (
    exact_rank_df["rank_change"].abs()
)

exact_rank_df["rank_status"] = np.where(
    exact_rank_df["rank_change"] > 0,
    "Improved",
    np.where(
        exact_rank_df["rank_change"] < 0,
        "Declined",
        "Stable"
    )
)

print(
    f"Average 2023 rank: "
    f"{exact_rank_df['the_rank_2023_numeric'].mean():.2f}"
)

print(
    f"Average 2024 rank: "
    f"{exact_rank_df['the_rank_2024_numeric'].mean():.2f}"
)

print(
    f"Average exact rank change: "
    f"{exact_rank_df['rank_change'].mean():.2f}"
)

print(
    f"Median absolute rank change: "
    f"{exact_rank_df['absolute_rank_change'].median():.2f}"
)

print(
    f"Mean absolute rank change: "
    f"{exact_rank_df['absolute_rank_change'].mean():.2f}"
)

print("\nRank status:")

print(
    exact_rank_df["rank_status"]
    .value_counts()
)

# ==============================================================
# STEP 4 - SAVE EXACT RANK OVERLAP
# ==============================================================

exact_rank_output = exact_rank_df[
    [
        "university_id",
        "university_name",
        "country_name",
        "the_rank_2023",
        "the_rank_2024",
        "the_rank_2023_numeric",
        "the_rank_2024_numeric",
        "rank_change",
        "absolute_rank_change",
        "rank_status"
    ]
].sort_values(
    "rank_change",
    ascending=False
)

exact_rank_file = os.path.join(
    EDA_DIR,
    "the_2023_2024_exact_rank_overlap_v2.csv"
)

exact_rank_output.to_csv(
    exact_rank_file,
    index=False
)

print(
    f"\nSaved: {exact_rank_file}"
)

# ==============================================================
# STEP 5 - TOP IMPROVEMENTS
# ==============================================================

print("\n" + "=" * 70)
print("4. TOP EXACT RANK IMPROVEMENTS")
print("=" * 70)

improvements = exact_rank_output[
    exact_rank_output["rank_change"] > 0
].head(20)

print(
    improvements[
        [
            "university_name",
            "the_rank_2023",
            "the_rank_2024",
            "rank_change"
        ]
    ].to_string(index=False)
)

improvements_file = os.path.join(
    EDA_DIR,
    "the_exact_rank_improvements_v2.csv"
)

improvements.to_csv(
    improvements_file,
    index=False
)

# ==============================================================
# STEP 6 - TOP DECLINES
# ==============================================================

print("\n" + "=" * 70)
print("5. TOP EXACT RANK DECLINES")
print("=" * 70)

declines = exact_rank_output[
    exact_rank_output["rank_change"] < 0
].sort_values(
    "rank_change",
    ascending=True
).head(20)

print(
    declines[
        [
            "university_name",
            "the_rank_2023",
            "the_rank_2024",
            "rank_change"
        ]
    ].to_string(index=False)
)

declines_file = os.path.join(
    EDA_DIR,
    "the_exact_rank_declines_v2.csv"
)

declines.to_csv(
    declines_file,
    index=False
)

# ==============================================================
# STEP 7 - STABLE UNIVERSITIES
# ==============================================================

print("\n" + "=" * 70)
print("6. STABLE UNIVERSITIES")
print("=" * 70)

stable = exact_rank_output[
    exact_rank_output["rank_change"] == 0
]

print(
    f"Stable universities: {len(stable)}"
)

stable_file = os.path.join(
    EDA_DIR,
    "the_exact_rank_stable_v2.csv"
)

stable.to_csv(
    stable_file,
    index=False
)

print(
    stable[
        [
            "university_name",
            "the_rank_2023",
            "the_rank_2024"
        ]
    ].to_string(index=False)
)

# ==============================================================
# STEP 8 - SCORE TREND
# ==============================================================

print("\n" + "=" * 70)
print("7. THE 2023 -> 2024 SCORE TREND")
print("=" * 70)

score_df = df[
    df["the_score_2023_numeric"].notna() &
    df["the_score_2024_numeric"].notna()
].copy()

score_df["score_change"] = (
    score_df["the_score_2024_numeric"]
    - score_df["the_score_2023_numeric"]
)

score_df["absolute_score_change"] = (
    score_df["score_change"].abs()
)

print(
    f"Universities with scores in BOTH years: "
    f"{len(score_df)}"
)

print(
    f"Average 2023 score: "
    f"{score_df['the_score_2023_numeric'].mean():.2f}"
)

print(
    f"Average 2024 score: "
    f"{score_df['the_score_2024_numeric'].mean():.2f}"
)

print(
    f"Average score change: "
    f"{score_df['score_change'].mean():.2f}"
)

print(
    f"Median score change: "
    f"{score_df['score_change'].median():.2f}"
)

print(
    f"Mean absolute score change: "
    f"{score_df['absolute_score_change'].mean():.2f}"
)

score_output = score_df[
    [
        "university_id",
        "university_name",
        "country_name",
        "the_overall_score_2023",
        "the_overall_score_2024",
        "score_change",
        "absolute_score_change"
    ]
].sort_values(
    "score_change",
    ascending=False
)

score_file = os.path.join(
    EDA_DIR,
    "the_2023_2024_score_overlap_v2.csv"
)

score_output.to_csv(
    score_file,
    index=False
)

print(
    f"\nSaved: {score_file}"
)

# ==============================================================
# STEP 9 - FIGURE: EXACT RANK SCATTER
# ==============================================================

print("\n" + "=" * 70)
print("8. CREATING FIGURES")
print("=" * 70)

if len(exact_rank_df) > 0:

    plt.figure(figsize=(9, 7))

    plt.scatter(
        exact_rank_df["the_rank_2023_numeric"],
        exact_rank_df["the_rank_2024_numeric"],
        alpha=0.7
    )

    max_rank = max(
        exact_rank_df["the_rank_2023_numeric"].max(),
        exact_rank_df["the_rank_2024_numeric"].max()
    )

    plt.plot(
        [1, max_rank],
        [1, max_rank],
        linestyle="--"
    )

    plt.xlabel("THE 2023 Exact Rank")
    plt.ylabel("THE 2024 Rank")

    plt.title(
        "THE 2023 vs THE 2024 Exact Rank Comparison"
    )

    plt.tight_layout()

    scatter_file = os.path.join(
        FIG_DIR,
        "the_2023_vs_2024_exact_rank_scatter_v2.png"
    )

    plt.savefig(
        scatter_file,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {scatter_file}"
    )

# ==============================================================
# STEP 10 - RANK CHANGE DISTRIBUTION
# ==============================================================

if len(exact_rank_df) > 0:

    plt.figure(figsize=(10, 6))

    plt.hist(
        exact_rank_df["rank_change"],
        bins=20
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
        "THE Exact Rank Change Distribution"
    )

    plt.tight_layout()

    rank_change_file = os.path.join(
        FIG_DIR,
        "the_exact_rank_change_distribution_v2.png"
    )

    plt.savefig(
        rank_change_file,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {rank_change_file}"
    )

# ==============================================================
# STEP 11 - SCORE CHANGE DISTRIBUTION
# ==============================================================

if len(score_df) > 0:

    plt.figure(figsize=(10, 6))

    plt.hist(
        score_df["score_change"],
        bins=20
    )

    plt.axvline(
        0,
        linestyle="--"
    )

    plt.xlabel("THE Overall Score Change")
    plt.ylabel("Number of Universities")

    plt.title(
        "THE 2023 -> 2024 Overall Score Change"
    )

    plt.tight_layout()

    score_change_file = os.path.join(
        FIG_DIR,
        "the_score_change_distribution_v2.png"
    )

    plt.savefig(
        score_change_file,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {score_change_file}"
    )

# ==============================================================
# FINAL SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("STEP 9.7 V2 SUMMARY")
print("=" * 70)

print(f"Total universities: {len(df)}")

print(
    f"Exact THE 2023 rank + THE 2024 rank overlap: "
    f"{len(exact_rank_df)}"
)

print(
    f"THE 2023 banded records excluded from exact trend: "
    f"{df['the_2023_is_banded'].sum()}"
)

print(
    f"Improved: "
    f"{(exact_rank_df['rank_status'] == 'Improved').sum()}"
)

print(
    f"Declined: "
    f"{(exact_rank_df['rank_status'] == 'Declined').sum()}"
)

print(
    f"Stable: "
    f"{(exact_rank_df['rank_status'] == 'Stable').sum()}"
)

print(
    f"Score overlap: "
    f"{len(score_df)}"
)

print("\n" + "=" * 70)
print("STEP 9.7 V2 COMPLETED")
print("=" * 70)

print("\nIMPORTANT:")
print(
    "THE 2023 banded ranks were excluded from exact rank-change analysis."
)
print(
    "The final analytical dataset was NOT modified."
)