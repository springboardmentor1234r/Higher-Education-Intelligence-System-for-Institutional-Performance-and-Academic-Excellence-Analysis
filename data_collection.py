import pandas as pd
import re

# ---------------------------------------------------
# 1. LOAD DATASETS
# ---------------------------------------------------

qs_path = "../data/QS_2024.csv"
the_path = "../data/THE_2024.csv"

qs = pd.read_csv(qs_path)
the = pd.read_csv(the_path)

print("QS original shape:", qs.shape)
print("THE original shape:", the.shape)


# ---------------------------------------------------
# 2. REMOVE EXTRA QS HEADER ROW
# ---------------------------------------------------

qs = qs[qs["Institution Name"] != "institution"].copy()

print("QS after removing extra row:", qs.shape)


# ---------------------------------------------------
# 3. KEEP ACTUAL RANKED THE UNIVERSITIES
# ---------------------------------------------------

the["THE_Rank"] = pd.to_numeric(
    the["rank"].astype(str).str.extract(r"(\d+)")[0],
    errors="coerce"
)

the = the[the["THE_Rank"].notna()].copy()

print("THE ranked universities:", the.shape)


# ---------------------------------------------------
# 4. STANDARDIZE UNIVERSITY NAMES
# ---------------------------------------------------

def normalize_name(value):

    value = str(value).lower().strip()

    # Remove text inside brackets
    value = re.sub(r"\([^)]*\)", "", value)

    # Replace special characters
    value = re.sub(r"[^a-z0-9]+", " ", value)

    # Remove extra spaces
    value = re.sub(r"\s+", " ", value).strip()

    return value


qs["University_Key"] = qs["Institution Name"].apply(normalize_name)
the["University_Key"] = the["name"].apply(normalize_name)


# ---------------------------------------------------
# 5. STANDARDIZE COUNTRY NAMES
# ---------------------------------------------------

qs["Country"] = qs["Country"].astype(str).str.strip()
the["location"] = the["location"].astype(str).str.strip()


# ---------------------------------------------------
# 6. REMOVE DUPLICATE UNIVERSITIES
# ---------------------------------------------------

qs = qs.drop_duplicates(subset="University_Key")
the = the.drop_duplicates(subset="University_Key")


# ---------------------------------------------------
# 7. MERGE QS + THE
# ---------------------------------------------------

merged = pd.merge(
    qs,
    the,
    on="University_Key",
    how="inner",
    suffixes=("_QS", "_THE")
)


# ---------------------------------------------------
# 8. SELECT IMPORTANT COLUMNS
# ---------------------------------------------------

raw_data = merged[
    [
        "University_Key",

        # University information
        "Institution Name",
        "Country",
        "Country Code",

        # QS ranking
        "2024 RANK",
        "Overall SCORE",
        "Academic Reputation Score",
        "Employer Reputation Score",
        "Faculty Student Score",
        "Citations per Faculty Score",
        "International Faculty Score",
        "International Students Score",

        # THE ranking
        "name",
        "location",
        "THE_Rank",
        "scores_overall",
        "scores_teaching",
        "scores_research",
        "scores_citations",
        "scores_industry_income",
        "scores_international_outlook",

        # Student information
        "stats_number_students",
        "stats_student_staff_ratio",
        "stats_pc_intl_students",
        "stats_female_male_ratio"
    ]
].copy()


# ---------------------------------------------------
# 9. RENAME COLUMNS
# ---------------------------------------------------

raw_data = raw_data.rename(
    columns={
        "Institution Name": "University_Name_QS",
        "Country": "Country_QS",
        "Country Code": "Country_Code",

        "2024 RANK": "QS_Rank",
        "Overall SCORE": "QS_Overall_Score",
        "Academic Reputation Score": "QS_Academic_Reputation",
        "Employer Reputation Score": "QS_Employer_Reputation",
        "Faculty Student Score": "QS_Faculty_Student_Score",
        "Citations per Faculty Score": "QS_Citations_Per_Faculty",
        "International Faculty Score": "QS_International_Faculty",
        "International Students Score": "QS_International_Students",

        "name": "University_Name_THE",
        "location": "Country_THE",

        "scores_overall": "THE_Overall_Score",
        "scores_teaching": "THE_Teaching_Score",
        "scores_research": "THE_Research_Score",
        "scores_citations": "THE_Citations_Score",
        "scores_industry_income": "THE_Industry_Income_Score",
        "scores_international_outlook": "THE_International_Outlook",

        "stats_number_students": "Total_Students",
        "stats_student_staff_ratio": "Student_Staff_Ratio",
        "stats_pc_intl_students": "International_Students",
        "stats_female_male_ratio": "Female_Male_Ratio"
    }
)


# ---------------------------------------------------
# 10. ADD YEAR
# ---------------------------------------------------

raw_data["Year"] = 2024


# ---------------------------------------------------
# 11. SAVE RAW MERGED DATA
# ---------------------------------------------------

output_path = "../data/university_raw_data.csv"

raw_data.to_csv(output_path, index=False)

print("\n------------------------------------")
print("DATA COLLECTION COMPLETE")
print("------------------------------------")
print("Final raw dataset shape:", raw_data.shape)
print("Saved:", output_path)