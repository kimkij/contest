import os
import pymupdf
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

# Initialize presentation
prs = Presentation()

# Render PDF pages to high-res PNG (300 DPI for crisp presentation display)
pdf_path = "results/contest_report_final.pdf"
doc = pymupdf.open(pdf_path)

# A4 portrait dimensions in inches: 8.27 x 11.69
# Let's set slide dimensions exactly to A4 portrait
prs.slide_width = Inches(8.27)
prs.slide_height = Inches(11.69)
blank_slide_layout = prs.slide_layouts[6] # completely blank layout

print(f"Converting {len(doc)} pages into PPTX slides...")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=250)
    img_path = f"results/pptx_slide_{i}.png"
    pix.save(img_path)
    
    # Add slide
    slide = prs.slides.add_slide(blank_slide_layout)
    
    # Add high-res rendered image covering the entire slide
    slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

output_pptx = "results/contest_report_presentation.pptx"
prs.save(output_pptx)
print(f"Successfully generated presentation: {output_pptx}")
