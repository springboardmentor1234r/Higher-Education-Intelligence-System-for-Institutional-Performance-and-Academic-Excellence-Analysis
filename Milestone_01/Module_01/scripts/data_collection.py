from pathlib import Path
import subprocess
import sys


# ============================================================
# EDUVISION_DV - MODULE 1: DATA COLLECTION
# ============================================================
#
# Purpose:
#     Download the four approved EduVision_DV datasets
#     directly from Kaggle and store them as raw data.
#
# This script does NOT:
#     - clean data
#     - remove duplicates
#     - merge datasets
#     - perform fuzzy matching
#     - calculate KPIs
#     - modify raw datasets
# ============================================================


# ------------------------------------------------------------
# 1. PROJECT DIRECTORIES
# ------------------------------------------------------------

# Project root = folder containing this script's parent directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Raw dataset directory
RAW_DIR = PROJECT_DIR / "university_raw_data"

# Create raw dataset directory if it doesn't exist
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. APPROVED KAGGLE DATASETS
# ------------------------------------------------------------

DATASETS = {
    "QS_2025": {
        "kaggle_id": "melissamonfared/qs-world-university-rankings-2025",
        "folder": RAW_DIR / "QS_2025"
    },

    "THE_2024": {
        "kaggle_id": "ddosad/timesworlduniversityrankings2024",
        "folder": RAW_DIR / "THE_2024"
    },

    "WUR_2023": {
        "kaggle_id": "alitaqi000/world-university-rankings-2023",
        "folder": RAW_DIR / "WUR_2023"
    },

    "World_Bank": {
        "kaggle_id": "theworldbank/education-statistics",
        "folder": RAW_DIR / "World_Bank"
    }
}


# ------------------------------------------------------------
# 3. CHECK KAGGLE INSTALLATION
# ------------------------------------------------------------

def check_kaggle():
    """
    Check whether the Kaggle CLI is installed.
    """

    result = subprocess.run(
        [sys.executable, "-m", "kaggle", "--version"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("ERROR: Kaggle CLI is not installed.")
        print()
        print("Install it using:")
        print("pip install kaggle")
        sys.exit(1)

    print("Kaggle CLI detected:")
    print(result.stdout.strip())
    print()


# ------------------------------------------------------------
# 4. DOWNLOAD ONE DATASET
# ------------------------------------------------------------

def download_dataset(dataset_name, kaggle_id, destination):
    """
    Download and extract one Kaggle dataset.
    """

    print("=" * 70)
    print(f"DATASET: {dataset_name}")
    print(f"Kaggle ID: {kaggle_id}")
    print(f"Destination: {destination}")
    print("=" * 70)

    # Create destination folder
    destination.mkdir(parents=True, exist_ok=True)

    # Check whether files already exist
    existing_files = list(destination.iterdir())

    if existing_files:
        print("STATUS: Files already exist.")
        print("Skipping download to avoid overwriting raw data.")
        print()
        return True

    command = [
        sys.executable,
        "-m",
        "kaggle",
        "datasets",
        "download",
        "-d",
        kaggle_id,
        "-p",
        str(destination),
        "--unzip"
    ]

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"SUCCESS: {dataset_name} downloaded.")
        print()
        return True

    print(f"FAILED: Could not download {dataset_name}.")
    print()
    return False


# ------------------------------------------------------------
# 5. MAIN PROGRAM
# ------------------------------------------------------------

def main():

    print()
    print("=" * 70)
    print("EDUVISION_DV - MODULE 1: DATA COLLECTION")
    print("=" * 70)
    print()

    # Check Kaggle
    check_kaggle()

    successful = []
    failed = []

    # Download each approved dataset
    for dataset_name, details in DATASETS.items():

        success = download_dataset(
            dataset_name,
            details["kaggle_id"],
            details["folder"]
        )

        if success:
            successful.append(dataset_name)
        else:
            failed.append(dataset_name)

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DATA COLLECTION SUMMARY")
    print("=" * 70)

    print()
    print(f"Successful datasets : {len(successful)}")
    print(f"Failed datasets     : {len(failed)}")

    print()

    if successful:
        print("SUCCESSFUL:")
        for dataset in successful:
            print(f"  [OK] {dataset}")

    print()

    if failed:
        print("FAILED:")
        for dataset in failed:
            print(f"  [FAILED] {dataset}")

    print()
    print("=" * 70)

    if not failed:
        print("MODULE 1 DATA COLLECTION COMPLETED SUCCESSFULLY.")
    else:
        print("MODULE 1 COMPLETED WITH DOWNLOAD ERRORS.")
        print("Check the failed dataset(s) before continuing.")

    print("=" * 70)
    print()


# ------------------------------------------------------------
# 6. PROGRAM ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()