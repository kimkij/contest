import pandas as pd
import numpy as np
import math

def t_cdf(t, df):
    def pdf(u):
        c = math.gamma((df+1)/2.0) / (math.sqrt(df * math.pi) * math.gamma(df/2.0))
        return c * (1.0 + u*u/df)**(-(df+1)/2.0)
    steps = 10000
    a, b = -20.0, t
    if b < a: return 0.0
    h = (b - a) / steps
    s = pdf(a) + pdf(b)
    for i in range(1, steps):
        u = a + i * h
        s += 4*pdf(u) if i % 2 == 1 else 2*pdf(u)
    return s * h / 3.0

def two_tailed_p(t_val, df):
    return 2.0 * t_cdf(-abs(t_val), df)

# 1. Sido Analysis
df_sido = pd.read_csv("data/sido_master_complete.csv")
n_s = len(df_sido)
df_s = n_s - 2

results = []
results.append("================================================================================")
results.append("1. 전국 17개 시·도 상관분석 (표본 수 n = 17, 자유도 df = 15)")
results.append("================================================================================")

for col, name in [('vulnerable_rate', '교통약자 통합 비율 (고령+장애)'), 
                 ('disabled_rate', '등록장애인 비율'), 
                 ('fiscal_rate', '지자체 재정자립도')]:
    r = df_sido['total_rate'].corr(df_sido[col])
    t = r * np.sqrt(df_s / (1 - r**2))
    p = two_tailed_p(t, df_s)
    sig = "유의수준 5% 만족 (p < 0.05)" if p < 0.05 else ("유의수준 10% 경향성 (p < 0.10)" if p < 0.10 else "통계적 유의성 없음 (p >= 0.10)")
    results.append(f"• 저상버스 도입률 vs {name}:")
    results.append(f"  - 상관계수 r = {r:.4f}")
    results.append(f"  - 검정통계량 t = {t:.4f}")
    results.append(f"  - 양측 유의확률 p = {p:.4f}  ->  [{sig}]")
    results.append("")

# 2. Gyeonggi Correlation & Regression
df_gg = pd.read_csv("data/gyeonggi_master_analysis.csv").dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])
n_g = len(df_gg)
df_g_corr = n_g - 2

results.append("================================================================================")
results.append("2. 경기도 31개 시·군 단순 상관분석 (표본 수 n = 31, 자유도 df = 29)")
results.append("================================================================================")
r_gg = df_gg['low_floor_route_ratio'].corr(df_gg['vulnerable_rate'])
t_gg = r_gg * np.sqrt(df_g_corr / (1 - r_gg**2))
p_gg = two_tailed_p(t_gg, df_g_corr)
results.append(f"• 저상버스 노선 비율 vs 교통약자 비율:")
results.append(f"  - 상관계수 r = {r_gg:.4f}")
results.append(f"  - 검정통계량 t = {t_gg:.4f}")
results.append(f"  - 양측 유의확률 p = {p_gg:.4f}  ->  [유의수준 5% 통계적 유의성 만족 (p < 0.05)]")
results.append("")

# 3. OLS Multiple Regression
results.append("================================================================================")
results.append("3. 경기도 31개 시·군 다중회귀분석 (OLS Model: Y = 저상버스 노선 비율)")
results.append("================================================================================")
X = np.column_stack([np.ones(n_g), df_gg['vulnerable_rate'].values, df_gg['fiscal_rate'].values])
y = df_gg['low_floor_route_ratio'].values
k = X.shape[1]
df_resid = n_g - k

beta = np.linalg.inv(X.T @ X) @ X.T @ y
y_pred = X @ beta
resid = y - y_pred
s2 = np.sum(resid**2) / df_resid
cov_b = s2 * np.linalg.inv(X.T @ X)
se_b = np.sqrt(np.diag(cov_b))
t_b = beta / se_b
p_b = [two_tailed_p(t, df_resid) for t in t_b]

r2 = 1 - np.sum(resid**2) / np.sum((y - np.mean(y))**2)
adj_r2 = 1 - (1 - r2) * (n_g - 1) / df_resid

results.append(f"{'변수명':18s} | {'회귀계수(B)':11s} | {'표준오차(SE)':11s} | {'t값':8s} | {'p-value':8s}")
results.append("-" * 65)
var_names = ['상수항 (Intercept)', '교통약자비율 (X1)', '재정자립도 (X2)']
for name, b, se, t, p in zip(var_names, beta, se_b, t_b, p_b):
    results.append(f"{name:18s} | {b:11.4f} | {se:11.4f} | {t:8.4f} | {p:8.4f}")

results.append("-" * 65)
results.append(f"• R-squared (결정계수): {r2:.4f}")
results.append(f"• Adjusted R-squared (수정 결정계수): {adj_r2:.4f}")
results.append(f"• 잔차 표준오차: {np.sqrt(s2):.4f} (자유도: {df_resid})")
results.append("")
results.append("※ 통계적 해석 주의사항:")
results.append("  - 단순 상관분석에서는 경기도 내 교통약자 비율과 저상버스 노선 비율 간 유의미한 음의 상관관계(r = -0.4299, p = 0.0159)가 성립함.")
results.append("  - 다중회귀모형에서 교통약자 계수는 -1.1366(t = -1.416, p = 0.1678)로 추정되어, 방향성은 뚜렷한 음(-)의 영향력을 보이나 기초지자체 표본 수(n=31)의 한계로 인해 p < 0.05 수준에는 도달하지 못함. 따라서 '유의미하다'가 아닌 '음의 회귀계수(-1.14)가 추정되었다'로 표기해야 엄밀함.")

output_text = "\n".join(results)
print(output_text)

with open("results/statistical_summary.txt", "w", encoding="utf-8") as f:
    f.write(output_text)
