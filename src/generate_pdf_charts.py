# generate_pdf_charts.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Font setup
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

os.makedirs('results', exist_ok=True)

# ----------------------------------------------------
# Chart 1: Sido Scatter Plot with Key Callouts
# ----------------------------------------------------
sido_df = pd.read_csv('data/sido_master_complete.csv')
fig, ax = plt.subplots(figsize=(8.5, 4.4), dpi=300)

for idx, row in sido_df.iterrows():
    color = '#ef4444' if row['total_rate'] < 20 else '#3b82f6'
    size = max(50, row['fiscal_rate'] * 3.8)
    ax.scatter(row['vulnerable_rate'], row['total_rate'], color=color, s=size, alpha=0.82, edgecolors='#1e293b', linewidth=0.8, zorder=3)

# OLS Trendline
m, b = np.polyfit(sido_df['vulnerable_rate'], sido_df['total_rate'], 1)
x_vals = np.linspace(13, 35, 100)
ax.plot(x_vals, m*x_vals + b, color='#ef4444', linestyle='--', linewidth=1.6, label=f'OLS 추세선 (r = -0.432, y = {m:.2f}x + {b:.2f})', zorder=2)

# Specific Callout Annotations
callouts = {
    '서울특별시': {'offset': (0.8, -1.0), 'align': 'left'},
    '대구광역시': {'offset': (0.8, 1.5), 'align': 'left'},
    '인천광역시': {'offset': (0.8, -4.5), 'align': 'left'},
    '전라남도': {'offset': (-4.8, 4.0), 'align': 'right'}
}

for idx, row in sido_df.iterrows():
    name = row['region']
    if name in callouts:
        c = callouts[name]
        label_text = f"[{name}]\n약자 {row['vulnerable_rate']}% | 도입 {row['total_rate']}%\n재정자립도 {row['fiscal_rate']}%"
        ax.annotate(label_text,
                    xy=(row['vulnerable_rate'], row['total_rate']),
                    xytext=(row['vulnerable_rate'] + c['offset'][0], row['total_rate'] + c['offset'][1]),
                    fontsize=7.8, weight='bold', color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.35', facecolor='#f8fafc', edgecolor='#64748b', alpha=0.95, linewidth=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.12', color='#334155', lw=1.0),
                    zorder=5)

ax.set_title('[전국 거시 실증] 전국 17개 시·도: 교통약자 비율 vs 저상버스 도입률', fontsize=11, weight='bold', color='#0f172a', pad=12)
ax.set_xlabel('교통약자(고령자+등록장애인) 인구 비율 (%)', fontsize=9, weight='bold', color='#334155')
ax.set_ylabel('저상버스 도입률 (%)', fontsize=9, weight='bold', color='#334155')
ax.set_xlim(12, 36)
ax.set_ylim(5, 65)
ax.grid(True, linestyle=':', color='#cbd5e1', alpha=0.7, zorder=1)
ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

plt.tight_layout()
plt.savefig('results/pdf_chart1_sido.png')
plt.close()
print("Saved results/pdf_chart1_sido.png")

# ----------------------------------------------------
# Chart 2: Gyeonggi 4-Quadrant Bubble Plot with Callouts
# ----------------------------------------------------
gg_df = pd.read_csv('data/gyeonggi_master_analysis.csv')
fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

med_x = 20.8
med_y = 18.6

# Quadrant dividing lines
ax.axvline(med_x, color='#64748b', linestyle='--', linewidth=1.2, alpha=0.8, zorder=2)
ax.axhline(med_y, color='#64748b', linestyle='--', linewidth=1.2, alpha=0.8, zorder=2)
ax.text(med_x + 0.3, 66, '중앙값 20.8%', fontsize=7.5, color='#64748b', weight='bold')
ax.text(38, med_y + 1.2, '중앙값 18.6%', fontsize=7.5, color='#64748b', weight='bold', ha='right')

for idx, row in gg_df.iterrows():
    # Classification
    if row['vulnerable_rate'] > med_x and row['low_floor_route_ratio'] < med_y:
        color = '#ef4444' # Deprived
    elif row['vulnerable_rate'] <= med_x and row['low_floor_route_ratio'] >= med_y:
        color = '#3b82f6' # Concentrated
    else:
        color = '#94a3b8' # Normal
    
    size = max(45, row['fiscal_rate'] * 3.8)
    ax.scatter(row['vulnerable_rate'], row['low_floor_route_ratio'], color=color, s=size, alpha=0.82, edgecolors='#1e293b', linewidth=0.8, zorder=3)

# Key Callouts
gg_callouts = {
    '하남시': {'offset': (-3.5, 3.5)},
    '부천시': {'offset': (1.2, 2.0)},
    '수원시': {'offset': (-3.6, -4.5)},
    '가평군': {'offset': (-2.5, 6.5)},
    '동두천시': {'offset': (1.2, 4.0)},
    '포천시': {'offset': (1.2, -3.5)}
}

for idx, row in gg_df.iterrows():
    name = row['city']
    if name in gg_callouts:
        c = gg_callouts[name]
        routes_info = f"{int(row['low_floor_routes'])}/{int(row['total_routes'])}개"
        label_text = f"[{name}]\n약자 {row['vulnerable_rate']}% | 저상노선 {row['low_floor_route_ratio']}%\n노선수: {routes_info} | 재정 {row['fiscal_rate']}%"
        ax.annotate(label_text,
                    xy=(row['vulnerable_rate'], row['low_floor_route_ratio']),
                    xytext=(row['vulnerable_rate'] + c['offset'][0], row['low_floor_route_ratio'] + c['offset'][1]),
                    fontsize=7.5, weight='bold', color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#475569', alpha=0.95, linewidth=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1', color='#1e293b', lw=1.0),
                    zorder=5)

# Legend patches
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='제1우선 소외구역 (수요 高, 공급 低)', markerfacecolor='#ef4444', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='자원 집중구역 (수요 低, 공급 高)', markerfacecolor='#3b82f6', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='일반 구역 (점 크기: 재정자립도)', markerfacecolor='#94a3b8', markersize=8)
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.9)

ax.set_title('[경기도 미시 전수] 경기도 31개 시·군: 수요-공급 4분면 매트릭스', fontsize=11, weight='bold', color='#0f172a', pad=12)
ax.set_xlabel('교통약자 인구 비율 (%) → [수요]', fontsize=9, weight='bold', color='#334155')
ax.set_ylabel('저상버스 운행 노선 비율 (%) → [공급]', fontsize=9, weight='bold', color='#334155')
ax.set_xlim(12, 42)
ax.set_ylim(-4, 72)
ax.grid(True, linestyle=':', color='#cbd5e1', alpha=0.7, zorder=1)

plt.tight_layout()
plt.savefig('results/pdf_chart2_gyeonggi.png')
plt.close()
print("Saved results/pdf_chart2_gyeonggi.png")
