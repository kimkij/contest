import fitz  # PyMuPDF
import json
import re

doc = fitz.open("data/tmacs_report_29.pdf")
print("Total pages in tmacs_report_29:", len(doc))

target_pages = []
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    if "저상버스" in text and ("보급률" in text or "도입률" in text or "보급대수" in text):
        target_pages.append(page_num + 1)

print(f"Target pages found ({len(target_pages)}): {target_pages[:20]}")

# Inspect text of the first 5 target pages
with open("data/extracted_report_text.txt", "w", encoding="utf-8") as out:
    for p in target_pages:
        out.write(f"\n================ PAGE {p} ================\n")
        out.write(doc[p-1].get_text())

print("Saved target pages text to data/extracted_report_text.txt")
