import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - DIAGNOSE UNIVERSITY MATCHING
# ============================================================

BASE_DIR = Path("data/processed")

MASTER_FILE = BASE_DIR / "university_master.csv"
QS_FILE = BASE_DIR / "qs_2025_common.csv"
THE24_FILE = BASE_DIR / "the_2024_common.csv"
THE23_FILE = BASE_DIR / "the_2023_common.csv"


# ============================================================
# STEP 1 - LOAD
# ============================================================

print("=" * 70)
print("STEP 1 - LOADING DATA")
print("=" * 70)

master = pd.read_csv(MASTER_FILE)
qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE24_FILE)
the23 = pd.read_csv(THE23_FILE)

print(f"Master:   {len(master):,}")
print(f"QS 2025:  {len(qs):,}")
print(f"THE 2024: {len(the24):,}")
print(f"THE 2023: {len(the23):,}")


# ============================================================
# STEP 2 - NAME MATCH CHECK
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 - NAME MATCH CHECK")
print("=" * 70)

master_names = set(master["university_name_clean"])

qs_name_matches = qs["university_name_clean"].isin(master_names).sum()
the24_name_matches = the24["university_name_clean"].isin(master_names).sum()
the23_name_matches = the23["university_name_clean"].isin(master_names).sum()

print(f"QS name matches:       {qs_name_matches:,}")
print(f"THE 2024 name matches: {the24_name_matches:,}")
print(f"THE 2023 name matches: {the23_name_matches:,}")


# ============================================================
# STEP 3 - COUNTRY-AWARE MATCH CHECK
# ============================================================

print("\n" + "=" * 70)
print("STEP 3 - NAME + COUNTRY MATCH CHECK")
print("=" * 70)

master_pairs = set(
    zip(
        master["university_name_clean"],
        master["country_name_clean"]
    )
)

qs_pairs = set(
    zip(
        qs["university_name_clean"],
        qs["country_name_clean"]
    )
)

the24_pairs = set(
    zip(
        the24["university_name_clean"],
        the24["country_name_clean"]
    )
)

the23_pairs = set(
    zip(
        the23["university_name_clean"],
        the23["country_name_clean"]
    )
)

print(
    f"QS name + country matches:       "
    f"{len(qs_pairs.intersection(master_pairs)):,}"
)

print(
    f"THE 2024 name + country matches: "
    f"{len(the24_pairs.intersection(master_pairs)):,}"
)

print(
    f"THE 2023 name + country matches: "
    f"{len(the23_pairs.intersection(master_pairs)):,}"
)


# ============================================================
# STEP 4 - CHECK MASTER DUPLICATE NAME/COUNTRY PAIRS
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 - CHECK DUPLICATE NAME + COUNTRY PAIRS")
print("=" * 70)

master_pair_duplicates = master[
    master.duplicated(
        subset=[
            "university_name_clean",
            "country_name_clean"
        ],
        keep=False
    )
]

print(
    "Duplicate master name + country pairs:",
    len(master_pair_duplicates)
)


# ============================================================
# STEP 5 - CHECK COUNTRY MISMATCHES
# ============================================================

print("\n" + "=" * 70)
print("STEP 5 - CHECK COUNTRY MISMATCHES")
print("=" * 70)

master_lookup = master[
    [
        "university_name_clean",
        "country_name_clean",
        "university_id"
    ]
].copy()

qs_check = qs.merge(
    master_lookup,
    on="university_name_clean",
    how="left",
    suffixes=("_qs", "_master")
)

country_mismatch_qs = qs_check[
    qs_check["country_name_clean_qs"]
    != qs_check["country_name_clean_master"]
]

print(
    "QS country mismatches after name matching:",
    len(country_mismatch_qs)
)

the24_check = the24.merge(
    master_lookup,
    on="university_name_clean",
    how="left",
    suffixes=("_the24", "_master")
)

country_mismatch_the24 = the24_check[
    the24_check["country_name_clean_the24"]
    != the24_check["country_name_clean_master"]
]

print(
    "THE 2024 country mismatches after name matching:",
    len(country_mismatch_the24)
)

the23_check = the23.merge(
    master_lookup,
    on="university_name_clean",
    how="left",
    suffixes=("_the23", "_master")
)

country_mismatch_the23 = the23_check[
    the23_check["country_name_clean_the23"]
    != the23_check["country_name_clean_master"]
]

print(
    "THE 2023 country mismatches after name matching:",
    len(country_mismatch_the23)
)


# ============================================================
# STEP 6 - EXAMPLE MISMATCHES
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 - SAMPLE COUNTRY MISMATCHES")
print("=" * 70)

if len(country_mismatch_qs) > 0:

    print("\nQS examples:")
    print(
        country_mismatch_qs[
            [
                "university_name_clean",
                "country_name_clean_qs",
                "country_name_clean_master",
                "university_id"
            ]
        ].head(10).to_string(index=False)
    )

if len(country_mismatch_the24) > 0:

    print("\nTHE 2024 examples:")
    print(
        country_mismatch_the24[
            [
                "university_name_clean",
                "country_name_clean_the24",
                "country_name_clean_master",
                "university_id"
            ]
        ].head(10).to_string(index=False)
    )

if len(country_mismatch_the23) > 0:

    print("\nTHE 2023 examples:")
    print(
        country_mismatch_the23[
            [
                "university_name_clean",
                "country_name_clean_the23",
                "country_name_clean_master",
                "university_id"
            ]
        ].head(10).to_string(index=False)
    )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("DIAGNOSTIC CHECK COMPLETED")
print("=" * 70)