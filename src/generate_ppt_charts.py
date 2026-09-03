import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

sido = pd.read_csv("data/sido_master_complete.csv")
gg = pd.read_csv("data/gyeonggi_master_analysis.csv").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------------------------------------
# Chart 1: Sido Disparity Clean Horizontal Bar (for Slide 2)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=300)
sido_sorted = sido.sort_values(by='total_rate', ascending=True)
colors = ['#e53e3e' if r < 20 else ('#3182ce' if r > 40 else '#718096') for r in sido_sorted['total_rate']]

bars = ax.barh(sido_sorted['region'], sido_sorted['total_rate'], color=colors, height=0.7, edgecolor='none')
ax.axvline(34.2, color='#4a5568', linestyle='--', linewidth=1.2, label='전국 평균 (34.2%)')

for bar, v_rate in zip(bars, sido_sorted['vulnerable_rate']):
    w = bar.get_width()
    ax.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.1f}% (교통약자 {v_rate:.1f}%)', 
            va='center', ha='left', fontsize=8, color='#2d3748', fontweight='bold' if w > 50 or w < 15 else 'normal')

ax.set_title("17개 시·도별 저상버스 도입률 vs 교통약자 비율", fontsize=11, fontweight='bold', color='#1a365d', pad=10)
ax.set_xlabel("저상버스 도입률 (%)", fontsize=9, color='#4a5568')
ax.set_xlim(0, 68)
ax.tick_params(axis='both', labelsize=8)
ax.legend(loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig("results/ppt_chart_sido.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Chart 2: National Scatter with Inverted Trend (for Slide 2)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=300)
sc = ax.scatter(sido['vulnerable_rate'], sido['total_rate'], s=sido['fiscal_rate']*3.5, 
                c=sido['fiscal_rate'], cmap='RdYlBu', alpha=0.85, edgecolors='#2d3748', linewidth=0.8)

# trendline
m, b = np.polyfit(sido['vulnerable_rate'], sido['total_rate'], 1)
x_seq = np.linspace(sido['vulnerable_rate'].min(), sido['vulnerable_rate'].max(), 50)
ax.plot(x_seq, m*x_seq + b, color='#e53e3e', linestyle='--', linewidth=1.5, label='음(-)의 상관관계 (r = -0.435)')

for _, row in sido.iterrows():
    ax.annotate(row['region'][:2], (row['vulnerable_rate']+0.3, row['total_rate']+0.6), fontsize=8, color='#1a202c')

ax.set_title("전국 시·도: 교통약자 비율이 높을수록 저상버스는 감소", fontsize=11, fontweight='bold', color='#1a365d', pad=10)
ax.set_xlabel("교통약자(고령자+등록장애인) 비율 (%)", fontsize=9)
ax.set_ylabel("저상버스 도입률 (%)", fontsize=9)
ax.tick_params(axis='both', labelsize=8)
ax.legend(loc='upper right', fontsize=8)
cbar = fig.colorbar(sc, ax=ax, orientation='horizontal', fraction=0.04, pad=0.18)
cbar.set_label('지자체 재정자립도 (%) [푸를수록 부유]', fontsize=8)
cbar.ax.tick_params(labelsize=7)
plt.tight_layout()
plt.savefig("results/ppt_chart_scatter_sido.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Chart 3: Gyeonggi 4-Quadrant Priority Matrix (for Slide 3)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
med_x = gg['vulnerable_rate'].median()
med_y = gg['low_floor_route_ratio'].median()

ax.axvline(med_x, color='#a0aec0', linestyle='--', linewidth=1)
ax.axhline(med_y, color='#a0aec0', linestyle='--', linewidth=1)

sc = ax.scatter(gg['vulnerable_rate'], gg['low_floor_route_ratio'], s=gg['fiscal_rate']*4.5, 
                c=gg['fiscal_rate'], cmap='RdYlBu', alpha=0.85, edgecolors='#2d3748', linewidth=0.8)

for _, row in gg.iterrows():
    dx, dy = 0.3, 0.7
    if row['관할시군'] in ['가평군', '연천군']:
        dy = 1.3
    elif row['관할시군'] in ['하남시']:
        dy = -2.2
    ax.annotate(row['관할시군'], (row['vulnerable_rate']+dx, row['low_floor_route_ratio']+dy), fontsize=7.5)

# Highlighting boxes
ax.text(28.0, 3.0, "【제1우선 긴급투입 지역】\n• 교통약자 30~40% 밀집\n• 저상버스 노선 0~12% 바닥\n• 가평·연천·여주·동두천·포천", 
        fontsize=8.5, color='#9b2c2c', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff5f5', edgecolor='#feb2b2', alpha=0.9))

ax.text(14.0, 58.0, "【자원 집중 지역】\n• 교통약자 15~20% 상대적 저조\n• 저상버스 노선 50~64% 집중\n• 하남·광명·부천·수원", 
        fontsize=8.5, color='#2b6cb0', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#ebf8ff', edgecolor='#bee3f8', alpha=0.9))

ax.set_title("경기도 31개 시·군: 수요-공급 4분면 매트릭스 (노선 6,431개 전수)", fontsize=11, fontweight='bold', color='#1a365d', pad=10)
ax.set_xlabel("교통약자 인구 비율 (%) → [수요]", fontsize=9)
ax.set_ylabel("저상버스 운행 노선 비율 (%) → [공급]", fontsize=9)
ax.set_xlim(13, 42)
ax.set_ylim(-3, 70)
ax.tick_params(axis='both', labelsize=8)

cbar = fig.colorbar(sc, ax=ax, orientation='vertical', fraction=0.03, pad=0.02)
cbar.set_label('재정자립도 (%)', fontsize=8)
cbar.ax.tick_params(labelsize=7)

plt.tight_layout()
plt.savefig("results/ppt_chart_quadrant.png", dpi=300)
plt.close()
print("All PPT charts generated successfully!")
