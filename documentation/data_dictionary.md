# EduVision_DV – Master Data Dictionary

## Overview

This document provides a comprehensive data dictionary for all four core datasets analyzed in the **EduVision_DV** project. It documents variable definitions, standardized naming conventions, data types, units of measure, missing value statistics, and mapping towards the project's four Tableau dashboards and six required KPIs.

### KPI Categorization Rule

Per analytical rigor guidelines, metric fields are distinguished carefully into:

- **Actual Percentage**: Exact percentage value (e.g., `International Student` in THE 2023: `24%`).

- **Actual Ratio**: Exact mathematical ratio (e.g., `No of student per staff` in THE 2023: `9.6`).

- **Score**: Standardized index score scaled from 0–100 (e.g., `Citations_per_Faculty_Score` in QS 2025).

- **Rank**: Ordinal global position integer/range (e.g., `RANK_2025` in QS 2025).

- **Derived Metric**: Engineered metric combining multi-dataset fields during ETL.


## Dataset: QS World University Rankings 2025

| Original Column Name | Standardized Name | Data Type | Meaning | Unit | Example | Missing % | Identifier | Dashboard Relevance | KPI Support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RANK_2025` | `rank_2025` | `str` | Global rank position assigned by QS for year 2025 | Rank Position | `1` | 0.0% | No | Univ Overview, Country Comp | KPI 1: Global Ranking Score (Rank component) |
| `RANK_2024` | `rank_2024` | `str` | Global rank position assigned by QS for year 2024 | Rank Position | `1` | 1.4% | No | Univ Overview, Country Comp | KPI 1: Global Ranking Score (Rank component) |
| `Institution_Name` | `university_name` | `str` | Official name of the higher education institution | N/A | `Massachusetts Institute of Technology (MIT) ` | 0.0% | Yes (Primary) | Univ Overview, Research, Student | None |
| `Location` | `country` | `str` | Country location of the university | N/A | `United States` | 0.0% | No | Univ Overview, Country Comp | None |
| `Region` | `region` | `str` | Geographic world region | N/A | `Americas` | 0.0% | No | Univ Overview, Country Comp | None |
| `SIZE` | `size` | `str` | QS Institutional classification category for size | N/A | `M` | 0.0% | No | Univ Overview | None |
| `FOCUS` | `focus` | `str` | QS Institutional classification category for focus | N/A | `CO` | 0.0% | No | Univ Overview | None |
| `RES.` | `res` | `str` | QS Institutional classification category for res. | N/A | `VH` | 0.0% | No | Univ Overview | None |
| `STATUS` | `status` | `str` | QS Institutional classification category for status | N/A | `B` | 2.46% | No | Univ Overview | None |
| `Academic_Reputation_Score` | `academic_reputation_score` | `float64` | Academic reputation survey score or rank | Score (0-100) | `100.0` | 0.0% | No | Univ Overview, Research | KPI 5: Academic Reputation Score (Actual Score) |
| `Academic_Reputation_Rank` | `academic_reputation_rank` | `str` | Academic reputation survey score or rank | Rank Position | `4` | 0.0% | No | Univ Overview, Research | None |
| `Employer_Reputation_Score` | `employer_reputation_score` | `float64` | Employer reputation survey score or rank | Score (0-100) | `100.0` | 0.0% | No | Univ Overview | None |
| `Employer_Reputation_Rank` | `employer_reputation_rank` | `str` | Employer reputation survey score or rank | Rank Position | `2` | 0.0% | No | Univ Overview | None |
| `Faculty_Student_Score` | `faculty_student_score` | `float64` | Faculty-to-student score or rank (Note: Benchmark Score 0-100, not actual ratio) | Score (0-100) | `100.0` | 0.0% | No | Student | KPI 3: Faculty-to-Student Ratio (Proxy Score; Actual Ratio requires derived calculation) |
| `Faculty_Student_Rank` | `faculty_student_rank` | `str` | Faculty-to-student score or rank (Note: Benchmark Score 0-100, not actual ratio) | Rank Position | `11` | 0.0% | No | Student | None |
| `Citations_per_Faculty_Score` | `citations_per_faculty_score` | `float64` | Citations per faculty score or rank (Note: Benchmark Score 0-100, not raw citation count) | Score (0-100) | `100.0` | 0.0% | No | Research | KPI 2: Research Impact Score (Actual Score) |
| `Citations_per_Faculty_Rank` | `citations_per_faculty_rank` | `str` | Citations per faculty score or rank (Note: Benchmark Score 0-100, not raw citation count) | Rank Position | `9` | 0.0% | No | Research | None |
| `International_Faculty_Score` | `international_faculty_score` | `float64` | Proportion of international faculty score or rank | Score (0-100) | `99.3` | 6.65% | No | Student | None |
| `International_Faculty_Rank` | `international_faculty_rank` | `str` | Proportion of international faculty score or rank | Rank Position | `100` | 6.65% | No | Student | None |
| `International_Students_Score` | `international_students_score` | `float64` | Proportion of international students score or rank (Note: Benchmark Score 0-100, not actual percentage) | Score (0-100) | `86.8` | 3.86% | No | Student | KPI 4: International Student Percentage (Proxy Score; Actual % requires derived calculation) |
| `International_Students_Rank` | `international_students_rank` | `str` | Proportion of international students score or rank (Note: Benchmark Score 0-100, not actual percentage) | Rank Position | `143` | 3.86% | No | Student | None |
| `International_Research_Network_Score` | `international_research_network_score` | `float64` | Diversity of international research collaboration score or rank | Score (0-100) | `96.0` | 0.07% | No | Research | KPI 6: Research Productivity Index (Proxy Score; Raw productivity requires derived calculation) |
| `International_Research_Network_Rank` | `international_research_network_rank` | `str` | Diversity of international research collaboration score or rank | Rank Position | `58` | 0.07% | No | Research | None |
| `Employment_Outcomes_Score` | `employment_outcomes_score` | `float64` | Employment outcomes score metric score or rank | Score (0-100) | `100.0` | 0.0% | No | Univ Overview | None |
| `Employment_Outcomes_Rank` | `employment_outcomes_rank` | `str` | Employment outcomes rank metric score or rank | Rank Position | `8` | 0.0% | No | Univ Overview | None |
| `Sustainability_Score` | `sustainability_score` | `float64` | Sustainability score metric score or rank | Score (0-100) | `99.0` | 1.26% | No | Univ Overview | None |
| `Sustainability_Rank` | `sustainability_rank` | `str` | Sustainability rank metric score or rank | Rank Position | `15=` | 1.26% | No | Univ Overview | None |
| `Overall_Score` | `overall_score` | `str` | Consolidated overall QS global benchmark score | Score (0-100) | `100` | 60.01% | No | Univ Overview, Country Comp | KPI 1: Global Ranking Score (Actual Score) |

---

## Dataset: THE World University Rankings 2023

| Original Column Name | Standardized Name | Data Type | Meaning | Unit | Example | Missing % | Identifier | Dashboard Relevance | KPI Support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `University Rank` | `world_rank` | `str` | Global rank position assigned by Times Higher Education 2023 | Rank Position | `1` | 0.0% | No | Univ Overview, Country Comp | KPI 1: Global Ranking Score (Rank component) |
| `Name of University` | `university_name` | `str` | Official institution name | N/A | `University of Oxford` | 4.61% | Yes (Primary) | Univ Overview, Research, Student | None |
| `Location` | `country` | `str` | Country or territory where institution is located | N/A | `United Kingdom` | 12.56% | No | Univ Overview, Country Comp | None |
| `No of student` | `num_students` | `str` | Total full-time equivalent (FTE) student enrollment | Count (Headcount) | `20,965` | 5.64% | No | Univ Overview, Student | KPI 3 & 4: Supporting metric for actual student counts |
| `No of student per staff` | `student_staff_ratio` | `float64` | Actual number of FTE students per staff member | Ratio (Students : 1 Staff) | `10.6` | 5.68% | No | Student | KPI 3: Faculty-to-Student Ratio (Actual Ratio) |
| `International Student` | `pct_international_students` | `str` | Actual percentage of international students enrolled | Percentage (%) | `42%` | 5.64% | No | Student, Country Comp | KPI 4: International Student Percentage (Actual Percentage) |
| `Female:Male Ratio` | `female_male_ratio` | `str` | Proportion of female to male students | Ratio (Female : Male) | `48 : 52` | 9.1% | No | Student | None |
| `OverAll Score` | `overall_score` | `str` | Consolidated overall THE benchmark score | Score (0-100) | `96.4` | 23.15% | No | Univ Overview, Country Comp | KPI 1: Global Ranking Score (Actual Score) |
| `Teaching Score` | `teaching_score` | `float64` | Teaching environment score (includes academic reputation & staff ratios) | Score (0-100) | `92.3` | 23.15% | No | Univ Overview, Student | KPI 5: Academic Reputation Score (Partial teaching/reputation proxy) |
| `Research Score` | `research_score` | `float64` | Research reputation, income, and volume score | Score (0-100) | `99.7` | 23.15% | No | Research | KPI 6: Research Productivity Index (Score component) |
| `Citations Score` | `citations_score` | `float64` | Research citation impact score | Score (0-100) | `99.0` | 23.15% | No | Research | KPI 2: Research Impact Score (Actual Score) |
| `Industry Income Score` | `industry_income_score` | `float64` | Knowledge transfer and industry research funding score | Score (0-100) | `74.9` | 23.15% | No | Research | None |
| `International Outlook Score` | `international_outlook_score` | `float64` | Combined international staff, student, and research collaboration score | Score (0-100) | `96.2` | 23.15% | No | Student, Country Comp | None |

---

## Dataset: World Bank Education Statistics (Data)

| Original Column Name | Standardized Name | Data Type | Meaning | Unit | Example | Missing % | Identifier | Dashboard Relevance | KPI Support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Country Name` | `country_name` | `str` | Standardized country or region name | N/A | `Arab World` | 0.0% | Yes | Country Comp | None |
| `Country Code` | `country_code` | `str` | ISO 3-letter country/region code | N/A | `ARB` | 0.0% | Yes (ISO Alpha-3) | Country Comp | None |
| `Indicator Name` | `indicator_name` | `str` | Description of global education / economic indicator | N/A | `Adjusted net enrolment rate, lower secondary, b...` | 0.0% | No | Country Comp | Country Comparison macro metrics (e.g. Tertiary Enrollment %) |
| `Indicator Code` | `indicator_code` | `str` | Unique World Bank series code | N/A | `UIS.NERA.2` | 0.0% | Yes (Series ID) | Country Comp | None |
| `1970` | `year_1970` | `float64` | Annual indicator value recorded or projected for year 1970 | Varies by Indicator Code | `54.8221206665039` | 91.85% | No | Country Comp | None |
| `1971` | `year_1971` | `float64` | Annual indicator value recorded or projected for year 1971 | Varies by Indicator Code | `54.8941383361816` | 95.99% | No | Country Comp | None |
| `1972` | `year_1972` | `float64` | Annual indicator value recorded or projected for year 1972 | Varies by Indicator Code | `56.2094383239746` | 95.98% | No | Country Comp | None |
| `1973` | `year_1973` | `float64` | Annual indicator value recorded or projected for year 1973 | Varies by Indicator Code | `57.2671089172363` | 95.99% | No | Country Comp | None |
| `1974` | `year_1974` | `float64` | Annual indicator value recorded or projected for year 1974 | Varies by Indicator Code | `57.991138458252` | 95.97% | No | Country Comp | None |
| `1975` | `year_1975` | `float64` | Annual indicator value recorded or projected for year 1975 | Varies by Indicator Code | `59.3655395507813` | 90.16% | No | Country Comp | None |
| `1976` | `year_1976` | `float64` | Annual indicator value recorded or projected for year 1976 | Varies by Indicator Code | `60.9999618530273` | 95.77% | No | Country Comp | None |
| `1977` | `year_1977` | `float64` | Annual indicator value recorded or projected for year 1977 | Varies by Indicator Code | `61.922679901123` | 95.76% | No | Country Comp | None |
| `1978` | `year_1978` | `float64` | Annual indicator value recorded or projected for year 1978 | Varies by Indicator Code | `62.6934204101563` | 95.76% | No | Country Comp | None |
| `1979` | `year_1979` | `float64` | Annual indicator value recorded or projected for year 1979 | Varies by Indicator Code | `64.383186340332` | 95.85% | No | Country Comp | None |
| `1980` | `year_1980` | `float64` | Annual indicator value recorded or projected for year 1980 | Varies by Indicator Code | `65.6177673339844` | 89.95% | No | Country Comp | None |
| `1981` | `year_1981` | `float64` | Annual indicator value recorded or projected for year 1981 | Varies by Indicator Code | `66.0851516723633` | 95.63% | No | Country Comp | None |
| `1982` | `year_1982` | `float64` | Annual indicator value recorded or projected for year 1982 | Varies by Indicator Code | `66.6081390380859` | 95.77% | No | Country Comp | None |
| `1983` | `year_1983` | `float64` | Annual indicator value recorded or projected for year 1983 | Varies by Indicator Code | `67.2904510498047` | 95.66% | No | Country Comp | None |
| `1984` | `year_1984` | `float64` | Annual indicator value recorded or projected for year 1984 | Varies by Indicator Code | `68.5100936889648` | 95.65% | No | Country Comp | None |
| `1985` | `year_1985` | `float64` | Annual indicator value recorded or projected for year 1985 | Varies by Indicator Code | `69.0332107543945` | 89.82% | No | Country Comp | None |
| `1986` | `year_1986` | `float64` | Annual indicator value recorded or projected for year 1986 | Varies by Indicator Code | `69.9449081420898` | 95.56% | No | Country Comp | None |
| `1987` | `year_1987` | `float64` | Annual indicator value recorded or projected for year 1987 | Varies by Indicator Code | `71.0418701171875` | 95.64% | No | Country Comp | None |
| `1988` | `year_1988` | `float64` | Annual indicator value recorded or projected for year 1988 | Varies by Indicator Code | `71.6937789916992` | 95.65% | No | Country Comp | None |
| `1989` | `year_1989` | `float64` | Annual indicator value recorded or projected for year 1989 | Varies by Indicator Code | `71.6990966796875` | 95.77% | No | Country Comp | None |
| `1990` | `year_1990` | `float64` | Annual indicator value recorded or projected for year 1990 | Varies by Indicator Code | `71.9958190917969` | 85.97% | No | Country Comp | None |
| `1991` | `year_1991` | `float64` | Annual indicator value recorded or projected for year 1991 | Varies by Indicator Code | `72.6028366088867` | 91.61% | No | Country Comp | None |
| `1992` | `year_1992` | `float64` | Annual indicator value recorded or projected for year 1992 | Varies by Indicator Code | `70.0327224731445` | 91.48% | No | Country Comp | None |
| `1993` | `year_1993` | `float64` | Annual indicator value recorded or projected for year 1993 | Varies by Indicator Code | `70.4648208618164` | 91.45% | No | Country Comp | None |
| `1994` | `year_1994` | `float64` | Annual indicator value recorded or projected for year 1994 | Varies by Indicator Code | `72.6456832885742` | 91.27% | No | Country Comp | None |
| `1995` | `year_1995` | `float64` | Annual indicator value recorded or projected for year 1995 | Varies by Indicator Code | `71.8117599487305` | 85.19% | No | Country Comp | None |
| `1996` | `year_1996` | `float64` | Annual indicator value recorded or projected for year 1996 | Varies by Indicator Code | `73.9035110473633` | 91.34% | No | Country Comp | None |
| `1997` | `year_1997` | `float64` | Annual indicator value recorded or projected for year 1997 | Varies by Indicator Code | `74.4252014160156` | 91.72% | No | Country Comp | None |
| `1998` | `year_1998` | `float64` | Annual indicator value recorded or projected for year 1998 | Varies by Indicator Code | `75.1108169555664` | 90.43% | No | Country Comp | None |
| `1999` | `year_1999` | `float64` | Annual indicator value recorded or projected for year 1999 | Varies by Indicator Code | `76.2543182373047` | 86.6% | No | Country Comp | None |
| `2000` | `year_2000` | `float64` | Annual indicator value recorded or projected for year 2000 | Varies by Indicator Code | `77.2456817626953` | 80.08% | No | Country Comp | None |
| `2001` | `year_2001` | `float64` | Annual indicator value recorded or projected for year 2001 | Varies by Indicator Code | `78.8005218505859` | 86.07% | No | Country Comp | None |
| `2002` | `year_2002` | `float64` | Annual indicator value recorded or projected for year 2002 | Varies by Indicator Code | `80.051399230957` | 86.0% | No | Country Comp | None |
| `2003` | `year_2003` | `float64` | Annual indicator value recorded or projected for year 2003 | Varies by Indicator Code | `80.8053894042969` | 85.3% | No | Country Comp | None |
| `2004` | `year_2004` | `float64` | Annual indicator value recorded or projected for year 2004 | Varies by Indicator Code | `81.607063293457` | 85.48% | No | Country Comp | None |
| `2005` | `year_2005` | `float64` | Annual indicator value recorded or projected for year 2005 | Varies by Indicator Code | `82.4894866943359` | 79.24% | No | Country Comp | None |
| `2006` | `year_2006` | `float64` | Annual indicator value recorded or projected for year 2006 | Varies by Indicator Code | `82.6855087280273` | 84.18% | No | Country Comp | None |
| `2007` | `year_2007` | `float64` | Annual indicator value recorded or projected for year 2007 | Varies by Indicator Code | `83.2803421020508` | 84.52% | No | Country Comp | None |
| `2008` | `year_2008` | `float64` | Annual indicator value recorded or projected for year 2008 | Varies by Indicator Code | `84.0118713378906` | 84.85% | No | Country Comp | None |
| `2009` | `year_2009` | `float64` | Annual indicator value recorded or projected for year 2009 | Varies by Indicator Code | `84.1959609985352` | 83.98% | No | Country Comp | None |
| `2010` | `year_2010` | `float64` | Annual indicator value recorded or projected for year 2010 | Varies by Indicator Code | `85.2119979858398` | 72.67% | No | Country Comp | None |
| `2011` | `year_2011` | `float64` | Annual indicator value recorded or projected for year 2011 | Varies by Indicator Code | `85.2451400756836` | 83.54% | No | Country Comp | None |
| `2012` | `year_2012` | `float64` | Annual indicator value recorded or projected for year 2012 | Varies by Indicator Code | `86.1016693115234` | 83.4% | No | Country Comp | None |
| `2013` | `year_2013` | `float64` | Annual indicator value recorded or projected for year 2013 | Varies by Indicator Code | `85.5119400024414` | 84.5% | No | Country Comp | None |
| `2014` | `year_2014` | `float64` | Annual indicator value recorded or projected for year 2014 | Varies by Indicator Code | `85.3201522827148` | 87.17% | No | Country Comp | None |
| `2015` | `year_2015` | `float64` | Annual indicator value recorded or projected for year 2015 | Varies by Indicator Code | `62.4392794473723` | 85.22% | No | Country Comp | None |
| `2016` | `year_2016` | `float64` | Annual indicator value recorded or projected for year 2016 | Varies by Indicator Code | `21923168354725.3` | 98.14% | No | Country Comp | None |
| `2017` | `year_2017` | `float64` | Annual indicator value recorded or projected for year 2017 | Varies by Indicator Code | `2.0` | 99.98% | No | Country Comp | None |
| `2020` | `year_2020` | `float64` | Annual indicator value recorded or projected for year 2020 | Varies by Indicator Code | `2.0` | 94.2% | No | Country Comp | None |
| `2025` | `year_2025` | `float64` | Annual indicator value recorded or projected for year 2025 | Varies by Indicator Code | `2.1` | 94.2% | No | Country Comp | None |
| `2030` | `year_2030` | `float64` | Annual indicator value recorded or projected for year 2030 | Varies by Indicator Code | `2.2` | 94.2% | No | Country Comp | None |
| `2035` | `year_2035` | `float64` | Annual indicator value recorded or projected for year 2035 | Varies by Indicator Code | `2.3` | 94.2% | No | Country Comp | None |
| `2040` | `year_2040` | `float64` | Annual indicator value recorded or projected for year 2040 | Varies by Indicator Code | `2.3` | 94.2% | No | Country Comp | None |
| `2045` | `year_2045` | `float64` | Annual indicator value recorded or projected for year 2045 | Varies by Indicator Code | `2.3` | 94.2% | No | Country Comp | None |
| `2050` | `year_2050` | `float64` | Annual indicator value recorded or projected for year 2050 | Varies by Indicator Code | `2.4` | 94.2% | No | Country Comp | None |
| `2055` | `year_2055` | `float64` | Annual indicator value recorded or projected for year 2055 | Varies by Indicator Code | `2.5` | 94.2% | No | Country Comp | None |
| `2060` | `year_2060` | `float64` | Annual indicator value recorded or projected for year 2060 | Varies by Indicator Code | `2.5` | 94.2% | No | Country Comp | None |
| `2065` | `year_2065` | `float64` | Annual indicator value recorded or projected for year 2065 | Varies by Indicator Code | `2.5` | 94.2% | No | Country Comp | None |
| `2070` | `year_2070` | `float64` | Annual indicator value recorded or projected for year 2070 | Varies by Indicator Code | `2.6` | 94.2% | No | Country Comp | None |
| `2075` | `year_2075` | `float64` | Annual indicator value recorded or projected for year 2075 | Varies by Indicator Code | `2.6` | 94.2% | No | Country Comp | None |
| `2080` | `year_2080` | `float64` | Annual indicator value recorded or projected for year 2080 | Varies by Indicator Code | `2.6` | 94.2% | No | Country Comp | None |
| `2085` | `year_2085` | `float64` | Annual indicator value recorded or projected for year 2085 | Varies by Indicator Code | `2.7` | 94.2% | No | Country Comp | None |
| `2090` | `year_2090` | `float64` | Annual indicator value recorded or projected for year 2090 | Varies by Indicator Code | `2.7` | 94.2% | No | Country Comp | None |
| `2095` | `year_2095` | `float64` | Annual indicator value recorded or projected for year 2095 | Varies by Indicator Code | `2.7` | 94.2% | No | Country Comp | None |
| `2100` | `year_2100` | `float64` | Annual indicator value recorded or projected for year 2100 | Varies by Indicator Code | `2.7` | 94.2% | No | Country Comp | None |
| `Unnamed: 69` | `unnamed:_69` | `float64` | Auxiliary metadata column | N/A | `N/A (All Null)` | 100.0% | No | General Meta | None |

---

## Dataset: World Bank Country Metadata

| Original Column Name | Standardized Name | Data Type | Meaning | Unit | Example | Missing % | Identifier | Dashboard Relevance | KPI Support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Country Code` | `country_code` | `str` | ISO 3-letter country code | N/A | `ABW` | 0.0% | Yes (ISO Alpha-3) | Country Comp | None |
| `Short Name` | `short_name` | `str` | Country demographic/economic metadata: Short Name | N/A | `Aruba` | 0.0% | No | Country Comp | None |
| `Table Name` | `table_name` | `str` | Country demographic/economic metadata: Table Name | N/A | `Aruba` | 0.0% | No | Country Comp | None |
| `Long Name` | `long_name` | `str` | Country demographic/economic metadata: Long Name | N/A | `Aruba` | 0.0% | No | Country Comp | None |
| `2-alpha code` | `2-alpha_code` | `str` | Country demographic/economic metadata: 2-alpha code | N/A | `AW` | 1.24% | No | Country Comp | None |
| `Currency Unit` | `currency_unit` | `str` | Country demographic/economic metadata: Currency Unit | N/A | `Aruban florin` | 10.79% | No | Country Comp | None |
| `Special Notes` | `special_notes` | `str` | Country demographic/economic metadata: Special Notes | N/A | `SNA data for 2000-2011 are updated from officia...` | 39.83% | No | Country Comp | None |
| `Region` | `region` | `str` | Geographic region classification (e.g., East Asia & Pacific) | N/A | `Latin America & Caribbean` | 11.2% | No | Univ Overview, Country Comp | None |
| `Income Group` | `income_group` | `str` | World Bank income level tier (e.g., High income, Upper middle income) | N/A | `High income: nonOECD` | 11.2% | No | Univ Overview, Country Comp | None |
| `WB-2 code` | `wb-2_code` | `str` | Country demographic/economic metadata: WB-2 code | N/A | `AW` | 0.41% | No | Country Comp | None |
| `National accounts base year` | `national_accounts_base_year` | `str` | Country demographic/economic metadata: National accounts base year | N/A | `2000` | 14.94% | No | Country Comp | None |
| `National accounts reference year` | `national_accounts_reference_year` | `float64` | Country demographic/economic metadata: National accounts reference year | N/A | `1996.0` | 86.72% | No | Country Comp | None |
| `SNA price valuation` | `sna_price_valuation` | `str` | Country demographic/economic metadata: SNA price valuation | N/A | `Value added at basic prices (VAB)` | 18.26% | No | Country Comp | None |
| `Lending category` | `lending_category` | `str` | Country demographic/economic metadata: Lending category | N/A | `IDA` | 40.25% | No | Country Comp | None |
| `Other groups` | `other_groups` | `str` | Country demographic/economic metadata: Other groups | N/A | `HIPC` | 75.93% | No | Country Comp | None |
| `System of National Accounts` | `system_of_national_accounts` | `str` | Country demographic/economic metadata: System of National Accounts | N/A | `Country uses the 1993 System of National Accoun...` | 10.79% | No | Country Comp | None |
| `Alternative conversion factor` | `alternative_conversion_factor` | `str` | Country demographic/economic metadata: Alternative conversion factor | N/A | `1991–96` | 80.5% | No | Country Comp | None |
| `PPP survey year` | `ppp_survey_year` | `str` | Country demographic/economic metadata: PPP survey year | N/A | `2005` | 39.83% | No | Country Comp | None |
| `Balance of Payments Manual in use` | `balance_of_payments_manual_in_use` | `str` | Country demographic/economic metadata: Balance of Payments Manual in use | N/A | `IMF Balance of Payments Manual, 6th edition.` | 24.9% | No | Country Comp | None |
| `External debt Reporting status` | `external_debt_reporting_status` | `str` | Country demographic/economic metadata: External debt Reporting status | N/A | `Actual` | 48.55% | No | Country Comp | None |
| `System of trade` | `system_of_trade` | `str` | Country demographic/economic metadata: System of trade | N/A | `Special trade system` | 17.01% | No | Country Comp | None |
| `Government Accounting concept` | `government_accounting_concept` | `str` | Country demographic/economic metadata: Government Accounting concept | N/A | `Consolidated central government` | 33.2% | No | Country Comp | None |
| `IMF data dissemination standard` | `imf_data_dissemination_standard` | `str` | Country demographic/economic metadata: IMF data dissemination standard | N/A | `General Data Dissemination System (GDDS)` | 24.9% | No | Country Comp | None |
| `Latest population census` | `latest_population_census` | `str` | Country demographic/economic metadata: Latest population census | N/A | `2010` | 11.62% | No | Country Comp | None |
| `Latest household survey` | `latest_household_survey` | `str` | Country demographic/economic metadata: Latest household survey | N/A | `Multiple Indicator Cluster Survey (MICS), 2010/11` | 41.49% | No | Country Comp | None |
| `Source of most recent Income and expenditure data` | `source_of_most_recent_income_and_expenditure_data` | `str` | Country demographic/economic metadata: Source of most recent Income and expenditure data | N/A | `Integrated household survey (IHS), 2008` | 33.61% | No | Country Comp | None |
| `Vital registration complete` | `vital_registration_complete` | `str` | Country demographic/economic metadata: Vital registration complete | N/A | `Yes` | 53.94% | No | Country Comp | None |
| `Latest agricultural census` | `latest_agricultural_census` | `str` | Country demographic/economic metadata: Latest agricultural census | N/A | `2013/14` | 41.08% | No | Country Comp | None |
| `Latest industrial data` | `latest_industrial_data` | `float64` | Country demographic/economic metadata: Latest industrial data | N/A | `2010.0` | 55.6% | No | Country Comp | None |
| `Latest trade data` | `latest_trade_data` | `float64` | Country demographic/economic metadata: Latest trade data | N/A | `2012.0` | 23.24% | No | Country Comp | None |
| `Latest water withdrawal data` | `latest_water_withdrawal_data` | `str` | Country demographic/economic metadata: Latest water withdrawal data | N/A | `2000` | 25.73% | No | Country Comp | None |
| `Unnamed: 31` | `unnamed:_31` | `float64` | Country demographic/economic metadata: Unnamed: 31 | N/A | `N/A (All Null)` | 100.0% | No | Country Comp | None |

---

## Six Required KPIs & Source Mapping Summary

The table below details how the six required project KPIs are supported across datasets, distinguishing between actual values, benchmark scores, and derived calculations:


| KPI # | KPI Name | Target Type | Primary Source Column(s) | Dataset Source | Status & Categorization |
| --- | --- | --- | --- | --- | --- |
| 1 | **Global Ranking Score** | Score & Rank | `Overall_Score`, `RANK_2025`<br>`OverAll Score`, `University Rank` | QS 2025<br>THE 2023 | **Directly Available**: Actual score (0–100) & rank position. |
| 2 | **Research Impact Score** | Score | `Citations_per_Faculty_Score`<br>`Citations Score` | QS 2025<br>THE 2023 | **Directly Available**: Normalized citation impact scores (0–100). |
| 3 | **Faculty-to-Student Ratio** | Actual Ratio vs Score | `No of student per staff`<br>`Faculty_Student_Score` | THE 2023<br>QS 2025 | **Directly Available** in THE (Actual Ratio: Students/Staff). QS provides Score. Actual Faculty/Student ratio requires derived calculation in QS. |
| 4 | **International Student Percentage** | Actual % vs Score | `International Student`<br>`International_Students_Score` | THE 2023<br>QS 2025 | **Directly Available** in THE (Actual Percentage %). QS provides Score. |
| 5 | **Academic Reputation Score** | Score | `Academic_Reputation_Score`<br>`Teaching Score` | QS 2025<br>THE 2023 | **Directly Available** in QS 2025 (0–100 score). THE provides teaching/reputation proxy score. |
| 6 | **Research Productivity Index** | Derived Metric / Score | `Research Score`<br>`International_Research_Network_Score` | THE 2023<br>QS 2025 | **Requires Derived Calculation**: Raw paper count per faculty is not directly available; supported via normalized score indexes. |