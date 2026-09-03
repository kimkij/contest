import requests

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

params = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "orgId": "117",
    "tblId": "DT_117061_001",
    "prdSe": "Y",
    "startPrdDe": "2023",
    "endPrdDe": "2023",
    "itmId": "ALL",
    "objL1": "ALL"
}

res = requests.get(url, params=params, timeout=15)
print("Parameter Data Status:", res.status_code)
try:
    data = res.json()
    if isinstance(data, list):
        print(f"SUCCESS!! Received {len(data)} rows.")
        print("Sample row:", data[0])
    else:
        print("Response JSON:", data)
except Exception as e:
    print("Error parsing json:", e, res.text[:300])
