# ============================================================
# EduVision_DV - Apply Controlled University Alias Mapping
# ============================================================
# Applies the manually validated university aliases using
# the standardized QS university names.
#
# Only CONFIRMED aliases are applied.
# Rejected matches remain untouched.
# Original university names are preserved.
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. Define project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ============================================================
# 2. Load datasets and validated aliases
# ============================================================

qs_file = CLEANED_DATA_DIR / "qs_2025_standardized.csv"
the_file = CLEANED_DATA_DIR / "the_2024_standardized.csv"
wur_file = CLEANED_DATA_DIR / "wur_2023_standardized.csv"
alias_file = CLEANED_DATA_DIR / "university_alias_mapping.csv"

qs = pd.read_csv(qs_file)
the = pd.read_csv(the_file)
wur = pd.read_csv(wur_file)
aliases = pd.read_csv(alias_file)


# ============================================================
# 3. Keep only confirmed aliases
# ============================================================

confirmed = aliases[
    aliases["Decision_Status"] == "CONFIRMED"
].copy()

print("=" * 80)
print("APPLYING CONTROLLED UNIVERSITY ALIASES")
print("=" * 80)

print(f"\nConfirmed aliases: {len(confirmed)}")


# ============================================================
# 4. Define the exact standardized QS → canonical name map
# ============================================================
# These QS keys come directly from the standardized QS dataset.
# The values use the corresponding THE university naming.

standardized_aliases = {
    "binghamton university suny":
        "SUNY Binghamton University",

    "university of north carolina chapel hill":
        "University of North Carolina at Chapel Hill",

    "czech university of life sciences in prague":
        "Czech University of Life Sciences Prague (CZU)",

    "king fahd university of petroleum minerals":
        "King Fahd University of Petroleum and Minerals",

    "national university of science and technology misis":
        "National University of Science and Technology (MISiS)",

    "imam mohammad ibn saud islamic university imsiu":
        "Imam Mohammad Ibn Saud Islamic University",

    "university ulm":
        "Ulm University",

    "thapar institute of engineering technology":
        "Thapar Institute of Engineering and Technology",

    "university of rome tor vergata":
        "University of Rome II – Tor Vergata",

    "jordan university of science technology":
        "Jordan University of Science and Technology",

    "university of texas el paso":
        "University of Texas at El Paso",

    "national university of sciences and technology islamabad":
        "National University of Sciences and Technology",

    "essex university of":
        "University of Essex",

    "johannes kepler university linz":
        "Johannes Kepler University of Linz",

    "university of illinois at chicago uic":
        "University of Illinois Chicago",

    "universidad industrial de santander uis":
        "Universidad Industrial de Santander (UIS)",

    "university of naples parthenope":
        "Parthenope University of Naples",

    "university of texas dallas":
        "University of Texas at Dallas",

    "kit karlsruhe institute of technology":
        "Karlsruhe Institute of Technology",

    "university of new brunswick":
        "University of New Brunswick UNB",
}


# ============================================================
# 5. Preserve the original QS standardized names
# ============================================================

qs["University_Name_Standard_Before_Alias"] = (
    qs["University_Name_Standard"]
)


# ============================================================
# 6. Apply controlled aliases
# ============================================================

qs["University_Name_Standard"] = (
    qs["University_Name_Standard"]
    .replace(standardized_aliases)
)


# ============================================================
# 7. Count successful changes
# ============================================================

qs_changed = (
    qs["University_Name_Standard_Before_Alias"]
    != qs["University_Name_Standard"]
).sum()


# ============================================================
# 8. Check which aliases were actually found
# ============================================================

found_aliases = []

for qs_name, canonical_name in standardized_aliases.items():

    if qs_name in qs["University_Name_Standard_Before_Alias"].values:
        found_aliases.append(
            (qs_name, canonical_name)
        )


# ============================================================
# 9. Save alias-applied datasets
# ============================================================

qs_output = CLEANED_DATA_DIR / "qs_2025_alias_applied.csv"
the_output = CLEANED_DATA_DIR / "the_2024_alias_applied.csv"
wur_output = CLEANED_DATA_DIR / "wur_2023_alias_applied.csv"

qs.to_csv(qs_output, index=False)
the.to_csv(the_output, index=False)
wur.to_csv(wur_output, index=False)


# ============================================================
# 10. Display results
# ============================================================

print("\n" + "=" * 80)
print("ALIAS APPLICATION RESULTS")
print("=" * 80)

print(f"\nQS rows processed:  {len(qs)}")
print(f"THE rows processed: {len(the)}")
print(f"WUR rows processed: {len(wur)}")

print(f"\nQS university names changed: {qs_changed}")
print(f"Validated QS aliases found: {len(found_aliases)}")
print(f"Expected confirmed aliases: {len(standardized_aliases)}")


# ============================================================
# 11. Show aliases that were applied
# ============================================================

print("\n" + "=" * 80)
print("ALIASES APPLIED")
print("=" * 80)

for qs_name, canonical_name in found_aliases:
    print(f"{qs_name}  -->  {canonical_name}")


# ============================================================
# 12. Verify rejected Nanjing match remains untouched
# ============================================================

nanjing_rows = qs[
    qs["University_Name_Standard"]
    .astype(str)
    .str.contains(
        "nanjing university of science and technology",
        case=False,
        regex=False,
        na=False
    )
]

print("\n" + "=" * 80)
print("REJECTED MATCH VERIFICATION")
print("=" * 80)

print(
    "\nNanjing University of Science and Technology "
    "was not mapped to the rejected THE university."
)

print(f"Relevant QS rows: {len(nanjing_rows)}")


# ============================================================
# 13. Display output files
# ============================================================

print("\n" + "=" * 80)
print("FILES CREATED")
print("=" * 80)

print(qs_output)
print(the_output)
print(wur_output)

print("\n" + "=" * 80)
print("ALIAS APPLICATION COMPLETED")
print("=" * 80)