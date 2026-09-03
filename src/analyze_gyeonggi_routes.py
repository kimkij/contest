import pandas as pd
import numpy as np

# Load Gyeonggi route data
df_gg = pd.read_csv("data/gyeonggi_routes.csv", encoding="cp949")
print(f"Total Gyeonggi routes: {len(df_gg)}")
print("Operating status values:", df_gg['저상버스운행유무'].value_counts())

# Group by 관할시군
gg_group = df_gg.groupby('관할시군').agg(
    total_routes=('노선번호', 'count'),
    low_floor_routes=('저상버스운행유무', lambda x: (x == 'Y').sum())
).reset_index()
gg_group['low_floor_route_ratio'] = (gg_group['low_floor_routes'] / gg_group['total_routes']) * 100
print("\nTop 5 Gyeonggi by low floor route ratio:")
print(gg_group.sort_values(by='low_floor_route_ratio', ascending=False).head(5))

# Load KOSIS sigungu data
df_dis = pd.read_csv("data/kosis_disabled_sigungu_2023.csv")
df_eld = pd.read_csv("data/kosis_elderly_sigungu_2023.csv")
df_fis = pd.read_csv("data/kosis_fiscal_sigungu_2023.csv")

# Match with Gyeonggi 31 municipalities
# Clean city names (e.g., '수원시', '고양시', '가평군' etc.)
def clean_city(name):
    if not isinstance(name, str): return ""
    return name.split()[0]  # Take first part if '고양시 덕양구' -> '고양시'

# Aggregate KOSIS by 시/군 for Gyeonggi
# Let's inspect C1_NM in df_dis for Gyeonggi
gg_cities = gg_group['관할시군'].unique()
print("\nUnique Gyeonggi 관할시군 in bus routes:", len(gg_cities), gg_cities)

# Merge Gyeonggi bus routes summary
gg_group.to_csv("data/gyeonggi_city_bus_summary.csv", index=False, encoding="utf-8-sig")
