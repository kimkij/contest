import requests
import re
import json

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0"}

datasets = [
    {"name": "seoul_routes", "pk": "15086332"},
    {"name": "gyeonggi_routes", "pk": "15113523"},
    {"name": "incheon_routes", "pk": "15045239"}
]

for d in datasets:
    page_url = f"https://www.data.go.kr/data/{d['pk']}/fileData.do"
    res = session.get(page_url, headers=headers)
    uddi_match = re.search(r'uddi:[a-f0-9\-]+', res.text)
    if uddi_match:
        uddi = uddi_match.group(0)
        # get file info
        info_res = session.post(
            "https://www.data.go.kr/tcs/dss/selectFileDataDownload.do",
            data={
                "publicDataPk": d['pk'],
                "publicDataDetailPk": uddi,
                "fileDetailSn": "1",
                "publicDataHistSn": "1",
                "publicDataTyCode": "PR0051"
            },
            headers={"User-Agent": "Mozilla/5.0", "Referer": page_url}
        )
        info = info_res.json()
        atchFileId = info.get("atchFileId") or info.get("fileDataRegistVO", {}).get("atchFileId")
        fileDetailSn = info.get("fileDetailSn") or "1"
        dl_url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={atchFileId}&fileDetailSn={fileDetailSn}"
        dl_res = session.get(dl_url, headers={"User-Agent": "Mozilla/5.0", "Referer": page_url})
        out_name = f"data/{d['name']}.csv"
        with open(out_name, "wb") as f:
            f.write(dl_res.content)
        print(f"Downloaded {d['name']}: {len(dl_res.content)} bytes -> {out_name}")
