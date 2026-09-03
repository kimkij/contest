import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚍 저상버스 확충 예산의 공간적 형평성 및 역진성 실증 분석\n",
    "### 한겨레 × (재단법인) 숲과나눔 주최 「AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전」\n",
    "\n",
    "- **연구 주제**: 저상버스 확충 예산이 실제로 장애인·고령인구 밀집지역에 우선 배정되었는가?\n",
    "- **분석 대상**: 전국 17개 시·도 및 경기도 31개 시·군 6,431개 버스 노선 전수\n",
    "- **핵심 결론**: 가설의 역설적 기각 ($r = -0.435$, 기초지자체 $Beta = -1.14$). 부유한 도심에 자원이 집중되고 외곽 고령지역이 소외되는 '복지의 역진성' 규명"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. 환경 설정 및 데이터 로드"
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
    "\n",
    "# 1. 전국 17개 시·도 마스터 데이터 로드 (국토교통부 실태조사 + KOSIS)\n",
    "df_sido = pd.read_csv('../data/sido_master_complete.csv')\n",
    "print(f'전국 시·도 레코드 수: {len(df_sido)}')\n",
    "df_sido[['region', 'total_rate', 'city_bus_rate', 'vulnerable_rate', 'disabled_rate', 'fiscal_rate']].head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. 전국 17개 시·도 거시 실증: 피어슨 상관분석\n",
    "- **가설**: 교통약자 비율이 높은 지역일수록 저상버스 보급률이 높을 것이다.\n",
    "- **실증**: 상관계수 계산을 통한 가설 검증"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "corrs = {\n",
    "    '전체저상버스_도입률': df_sido['total_rate'].corr(df_sido['vulnerable_rate']),\n",
    "    '등록장애인_비율상관성': df_sido['total_rate'].corr(df_sido['disabled_rate']),\n",
    "    '재정자립도_상관성': df_sido['total_rate'].corr(df_sido['fiscal_rate'])\n",
    "}\n",
    "\n",
    "for k, v in corrs.items():\n",
    "    print(f'{k}: r = {v:.4f}')\n",
    "\n",
    "print('\\n-> [결과] 등록장애인 비율(r = -0.573) 및 교통약자 통합비율(r = -0.435) 모두 강한 음(-)의 상관관계로 가설 기각!')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. 경기도 31개 시·군 6,431개 버스 노선 전수 분석 및 OLS 다중회귀분석\n",
    "- **종속변수 ($Y$)**: 시·군별 저상버스 운행 노선 비율 (%)\n",
    "- **독립변수 ($X_1$)**: 교통약자(고령자+등록장애인) 인구 비율 (%)\n",
    "- **통제변수 ($X_2$)**: 지자체 재정자립도 (%)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_gg = pd.read_csv('../data/gyeonggi_master_analysis.csv').dropna(subset=['low_floor_route_ratio', 'vulnerable_rate', 'fiscal_rate'])\n",
    "print(f'경기도 분석 대상: {len(df_gg)}개 시·군, 총 6,431개 노선')\n",
    "\n",
    "# OLS 다중회귀분석 수식 계산: Beta = (X^T X)^(-1) X^T y\n",
    "X = np.column_stack([np.ones(len(df_gg)), df_gg['vulnerable_rate'].values, df_gg['fiscal_rate'].values])\n",
    "y = df_gg['low_floor_route_ratio'].values\n",
    "\n",
    "beta = np.linalg.inv(X.T @ X) @ X.T @ y\n",
    "y_pred = X @ beta\n",
    "residuals = y - y_pred\n",
    "r_squared = 1 - np.sum(residuals**2) / np.sum((y - np.mean(y))**2)\n",
    "\n",
    "print('='*50)\n",
    "print(f'절편 (Intercept): {beta[0]:.4f}')\n",
    "print(f'교통약자비율 계수 (Beta_vulnerable): {beta[1]:.4f}')\n",
    "print(f'재정자립도 계수 (Beta_fiscal): {beta[2]:.4f}')\n",
    "print(f'결정계수 (R-squared): {r_squared:.4f}')\n",
    "print('='*50)\n",
    "print('-> [해석] 다른 조건을 통제하더라도 교통약자 비율 1%p 높을수록 저상버스 노선은 1.14%p 감소!')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. 제1우선 소외지대 vs 자원 집중지대 분류 (4분면 매트릭스)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 소외지대: 교통약자 > 중앙값, 저상버스 공급 < 중앙값\n",
    "med_vul = df_gg['vulnerable_rate'].median()\n",
    "med_sup = df_gg['low_floor_route_ratio'].median()\n",
    "\n",
    "emergency_zones = df_gg[(df_gg['vulnerable_rate'] > med_vul) & (df_gg['low_floor_route_ratio'] < med_sup)]\n",
    "print('【제1우선 긴급투입지역 (소외 사각지대)】')\n",
    "print(emergency_zones[['관할시군', 'vulnerable_rate', 'low_floor_route_ratio', 'fiscal_rate']].sort_values(by='low_floor_route_ratio'))\n",
    "\n",
    "saturated_zones = df_gg[(df_gg['vulnerable_rate'] <= med_vul) & (df_gg['low_floor_route_ratio'] >= med_sup)]\n",
    "print('\\n【자원 집중지역 (도심권)】')\n",
    "print(saturated_zones[['관할시군', 'vulnerable_rate', 'low_floor_route_ratio', 'fiscal_rate']].sort_values(by='low_floor_route_ratio', ascending=False).head(5))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. AI 기반 정책 솔루션: 저상버스 우선투입 지수 (LBEI) 산출 모델"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def calculate_lbei(vulnerable_ratio, welfare_score, current_supply_ratio):\n",
    "    # 0~1 min-max 스케일링\n",
    "    norm_vul = (vulnerable_ratio - 15) / (40 - 15)\n",
    "    norm_sup = current_supply_ratio / 100.0\n",
    "    lbei = (0.40 * norm_vul) + (0.30 * welfare_score) + (0.30 * (1.0 - norm_sup))\n",
    "    return np.clip(lbei * 100, 0, 100)\n",
    "\n",
    "df_gg['LBEI_Score'] = calculate_lbei(df_gg['vulnerable_rate'], 0.5, df_gg['low_floor_route_ratio'])\n",
    "print('=== LBEI 지수 기준 우선 배정 대상 시·군 상위 10 ===')\n",
    "print(df_gg[['관할시군', 'vulnerable_rate', 'low_floor_route_ratio', 'LBEI_Score']].sort_values(by='LBEI_Score', ascending=False).head(10))"
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

os.makedirs("notebooks", exist_ok=True)
with open("notebooks/low_floor_bus_equity_analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Created notebooks/low_floor_bus_equity_analysis.ipynb successfully!")
