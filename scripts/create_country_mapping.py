import pandas as pd

# ============================================
# FILE PATHS
# ============================================
university_file = "data/processed/university_integrated.csv"
worldbank_file = "data/cleaned/edstats_country_cleaned.csv"

# ============================================
# LOAD DATA
# ============================================
university = pd.read_csv(university_file)
worldbank = pd.read_csv(worldbank_file)

print("=" * 70)
print("STEP 8F.2 - COUNTRY MAPPING")
print("=" * 70)

# ============================================
# CREATE STANDARDIZED WORLD BANK NAME
# ============================================
worldbank["country_name_clean"] = (
    worldbank["Short Name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

# ============================================
# COUNTRY NAME MAPPING
# ============================================
country_mapping = {

    # Brunei
    "brunei darussalam": "brunei",

    # Hong Kong
    "hong kong": "hong kong sar, china",

    # Iran
   "iran, islamic republic of": "iran",

    # Kyrgyzstan
    "kyrgyzstan": "kyrgyz republic",

    # Macao
    "macao": "macao sar, china",
    "macau sar": "macao sar, china",

    # North Macedonia
  "north macedonia": "macedonia",

    # Palestine
    "palestine": "west bank and gaza",
    "palestinian territory, occupied": "west bank and gaza",

    # South Korea
    "south korea": "korea",

    # Slovakia
    "slovakia": "slovak republic",

    # Taiwan
    # No forced mapping.
    # World Bank EdStatsCountry may not contain Taiwan
    # as a standard country record.

    # Northern Cyprus
    # No forced mapping.

    # Unknown
    # No mapping.
}

# ============================================
# CHECK WHETHER TARGETS EXIST
# ============================================
print("\n" + "=" * 70)
print("CHECKING MAPPED WORLD BANK NAMES")
print("=" * 70)

for source, target in country_mapping.items():

    exists = target in set(worldbank["country_name_clean"])

    print(
        f"{source:35} -> "
        f"{target:30} | "
        f"{'FOUND' if exists else 'NOT FOUND'}"
    )

# ============================================
# DISPLAY POSSIBLE WORLD BANK NAMES
# ============================================
print("\n" + "=" * 70)
print("WORLD BANK NAMES RELATED TO MAPPING")
print("=" * 70)

keywords = [
    "brunei",
    "hong kong",
    "iran",
    "kyrgyz",
    "macao",
    "macau",
    "macedonia",
    "palest",
    "slovak",
    "korea",
    "taiwan",
    "cyprus"
]

for keyword in keywords:

    matches = worldbank[
        worldbank["country_name_clean"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]["Short Name"].tolist()

    if matches:
        print(f"\n{keyword}:")
        for value in matches:
            print("  ", value)

# ============================================
# SAVE MAPPING
# ============================================
mapping_df = pd.DataFrame(
    list(country_mapping.items()),
    columns=[
        "university_country",
        "worldbank_country"
    ]
)

mapping_df.to_csv(
    "data/processed/country_mapping.csv",
    index=False
)

print("\nSaved:")
print("data/processed/country_mapping.csv")

print("\n" + "=" * 70)
print("STEP 8F.2 COMPLETED")
print("=" * 70)