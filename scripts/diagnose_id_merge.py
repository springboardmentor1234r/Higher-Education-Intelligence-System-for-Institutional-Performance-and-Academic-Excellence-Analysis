import pandas as pd
from pathlib import Path

BASE_DIR = Path("data/processed")

MASTER_FILE = BASE_DIR / "university_master.csv"
QS_FILE = BASE_DIR / "qs_2025_with_id.csv"
THE24_FILE = BASE_DIR / "the_2024_with_id.csv"
THE23_FILE = BASE_DIR / "the_2023_with_id.csv"

print("=" * 70)
print("STEP 8E - DIAGNOSING UNIVERSITY ID MERGE")
print("=" * 70)

master = pd.read_csv(MASTER_FILE)
qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE24_FILE)
the23 = pd.read_csv(THE23_FILE)


# ---------------------------------------------------------
# 1. DATA TYPES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("1. UNIVERSITY ID DATA TYPES")
print("=" * 70)

print(f"Master university_id : {master['university_id'].dtype}")
print(f"QS university_id     : {qs['university_id'].dtype}")
print(f"THE 2024 university_id : {the24['university_id'].dtype}")
print(f"THE 2023 university_id : {the23['university_id'].dtype}")


# ---------------------------------------------------------
# 2. SAMPLE IDs
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("2. SAMPLE UNIVERSITY IDs")
print("=" * 70)

print("\nMASTER:")
print(master[["university_id", "university_name"]].head(10).to_string(index=False))

print("\nQS:")
print(qs[["university_id", "university_name"]].head(10).to_string(index=False))

print("\nTHE 2024:")
print(the24[["university_id", "university_name"]].head(10).to_string(index=False))

print("\nTHE 2023:")
print(the23[["university_id", "university_name"]].head(10).to_string(index=False))


# ---------------------------------------------------------
# 3. SET INTERSECTIONS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("3. DIRECT ID SET INTERSECTIONS")
print("=" * 70)

master_ids = set(master["university_id"].astype(str).str.strip())
qs_ids = set(qs["university_id"].astype(str).str.strip())
the24_ids = set(the24["university_id"].astype(str).str.strip())
the23_ids = set(the23["university_id"].astype(str).str.strip())

print(f"Master IDs : {len(master_ids):,}")
print(f"QS IDs     : {len(qs_ids):,}")
print(f"THE24 IDs  : {len(the24_ids):,}")
print(f"THE23 IDs  : {len(the23_ids):,}")

print(f"\nMaster <-> QS 2025   : {len(master_ids & qs_ids):,}")
print(f"Master <-> THE 2024  : {len(master_ids & the24_ids):,}")
print(f"Master <-> THE 2023  : {len(master_ids & the23_ids):,}")


# ---------------------------------------------------------
# 4. MERGE TEST
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("4. ACTUAL PANDAS MERGE TEST")
print("=" * 70)

master_test = master[
    ["university_id", "university_name"]
].copy()

qs_test = qs[
    ["university_id", "qs_rank_2025"]
].copy()

the24_test = the24[
    ["university_id", "the_rank_2024"]
].copy()

the23_test = the23[
    ["university_id", "the_rank_2023"]
].copy()


test_qs = master_test.merge(
    qs_test,
    on="university_id",
    how="left",
    indicator=True
)

test_the24 = master_test.merge(
    the24_test,
    on="university_id",
    how="left",
    indicator=True
)

test_the23 = master_test.merge(
    the23_test,
    on="university_id",
    how="left",
    indicator=True
)

print("\nQS merge:")
print(test_qs["_merge"].value_counts())

print("\nTHE 2024 merge:")
print(test_the24["_merge"].value_counts())

print("\nTHE 2023 merge:")
print(test_the23["_merge"].value_counts())


# ---------------------------------------------------------
# 5. CHECK FIRST COMMON ID
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("5. FIRST COMMON ID TEST")
print("=" * 70)

common_qs = list(master_ids & qs_ids)

if common_qs:
    test_id = common_qs[0]

    print(f"Test ID: {test_id}")

    print("\nMaster row:")
    print(
        master[
            master["university_id"].astype(str).str.strip() == test_id
        ][["university_id", "university_name"]]
        .to_string(index=False)
    )

    print("\nQS row:")
    print(
        qs[
            qs["university_id"].astype(str).str.strip() == test_id
        ][["university_id", "university_name", "qs_rank_2025"]]
        .to_string(index=False)
    )


# ---------------------------------------------------------
# 6. CHECK ID FORMAT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("6. ID FORMAT CHECK")
print("=" * 70)

print("\nMaster first 20 IDs:")
print(master["university_id"].astype(str).head(20).tolist())

print("\nQS first 20 IDs:")
print(qs["university_id"].astype(str).head(20).tolist())

print("\nTHE 2024 first 20 IDs:")
print(the24["university_id"].astype(str).head(20).tolist())

print("\nTHE 2023 first 20 IDs:")
print(the23["university_id"].astype(str).head(20).tolist())


print("\n" + "=" * 70)
print("STEP 8E DIAGNOSTIC COMPLETED")
print("=" * 70)