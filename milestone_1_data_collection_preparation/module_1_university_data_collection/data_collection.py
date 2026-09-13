import pandas as pd

qs = pd.read_csv("data/raw/qs_2025.csv")
the = pd.read_csv("data/raw/the_2024.csv")
wur = pd.read_csv("data/raw/wur_2023.csv")

qs_common = pd.DataFrame({
    "university_name": qs["institution_name"],
    "country": qs["location"],
    "rank": qs["rank_2025"],
    "source": "QS"
})

the_common = pd.DataFrame({
    "university_name": the["name"],
    "country": the["location"],
    "rank": the["rank"],
    "source": "THE"
})

wur_common = pd.DataFrame({
    "university_name": wur["name_of_university"],
    "country": wur["location"],
    "rank": wur["university_rank"],
    "source": "WUR"
})

university_raw_data = pd.concat(
    [qs_common, the_common, wur_common],
    ignore_index=True
)

university_raw_data.to_csv(
    "university_raw_data.csv",
    index=False
)

print("Data collection completed")