import requests
import re
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def download_dataset(pk, name):
    page_url = f"https://www.data.go.kr/data/{pk}/fileData.do"
    session = requests.Session()
    res = session.get(page_url, headers=headers, timeout=10)
    uddi_match = re.search(r'uddi:[a-f0-9\-]+', res.text)
    if not uddi_match:
        print(f"[{name}] UDDI not found")
        return False
    uddi = uddi_match.group(0)
    info_res = session.post(
        "https://www.data.go.kr/tcs/dss/selectFileDataDownload.do",
        data={
            "publicDataPk": pk,
            "publicDataDetailPk": uddi,
            "fileDetailSn": "1",
            "publicDataHistSn": "1",
            "publicDataTyCode": "PR0051"
        },
        headers={"User-Agent": "Mozilla/5.0", "Referer": page_url},
        timeout=10
    )
    info = info_res.json()
    atchFileId = info.get("atchFileId") or info.get("fileDataRegistVO", {}).get("atchFileId")
    fileDetailSn = info.get("fileDetailSn") or "1"
    dl_url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={atchFileId}&fileDetailSn={fileDetailSn}"
    
    # Try streaming download with retries
    for attempt in range(3):
        try:
            r = session.get(dl_url, headers={"User-Agent": "Mozilla/5.0", "Referer": page_url}, timeout=15, stream=True)
            if r.status_code == 200:
                with open(f"data/{name}.csv", "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"[{name}] Successfully saved ({r.status_code})")
                return True
        except Exception as e:
            print(f"[{name}] Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return False

download_dataset("15086332", "seoul_routes")
download_dataset("15113523", "gyeonggi_routes")
download_dataset("15045239", "incheon_routes")
