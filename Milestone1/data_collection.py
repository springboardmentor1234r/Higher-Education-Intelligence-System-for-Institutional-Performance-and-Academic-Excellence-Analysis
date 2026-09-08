from pathlib import Path
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "Milestone1" / "university_raw_data.csv"


# Dataset files
QS_FILE = RAW_DIR / "QS World University Rankings 2025 (Top global universities).csv"
THE_FILE = RAW_DIR / "TIMES_WorldUniversityRankings_2024.csv"
WUR_FILE = RAW_DIR / "World University Rankings 2023.csv"


def load_csv(file_path):
    """Load a CSV file with UTF-8 or Latin-1 encoding."""
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1")

    print(f"Loaded: {file_path.name} ({df.shape[0]} rows, {df.shape[1]} columns)")
    return df


def load_university_datasets():
    """Load QS, THE and WUR datasets."""
    return (
        load_csv(QS_FILE),
        load_csv(THE_FILE),
        load_csv(WUR_FILE)
    )


def calculate_completeness(df, dataset_name):
    """Calculate overall and column-level dataset completeness."""

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isna().sum().sum()
    completeness = (total_cells - missing_cells) / total_cells * 100

    print("\n" + "=" * 80)
    print(f"DATASET COMPLETENESS: {dataset_name}")
    print("=" * 80)
    print(f"Rows                 : {df.shape[0]}")
    print(f"Columns              : {df.shape[1]}")
    print(f"Missing cells        : {missing_cells}")
    print(f"Overall completeness : {completeness:.2f}%")

    report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percentage": (df.isna().mean() * 100).round(2),
        "completeness_percentage": ((1 - df.isna().mean()) * 100).round(2)
    })

    print("\nColumn-level completeness:")
    print(report.to_string(index=False))

    return report


def collect_qs_indicators(qs):
    """Collect required QS performance indicators."""

    columns = [
        "Institution_Name", "Location", "Region", "RANK_2025",
        "Academic_Reputation_Score", "Employer_Reputation_Score",
        "Faculty_Student_Score", "Citations_per_Faculty_Score",
        "International_Faculty_Score", "International_Students_Score",
        "International_Research_Network_Score", "Employment_Outcomes_Score",
        "Sustainability_Score", "Overall_Score"
    ]

    data = qs[columns].copy()
    data["source"] = "QS"
    data["ranking_year"] = 2025

    return data.rename(columns={
        "Institution_Name": "university_name",
        "Location": "country",
        "Region": "region",
        "RANK_2025": "global_rank",
        "Academic_Reputation_Score": "academic_reputation_score",
        "Employer_Reputation_Score": "employer_reputation_score",
        "Faculty_Student_Score": "faculty_student_score",
        "Citations_per_Faculty_Score": "citations_per_faculty_score",
        "International_Faculty_Score": "international_faculty_score",
        "International_Students_Score": "international_students_score",
        "International_Research_Network_Score": "international_research_network_score",
        "Employment_Outcomes_Score": "employment_outcomes_score",
        "Sustainability_Score": "sustainability_score",
        "Overall_Score": "overall_score"
    })


def collect_the_indicators(the):
    """Collect required THE performance indicators."""

    columns = [
        "name", "location", "rank", "scores_overall",
        "scores_teaching", "scores_research", "scores_citations",
        "scores_industry_income", "scores_international_outlook",
        "stats_number_students", "stats_student_staff_ratio",
        "stats_pc_intl_students", "stats_female_male_ratio"
    ]

    data = the[columns].copy()
    data["source"] = "THE"
    data["ranking_year"] = 2024

    return data.rename(columns={
        "name": "university_name",
        "location": "country",
        "rank": "global_rank",
        "scores_overall": "overall_score",
        "scores_teaching": "teaching_score",
        "scores_research": "research_score",
        "scores_citations": "citations_score",
        "scores_industry_income": "industry_income_score",
        "scores_international_outlook": "international_outlook_score",
        "stats_number_students": "number_of_students",
        "stats_student_staff_ratio": "student_staff_ratio",
        "stats_pc_intl_students": "international_student_percentage",
        "stats_female_male_ratio": "female_male_ratio"
    })


def collect_wur_indicators(wur):
    """Collect required WUR performance indicators."""

    columns = [
        "Name of University", "Location", "University Rank",
        "No of student", "No of student per staff",
        "International Student", "Female:Male Ratio",
        "OverAll Score", "Teaching Score", "Research Score",
        "Citations Score", "Industry Income Score",
        "International Outlook Score"
    ]

    data = wur[columns].copy()
    data["source"] = "WUR"
    data["ranking_year"] = 2023

    return data.rename(columns={
        "Name of University": "university_name",
        "Location": "country",
        "University Rank": "global_rank",
        "No of student": "number_of_students",
        "No of student per staff": "student_staff_ratio",
        "International Student": "international_student_percentage",
        "Female:Male Ratio": "female_male_ratio",
        "OverAll Score": "overall_score",
        "Teaching Score": "teaching_score",
        "Research Score": "research_score",
        "Citations Score": "citations_score",
        "Industry Income Score": "industry_income_score",
        "International Outlook Score": "international_outlook_score"
    })


# Common structure for all three ranking datasets
COMMON_COLUMNS = [
    "university_name", "country", "region", "source", "ranking_year",
    "global_rank", "overall_score",
    "academic_reputation_score", "employer_reputation_score",
    "faculty_student_score", "student_staff_ratio",
    "citations_per_faculty_score", "citations_score",
    "teaching_score", "research_score",
    "industry_income_score", "international_outlook_score",
    "international_faculty_score", "international_students_score",
    "international_student_percentage",
    "international_research_network_score",
    "employment_outcomes_score", "sustainability_score",
    "number_of_students", "female_male_ratio"
]


def create_common_structure(df):
    """Ensure all datasets have the same columns."""
    df = df.copy()

    for column in COMMON_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    return df[COMMON_COLUMNS]


def collect_performance_indicators(qs, the, wur):
    """Collect and standardize the selected indicators."""

    qs_data = create_common_structure(
        collect_qs_indicators(qs)
    )

    the_data = create_common_structure(
        collect_the_indicators(the)
    )

    wur_data = create_common_structure(
        collect_wur_indicators(wur)
    )

    print("\n" + "=" * 80)
    print("COLLECTING UNIVERSITY PERFORMANCE INDICATORS")
    print("=" * 80)
    print(f"QS indicators collected : {len(qs_data)}")
    print(f"THE indicators collected: {len(the_data)}")
    print(f"WUR indicators collected: {len(wur_data)}")

    return qs_data, the_data, wur_data


def combine_datasets(qs_data, the_data, wur_data):
    """Combine QS, THE and WUR into one common structure."""

    combined = pd.concat(
        [qs_data, the_data, wur_data],
        ignore_index=True
    )

    print("\n" + "=" * 80)
    print("CREATING COMMON UNIVERSITY STRUCTURE")
    print("=" * 80)
    print(f"Total source records  : {len(combined)}")
    print(f"Unique university names: {combined['university_name'].nunique()}")

    print("\nRecords by source:")
    print(combined["source"].value_counts())

    return combined


def save_output(df):
    """Save the final Module 1 dataset."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 80)
    print("RAW UNIVERSITY DATA SAVED")
    print("=" * 80)
    print(f"File    : {OUTPUT_FILE}")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")


def main():

    print("\n" + "=" * 80)
    print("EduVision_DV - Module 1")
    print("University Data Collection")
    print("=" * 80)

    qs, the, wur = load_university_datasets()

    # Dataset completeness
    calculate_completeness(
        qs,
        "QS World University Rankings 2025"
    )
    calculate_completeness(
        the,
        "THE World University Rankings 2024"
    )
    calculate_completeness(
        wur,
        "World University Rankings 2023"
    )

    # Collect performance indicators
    qs_data, the_data, wur_data = collect_performance_indicators(
        qs, the, wur
    )

    # Create common structure
    university_raw_data = combine_datasets(
        qs_data, the_data, wur_data
    )

    # Save output
    save_output(university_raw_data)


if __name__ == "__main__":
    main()