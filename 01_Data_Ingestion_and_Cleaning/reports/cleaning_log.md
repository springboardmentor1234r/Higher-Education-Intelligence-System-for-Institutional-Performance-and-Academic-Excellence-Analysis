[clean_times] 2603 -> 2603 rows | 0 dupes removed | 1402 missing total_score (kept null) | numeric coercion applied to num_students, international_students, income, world_rank
[clean_cwur] 2200 -> 2200 rows | 0 dupes removed | 200 rows missing broad_impact (not reported before 2014, kept null)
[clean_shanghai] 4897 -> 4891 rows | 6 dupes removed | 3790 rows missing total_score (kept null — ARWU doesn't publish a composite score below the top tier)
[clean_qs2023] 100 -> 100 rows | 0 dupes removed | parsed '%' / 'a : b' ratio / comma-thousands text fields to numeric
[clean_school_country] 818 -> 818 rows | 0 dupes removed
[clean_expenditure] 333 wide rows -> 785 long (country, year) observations after melting 6 year columns and dropping empty cells
[clean_attainment] 79055 wide rows (425 series) -> filtered to 97 tertiary-education series -> 78430 long observations after melting