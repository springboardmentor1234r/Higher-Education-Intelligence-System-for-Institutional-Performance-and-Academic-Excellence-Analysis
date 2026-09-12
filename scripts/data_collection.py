from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/"data_final"
FILES=["qs_2025_raw.csv","the_2024_raw.csv","wur_2023_raw.csv","world_education_raw.csv"]
for f in FILES:
    p=raw/f
    if p.exists():
        df=pd.read_csv(p); print(f"[verified] {f}: {len(df):,} rows x {df.shape[1]} cols")
    else: print(f"[missing] {f}")
