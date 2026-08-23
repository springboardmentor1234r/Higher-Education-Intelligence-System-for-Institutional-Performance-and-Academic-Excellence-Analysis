import os
import pandas as pd

source_path = "D:\\Tech\\Projects\\Visualization\\Infosis\\QS World University Rankings 2025 (Top global universities).csv"    

# 1. Read the raw dataset
print("Reading raw dataset...")
if source_path.endswith(".xlsx") or source_path.endswith(".xls"):
    df_raw = pd.read_excel(source_path)
else:
    df_raw = pd.read_csv(source_path, encoding='latin-1')
        

# 2. Check completeness target (>95%)
completeness = (1 - (df_raw.isnull().sum().sum() / df_raw.size)) * 100

print(f"Total rows: {len(df_raw)} | Total columns: {df_raw.shape[1]}")
print(f"Raw Completeness: {completeness:.2f}%")


print(f"Missing values: {df_raw.isnull().sum().sum()}")
print(f"Total values: {df_raw.size}")
print(f"Percentage of missing values: {df_raw.isnull().sum().sum() / df_raw.size * 100:.2f}%")

# 3. Check if completeness meets target
if completeness < 95:
    print("Completeness is below the target of 95%.")
else:
    print("Completeness meets the target of 95%.")

# 4. Save the raw dataset to a CSV file
#df_raw.to_csv("university_raw_data.csv", index=False)
print("Saved university_raw_data.csv")
