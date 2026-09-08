import pandas as pd

df = pd.read_csv('data/sido_master_complete.csv', encoding='utf-8')
print('=== SIDO SORTED BY TOTAL_RATE DESC ===')
df_sido = df.sort_values(by='total_rate', ascending=False)
for idx, r in df_sido.iterrows():
    print(f"{r['region']}: 도입률={r['total_rate']:.1f}%, 시내={r['city_bus_rate']:.1f}%, 약자={r['vulnerable_rate']:.1f}%, 고령={r['elderly_rate']:.1f}%, 장애={r['disabled_rate']:.2f}%, 재정={r['fiscal_rate']:.1f}%")

print('\n=== GYEONGGI SAMPLE SORTED BY LOW_FLOOR_ROUTE_RATIO DESC ===')
sample_cities = ['가평군', '연천군', '여주시', '동두천시', '포천시', '양평군', '수원시', '부천시', '광명시', '하남시', '성남시', '용인시']
df_gg = pd.read_csv('data/gyeonggi_master_analysis.csv', encoding='utf-8')
df_gg_sample = df_gg[df_gg['city'].isin(sample_cities)].sort_values(by='low_floor_route_ratio', ascending=False)
for idx, r in df_gg_sample.iterrows():
    print(f"{r['city']}: 노선비율={r['low_floor_route_ratio']:.1f}%, 노선수={int(r['low_floor_routes'])}/{int(r['total_routes'])}개, 약자={r['vulnerable_rate']:.1f}%, 고령={r['elderly_rate']:.1f}%, 장애={r['disabled_rate']:.2f}%, 재정={r['fiscal_rate']:.1f}%")
