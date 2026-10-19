from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parent
def generate():
    kpi=pd.read_csv(BASE/"kpi_university_summary.csv",low_memory=False)
    with pd.ExcelWriter(BASE/"university_final_dataset.xlsx",engine="openpyxl") as w:
        kpi.to_excel(w,sheet_name="university_final_dataset",index=False)
        for fn,sheet in [("kpi_availability_and_definitions.csv","kpi_definitions"),("kpi_mapping.csv","kpi_mapping")]:
            p=BASE/fn
            if p.exists(): pd.read_csv(p,low_memory=False).to_excel(w,sheet_name=sheet,index=False)
    print("Created university_final_dataset.xlsx")
if __name__=="__main__": generate()
