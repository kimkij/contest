import requests
import json

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.data.go.kr/data/15106061/fileData.do"
}

# step 1: get file info
step1_url = "https://www.data.go.kr/tcs/dss/selectFileDataDownload.do"
data = {
    "publicDataPk": "15106061",
    "publicDataDetailPk": "uddi:dd968e72-d1dc-48f1-94e4-a859dbf26958",
    "atchFileId": "",
    "fileDetailSn": "1",
    "publicDataHistSn": "4",
    "publicDataTyCode": "PR0051"
}
res1 = session.post(step1_url, data=data, headers=headers)
info = res1.json()
atchFileId = info.get("atchFileId") or info.get("fileDataRegistVO", {}).get("atchFileId")
fileDetailSn = info.get("fileDetailSn") or "1"
print(f"atchFileId: {atchFileId}, fileDetailSn: {fileDetailSn}")

# download url pattern in data.go.kr: /cmm/cmm/fileDownload.do?atchFileId=...&fileSn=...
dl_url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={atchFileId}&fileDetailSn={fileDetailSn}"
res2 = session.get(dl_url, headers=headers)
print("Download status:", res2.status_code, "Length:", len(res2.content))

if len(res2.content) > 100 and res2.status_code == 200:
    with open("data/low_floor_bus_raw.csv", "wb") as f:
        f.write(res2.content)
    print("Saved to data/low_floor_bus_raw.csv!")
    # preview
    try:
        text = res2.content.decode('cp949')
    except:
        text = res2.content.decode('utf-8', errors='ignore')
    print("Preview:\n", "\n".join(text.splitlines()[:15]))
else:
    print("Response text:", res2.text[:300])
