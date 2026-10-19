import os
import pandas as pd
import numpy as np
import re
import unicodedata

BASE_DIR = r"c:\Users\Sonia\Downloads\EduVision_DV"
RAW_DIR = os.path.join(BASE_DIR, "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

# Comprehensive Country Standardization Map
COUNTRY_MAP = {
    'China (Mainland)': 'China',
    'Russian Federation': 'Russia',
    'Hong Kong SAR': 'Hong Kong',
    'Hong Kong SAR, China': 'Hong Kong',
    'Macau SAR': 'Macao',
    'Macao SAR, China': 'Macao',
    'Palestinian Territory, Occupied': 'Palestine',
    'West Bank and Gaza': 'Palestine',
    'Iran, Islamic Republic of': 'Iran',
    'Iran, Islamic Rep.': 'Iran',
    'South Korea': 'Korea, Rep.',
    'Republic of Korea': 'Korea, Rep.',
    'Korea, Rep.': 'Korea, Rep.',
    'Slovakia': 'Slovak Republic',
    'Kyrgyzstan': 'Kyrgyz Republic',
    'US': 'United States',
    'USA': 'United States',
    'United States of America': 'United States',
    'UK': 'United Kingdom',
    'Great Britain': 'United Kingdom',
    'Egypt, Arab Rep.': 'Egypt',
    'Venezuela, RB': 'Venezuela',
    'Syrian Arab Republic': 'Syria',
    'Yemen, Rep.': 'Yemen',
    'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
    'Congo, Rep.': 'Republic of the Congo',
    'Gambia, The': 'Gambia',
    'Bahamas, The': 'Bahamas',
    'Macedonia, FYR': 'North Macedonia',
    'St. Lucia': 'Saint Lucia',
    'St. Vincent and the Grenadines': 'Saint Vincent and the Grenadines',
    'St. Kitts and Nevis': 'Saint Kitts and Nevis',
    'Czechia': 'Czech Republic'
}

# Standardized Continent-Level Region Lookup by Country
COUNTRY_TO_REGION = {
    'United States': 'North America', 'Canada': 'North America', 'Bermuda': 'North America', 'Puerto Rico': 'North America',
    'Argentina': 'Latin America & Caribbean', 'Bahamas': 'Latin America & Caribbean', 'Barbados': 'Latin America & Caribbean',
    'Bolivia': 'Latin America & Caribbean', 'Brazil': 'Latin America & Caribbean', 'Chile': 'Latin America & Caribbean',
    'Colombia': 'Latin America & Caribbean', 'Costa Rica': 'Latin America & Caribbean', 'Cuba': 'Latin America & Caribbean',
    'Dominican Republic': 'Latin America & Caribbean', 'Ecuador': 'Latin America & Caribbean', 'El Salvador': 'Latin America & Caribbean',
    'Guatemala': 'Latin America & Caribbean', 'Guyana': 'Latin America & Caribbean', 'Haiti': 'Latin America & Caribbean',
    'Honduras': 'Latin America & Caribbean', 'Jamaica': 'Latin America & Caribbean', 'Mexico': 'Latin America & Caribbean',
    'Nicaragua': 'Latin America & Caribbean', 'Panama': 'Latin America & Caribbean', 'Paraguay': 'Latin America & Caribbean',
    'Peru': 'Latin America & Caribbean', 'Suriname': 'Latin America & Caribbean', 'Trinidad and Tobago': 'Latin America & Caribbean',
    'Uruguay': 'Latin America & Caribbean', 'Venezuela': 'Latin America & Caribbean',
    'Albania': 'Europe', 'Andorra': 'Europe', 'Austria': 'Europe', 'Belarus': 'Europe', 'Belgium': 'Europe',
    'Bosnia and Herzegovina': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Cyprus': 'Europe',
    'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe', 'France': 'Europe',
    'Georgia': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe', 'Iceland': 'Europe',
    'Ireland': 'Europe', 'Italy': 'Europe', 'Kosovo': 'Europe', 'Latvia': 'Europe', 'Liechtenstein': 'Europe',
    'Lithuania': 'Europe', 'Luxembourg': 'Europe', 'Malta': 'Europe', 'Moldova': 'Europe', 'Monaco': 'Europe',
    'Montenegro': 'Europe', 'Netherlands': 'Europe', 'North Macedonia': 'Europe', 'Northern Cyprus': 'Europe',
    'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe', 'Russia': 'Europe',
    'San Marino': 'Europe', 'Serbia': 'Europe', 'Slovak Republic': 'Europe', 'Slovenia': 'Europe', 'Spain': 'Europe',
    'Sweden': 'Europe', 'Switzerland': 'Europe', 'Ukraine': 'Europe', 'United Kingdom': 'Europe',
    'Australia': 'Oceania', 'Fiji': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
    'Algeria': 'Africa', 'Angola': 'Africa', 'Botswana': 'Africa', 'Cameroon': 'Africa', 'Egypt': 'Africa',
    'Ethiopia': 'Africa', 'Ghana': 'Africa', 'Kenya': 'Africa', 'Mauritius': 'Africa', 'Morocco': 'Africa',
    'Mozambique': 'Africa', 'Namibia': 'Africa', 'Nigeria': 'Africa', 'Rwanda': 'Africa', 'Senegal': 'Africa',
    'South Africa': 'Africa', 'Sudan': 'Africa', 'Tanzania': 'Africa', 'Tunisia': 'Africa', 'Uganda': 'Africa',
    'Zambia': 'Africa', 'Zimbabwe': 'Africa'
}

def remove_accents(input_str):
    if not isinstance(input_str, str):
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_country_name(c):
    if pd.isna(c):
        return "Unknown"
    c_str = str(c).strip()
    return COUNTRY_MAP.get(c_str, c_str)

def get_standardized_region(qs_region_val, country_name):
    if pd.notnull(qs_region_val) and str(qs_region_val).strip() not in ['Not Classified', 'Other', 'nan', '']:
        r = str(qs_region_val).strip()
        if r == 'Americas':
            return COUNTRY_TO_REGION.get(country_name, 'North America' if country_name in ['United States', 'Canada'] else 'Latin America & Caribbean')
        elif r in ['Asia', 'Europe', 'Oceania', 'Africa']:
            return r
    return COUNTRY_TO_REGION.get(country_name, None)

def clean_uni_string(name):
    if pd.isna(name):
        return ""
    name = remove_accents(str(name))
    name = name.lower()
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'[^\w\s]', ' ', name)
    name = re.sub(r'^\bthe\b\s+', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def uni_token_key(clean_name):
    stop_words = {'of', 'and', 'the', 'for', 'in', 'at', 'de', 'la', 'des', 'der', 'und', 'di', 'en', 'le'}
    words = sorted([w for w in clean_name.split() if w not in stop_words])
    return " ".join(words)

def build_dimensions():
    df_qs = pd.read_csv(os.path.join(RAW_DIR, "qs_2025.csv"), encoding='latin1')
    df_the = pd.read_csv(os.path.join(RAW_DIR, "the_2024.csv"), encoding='latin1')
    df_wur = pd.read_csv(os.path.join(RAW_DIR, "wur_2023.csv"), encoding='latin1')
    
    ed_dir = os.path.join(RAW_DIR, "world_bank_edstats")
    df_ed_country = pd.read_csv(os.path.join(ed_dir, "EdStatsCountry.csv"), encoding='utf-8')
    
    # 1. Build dim_country
    all_raw_countries = set(df_qs['Location'].dropna().unique()).union(
        set(df_the['location'].dropna().unique())).union(
        set(df_wur['Location'].dropna().unique())).union(
        set(df_ed_country['Table Name'].dropna().unique())).union(
        set(df_ed_country['Short Name'].dropna().unique()))
    
    canon_countries = sorted(list(set([clean_country_name(c) for c in all_raw_countries if c])))
    
    # Map country metadata from EdStatsCountry
    ed_meta = {}
    for idx, r in df_ed_country.iterrows():
        c_name = clean_country_name(r['Table Name'])
        ed_meta[c_name] = {
            'code': r['Country Code'],
            'income_group': r['Income Group'] if pd.notnull(r['Income Group']) else 'Unclassified'
        }
        short_n = clean_country_name(r['Short Name'])
        if short_n not in ed_meta:
            ed_meta[short_n] = ed_meta[c_name]
            
    country_rows = []
    for idx, cname in enumerate(canon_countries, 1):
        cid = f"CTY_{idx:03d}"
        meta = ed_meta.get(cname, {'code': 'N/A', 'income_group': 'Unclassified'})
        reg = COUNTRY_TO_REGION.get(cname, None)
        country_rows.append({
            'country_id': cid,
            'country_name': cname,
            'country_code': meta['code'],
            'region': reg,
            'income_group': meta['income_group']
        })
        
    dim_country = pd.DataFrame(country_rows)
    country_lookup = dict(zip(dim_country['country_name'], dim_country['country_id']))
    
    # 2. Collect all university instances across 3 datasets
    qs_unis = df_qs[['Institution_Name', 'Location', 'Region']].rename(
        columns={'Institution_Name': 'orig_name', 'Location': 'raw_country', 'Region': 'raw_region'}).assign(source='QS')
    the_unis = df_the[['name', 'location']].rename(
        columns={'name': 'orig_name', 'location': 'raw_country'}).assign(raw_region=np.nan, source='THE')
    wur_unis = df_wur[['Name of University', 'Location']].rename(
        columns={'Name of University': 'orig_name', 'Location': 'raw_country'}).assign(raw_region=np.nan, source='WUR')
    
    all_unis = pd.concat([qs_unis, the_unis, wur_unis], ignore_index=True)
    all_unis['country_name'] = all_unis['raw_country'].apply(clean_country_name)
    all_unis['country_id'] = all_unis['country_name'].map(country_lookup)
    all_unis['clean_name'] = all_unis['orig_name'].apply(clean_uni_string)
    all_unis['token_key'] = all_unis['clean_name'].apply(uni_token_key)
    
    # Deduplicate & entity resolve within (country_id, token_key)
    grouped = all_unis.groupby(['country_id', 'token_key'])
    uni_records = []
    
    for (cid, tkey), group in grouped:
        if not tkey:
            continue
        cname = group['country_name'].iloc[0]
        qs_rows = group[group['source'] == 'QS']
        the_rows = group[group['source'] == 'THE']
        if len(qs_rows) > 0:
            canon_name = qs_rows['orig_name'].iloc[0]
            raw_reg = qs_rows['raw_region'].iloc[0]
        elif len(the_rows) > 0:
            canon_name = the_rows['orig_name'].iloc[0]
            raw_reg = np.nan
        else:
            canon_name = group['orig_name'].iloc[0]
            raw_reg = np.nan
            
        region_val = get_standardized_region(raw_reg, cname)
        
        uni_records.append({
            'country_id': cid,
            'country_name': cname,
            'token_key': tkey,
            'university_name': canon_name,
            'region': region_val
        })
        
    uni_df = pd.DataFrame(uni_records)
    uni_df = uni_df.sort_values(['country_name', 'university_name']).reset_index(drop=True)
    uni_df['university_id'] = [f"UNI_{i:04d}" for i in range(1, len(uni_df) + 1)]
    
    dim_university = uni_df[['university_id', 'university_name', 'country_id', 'country_name', 'region']]
    
    return dim_country, dim_university, country_lookup

if __name__ == "__main__":
    dim_country, dim_university, country_lookup = build_dimensions()
    
    print(f"dim_country built: {len(dim_country)} rows")
    print(dim_country['region'].value_counts(dropna=False))
    
    print(f"\ndim_university built: {len(dim_university)} rows")
    print(dim_university['region'].value_counts(dropna=False))
    
    # Save dimensions to data/cleaned
    dim_country.to_csv(os.path.join(CLEANED_DIR, "dim_country.csv"), index=False)
    dim_university.to_csv(os.path.join(CLEANED_DIR, "dim_university.csv"), index=False)
    
    dim_country.to_excel(os.path.join(CLEANED_DIR, "dim_country.xlsx"), index=False)
    dim_university.to_excel(os.path.join(CLEANED_DIR, "dim_university.xlsx"), index=False)
    
    print("Exported standardized dim_country and dim_university to CSV and XLSX!")
