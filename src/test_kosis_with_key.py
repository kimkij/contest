import requests

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/statisticsData.do"

# Let's check required parameters for statisticsData.do
# Typically: method=getList, apiKey, format=json, jsonVD=Y, userStatsId=... OR orgId, tblId, prdSe, startPrdDe, endPrdDe, itmId, objL1, etc.
# If user didn't register MyData, userStatsId is not used.
# Let's test standard parameters:
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
    "objL1": "ALL",
    "objL2": "ALL"
}

res = requests.get(url, params=params, timeout=15)
print("Status:", res.status_code)
print("Response text:", res.text[:300])
