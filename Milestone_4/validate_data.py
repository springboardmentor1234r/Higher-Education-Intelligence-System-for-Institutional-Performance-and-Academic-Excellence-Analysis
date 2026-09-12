from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
final=ROOT/"data_final"
for f in sorted(final.glob("*.csv")):
    df=pd.read_csv(f)
    print(f"{f.name}: {len(df):,} x {df.shape[1]}, duplicates={df.duplicated().sum():,}, missing={df.isna().sum().sum():,}")
