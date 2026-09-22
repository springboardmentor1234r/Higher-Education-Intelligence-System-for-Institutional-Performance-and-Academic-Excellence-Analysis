import time
import requests
import pandas as pd

INPUT_FILE = (
    "Milestone_1_Data_Collection_and_Preparation/"
    "Module_2_Data_Cleaning_and_Transformation/"
    "data/university_integrated_worldbank_education.csv"
)

OUTPUT_FILE = "data/publications/raw/openalex_institutions.csv"

YEARS = [2023, 2024, 2025]

session = requests.Session()
session.headers.update({
    "User-Agent": "EduVision university publication analysis"
})


def search_institution(name, country_code=None):
    """Search OpenAlex for an institution and return the best matching result."""

    url = "https://api.openalex.org/institutions"

    params = {
        "search": name,
        "per-page": 10
    }

    try:
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None

        # Prefer an exact country-code match when available.
        if country_code:
            for result in results:
                if result.get("country_code") == country_code:
                    return result

        # Otherwise use the first OpenAlex result.
        return results[0]

    except requests.RequestException as e:
        print(f"Request error for {name}: {e}")
        return None


def get_year_count(counts_by_year, year):
    """Extract publication count for a specific year."""

    for item in counts_by_year or []:
        if item.get("year") == year:
            return item.get("works_count")

    return None


def main():

    print("Loading EduVision university dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Universities found: {len(df)}")

    records = []

    for index, row in df.iterrows():

        university_id = row["university_id"]
        university_name = row["university_name"]
        country_name = row["country_name"]

        print(
            f"[{index + 1}/{len(df)}] "
            f"{university_name} | {country_name}"
        )

        result = search_institution(university_name)

        if result:

            country_code = result.get("country_code")

            # If the first result's country does not match our
            # university country, try searching with the country name.
            if (
                country_name
                and result.get("geo")
                and result["geo"].get("country")
                and result["geo"].get("country") != country_name
            ):
                result2 = search_institution(
                    f"{university_name} {country_name}"
                )

                if result2:
                    result = result2
                    country_code = result.get("country_code")

            counts = result.get("counts_by_year", [])

            record = {
                "university_id": university_id,
                "university_name": university_name,
                "country_name": country_name,
                "openalex_id": result.get("id"),
                "openalex_display_name": result.get("display_name"),
                "openalex_country_code": country_code,
                "openalex_country": (
                    result.get("geo", {}) or {}
                ).get("country"),
                "openalex_ror": result.get("ror"),
                "openalex_works_count": result.get("works_count"),
            }

            for year in YEARS:
                record[f"openalex_works_{year}"] = get_year_count(
                    counts,
                    year
                )

        else:

            record = {
                "university_id": university_id,
                "university_name": university_name,
                "country_name": country_name,
                "openalex_id": None,
                "openalex_display_name": None,
                "openalex_country_code": None,
                "openalex_country": None,
                "openalex_ror": None,
                "openalex_works_count": None,
            }

            for year in YEARS:
                record[f"openalex_works_{year}"] = None

        records.append(record)

        # Small delay to avoid sending requests too quickly.
        time.sleep(0.2)

        # Save progress every 100 universities.
        if (index + 1) % 100 == 0:

            progress_df = pd.DataFrame(records)

            progress_df.to_csv(
                OUTPUT_FILE,
                index=False
            )

            print(
                f"Progress saved: {index + 1} universities"
            )

    final_df = pd.DataFrame(records)

    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nCollection completed.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Rows collected: {len(final_df)}")
    print(
        "Matched OpenAlex institutions:",
        final_df["openalex_id"].notna().sum()
    )


if __name__ == "__main__":
    main()