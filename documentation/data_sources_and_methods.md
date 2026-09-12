# Data Sources and Methods

The project uses the four datasets supplied for this submission:
1. QS World University Rankings 2025
2. Times Higher Education World University Rankings 2024
3. World University Rankings 2023
4. `world-education-data.csv` for country-level education indicators

The supplied milestone material emphasizes that university-level and country-level data have different grains and should not be blindly merged. The final model therefore uses university_id and country_id relationships.

University matching uses conservative normalized-name matching. Aggressive fuzzy matching was not automatically approved because campus-level false matches can corrupt the analysis.

Missing scores are retained as missing; they are not replaced with zero.
