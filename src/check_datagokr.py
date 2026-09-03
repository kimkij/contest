import requests
from bs4 import BeautifulSoup
import re

url = "https://www.data.go.kr/data/15106061/fileData.do"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

res = requests.get(url, headers=headers)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")
print("Title:", soup.title.string.strip() if soup.title else "")

for btn in soup.find_all(["a", "button"]):
    onclick = btn.get("onclick", "")
    href = btn.get("href", "")
    text = btn.get_text(strip=True)
    if "다운로드" in text or "down" in onclick.lower() or "download" in href.lower():
        print(f"Tag: {btn.name} | Text: {text} | href: {href} | onclick: {onclick}")
