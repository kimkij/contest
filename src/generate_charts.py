import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set Korean font for Windows
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

sido = pd.read_csv("data/sido_master_complete.csv")
gg = pd.read_csv("data/gyeonggi_master_analysis.csv").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# 1. 전국 17개 시도 분석 차트
ax1 = axes[0]
sc1 = ax1.scatter(sido['vulnerable_rate'], sido['total_rate'], s=sido['fiscal_rate']*3, c=sido['fiscal_rate'], cmap='coolwarm', alpha=0.8, edgecolors='black')
# Trendline
m, b = np.polyfit(sido['vulnerable_rate'], sido['total_rate'], 1)
x_seq = np.linspace(sido['vulnerable_rate'].min(), sido['vulnerable_rate'].max(), 50)
ax1.plot(x_seq, m*x_seq + b, color='red', linestyle='--', label=f'추세선 (r = -0.435)')

for idx, row in sido.iterrows():
    ax1.annotate(row['region'][:2], (row['vulnerable_rate']+0.3, row['total_rate']+0.5), fontsize=9)

ax1.set_title("[전국 17개 시·도] 교통약자 비율 vs 저상버스 보급률\n(점 크기/색상: 재정자립도)", fontsize=13, fontweight='bold')
ax1.set_xlabel("교통약자(장애인+고령자) 인구비율 (%)", fontsize=11)
ax1.set_ylabel("저상버스 보급률 (%)", fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# 2. 경기도 31개 시군 분석 차트
ax2 = axes[1]
sc2 = ax2.scatter(gg['vulnerable_rate'], gg['low_floor_route_ratio'], s=gg['fiscal_rate']*4, c=gg['fiscal_rate'], cmap='coolwarm', alpha=0.8, edgecolors='black')
m2, b2 = np.polyfit(gg['vulnerable_rate'], gg['low_floor_route_ratio'], 1)
x_seq2 = np.linspace(gg['vulnerable_rate'].min(), gg['vulnerable_rate'].max(), 50)
ax2.plot(x_seq2, m2*x_seq2 + b2, color='red', linestyle='--', label=f'추세선 (r = -0.430, t = -2.56)')

for idx, row in gg.iterrows():
    if row['low_floor_route_ratio'] > 50 or row['vulnerable_rate'] > 30 or row['low_floor_route_ratio'] < 10:
        ax2.annotate(row['관할시군'], (row['vulnerable_rate']+0.2, row['low_floor_route_ratio']+0.8), fontsize=8)

ax2.set_title("[경기도 31개 시·군] 교통약자 비율 vs 저상버스 노선비율\n(점 크기/색상: 재정자립도)", fontsize=13, fontweight='bold')
ax2.set_xlabel("교통약자(장애인+고령자) 인구비율 (%)", fontsize=11)
ax2.set_ylabel("저상버스 운행 노선 비율 (%)", fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')

# Colorbar
cbar = fig.colorbar(sc2, ax=axes.ravel().tolist(), orientation='horizontal', fraction=0.04, pad=0.12)
cbar.set_label('지자체 재정자립도 (%)', fontsize=11)

plt.suptitle("공모전 분석 실증 결과: '교통약자가 많을수록 저상버스는 오히려 적다' (역진적 배정 규명)", fontsize=15, fontweight='bold', y=0.98)
plt.savefig("results/analysis_scatter_plot.png", dpi=300, bbox_inches='tight')
print("Saved chart to results/analysis_scatter_plot.png")
