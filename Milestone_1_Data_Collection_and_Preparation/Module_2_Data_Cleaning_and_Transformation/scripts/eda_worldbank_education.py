import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# STEP 9.8 - WORLD BANK EDUCATION ANALYSIS
# ============================================================

print("=" * 70)
print("STEP 9.8 - WORLD BANK EDUCATION ANALYSIS")
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

education_columns = {
    "Tertiary Enrollment Ratio":
        "wb_tertiary_enrollment_ratio_2015",

    "Tertiary Graduation Ratio":
        "wb_tertiary_graduation_ratio_2015",

    "Female Tertiary Students (%)":
        "wb_female_tertiary_students_pct_2015",

    "Tertiary Pupil-Teacher Ratio":
        "wb_tertiary_pupil_teacher_ratio_2015",

    "Youth Literacy Rate 15-24 (%)":
        "wb_youth_literacy_15_24_pct_2015",

    "Tertiary Graduates":
        "wb_tertiary_graduates_2015",
}

required_columns = [
    "university_id",
    "university_name",
    "country_name",
    "country_code",
    "wb_country_code",
    "wb_country_name",
    "wb_region",
    "wb_income_group",
    "worldbank_linked",
    "worldbank_education_2015_linked",
    "qs_rank_2025",
    "qs_overall_score",
    "the_rank_2024",
    "the_overall_score_2024",
] + list(education_columns.values())

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR: Missing required columns:")

    for column in missing_columns:
        print(f"  - {column}")

    raise SystemExit(1)

print("Required columns: PASS")


# ============================================================
# CONVERT EDUCATION VARIABLES TO NUMERIC
# ============================================================

for column in education_columns.values():

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# 1. EDUCATION DATA COVERAGE
# ============================================================

print("\n" + "=" * 70)
print("1. WORLD BANK EDUCATION DATA COVERAGE")
print("=" * 70)

coverage_rows = []

for label, column in education_columns.items():

    available = df[column].notna().sum()
    missing = df[column].isna().sum()

    coverage = (
        available / len(df) * 100
    )

    coverage_rows.append({
        "indicator": label,
        "column": column,
        "available": available,
        "missing": missing,
        "coverage_percent": coverage
    })

    print(
        f"{label:40s} "
        f"Available: {available:4d} | "
        f"Missing: {missing:4d} | "
        f"Coverage: {coverage:.2f}%"
    )


coverage_df = pd.DataFrame(coverage_rows)

coverage_df.to_csv(
    EDA_DIR / "worldbank_education_indicator_coverage.csv",
    index=False
)


# ============================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("2. EDUCATION INDICATOR DESCRIPTIVE STATISTICS")
print("=" * 70)

statistics_rows = []

for label, column in education_columns.items():

    series = df[column].dropna()

    statistics_rows.append({
        "indicator": label,
        "count": series.count(),
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "min": series.min(),
        "max": series.max(),
        "q25": series.quantile(0.25),
        "q75": series.quantile(0.75),
    })


education_statistics = pd.DataFrame(
    statistics_rows
)

print(
    education_statistics.to_string(
        index=False
    )
)

education_statistics.to_csv(
    EDA_DIR / "worldbank_education_descriptive_statistics.csv",
    index=False
)


# ============================================================
# 3. COUNTRY-LEVEL EDUCATION DATA
# ============================================================

print("\n" + "=" * 70)
print("3. COUNTRY-LEVEL EDUCATION ANALYSIS")
print("=" * 70)

country_columns = [
    "wb_country_code",
    "wb_country_name",
    "wb_region",
    "wb_income_group",
] + list(education_columns.values())

country_education = (
    df[country_columns]
    .groupby(
        [
            "wb_country_code",
            "wb_country_name",
            "wb_region",
            "wb_income_group",
        ],
        dropna=False
    )
    .mean(numeric_only=True)
    .reset_index()
)

print(
    f"Unique countries with education-linked university records: "
    f"{len(country_education)}"
)


# Save full country-level dataset

country_education.to_csv(
    EDA_DIR / "worldbank_education_by_country.csv",
    index=False
)


# ============================================================
# 4. TOP COUNTRIES - TERTIARY ENROLLMENT
# ============================================================

print("\n" + "=" * 70)
print("4. TOP COUNTRIES - TERTIARY ENROLLMENT RATIO")
print("=" * 70)

top_enrollment = (
    country_education
    .dropna(
        subset=[
            "wb_tertiary_enrollment_ratio_2015"
        ]
    )
    .sort_values(
        "wb_tertiary_enrollment_ratio_2015",
        ascending=False
    )
    .head(20)
)

print(
    top_enrollment[
        [
            "wb_country_name",
            "wb_tertiary_enrollment_ratio_2015"
        ]
    ].to_string(index=False)
)

top_enrollment.to_csv(
    EDA_DIR / "top_countries_tertiary_enrollment.csv",
    index=False
)


# ============================================================
# 5. TOP COUNTRIES - GRADUATION RATIO
# ============================================================

print("\n" + "=" * 70)
print("5. TOP COUNTRIES - TERTIARY GRADUATION RATIO")
print("=" * 70)

top_graduation = (
    country_education
    .dropna(
        subset=[
            "wb_tertiary_graduation_ratio_2015"
        ]
    )
    .sort_values(
        "wb_tertiary_graduation_ratio_2015",
        ascending=False
    )
    .head(20)
)

print(
    top_graduation[
        [
            "wb_country_name",
            "wb_tertiary_graduation_ratio_2015"
        ]
    ].to_string(index=False)
)

top_graduation.to_csv(
    EDA_DIR / "top_countries_tertiary_graduation.csv",
    index=False
)


# ============================================================
# 6. TOP COUNTRIES - FEMALE TERTIARY STUDENTS
# ============================================================

print("\n" + "=" * 70)
print("6. TOP COUNTRIES - FEMALE TERTIARY STUDENTS")
print("=" * 70)

top_female = (
    country_education
    .dropna(
        subset=[
            "wb_female_tertiary_students_pct_2015"
        ]
    )
    .sort_values(
        "wb_female_tertiary_students_pct_2015",
        ascending=False
    )
    .head(20)
)

print(
    top_female[
        [
            "wb_country_name",
            "wb_female_tertiary_students_pct_2015"
        ]
    ].to_string(index=False)
)

top_female.to_csv(
    EDA_DIR / "top_countries_female_tertiary_students.csv",
    index=False
)


# ============================================================
# 7. TOP COUNTRIES - YOUTH LITERACY
# ============================================================

print("\n" + "=" * 70)
print("7. TOP COUNTRIES - YOUTH LITERACY")
print("=" * 70)

top_literacy = (
    country_education
    .dropna(
        subset=[
            "wb_youth_literacy_15_24_pct_2015"
        ]
    )
    .sort_values(
        "wb_youth_literacy_15_24_pct_2015",
        ascending=False
    )
    .head(20)
)

print(
    top_literacy[
        [
            "wb_country_name",
            "wb_youth_literacy_15_24_pct_2015"
        ]
    ].to_string(index=False)
)

top_literacy.to_csv(
    EDA_DIR / "top_countries_youth_literacy.csv",
    index=False
)


# ============================================================
# 8. REGION-LEVEL EDUCATION
# ============================================================

print("\n" + "=" * 70)
print("8. WORLD BANK REGION-LEVEL EDUCATION")
print("=" * 70)

region_education = (
    df[
        [
            "wb_region"
        ] + list(education_columns.values())
    ]
    .groupby(
        "wb_region",
        dropna=False
    )
    .mean(numeric_only=True)
    .reset_index()
)

print(
    region_education.to_string(
        index=False
    )
)

region_education.to_csv(
    EDA_DIR / "worldbank_education_by_region.csv",
    index=False
)


# ============================================================
# 9. INCOME-GROUP EDUCATION
# ============================================================

print("\n" + "=" * 70)
print("9. INCOME-GROUP EDUCATION")
print("=" * 70)

income_education = (
    df[
        [
            "wb_income_group"
        ] + list(education_columns.values())
    ]
    .groupby(
        "wb_income_group",
        dropna=False
    )
    .mean(numeric_only=True)
    .reset_index()
)

print(
    income_education.to_string(
        index=False
    )
)

income_education.to_csv(
    EDA_DIR / "worldbank_education_by_income_group.csv",
    index=False
)


# ============================================================
# 10. EDUCATION VS QS SCORE
# ============================================================

print("\n" + "=" * 70)
print("10. EDUCATION VS QS 2025 OVERALL SCORE")
print("=" * 70)

qs_correlations = []

for label, education_column in education_columns.items():

    subset = df[
        [
            education_column,
            "qs_overall_score"
        ]
    ].dropna()

    if len(subset) >= 3:

        pearson = subset[
            education_column
        ].corr(
            subset["qs_overall_score"],
            method="pearson"
        )

        spearman = subset[
            education_column
        ].corr(
            subset["qs_overall_score"],
            method="spearman"
        )

    else:

        pearson = np.nan
        spearman = np.nan

    qs_correlations.append({
        "education_indicator": label,
        "sample_size": len(subset),
        "pearson_correlation": pearson,
        "spearman_correlation": spearman
    })


qs_correlation_df = pd.DataFrame(
    qs_correlations
)

print(
    qs_correlation_df.to_string(
        index=False
    )
)

qs_correlation_df.to_csv(
    EDA_DIR / "education_vs_qs_correlations.csv",
    index=False
)


# ============================================================
# 11. EDUCATION VS THE SCORE
# ============================================================

print("\n" + "=" * 70)
print("11. EDUCATION VS THE 2024 OVERALL SCORE")
print("=" * 70)

the_correlations = []

for label, education_column in education_columns.items():

    subset = df[
        [
            education_column,
            "the_overall_score_2024"
        ]
    ].dropna()

    if len(subset) >= 3:

        pearson = subset[
            education_column
        ].corr(
            subset["the_overall_score_2024"],
            method="pearson"
        )

        spearman = subset[
            education_column
        ].corr(
            subset["the_overall_score_2024"],
            method="spearman"
        )

    else:

        pearson = np.nan
        spearman = np.nan

    the_correlations.append({
        "education_indicator": label,
        "sample_size": len(subset),
        "pearson_correlation": pearson,
        "spearman_correlation": spearman
    })


the_correlation_df = pd.DataFrame(
    the_correlations
)

print(
    the_correlation_df.to_string(
        index=False
    )
)

the_correlation_df.to_csv(
    EDA_DIR / "education_vs_the_correlations.csv",
    index=False
)


# ============================================================
# 12. EDUCATION VS QS RANK
# ============================================================

print("\n" + "=" * 70)
print("12. EDUCATION VS QS 2025 RANK")
print("=" * 70)

qs_rank_correlations = []

for label, education_column in education_columns.items():

    subset = df[
        [
            education_column,
            "qs_rank_2025"
        ]
    ].copy()

    subset["qs_rank_2025"] = pd.to_numeric(
        subset["qs_rank_2025"],
        errors="coerce"
    )

    subset = subset.dropna()

    if len(subset) >= 3:

        pearson = subset[
            education_column
        ].corr(
            subset["qs_rank_2025"],
            method="pearson"
        )

        spearman = subset[
            education_column
        ].corr(
            subset["qs_rank_2025"],
            method="spearman"
        )

    else:

        pearson = np.nan
        spearman = np.nan

    qs_rank_correlations.append({
        "education_indicator": label,
        "sample_size": len(subset),
        "pearson_correlation": pearson,
        "spearman_correlation": spearman
    })


qs_rank_correlation_df = pd.DataFrame(
    qs_rank_correlations
)

print(
    qs_rank_correlation_df.to_string(
        index=False
    )
)

qs_rank_correlation_df.to_csv(
    EDA_DIR / "education_vs_qs_rank_correlations.csv",
    index=False
)


# ============================================================
# 13. EDUCATION VS THE RANK
# ============================================================

print("\n" + "=" * 70)
print("13. EDUCATION VS THE 2024 RANK")
print("=" * 70)

the_rank_correlations = []

for label, education_column in education_columns.items():

    subset = df[
        [
            education_column,
            "the_rank_2024"
        ]
    ].copy()

    subset["the_rank_2024"] = pd.to_numeric(
        subset["the_rank_2024"],
        errors="coerce"
    )

    subset = subset.dropna()

    if len(subset) >= 3:

        pearson = subset[
            education_column
        ].corr(
            subset["the_rank_2024"],
            method="pearson"
        )

        spearman = subset[
            education_column
        ].corr(
            subset["the_rank_2024"],
            method="spearman"
        )

    else:

        pearson = np.nan
        spearman = np.nan

    the_rank_correlations.append({
        "education_indicator": label,
        "sample_size": len(subset),
        "pearson_correlation": pearson,
        "spearman_correlation": spearman
    })


the_rank_correlation_df = pd.DataFrame(
    the_rank_correlations
)

print(
    the_rank_correlation_df.to_string(
        index=False
    )
)

the_rank_correlation_df.to_csv(
    EDA_DIR / "education_vs_the_rank_correlations.csv",
    index=False
)


# ============================================================
# 14. CREATE CORRELATION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("14. EDUCATION + RANKING CORRELATION MATRIX")
print("=" * 70)

correlation_columns = list(
    education_columns.values()
) + [
    "qs_overall_score",
    "the_overall_score_2024",
]

correlation_matrix = df[
    correlation_columns
].corr(
    method="spearman"
)

print(
    correlation_matrix.to_string()
)

correlation_matrix.to_csv(
    EDA_DIR / "education_ranking_spearman_correlation_matrix.csv"
)


# ============================================================
# 15. FIGURE - EDUCATION COVERAGE
# ============================================================

plt.figure(figsize=(11, 7))

coverage_plot = coverage_df.sort_values(
    "coverage_percent"
)

plt.barh(
    coverage_plot["indicator"],
    coverage_plot["coverage_percent"]
)

plt.xlabel("Coverage (%)")
plt.ylabel("Education Indicator")

plt.title(
    "World Bank Education Indicator Coverage"
)

plt.xlim(0, 100)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "worldbank_education_coverage.png",
    dpi=300
)

plt.close()


# ============================================================
# 16. FIGURE - REGION EDUCATION
# ============================================================

region_plot = region_education.dropna(
    subset=["wb_region"]
).copy()

if len(region_plot) > 0:

    plt.figure(figsize=(12, 7))

    plt.bar(
        region_plot["wb_region"],
        region_plot[
            "wb_tertiary_enrollment_ratio_2015"
        ]
    )

    plt.xlabel("World Bank Region")
    plt.ylabel(
        "Average Tertiary Enrollment Ratio (%)"
    )

    plt.title(
        "Average Tertiary Enrollment Ratio by World Bank Region"
    )

    plt.xticks(
        rotation=35,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "tertiary_enrollment_by_region.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 17. FIGURE - INCOME GROUP EDUCATION
# ============================================================

income_plot = income_education.dropna(
    subset=["wb_income_group"]
).copy()

if len(income_plot) > 0:

    plt.figure(figsize=(11, 7))

    plt.bar(
        income_plot["wb_income_group"],
        income_plot[
            "wb_tertiary_enrollment_ratio_2015"
        ]
    )

    plt.xlabel("World Bank Income Group")
    plt.ylabel(
        "Average Tertiary Enrollment Ratio (%)"
    )

    plt.title(
        "Average Tertiary Enrollment Ratio by Income Group"
    )

    plt.xticks(
        rotation=35,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "tertiary_enrollment_by_income_group.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 18. FIGURE - QS SCORE VS ENROLLMENT
# ============================================================

qs_enrollment = df[
    [
        "wb_tertiary_enrollment_ratio_2015",
        "qs_overall_score"
    ]
].dropna()

if len(qs_enrollment) >= 3:

    plt.figure(figsize=(9, 7))

    plt.scatter(
        qs_enrollment[
            "wb_tertiary_enrollment_ratio_2015"
        ],
        qs_enrollment[
            "qs_overall_score"
        ],
        alpha=0.6
    )

    plt.xlabel(
        "Tertiary Enrollment Ratio (%)"
    )

    plt.ylabel(
        "QS 2025 Overall Score"
    )

    plt.title(
        "Tertiary Enrollment vs QS 2025 Overall Score"
    )

    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "education_vs_qs_score.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 19. FIGURE - THE SCORE VS ENROLLMENT
# ============================================================

the_enrollment = df[
    [
        "wb_tertiary_enrollment_ratio_2015",
        "the_overall_score_2024"
    ]
].dropna()

if len(the_enrollment) >= 3:

    plt.figure(figsize=(9, 7))

    plt.scatter(
        the_enrollment[
            "wb_tertiary_enrollment_ratio_2015"
        ],
        the_enrollment[
            "the_overall_score_2024"
        ],
        alpha=0.6
    )

    plt.xlabel(
        "Tertiary Enrollment Ratio (%)"
    )

    plt.ylabel(
        "THE 2024 Overall Score"
    )

    plt.title(
        "Tertiary Enrollment vs THE 2024 Overall Score"
    )

    plt.tight_layout()

    plt.savefig(
        FIG_DIR / "education_vs_the_score.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 20. FINAL EDUCATION LINKAGE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("20. FINAL EDUCATION LINKAGE SUMMARY")
print("=" * 70)

education_linked = df[
    "worldbank_education_2015_linked"
].eq(True).sum()

education_not_linked = (
    len(df) - education_linked
)

print(
    f"Universities with World Bank education data: "
    f"{education_linked}"
)

print(
    f"Universities without World Bank education data: "
    f"{education_not_linked}"
)

print(
    f"Education linkage rate: "
    f"{education_linked / len(df) * 100:.2f}%"
)


# ============================================================
# OUTPUT FILE LIST
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

output_files = [
    "worldbank_education_indicator_coverage.csv",
    "worldbank_education_descriptive_statistics.csv",
    "worldbank_education_by_country.csv",
    "top_countries_tertiary_enrollment.csv",
    "top_countries_tertiary_graduation.csv",
    "top_countries_female_tertiary_students.csv",
    "top_countries_youth_literacy.csv",
    "worldbank_education_by_region.csv",
    "worldbank_education_by_income_group.csv",
    "education_vs_qs_correlations.csv",
    "education_vs_the_correlations.csv",
    "education_vs_qs_rank_correlations.csv",
    "education_vs_the_rank_correlations.csv",
    "education_ranking_spearman_correlation_matrix.csv",
]

for file_name in output_files:
    print(f"data/eda/{file_name}")


print("\nFigures:")

figure_files = [
    "worldbank_education_coverage.png",
    "tertiary_enrollment_by_region.png",
    "tertiary_enrollment_by_income_group.png",
    "education_vs_qs_score.png",
    "education_vs_the_score.png",
]

for file_name in figure_files:
    print(f"reports/figures/{file_name}")


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.8 COMPLETED SUCCESSFULLY")
print("=" * 70)