import markdown
from fpdf import FPDF
import re
import os

# Let's generate a clean HTML presentation for printing or viewing as PDF
with open("results/contest_report.md", "r", encoding="utf-8") as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>AI와 함께하는 교통문제 해결 데이터 분석 공모전 보고서</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
        }}
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            line-height: 1.65;
            color: #2c3e50;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            background: #fff;
        }}
        h1 {{
            font-size: 20pt;
            color: #1a365d;
            border-bottom: 3px solid #2b6cb0;
            padding-bottom: 8px;
            margin-top: 10px;
            line-height: 1.3;
        }}
        h2 {{
            font-size: 15pt;
            color: #2b6cb0;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 5px;
            margin-top: 25px;
        }}
        h3 {{
            font-size: 12pt;
            color: #2d3748;
            margin-top: 20px;
            border-left: 4px solid #3182ce;
            padding-left: 8px;
        }}
        h4 {{
            font-size: 11pt;
            color: #4a5568;
            margin-top: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9.5pt;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 8px 10px;
            text-align: left;
        }}
        th {{
            background-color: #ebf8ff;
            color: #2b6cb0;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        ul, ol {{
            padding-left: 20px;
            font-size: 10pt;
        }}
        li {{
            margin-bottom: 6px;
        }}
        p {{
            font-size: 10pt;
            margin: 8px 0;
        }}
        .chart-box {{
            text-align: center;
            margin: 25px 0;
            page-break-inside: avoid;
        }}
        .chart-box img {{
            width: 98%;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .caption {{
            font-size: 9pt;
            color: #718096;
            margin-top: 6px;
            font-weight: bold;
        }}
        .summary-box {{
            background-color: #f0fff4;
            border: 1px solid #9ae6b4;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
        }}
        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
{html_body}

<div class="page-break"></div>
<h2>[시각화 1] 전국 및 경기도 실증 분석 산점도</h2>
<div class="chart-box">
    <img src="analysis_scatter_plot.png" alt="전국 및 경기도 통합 산점도">
    <div class="caption">&lt;그림 1&gt; 전국 17개 시도 및 경기도 31개 시군의 교통약자 비율 대비 저상버스 보급 현황</div>
</div>

<h2>[시각화 2] 전국 17개 시·도 도입률 및 취약계층 격차</h2>
<div class="chart-box">
    <img src="chart_sido_disparity.png" alt="전국 시도 격차">
    <div class="caption">&lt;그림 2&gt; 17개 광역 시도별 저상버스 도입률 (20% 미만 취약지역 집중 분석)</div>
</div>

<div class="page-break"></div>
<h2>[시각화 3] 경기도 31개 시·군 수요-공급 4분면 매트릭스</h2>
<div class="chart-box">
    <img src="chart_quadrant_matrix.png" alt="4분면 매트릭스">
    <div class="caption">&lt;그림 3&gt; 경기도 시군별 교통약자 수요 vs 공급 4분면 매트릭스 (긴급투입지대 vs 자원집중지대)</div>
</div>

</body>
</html>
"""

with open("results/contest_report.html", "w", encoding="utf-8") as out:
    out.write(html_template)

print("Saved beautiful report HTML to results/contest_report.html")
