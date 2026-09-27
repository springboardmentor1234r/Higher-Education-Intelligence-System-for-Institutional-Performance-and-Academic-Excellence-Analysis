# Raw Data Validation Report

This report summarizes the schema, shape, missingness, and duplicate statistics for all four raw input datasets.

## 1. Dataset: QS 2025 (`qs_2025.csv`)
- **Shape**: 1,503 rows x 28 columns
- **Duplicate Rows**: 0
- **Columns (28)**: `RANK_2025, RANK_2024, Institution_Name, Location, Region, SIZE, FOCUS, RES., STATUS, Academic_Reputation_Score`, ... (+18 more)

### Missing Data Summary (% Null)

| Column Name | Dtype | Missing % |
|---|---|---|
| `RANK_2024` | `str` | 1.4% |
| `STATUS` | `str` | 2.46% |
| `International_Faculty_Score` | `float64` | 6.65% |
| `International_Faculty_Rank` | `str` | 6.65% |
| `International_Students_Score` | `float64` | 3.86% |
| `International_Students_Rank` | `str` | 3.86% |
| `International_Research_Network_Score` | `float64` | 0.07% |
| `International_Research_Network_Rank` | `str` | 0.07% |
| `Sustainability_Score` | `float64` | 1.26% |
| `Sustainability_Rank` | `str` | 1.26% |
| `Overall_Score` | `str` | 60.01% |

## 1. Dataset: THE 2024 (`the_2024.csv`)
- **Shape**: 2,673 rows x 29 columns
- **Duplicate Rows**: 0
- **Columns (29)**: `rank, name, scores_overall, scores_overall_rank, scores_teaching, scores_teaching_rank, scores_research, scores_research_rank, scores_citations, scores_citations_rank`, ... (+19 more)

### Missing Data Summary (% Null)

| Column Name | Dtype | Missing % |
|---|---|---|
| `scores_overall` | `str` | 28.77% |
| `scores_teaching` | `float64` | 28.77% |
| `scores_research` | `float64` | 28.77% |
| `scores_citations` | `float64` | 28.77% |
| `scores_industry_income` | `float64` | 28.77% |
| `scores_international_outlook` | `float64` | 28.77% |
| `stats_female_male_ratio` | `str` | 3.48% |
| `subjects_offered` | `str` | 0.15% |
| `website_url` | `str` | 87.13% |

## 1. Dataset: WUR 2023 (`wur_2023.csv`)
- **Shape**: 2,341 rows x 13 columns
- **Duplicate Rows**: 29
- **Columns (13)**: `University Rank, Name of University, Location, No of student, No of student per staff, International Student, Female:Male Ratio, OverAll Score, Teaching Score, Research Score`, ... (+3 more)

### Missing Data Summary (% Null)

| Column Name | Dtype | Missing % |
|---|---|---|
| `Name of University` | `str` | 4.61% |
| `Location` | `str` | 12.56% |
| `No of student` | `str` | 5.64% |
| `No of student per staff` | `float64` | 5.68% |
| `International Student` | `str` | 5.64% |
| `Female:Male Ratio` | `str` | 9.1% |
| `OverAll Score` | `str` | 23.15% |
| `Teaching Score` | `float64` | 23.15% |
| `Research Score` | `float64` | 23.15% |
| `Citations Score` | `float64` | 23.15% |
| `Industry Income Score` | `float64` | 23.15% |
| `International Outlook Score` | `float64` | 23.15% |

## 1. Dataset: World Bank EdStats (EdStatsData.csv) (`world_bank_edstats/EdStatsData.csv`)
- **Shape**: 886,930 rows x 70 columns
- **Duplicate Rows**: 0
- **Columns (70)**: `Country Name, Country Code, Indicator Name, Indicator Code, 1970, 1971, 1972, 1973, 1974, 1975`, ... (+60 more)

### Missing Data Summary (% Null)

| Column Name | Dtype | Missing % |
|---|---|---|
| (EdStats composite inspection) | - | - |

