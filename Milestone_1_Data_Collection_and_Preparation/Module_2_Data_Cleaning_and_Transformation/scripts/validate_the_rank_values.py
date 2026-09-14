import pandas as pd
from pathlib import Path


print("=" * 70)
print("STEP 9.7A - VALIDATE THE RANK REPRESENTATION")
print("=" * 70)


# ============================================================
# PATHS
# ============================================================

INPUT_FILE = Path(
    "data/processed/university_integrated_worldbank_education.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("\nFinal analytical dataset:")
print(f"Shape: {df.shape}")


# ============================================================
# INSPECT ORIGINAL RANK VALUES
# ============================================================

print("\n" + "=" * 70)
print("1. THE 2023 ORIGINAL RANK VALUES")
print("=" * 70)

print(
    df["the_rank_2023"]
    .dropna()
    .astype(str)
    .value_counts()
    .head(40)
    .to_string()
)


print("\n" + "=" * 70)
print("2. THE 2024 ORIGINAL RANK VALUES")
print("=" * 70)

print(
    df["the_rank_2024"]
    .dropna()
    .astype(str)
    .value_counts()
    .head(40)
    .to_string()
)


# ============================================================
# SHOW VALUES THAT CONTAIN RANGES / SPECIAL FORMATS
# ============================================================

print("\n" + "=" * 70)
print("3. THE 2023 VALUES CONTAINING NON-NUMERIC CHARACTERS")
print("=" * 70)

the23_strings = (
    df["the_rank_2023"]
    .dropna()
    .astype(str)
)

non_numeric_23 = the23_strings[
    ~the23_strings.str.fullmatch(r"\d+(\.\d+)?")
]

print(f"Count: {len(non_numeric_23)}")

print(
    non_numeric_23
    .drop_duplicates()
    .head(50)
    .to_string(index=False)
)


print("\n" + "=" * 70)
print("4. THE 2024 VALUES CONTAINING NON-NUMERIC CHARACTERS")
print("=" * 70)

the24_strings = (
    df["the_rank_2024"]
    .dropna()
    .astype(str)
)

non_numeric_24 = the24_strings[
    ~the24_strings.str.fullmatch(r"\d+(\.\d+)?")
]

print(f"Count: {len(non_numeric_24)}")

print(
    non_numeric_24
    .drop_duplicates()
    .head(50)
    .to_string(index=False)
)


# ============================================================
# CHECK SUSPICIOUS DECIMAL VALUES
# ============================================================

print("\n" + "=" * 70)
print("5. SUSPICIOUS DECIMAL VALUES")
print("=" * 70)

numeric_23 = pd.to_numeric(
    df["the_rank_2023"],
    errors="coerce"
)

numeric_24 = pd.to_numeric(
    df["the_rank_2024"],
    errors="coerce"
)

suspicious_23 = df[
    numeric_23.notna()
    & (numeric_23 % 1 != 0)
].copy()

suspicious_24 = df[
    numeric_24.notna()
    & (numeric_24 % 1 != 0)
].copy()

print(
    f"THE 2023 decimal numeric values: "
    f"{len(suspicious_23)}"
)

print(
    f"THE 2024 decimal numeric values: "
    f"{len(suspicious_24)}"
)


if len(suspicious_23) > 0:

    print("\nTHE 2023 suspicious values:")

    print(
        suspicious_23[
            [
                "university_id",
                "university_name",
                "the_rank_2023",
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


if len(suspicious_24) > 0:

    print("\nTHE 2024 suspicious values:")

    print(
        suspicious_24[
            [
                "university_id",
                "university_name",
                "the_rank_2024",
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


# ============================================================
# CHECK VALUES GREATER THAN 200
# ============================================================

print("\n" + "=" * 70)
print("6. VALUES ABOVE 200")
print("=" * 70)

above_200_23 = df[
    numeric_23 > 200
][
    [
        "university_id",
        "university_name",
        "the_rank_2023",
    ]
]

above_200_24 = df[
    numeric_24 > 200
][
    [
        "university_id",
        "university_name",
        "the_rank_2024",
    ]
]

print(
    f"THE 2023 numeric values > 200: "
    f"{len(above_200_23)}"
)

print(
    f"THE 2024 numeric values > 200: "
    f"{len(above_200_24)}"
)

if len(above_200_23) > 0:
    print("\nTHE 2023 examples:")
    print(
        above_200_23.head(30).to_string(index=False)
    )

if len(above_200_24) > 0:
    print("\nTHE 2024 examples:")
    print(
        above_200_24.head(30).to_string(index=False)
    )


# ============================================================
# SHOW THE EXACT PROBLEMATIC RECORDS
# ============================================================

print("\n" + "=" * 70)
print("7. EXAMPLE UNIVERSITY RANK RECORDS")
print("=" * 70)

example_names = [
    "university of twente",
    "texas a&m university",
    "chalmers university of technology",
    "purdue university west lafayette",
    "technical university of denmark",
]

examples = df[
    df["university_name"]
    .astype(str)
    .str.lower()
    .isin(example_names)
][
    [
        "university_id",
        "university_name",
        "the_rank_2023",
        "the_rank_2024",
        "the_overall_score_2023",
        "the_overall_score_2024",
    ]
]

print(
    examples.to_string(index=False)
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9.7A SUMMARY")
print("=" * 70)

print(
    "This validation checks whether THE ranking fields contain:"
)

print("  - Exact numeric ranks")
print("  - Ranking bands such as 251-300")
print("  - Decimal/special values")
print("  - Incorrectly parsed ranking values")

print("\nDo NOT modify the final analytical dataset yet.")

print("=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)