# =====================================================================
# EduVision_DV — Milestone 2
# generate_education_kpis.py  (Colab version)
#
# Builds: university_final_dataset.xlsx
#
# INPUT (upload when prompted):
#   01 University Overview.xlsx   <- MASTER (QS 2025, 1,503 universities)
#   02 Research Analytics.xlsx    <- THE 2024                 (optional, for reference/QA only)
#   03 Student Analytics.xlsx     <- WUR 2023                 (optional, for reference/QA only)
#   04 Country Comparison.xlsx    <- World Bank indicators     (optional, only used if
#                                                                MERGE_COUNTRY_INDICATORS = True)
#   Six KPIs.xlsx                 <- your already-computed 6 KPIs (918 universities, 0 nulls)
#
# LOGIC:
#   university_final_dataset = 01 University Overview  INNER JOIN  Six KPIs   on university_id
#   (INNER join, not LEFT — this is what keeps the result at 0 missing values.
#    Six KPIs only has 918 of the master's 1,503 universities because those are the
#    only ones with a real THE-2024-or-WUR-2023 research source; INNER join keeps
#    exactly that clean subset instead of re-introducing nulls for the other 585.)
#
#   02 and 03 are NOT re-merged here — they were already cascaded into Six KPIs
#   upstream (THE 2024 primary, WUR 2023 fallback), so merging them again would only
#   create duplicate/overlapping columns and reopen the missing-value problem.
#
#   04 Country Comparison is a different grain (country x indicator x year, not
#   university-level). It's optional — set MERGE_COUNTRY_INDICATORS = True below to
#   pivot it to one row per country (latest year per indicator) and attach it.
# =====================================================================

import pandas as pd

# ----------------------------------------------------------------------
# 0. SETTINGS — change these if you want different behaviour
# ----------------------------------------------------------------------
MERGE_COUNTRY_INDICATORS = False   # True -> also attach 04 Country Comparison as extra columns
OUTPUT_FILENAME = "university_final_dataset.xlsx"

# ----------------------------------------------------------------------
# 1. UPLOAD FILES  (Colab file picker)
# ----------------------------------------------------------------------
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

def load_excel(expected_name_hint, required=True):
    """Prompts an upload in Colab and reads the file into a DataFrame.
    Outside Colab, looks for the file in the current directory instead."""
    import os
    if IN_COLAB:
        print(f"\n>>> Please upload: {expected_name_hint}")
        uploaded = files.upload()
        fname = list(uploaded.keys())[0]
        return pd.read_excel(fname)
    else:
        if os.path.exists(expected_name_hint):
            return pd.read_excel(expected_name_hint)
        elif required:
            raise FileNotFoundError(f"Could not find '{expected_name_hint}' in the working directory.")
        else:
            return None

print("="*70)
print("STEP 1 — UPLOAD YOUR 5 DATASETS")
print("="*70)

df_master = load_excel("01 University Overview.xlsx")        # required
df_kpi    = load_excel("Six KPIs.xlsx")                       # required
df_02     = load_excel("02 Research Analytics.xlsx", required=False)   # optional, QA only
df_03     = load_excel("03 Student Analytics.xlsx", required=False)    # optional, QA only
df_04     = load_excel("04 Country Comparison.xlsx",
                        required=MERGE_COUNTRY_INDICATORS)     # required only if merging it in

print(f"\n01 University Overview : {df_master.shape}")
print(f"Six KPIs                : {df_kpi.shape}")
if df_02 is not None:
    print(f"02 Research Analytics   : {df_02.shape}  (loaded for reference only, not merged)")
if df_03 is not None:
    print(f"03 Student Analytics    : {df_03.shape}  (loaded for reference only, not merged)")
if df_04 is not None:
    print(f"04 Country Comparison   : {df_04.shape}")

# ----------------------------------------------------------------------
# 2. VALIDATE THE JOIN KEY BEFORE MERGING
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("STEP 2 — VALIDATE JOIN KEY (university_id)")
print("="*70)

for name, d in [("01 University Overview", df_master), ("Six KPIs", df_kpi)]:
    assert 'university_id' in d.columns, f"'{name}' has no university_id column — cannot merge on it."
    dup = d['university_id'].duplicated().sum()
    print(f"{name}: {len(d)} rows, {dup} duplicate university_id")
    assert dup == 0, f"'{name}' has duplicate university_id — dedupe before merging."

not_in_master = set(df_kpi['university_id']) - set(df_master['university_id'])
print(f"Six KPIs university_ids NOT found in master: {len(not_in_master)} (should be 0)")

# ----------------------------------------------------------------------
# 3. MERGE  (INNER JOIN on university_id — keeps only universities present in BOTH)
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("STEP 3 — MERGE 01 University Overview + Six KPIs (INNER JOIN)")
print("="*70)

final_df = df_master.merge(
    df_kpi,
    on='university_id',
    how='inner',
    suffixes=('', '_kpi')
)

# Drop columns that were duplicated by the merge (same info from both sides,
# e.g. university_name, country_id, country_name, region, overall_score_is_estimated)
# Keep the master's version of each; drop the KPI-side duplicate.
dupe_cols = [c for c in final_df.columns if c.endswith('_kpi')]
if dupe_cols:
    print(f"Dropping {len(dupe_cols)} duplicate columns carried over from Six KPIs: {dupe_cols}")
    final_df = final_df.drop(columns=dupe_cols)

print(f"\nMerged shape: {final_df.shape}")

# ----------------------------------------------------------------------
# 4. OPTIONAL — ATTACH 04 COUNTRY COMPARISON (pivoted to one row per country)
# ----------------------------------------------------------------------
if MERGE_COUNTRY_INDICATORS and df_04 is not None:
    print("\n" + "="*70)
    print("STEP 4 — ATTACH COUNTRY-LEVEL INDICATORS (04 Country Comparison)")
    print("="*70)

    # 04 is country x indicator x year (long format). Take the most recent
    # year available per country+indicator, then pivot to one row per country.
    latest = (df_04.sort_values('year')
                    .groupby(['country_id', 'indicator_code'])
                    .tail(1))
    country_wide = latest.pivot(index='country_id',
                                 columns='indicator_name',
                                 values='value').reset_index()

    before_rows = len(final_df)
    final_df = final_df.merge(country_wide, on='country_id', how='left')
    print(f"Rows before: {before_rows}  |  Rows after: {len(final_df)}  (left join — row count must not change)")
    assert len(final_df) == before_rows, "Row count changed after country merge — check for duplicate country_id in country_wide."

    missing_indicator_countries = final_df[country_wide.columns.drop('country_id')].isna().all(axis=1).sum()
    print(f"Universities with NO country-indicator data available (e.g. Taiwan, Northern Cyprus): {missing_indicator_countries}")
    print("(These are real, documented gaps in the World Bank source — not a bug — left as NaN.)")
else:
    print("\nSTEP 4 — Skipped (MERGE_COUNTRY_INDICATORS = False)")

# ----------------------------------------------------------------------
# 5. FINAL QA CHECKS
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("STEP 5 — FINAL QA")
print("="*70)

n_missing = int(final_df.isna().sum().sum())
n_dupe_ids = int(final_df['university_id'].duplicated().sum())
n_dupe_rows = int(final_df.duplicated().sum())
all_from_master = final_df['university_id'].isin(df_master['university_id']).all()

print(f"Final shape                : {final_df.shape}")
print(f"Missing values             : {n_missing}")
print(f"Duplicate university_id    : {n_dupe_ids}")
print(f"Duplicate full rows        : {n_dupe_rows}")
print(f"Every row traces to master : {all_from_master}")

if not MERGE_COUNTRY_INDICATORS:
    assert n_missing == 0, "Unexpected missing values — check upstream files for changes."
assert n_dupe_ids == 0, "Unexpected duplicate university_id."
assert n_dupe_rows == 0, "Unexpected duplicate rows."
assert all_from_master, "Some rows do not trace back to the master dataset."
print("\nAll QA checks passed.")

# ----------------------------------------------------------------------
# 6. SAVE AND DOWNLOAD
# ----------------------------------------------------------------------
print("\n" + "="*70)
print(f"STEP 6 — SAVE '{OUTPUT_FILENAME}'")
print("="*70)

final_df.to_excel(OUTPUT_FILENAME, index=False)
print(f"Saved: {OUTPUT_FILENAME}")

if IN_COLAB:
    files.download(OUTPUT_FILENAME)
    print("Download triggered.")
else:
    print(f"File written to the current directory: {OUTPUT_FILENAME}")
