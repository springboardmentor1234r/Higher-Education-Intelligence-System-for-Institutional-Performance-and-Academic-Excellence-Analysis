import os
import json

nb_path = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\notebooks\03_standardization_and_ids.ipynb"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# EduVision_DV – University & Country Standardization Pipeline\n",
            "\n",
            "## Objectives\n",
            "1. **Deterministic University Cleaning**: Apply deterministic text normalization (lowercase, trim whitespace, remove repeated spaces/punctuation, normalize formatting).\n",
            "2. **Canonical Country Mapping**: Map raw country text variants (e.g. `USA`, `US`, `United States of America`) to single canonical country names (`United States`) with stable `country_id` keys.\n",
            "3. **Stable Identifiers**: Generate surrogate keys for countries (`C001`, `C002`, ...) and universities (`U000001`, `U000002`, ...).\n",
            "4. **Dimension Tables Export**: Create `dim_country.csv` and `dim_university.csv` in `../../data/final/`.\n",
            "5. **Candidate Match Generation**: Generate cross-dataset candidate pairs in `../../reports/university_matching_candidates.csv` without auto-merging uncertain fuzzy matches."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import re\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "from difflib import SequenceMatcher\n",
            "\n",
            "cleaned_dir = r'../data/cleaned'\n",
            "final_dir = r'../data/final'\n",
            "reports_dir = r'../reports'\n",
            "\n",
            "os.makedirs(final_dir, exist_ok=True)\n",
            "os.makedirs(reports_dir, exist_ok=True)\n",
            "print('Environment initialized.')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 1: Load Cleaned Datasets & Establish Canonical Country Map"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df_qs = pd.read_csv(os.path.join(cleaned_dir, 'qs_2025_cleaned.csv'), low_memory=False)\n",
            "df_wur = pd.read_csv(os.path.join(cleaned_dir, 'wur_2023_cleaned.csv'), low_memory=False)\n",
            "\n",
            "print(f'QS 2025 Rows: {len(df_qs)}')\n",
            "print(f'WUR 2023 Rows: {len(df_wur)}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 2: Build `dim_country.csv` & Country Reports"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "dim_country = pd.read_csv(os.path.join(final_dir, 'dim_country.csv'))\n",
            "country_report = pd.read_csv(os.path.join(reports_dir, 'country_standardization_report.csv'))\n",
            "\n",
            "print('Sample Canonical Countries:')\n",
            "display(dim_country.head(10))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 3: Build `dim_university.csv` & University Standardization Reports"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "dim_univ = pd.read_csv(os.path.join(final_dir, 'dim_university.csv'))\n",
            "univ_report = pd.read_csv(os.path.join(reports_dir, 'university_standardization_report.csv'))\n",
            "\n",
            "print('Sample University Dimension Table:')\n",
            "display(dim_univ.head(10))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 4: Candidate Cross-Dataset Match Generation\n",
            "Generate candidate matches across QS and WUR within the same country for user review."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "candidates = pd.read_csv(os.path.join(reports_dir, 'university_matching_candidates.csv'))\n",
            "print(f'Total Candidate Pairs Generated: {len(candidates)}')\n",
            "display(candidates.head(15))"
        ]
    }
]

notebook_dict = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook_dict, f, indent=2)

print(f"Created notebook {nb_path}")
