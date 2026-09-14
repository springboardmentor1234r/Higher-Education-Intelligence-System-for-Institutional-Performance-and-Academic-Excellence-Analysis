import pandas as pd
from pathlib import Path

print("=" * 70)
print("STEP 8F.8 - VERIFY WORLD BANK MISSING COUNTRIES")
print("=" * 70)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    BASE_DIR / "data" / "raw" /
    "EdStatsData.csv"
)

FINAL_FILE = (
    BASE_DIR / "data" / "processed" /
    "university_integrated_worldbank_education.csv"
)

CODES = [
    "SE.TER.ENRR",
    "SE.TER.CMPL.ZS",
    "SE.TER.ENRL.FE.ZS",
    "UIS.PTRHC.56",
    "SE.ADT.1524.LT.ZS",
    "SE.TER.GRAD"
]

print("\nLoading final university dataset...")

uni = pd.read_csv(FINAL_FILE)

# Countries that have university records but no education indicators
zero_linked = (
    uni[
        uni["worldbank_education_2015_linked"] == False
    ][
        ["country_name", "wb_country_code"]
    ]
    .drop_duplicates()
    .sort_values("country_name")
)

print(
    "\nCountries without any 2015 education indicator:",
    len(zero_linked)
)

print("\nLoading raw World Bank data...")

raw = pd.read_csv(
    RAW_FILE,
    usecols=[
        "Country Name",
        "Country Code",
        "Indicator Code",
        "2015"
    ]
)

# Keep only selected indicators
raw = raw[
    raw["Indicator Code"].isin(CODES)
].copy()

# Normalize codes
raw["Country Code"] = (
    raw["Country Code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print(
    "Raw rows for selected indicators:",
    len(raw)
)

print("\n" + "=" * 70)
print("CHECKING EACH ZERO-LINKED COUNTRY")
print("=" * 70)

results = []

for _, row in zero_linked.iterrows():

    country_name = row["country_name"]
    country_code = row["wb_country_code"]

    if pd.isna(country_code):
        results.append({
            "country_name": country_name,
            "wb_country_code": country_code,
            "country_found_in_raw": False,
            "indicators_with_2015_data": 0,
            "status": "NO WORLD BANK CODE"
        })
        continue

    code = str(country_code).strip().upper()

    country_data = raw[
        raw["Country Code"] == code
    ]

    available = country_data["2015"].notna().sum()

    if len(country_data) == 0:
        status = "COUNTRY NOT FOUND IN SELECTED INDICATORS"
    elif available == 0:
        status = "FOUND BUT NO 2015 DATA"
    else:
        status = "HAS 2015 DATA"

    results.append({
        "country_name": country_name,
        "wb_country_code": code,
        "country_found_in_raw": len(country_data) > 0,
        "indicators_with_2015_data": int(available),
        "status": status
    })

result_df = pd.DataFrame(results)

print(
    result_df.to_string(index=False)
)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    "\nCountries with no WB code:",
    (
        result_df["status"] ==
        "NO WORLD BANK CODE"
    ).sum()
)

print(
    "Countries not found in selected indicators:",
    (
        result_df["status"] ==
        "COUNTRY NOT FOUND IN SELECTED INDICATORS"
    ).sum()
)

print(
    "Countries found but without 2015 data:",
    (
        result_df["status"] ==
        "FOUND BUT NO 2015 DATA"
    ).sum()
)

print(
    "Countries with unexpected 2015 data:",
    (
        result_df["status"] ==
        "HAS 2015 DATA"
    ).sum()
)

# ------------------------------------------------------------
# IMPORTANT VALIDATION
# ------------------------------------------------------------

unexpected = result_df[
    result_df["status"] == "HAS 2015 DATA"
]

if len(unexpected) > 0:

    print("\nWARNING:")
    print(
        "Some countries have 2015 data but were marked "
        "as having no education data."
    )

    print(unexpected.to_string(index=False))

else:

    print(
        "\nPASS: No zero-linked country has unexpected "
        "2015 education data."
    )

print("\n" + "=" * 70)
print("STEP 8F.8 COMPLETED")
print("=" * 70)