import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("STEP 9.9 - OVERALL CORRELATION ANALYSIS")
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
# 1. LOAD DATA
# ==============================================================

print("\n" + "=" * 70)
print("LOADING FINAL ANALYTICAL DATASET")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")

# ==============================================================
# 2. SELECT IMPORTANT NUMERIC VARIABLES
# ==============================================================

variables = [
    # QS
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",

    # THE
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "the_female_percentage_2024",

    # World Bank
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015",
    "wb_tertiary_graduates_2015"
]

variables = [col for col in variables if col in df.columns]

numeric_df = df[variables].apply(pd.to_numeric, errors="coerce")

print(f"Numeric variables selected: {len(variables)}")

# ==============================================================
# 3. DESCRIPTIVE CORRELATION MATRIX
# ==============================================================

print("\n" + "=" * 70)
print("1. PEARSON CORRELATION MATRIX")
print("=" * 70)

pearson_corr = numeric_df.corr(method="pearson")

pearson_file = os.path.join(
    EDA_DIR,
    "overall_pearson_correlation_matrix.csv"
)

pearson_corr.to_csv(pearson_file)

print(f"Saved: {pearson_file}")

# ==============================================================
# 4. SPEARMAN CORRELATION MATRIX
# ==============================================================

print("\n" + "=" * 70)
print("2. SPEARMAN CORRELATION MATRIX")
print("=" * 70)

spearman_corr = numeric_df.corr(method="spearman")

spearman_file = os.path.join(
    EDA_DIR,
    "overall_spearman_correlation_matrix.csv"
)

spearman_corr.to_csv(spearman_file)

print(f"Saved: {spearman_file}")

# ==============================================================
# 5. CORRELATIONS WITH QS OVERALL SCORE
# ==============================================================

print("\n" + "=" * 70)
print("3. CORRELATION WITH QS 2025 OVERALL SCORE")
print("=" * 70)

qs_corr = pd.DataFrame({
    "variable": spearman_corr["qs_overall_score"].index,
    "spearman_correlation": spearman_corr["qs_overall_score"].values
})

qs_corr = qs_corr[
    qs_corr["variable"] != "qs_overall_score"
].copy()

qs_corr["absolute_correlation"] = (
    qs_corr["spearman_correlation"].abs()
)

qs_corr = qs_corr.sort_values(
    "absolute_correlation",
    ascending=False
)

qs_file = os.path.join(
    EDA_DIR,
    "correlations_with_qs_overall.csv"
)

qs_corr.to_csv(qs_file, index=False)

print(qs_corr.to_string(index=False))

# ==============================================================
# 6. CORRELATIONS WITH THE OVERALL SCORE
# ==============================================================

print("\n" + "=" * 70)
print("4. CORRELATION WITH THE 2024 THE OVERALL SCORE")
print("=" * 70)

the_corr = pd.DataFrame({
    "variable": spearman_corr["the_overall_score_2024"].index,
    "spearman_correlation": spearman_corr[
        "the_overall_score_2024"
    ].values
})

the_corr = the_corr[
    the_corr["variable"] != "the_overall_score_2024"
].copy()

the_corr["absolute_correlation"] = (
    the_corr["spearman_correlation"].abs()
)

the_corr = the_corr.sort_values(
    "absolute_correlation",
    ascending=False
)

the_file = os.path.join(
    EDA_DIR,
    "correlations_with_the_overall.csv"
)

the_corr.to_csv(the_file, index=False)

print(the_corr.to_string(index=False))

# ==============================================================
# 7. TOP STRONG CORRELATIONS
# ==============================================================

print("\n" + "=" * 70)
print("5. STRONGEST OVERALL CORRELATIONS")
print("=" * 70)

pairs = []

for i in range(len(spearman_corr.columns)):
    for j in range(i + 1, len(spearman_corr.columns)):

        var1 = spearman_corr.columns[i]
        var2 = spearman_corr.columns[j]

        corr = spearman_corr.iloc[i, j]

        if pd.notna(corr):
            pairs.append({
                "variable_1": var1,
                "variable_2": var2,
                "spearman_correlation": corr,
                "absolute_correlation": abs(corr)
            })

pairs_df = pd.DataFrame(pairs)

pairs_df = pairs_df.sort_values(
    "absolute_correlation",
    ascending=False
)

pairs_file = os.path.join(
    EDA_DIR,
    "strongest_overall_correlations.csv"
)

pairs_df.to_csv(pairs_file, index=False)

print("\nTop 20 correlations:")
print(pairs_df.head(20).to_string(index=False))

# ==============================================================
# 8. QS/THE/WORLD BANK GROUP CORRELATIONS
# ==============================================================

print("\n" + "=" * 70)
print("6. KEY CROSS-DOMAIN CORRELATIONS")
print("=" * 70)

qs_vars = [
    col for col in variables
    if col.startswith("qs_")
    and col != "qs_overall_score"
]

the_vars = [
    col for col in variables
    if col.startswith("the_")
    and col != "the_overall_score_2024"
]

wb_vars = [
    col for col in variables
    if col.startswith("wb_")
]

cross_domain = []

for qs_var in qs_vars:
    for wb_var in wb_vars:

        if qs_var in spearman_corr.index and wb_var in spearman_corr.index:

            value = spearman_corr.loc[qs_var, wb_var]

            if pd.notna(value):
                cross_domain.append({
                    "ranking_variable": qs_var,
                    "education_variable": wb_var,
                    "spearman_correlation": value,
                    "absolute_correlation": abs(value)
                })

for the_var in the_vars:
    for wb_var in wb_vars:

        if the_var in spearman_corr.index and wb_var in spearman_corr.index:

            value = spearman_corr.loc[the_var, wb_var]

            if pd.notna(value):
                cross_domain.append({
                    "ranking_variable": the_var,
                    "education_variable": wb_var,
                    "spearman_correlation": value,
                    "absolute_correlation": abs(value)
                })

cross_df = pd.DataFrame(cross_domain)

cross_df = cross_df.sort_values(
    "absolute_correlation",
    ascending=False
)

cross_file = os.path.join(
    EDA_DIR,
    "cross_domain_correlations.csv"
)

cross_df.to_csv(cross_file, index=False)

print("\nTop 20 cross-domain correlations:")
print(cross_df.head(20).to_string(index=False))

# ==============================================================
# 9. QS HEATMAP
# ==============================================================

print("\n" + "=" * 70)
print("7. CREATING VISUALIZATIONS")
print("=" * 70)

# QS + World Bank
qs_heatmap_vars = [
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015"
]

qs_heatmap_vars = [
    col for col in qs_heatmap_vars
    if col in spearman_corr.columns
]

qs_matrix = spearman_corr.loc[
    qs_heatmap_vars,
    qs_heatmap_vars
]

plt.figure(figsize=(12, 9))
plt.imshow(qs_matrix, aspect="auto")
plt.colorbar(label="Spearman Correlation")

plt.xticks(
    range(len(qs_matrix.columns)),
    qs_matrix.columns,
    rotation=90
)

plt.yticks(
    range(len(qs_matrix.index)),
    qs_matrix.index
)

plt.title("QS Ranking and World Bank Education Correlations")
plt.tight_layout()

qs_heatmap_file = os.path.join(
    FIG_DIR,
    "qs_worldbank_correlation_heatmap.png"
)

plt.savefig(qs_heatmap_file, dpi=300)
plt.close()

# ==============================================================
# 10. THE HEATMAP
# ==============================================================

the_heatmap_vars = [
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "wb_tertiary_enrollment_ratio_2015",
    "wb_tertiary_graduation_ratio_2015",
    "wb_female_tertiary_students_pct_2015",
    "wb_tertiary_pupil_teacher_ratio_2015",
    "wb_youth_literacy_15_24_pct_2015"
]

the_heatmap_vars = [
    col for col in the_heatmap_vars
    if col in spearman_corr.columns
]

the_matrix = spearman_corr.loc[
    the_heatmap_vars,
    the_heatmap_vars
]

plt.figure(figsize=(12, 9))
plt.imshow(the_matrix, aspect="auto")
plt.colorbar(label="Spearman Correlation")

plt.xticks(
    range(len(the_matrix.columns)),
    the_matrix.columns,
    rotation=90
)

plt.yticks(
    range(len(the_matrix.index)),
    the_matrix.index
)

plt.title("THE Ranking and World Bank Education Correlations")
plt.tight_layout()

the_heatmap_file = os.path.join(
    FIG_DIR,
    "the_worldbank_correlation_heatmap.png"
)

plt.savefig(the_heatmap_file, dpi=300)
plt.close()

# ==============================================================
# 11. TOP CORRELATIONS BAR CHART
# ==============================================================

top_pairs = pairs_df.head(15).copy()

labels = (
    top_pairs["variable_1"]
    + " ↔ "
    + top_pairs["variable_2"]
)

plt.figure(figsize=(12, 8))

plt.barh(
    range(len(top_pairs)),
    top_pairs["spearman_correlation"]
)

plt.yticks(
    range(len(top_pairs)),
    labels
)

plt.axvline(
    0,
    linewidth=1
)

plt.xlabel("Spearman Correlation")
plt.title("Top 15 Overall Correlations")

plt.gca().invert_yaxis()

plt.tight_layout()

top_corr_file = os.path.join(
    FIG_DIR,
    "top_overall_correlations.png"
)

plt.savefig(top_corr_file, dpi=300)
plt.close()

# ==============================================================
# 12. FINAL SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("STEP 9.9 SUMMARY")
print("=" * 70)

print(f"Total universities: {len(df)}")
print(f"Variables analyzed: {len(variables)}")

print("\nStrongest correlations overall:")

for _, row in pairs_df.head(10).iterrows():
    print(
        f"{row['variable_1']} <-> "
        f"{row['variable_2']}: "
        f"{row['spearman_correlation']:.4f}"
    )

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print("data/eda/overall_pearson_correlation_matrix.csv")
print("data/eda/overall_spearman_correlation_matrix.csv")
print("data/eda/correlations_with_qs_overall.csv")
print("data/eda/correlations_with_the_overall.csv")
print("data/eda/strongest_overall_correlations.csv")
print("data/eda/cross_domain_correlations.csv")

print("\nFigures:")
print("reports/figures/qs_worldbank_correlation_heatmap.png")
print("reports/figures/the_worldbank_correlation_heatmap.png")
print("reports/figures/top_overall_correlations.png")

print("\n" + "=" * 70)
print("STEP 9.9 COMPLETED SUCCESSFULLY")
print("=" * 70)