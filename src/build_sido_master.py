import pandas as pd

# 1. Bus Data
df_bus = pd.read_csv("data/low_floor_bus_2023_by_sido.csv")

# 2. Disabled Data from KOSIS (DT_1YL202003E)
df_dis = pd.read_csv("data/kosis_disabled_sigungu_2023.csv")

# 3. Elderly & Total Pop Data from KOSIS (DT_1YL20631)
df_eld = pd.read_csv("data/kosis_elderly_sigungu_2023.csv")

# 4. Fiscal Independence Data from KOSIS (DT_1YL20921)
df_fis = pd.read_csv("data/kosis_fiscal_sigungu_2023.csv")

# Exact mapping between bus region name and KOSIS C1_NM
sido_kosis_map = {
    '서울특별시': '서울특별시',
    '부산광역시': '부산광역시',
    '대구광역시': '대구광역시',
    '인천광역시': '인천광역시',
    '광주광역시': '광주광역시',
    '대전광역시': '대전광역시',
    '울산광역시': '울산광역시',
    '세종특별자치시': '세종특별자치시',
    '경기도': '경기도',
    '강원특별자치도': '강원특별자치도',
    '충청북도': '충청북도',
    '충청남도': '충청남도',
    '전라북도': '전북특별자치도',
    '전라남도': '전라남도',
    '경상북도': '경상북도',
    '경상남도': '경상남도',
    '제주특별자치도': '제주특별자치도'
}

records = []
for idx, r in df_bus.iterrows():
    region = r['region']
    kosis_name = sido_kosis_map[region]
    
    # Disabled population (note: Jeju is recorded as '제주도' in the disabled dataset)
    dis_name = '제주도' if kosis_name == '제주특별자치도' else kosis_name
    r_dis = df_dis[df_dis['C1_NM'] == dis_name]
    dis_pop = float(r_dis['DT'].values[0])
    
    # Elderly rate and Total population
    r_eld = df_eld[df_eld['C1_NM'] == kosis_name]
    tot_pop = float(r_eld[r_eld['ITM_NM'].str.contains('전체인구')]['DT'].values[0])
    eld_rate = float(r_eld[r_eld['ITM_NM'].str.contains('고령인구비율')]['DT'].values[0])
    
    # Fiscal independence (세입과목개편전 standard)
    r_fis = df_fis[df_fis['C1_NM'] == kosis_name]
    fis_rate = float(r_fis[r_fis['ITM_NM'].str.contains('세입과목개편전')]['DT'].values[0])
    
    # Calculations
    dis_rate = (dis_pop / tot_pop) * 100.0
    vul_rate = eld_rate + dis_rate
    
    rec = dict(r)
    rec['key'] = region[:2]
    rec['total_pop'] = tot_pop
    rec['disabled_pop'] = dis_pop
    rec['elderly_rate'] = eld_rate
    rec['disabled_rate'] = dis_rate
    rec['vulnerable_rate'] = vul_rate
    rec['fiscal_rate'] = fis_rate
    records.append(rec)

df_master = pd.DataFrame(records)

df_master.to_csv("data/sido_master_complete.csv", index=False, encoding="utf-8-sig")
print("Saved data/sido_master_complete.csv successfully with exact 17 sido KOSIS metrics!")
print(df_master[['region', 'total_pop', 'disabled_pop', 'elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate', 'total_rate']])
