import requests
from bs4 import BeautifulSoup
import re

url = "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/weak_report_list.do?mid=S3106"
res = requests.get(url)
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")

# look for rows in the table
rows = soup.find_all("tr")
for r in rows:
    tds = r.find_all(["td", "th"])
    row_text = [td.get_text(strip=True) for td in tds]
    links = r.find_all("a", href=True)
    onclicks = [a.get("onclick", "") or a.get("href", "") for a in links]
    if any("보고서" in t or "20" in t for t in row_text):
        print("Row:", " | ".join(row_text[:4]))
        print("Actions:", onclicks)
