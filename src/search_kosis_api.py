import requests

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
url = "https://kosis.kr/openapi/statisticsSearch.do"

params = {
    "method": "getList",
    "apiKey": api_key,
    "format": "json",
    "jsonVD": "Y",
    "searchNm": "등록장애인"
}

res = requests.get(url, params=params, timeout=15)
print("Search Status:", res.status_code)
try:
    items = res.json()
    if isinstance(items, list):
        print(f"Found {len(items)} tables!")
        for item in items[:10]:
            print(f"orgId: {item.get('orgId')}, tblId: {item.get('tblId')}, tblNm: {item.get('tblNm')}")
    else:
        print("Response JSON:", items)
except Exception as e:
    print("Error parsing json:", e, res.text[:300])
