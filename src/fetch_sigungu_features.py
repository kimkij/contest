import requests
import json
import pandas as pd

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

# 1. Fetch 고령인구비율 (DT_1YL20631)
print("Fetching Elderly ratio (DT_1YL20631)...")
p_elderly = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "orgId": "101",
    "tblId": "DT_1YL20631",
    "prdSe": "Y",
    "startPrdDe": "2023",
    "endPrdDe": "2023",
    "itmId": "ALL",
    "objL1": "ALL"
}
r1 = requests.get(url, params=p_elderly, timeout=15)
df_elderly = pd.DataFrame(r1.json())
print(f"Elderly records: {len(df_elderly)}")
df_elderly.to_csv("data/kosis_elderly_sigungu_2023.csv", index=False, encoding="utf-8-sig")

# 2. Fetch 재정자립도 (DT_1YL20921)
print("Fetching Fiscal independence (DT_1YL20921)...")
p_fiscal = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "orgId": "101",
    "tblId": "DT_1YL20921",
    "prdSe": "Y",
    "startPrdDe": "2023",
    "endPrdDe": "2023",
    "itmId": "ALL",
    "objL1": "ALL"
}
r2 = requests.get(url, params=p_fiscal, timeout=15)
df_fiscal = pd.DataFrame(r2.json())
print(f"Fiscal records: {len(df_fiscal)}")
df_fiscal.to_csv("data/kosis_fiscal_sigungu_2023.csv", index=False, encoding="utf-8-sig")

print("Successfully saved both datasets to data/!")
