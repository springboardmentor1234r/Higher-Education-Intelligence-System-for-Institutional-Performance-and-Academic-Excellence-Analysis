# EduVision_DV: Data Dictionary & Star Schema Architecture

This document provides a comprehensive technical reference for all entities, dimension tables, and fact tables within the EduVision_DV star schema.

---

## 1. Dimensional Model Overview
The analytical model implements an optimized Star Schema:
- **`dim_university`**: Conformed dimension for higher education institutions.
- **`dim_country`**: Conformed dimension for countries and macro-regions.
- **`fact_university_performance`**: Core institutional rankings and multi-dimensional scores (QS 2025).
- **`fact_research`**: Institutional research output and citation metrics (THE 2024).
- **`fact_student`**: Enrollment figures, staff ratios, and international diversity (WUR 2023).
- **`fact_country_education`**: Macroeconomic and education system indicators (World Bank).
- **`kpi_master`**: Analytical master table pre-aggregating the six core project KPIs.

---

## 2. Table Specifications

### `dim_university`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `university_id` | VARCHAR(10) | Primary Key | Unique institutional master identifier (`U0001` .. `U1503`) |
| `university_name` | VARCHAR(255) | Attribute | Standardized institutional name |
| `country_id` | VARCHAR(10) | Foreign Key | Reference to `dim_country.country_id` |
| `country_name` | VARCHAR(100) | Attribute | Standardized country of residence |
| `region` | VARCHAR(50) | Attribute | Continental region (Europe, North America, Asia, etc.) |

### `dim_country`
| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `country_id` | VARCHAR(10) | Primary Key | Standardized country code identifier (`C0001` .. `C0106`) |
| `country_name` | VARCHAR(100) | Attribute | Standardized geopolitical country name |
| `region` | VARCHAR(50) | Attribute | Geographic macro-region |

### `fact_university_performance`
| Column Name | Data Type | Description |
|---|---|---|
| `university_id` | VARCHAR(10) | Foreign Key referencing `dim_university` |
| `year` | INTEGER | Assessment year (2025) |
| `global_rank` | INTEGER | Global university rank |
| `overall_score` | FLOAT | QS overall composite institutional score (0–100) |
| `academic_reputation` | FLOAT | Academic reputation survey score (0–100) |
| `employer_reputation` | FLOAT | Employer reputation survey score (0–100) |
| `faculty_student_score`| FLOAT | Academic staffing index (0–100) |
| `citations_score` | FLOAT | Citations per faculty score (0–100) |
| `international_faculty`| FLOAT | International faculty score (0–100) |
| `international_students`|FLOAT | International student score (0–100) |
| `research_network_score`|FLOAT| International research collaboration network score (0–100) |
| `sustainability_score` | FLOAT | Social and environmental impact score (0–100) |

### `fact_research`
| Column Name | Data Type | Description |
|---|---|---|
| `university_id` | VARCHAR(10) | Foreign Key referencing `dim_university` |
| `year` | INTEGER | Assessment year (2024) |
| `research_score` | FLOAT | THE research environment score (0–100) |
| `citation_score` | FLOAT | THE research citation impact score (0–100) |
| `teaching_score` | FLOAT | THE teaching score (0–100) |
| `industry_income_score`| FLOAT | THE commercialization / grant income score (0–100) |
| `international_outlook_score`| FLOAT | THE cross-border outlook score (0–100) |

### `fact_student`
| Column Name | Data Type | Description |
|---|---|---|
| `university_id` | VARCHAR(10) | Foreign Key referencing `dim_university` |
| `year` | INTEGER | Assessment year (2023) |
| `total_students` | FLOAT | Full-time equivalent (FTE) student enrollment headcount |
| `students_per_staff` | FLOAT | Actual ratio of students per academic staff member |
| `international_student_percentage` | FLOAT | True percentage of international students (0.0% – 100.0%) |
| `female_male_ratio` | VARCHAR(20) | Demographic breakdown of female to male students |
| `international_students` | FLOAT | Estimated headcount of international students |

### `fact_country_education`
| Column Name | Data Type | Description |
|---|---|---|
| `country_id` | VARCHAR(10) | Foreign Key referencing `dim_country` |
| `country_name` | VARCHAR(100) | Country name |
| `year` | INTEGER | Observation year (2010–2023) |
| `indicator` | VARCHAR(255) | Name of educational or macroeconomic indicator |
| `value` | FLOAT | Metric value |
