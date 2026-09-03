import pandas as pd
import numpy as np

# 1. Load Gyeonggi Bus Summary (31 cities)
df_gg_bus = pd.read_csv("data/gyeonggi_city_bus_summary.csv")

# 2. Load KOSIS tables
df_dis = pd.read_csv("data/kosis_disabled_sigungu_2023.csv")
df_eld = pd.read_csv("data/kosis_elderly_sigungu_2023.csv")
df_fis = pd.read_csv("data/kosis_fiscal_sigungu_2023.csv")

# Let's clean and match city names
# Note: KOSIS has entries like '수원시', '고양시', '용인시' or sub-districts like '장안구'
# Let's inspect which of the 31 cities match directly in C1_NM
matched_data = []

for city in df_gg_bus['관할시군']:
    # Disabled pop
    sub_dis = df_dis[df_dis['C1_NM'] == city]
    if sub_dis.empty:
        # maybe sum of districts? e.g. for 수원시, sum 장안구, 권선구, 팔달구, 영통구
        sub_dis = df_dis[df_dis['C1_NM'].str.contains(city, na=False)]
    dis_val = pd.to_numeric(sub_dis['DT'], errors='coerce').sum() if not sub_dis.empty else np.nan
    
    # Elderly
    sub_eld_tot = df_eld[(df_eld['C1_NM'] == city) & (df_eld['ITM_NM'].str.contains("전체인구", na=False))]
    if sub_eld_tot.empty:
        sub_eld_tot = df_eld[(df_eld['C1_NM'].str.contains(city, na=False)) & (df_eld['ITM_NM'].str.contains("전체인구", na=False))]
    tot_pop = pd.to_numeric(sub_eld_tot['DT'], errors='coerce').sum() if not sub_eld_tot.empty else np.nan
    
    sub_eld_65 = df_eld[(df_eld['C1_NM'] == city) & (df_eld['ITM_NM'].str.contains("65세이상", na=False))]
    if sub_eld_65.empty:
        sub_eld_65 = df_eld[(df_eld['C1_NM'].str.contains(city, na=False)) & (df_eld['ITM_NM'].str.contains("65세이상", na=False))]
    eld_pop = pd.to_numeric(sub_eld_65['DT'], errors='coerce').sum() if not sub_eld_65.empty else np.nan
    
    # Fiscal
    sub_fis = df_fis[df_fis['C1_NM'] == city]
    if sub_fis.empty:
        sub_fis = df_fis[df_fis['C1_NM'].str.contains(city, na=False)]
    fis_val = pd.to_numeric(sub_fis['DT'], errors='coerce').mean() if not sub_fis.empty else np.nan
    
    matched_data.append({
        "city": city,
        "total_pop": tot_pop,
        "disabled_pop": dis_val,
        "elderly_pop": eld_pop,
        "elderly_rate": (eld_pop / tot_pop * 100) if tot_pop > 0 else np.nan,
        "disabled_rate": (dis_val / tot_pop * 100) if tot_pop > 0 else np.nan,
        "vulnerable_rate": ((eld_pop + dis_val) / tot_pop * 100) if tot_pop > 0 else np.nan,
        "fiscal_rate": fis_val
    })

df_gg_kosis = pd.DataFrame(matched_data)
df_gg_master = df_gg_bus.merge(df_gg_kosis, left_on='관할시군', right_on='city')
print(df_gg_master.head(10))
df_gg_master.to_csv("data/gyeonggi_master_analysis.csv", index=False, encoding="utf-8-sig")
print("Saved data/gyeonggi_master_analysis.csv successfully!")
