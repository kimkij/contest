import requests
from bs4 import BeautifulSoup
import re

url = "https://lofin365.go.kr/portal/bbs/bbsSelect.do"
params = {
    "bbsId": "BBSMSTR_000000000050", # typical board id or let's find
}
# Let's inspect lofin365 main or search page
res = requests.get("https://lofin365.go.kr", headers={"User-Agent": "Mozilla/5.0"})
print("lofin365 main status:", res.status_code)
