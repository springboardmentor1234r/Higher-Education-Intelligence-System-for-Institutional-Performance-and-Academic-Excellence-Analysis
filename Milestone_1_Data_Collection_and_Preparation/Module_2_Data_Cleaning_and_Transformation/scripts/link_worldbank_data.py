import pandas as pd

# ============================================
# FILE PATHS
# ============================================
university_file = "data/processed/university_integrated.csv"
worldbank_file = "data/cleaned/edstats_country_cleaned.csv"
mapping_file = "data/processed/country_mapping.csv"

output_file = "data/processed/university_integrated_worldbank.csv"

# ============================================
# LOAD DATA
# ============================================
university = pd.read_csv(university_file)
worldbank = pd.read_csv(worldbank_file)
mapping = pd.read_csv(mapping_file)

print("=" * 70)
print("STEP 8F.3 - WORLD BANK COUNTRY LINKING")
print("=" * 70)

print("\nUniversity dataset:", university.shape)
print("World Bank dataset:", worldbank.shape)
print("Mapping dataset:", mapping.shape)

# ============================================
# STANDARDIZE COUNTRY NAMES
# ============================================
university["country_name_canonical"] = (
    university["country_name_canonical"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

worldbank["country_name_clean"] = (
    worldbank["Short Name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

mapping["university_country"] = (
    mapping["university_country"]
    .astype(str)
    .str.strip()
    .str.lower()
)

mapping["worldbank_country"] = (
    mapping["worldbank_country"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# ============================================
# CREATE COUNTRY MATCH KEY
# ============================================
university["worldbank_match_key"] = (
    university["country_name_canonical"]
)

# Replace only the explicitly mapped countries
country_map = dict(
    zip(
        mapping["university_country"],
        mapping["worldbank_country"]
    )
)

university["worldbank_match_key"] = (
    university["worldbank_match_key"]
    .replace(country_map)
)

# ============================================
# CHECK WORLD BANK DUPLICATE MATCH KEYS
# ============================================
duplicate_wb = worldbank[
    worldbank["country_name_clean"].duplicated(keep=False)
]

print("\nWorld Bank duplicate country names:",
      duplicate_wb.shape[0])

if not duplicate_wb.empty:
    print("\nWARNING: Duplicate World Bank country names:")
    print(
        duplicate_wb[
            ["Country Code", "Short Name"]
        ].to_string(index=False)
    )

# ============================================
# SELECT WORLD BANK COLUMNS
# ============================================
worldbank_selected = worldbank[
    [
        "country_name_clean",
        "Country Code",
        "Short Name",
        "Long Name",
        "2-alpha code",
        "Region",
        "Income Group"
    ]
].copy()

worldbank_selected = worldbank_selected.rename(
    columns={
        "Country Code": "wb_country_code",
        "Short Name": "wb_country_name",
        "Long Name": "wb_long_name",
        "2-alpha code": "wb_2alpha_code",
        "Region": "wb_region",
        "Income Group": "wb_income_group"
    }
)

# ============================================
# MERGE WORLD BANK DATA
# ============================================
before_rows = len(university)

integrated = university.merge(
    worldbank_selected,
    how="left",
    left_on="worldbank_match_key",
    right_on="country_name_clean",
    validate="many_to_one"
)

after_rows = len(integrated)

print("\n" + "=" * 70)
print("MERGE VALIDATION")
print("=" * 70)

print("Rows before merge:", before_rows)
print("Rows after merge:", after_rows)

# ============================================
# REMOVE TECHNICAL MATCH COLUMN
# ============================================
integrated = integrated.drop(
    columns=["country_name_clean"],
    errors="ignore"
)

# ============================================
# CREATE LINK STATUS
# ============================================
integrated["worldbank_linked"] = (
    integrated["wb_country_code"].notna()
)

# ============================================
# LINKAGE STATISTICS
# ============================================
linked_universities = integrated[
    integrated["worldbank_linked"]
]

unlinked_universities = integrated[
    ~integrated["worldbank_linked"]
]

print("\n" + "=" * 70)
print("WORLD BANK LINKAGE SUMMARY")
print("=" * 70)

print(
    "Universities linked to World Bank:",
    len(linked_universities)
)

print(
    "Universities not linked:",
    len(unlinked_universities)
)

print(
    "Linkage rate:",
    round(
        len(linked_universities)
        / len(integrated)
        * 100,
        2
    ),
    "%"
)

# ============================================
# COUNTRY-LEVEL LINKAGE
# ============================================
country_status = (
    integrated[
        [
            "country_name_canonical",
            "worldbank_match_key",
            "worldbank_linked"
        ]
    ]
    .drop_duplicates()
    .sort_values("country_name_canonical")
)

print("\nUnique university countries:",
      country_status.shape[0])

print(
    "Countries linked:",
    country_status["worldbank_linked"].sum()
)

print(
    "Countries not linked:",
    (~country_status["worldbank_linked"]).sum()
)

# ============================================
# DISPLAY UNLINKED COUNTRIES
# ============================================
unlinked_countries = country_status[
    ~country_status["worldbank_linked"]
]

print("\n" + "=" * 70)
print("UNLINKED UNIVERSITY COUNTRIES")
print("=" * 70)

if len(unlinked_countries) > 0:
    print(
        unlinked_countries[
            [
                "country_name_canonical",
                "worldbank_match_key"
            ]
        ].to_string(index=False)
    )
else:
    print("None")

# ============================================
# VALIDATE UNIVERSITY IDS
# ============================================
missing_ids = integrated["university_id"].isna().sum()
duplicate_ids = integrated["university_id"].duplicated().sum()

print("\n" + "=" * 70)
print("UNIVERSITY ID VALIDATION")
print("=" * 70)

print("Missing university IDs:", missing_ids)
print("Duplicate university IDs:", duplicate_ids)

# ============================================
# SAVE OUTPUT
# ============================================
integrated.to_csv(
    output_file,
    index=False
)

print("\nSaved:")
print(output_file)

print("\nFinal shape:", integrated.shape)

# ============================================
# FINAL VALIDATION
# ============================================
if (
    before_rows == after_rows
    and missing_ids == 0
    and duplicate_ids == 0
):
    print("\n" + "=" * 70)
    print("STEP 8F.3 PASSED")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("STEP 8F.3 FAILED")
    print("=" * 70)