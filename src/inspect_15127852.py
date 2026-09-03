import requests
from bs4 import BeautifulSoup

url = "https://www.data.go.kr/data/15127852/fileData.do"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', errors='ignore'), "html.parser")
title = soup.find("h3", class_="title") or soup.find("title")
print("Title:", title.get_text(strip=True) if title else "")

# look for description
desc = soup.find("div", class_="desc") or soup.find("p", class_="desc")
print("Desc:", desc.get_text(strip=True)[:200] if desc else "")
