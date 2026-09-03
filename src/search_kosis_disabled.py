import requests
import json

# Let's search KOSIS OpenAPI or stat.kosis.kr for disabled population by sigungu
# Table ID for disabled population in KOSIS: typically 'DT_1BM13' or 'DT_1F01' or 'DT_13801_...
# Let's search using KOSIS search or direct scraping of KOSIS table list
url = "https://kosis.kr/statHtml/statHtml.do"
# Or search via SGIS / KOSIS search api
search_url = "https://kosis.kr/search/search.do"
params = {"query": "시군구별 등록장애인수"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

res = requests.get(search_url, params=params, headers=headers)
print("Search status:", res.status_code)
from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text, "html.parser")
for a in soup.find_all("a", href=True):
    if "statHtml" in a['href'] or "tblId" in a['href']:
        print(a.get_text(strip=True)[:50], a['href'])
