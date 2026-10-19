# EduVision Dimensional Data Model

The EduVision analytics pipeline implements a relational dimensional model (Star Schema) to unify university performance metrics across QS 2025, THE 2024, WUR 2023, and World Bank EdStats.

---

## Star Schema Overview

```
                   +-------------------+
                   |    dim_country    |
                   +-------------------+
                   | PK: country_id    |
                   | country_name      |
                   | country_code      |
                   | region            |
                   | income_group      |
                   +---------+---------+
                             | 1:N
                             |
                   +---------v---------+
                   |  dim_university   |
                   +-------------------+
                   | PK: university_id |
                   | university_name   |
                   | FK: country_id    |
                   | country_name      |
                   | region            |
                   +----+----+----+----+
                        |    |    |
        +---------------+    |    +---------------+
        | 1:N                | 1:N                | 1:N
+-------v---------+  +-------v---------+  +-------v---------+
| fact_university_|  |  fact_research  |  |  fact_student   |
|   performance   |  +-----------------+  +-----------------+
+-----------------+  | FK:uni_id       |  | FK:uni_id       |
| FK:uni_id       |  | year            |  | year            |
| year            |  | research_score  |  | total_students  |
| global_rank     |  | citation_score  |  | students_per_   |
| overall_score   |  | research_impact |  |   staff         |
| academic_rep    |  | research_prod   |  | intl_students   |
| employer_rep    |  +-----------------+  | intl_student_%  |
+-----------------+                       +-----------------+

               +------------------------+
               | fact_country_education |
               +------------------------+
               | FK: country_id         |
               | year                   |
               | indicator_code         |
               | indicator_name         |
               | value                  |
               +------------------------+
```

---

## Table Schemas

### 1. `dim_country`
- `country_id` (VARCHAR, PK): Unique surrogate key (`CTY_001` ... `CTY_258`).
- `country_name` (VARCHAR): Standardized canonical country name.
- `country_code` (VARCHAR): ISO 3-letter country code.
- `region` (VARCHAR): Geographic macro-region (e.g., Europe & Central Asia, North America).
- `income_group` (VARCHAR): World Bank income classification (e.g., High income: OECD).

### 2. `dim_university`
- `university_id` (VARCHAR, PK): Unique surrogate key (`UNI_0001` ... `UNI_3402`).
- `university_name` (VARCHAR): Canonical university title.
- `country_id` (VARCHAR, FK): Foreign key to `dim_country.country_id`.
- `country_name` (VARCHAR): Associated country name.
- `region` (VARCHAR): Macro-region location.

### 3. `fact_university_performance`
- `university_id` (VARCHAR, FK): Foreign key to `dim_university`.
- `year` (INT): Ranking year (2023, 2024, 2025).
- `global_rank` (FLOAT): Institutional global rank.
- `overall_score` (FLOAT): Score on 0-100 scale.
- `academic_reputation` (FLOAT): Academic reputation / teaching score.
- `employer_reputation` (FLOAT): Employer reputation / industry income score.

### 4. `fact_research`
- `university_id` (VARCHAR, FK): Foreign key to `dim_university`.
- `year` (INT): Ranking year.
- `research_score` (FLOAT): Research score (0-100).
- `citation_score` (FLOAT): Citations per faculty / citations score.
- `research_impact` (FLOAT): Research impact metric.
- `research_productivity` (FLOAT): Derived research productivity index.

### 5. `fact_student`
- `university_id` (VARCHAR, FK): Foreign key to `dim_university`.
- `year` (INT): Ranking year.
- `total_students` (FLOAT): Total enrolled headcount.
- `students_per_staff` (FLOAT): Student-to-faculty headcount ratio.
- `international_students` (FLOAT): Total international enrolled headcount.
- `international_student_percentage` (FLOAT): Percentage of international students.

### 6. `fact_country_education`
- `country_id` (VARCHAR, FK): Foreign key to `dim_country`.
- `year` (INT): Observation year.
- `indicator_code` (VARCHAR): World Bank EdStats series code.
- `indicator_name` (VARCHAR): Full indicator description.
- `value` (FLOAT): Observed metric value.
