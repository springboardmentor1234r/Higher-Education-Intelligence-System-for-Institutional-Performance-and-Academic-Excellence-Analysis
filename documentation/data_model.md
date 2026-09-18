# EduVision_DV – Data Model Specification

## Architecture Overview
EduVision_DV uses a Star Schema relational architecture to separate institutional dimensions from performance facts.

## Dimensions
1. dim_university: Unique primary key university_id.
2. dim_country: Unique primary key country_id.

## Fact Tables
1. act_university_performance: Composite key (university_id, year).
2. act_research: Composite key (university_id, year).
3. act_student: Composite key (university_id, year).
4. act_country_education: Composite key (country_id, year, indicator).
