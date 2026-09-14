import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - VALIDATE UNIVERSITY ID OVERLAP
# ============================================================

BASE_DIR = Path("data/processed")

QS_FILE = BASE_DIR / "qs_2025_with_id.csv"
THE24_FILE = BASE_DIR / "the_2024_with_id.csv"
THE23_FILE = BASE_DIR / "the_2023_with_id.csv"

print("=" * 70)
print("STEP 8C - VALIDATING UNIVERSITY ID OVERLAP")
print("=" * 70)

qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE24_FILE)
the23 = pd.read_csv(THE23_FILE)

# Create ID sets
qs_ids = set(qs["university_id"].dropna())
the24_ids = set(the24["university_id"].dropna())
the23_ids = set(the23["university_id"].dropna())

print(f"QS 2025 IDs:  {len(qs_ids):,}")
print(f"THE 2024 IDs: {len(the24_ids):,}")
print(f"THE 2023 IDs: {len(the23_ids):,}")


# ============================================================
# QS <-> THE 2024
# ============================================================

qs_the24 = qs_ids.intersection(the24_ids)

print("\n" + "=" * 70)
print("QS 2025 <-> THE 2024")
print("=" * 70)

print(f"ID matches: {len(qs_the24):,}")


# ============================================================
# QS <-> THE 2023
# ============================================================

qs_the23 = qs_ids.intersection(the23_ids)

print("\n" + "=" * 70)
print("QS 2025 <-> THE 2023")
print("=" * 70)

print(f"ID matches: {len(qs_the23):,}")


# ============================================================
# THE 2024 <-> THE 2023
# ============================================================

the24_the23 = the24_ids.intersection(the23_ids)

print("\n" + "=" * 70)
print("THE 2024 <-> THE 2023")
print("=" * 70)

print(f"ID matches: {len(the24_the23):,}")


# ============================================================
# ALL THREE
# ============================================================

all_three = qs_ids.intersection(
    the24_ids,
    the23_ids
)

print("\n" + "=" * 70)
print("ALL THREE DATASETS")
print("=" * 70)

print(f"QS + THE 2024 + THE 2023: {len(all_three):,}")


# ============================================================
# EXPECTED VS ACTUAL
# ============================================================

print("\n" + "=" * 70)
print("EXPECTED VS ACTUAL")
print("=" * 70)

expected = {
    "QS vs THE 2024": 788,
    "QS vs THE 2023": 745,
    "THE 2024 vs THE 2023": 2066,
    "All Three": 722
}

actual = {
    "QS vs THE 2024": len(qs_the24),
    "QS vs THE 2023": len(qs_the23),
    "THE 2024 vs THE 2023": len(the24_the23),
    "All Three": len(all_three)
}

for key in expected:
    status = "✅" if expected[key] == actual[key] else "❌"

    print(
        f"{status} {key}: "
        f"Expected = {expected[key]:,}, "
        f"Actual = {actual[key]:,}"
    )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("ID OVERLAP VALIDATION COMPLETED")
print("=" * 70)