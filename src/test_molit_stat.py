import requests
from bs4 import BeautifulSoup
import re

url = "https://stat.molit.go.kr/portal/cate/statView.do?hRsId=334"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

for s in soup.find_all("script"):
    if s.string and "function download()" in s.string:
        print(s.string)
