import requests

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.data.go.kr/data/15106061/fileData.do",
    "Origin": "https://www.data.go.kr",
    "X-Requested-With": "XMLHttpRequest"
}

# 1. visit page to get session cookies
res = session.get("https://www.data.go.kr/data/15106061/fileData.do", headers=headers)
print("Page visit status:", res.status_code)

# 2. call /tcs/dss/selectFileDataDownload.do
# onclick was: fileDetailObj.fn_fileDataDown('15106061', 'uddi:dd968e72-d1dc-48f1-94e4-a859dbf26958', '','1', '4')
data = {
    "publicDataPk": "15106061",
    "publicDataDetailPk": "uddi:dd968e72-d1dc-48f1-94e4-a859dbf26958",
    "atchFileId": "",
    "fileDetailSn": "1",
    "publicDataHistSn": "4",
    "publicDataTyCode": "PR0051"
}

res2 = session.post("https://www.data.go.kr/tcs/dss/selectFileDataDownload.do", data=data, headers=headers)
print("Download check status:", res2.status_code)
print("Download check response:", res2.text)
