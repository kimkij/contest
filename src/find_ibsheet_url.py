import requests
from bs4 import BeautifulSoup
import re

url = "https://stat.molit.go.kr/portal/cate/statView.do?hRsId=334"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

for s in soup.find_all("script"):
    if s.string and "sheet01.DoSearch" in s.string or (s.string and "DoSearch" in s.string):
        for line in s.string.splitlines():
            if "DoSearch" in line or "url" in line.lower() or "action" in line.lower():
                print(line.strip()[:150])
