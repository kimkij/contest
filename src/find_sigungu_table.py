import requests

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/statisticsSearch.do"

params = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "searchNm": "시군구 등록장애인"
}

res = requests.get(url, params=params, timeout=15)
items = res.json()
print("Search count:", len(items))
for it in items:
    print(f"ORG: {it.get('ORG_ID')}, TBL: {it.get('TBL_ID')}, Name: {it.get('TBL_NM')}")
