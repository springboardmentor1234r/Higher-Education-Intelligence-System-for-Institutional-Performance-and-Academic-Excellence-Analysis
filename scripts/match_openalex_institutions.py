import re
import unicodedata
import pandas as pd
from difflib import SequenceMatcher


INPUT_FILE = "data/publications/raw/openalex_institutions.csv"
OUTPUT_FILE = "data/publications/processed/openalex_publications_review.csv"


# Common abbreviations and aliases
ALIASES = {
    "mit": "massachusetts institute of technology",
    "nus": "national university of singapore",
    "ucl": "university college london",
    "epfl": "ecole polytechnique federale de lausanne",
    "ucla": "university of california los angeles",
    "ucsd": "university of california san diego",
    "ucb": "university of california berkeley",
    "nyu": "new york university",
    "unsw sydney": "university of new south wales",
    "ntu": "nanyang technological university",
    "caltech": "california institute of technology",
    "kth": "kth royal institute of technology",
}


def normalize(text):
    """Normalize university names for comparison."""

    if pd.isna(text):
        return ""

    text = str(text).lower().strip()

    # Remove accents
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    # Replace aliases
    for alias, replacement in ALIASES.items():
        text = re.sub(
            rf"\b{re.escape(alias)}\b",
            replacement,
            text
        )

    # Remove bracketed abbreviations
    text = re.sub(r"\([^)]*\)", " ", text)

    # Remove punctuation
    text = re.sub(r"[^a-z0-9 ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove common leading words
    text = re.sub(r"^the ", "", text)

    return text


def similarity(a, b):
    """Return name similarity from 0 to 1."""

    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0

    if a == b:
        return 1.0

    return SequenceMatcher(None, a, b).ratio()


def main():

    print("Loading existing OpenAlex results...")

    df = pd.read_csv(INPUT_FILE)

    print("Rows:", len(df))

    # Calculate normalized names
    df["normalized_university_name"] = (
        df["university_name"].apply(normalize)
    )

    df["normalized_openalex_name"] = (
        df["openalex_display_name"].apply(normalize)
    )

    # Calculate name similarity
    df["name_similarity"] = df.apply(
        lambda row: similarity(
            row["university_name"],
            row["openalex_display_name"]
        )
        if pd.notna(row["openalex_id"])
        else 0,
        axis=1
    )

    # Country consistency
    df["country_match"] = (
        df["openalex_country_code"].notna()
    )

    # Strict validation
    def classify(row):

        if pd.isna(row["openalex_id"]):
            return "Unmatched"

        score = row["name_similarity"]

        if score >= 0.90:
            return "Validated"

        if score >= 0.70:
            return "Review"

        return "Rejected"

    df["publication_match_status"] = df.apply(
        classify,
        axis=1
    )

    # Remove publication values from rejected matches
    rejected = df["publication_match_status"].isin(
        ["Rejected", "Unmatched"]
    )

    publication_columns = [
        "openalex_id",
        "openalex_display_name",
        "openalex_country_code",
        "openalex_country",
        "openalex_ror",
        "openalex_works_count",
        "openalex_works_2023",
        "openalex_works_2024",
        "openalex_works_2025",
    ]

    df.loc[
        rejected,
        publication_columns
    ] = pd.NA

    # Save review dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nSaved:")
    print(OUTPUT_FILE)

    print("\nMatch status:")
    print(
        df["publication_match_status"]
        .value_counts()
        .to_string()
    )

    print("\nSimilarity statistics:")
    print(
        df["name_similarity"]
        .describe()
        .to_string()
    )


if __name__ == "__main__":
    main()