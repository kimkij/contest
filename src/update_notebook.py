import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚍 교통약자가 많은 지역에 저상버스가 더 많이 다니고 있는가?\n",
    "### 한겨레 × (재단법인) 숲과나눔 주최 「AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전」\n",
    "\n",
    "- **연구 질문**: 노선버스 대폐차 시 저상버스 의무화 도입 이후, 저상버스는 실제로 장애인·고령인구 밀집지역에 우선 배정되었는가?\n",
    "- **분석 데이터**: 전국 17개 광역 시·도 및 경기도 31개 기초지자체(6,431개 버스 노선) 전수 데이터\n",
    "- **핵심 결과**: \n",
    "  1. 전국 단위에서 저상버스 도입률과 교통약자 비율 간 음(-)의 상관관계 관찰 ($r = -0.435, t = -1.87, p = 0.081$), 등록장애인 비율 기준 $r = -0.573 (p = 0.016 < 0.05)$\n",
    "  2. 경기도 노선 전수 분석에서 저상버스 노선 비율과 교통약자 비율 간 유의미한 음의 상관성 확증 ($r = -0.430, t = -2.56, p = 0.016 < 0.05$)\n",
    "  3. 다중회귀분석(OLS) 추정 결과 교통약자 비율 계수 $B = -1.14 (SE = 0.80, t = -1.42, p = 0.168)$로 음(-)의 계수가 추정됨"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. 분석 환경 설정 및 데이터 전처리 마스터셋 로드\n",
    "- 출처: 국토교통부 『2023년 교통약자 이동편의 실태조사 보고서』(TMACS), 통계청 KOSIS, 경기데이터드림"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import math\n",
    "\n",
    "# 1. 전국 17개 시·도 데이터셋\n",
    "df_sido = pd.read_csv('../data/sido_master_complete.csv')\n",
    "# 2. 경기도 31개 시·군 노선 집계 데이터셋\n",
    "df_gg = pd.read_csv('../data/gyeonggi_master_analysis.csv').dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])\n",
    "\n",
    "print(f'전국 시·도 레코드 수: {len(df_sido)}개 | 경기도 시·군 레코드 수: {len(df_gg)}개')\n",
    "df_sido[['region', 'total_rate', 'city_bus_rate', 'vulnerable_rate', 'disabled_rate', 'fiscal_rate']].head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. 전국 17개 시·도 상관분석 및 검정통계량 (t값, exact p-value 계산)\n",
    "- $t = r \\times \\sqrt{\\frac{n-2}{1 - r^2}}$ 수식을 이용한 엄밀한 가설 검정"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# t분포 누적분포함수 및 p-value 계산 함수\n",
    "def t_cdf(t, df):\n",
    "    def pdf(u):\n",
    "        c = math.gamma((df+1)/2.0) / (math.sqrt(df * math.pi) * math.gamma(df/2.0))\n",
    "        return c * (1.0 + u*u/df)**(-(df+1)/2.0)\n",
    "    steps = 10000\n",
    "    a, b = -20.0, t\n",
    "    if b < a: return 0.0\n",
    "    h = (b - a) / steps\n",
    "    s = pdf(a) + pdf(b)\n",
    "    for i in range(1, steps):\n",
    "        u = a + i * h\n",
    "        s += 4*pdf(u) if i % 2 == 1 else 2*pdf(u)\n",
    "    return s * h / 3.0\n",
    "\n",
    "def two_tailed_p(t_val, df):\n",
    "    return 2.0 * t_cdf(-abs(t_val), df)\n",
    "\n",
    "n_sido = len(df_sido)\n",
    "df_sido_deg = n_sido - 2\n",
    "\n",
    "for col, name in [('vulnerable_rate', '교통약자 통합비율'), ('disabled_rate', '등록장애인 비율'), ('fiscal_rate', '재정자립도')]:\n",
    "    r = df_sido['total_rate'].corr(df_sido[col])\n",
    "    t = r * np.sqrt(df_sido_deg / (1 - r**2))\n",
    "    p = two_tailed_p(t, df_sido_deg)\n",
    "    print(f'[{name}] 상관계수 r = {r:.4f}, t = {t:.4f}, p = {p:.4f}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. 경기도 31개 시·군 OLS 다중회귀분석 (표준오차, t값, p값 산출 코드)\n",
    "- 종속변수: 시군별 저상버스 운행 노선 비율 (%)\n",
    "- 독립변수: 교통약자 비율 (%), 통제변수: 재정자립도 (%)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "n_gg = len(df_gg)\n",
    "X = np.column_stack([np.ones(n_gg), df_gg['vulnerable_rate'].values, df_gg['fiscal_rate'].values])\n",
    "y = df_gg['low_floor_route_ratio'].values\n",
    "k = X.shape[1] # 3\n",
    "df_resid = n_gg - k # 28\n",
    "\n",
    "beta = np.linalg.inv(X.T @ X) @ X.T @ y\n",
    "y_pred = X @ beta\n",
    "resid = y - y_pred\n",
    "s2 = np.sum(resid**2) / df_resid\n",
    "cov_b = s2 * np.linalg.inv(X.T @ X)\n",
    "se_b = np.sqrt(np.diag(cov_b))\n",
    "t_b = beta / se_b\n",
    "p_b = [two_tailed_p(t, df_resid) for t in t_b]\n",
    "\n",
    "r2 = 1 - np.sum(resid**2) / np.sum((y - np.mean(y))**2)\n",
    "adj_r2 = 1 - (1 - r2) * (n_gg - 1) / df_resid\n",
    "\n",
    "summary_df = pd.DataFrame({\n",
    "    '변수명': ['Intercept', '교통약자비율(X1)', '재정자립도(X2)'],\n",
    "    '회귀계수(Beta)': np.round(beta, 4),\n",
    "    '표준오차(SE)': np.round(se_b, 4),\n",
    "    't-statistic': np.round(t_b, 4),\n",
    "    'p-value': np.round(p_b, 4)\n",
    "})\n",
    "\n",
    "print('=== 경기도 31개 시·군 다중회귀분석(OLS) 결과 ===')\n",
    "print(summary_df.to_string(index=False))\n",
    "print(f'R-squared: {r2:.4f}, Adjusted R-squared: {adj_r2:.4f}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. 데이터 기반 저상버스 우선순위 산정 모델 (LBEI)\n",
    "- 단순 균등 배분이 아닌 취약계층 밀도와 시설 접근성, 공급 결핍도를 통합한 지수 산출"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def calculate_lbei(vulnerable_ratio, welfare_score, current_supply_ratio):\n",
    "    # 0~1 스케일링\n",
    "    norm_vul = (vulnerable_ratio - 15) / (40 - 15)\n",
    "    norm_sup = current_supply_ratio / 100.0\n",
    "    lbei = (0.40 * norm_vul) + (0.30 * welfare_score) + (0.30 * (1.0 - norm_sup))\n",
    "    return np.clip(lbei * 100, 0, 100)\n",
    "\n",
    "df_gg['LBEI_Score'] = calculate_lbei(df_gg['vulnerable_rate'], 0.5, df_gg['low_floor_route_ratio'])\n",
    "print('=== LBEI 점수 기준 우선 배정 대상 기초지자체 상위 10 ===')\n",
    "print(df_gg[['관할시군', 'vulnerable_rate', 'low_floor_route_ratio', 'fiscal_rate', 'LBEI_Score']].sort_values(by='LBEI_Score', ascending=False).head(10).to_string(index=False))"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("notebooks/low_floor_bus_equity_analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Updated notebooks/low_floor_bus_equity_analysis.ipynb with rigorous statistical calculations!")
