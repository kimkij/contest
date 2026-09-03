import pandas as pd
import numpy as np

def pearson_r(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    mx, my = np.mean(x), np.mean(y)
    r_num = np.sum((x - mx) * (y - my))
    r_den = np.sqrt(np.sum((x - mx)**2) * np.sum((y - my)**2))
    r = r_num / r_den
    # t-stat and approx p-value
    df = n - 2
    t = r * np.sqrt(df / (1 - r**2))
    return r, t

# 1. 전국 17개 시도 분석
sido = pd.read_csv("data/sido_master_complete.csv")
print("="*60)
print("1. 전국 17개 시·도 피어슨 상관계수 분석")
print("="*60)

for var in ['elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate']:
    r, t = pearson_r(sido['city_bus_rate'], sido[var])
    r_tot, t_tot = pearson_r(sido['total_rate'], sido[var])
    print(f"[시내버스도입률 vs {var:15s}]: r = {r:+.3f} (t = {t:+.2f})")
    print(f"[전체버스도입률 vs {var:15s}]: r = {r_tot:+.3f} (t = {t_tot:+.2f})")

# 2. 경기도 31개 시·군 분석
gg = pd.read_csv("data/gyeonggi_master_analysis.csv").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])
print("\n" + "="*60)
print("2. 경기도 31개 시·군 기초지자체 상관계수 분석")
print("="*60)

for var in ['elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate']:
    r, t = pearson_r(gg['low_floor_route_ratio'], gg[var])
    print(f"[저상버스노선비율 vs {var:15s}]: r = {r:+.3f} (t = {t:+.2f})")

# 3. OLS 다중회귀분석 (수학적 행렬 연산)
# y = b0 + b1*vulnerable_rate + b2*fiscal_rate
X = gg[['vulnerable_rate', 'fiscal_rate']].values
y = gg['low_floor_route_ratio'].values
X_mat = np.column_stack([np.ones(len(X)), X])
beta = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ y

# R-squared
y_pred = X_mat @ beta
ss_tot = np.sum((y - np.mean(y))**2)
ss_res = np.sum((y - y_pred)**2)
r2 = 1 - (ss_res / ss_tot)

print("\n" + "="*60)
print("3. 경기도 다중회귀분석 결과 (OLS)")
print("="*60)
print(f"회귀식: 저상버스노선비율 = {beta[0]:.2f} + ({beta[1]:.2f} * 교통약자비율) + ({beta[2]:.2f} * 재정자립도)")
print(f"결정계수 (R-squared): {r2:.4f}")

with open("results/statistical_summary.txt", "w", encoding="utf-8") as out:
    out.write("=== 저상버스 확충 및 교통약자 형평성 분석 결과 요약 ===\n\n")
    out.write("1. 전국 17개 시도 분석:\n")
    for var in ['elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate']:
        r, t = pearson_r(sido['city_bus_rate'], sido[var])
        out.write(f" - 시내버스 저상버스 보급률 vs {var}: r = {r:+.3f} (t = {t:+.2f})\n")
    out.write("\n2. 경기도 31개 시군 분석:\n")
    for var in ['elderly_rate', 'disabled_rate', 'vulnerable_rate', 'fiscal_rate']:
        r, t = pearson_r(gg['low_floor_route_ratio'], gg[var])
        out.write(f" - 저상버스 운행노선비율 vs {var}: r = {r:+.3f} (t = {t:+.2f})\n")
    out.write(f"\n3. 회귀분석 결과:\n - 결정계수 R²: {r2:.4f}\n - 교통약자비율 Beta: {beta[1]:.2f}\n - 재정자립도 Beta: {beta[2]:.2f}\n")

print("\nReport saved to results/statistical_summary.txt")
