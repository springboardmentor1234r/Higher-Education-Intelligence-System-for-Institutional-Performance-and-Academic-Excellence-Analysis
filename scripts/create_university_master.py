import pandas as pd
from pathlib import Path

# ============================================================
# EDUVISION - CREATE CORRECTED UNIVERSITY MASTER
# ============================================================

BASE_DIR = Path("data/processed")

QS_FILE = BASE_DIR / "qs_2025_common.csv"
THE_2024_FILE = BASE_DIR / "the_2024_common.csv"
THE_2023_FILE = BASE_DIR / "the_2023_common.csv"

OUTPUT_FILE = BASE_DIR / "university_master.csv"


# ============================================================
# STEP 1 - LOAD DATA
# ============================================================

print("=" * 70)
print("STEP 1 - LOADING UNIVERSITY DATA")
print("=" * 70)

qs = pd.read_csv(QS_FILE)
the24 = pd.read_csv(THE_2024_FILE)
the23 = pd.read_csv(THE_2023_FILE)

print(f"QS 2025:  {len(qs):,}")
print(f"THE 2024: {len(the24):,}")
print(f"THE 2023: {len(the23):,}")


# ============================================================
# STEP 2 - CREATE MASTER BASE
# ============================================================

print("\n" + "=" * 70)
print("STEP 2 - CREATING UNIVERSITY MASTER BASE")
print("=" * 70)

# Keep QS first because QS has the most complete country information.
qs_master = qs[
    [
        "university_name",
        "university_name_clean",
        "country_name",
        "country_name_clean",
        "country_code"
    ]
].copy()

the24_master = the24[
    [
        "university_name",
        "university_name_clean",
        "country_name",
        "country_name_clean"
    ]
].copy()

the23_master = the23[
    [
        "university_name",
        "university_name_clean",
        "country_name",
        "country_name_clean"
    ]
].copy()


# ============================================================
# STEP 3 - COMBINE ALL UNIVERSITIES
# ============================================================

all_universities = pd.concat(
    [
        qs_master,
        the24_master,
        the23_master
    ],
    ignore_index=True
)

print(
    f"Total records before deduplication: "
    f"{len(all_universities):,}"
)


# ============================================================
# STEP 4 - KEEP ONE MASTER RECORD PER UNIVERSITY NAME
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 - CREATING UNIQUE UNIVERSITY MASTER")
print("=" * 70)

all_universities = all_universities.drop_duplicates(
    subset=["university_name_clean"],
    keep="first"
).copy()

print(
    f"Unique universities: "
    f"{len(all_universities):,}"
)


# ============================================================
# STEP 5 - STANDARDIZE TEXT
# ============================================================

all_universities["university_name"] = (
    all_universities["university_name"]
    .astype(str)
    .str.strip()
)

all_universities["university_name_clean"] = (
    all_universities["university_name_clean"]
    .astype(str)
    .str.strip()
    .str.lower()
)

all_universities["country_name"] = (
    all_universities["country_name"]
    .astype(str)
    .str.strip()
)

all_universities["country_name_clean"] = (
    all_universities["country_name_clean"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# STEP 6 - CREATE COUNTRY CANONICAL NAME
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 - CREATING CANONICAL COUNTRY NAMES")
print("=" * 70)


def canonical_country(country):

    if pd.isna(country):
        return country

    country = str(country).strip().lower()

    country_mapping = {

        # China variations
        "china (mainland)": "china",
        "mainland china": "china",

        # Hong Kong variations
        "hong kong sar": "hong kong",
        "hong kong s.a.r.": "hong kong",

        # Macau variations
        "macao sar": "macao",
        "macao sar, china": "macao",

        # United States variations
        "usa": "united states",
        "u.s.a.": "united states",
        "us": "united states",

        # United Kingdom variations
        "uk": "united kingdom",
        "u.k.": "united kingdom",

        # Korea variations
        "south korea": "south korea",
        "korea, south": "south korea",
        "republic of korea": "south korea",

        # Russia variations
        "russian federation": "russia"
    }

    return country_mapping.get(country, country)


all_universities["country_name_canonical"] = (
    all_universities["country_name_clean"]
    .apply(canonical_country)
)


# ============================================================
# STEP 7 - CREATE UNIVERSITY IDs
# ============================================================

print("\n" + "=" * 70)
print("STEP 7 - CREATING UNIVERSITY IDs")
print("=" * 70)

all_universities = all_universities.reset_index(drop=True)

all_universities.insert(
    0,
    "university_id",
    [
        f"U{i:04d}"
        for i in range(1, len(all_universities) + 1)
    ]
)

print(
    f"University IDs created: "
    f"{all_universities['university_id'].nunique():,}"
)


# ============================================================
# STEP 8 - VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 8 - MASTER VALIDATION")
print("=" * 70)

print(
    "Missing university IDs:",
    all_universities["university_id"].isna().sum()
)

print(
    "Duplicate university IDs:",
    all_universities["university_id"].duplicated().sum()
)

print(
    "Missing university names:",
    all_universities["university_name"].isna().sum()
)

print(
    "Duplicate university names:",
    all_universities["university_name_clean"].duplicated().sum()
)

print(
    "Missing canonical countries:",
    all_universities["country_name_canonical"].isna().sum()
)


# ============================================================
# STEP 9 - SAVE MASTER
# ============================================================

print("\n" + "=" * 70)
print("STEP 9 - SAVING UNIVERSITY MASTER")
print("=" * 70)

all_universities.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"Saved: {OUTPUT_FILE}")
print(f"Final shape: {all_universities.shape}")


# ============================================================
# STEP 10 - SAMPLE
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE MASTER RECORDS")
print("=" * 70)

print(
    all_universities[
        [
            "university_id",
            "university_name",
            "country_name",
            "country_name_canonical"
        ]
    ].head(10).to_string(index=False)
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("CORRECTED UNIVERSITY MASTER CREATED")
print("=" * 70)

print("Primary university matching key:")
print("university_name_clean")

print("Country normalization:")
print("country_name_canonical")

print("No fuzzy matching used.")