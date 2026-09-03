import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

gg = pd.read_csv("data/gyeonggi_master_analysis.csv").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])

fig, ax = plt.subplots(figsize=(11, 7.5))

med_x = gg['vulnerable_rate'].median()
med_y = gg['low_floor_route_ratio'].median()

ax.axvline(med_x, color='#888888', linestyle='--', alpha=0.7)
ax.axhline(med_y, color='#888888', linestyle='--', alpha=0.7)

sc = ax.scatter(gg['vulnerable_rate'], gg['low_floor_route_ratio'], s=gg['fiscal_rate']*5, 
                c=gg['fiscal_rate'], cmap='YlOrRd_r', alpha=0.85, edgecolors='black')

for _, row in gg.iterrows():
    # adjust positions to avoid overlap
    dx, dy = 0.4, 0.8
    if row['관할시군'] in ['가평군', '연천군']:
        dy = 1.5
    elif row['관할시군'] in ['하남시']:
        dy = -2.2
    ax.annotate(row['관할시군'], (row['vulnerable_rate']+dx, row['low_floor_route_ratio']+dy), fontsize=9)

# Quadrant labels placed cleanly
ax.text(28.0, 5.0, 
        "【제1우선 긴급투입지역 (소외지대)】\n• 교통약자 밀집(30%~40%), 저상버스 전무(0%~12%)\n• 가평·연천·여주·동두천·포천\n• 재정자립도 최하위(14%~20%)로 자체 확충 불가", 
        fontsize=10.5, color='#b71c1c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.6', facecolor='#ffebee', edgecolor='#ef5350', alpha=0.9))

ax.text(14.0, 58.0, 
        "【자원 집중지역 (도심권)】\n• 교통약자 비율 20% 내외, 저상버스 도입 50%~64%\n• 하남·광명·부천·수원·과천\n• 재정자립도 우수(35%~50%)로 선제적 전환", 
        fontsize=10.5, color='#0d47a1', fontweight='bold', bbox=dict(boxstyle='round,pad=0.6', facecolor='#e3f2fd', edgecolor='#42a5f5', alpha=0.9))

ax.set_title("[경기도 31개 시·군] 교통약자 수요-저상버스 공급 4분면 매트릭스\n(점 크기/색상: 재정자립도 - 붉을수록 재정 열악)", fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel("교통약자(고령자+장애인) 인구 비율 (%) → [수요 지표]", fontsize=11)
ax.set_ylabel("저상버스 운행 노선 비율 (%) → [공급 지표]", fontsize=11)
ax.set_xlim(13, 42)
ax.set_ylim(-3, 70)
ax.grid(True, linestyle=':', alpha=0.4)

cbar = fig.colorbar(sc, ax=ax, orientation='vertical', fraction=0.03, pad=0.03)
cbar.set_label('재정자립도 (%)', fontsize=10)

plt.tight_layout()
plt.savefig("results/chart_quadrant_matrix.png", dpi=300)
plt.close()
print("Adjusted and saved results/chart_quadrant_matrix.png")
