"""
EduVision_DV - data_collection.py
---------------------------------
Downloads ONLY the four approved raw datasets required by EduVision_DV.

Datasets:
1. QS World University Rankings 2025
2. Times Higher Education (THE) World University Rankings 2024
3. World University Rankings 2023 (WUR 2023)
4. World Bank Education Statistics / EdStats

Designed for Google Colab.
No cleaning, renaming, merging, fuzzy matching, KPI engineering, or transformation
is performed here. Raw downloaded files are preserved.

Sources selected according to the EduVision_DV project guide:
- QS 2025: melissamonfared/qs-world-university-rankings-2025
- THE 2024: ddosad/timesworlduniversityrankings2024
- WUR 2023: alitaqi000/world-university-rankings-2023
- World Bank Education: theworldbank/world-bank-intl-education
"""

from pathlib import Path
import sys
import subprocess
import shutil
import json
from datetime import datetime


# ---------------------------------------------------------------------
# 1. Install the ONLY external package required for downloading
# ---------------------------------------------------------------------
def install_dependencies():
    try:
        import kagglehub  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "kagglehub"]
        )


install_dependencies()

import kagglehub


# ---------------------------------------------------------------------
# 2. Configuration
# ---------------------------------------------------------------------
BASE_DIR = Path.cwd() / "EduVision_DV"
RAW_DIR = BASE_DIR / "01_raw_datasets"
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "qs_2025": {
        "kaggle_id": "melissamonfared/qs-world-university-rankings-2025",
        "folder": "QS_2025",
        "expected_year": 2025,
    },
    "the_2024": {
        "kaggle_id": "ddosad/timesworlduniversityrankings2024",
        "folder": "THE_2024",
        "expected_year": 2024,
    },
    "wur_2023": {
        "kaggle_id": "alitaqi000/world-university-rankings-2023",
        "folder": "WUR_2023",
        "expected_year": 2023,
    },
    "country_comparison": {
        "kaggle_id": "theworldbank/world-bank-intl-education",
        "folder": "WorldBank_Education",
        "expected_year": "country/year level",
    },
}


# ---------------------------------------------------------------------
# 3. Helper functions
# ---------------------------------------------------------------------
def copy_downloaded_dataset(dataset_key, source_dir, destination_dir):
    """Copy the complete downloaded dataset into the project's raw folder."""
    destination_dir.mkdir(parents=True, exist_ok=True)

    source_dir = Path(source_dir)

    if not source_dir.exists():
        raise FileNotFoundError(
            f"Downloaded dataset directory does not exist: {source_dir}"
        )

    copied_files = []

    # Copy every file recursively. This is intentional:
    # raw datasets must remain unchanged.
    for item in source_dir.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(source_dir)
            target = destination_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(item, target)
            copied_files.append(str(target.relative_to(BASE_DIR)))

    if not copied_files:
        raise RuntimeError(
            f"No files were found inside the downloaded dataset for {dataset_key}."
        )

    return copied_files


def write_manifest(results):
    """Write collection metadata without modifying the raw datasets."""
    manifest = {
        "project": "EduVision_DV",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Raw dataset collection only",
        "datasets": results,
    }

    manifest_path = RAW_DIR / "data_collection_manifest.json"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest_path


def download_one(dataset_key, config):
    print("\n" + "=" * 72)
    print(f"Downloading: {dataset_key}")
    print(f"Kaggle dataset: {config['kaggle_id']}")
    print("=" * 72)

    destination_dir = RAW_DIR / config["folder"]

    # Download from Kaggle using kagglehub.
    # For public datasets, this is the only dataset-download mechanism used.
    downloaded_path = kagglehub.dataset_download(config["kaggle_id"])

    copied_files = copy_downloaded_dataset(
        dataset_key=dataset_key,
        source_dir=downloaded_path,
        destination_dir=destination_dir,
    )

    print(f"Downloaded successfully: {len(copied_files)} file(s)")
    print(f"Saved to: {destination_dir}")

    return {
        "dataset_key": dataset_key,
        "kaggle_id": config["kaggle_id"],
        "expected_year": config["expected_year"],
        "destination": str(destination_dir),
        "files": copied_files,
        "status": "SUCCESS",
    }


# ---------------------------------------------------------------------
# 4. Main collection process
# ---------------------------------------------------------------------
def main():
    print("\nEduVision_DV - Raw Dataset Collection")
    print("Google Colab compatible")
    print("Collection only: NO cleaning / NO merging / NO KPI engineering")
    print(f"Output directory: {BASE_DIR}\n")

    results = []
    failures = []

    for dataset_key, config in DATASETS.items():
        try:
            result = download_one(dataset_key, config)
            results.append(result)

        except Exception as exc:
            print(f"\nFAILED: {dataset_key}")
            print(f"Reason: {exc}")
            failures.append(
                {
                    "dataset_key": dataset_key,
                    "kaggle_id": config["kaggle_id"],
                    "status": "FAILED",
                    "error": str(exc),
                }
            )

    manifest_path = write_manifest(results + failures)

    print("\n" + "=" * 72)
    print("COLLECTION SUMMARY")
    print("=" * 72)

    for result in results:
        print(f"[OK]   {result['dataset_key']}: {result['kaggle_id']}")

    for failure in failures:
        print(f"[FAIL] {failure['dataset_key']}: {failure['kaggle_id']}")

    print(f"\nManifest: {manifest_path}")

    if failures:
        print(
            "\nSome datasets failed to download. "
            "Check the error above and rerun the script."
        )
        return 1

    print("\nAll 4 approved datasets downloaded successfully.")
    print(f"Raw datasets are preserved under: {RAW_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
