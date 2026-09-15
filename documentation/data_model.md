# Tableau Data Model

Use relationships, not one giant many-to-many physical join.

`dim_university.university_id` → university performance/research/student facts.

`dim_country.country_id` → `dim_university.country_id` and `fact_country_education.country_id`.

Keep `year` and `source` in fact tables.
