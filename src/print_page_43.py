with open("data/extracted_report_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("================ PAGE ")
for p in pages:
    if p.startswith("43\n") or p.startswith("43 "):
        print("PAGE 43:\n", p[:1200])
    if p.startswith("15\n") or p.startswith("15 "):
        print("PAGE 15:\n", p[:1200])
