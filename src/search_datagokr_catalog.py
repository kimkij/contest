import requests
from bs4 import BeautifulSoup
import urllib.parse

# Search data.go.kr for "등록장애인"
url = "https://www.data.go.kr/tcs/dss/selectDataSetList.do"
params = {
    "keyword": "등록장애인",
    "bcyclGbn": "",
    "searchCondition": "title",
    "dataType": "FILE"
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

res = requests.get(url, params=params, headers=headers)
print("Status:", res.status_code)
soup = BeautifulSoup(res.text, "html.parser")
items = soup.find_all("span", class_="title")
for item in items[:10]:
    print("Found title:", item.get_text(strip=True))

# find links
for a in soup.find_all("a", href=True):
    if "/data/" in a['href'] and "fileData.do" in a['href']:
        title = a.get_text(strip=True)
        if title:
            print("Link:", a['href'], "Text:", title)
