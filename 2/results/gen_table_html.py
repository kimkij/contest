import pandas as pd

df = pd.read_csv('data/sido_master_complete.csv', encoding='utf-8')
print("--- SIDO ROWS ---")
for idx, r in df.sort_values(by='total_rate', ascending=False).iterrows():
    rate = r['total_rate']
    if rate >= 40:
        cls = '우수 도입'
        badge = 'badge-blue'
    elif rate >= 20:
        cls = '보통'
        badge = 'badge-gray'
    elif rate <= 12:
        cls = '전국 최하위'
        badge = 'badge-red'
    else:
        cls = '취약 지역'
        badge = 'badge-red'
    print(f"<tr><td><strong>{r['region']}</strong></td><td>{r['total_rate']:.1f}%</td><td>{r['city_bus_rate']:.1f}%</td><td>{r['vulnerable_rate']:.1f}%</td><td>{r['elderly_rate']:.1f}%</td><td>{r['disabled_rate']:.2f}%</td><td>{r['fiscal_rate']:.1f}%</td><td><span class=\"badge-pill {badge}\">{cls}</span></td></tr>")

print("\n--- GYEONGGI ROWS ---")
sample_cities = ['가평군', '연천군', '여주시', '동두천시', '포천시', '양평군', '수원시', '부천시', '광명시', '하남시', '성남시', '용인시']
df_gg = pd.read_csv('data/gyeonggi_master_analysis.csv', encoding='utf-8')
df_gg_sample = df_gg[df_gg['city'].isin(sample_cities)].sort_values(by='low_floor_route_ratio', ascending=False)
for idx, r in df_gg_sample.iterrows():
    ratio = r['low_floor_route_ratio']
    if ratio >= 50:
        bg = 'style="background:#eff6ff;"'
        cls = '자원 집중지'
        badge = 'badge-blue'
    elif ratio <= 15.5:
        bg = 'style="background:#fef2f2;"'
        if r['city'] == '여주시':
            cls = '제1우선 소외지(소표본)'
        else:
            cls = '제1우선 소외지'
        badge = 'badge-red'
    else:
        bg = ''
        cls = '일반 구역'
        badge = 'badge-gray'
    
    routes_str = f"{int(r['low_floor_routes'])} / {int(r['total_routes'])}개"
    print(f"<tr {bg}><td><strong>{r['city']}</strong></td><td><strong>{r['low_floor_route_ratio']:.1f}%</strong></td><td>{routes_str}</td><td>{r['vulnerable_rate']:.1f}%</td><td>{r['elderly_rate']:.1f}%</td><td>{r['disabled_rate']:.2f}%</td><td>{r['fiscal_rate']:.1f}%</td><td><span class=\"badge-pill {badge}\">{cls}</span></td></tr>")
