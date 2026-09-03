import pymupdf
import re

doc = pymupdf.open("data/tmacs_report_29.pdf")
print(f"Total pages: {len(doc)}")

# Let's search pages 170 to 228
with open("data/appendix_tables.txt", "w", encoding="utf-8") as out:
    for p_num in range(170, len(doc)):
        text = doc[p_num].get_text()
        out.write(f"\n--- PAGE {p_num+1} ---\n")
        out.write(text)

print("Saved pages 171-228 to data/appendix_tables.txt")
