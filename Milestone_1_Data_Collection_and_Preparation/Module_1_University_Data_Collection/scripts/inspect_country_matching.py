import pandas as pd

# ==============================
# FILE PATHS
# ==============================
university_file = "data/processed/university_integrated.csv"
worldbank_file = "data/cleaned/edstats_country_cleaned.csv"

# ==============================
# LOAD DATA
# ==============================
university = pd.read_csv(university_file)
worldbank = pd.read_csv(worldbank_file)

print("=" * 70)
print("STEP 8F.1 - COUNTRY MATCHING INSPECTION")
print("=" * 70)

print("\nUniversity Integrated Dataset")
print("Shape:", university.shape)

print("\nWorld Bank Dataset")
print("Shape:", worldbank.shape)

# ==============================
# UNIVERSITY COUNTRIES
# ==============================
university_countries = (
    university["country_name_canonical"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .unique()
)

print("\nUnique university countries:", len(university_countries))

# ==============================
# WORLD BANK COUNTRIES
# ==============================
worldbank_countries = (
    worldbank["Short Name"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .unique()
)

print("Unique World Bank names:", len(worldbank_countries))

# ==============================
# EXACT MATCHES
# ==============================
university_set = set(university_countries)
worldbank_set = set(worldbank_countries)

matched = sorted(university_set.intersection(worldbank_set))
unmatched = sorted(university_set - worldbank_set)

print("\n" + "=" * 70)
print("COUNTRY MATCHING SUMMARY")
print("=" * 70)

print("University unique countries:", len(university_set))
print("World Bank unique names:", len(worldbank_set))
print("Exact matches:", len(matched))
print("Unmatched university countries:", len(unmatched))

# ==============================
# DISPLAY MATCHES
# ==============================
print("\n" + "=" * 70)
print("EXACT MATCHES")
print("=" * 70)

for country in matched:
    print(country)

# ==============================
# DISPLAY UNMATCHED
# ==============================
print("\n" + "=" * 70)
print("UNMATCHED UNIVERSITY COUNTRIES")
print("=" * 70)

for country in unmatched:
    print(country)

# ==============================
# SAVE UNMATCHED
# ==============================
pd.DataFrame({
    "unmatched_country": unmatched
}).to_csv(
    "data/processed/unmatched_worldbank_countries.csv",
    index=False
)

print("\nSaved:")
print("data/processed/unmatched_worldbank_countries.csv")

print("\n" + "=" * 70)
print("STEP 8F.1 COMPLETED")
print("=" * 70)

