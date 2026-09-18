import os
import json

nb_path = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\notebooks\04_kpi_engineering.ipynb"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# EduVision_DV – Key Performance Indicator (KPI) Engineering\n",
            "\n",
            "## Objectives\n",
            "This notebook calculates and validates the **six core project KPIs**:\n",
            "1. **Global Ranking Score**\n",
            "2. **Research Impact Score**\n",
            "3. **Faculty-to-Student Ratio** (Faculty per 100 students)\n",
            "4. **International Student Percentage** (%)\n",
            "5. **Academic Reputation Score**\n",
            "6. **Research Productivity Index** (Approved Option 1 Tri-Pillar Model)\n",
            "\n",
            "### Methodological Rules\n",
            "- Use ONLY approved source fields and formulas.\n",
            "- Preserve missing values (`NaN`); do not impute missing scores or ratios with zero.\n",
            "- Validate value ranges, detect outliers using IQR, and check for impossible values.\n",
            "- Export outputs to `../../data/final/kpi_university.csv`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "\n",
            "final_dir = r'../data/final'\n",
            "reports_dir = r'../reports'\n",
            "\n",
            "kpi_df = pd.read_csv(os.path.join(final_dir, 'kpi_university.csv'))\n",
            "kpi_val = pd.read_csv(os.path.join(reports_dir, 'kpi_validation_report.csv'))\n",
            "\n",
            "print(f'Engineered KPI University Table Shape: {kpi_df.shape}')\n",
            "display(kpi_df.head(10))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 1: Statistical Summary of Calculated KPIs"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "kpi_cols = [\n",
            "    'global_ranking_score',\n",
            "    'research_impact_score',\n",
            "    'faculty_student_ratio',\n",
            "    'international_student_percentage',\n",
            "    'academic_reputation_score',\n",
            "    'research_productivity_index'\n",
            "]\n",
            "display(kpi_df[kpi_cols].describe().T)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 2: KPI Range Validation & Outlier Audit Report"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "display(kpi_val)"
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
