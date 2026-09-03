import requests
import sys

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/weak_report_list.do?mid=S3106"
}

# Download file 30 (2023 실태조사)
res = session.post(
    "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/reportDownload.do",
    data={"fileNum": "30"},
    headers=headers
)

if res.status_code == 200 and len(res.content) > 1000:
    filename = "data/tmacs_report_30.pdf"
    with open(filename, "wb") as f:
        f.write(res.content)
    print(f"Successfully saved {filename}, size: {len(res.content)} bytes")

# Download file 29 (2023 실태조사 종합보고서)
res2 = session.post(
    "https://tmacs.kotsa.or.kr/web/TraffickingWeak/psd/reportDownload.do",
    data={"fileNum": "29"},
    headers=headers
)
if res2.status_code == 200 and len(res2.content) > 1000:
    filename2 = "data/tmacs_report_29.pdf"
    with open(filename2, "wb") as f:
        f.write(res2.content)
    print(f"Successfully saved {filename2}, size: {len(res2.content)} bytes")
