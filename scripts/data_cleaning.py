from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/"data_final"
for f in ["qs_2025_cleaned.csv","the_2024_cleaned.csv","wur_2023_cleaned.csv","country_education_cleaned.csv"]:
    df=pd.read_csv(raw/f)
    print(f, "duplicates:", df.duplicated().sum(), "missing cells:", int(df.isna().sum().sum()))
