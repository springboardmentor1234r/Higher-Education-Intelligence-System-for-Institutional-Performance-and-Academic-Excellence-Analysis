# EduVision_DV - Dataset Validation & Profiling Report

## Executive Summary

A total of **14 raw dataset files** were identified, profiled, and inspected in `data/raw/`.

## Summary Table of Profiled Datasets

| File Name | File Type | Rows | Cols | Missing Cells (%) | Duplicate Rows | Dup Univ Names | Key Univ/Country Cols |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cwurData.csv` | CSV | 2,200 | 14 | 200 (0.65%) | 0 | 1,176 | `institution` / `country, national_rank` |
| `educational_attainment_supplementary_data.csv` | CSV | 79,055 | 29 | 1,816,203 (79.22%) | 2 | 0 | `N/A` / `country_name` |
| `school_and_country_table.csv` | CSV | 818 | 2 | 0 (0.0%) | 0 | 0 | `school_name` / `country` |
| `shanghaiData.csv` | CSV | 4,897 | 11 | 3,829 (7.11%) | 0 | 4,238 | `university_name` / `national_rank` |
| `timesData.csv` | CSV | 2,603 | 14 | 418 (1.15%) | 0 | 1,785 | `university_name` / `country, international, international_students` |
| `WorldUniversityRankings2023.csv` | CSV | 100 | 13 | 38 (2.92%) | 0 | 12 | `University Rank, Name of University` / `Location, International Student, International Outlook Score` |
| `EdStatsCountry-Series.csv` | CSV | 613 | 4 | 613 (25.0%) | 0 | 0 | `N/A` / `CountryCode` |
| `EdStatsCountry.csv` | CSV | 241 | 32 | 2,354 (30.52%) | 0 | 0 | `N/A` / `Country Code, Region, National accounts base year, National accounts reference year, System of National Accounts, IMF data dissemination standard` |
| `EdStatsData.csv` | CSV | 886,930 | 70 | 53,455,179 (86.1%) | 0 | 0 | `N/A` / `Country Name, Country Code` |
| `EdStatsFootNote.csv` | CSV | 643,638 | 5 | 643,638 (20.0%) | 0 | 0 | `N/A` / `CountryCode` |
| `EdStatsSeries.csv` | CSV | 3,665 | 21 | 55,203 (71.72%) | 0 | 0 | `N/A` / `N/A` |
| `EdStatsEXCEL.xlsx` | XLSX | 886,930 | 69 | 52,568,249 (85.9%) | 0 | 0 | `N/A` / `Country Name, Country Code` |
| `QS World University Rankings 2025 (Top global universities).csv` | CSV | 1,503 | 28 | 1,316 (3.13%) | 0 | 0 | `Institution_Name` / `Location, Region, International_Faculty_Score, International_Faculty_Rank, International_Students_Score, International_Students_Rank, International_Research_Network_Score, International_Research_Network_Rank` |
| `World University Rankings 2023.csv` | CSV | 2,341 | 13 | 4,264 (14.01%) | 29 | 2,179 | `University Rank, Name of University` / `Location, International Student, International Outlook Score` |

---

## Detailed File Profiles

### 1. `cwurData.csv`

- **Relative Path**: `cwurData.csv`
- **File Type**: CSV
- **Dimensions**: 2,200 rows × 14 columns
- **Missing Values**: 200 (0.65%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 1,176
- **University-Name Column**: `institution`
- **Country/Location Column**: `country, national_rank`
- **Year Information**: `year`
- **Important Ranking Fields**: `world_rank, national_rank, score`
- **Research-Related Fields**: `publications, patents`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `quality_of_education, quality_of_faculty`
- **Citation Fields**: `citations, broad_impact`

**Column Schema & Data Types:**
```
  - world_rank: int64
  - institution: str
  - country: str
  - national_rank: int64
  - quality_of_education: int64
  - alumni_employment: int64
  - quality_of_faculty: int64
  - publications: int64
  - influence: int64
  - citations: int64
  - broad_impact: float64
  - patents: int64
  - score: float64
  - year: int64
```

### 2. `educational_attainment_supplementary_data.csv`

- **Relative Path**: `educational_attainment_supplementary_data.csv`
- **File Type**: CSV
- **Dimensions**: 79,055 rows × 29 columns
- **Missing Values**: 1,816,203 (79.22%)
- **Duplicate Rows**: 2
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `country_name`
- **Year Information**: `1985, 1986, 1987, 1990, 1991, 1992, 1993, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2015`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - country_name: str
  - series_name: str
  - 1985: float64
  - 1986: float64
  - 1987: float64
  - 1990: float64
  - 1991: float64
  - 1992: float64
  - 1993: float64
  - 1995: float64
  - 1996: float64
  - 1997: float64
  - 1998: float64
  - 1999: float64
  - 2000: float64
  - 2001: float64
  - 2002: float64
  - 2003: float64
  - 2004: float64
  - 2005: float64
  - 2006: float64
  - 2007: float64
  - 2008: float64
  - 2009: float64
  - 2010: float64
  - 2011: float64
  - 2012: float64
  - 2013: float64
  - 2015: float64
```

### 3. `school_and_country_table.csv`

- **Relative Path**: `school_and_country_table.csv`
- **File Type**: CSV
- **Dimensions**: 818 rows × 2 columns
- **Missing Values**: 0 (0.0%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `school_name`
- **Country/Location Column**: `country`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - school_name: str
  - country: str
```

### 4. `shanghaiData.csv`

- **Relative Path**: `shanghaiData.csv`
- **File Type**: CSV
- **Dimensions**: 4,897 rows × 11 columns
- **Missing Values**: 3,829 (7.11%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 4,238
- **University-Name Column**: `university_name`
- **Country/Location Column**: `national_rank`
- **Year Information**: `year`
- **Important Ranking Fields**: `world_rank, national_rank, total_score`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - world_rank: str
  - university_name: str
  - national_rank: str
  - total_score: float64
  - alumni: float64
  - award: float64
  - hici: float64
  - ns: float64
  - pub: float64
  - pcp: float64
  - year: int64
```

### 5. `timesData.csv`

- **Relative Path**: `timesData.csv`
- **File Type**: CSV
- **Dimensions**: 2,603 rows × 14 columns
- **Missing Values**: 418 (1.15%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 1,785
- **University-Name Column**: `university_name`
- **Country/Location Column**: `country, international, international_students`
- **Year Information**: `year`
- **Important Ranking Fields**: `world_rank, total_score`
- **Research-Related Fields**: `research`
- **Student-Related Fields**: `num_students, student_staff_ratio, female_male_ratio`
- **International Student Fields**: `international, international_students`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `citations`

**Column Schema & Data Types:**
```
  - world_rank: str
  - university_name: str
  - country: str
  - teaching: float64
  - international: str
  - research: float64
  - citations: float64
  - income: str
  - total_score: str
  - num_students: str
  - student_staff_ratio: float64
  - international_students: str
  - female_male_ratio: str
  - year: int64
```

### 6. `WorldUniversityRankings2023.csv`

- **Relative Path**: `WorldUniversityRankings2023.csv`
- **File Type**: CSV
- **Dimensions**: 100 rows × 13 columns
- **Missing Values**: 38 (2.92%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 12
- **University-Name Column**: `University Rank, Name of University`
- **Country/Location Column**: `Location, International Student, International Outlook Score`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `University Rank, OverAll Score, Teaching Score, Research Score, Citations Score, Industry Income Score, International Outlook Score`
- **Research-Related Fields**: `Research Score`
- **Student-Related Fields**: `No of student, No of student per staff, Female:Male Ratio`
- **International Student Fields**: `International Student, International Outlook Score`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `Citations Score`

**Column Schema & Data Types:**
```
  - University Rank: int64
  - Name of University: str
  - Location: str
  - No of student: str
  - No of student per staff: float64
  - International Student: str
  - Female:Male Ratio: str
  - OverAll Score: float64
  - Teaching Score: float64
  - Research Score: float64
  - Citations Score: float64
  - Industry Income Score: float64
  - International Outlook Score: float64
```

### 7. `EdStatsCountry-Series.csv`

- **Relative Path**: `archive (8)\edstats-csv-zip-32-mb-\EdStatsCountry-Series.csv`
- **File Type**: CSV
- **Dimensions**: 613 rows × 4 columns
- **Missing Values**: 613 (25.0%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `CountryCode`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - CountryCode: str
  - SeriesCode: str
  - DESCRIPTION: str
  - Unnamed: 3: float64
```

### 8. `EdStatsCountry.csv`

- **Relative Path**: `archive (8)\edstats-csv-zip-32-mb-\EdStatsCountry.csv`
- **File Type**: CSV
- **Dimensions**: 241 rows × 32 columns
- **Missing Values**: 2,354 (30.52%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `Country Code, Region, National accounts base year, National accounts reference year, System of National Accounts, IMF data dissemination standard`
- **Year Information**: `National accounts base year, National accounts reference year, PPP survey year`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `Vital registration complete`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `PPP survey year, Latest household survey`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - Country Code: str
  - Short Name: str
  - Table Name: str
  - Long Name: str
  - 2-alpha code: str
  - Currency Unit: str
  - Special Notes: str
  - Region: str
  - Income Group: str
  - WB-2 code: str
  - National accounts base year: str
  - National accounts reference year: float64
  - SNA price valuation: str
  - Lending category: str
  - Other groups: str
  - System of National Accounts: str
  - Alternative conversion factor: str
  - PPP survey year: str
  - Balance of Payments Manual in use: str
  - External debt Reporting status: str
  - System of trade: str
  - Government Accounting concept: str
  - IMF data dissemination standard: str
  - Latest population census: str
  - Latest household survey: str
  - Source of most recent Income and expenditure data: str
  - Vital registration complete: str
  - Latest agricultural census: str
  - Latest industrial data: float64
  - Latest trade data: float64
  - Latest water withdrawal data: str
  - Unnamed: 31: float64
```

### 9. `EdStatsData.csv`

- **Relative Path**: `archive (8)\edstats-csv-zip-32-mb-\EdStatsData.csv`
- **File Type**: CSV
- **Dimensions**: 886,930 rows × 70 columns
- **Missing Values**: 53,455,179 (86.1%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `Country Name, Country Code`
- **Year Information**: `1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - Country Name: str
  - Country Code: str
  - Indicator Name: str
  - Indicator Code: str
  - 1970: float64
  - 1971: float64
  - 1972: float64
  - 1973: float64
  - 1974: float64
  - 1975: float64
  - 1976: float64
  - 1977: float64
  - 1978: float64
  - 1979: float64
  - 1980: float64
  - 1981: float64
  - 1982: float64
  - 1983: float64
  - 1984: float64
  - 1985: float64
  - 1986: float64
  - 1987: float64
  - 1988: float64
  - 1989: float64
  - 1990: float64
  - 1991: float64
  - 1992: float64
  - 1993: float64
  - 1994: float64
  - 1995: float64
  - 1996: float64
  - 1997: float64
  - 1998: float64
  - 1999: float64
  - 2000: float64
  - 2001: float64
  - 2002: float64
  - 2003: float64
  - 2004: float64
  - 2005: float64
  - 2006: float64
  - 2007: float64
  - 2008: float64
  - 2009: float64
  - 2010: float64
  - 2011: float64
  - 2012: float64
  - 2013: float64
  - 2014: float64
  - 2015: float64
  - 2016: float64
  - 2017: float64
  - 2020: float64
  - 2025: float64
  - 2030: float64
  - 2035: float64
  - 2040: float64
  - 2045: float64
  - 2050: float64
  - 2055: float64
  - 2060: float64
  - 2065: float64
  - 2070: float64
  - 2075: float64
  - 2080: float64
  - 2085: float64
  - 2090: float64
  - 2095: float64
  - 2100: float64
  - Unnamed: 69: float64
```

### 10. `EdStatsFootNote.csv`

- **Relative Path**: `archive (8)\edstats-csv-zip-32-mb-\EdStatsFootNote.csv`
- **File Type**: CSV
- **Dimensions**: 643,638 rows × 5 columns
- **Missing Values**: 643,638 (20.0%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `CountryCode`
- **Year Information**: `Year`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - CountryCode: str
  - SeriesCode: str
  - Year: str
  - DESCRIPTION: str
  - Unnamed: 4: float64
```

### 11. `EdStatsSeries.csv`

- **Relative Path**: `archive (8)\edstats-csv-zip-32-mb-\EdStatsSeries.csv`
- **File Type**: CSV
- **Dimensions**: 3,665 rows × 21 columns
- **Missing Values**: 55,203 (71.72%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `N/A`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - Series Code: str
  - Topic: str
  - Indicator Name: str
  - Short definition: str
  - Long definition: str
  - Unit of measure: float64
  - Periodicity: str
  - Base Period: str
  - Other notes: str
  - Aggregation method: str
  - Limitations and exceptions: str
  - Notes from original source: float64
  - General comments: str
  - Source: str
  - Statistical concept and methodology: str
  - Development relevance: str
  - Related source links: str
  - Other web links: float64
  - Related indicators: float64
  - License Type: float64
  - Unnamed: 20: float64
```

### 12. `EdStatsEXCEL.xlsx`

- **Relative Path**: `archive (8)\edstats-excel-zip-72-mb-\EdStatsEXCEL.xlsx`
- **File Type**: XLSX
- **Dimensions**: 886,930 rows × 69 columns
- **Missing Values**: 52,568,249 (85.9%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `N/A`
- **Country/Location Column**: `Country Name, Country Code`
- **Year Information**: `1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100`
- **Important Ranking Fields**: `N/A`
- **Research-Related Fields**: `N/A`
- **Student-Related Fields**: `N/A`
- **International Student Fields**: `N/A`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `N/A`

**Column Schema & Data Types:**
```
  - Country Name: str
  - Country Code: str
  - Indicator Name: str
  - Indicator Code: str
  - 1970: float64
  - 1971: float64
  - 1972: float64
  - 1973: float64
  - 1974: float64
  - 1975: float64
  - 1976: float64
  - 1977: float64
  - 1978: float64
  - 1979: float64
  - 1980: float64
  - 1981: float64
  - 1982: float64
  - 1983: float64
  - 1984: float64
  - 1985: float64
  - 1986: float64
  - 1987: float64
  - 1988: float64
  - 1989: float64
  - 1990: float64
  - 1991: float64
  - 1992: float64
  - 1993: float64
  - 1994: float64
  - 1995: float64
  - 1996: float64
  - 1997: float64
  - 1998: float64
  - 1999: float64
  - 2000: float64
  - 2001: float64
  - 2002: float64
  - 2003: float64
  - 2004: float64
  - 2005: float64
  - 2006: float64
  - 2007: float64
  - 2008: float64
  - 2009: float64
  - 2010: float64
  - 2011: float64
  - 2012: float64
  - 2013: float64
  - 2014: float64
  - 2015: float64
  - 2016: float64
  - 2017: float64
  - 2020: float64
  - 2025: float64
  - 2030: float64
  - 2035: float64
  - 2040: float64
  - 2045: float64
  - 2050: float64
  - 2055: float64
  - 2060: float64
  - 2065: float64
  - 2070: float64
  - 2075: float64
  - 2080: float64
  - 2085: float64
  - 2090: float64
  - 2095: float64
  - 2100: float64
```

### 13. `QS World University Rankings 2025 (Top global universities).csv`

- **Relative Path**: `QS_Ranking\QS World University Rankings 2025 (Top global universities).csv`
- **File Type**: CSV
- **Dimensions**: 1,503 rows × 28 columns
- **Missing Values**: 1,316 (3.13%)
- **Duplicate Rows**: 0
- **Duplicate University Names**: 0
- **University-Name Column**: `Institution_Name`
- **Country/Location Column**: `Location, Region, International_Faculty_Score, International_Faculty_Rank, International_Students_Score, International_Students_Rank, International_Research_Network_Score, International_Research_Network_Rank`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `RANK_2025, RANK_2024, Academic_Reputation_Score, Academic_Reputation_Rank, Employer_Reputation_Score, Employer_Reputation_Rank, Faculty_Student_Score, Faculty_Student_Rank, Citations_per_Faculty_Score, Citations_per_Faculty_Rank, International_Faculty_Score, International_Faculty_Rank, International_Students_Score, International_Students_Rank, International_Research_Network_Score, International_Research_Network_Rank, Employment_Outcomes_Score, Employment_Outcomes_Rank, Sustainability_Score, Sustainability_Rank, Overall_Score`
- **Research-Related Fields**: `International_Research_Network_Score, International_Research_Network_Rank`
- **Student-Related Fields**: `Faculty_Student_Score, Faculty_Student_Rank`
- **International Student Fields**: `International_Faculty_Score, International_Faculty_Rank, International_Students_Score, International_Students_Rank, International_Research_Network_Score, International_Research_Network_Rank`
- **Academic Reputation Fields**: `Academic_Reputation_Score, Academic_Reputation_Rank, Employer_Reputation_Score, Employer_Reputation_Rank`
- **Citation Fields**: `Citations_per_Faculty_Score, Citations_per_Faculty_Rank`

**Column Schema & Data Types:**
```
  - RANK_2025: str
  - RANK_2024: str
  - Institution_Name: str
  - Location: str
  - Region: str
  - SIZE: str
  - FOCUS: str
  - RES.: str
  - STATUS: str
  - Academic_Reputation_Score: float64
  - Academic_Reputation_Rank: str
  - Employer_Reputation_Score: float64
  - Employer_Reputation_Rank: str
  - Faculty_Student_Score: float64
  - Faculty_Student_Rank: str
  - Citations_per_Faculty_Score: float64
  - Citations_per_Faculty_Rank: str
  - International_Faculty_Score: float64
  - International_Faculty_Rank: str
  - International_Students_Score: float64
  - International_Students_Rank: str
  - International_Research_Network_Score: float64
  - International_Research_Network_Rank: str
  - Employment_Outcomes_Score: float64
  - Employment_Outcomes_Rank: str
  - Sustainability_Score: float64
  - Sustainability_Rank: str
  - Overall_Score: str
```

### 14. `World University Rankings 2023.csv`

- **Relative Path**: `World_Ranking\World University Rankings 2023.csv`
- **File Type**: CSV
- **Dimensions**: 2,341 rows × 13 columns
- **Missing Values**: 4,264 (14.01%)
- **Duplicate Rows**: 29
- **Duplicate University Names**: 2,179
- **University-Name Column**: `University Rank, Name of University`
- **Country/Location Column**: `Location, International Student, International Outlook Score`
- **Year Information**: `N/A`
- **Important Ranking Fields**: `University Rank, OverAll Score, Teaching Score, Research Score, Citations Score, Industry Income Score, International Outlook Score`
- **Research-Related Fields**: `Research Score`
- **Student-Related Fields**: `No of student, No of student per staff, Female:Male Ratio`
- **International Student Fields**: `International Student, International Outlook Score`
- **Academic Reputation Fields**: `N/A`
- **Citation Fields**: `Citations Score`

**Column Schema & Data Types:**
```
  - University Rank: str
  - Name of University: str
  - Location: str
  - No of student: str
  - No of student per staff: float64
  - International Student: str
  - Female:Male Ratio: str
  - OverAll Score: str
  - Teaching Score: float64
  - Research Score: float64
  - Citations Score: float64
  - Industry Income Score: float64
  - International Outlook Score: float64
```
