import pandas as pd

def normalize_sido(name):
    if not isinstance(name, str):
        return ""
    name = name.strip()
    if "서울" in name: return "서울"
    if "부산" in name: return "부산"
    if "대구" in name: return "대구"
    if "인천" in name: return "인천"
    if "광주" in name: return "광주"
    if "대전" in name: return "대전"
    if "울산" in name: return "울산"
    if "세종" in name: return "세종"
    if "경기" in name: return "경기"
    if "강원" in name: return "강원"
    if "충북" in name or "충청북" in name: return "충북"
    if "충남" in name or "충청남" in name: return "충남"
    if "전북" in name or "전라북" in name: return "전북"
    if "전남" in name or "전라남" in name: return "전남"
    if "경북" in name or "경상북" in name: return "경북"
    if "경남" in name or "경상남" in name: return "경남"
    if "제주" in name: return "제주"
    return name

# 1. Bus
df_bus = pd.read_csv("data/low_floor_bus_2023_by_sido.csv")
df_bus['key'] = df_bus['region'].apply(normalize_sido)

# 2. Disabled
df_dis = pd.read_csv("data/kosis_disabled_sigungu_2023.csv")
df_dis['key'] = df_dis['C1_NM'].apply(normalize_sido)
# filter to 17 sidos
sido_keys = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
df_dis_sido = df_dis[df_dis['key'].isin(sido_keys) & (df_dis['C1_NM'] != '제주시')].copy()
df_dis_sido['disabled_pop'] = pd.to_numeric(df_dis_sido['DT'], errors='coerce')
df_dis_map = df_dis_sido.set_index('key')['disabled_pop'].to_dict()

# 3. Elderly & Total Pop
df_eld = pd.read_csv("data/kosis_elderly_sigungu_2023.csv")
df_eld['key'] = df_eld['C1_NM'].apply(normalize_sido)
df_eld_sido = df_eld[df_eld['key'].isin(sido_keys) & (df_eld['C1_NM'] != '제주시')].copy()

# Total pop
df_tot = df_eld_sido[df_eld_sido['ITM_NM'].str.contains("전체인구", na=False)].copy()
df_tot['total_pop'] = pd.to_numeric(df_tot['DT'], errors='coerce')
tot_pop_map = df_tot.set_index('key')['total_pop'].to_dict()

# Elderly rate
df_er = df_eld_sido[df_eld_sido['ITM_NM'].str.contains("고령인구비율", na=False)].copy()
df_er['elderly_rate'] = pd.to_numeric(df_er['DT'], errors='coerce')
eld_rate_map = df_er.set_index('key')['elderly_rate'].to_dict()

# 4. Fiscal independence
df_fis = pd.read_csv("data/kosis_fiscal_sigungu_2023.csv")
df_fis['key'] = df_fis['C1_NM'].apply(normalize_sido)
# take the modern accounting definition (세입과목개편후) if available, or first
df_fis_sido = df_fis[df_fis['key'].isin(sido_keys)].drop_duplicates(subset=['key']).copy()
df_fis_sido['fiscal_rate'] = pd.to_numeric(df_fis_sido['DT'], errors='coerce')
fiscal_map = df_fis_sido.set_index('key')['fiscal_rate'].to_dict()

# Build merged master dataframe
df_master = df_bus.copy()
df_master['total_pop'] = df_master['key'].map(tot_pop_map)
df_master['disabled_pop'] = df_master['key'].map(df_dis_map)
df_master['elderly_rate'] = df_master['key'].map(eld_rate_map)
df_master['fiscal_rate'] = df_master['key'].map(fiscal_map)

# Calculate Disabled pop rate (%)
df_master['disabled_rate'] = (df_master['disabled_pop'] / df_master['total_pop']) * 100
# Combined Transportation Vulnerable Population Rate (%)
# 교통약자(장애인+고령자) 추정 비율 (%)
df_master['vulnerable_rate'] = df_master['elderly_rate'] + df_master['disabled_rate']

df_master.to_csv("data/sido_master_complete.csv", index=False, encoding="utf-8-sig")
print("Saved data/sido_master_complete.csv successfully!")
print(df_master[['region', 'city_bus_rate', 'total_rate', 'elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate']])
