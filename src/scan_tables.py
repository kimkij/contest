import re

with open("data/appendix_tables.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
print("Total split pages:", len(pages))

for p in pages[1:]:
    header = p.split("\n")[0]
    p_num = header.split(" ")[0]
    # search for table titles
    titles = re.findall(r'\[표\s*[^\]]+\]\s*[^\n]+', p)
    if titles:
        print(f"Page {p_num}:", titles)
