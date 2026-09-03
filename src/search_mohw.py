import requests
from bs4 import BeautifulSoup
import re

url = "https://www.mohw.go.kr/board.es?mid=a10411010100&bid=0019&act=view&list_no=1481190" # sample board
# Let's search mohw board
search_url = "https://www.mohw.go.kr/board.es"
params = {
    "mid": "a10411010100",
    "bid": "0019",
    "act": "list",
    "keyField": "title",
    "keyWord": "등록장애인 현황"
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(search_url, params=params, headers=headers)
print("MOHW search status:", res.status_code)
soup = BeautifulSoup(res.text, "html.parser")
for a in soup.find_all("a", href=True):
    if "list_no" in a['href']:
        print(a.get_text(strip=True), a['href'])
