
import pandas as pd

# Define base paths using raw string prefixes
SOURCE_BASE = r"D:\Tech\Projects\Visualization\Infosis"
DEST_BASE = r"D:\Tech\Projects\Visualization\Infosis\Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis\Milestone_1\raw"

# Dataset configuration mapping
DATASETS = {
    "QS World University Rankings 2025": {
        "source": SOURCE_BASE + r"\QS World University Rankings 2025 (Top global universities).csv",
        "dest": DEST_BASE + r"\qs_2025_raw.csv"
    },
    "THE World University Rankings 2024": {
        "source": SOURCE_BASE + r"\TIMES_WorldUniversityRankings_2024.csv",
        "dest": DEST_BASE + r"\the_2024_raw.csv"
    },
    "World University Rankings 2023": {
        "source": SOURCE_BASE + r"\World University Rankings 2023.csv",
        "dest": DEST_BASE + r"\wur_2023_raw.csv"
    }
}

print("=" * 70)
print("HIGHER EDUCATION INTELLIGENCE SYSTEM - DATA COLLECTION AUDIT")
print("=" * 70)


for name, paths in DATASETS.items():
    source_path = paths["source"]
    dest_path = paths["dest"]

    print(f"\nProcessing: {name}")

    # 1. Read the dataset
    try:
        if source_path.endswith((".xlsx", ".xls")):
            df_raw = pd.read_excel(source_path)
        else:
            df_raw = pd.read_csv(source_path, encoding="latin-1", low_memory=False)
    except Exception as e:
        print(f"  [X] Could not read file: {e}")
        continue

    # 2. Check metrics and completeness (>95%)
    total_cells = df_raw.size
    missing_cells = df_raw.isnull().sum().sum()
    completeness = (1 - (missing_cells / total_cells)) * 100

    print(f"  - Rows: {df_raw.shape[0]} | Columns: {df_raw.shape[1]}")
    print(f"  - Missing Values: {missing_cells:,} / {total_cells:,} ({missing_cells / total_cells * 100:.2f}%)")
    print(f"  - Completeness: {completeness:.2f}%")

    if completeness >= 95.0:
        print("  - Status: Target MET (>= 95%)")
    else:
        print("  - Status: Target BELOW 95%")


#  3. Export raw copy to destination
    try:
       df_raw.to_csv(dest_path, index=False)
       print(f"  - Saved to: {dest_path}")
    except Exception as e:
        print(f"  [X] Could not save destination file: {e}")

print("\n" + "=" * 70)
print("Data collection script execution finished.")
print("=" * 70)


# 1. Load the file
df_wb = pd.read_csv(r"D:\Tech\Projects\Visualization\Infosis\EdStatsData.csv", low_memory=False)

# 2. Select key education indicators mentioned in the brief
KEY_INDICATORS = [
    "Government expenditure on education, total (% of GDP)",
    "Gross enrolment ratio, tertiary, both sexes (%)",
    "School enrollment, tertiary (gross), gender parity index (GPI)",
    "Pupil-teacher ratio, tertiary",
    "Adult literacy rate, population 15+ years, both sexes (%)"
]

df_filtered = df_wb[df_wb['Indicator Name'].isin(KEY_INDICATORS)].copy()

# 3. Select metadata + recent years (e.g., 2015 to 2023)
year_cols = [str(yr) for yr in range(2015, 2024) if str(yr) in df_filtered.columns]
meta_cols = ['Country Name', 'Country Code', 'Indicator Name']

df_subset = df_filtered[meta_cols + year_cols]

# 4. Melt (unpivot) wide year columns into long format
df_long = df_subset.melt(
    id_vars=['Country Name', 'Country Code', 'Indicator Name'],
    value_vars=year_cols,
    var_name='year',
    value_name='value'
)

# 5. Clean up missing values and format
df_long = df_long.dropna(subset=['value'])
df_long.rename(columns={'Country Name': 'country_name', 'Indicator Name': 'indicator'}, inplace=True)

# Save to destination
df_long.to_csv(r"D:\Tech\Projects\Visualization\Infosis\Higher-Education-Intelligence-System-for-Institutional-Performance-and-Academic-Excellence-Analysis\Milestone_1\raw\world_bank_education_raw.csv", index=False)
print("Saved reshaped World Bank dataset with columns:", df_long.columns.tolist())


