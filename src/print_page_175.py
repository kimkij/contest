with open("data/appendix_tables.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
for p in pages:
    if p.startswith("175 ") or p.startswith("176 ") or p.startswith("199 "):
        print("="*40)
        print("PAGE", p[:500])
