import requests

url = "https://openapi.gg.go.kr/BusLwflBusM"
params = {
    "Type": "json",
    "pIndex": 1,
    "pSize": 5
}
try:
    res = requests.get(url, params=params, timeout=5)
    print("Gyeonggi openapi status:", res.status_code)
    print("Response snippet:", res.text[:300])
except Exception as e:
    print("Error:", e)
