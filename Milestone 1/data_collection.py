from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parent
SOURCES={"QS 2024":BASE/"2024 QS World University Rankings 1.1 (For qs.com).csv","THE 2024":BASE/"TIMES_WorldUniversityRankings_2024.csv","WUR 2023":BASE/"World University Rankings 2023.csv"}
frames=[]
for source,path in SOURCES.items():
    if path.exists():
        df=pd.read_csv(path,low_memory=False); df.insert(0,"source_dataset",source); frames.append(df)
if not frames: raise FileNotFoundError("No ranking CSV files found")
out=pd.concat(frames,ignore_index=True,sort=False); out.to_csv(BASE/"university_raw_data.csv",index=False)
print(f"Wrote {len(out):,} rows")
