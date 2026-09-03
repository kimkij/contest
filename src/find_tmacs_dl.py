import requests
from bs4 import BeautifulSoup
import re

url = "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/weak_report_list.do?mid=S3106"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
for s in soup.find_all("script"):
    if s.string and "reportDownload" in s.string:
        print("Found script:\n", s.string)
