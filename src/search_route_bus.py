import requests
from bs4 import BeautifulSoup
import re

# search data.go.kr for "노선별 저상버스"
url = "https://www.data.go.kr/tcs/dss/selectDataSetList.do"
params = {
    "keyword": "노선별 저상버스",
    "dataType": "FILE"
}
res = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")
for a in soup.find_all("a", href=True):
    if "/data/" in a['href'] and "fileData.do" in a['href']:
        print("Link:", a['href'], "Text:", a.get_text(strip=True))
