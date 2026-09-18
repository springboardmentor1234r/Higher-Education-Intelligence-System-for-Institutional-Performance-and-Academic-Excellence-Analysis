import os
import json

nb_path = r"c:\Users\mbpsi\OneDrive\Desktop\EduVision_DV\notebooks\04_kpi_engineering_and_final_data.ipynb"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# EduVision_DV – KPI Engineering & Final Data Modeling\n",
            "\n",
            "## Objectives\n",
            "1. **KPI Engineering**: Compute the 6 core project KPIs across all institutional entities:\n",
            "   - KPI 1: **Global Ranking Score**\n",
            "   - KPI 2: **Research Impact Score**\n",
            "   - KPI 3: **Faculty-to-Student Ratio** (Actual Ratio & Score)\n",
            "   - KPI 4: **International Student Percentage** (Actual % & Score)\n",
            "   - KPI 5: **Academic Reputation Score**\n",
            "   - KPI 6: **Research Productivity Index**\n",
            "2. **Fact Table Generation**: Create `fact_university_rankings.csv` and `fact_country_education.csv` in `../../data/final/`.\n",
            "3. **Tableau Integration Ready**: Ensure all output datasets are clean, structured, and ready for Tableau connection."
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
            "fact_univ = pd.read_csv(os.path.join(final_dir, 'fact_university_rankings.csv'))\n",
            "fact_country = pd.read_csv(os.path.join(final_dir, 'fact_country_education.csv'))\n",
            "\n",
            "print(f'Fact University Rankings Shape: {fact_univ.shape}')\n",
            "print(f'Fact Country Education Shape: {fact_country.shape}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 1: Inspect Engineered Institutional KPIs\n",
            "Display sample records from `fact_university_rankings.csv`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "kpi_cols = [\n",
            "    'university_id', 'university_name', 'country_name', \n",
            "    'kpi_1_global_ranking_score', 'kpi_2_research_impact_score', \n",
            "    'kpi_3_faculty_per_100_students', 'kpi_4_intl_student_pct', \n",
            "    'kpi_5_academic_reputation_score', 'kpi_6_research_productivity_index'\n",
            "]\n",
            "display(fact_univ[kpi_cols].head(10))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 2: Summary Statistics for Core KPIs"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "display(fact_univ[kpi_cols[3:]].describe())"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 3: Inspect Country-Level Education Aggregates"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "display(fact_country.head(10))"
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
