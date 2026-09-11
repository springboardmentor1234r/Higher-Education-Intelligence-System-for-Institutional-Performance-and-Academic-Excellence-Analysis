# Matching Methodology

## Rule
Fuzzy matching identifies *candidates* only. A match is only written into
`dim_university` if:
1. Exact match on (standardized name, standardized country), OR
2. Fuzzy similarity >= 95 (rapidfuzz token_sort_ratio) AND same country,
   AND not in the manually-reviewed false-positive list.

Matches scoring 90-94.9 similarity are written to
`matches_for_manual_review.csv` and are **not** merged automatically - a
false match is worse than a missing match (per project reference guide,
Section 7).

## Known false positives (excluded even at >=95% similarity)
- national university
- national university of ireland
- northeastern university
- southwest university
- university of southern queensland

## Results
- dim_university rows: 4708
- QS universities: 1503
- THE universities: 2673
- WUR 2023 universities: 2233
- Present in all three sources: 742
