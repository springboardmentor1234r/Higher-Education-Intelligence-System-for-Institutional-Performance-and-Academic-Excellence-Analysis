import os
import pandas as pd
import numpy as np
import re

BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
RAW_DIR = os.path.join(BASE_DIR, "raw")

def parse_rank(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace('=', '').replace('+', '')
    if s in ['-', 'n/a', 'N/A', 'Reporter', '']:
        return np.nan
    if '-' in s or '–' in s:
        parts = re.split(r'[-–]', s)
        try:
            nums = [float(p.strip()) for p in parts if p.strip().isdigit()]
            if len(nums) > 0:
                return np.mean(nums)
        except:
            pass
    m = re.search(r'\d+', s)
    if m:
        return float(m.group(0))
    return np.nan

def parse_score(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ['-', 'n/a', 'N/A', '', 'n/a ']:
        return np.nan
    if '-' in s or '–' in s:
        parts = re.split(r'[-–]', s)
        try:
            nums = [float(p.strip()) for p in parts]
            if len(nums) > 0:
                return np.mean(nums)
        except:
            pass
    try:
        return float(s)
    except:
        return np.nan

def parse_int_commas(val):
    if pd.isna(val):
        return np.nan
    s = str(val).replace(',', '').strip()
    if s in ['-', 'n/a', 'N/A', '']:
        return np.nan
    try:
        return float(s)
    except:
        return np.nan

def parse_pct(val):
    if pd.isna(val):
        return np.nan
    s = str(val).replace('%', '').strip()
    if s in ['-', 'n/a', 'N/A', '']:
        return np.nan
    try:
        return float(s)
    except:
        return np.nan

def clean_qs(df):
    df_c = df.copy()
    df_c['year'] = 2025
    df_c['source'] = 'QS'
    df_c['global_rank'] = df_c['RANK_2025'].apply(parse_rank)
    df_c['overall_score'] = df_c['Overall_Score'].apply(parse_score)
    df_c['academic_reputation'] = df_c['Academic_Reputation_Score'].apply(parse_score)
    df_c['employer_reputation'] = df_c['Employer_Reputation_Score'].apply(parse_score)
    df_c['faculty_student_score'] = df_c['Faculty_Student_Score'].apply(parse_score)
    df_c['citation_score'] = df_c['Citations_per_Faculty_Score'].apply(parse_score)
    df_c['research_score'] = df_c['Citations_per_Faculty_Score'].apply(parse_score) # proxy score
    df_c['intl_faculty_score'] = df_c['International_Faculty_Score'].apply(parse_score)
    df_c['intl_student_score'] = df_c['International_Students_Score'].apply(parse_score)
    df_c['intl_research_network'] = df_c['International_Research_Network_Score'].apply(parse_score)
    df_c['sustainability_score'] = df_c['Sustainability_Score'].apply(parse_score)
    
    # QS does NOT provide raw student counts or exact student-staff ratio or actual intl student %, only scores
    df_c['total_students'] = np.nan
    df_c['students_per_staff'] = np.nan
    df_c['international_students'] = np.nan
    df_c['intl_student_pct'] = np.nan
    
    return df_c

def clean_the(df):
    df_c = df.copy()
    df_c['year'] = 2024
    df_c['source'] = 'THE'
    df_c['global_rank'] = df_c['rank'].apply(parse_rank)
    df_c['overall_score'] = df_c['scores_overall'].apply(parse_score)
    df_c['academic_reputation'] = df_c['scores_teaching'].apply(parse_score)
    df_c['employer_reputation'] = df_c['scores_industry_income'].apply(parse_score) # industry income
    df_c['research_score'] = df_c['scores_research'].apply(parse_score)
    df_c['citation_score'] = df_c['scores_citations'].apply(parse_score)
    
    df_c['total_students'] = df_c['stats_number_students'].apply(parse_int_commas)
    df_c['students_per_staff'] = df_c['stats_student_staff_ratio'].apply(parse_score)
    df_c['intl_student_pct'] = df_c['stats_pc_intl_students'].apply(parse_pct)
    
    # calculate international_students if pct and total present
    df_c['international_students'] = np.where(
        df_c['total_students'].notnull() & df_c['intl_student_pct'].notnull(),
        (df_c['total_students'] * df_c['intl_student_pct'] / 100.0).round(),
        np.nan
    )
    
    return df_c

def clean_wur(df):
    df_c = df.copy()
    df_c['year'] = 2023
    df_c['source'] = 'WUR'
    df_c['global_rank'] = df_c['University Rank'].apply(parse_rank)
    df_c['overall_score'] = df_c['OverAll Score'].apply(parse_score)
    df_c['academic_reputation'] = df_c['Teaching Score'].apply(parse_score)
    df_c['employer_reputation'] = df_c['Industry Income Score'].apply(parse_score)
    df_c['research_score'] = df_c['Research Score'].apply(parse_score)
    df_c['citation_score'] = df_c['Citations Score'].apply(parse_score)
    
    df_c['total_students'] = df_c['No of student'].apply(parse_int_commas)
    df_c['students_per_staff'] = df_c['No of student per staff'].apply(parse_score)
    df_c['intl_student_pct'] = df_c['International Student'].apply(parse_pct)
    
    df_c['international_students'] = np.where(
        df_c['total_students'].notnull() & df_c['intl_student_pct'].notnull(),
        (df_c['total_students'] * df_c['intl_student_pct'] / 100.0).round(),
        np.nan
    )
    
    return df_c
