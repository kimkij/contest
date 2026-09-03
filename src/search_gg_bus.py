import requests
from bs4 import BeautifulSoup

url = "https://data.gg.go.kr/portal/data/service/selectServicePage.do"
params = {"searchWord": "저상버스"}
res = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
print("Status:", res.status_code)
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")
for a in soup.find_all("a", href=True):
    txt = a.get_text(strip=True)
    if "저상버스" in txt:
        print("Link:", a['href'], "Text:", txt)
