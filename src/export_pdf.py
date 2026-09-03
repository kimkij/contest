from playwright.sync_api import sync_playwright
import os

# Render markdown into HTML without external markdown library
with open("results/contest_report.md", "r", encoding="utf-8") as f:
    text = f.read()

# Simple markdown to html converter for our clean text
html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>AI와 함께하는 교통문제 해결 데이터 분석 공모전 보고서</title>
    <style>
        @page {
            size: A4;
            margin: 18mm 15mm 18mm 15mm;
        }
        body {
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            max-width: 850px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            font-size: 10pt;
        }
        h1 { font-size: 17pt; color: #1a365d; border-bottom: 2.5px solid #2b6cb0; padding-bottom: 6px; margin-top: 10px; }
        h2 { font-size: 13pt; color: #2b6cb0; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin-top: 22px; }
        h3 { font-size: 11pt; color: #2d3748; margin-top: 16px; border-left: 3.5px solid #3182ce; padding-left: 7px; }
        h4 { font-size: 10pt; color: #4a5568; margin-top: 12px; }
        table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 8.8pt; }
        th, td { border: 1px solid #cbd5e0; padding: 6px 8px; text-align: left; }
        th { background-color: #ebf8ff; color: #2b6cb0; font-weight: bold; }
        tr:nth-child(even) { background-color: #f7fafc; }
        ul, ol { padding-left: 18px; margin: 6px 0; }
        li { margin-bottom: 4px; }
        p { margin: 6px 0; text-align: justify; }
        .chart-box { text-align: center; margin: 18px 0; page-break-inside: avoid; }
        .chart-box img { width: 95%; border: 1px solid #e2e8f0; border-radius: 4px; }
        .caption { font-size: 8.5pt; color: #718096; margin-top: 4px; font-weight: bold; }
        .summary-box { background-color: #f8fafc; border: 1px solid #cbd5e0; border-left: 4px solid #3182ce; border-radius: 4px; padding: 12px; margin: 15px 0; }
        .page-break { page-break-after: always; }
        strong { color: #1a202c; }
    </style>
</head>
<body>
"""

# Simple parser
lines = text.splitlines()
in_table = False
table_rows = []

for line in lines:
    line_s = line.strip()
    if not line_s:
        if in_table:
            html_content += "<table>\n"
            for i, r in enumerate(table_rows):
                cols = [c.strip() for c in r.split("|")[1:-1]]
                tag = "th" if i == 0 else "td"
                html_content += "  <tr>" + "".join([f"<{tag}>{c}</{tag}>" for c in cols]) + "</tr>\n"
            html_content += "</table>\n"
            in_table = False
            table_rows = []
        continue
    
    if line_s.startswith("|") and line_s.endswith("|"):
        if "---" in line_s:
            continue
        in_table = True
        table_rows.append(line_s)
        continue
        
    if in_table:
        html_content += "<table>\n"
        for i, r in enumerate(table_rows):
            cols = [c.strip() for c in r.split("|")[1:-1]]
            tag = "th" if i == 0 else "td"
            html_content += "  <tr>" + "".join([f"<{tag}>{c}</{tag}>" for c in cols]) + "</tr>\n"
        html_content += "</table>\n"
        in_table = False
        table_rows = []
        
    if line_s.startswith("# "):
        html_content += f"<h1>{line_s[2:]}</h1>\n"
    elif line_s.startswith("## "):
        html_content += f"<h2>{line_s[3:]}</h2>\n"
    elif line_s.startswith("### "):
        html_content += f"<h3>{line_s[4:]}</h3>\n"
    elif line_s.startswith("#### "):
        html_content += f"<h4>{line_s[5:]}</h4>\n"
    elif line_s.startswith("* ") or line_s.startswith("- "):
        html_content += f"<ul><li>{line_s[2:]}</li></ul>\n"
    elif line_s.startswith("1. ") or line_s.startswith("2. ") or line_s.startswith("3. "):
        html_content += f"<ol><li>{line_s[3:]}</li></ol>\n"
    elif line_s.startswith("---"):
        html_content += "<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;'>\n"
    else:
        # replace markdown bold
        p_text = line_s
        import re
        p_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p_text)
        p_text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', p_text)
        html_content += f"<p>{p_text}</p>\n"

# Add embedded charts at the end
html_content += """
<div class="page-break"></div>
<h2>[시각화 1] 전국 및 경기도 실증 분석 산점도 및 추세선</h2>
<div class="chart-box">
    <img src="analysis_scatter_plot.png">
    <div class="caption">&lt;그림 1&gt; 전국 17개 시도 및 경기도 31개 시군의 교통약자 비율 대비 저상버스 보급 현황 (역진적 배정 실증)</div>
</div>

<h2>[시각화 2] 전국 17개 시·도 도입률 및 취약계층 격차</h2>
<div class="chart-box">
    <img src="chart_sido_disparity.png">
    <div class="caption">&lt;그림 2&gt; 17개 광역 시도별 저상버스 도입률 (20% 미만 취약지역 집중 분석)</div>
</div>

<div class="page-break"></div>
<h2>[시각화 3] 경기도 31개 시·군 수요-공급 4분면 매트릭스</h2>
<div class="chart-box">
    <img src="chart_quadrant_matrix.png">
    <div class="caption">&lt;그림 3&gt; 경기도 시군별 교통약자 수요 vs 공급 4분면 매트릭스 (제1우선 소외지대 vs 자원집중지대 도출)</div>
</div>

</body>
</html>
"""

with open("results/contest_report.html", "w", encoding="utf-8") as out:
    out.write(html_content)

print("HTML saved, converting to PDF via Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///" + os.path.abspath("results/contest_report.html").replace("\\", "/"))
    page.pdf(
        path="results/저상버스_교통약자_배정형평성_분석보고서.pdf",
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
    )
    browser.close()

print("SUCCESS: Generated results/저상버스_교통약자_배정형평성_분석보고서.pdf")
