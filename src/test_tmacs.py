import requests
from bs4 import BeautifulSoup

url = "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/weak_report_list.do?mid=S3106"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

res = requests.get(url, headers=headers)
print("TMACS status:", res.status_code)
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")
for a in soup.find_all("a", href=True):
    txt = a.get_text(strip=True)
    if "실태조사" in txt or "보고서" in txt or "다운로드" in txt:
        print("Link:", a['href'], "Text:", txt)
