import pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
kpi=pd.read_csv(ROOT/"data_final/kpi_dataset.csv")
print("KPI rows:",len(kpi))
print("KPI fields:",", ".join(kpi.columns))
