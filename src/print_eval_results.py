with open("data/appendix_tables.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
for p in pages:
    if p.startswith("204 ") or p.startswith("205 ") or p.startswith("206 ") or p.startswith("207 ") or p.startswith("208 "):
        print("="*40)
        print("PAGE", p[:800])
