import requests
import json
import pandas as pd

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

# TBL 1: DT_1YL202003E (등록장애인수 시도/시/군/구)
params = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "orgId": "101",
    "tblId": "DT_1YL202003E",
    "prdSe": "Y",
    "startPrdDe": "2023",
    "endPrdDe": "2023",
    "itmId": "ALL",
    "objL1": "ALL"
}

res = requests.get(url, params=params, timeout=15)
print("DT_1YL202003E Status:", res.status_code)
data = res.json()
if isinstance(data, list):
    print(f"SUCCESS! Retrieved {len(data)} records for DT_1YL202003E")
    df = pd.DataFrame(data)
    print("Columns:", list(df.columns))
    print(df[['C1_NM', 'ITM_NM', 'DT']].head(10))
    df.to_csv("data/kosis_disabled_sigungu_2023.csv", index=False, encoding="utf-8-sig")
    print("Saved data/kosis_disabled_sigungu_2023.csv")
else:
    print("Response:", data)
