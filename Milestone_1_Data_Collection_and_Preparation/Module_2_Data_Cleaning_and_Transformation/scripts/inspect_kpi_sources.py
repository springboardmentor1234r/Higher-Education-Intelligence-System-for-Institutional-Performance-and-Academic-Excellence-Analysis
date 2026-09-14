import pandas as pd

INPUT_FILE = "data/processed/university_integrated_worldbank_education.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("KPI SOURCE DATA INSPECTION")
print("=" * 70)

kpi_columns = [
    "qs_overall_score",
    "qs_citations_per_faculty_score",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "qs_academic_reputation_score",
    "the_research_score_2024",
    "the_citations_score_2024",
]

print(f"\nDataset shape: {df.shape}")

print("\n" + "=" * 70)
print("KPI SOURCE AVAILABILITY")
print("=" * 70)

for col in kpi_columns:
    available = df[col].notna().sum()
    missing = df[col].isna().sum()
    coverage = available / len(df) * 100

    print(f"\n{col}")
    print(f"  Available : {available}")
    print(f"  Missing   : {missing}")
    print(f"  Coverage  : {coverage:.2f}%")

print("\n" + "=" * 70)
print("KPI SOURCE DESCRIPTIVE STATISTICS")
print("=" * 70)

print(df[kpi_columns].describe().T)

print("\n" + "=" * 70)
print("KPI SOURCE DATA TYPES")
print("=" * 70)

print(df[kpi_columns].dtypes)

print("\n" + "=" * 70)
print("KPI SOURCE CORRELATIONS")
print("=" * 70)

print(df[kpi_columns].corr(method="spearman").round(3))

print("\n" + "=" * 70)
print("INSPECTION COMPLETED")
print("=" * 70)