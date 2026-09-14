import pandas as pd
from pathlib import Path

BASE_DIR = Path("data/processed")
INPUT_FILE = BASE_DIR / "university_integrated.csv"

print("=" * 70)
print("STEP 8E - FINAL INTEGRATED DATA QUALITY VALIDATION")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nDataset shape: {df.shape}")

# ---------------------------------------------------------
# 1. BASIC VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("1. BASIC VALIDATION")
print("=" * 70)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns):,}")

print(f"Missing university IDs : {df['university_id'].isna().sum():,}")
print(f"Duplicate university IDs : {df['university_id'].duplicated().sum():,}")
print(f"Missing university names : {df['university_name'].isna().sum():,}")


# ---------------------------------------------------------
# 2. COUNTRY NAME CHECK
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("2. COUNTRY NAME CHECK")
print("=" * 70)

country = df["country_name"].astype(str)

problem_country = df[
    country.str.contains(
        r"United StatesUS|United KingdomGB",
        regex=True,
        na=False
    )
]

print(f"Suspicious country values: {len(problem_country):,}")

if len(problem_country) > 0:
    print("\nExamples:")
    print(
        problem_country[
            ["university_id", "university_name", "country_name", "country_code"]
        ]
        .head(20)
        .to_string(index=False)
    )


# ---------------------------------------------------------
# 3. NUMERIC COLUMN CHECK
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("3. NUMERIC DATA TYPE CHECK")
print("=" * 70)

numeric_columns = [
    "qs_rank_2025",
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",
    "the_rank_2024",
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_student_staff_ratio_2024",
    "the_international_students_pct_2024",
    "the_female_percentage_2024",
    "the_rank_2023",
    "the_overall_score_2023",
    "the_teaching_score_2023",
    "the_research_score_2023",
    "the_citations_score_2023",
    "the_industry_income_score_2023",
    "the_international_outlook_score_2023",
    "the_student_staff_ratio_2023",
    "the_international_students_pct_2023",
    "the_female_percentage_2023"
]

print("\nColumn data types:")

for col in numeric_columns:
    if col in df.columns:
        print(f"{col:45} {df[col].dtype}")


# ---------------------------------------------------------
# 4. CHECK FOR CONCATENATED NUMERIC VALUES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("4. SUSPICIOUS NUMERIC VALUES")
print("=" * 70)

for col in numeric_columns:

    if col not in df.columns:
        continue

    values = df[col].dropna().astype(str)

    suspicious = values[
        values.str.contains(
            r"\d+\.\d+\d+\.\d+",
            regex=True,
            na=False
        )
    ]

    if len(suspicious) > 0:

        print(f"\n⚠️ {col}")
        print(f"Suspicious values: {len(suspicious):,}")
        print(suspicious.head(10).tolist())


# ---------------------------------------------------------
# 5. CHECK SCORE RANGES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("5. SCORE RANGE CHECK")
print("=" * 70)

score_columns = [
    "qs_overall_score",
    "qs_academic_reputation_score",
    "qs_employer_reputation_score",
    "qs_faculty_student_score",
    "qs_citations_per_faculty_score",
    "qs_international_students_score",
    "qs_international_faculty_score",
    "qs_employment_outcomes_score",
    "qs_sustainability_score",
    "the_overall_score_2024",
    "the_teaching_score_2024",
    "the_research_score_2024",
    "the_citations_score_2024",
    "the_industry_income_score_2024",
    "the_international_outlook_score_2024",
    "the_overall_score_2023",
    "the_teaching_score_2023",
    "the_research_score_2023",
    "the_citations_score_2023",
    "the_industry_income_score_2023",
    "the_international_outlook_score_2023"
]

for col in score_columns:

    if col not in df.columns:
        continue

    numeric = pd.to_numeric(df[col], errors="coerce")

    invalid = numeric[
        (numeric < 0) | (numeric > 100)
    ]

    print(
        f"{col:45} "
        f"Invalid values: {len(invalid):,}"
    )


# ---------------------------------------------------------
# 6. DATASET PRESENCE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("6. DATASET PRESENCE")
print("=" * 70)

print(
    f"QS 2025 : {df['qs_present'].sum():,}"
)

print(
    f"THE 2024: {df['the24_present'].sum():,}"
)

print(
    f"THE 2023: {df['the23_present'].sum():,}"
)

print(
    f"All 3   : "
    f"{(df['qs_present'] & df['the24_present'] & df['the23_present']).sum():,}"
)


# ---------------------------------------------------------
# 7. MISSING VALUE SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("7. MISSING VALUE SUMMARY")
print("=" * 70)

missing = df.isna().sum()

print(
    missing[
        missing > 0
    ]
    .sort_values(ascending=False)
    .to_string()
)


# ---------------------------------------------------------
# 8. FINAL SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

print(
    f"Duplicate IDs: "
    f"{df['university_id'].duplicated().sum():,}"
)

print(
    f"Missing IDs: "
    f"{df['university_id'].isna().sum():,}"
)

print("\n" + "=" * 70)
print("STEP 8E COMPLETED")
print("=" * 70)