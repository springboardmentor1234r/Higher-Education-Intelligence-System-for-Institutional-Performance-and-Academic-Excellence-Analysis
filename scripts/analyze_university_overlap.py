import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - UNIVERSITY OVERLAP ANALYSIS
# ============================================================

BASE_DIR = Path("data/processed")

QS_FILE = BASE_DIR / "qs_2025_common.csv"
THE_2024_FILE = BASE_DIR / "the_2024_common.csv"
THE_2023_FILE = BASE_DIR / "the_2023_common.csv"

# ============================================================
# STEP 1 - LOAD DATA
# ============================================================

print("=" * 70)
print("STEP 1 - LOADING COMMON UNIVERSITY DATA")
print("=" * 70)

qs = pd.read_csv(QS_FILE)
the_2024 = pd.read_csv(THE_2024_FILE)
the_2023 = pd.read_csv(THE_2023_FILE)

print(f"QS 2025 universities: {len(qs):,}")
print(f"THE 2024 universities: {len(the_2024):,}")
print(f"THE 2023 universities: {len(the_2023):,}")


# ============================================================
# STEP 2 - CREATE NAME SETS
# ============================================================

qs_names = set(qs["university_name_clean"].dropna())
the24_names = set(the_2024["university_name_clean"].dropna())
the23_names = set(the_2023["university_name_clean"].dropna())


# ============================================================
# STEP 3 - QS 2025 <-> THE 2024
# ============================================================

qs_the24 = qs_names.intersection(the24_names)

print("\n" + "=" * 70)
print("STEP 3 - QS 2025 <-> THE 2024")
print("=" * 70)

print(f"QS 2025 universities: {len(qs_names):,}")
print(f"THE 2024 universities: {len(the24_names):,}")
print(f"Exact name matches: {len(qs_the24):,}")

qs_match_rate = (len(qs_the24) / len(qs_names)) * 100
the24_match_rate = (len(qs_the24) / len(the24_names)) * 100

print(f"QS 2025 match rate: {qs_match_rate:.2f}%")
print(f"THE 2024 match rate: {the24_match_rate:.2f}%")


# ============================================================
# STEP 4 - QS 2025 <-> THE 2023
# ============================================================

qs_the23 = qs_names.intersection(the23_names)

print("\n" + "=" * 70)
print("STEP 4 - QS 2025 <-> THE 2023")
print("=" * 70)

print(f"QS 2025 universities: {len(qs_names):,}")
print(f"THE 2023 universities: {len(the23_names):,}")
print(f"Exact name matches: {len(qs_the23):,}")

qs_match_rate_23 = (len(qs_the23) / len(qs_names)) * 100
the23_match_rate = (len(qs_the23) / len(the23_names)) * 100

print(f"QS 2025 match rate: {qs_match_rate_23:.2f}%")
print(f"THE 2023 match rate: {the23_match_rate:.2f}%")


# ============================================================
# STEP 5 - THE 2024 <-> THE 2023
# ============================================================

the24_the23 = the24_names.intersection(the23_names)

print("\n" + "=" * 70)
print("STEP 5 - THE 2024 <-> THE 2023")
print("=" * 70)

print(f"THE 2024 universities: {len(the24_names):,}")
print(f"THE 2023 universities: {len(the23_names):,}")
print(f"Exact name matches: {len(the24_the23):,}")

the24_match_rate_23 = (len(the24_the23) / len(the24_names)) * 100
the23_match_rate_24 = (len(the24_the23) / len(the23_names)) * 100

print(f"THE 2024 match rate: {the24_match_rate_23:.2f}%")
print(f"THE 2023 match rate: {the23_match_rate_24:.2f}%")


# ============================================================
# STEP 6 - ALL THREE DATASETS
# ============================================================

all_three = qs_names.intersection(
    the24_names,
    the23_names
)

print("\n" + "=" * 70)
print("STEP 6 - COMMON UNIVERSITIES IN ALL THREE DATASETS")
print("=" * 70)

print(f"Universities present in QS + THE 2024 + THE 2023: {len(all_three):,}")

all_three_qs_rate = (len(all_three) / len(qs_names)) * 100
all_three_the24_rate = (len(all_three) / len(the24_names)) * 100
all_three_the23_rate = (len(all_three) / len(the23_names)) * 100

print(f"Percentage of QS 2025: {all_three_qs_rate:.2f}%")
print(f"Percentage of THE 2024: {all_three_the24_rate:.2f}%")
print(f"Percentage of THE 2023: {all_three_the23_rate:.2f}%")


# ============================================================
# STEP 7 - QS UNIVERSITIES WITHOUT THE 2024 MATCH
# ============================================================

qs_without_the24 = qs_names - the24_names

print("\n" + "=" * 70)
print("STEP 7 - QS 2025 UNIVERSITIES WITHOUT THE 2024 MATCH")
print("=" * 70)

print(f"QS universities without exact THE 2024 match: {len(qs_without_the24):,}")


# ============================================================
# STEP 8 - SAVE MATCHING RESULTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 8 - SAVING OVERLAP RESULTS")
print("=" * 70)

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

overlap_summary = pd.DataFrame({
    "comparison": [
        "QS 2025 vs THE 2024",
        "QS 2025 vs THE 2023",
        "THE 2024 vs THE 2023",
        "All Three"
    ],
    "matching_universities": [
        len(qs_the24),
        len(qs_the23),
        len(the24_the23),
        len(all_three)
    ]
})

overlap_summary.to_csv(
    output_dir / "university_overlap_summary.csv",
    index=False
)

print("Saved:")
print("data/processed/university_overlap_summary.csv")


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STEP 5 COMPLETED")
print("=" * 70)

print("\nIMPORTANT:")
print("Only exact standardized-name matches were counted.")
print("No aggressive fuzzy matching was used.")
print("False university matches are avoided.")