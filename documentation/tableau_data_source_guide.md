# EduVision_DV – Tableau Data Source & Integration Guide

## Executive Summary

This document serves as the authoritative guide for connecting the **EduVision_DV** final analytical data package into Tableau Desktop / Tableau Cloud / Tableau Server. The data model is designed using Tableau's native **Logical Layer Relationships** (Noodles) to preserve table granularities, prevent accidental Cartesian joins, and eliminate data duplication.

--- 

## 1. Final Data Package Structure (`../../data/final/`)

The final Tableau data package consists of seven curated CSV files:


| File Name | Role in Tableau | Primary Key (PK) | Foreign Key(s) | Granularity Level |
| --- | --- | --- | --- | --- |
| `dim_university.csv` | University Dimension | `university_id` | `country_id` | 1 row per unique university entity |
| `dim_country.csv` | Country Dimension | `country_id` | N/A | 1 row per unique canonical country |
| `fact_university_performance.csv` | Institutional Rank Fact | (`university_id`, `year`, `source_ranking`) | `university_id` | 1 row per university per year per ranking source |
| `fact_research.csv` | Research Analytics Fact | (`university_id`, `year`, `source_ranking`) | `university_id` | 1 row per university per year per ranking source |
| `fact_student.csv` | Student Analytics Fact | (`university_id`, `year`, `source_ranking`) | `university_id` | 1 row per university per year per ranking source |
| `fact_country_education.csv` | Macro Country Fact | (`country_id`, `year`, `indicator_code`) | `country_id` | 1 row per country per year per indicator |
| `kpi_university.csv` | Consolidated KPI Table | `university_id` | `country_id` | 1 row per university summary KPI profile |

---

## 2. Recommended Tableau Data Model Architecture

To support the four required Tableau dashboards (**University Overview**, **Research Analytics**, **Student Analytics**, and **Country Comparison**), use Tableau's Logical Data Model with two clean star schemas.


### Schema 1: Higher Education Institutional Performance Model

Used for **University Overview**, **Research Analytics**, and **Student Analytics** dashboards.


```

                           +-----------------------+

                           |      dim_country      |

                           +-----------------------+

                           | PK: country_id        |

                           +-----------+----------+

                                       |

                                       | 1:N (Relationship on country_id)

                                       v

                           +-----------------------+

                           |    dim_university     |

                           +-----------------------+

                           | PK: university_id     |

                           | FK: country_id        |

                           +-----------+----------+

                                       |

        +------------------------------+------------------------------+

        | 1:N                          | 1:N                          | 1:N

        v                              v                              v

+-----------------------+      +-----------------------+      +-----------------------+

| fact_university_perf  |      |     fact_research     |      |     fact_student      |

+-----------------------+      +-----------------------+      +-----------------------+

| FK: university_id     |      | FK: university_id     |      | FK: university_id     |

| year, global_rank     |      | year, research_score  |      | year, total_students  |

| overall_score         |      | citation_score        |      | students_per_staff    |

+-----------------------+      +-----------------------+      +-----------------------+

```


### Schema 2: Country Macro-Level Education Model

Used for the **Country Comparison** dashboard to analyze macro-level World Bank statistics alongside national aggregate university performance.


```

                           +-----------------------+

                           |      dim_country      |

                           +-----------------------+

                           | PK: country_id        |

                           +-----------+----------+

                                       |

                                       | 1:N (Relationship on country_id)

                                       v

                           +-----------------------+

                           |fact_country_education |

                           +-----------------------+

                           | FK: country_id        |

                           | year, indicator, value|

                           +-----------------------+

```


---

## 3. Detailed Tableau Relationship Configurations


### Connection 1: `dim_university` to `dim_country`

- **Left Table**: `dim_university.csv`

- **Right Table**: `dim_country.csv`

- **Relationship Clause**: `dim_university.country_id = dim_country.country_id`

- **Cardinality**: Many-to-One (Many universities per 1 country)

- **Performance Option**: Referencing Integrity = `Some Records Match`


### Connection 2: `dim_university` to `fact_university_performance`

- **Left Table**: `dim_university.csv`

- **Right Table**: `fact_university_performance.csv`

- **Relationship Clause**: `dim_university.university_id = fact_university_performance.university_id`

- **Cardinality**: One-to-Many (1 university has multiple annual ranking records across QS/THE)

- **Performance Option**: Cardinality = `One-to-Many`


### Connection 3: `dim_university` to `fact_research`

- **Left Table**: `dim_university.csv`

- **Right Table**: `fact_research.csv`

- **Relationship Clause**: `dim_university.university_id = fact_research.university_id`

- **Cardinality**: One-to-Many


### Connection 4: `dim_university` to `fact_student`

- **Left Table**: `dim_university.csv`

- **Right Table**: `fact_student.csv`

- **Relationship Clause**: `dim_university.university_id = fact_student.university_id`

- **Cardinality**: One-to-Many


### Connection 5: `dim_country` to `fact_country_education`

- **Left Table**: `dim_country.csv`

- **Right Table**: `fact_country_education.csv`

- **Relationship Clause**: `dim_country.country_id = fact_country_education.country_id`

- **Cardinality**: One-to-Many (1 country has multiple annual indicator records)


---

## 4. Dashboard Field & Filter Mapping Guide


### Dashboard 1: University Overview Dashboard

- **Primary Data Source**: Schema 1 (`dim_university` + `fact_university_performance` + `kpi_university`)

- **Key Metrics**: `global_ranking_score`, `global_rank`, `overall_score`, `academic_reputation`

- **Recommended Tableau Filters**:

  - `source_ranking` (Single Value Dropdown e.g., *QS World University Rankings 2025*)

  - `region` (Multiple Values List)

  - `country_name` (Single Value Dropdown with Search)

  - `global_rank` (Range Slider e.g., Top 100, Top 500)


### Dashboard 2: Research Analytics Dashboard

- **Primary Data Source**: Schema 1 (`dim_university` + `fact_research` + `kpi_university`)

- **Key Metrics**: `research_impact_score`, `research_productivity_index`, `citation_score`, `citations_per_faculty_score`, `international_research_network_score`

- **Recommended Tableau Filters**:

  - `source_ranking`

  - `region`

  - `research_productivity_index` (Range Slider)


### Dashboard 3: Student Analytics Dashboard

- **Primary Data Source**: Schema 1 (`dim_university` + `fact_student` + `kpi_university`)

- **Key Metrics**: `faculty_student_ratio`, `international_student_percentage`, `total_students`, `students_per_staff`, `female_male_ratio`

- **Recommended Tableau Filters**:

  - `source_ranking`

  - `region`

  - `international_student_percentage` (Range Slider)


### Dashboard 4: Country Comparison Dashboard

- **Primary Data Source**: Schema 2 (`dim_country` + `fact_country_education` + `fact_university_performance`)

- **Key Metrics**: `ranked_university_count`, `avg_global_ranking_score`, `indicator_name` / `value` (World Bank Tertiary Enrolment %, Education Expenditure % GDP)

- **Recommended Tableau Filters**:

  - `region`

  - `year` (Multi-year timeline slider e.g., 2000–2017)

  - `indicator` (Parameter Control / Dropdown)


---

## 5. Important Tableau Best Practices & Tips

1. **Use Logical Relationships over Physical Joins**: Do not merge files physically into one flat table in Tableau Data Source tab. Use Tableau Noodles (relationships) to keep queries fast and aggregations accurate.

2. **Null Values**: Do not convert nulls to 0 in Tableau calculations. Use `IFNULL()` or `ZN()` only when creating specific display labels.

3. **Filter Context**: When calculating Top N universities, add `region` or `country_name` filters to Context in Tableau (`Add to Context`).
