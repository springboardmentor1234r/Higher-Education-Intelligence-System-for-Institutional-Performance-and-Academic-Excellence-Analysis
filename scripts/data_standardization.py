import re, pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data_final/dim_university.csv")
def normalize_name(x):
    x=re.sub(r"^the\\s+","",str(x).lower().strip())
    return re.sub(r"[^a-z0-9]","",x)
df["normalized_name"]=df["university_name"].map(normalize_name)
print("Standardized university keys:", df["normalized_name"].notna().sum())
