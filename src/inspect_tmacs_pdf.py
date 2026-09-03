import pypdf
import sys

def check_pdf(pdf_path):
    print(f"\n--- Checking {pdf_path} ---")
    reader = pypdf.PdfReader(pdf_path)
    print("Num pages:", len(reader.pages))
    
    # search for "저상버스" or "시·군·구" or "도입률"
    matches = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if "저상버스" in text and ("시·군" in text or "시군구" in text or "보급률" in text):
            matches.append((i+1, [line.strip() for line in text.splitlines() if "저상버스" in line][:2]))
    print(f"Pages with low-floor bus and sigungu: {len(matches)}")
    for p_num, lines in matches[:8]:
        print(f"Page {p_num}: {lines}")

check_pdf("data/tmacs_report_30.pdf")
check_pdf("data/tmacs_report_29.pdf")
