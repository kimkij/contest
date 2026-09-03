import requests
import json

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.data.go.kr/data/15127852/fileData.do"
}

# find uddi from page
res = session.get("https://www.data.go.kr/data/15127852/fileData.do", headers=headers)
import re
uddi_match = re.search(r'uddi:[a-f0-9\-]+', res.text)
print("UDDI match:", uddi_match.group(0) if uddi_match else "None")

if uddi_match:
    uddi = uddi_match.group(0)
    data = {
        "publicDataPk": "15127852",
        "publicDataDetailPk": uddi,
        "atchFileId": "",
        "fileDetailSn": "1",
        "publicDataHistSn": "1",
        "publicDataTyCode": "PR0051"
    }
    r = session.post("https://www.data.go.kr/tcs/dss/selectFileDataDownload.do", data=data, headers=headers)
    info = r.json()
    atchFileId = info.get("atchFileId") or info.get("fileDataRegistVO", {}).get("atchFileId")
    fileDetailSn = info.get("fileDetailSn") or "1"
    dl_url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={atchFileId}&fileDetailSn={fileDetailSn}"
    res_dl = session.get(dl_url, headers=headers)
    print("Download length:", len(res_dl.content))
    with open("data/mohw_disabled_raw.csv", "wb") as f:
        f.write(res_dl.content)
    # read preview
    try:
        lines = res_dl.content.decode('cp949').splitlines()
    except:
        lines = res_dl.content.decode('utf-8', errors='ignore').splitlines()
    for l in lines[:15]:
        print(l)
