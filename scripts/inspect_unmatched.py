# ============================================================
# EduVision_DV - Unmatched University Inspection
# ============================================================
# This script identifies possible university-name variations
# that were not matched by exact standardized names.
#
# It does NOT modify any dataset.
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"


# ------------------------------------------------------------
# Load standardized datasets
# ------------------------------------------------------------

qs = pd.read_csv(
    CLEANED_DATA_DIR / "qs_2025_standardized.csv"
)

the = pd.read_csv(
    CLEANED_DATA_DIR / "the_2024_standardized.csv"
)

wur = pd.read_csv(
    CLEANED_DATA_DIR / "wur_2023_standardized.csv"
)


# ------------------------------------------------------------
# Remove missing standardized names
# ------------------------------------------------------------

qs = qs[qs["University_Name_Standard"].notna()].copy()
the = the[the["University_Name_Standard"].notna()].copy()
wur = wur[wur["University_Name_Standard"].notna()].copy()


# ------------------------------------------------------------
# Create name sets
# ------------------------------------------------------------

qs_names = set(qs["University_Name_Standard"])
the_names = set(the["University_Name_Standard"])
wur_names = set(wur["University_Name_Standard"])


# ------------------------------------------------------------
# Find pairwise unmatched universities
# ------------------------------------------------------------

qs_not_the = sorted(qs_names - the_names)
qs_not_wur = sorted(qs_names - wur_names)

the_not_qs = sorted(the_names - qs_names)
the_not_wur = sorted(the_names - wur_names)

wur_not_qs = sorted(wur_names - qs_names)
wur_not_the = sorted(wur_names - the_names)


# ------------------------------------------------------------
# Print counts
# ------------------------------------------------------------

print("=" * 80)
print("UNMATCHED UNIVERSITY INSPECTION")
print("=" * 80)

print("\nQS not in THE:", len(qs_not_the))
print("QS not in WUR:", len(qs_not_wur))

print("\nTHE not in QS:", len(the_not_qs))
print("THE not in WUR:", len(the_not_wur))

print("\nWUR not in QS:", len(wur_not_qs))
print("WUR not in THE:", len(wur_not_the))


# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

def show_original_records(df, names, dataset_name, limit=40):

    print("\n" + "=" * 80)
    print(dataset_name)
    print("=" * 80)

    subset = df[
        df["University_Name_Standard"].isin(names)
    ][
        [
            "University_Name_Original",
            "University_Name_Standard",
            "Country_Standard",
        ]
    ].drop_duplicates()

    print(subset.head(limit).to_string(index=False))


# ------------------------------------------------------------
# Show QS universities not found in THE
# ------------------------------------------------------------

show_original_records(
    qs,
    qs_not_the,
    "QS UNIVERSITIES NOT FOUND IN THE",
)


# ------------------------------------------------------------
# Show QS universities not found in WUR
# ------------------------------------------------------------

show_original_records(
    qs,
    qs_not_wur,
    "QS UNIVERSITIES NOT FOUND IN WUR",
)


# ------------------------------------------------------------
# Show THE universities not found in QS
# ------------------------------------------------------------

show_original_records(
    the,
    the_not_qs,
    "THE UNIVERSITIES NOT FOUND IN QS",
)


# ------------------------------------------------------------
# Show WUR universities not found in QS
# ------------------------------------------------------------

show_original_records(
    wur,
    wur_not_qs,
    "WUR UNIVERSITIES NOT FOUND IN QS",
)


# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("UNMATCHED UNIVERSITY INSPECTION COMPLETED")
print("=" * 80)