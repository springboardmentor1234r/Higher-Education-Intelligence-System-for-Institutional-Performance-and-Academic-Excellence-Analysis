# ============================================================
# EduVision_DV - KPI Validation
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_DATA_DIR = PROJECT_ROOT / "data" / "final"


# ============================================================
# 2. Load KPI dataset
# ============================================================

df = pd.read_csv(
    FINAL_DATA_DIR /
    "university_kpi_dataset.csv"
)


# ============================================================
# 3. Define KPI columns
# ============================================================

kpis = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]


# ============================================================
# 4. Check duplicate University IDs
# ============================================================

duplicates = df["University_ID"].duplicated().sum()

print("=" * 80)
print("KPI VALIDATION")
print("=" * 80)

print(
    f"\nDuplicate University IDs: {duplicates}"
)


# ============================================================
# 5. Check missing KPI values
# ============================================================

print("\n" + "=" * 80)
print("MISSING KPI VALUES")
print("=" * 80)

for kpi in kpis:
    print(
        f"{kpi}: "
        f"{df[kpi].isna().sum()}"
    )


# ============================================================
# 6. Check negative KPI values
# ============================================================

print("\n" + "=" * 80)
print("NEGATIVE VALUES")
print("=" * 80)

for kpi in kpis:
    negative_count = (
        df[kpi] < 0
    ).sum()

    print(
        f"{kpi}: "
        f"{negative_count}"
    )


# ============================================================
# 7. Check percentage range
# ============================================================

print("\n" + "=" * 80)
print("INTERNATIONAL STUDENT PERCENTAGE CHECK")
print("=" * 80)

invalid_percentage = df[
    (df["International_Student_Percentage"] < 0)
    |
    (df["International_Student_Percentage"] > 100)
]

print(
    f"Invalid percentage records: "
    f"{len(invalid_percentage)}"
)


# ============================================================
# 8. Check 0-100 KPI ranges
# ============================================================

score_kpis = [
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
]

print("\n" + "=" * 80)
print("0-100 KPI RANGE CHECK")
print("=" * 80)

for kpi in score_kpis:

    invalid = df[
        (df[kpi] < 0)
        |
        (df[kpi] > 100)
    ]

    print(
        f"{kpi}: "
        f"{len(invalid)} invalid records"
    )


# ============================================================
# 9. Inspect unusually high faculty-to-student ratios
# ============================================================

print("\n" + "=" * 80)
print("HIGH FACULTY-TO-STUDENT RATIOS")
print("=" * 80)

high_ratio = df[
    df["Faculty_to_Student_Ratio"] > 50
].sort_values(
    "Faculty_to_Student_Ratio",
    ascending=False
)

print(
    high_ratio[
        [
            "University_ID",
            "University_Name",
            "Faculty_to_Student_Ratio",
            "THE_Students_to_Staff_Ratio",
            "WUR_No_of_student_per_staff"
        ]
    ].to_string(index=False)
)


# ============================================================
# 10. Check country information
# ============================================================

print("\n" + "=" * 80)
print("COUNTRY INFORMATION")
print("=" * 80)

if "Country_Standard" in df.columns:

    missing_country = (
        df["Country_Standard"]
        .isna()
        .sum()
    )

    print(
        f"Missing country values: "
        f"{missing_country}"
    )


# ============================================================
# 11. General dataset statistics
# ============================================================

print("\n" + "=" * 80)
print("FINAL DATASET CHECK")
print("=" * 80)

print(
    f"Universities: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)

print(
    f"Total missing cells: "
    f"{df.isna().sum().sum()}"
)


# ============================================================
# 12. KPI descriptive statistics
# ============================================================

print("\n" + "=" * 80)
print("KPI STATISTICS")
print("=" * 80)

print(
    df[kpis]
    .describe()
    .round(2)
    .to_string()
)


# ============================================================
# 13. Completion
# ============================================================

print("\n" + "=" * 80)
print("KPI VALIDATION COMPLETED")
print("=" * 80)