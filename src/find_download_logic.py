import requests
from bs4 import BeautifulSoup
import re

res = requests.get("https://www.data.go.kr/data/15106061/fileData.do")
soup = BeautifulSoup(res.text, "html.parser")
scripts = soup.find_all("script", src=True)
for s in scripts:
    src = s['src']
    if any(k in src.lower() for k in ['file', 'detail', 'data']):
        print("Script:", src)
        try:
            js_url = "https://www.data.go.kr" + src if src.startswith("/") else src
            js_res = requests.get(js_url, timeout=5)
            if "fn_fileDataDown" in js_res.text:
                print("FOUND in", src)
                match = re.search(r'fn_fileDataDown[^{]*\{.*?\n\}', js_res.text, re.DOTALL)
                if match:
                    print(match.group(0)[:600])
                else:
                    # print where it appears
                    idx = js_res.text.find("fn_fileDataDown")
                    print(js_res.text[idx:idx+500])
        except Exception as e:
            print("Error:", e)
