import requests
import json

api_key = "N2ZlMmQxNzJlNTc0MDcyNzI0NTA1ZjhiM2Y3NTA5Nzc="
search_url = "https://kosis.kr/openapi/statisticsSearch.do"

def search_kosis(query):
    params = {
        "method": "getList",
        "apiKey": api_key,
        "format": "json",
        "jsonVD": "Y",
        "searchNm": query
    }
    r = requests.get(search_url, params=params)
    try:
        return r.json()
    except:
        print("Raw text:", r.text[:200])
        return []

print("Searching '고령인구비율'...")
e_res = search_kosis("고령인구비율")
for it in e_res[:5]:
    print(f"ORG: {it.get('ORG_ID')}, TBL: {it.get('TBL_ID')}, Name: {it.get('TBL_NM')}")

print("\nSearching '재정자립도'...")
f_res = search_kosis("재정자립도")
for it in f_res[:5]:
    print(f"ORG: {it.get('ORG_ID')}, TBL: {it.get('TBL_ID')}, Name: {it.get('TBL_NM')}")
