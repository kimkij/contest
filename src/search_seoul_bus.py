import requests
from bs4 import BeautifulSoup
import urllib.parse

# Search Seoul Open Data Plaza
url = "https://data.seoul.go.kr/dataList/datasetList.do"
params = {"keyword": "저상버스"}
res = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
print("Seoul data status:", res.status_code)
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")
for a in soup.find_all("a", href=True):
    txt = a.get_text(strip=True)
    if "저상버스" in txt and "/dataList/" in a['href']:
        print("Link:", a['href'], "Text:", txt)
