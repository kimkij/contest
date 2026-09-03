import requests
import json
import pandas as pd

# Test KOSIS open API without key or search endpoint
url = "https://kosis.kr/openapi/statisticsData.do"
params = {
    "method": "getList",
    "apiKey": "test",
    "format": "json"
}
try:
    res = requests.get(url, params=params, timeout=5)
    print("KOSIS response code:", res.status_code)
    print("KOSIS snippet:", res.text[:200])
except Exception as e:
    print("Error:", e)
