import pandas as pd
from pathlib import Path

BASE_DIR = Path("data/processed")

MASTER_FILE = BASE_DIR / "university_master.csv"
QS_FILE = BASE_DIR / "qs_2025_with_id.csv"
THE24_FILE = BASE_DIR / "the_2024_with_id.csv"
THE23_FILE = BASE_DIR / "the_2023_with_id.csv"

OUTPUT_FILE = BASE_DIR / "university_integrated.csv"

print("=" * 70)
print("STEP 8D - INTEGRATING UNIVERSITY DATA")
print("=" * 70)

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

master = pd.read_csv(MASTER_FILE)
qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE24_FILE)
the23 = pd.read_csv(THE23_FILE)

print(f"\nMaster universities : {len(master):,}")
print(f"QS 2025             : {len(qs):,}")
print(f"THE 2024            : {len(the24):,}")
print(f"THE 2023            : {len(the23):,}")


# ---------------------------------------------------------
# 2. VALIDATE IDS
# ---------------------------------------------------------

for name, df in [
    ("Master", master),
    ("QS 2025", qs),
    ("THE 2024", the24),
    ("THE 2023", the23)
]:

    missing_ids = df["university_id"].isna().sum()
    duplicate_ids = df["university_id"].duplicated().sum()

    print(f"\n{name}")
    print(f"  Missing IDs   : {missing_ids}")
    print(f"  Duplicate IDs : {duplicate_ids}")

    if missing_ids > 0:
        raise ValueError(f"{name} contains missing university IDs.")

    if duplicate_ids > 0:
        raise ValueError(f"{name} contains duplicate university IDs.")


# ---------------------------------------------------------
# 3. MASTER BASE
# ---------------------------------------------------------

master_base = master[
    [
        "university_id",
        "university_name",
        "country_name",
        "country_code",
        "country_name_canonical"
    ]
].copy()


# ---------------------------------------------------------
# 4. QS DATA
# ---------------------------------------------------------

qs_data = qs[
    [
        "university_id",
        "qs_rank_2025",
        "qs_overall_score",
        "qs_academic_reputation_score",
        "qs_employer_reputation_score",
        "qs_faculty_student_score",
        "qs_citations_per_faculty_score",
        "qs_international_students_score",
        "qs_international_faculty_score",
        "qs_employment_outcomes_score",
        "qs_sustainability_score"
    ]
].copy()

# Dataset presence flag
qs_data["qs_present"] = True


# ---------------------------------------------------------
# 5. THE 2024 DATA
# ---------------------------------------------------------

the24_data = the24[
    [
        "university_id",
        "the_rank_2024",
        "the_overall_score_2024",
        "the_teaching_score_2024",
        "the_research_score_2024",
        "the_citations_score_2024",
        "the_industry_income_score_2024",
        "the_international_outlook_score_2024",
        "the_student_staff_ratio_2024",
        "the_international_students_pct_2024",
        "the_female_percentage_2024"
    ]
].copy()

# Dataset presence flag
the24_data["the24_present"] = True


# ---------------------------------------------------------
# 6. THE 2023 DATA
# ---------------------------------------------------------

the23_data = the23[
    [
        "university_id",
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
].copy()

# Dataset presence flag
the23_data["the23_present"] = True


# ---------------------------------------------------------
# 7. INTEGRATE QS
# ---------------------------------------------------------

integrated = master_base.merge(
    qs_data,
    on="university_id",
    how="left",
    validate="one_to_one"
)

print("\nQS integration completed.")


# ---------------------------------------------------------
# 8. INTEGRATE THE 2024
# ---------------------------------------------------------

integrated = integrated.merge(
    the24_data,
    on="university_id",
    how="left",
    validate="one_to_one"
)

print("THE 2024 integration completed.")


# ---------------------------------------------------------
# 9. INTEGRATE THE 2023
# ---------------------------------------------------------

integrated = integrated.merge(
    the23_data,
    on="university_id",
    how="left",
    validate="one_to_one"
)

print("THE 2023 integration completed.")


# ---------------------------------------------------------
# 10. CONVERT PRESENCE FLAGS
# ---------------------------------------------------------

integrated["qs_present"] = (
    integrated["qs_present"]
    .fillna(False)
    .astype(bool)
)

integrated["the24_present"] = (
    integrated["the24_present"]
    .fillna(False)
    .astype(bool)
)

integrated["the23_present"] = (
    integrated["the23_present"]
    .fillna(False)
    .astype(bool)
)


# ---------------------------------------------------------
# 11. ROW COUNT VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("INTEGRATION VALIDATION")
print("=" * 70)

print(f"Master rows     : {len(master):,}")
print(f"Integrated rows : {len(integrated):,}")

if len(integrated) != len(master):
    raise ValueError("Row count changed during integration!")

print("✅ Row count preserved.")


# ---------------------------------------------------------
# 12. UNIVERSITY ID VALIDATION
# ---------------------------------------------------------

missing_ids = integrated["university_id"].isna().sum()
duplicate_ids = integrated["university_id"].duplicated().sum()

print(f"\nMissing university IDs   : {missing_ids}")
print(f"Duplicate university IDs : {duplicate_ids}")

if missing_ids != 0:
    raise ValueError("Missing university IDs found.")

if duplicate_ids != 0:
    raise ValueError("Duplicate university IDs found.")


# ---------------------------------------------------------
# 13. DATASET COVERAGE
# ---------------------------------------------------------

qs_coverage = integrated["qs_present"].sum()
the24_coverage = integrated["the24_present"].sum()
the23_coverage = integrated["the23_present"].sum()

all_three_coverage = (
    integrated["qs_present"]
    & integrated["the24_present"]
    & integrated["the23_present"]
).sum()


print("\n" + "=" * 70)
print("DATASET COVERAGE")
print("=" * 70)

print(f"QS 2025 attached     : {qs_coverage:,}")
print(f"THE 2024 attached    : {the24_coverage:,}")
print(f"THE 2023 attached    : {the23_coverage:,}")
print(f"All three attached   : {all_three_coverage:,}")


# ---------------------------------------------------------
# 14. EXPECTED COVERAGE
# ---------------------------------------------------------

expected = {
    "QS 2025": 1503,
    "THE 2024": 2671,
    "THE 2023": 2233,
    "All Three": 722
}

actual = {
    "QS 2025": qs_coverage,
    "THE 2024": the24_coverage,
    "THE 2023": the23_coverage,
    "All Three": all_three_coverage
}

print("\n" + "=" * 70)
print("EXPECTED VS ACTUAL COVERAGE")
print("=" * 70)

for name in expected:

    status = "✅" if expected[name] == actual[name] else "❌"

    print(
        f"{status} {name}: "
        f"Expected = {expected[name]:,}, "
        f"Actual = {actual[name]:,}"
    )

    if expected[name] != actual[name]:
        raise ValueError(
            f"{name} coverage does not match expected value."
        )


# ---------------------------------------------------------
# 15. MISSING DATASET RECORDS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET PRESENCE SUMMARY")
print("=" * 70)

print(
    f"Universities without QS 2025 : "
    f"{(~integrated['qs_present']).sum():,}"
)

print(
    f"Universities without THE 2024 : "
    f"{(~integrated['the24_present']).sum():,}"
)

print(
    f"Universities without THE 2023 : "
    f"{(~integrated['the23_present']).sum():,}"
)

print(
    f"Universities present in all 3 : "
    f"{all_three_coverage:,}"
)


# ---------------------------------------------------------
# 16. SAVE
# ---------------------------------------------------------

integrated.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("INTEGRATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"Final shape: {integrated.shape}")
print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst 5 rows:")
print(
    integrated.head().to_string(index=False)
)

print("\n" + "=" * 70)
print("✅ STEP 8D PASSED")
print("=" * 70)