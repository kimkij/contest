# -*- coding: utf-8 -*-
"""
Ensure gen_editable_docx.py strictly sets A4 portrait dimensions (210mm x 297mm)
with clean margins, typography, and tables matching contest_report_final.pdf.
"""
import os
import docx
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="cbd5e1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_docx():
    doc = docx.Document()

    # Set strict A4 Portrait: 210mm x 297mm
    sections = doc.sections
    for section in sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(15)
        section.bottom_margin = Mm(15)
        section.left_margin = Mm(18)
        section.right_margin = Mm(18)

    # Style definitions
    style_normal = doc.styles['Normal']
    style_normal.font.name = '맑은 고딕'
    style_normal.font.size = Pt(9.2)
    style_normal.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    style_normal.paragraph_format.line_spacing = 1.35
    style_normal.paragraph_format.space_after = Pt(4)

    # ==========================================
    # COVER PAGE
    # ==========================================
    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_before = Pt(50)
    p_tag.paragraph_format.space_after = Pt(25)
    r_tag = p_tag.add_run("한겨레 × (재단법인) 숲과나눔 「AI와 함께하는 교통문제 해결 데이터 분석 공모전」 제출작")
    r_tag.font.bold = True
    r_tag.font.size = Pt(10.5)
    r_tag.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(18)
    r_t1 = p_title.add_run("교통약자가 많은 지역에\n")
    r_t1.font.bold = True
    r_t1.font.size = Pt(25)
    r_t1.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    r_t2 = p_title.add_run("저상버스가 더 많이 다니고 있는가?")
    r_t2.font.bold = True
    r_t2.font.size = Pt(25)
    r_t2.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub = p_sub.add_run("전국 17개 시·도 및 경기도 31개 시·군 6,431개 버스 노선 전수 분석을 통해 본\n저상버스 도입의 공간적 역진성(Regressive Allocation)과 정책 개선 방안")
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    r_sub.font.bold = True

    # Metadata box table
    tbl_meta = doc.add_table(rows=5, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_meta, color="cbd5e1")
    meta_data = [
        ("보고서 핵심 메타데이터 & 접속 채널", ""),
        ("분석 기준연도", "2023년 (국토교통부 실태조사 공인 확정 통계)"),
        ("전수 분석 대상", "전국 17개 시·도 및 경기도 31개 시·군 6,431개 버스 노선"),
        ("온라인 웹 보고서", "https://contest-lab.github.io/contest/"),
        ("GitHub 소스코드", "https://github.com/contest-lab/contest")
    ]
    for row_idx, (col1, col2) in enumerate(meta_data):
        row = tbl_meta.rows[row_idx]
        if row_idx == 0:
            a, b = row.cells[0], row.cells[1]
            a.merge(b)
            p = a.paragraphs[0]
            r = p.add_run(col1)
            r.font.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
            set_cell_background(a, "f1f5f9")
            set_cell_margins(a, top=130, bottom=130, left=180, right=180)
        else:
            c1, c2 = row.cells[0], row.cells[1]
            c1.width = Mm(50)
            c2.width = Mm(110)
            set_cell_background(c1, "f8fafc")
            set_cell_margins(c1, top=90, bottom=90, left=140, right=140)
            set_cell_margins(c2, top=90, bottom=90, left=140, right=140)
            p1 = c1.paragraphs[0]
            r1 = p1.add_run(col1)
            r1.font.bold = True
            r1.font.size = Pt(9.0)
            r1.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
            p2 = c2.paragraphs[0]
            r2 = p2.add_run(col2)
            r2.font.size = Pt(9.0)
            if "http" in col2:
                r2.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
                r2.font.bold = True
            else:
                r2.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_before = Pt(55)
    r_a1 = p_author.add_run("제출자: ")
    r_a1.font.bold = True
    r_a1.font.size = Pt(10.5)
    r_a2 = p_author.add_run("김일중\n")
    r_a2.font.bold = True
    r_a2.font.size = Pt(10.5)
    r_a3 = p_author.add_run("제출일자: ")
    r_a3.font.bold = True
    r_a3.font.size = Pt(10.0)
    r_a4 = p_author.add_run("2026년 9월")
    r_a4.font.size = Pt(10.0)

    doc.add_page_break()

    # ==========================================
    # PAGE 1: 서론 & 전국 17개 시도 거시 실증
    # ==========================================
    p_hdr1 = doc.add_paragraph()
    r_h1 = p_hdr1.add_run("Part 1. 서론 및 전국 17개 시·도 거시 실증")
    r_h1.font.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr1.paragraph_format.space_after = Pt(6)

    p_s1 = doc.add_paragraph()
    r_s1 = p_s1.add_run("1. 문제 제기: \"진짜 필요한 곳에 저상버스가 더 많이 가고 있는가?\"")
    r_s1.font.bold = True
    r_s1.font.size = Pt(11)
    r_s1.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_desc1 = doc.add_paragraph(
        "2023년 1월부터 노선버스 대폐차 시 저상버스 도입 의무화가 시행되었으나, 막대한 국가 재정(대당 약 9,000만 원)이 "
        "투입되는 저상버스가 정작 고령자와 등록장애인 등 교통약자 밀집 지역에 우선 공급되고 있는지에 대한 실증 연구는 부재했습니다. "
        "이에 본 연구는 국토교통부 실태조사 및 전국 인가 노선 전수 데이터를 활용하여 교통약자 이동권의 공간적 배분 실태를 검증했습니다."
    )

    # KPI Table
    tbl_kpi = doc.add_table(rows=1, cols=4)
    tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kpi, color="cbd5e1")
    kpi_cards = [
        ("[전국 거시] 17개 시·도", "r = -0.432", "약자 비율 높은 시·도일수록 도입률 낮은 경향", "dc2626"),
        ("경기도 31개 시·군", "r = -0.430", "전국 거시와 마찬가지로 취약지역 결핍 확인", "2563eb"),
        ("전국 광역 도입률 격차", "4.9배", "전남(11.5%) vs 서울(56.8%)", "d97706"),
        ("고령 취약지 저상노선", "0.0%", "가평군·연천군 등 0개 노선", "0891b2")
    ]
    for idx, (title, val, desc, color_hex) in enumerate(kpi_cards):
        c = tbl_kpi.rows[0].cells[idx]
        set_cell_background(c, "f8fafc")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rt = p.add_run(title + "\n")
        rt.font.size = Pt(7.5)
        rt.font.bold = True
        rt.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
        
        rv = p.add_run(val + "\n")
        rv.font.size = Pt(13)
        rv.font.bold = True
        rv.font.color.rgb = RGBColor(int(color_hex[:2], 16), int(color_hex[2:4], 16), int(color_hex[4:], 16))
        
        rd = p.add_run(desc)
        rd.font.size = Pt(7.0)
        rd.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_paragraph().paragraph_format.space_before = Pt(4)

    p_s2 = doc.add_paragraph()
    r_s2 = p_s2.add_run("2. [전국 거시 실증] 17개 시·도: 교통약자 비율 vs 저상버스 도입률")
    r_s2.font.bold = True
    r_s2.font.size = Pt(11)
    r_s2.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    doc.add_paragraph(
        "전국 17개 시·도 분석 결과, 교통약자가 많은 곳에 저상버스가 많을 것이라는 상식과 달리 r = -0.432(등록장애인 기준 r = -0.571, p < 0.05)의 음(-)의 상관관계가 관찰되었습니다."
    )

    # Chart 1 Image
    chart1_path = "c:/Users/hani/Desktop/antigravity/contest/results/pdf_chart1_sido.png"
    if os.path.exists(chart1_path):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(chart1_path, width=Mm(165))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc1 = p_cap1.add_run("[그림 1] 전국 17개 시·도 저상버스 도입률 산점도 (점 크기: 재정자립도, 주요 지자체 실측 수치 라벨링 반영)")
        rc1.font.size = Pt(7.5)
        rc1.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # Callout 1
    tbl_call1 = doc.add_table(rows=1, cols=1)
    tbl_call1.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = tbl_call1.rows[0].cells[0]
    set_cell_background(c1, "f1f5f9")
    set_cell_margins(c1, top=120, bottom=120, left=160, right=160)
    p_c1 = c1.paragraphs[0]
    rc1_title = p_c1.add_run("재정자립도와의 상관성 비교 실증 (Part 3 가설 연계):\n")
    rc1_title.font.bold = True
    rc1_title.font.size = Pt(8.5)
    rc1_title.font.color.rgb = RGBColor(0x03, 0x69, 0xa1)
    rc1_body = p_c1.add_run(
        "저상버스 도입률은 교통약자 비율(r = -0.432)과는 반대로, 지자체 재정자립도(r = +0.619, t = 3.05, p = 0.008 < 0.05)와 "
        "뚜렷한 양(+)의 상관관계를 보였습니다. 이는 현행 제도의 취지가 '수요자 중심 복지'여야 함에도, 실제 도입 현장에서는 "
        "지자체의 재정 부담 능력(지방비 50% 매칭)이 저상버스 보급 여부를 가르는 결정적 진입 장벽으로 작동하고 있음을 강력히 시사합니다."
    )
    rc1_body.font.size = Pt(8.0)

    doc.add_page_break()

    # ==========================================
    # PAGE 2: 경기도 31개 기초지자체 미시 전수 분석
    # ==========================================
    p_hdr2 = doc.add_paragraph()
    r_h2 = p_hdr2.add_run("Part 2. 경기도 31개 기초지자체 6,431개 노선 미시 전수 분석")
    r_h2.font.bold = True
    r_h2.font.size = Pt(13)
    r_h2.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr2.paragraph_format.space_after = Pt(6)

    p_s3 = doc.add_paragraph()
    r_s3 = p_s3.add_run("3. [기초단체 미시 전수] 경기도 31개 시·군 6,431개 버스 노선 검증")
    r_s3.font.bold = True
    r_s3.font.size = Pt(11)
    r_s3.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    doc.add_paragraph(
        "광역 단위 집계의 왜곡을 방지하기 위해 전국 축소판인 경기도 31개 시·군의 시내·마을버스 6,431개 노선 원장을 전수 분석했습니다. "
        "그 결과 경기도 기초자치단체 단위에서도 r = -0.430 (df = 29, t = -2.56, p = 0.016 < 0.05)으로 통계적으로 유의미한 역진적 배정이 입증되었습니다."
    )

    # Chart 2 Image
    chart2_path = "c:/Users/hani/Desktop/antigravity/contest/results/pdf_chart2_gyeonggi.png"
    if os.path.exists(chart2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(chart2_path, width=Mm(165))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc2 = p_cap2.add_run("[그림 2] 경기도 31개 시·군 수요-공급 4분면 매트릭스 (중앙값 기준 분할, 주요 시·군 실측 데이터 라벨링)")
        rc2.font.size = Pt(7.5)
        rc2.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    # 2 Column Box (Danger vs Success)
    tbl_quad = doc.add_table(rows=1, cols=2)
    tbl_quad.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_quad, color="cbd5e1")
    
    cq1 = tbl_quad.rows[0].cells[0]
    set_cell_background(cq1, "fef2f2")
    set_cell_margins(cq1, top=100, bottom=100, left=120, right=120)
    pq1 = cq1.paragraphs[0]
    rq1_t = pq1.add_run("[제1우선 소외구역] 수요 극대, 공급 바닥\n")
    rq1_t.font.bold = True
    rq1_t.font.size = Pt(8.2)
    rq1_t.font.color.rgb = RGBColor(0xb9, 0x1c, 0x1c)
    rq1_b = pq1.add_run(
        "가평군(0%), 연천군(0%), 여주시(0%), 동두천시(5.0%), 포천시(11.8%): 고령자·장애인 인구가 31~39%에 달하지만 "
        "저상버스는 전무합니다. 이들 지역의 재정자립도는 14.7% ~ 25.8%로 최하위권입니다."
    )
    rq1_b.font.size = Pt(7.5)

    cq2 = tbl_quad.rows[0].cells[1]
    set_cell_background(cq2, "f0fdf4")
    set_cell_margins(cq2, top=100, bottom=100, left=120, right=120)
    pq2 = cq2.paragraphs[0]
    rq2_t = pq2.add_run("[자원 집중구역] 도심권 신도시\n")
    rq2_t.font.bold = True
    rq2_t.font.size = Pt(8.2)
    rq2_t.font.color.rgb = RGBColor(0x15, 0x80, 0x3d)
    rq2_b = pq2.add_run(
        "하남시(63.9%), 광명시(62.7%), 부천시(59.6%), 수원시(52.7%): 교통약자 비율은 16.8% ~ 22.0% 수준이나, "
        "저상노선 비율은 52~64%에 달합니다. 재정자립도가 33~52%이며 평지 위주 인프라를 향유합니다."
    )
    rq2_b.font.size = Pt(7.5)

    doc.add_paragraph().paragraph_format.space_before = Pt(4)

    # Callout OLS
    tbl_ols = doc.add_table(rows=1, cols=1)
    tbl_ols.alignment = WD_TABLE_ALIGNMENT.CENTER
    co = tbl_ols.rows[0].cells[0]
    set_cell_background(co, "f1f5f9")
    set_cell_margins(co, top=120, bottom=120, left=160, right=160)
    p_co = co.paragraphs[0]
    rco_title = p_co.add_run("재정자립도를 통제해도 교통약자 소외는 유지되는가? (다중회귀 OLS 분석)\n")
    rco_title.font.bold = True
    rco_title.font.size = Pt(8.5)
    rco_title.font.color.rgb = RGBColor(0x03, 0x69, 0xa1)
    rco_body = p_co.add_run(
        "종속변수를 저상버스 노선 비율로 두고 재정자립도와 교통약자 비율을 동시 투입한 다중회귀분석 결과, "
        "재정자립도의 영향(β = +0.601, p = 0.0003)을 엄밀히 통제한 상태에서도 교통약자 비율의 회귀계수는 음(-)의 방향(β = -0.199, p = 0.178)을 유지했습니다. "
        "이는 지자체의 재정 여력만으로는 설명되지 않는 제도적·지형적 장벽이 취약지역에 복합적으로 작용하고 있음을 보여줍니다."
    )
    rco_body.font.size = Pt(8.0)

    doc.add_page_break()

    # ==========================================
    # PAGE 3: 실증 분석 원자료 상세 현황 표
    # ==========================================
    p_hdr3 = doc.add_paragraph()
    r_h3 = p_hdr3.add_run("Part 2 (부록 표). 전국 및 경기도 기초지자체 전수 통계 데이터")
    r_h3.font.bold = True
    r_h3.font.size = Pt(13)
    r_h3.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr3.paragraph_format.space_after = Pt(6)

    p_s4 = doc.add_paragraph()
    r_s4 = p_s4.add_run("4. 실증 분석 원자료 상세 현황 표 (전국 17개 시·도 및 경기도 31개 시·군)")
    r_s4.font.bold = True
    r_s4.font.size = Pt(11)
    r_s4.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_note = doc.add_paragraph("※ 화면 및 본문에는 가독성을 위해 소수점 첫째자리 표기값을 적용하였으며, 저상버스 도입률 기준 내림차순 정렬되었습니다.")
    p_note.runs[0].font.size = Pt(7.5)
    p_note.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    sido_data = [
        ("시·도명", "저상버스 도입률", "시내버스 도입률", "교통약자 비율", "고령인구 비율", "등록장애인 비율", "재정자립도", "판정 분류"),
        ("서울특별시", "56.8%", "66.7%", "22.6%", "18.5%", "4.13%", "81.2%", "우수 도입"),
        ("대구광역시", "46.1%", "46.5%", "25.1%", "19.6%", "5.49%", "52.3%", "우수 도입"),
        ("세종특별자치시", "41.3%", "46.4%", "14.3%", "11.0%", "3.34%", "69.7%", "우수 도입"),
        ("대전광역시", "39.0%", "39.7%", "21.9%", "17.0%", "4.95%", "46.4%", "보통"),
        ("광주광역시", "34.8%", "37.7%", "21.4%", "16.5%", "4.88%", "46.2%", "보통"),
        ("경상남도", "32.8%", "37.9%", "26.4%", "20.6%", "5.79%", "38.8%", "보통"),
        ("경기도", "30.7%", "32.1%", "19.9%", "15.6%", "4.28%", "65.7%", "보통"),
        ("부산광역시", "29.9%", "36.4%", "27.9%", "22.6%", "5.32%", "53.2%", "보통"),
        ("제주특별자치도", "26.1%", "41.9%", "30.6%", "24.0%", "6.57%", "29.4%", "보통"),
        ("충청북도", "25.4%", "33.3%", "26.9%", "20.8%", "6.08%", "36.2%", "보통"),
        ("강원특별자치도", "24.8%", "30.5%", "31.5%", "24.1%", "7.41%", "27.9%", "보통"),
        ("인천광역시", "18.6%", "18.8%", "21.7%", "16.6%", "5.06%", "59.6%", "취약 지역"),
        ("전북특별자치도", "18.3%", "18.9%", "23.4%", "17.9%", "5.46%", "36.9%", "취약 지역"),
        ("경상북도", "18.0%", "22.7%", "31.7%", "24.7%", "6.97%", "29.7%", "취약 지역"),
        ("충청남도", "16.5%", "21.7%", "27.6%", "21.3%", "6.28%", "37.9%", "취약 지역"),
        ("울산광역시", "13.8%", "14.6%", "20.5%", "15.9%", "4.64%", "56.6%", "취약 지역"),
        ("전라남도", "11.5%", "20.3%", "33.7%", "26.1%", "7.55%", "28.7%", "전국 최하위")
    ]
    
    tbl_sido = doc.add_table(rows=len(sido_data), cols=8)
    tbl_sido.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_sido, color="cbd5e1")
    
    for r_idx, row_vals in enumerate(sido_data):
        row = tbl_sido.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            if r_idx == 0:
                set_cell_background(cell, "f1f5f9")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "f8fafc")
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(7.0)
            if r_idx == 0:
                r.font.bold = True
            elif c_idx == 0:
                r.font.bold = True
            elif c_idx == 7:
                if "우수" in val:
                    r.font.color.rgb = RGBColor(0x1d, 0x4e, 0xd8)
                    r.font.bold = True
                elif "취약" in val or "최하위" in val:
                    r.font.color.rgb = RGBColor(0xb9, 0x1c, 0x1c)
                    r.font.bold = True

    p_g_sub = doc.add_paragraph()
    p_g_sub.paragraph_format.space_before = Pt(8)
    r_gsub = p_g_sub.add_run("경기도 주요 기초지자체(저상버스 노선 비율 기준 내림차순 정렬)")
    r_gsub.font.bold = True
    r_gsub.font.size = Pt(9.0)

    gg_data = [
        ("시·군명", "저상버스 노선 비율", "운행노선수 / 전체", "교통약자 비율", "고령인구 비율", "등록장애인 비율", "재정자립도", "4분면 배정 결과"),
        ("하남시", "63.9%", "46 / 72개", "18.1%", "14.4%", "3.62%", "52.0%", "자원 집중지"),
        ("광명시", "62.7%", "32 / 51개", "21.1%", "16.7%", "4.39%", "39.0%", "자원 집중지"),
        ("부천시", "59.6%", "112 / 188개", "22.0%", "17.2%", "4.78%", "33.0%", "자원 집중지"),
        ("수원시", "52.7%", "127 / 241개", "16.8%", "13.1%", "3.70%", "49.2%", "자원 집중지"),
        ("성남시", "16.1%", "18 / 112개", "20.5%", "16.6%", "3.89%", "61.5%", "일반 구역"),
        ("양평군", "15.3%", "72 / 470개", "36.0%", "29.4%", "6.55%", "21.1%", "제1우선 소외지"),
        ("포천시", "11.8%", "16 / 136개", "31.4%", "24.3%", "7.11%", "25.8%", "제1우선 소외지"),
        ("동두천시", "5.0%", "7 / 141개", "31.2%", "24.1%", "7.09%", "14.7%", "제1우선 소외지"),
        ("용인시", "3.1%", "8 / 256개", "18.9%", "15.4%", "3.47%", "53.3%", "일반 구역"),
        ("가평군", "0.0%", "0 / 58개", "38.2%", "30.0%", "8.13%", "20.6%", "제1우선 소외지"),
        ("여주시", "0.0%", "0 / 2개", "31.8%", "25.3%", "6.56%", "24.6%", "제1우선 소외지(소표본)"),
        ("연천군", "0.0%", "0 / 81개", "39.2%", "31.0%", "8.21%", "19.6%", "제1우선 소외지")
    ]
    
    tbl_gg = doc.add_table(rows=len(gg_data), cols=8)
    tbl_gg.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_gg, color="cbd5e1")

    for r_idx, row_vals in enumerate(gg_data):
        row = tbl_gg.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            if r_idx == 0:
                set_cell_background(cell, "f1f5f9")
            elif "자원 집중지" in row_vals[7]:
                set_cell_background(cell, "eff6ff")
            elif "소외지" in row_vals[7]:
                set_cell_background(cell, "fef2f2")
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(7.0)
            if r_idx == 0 or c_idx in (0, 1):
                r.font.bold = True
            if c_idx == 7:
                r.font.bold = True
                if "자원 집중지" in val:
                    r.font.color.rgb = RGBColor(0x1d, 0x4e, 0xd8)
                elif "소외지" in val:
                    r.font.color.rgb = RGBColor(0xb9, 0x1c, 0x1c)

    doc.add_page_break()

    # ==========================================
    # PAGE 4: 구조적 원인 진단 (3대 설명 가설)
    # ==========================================
    p_hdr4 = doc.add_paragraph()
    r_h4 = p_hdr4.add_run("Part 3. 구조적 원인 진단: 왜 역진적 배정이 일어나는가? (해석 가설)")
    r_h4.font.bold = True
    r_h4.font.size = Pt(13)
    r_h4.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr4.paragraph_format.space_after = Pt(6)

    p_s5 = doc.add_paragraph()
    r_s5 = p_s5.add_run("5. 구조적 설명 가설: 교통약자 밀집지에 저상버스가 적은 3대 메커니즘")
    r_s5.font.bold = True
    r_s5.font.size = Pt(11)
    r_s5.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_hnote = doc.add_paragraph("※ 본 항목들은 통계 분석에서 규명된 공간적 격차를 제도적·운영적 맥락에서 해석하기 위해 도출한 '설명 가설'입니다.")
    p_hnote.runs[0].font.size = Pt(8.0)
    p_hnote.runs[0].font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    hypotheses = [
        ("가설 01", "'국비 50% 정률 매칭' 제도의 재정적 장벽 가설",
         "저상버스 대당 구입 보조금(약 9,000만 원)은 일반 지자체 기준 국비 50%와 지자체 지방비 50%(약 4,500만 원)를 1:1 매칭해야 교부되는 정률 지원 구조입니다. (단, 서울은 국가 40%: 서울시 60%로 상이함).\n"
         "재정자립도가 14~25%에 불과한 농어촌 군 지역은 수십 대의 저상버스 지방비 매칭 예산을 편성하기 어렵습니다. 이로 인해 버스 대폐차 시기가 도래해도 저상버스 신청 자체를 충분히 집행하지 못했을 가능성이 큽니다.",
         "실증 부합성: 전국 17개 시도 재정자립도 상관계수 r = +0.619 (p = 0.008), 경기도 상위 4개 시군(하남·광명 등) 재정 35~52% vs 소외 5개 시군 14~25%의 재정 격차와 완벽히 일치."),
        
        ("가설 02", "운수회사의 승객 수요 및 운송 효율성 중심 배차 가설",
         "민간 버스 운수회사 및 준공영제 체계에서는 승객 회전율이 높고 운송 수입이 보장되는 도심 황금 간선 노선에 신차와 저상버스를 우선 배차하는 경향이 뚜렷합니다.\n"
         "반면 교통약자가 주로 거주하는 외곽 읍·면 지선 노선은 승객 밀도가 낮고 운행 거리가 길어 차량 교체 우선순위에서 지속적으로 후순위로 밀려 배제되었을 개연성이 높습니다.",
         "실증 부합성: 경기도 노선 전수 분석에서 수원(127개 노선 저상 투입) 등 간선 위주 지자체의 집중 배정 vs 가평·연천 등 군내 지선 노선의 0% 방치 현상 설명."),
        
        ("가설 03", "도로 인프라 환경과 '도입 예외 승인' 제도의 사각지대 가설",
         "현행 「교통약자법」 제14조 제4항 및 국토교통부 고시에 따라 도로의 종단경사(급경사), 굴곡, 과속방지턱 등 도로 환경이 부적합한 노선은 지자체 승인을 통해 저상버스 도입 의무에서 제외될 수 있습니다.\n"
         "도로 정비 예산이 부족한 외곽 농어촌일수록 예외 노선 신청 및 승인 비율이 높아져, 제도가 오히려 취약지역의 저상버스 도입을 공식적으로 차단하는 '역설적 사각지대'를 낳았을 가능성이 제기됩니다.",
         "실증 부합성: 차체 바닥이 낮은 대형 저상버스(11m)의 물리적 한계로 인해 도로 환경이 취약한 군 지역이 제도적으로 저상버스 투입 대상에서 원천 배제됨.")
    ]

    for h_tag, h_title, h_body, h_match in hypotheses:
        tbl_h = doc.add_table(rows=1, cols=1)
        tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_h, color="cbd5e1")
        ch = tbl_h.rows[0].cells[0]
        set_cell_background(ch, "f8fafc")
        set_cell_margins(ch, top=120, bottom=120, left=160, right=160)
        ph = ch.paragraphs[0]
        
        rt = ph.add_run(f"[{h_tag}] {h_title}\n")
        rt.font.bold = True
        rt.font.size = Pt(9.5)
        rt.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
        
        rb = ph.add_run(h_body + "\n\n")
        rb.font.size = Pt(8.3)
        rb.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        rm = ph.add_run(h_match)
        rm.font.size = Pt(7.8)
        rm.font.bold = True
        rm.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

        doc.add_paragraph().paragraph_format.space_before = Pt(3)

    doc.add_page_break()

    # ==========================================
    # PAGE 5: 정책 제언 & 한계
    # ==========================================
    p_hdr5 = doc.add_paragraph()
    r_h5 = p_hdr5.add_run("Part 4 & 5. 데이터 기반 정책 제언(안) 및 연구의 한계")
    r_h5.font.bold = True
    r_h5.font.size = Pt(13)
    r_h5.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr5.paragraph_format.space_after = Pt(6)

    p_s6 = doc.add_paragraph()
    r_s6 = p_s6.add_run("6. 데이터 기반 3대 정책 제언(안): 역진성 극복 로드맵")
    r_s6.font.bold = True
    r_s6.font.size = Pt(11)
    r_s6.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    doc.add_paragraph(
        "단순 문제 제기에 그치지 않고, 본 실증 분석 결과를 바탕으로 교통약자 이동 형평성을 실질적으로 회복하기 위한 3단계 정책 대안을 제안합니다."
    )

    policies = [
        ("Fiscal Reform", "교통약자 수요 연동형 차등 국비 보조율 제도(안)",
         "현행 50% 일률 국비 지원을 지자체 재정자립도와 교통약자 비율에 따라 30% ~ 80%로 차등화. 재정이 열악한 농어촌 지자체의 지방비 부담을 1,800만 원 선으로 대폭 경감하여 예산 장벽을 해소합니다.",
         "국비보조율(안) = 기본 50% + 약자가산(최대15%) + 재정가산(최대15%) → 최대 80%"),
        
        ("Data Scoring", "데이터 기반 '저상버스 도입 우선순위 평가 모델(안)'",
         "자의적·선착순 신청을 배제하고, 행정동별 약자 밀도, 병원·복지관 경유도, 공급 부족도를 결합한 종합 우선순위 평가 지표(안)를 산출하여 중앙정부 공모 평가 시 객관적 배정 쿼터제로 활용합니다.",
         "우선순위점수 = 0.4×(약자비율) + 0.3×(병원접근도) + 0.3×(1 - 현재공급률)"),
        
        ("Smart Infra", "중형 저상 전기버스 & 도로 환경 개선 패키지(안)",
         "대형(11m) 버스 운행이 불가능한 농어촌 지선 도로를 위해 중형(8~9m) 저상 전기버스 전용 지원 트랙을 신설하고, 도입 예외 구간의 도로 굴곡 및 단차 개선을 국비 1:1 패키지로 지원합니다.",
         "패키지 연계 = [중형 저상버스 보조금 신설] + [도로 굴곡·단차 정비 국비 패키지]")
    ]

    tbl_pol = doc.add_table(rows=1, cols=3)
    tbl_pol.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pol, color="cbd5e1")
    for p_idx, (tag, p_title, p_desc, p_form) in enumerate(policies):
        cp = tbl_pol.rows[0].cells[p_idx]
        set_cell_background(cp, "f8fafc")
        set_cell_margins(cp, top=120, bottom=120, left=120, right=120)
        pp = cp.paragraphs[0]
        
        rt = pp.add_run(f"[{tag}]\n")
        rt.font.bold = True
        rt.font.size = Pt(7.5)
        rt.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
        
        rh = pp.add_run(p_title + "\n\n")
        rh.font.bold = True
        rh.font.size = Pt(8.8)
        rh.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        
        rd = pp.add_run(p_desc + "\n\n")
        rd.font.size = Pt(7.6)
        rd.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        rf = pp.add_run(p_form)
        rf.font.size = Pt(7.0)
        rf.font.bold = True
        rf.font.color.rgb = RGBColor(0x03, 0x69, 0xa1)

    doc.add_paragraph().paragraph_format.space_before = Pt(8)

    p_s7 = doc.add_paragraph()
    r_s7 = p_s7.add_run("7. 본 분석의 방법론적 한계 및 향후 연구 과제")
    r_s7.font.bold = True
    r_s7.font.size = Pt(11)
    r_s7.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    tbl_lim = doc.add_table(rows=1, cols=1)
    tbl_lim.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lim, color="cbd5e1")
    cl = tbl_lim.rows[0].cells[0]
    set_cell_background(cl, "f8fafc")
    set_cell_margins(cl, top=120, bottom=120, left=160, right=160)
    pl = cl.paragraphs[0]
    limits = [
        ("횡단면 데이터의 한계", "본 연구는 2023년 시점의 데이터를 비교한 것으로, 통계적 관련성을 확인한 것이며 인과관계로 단정할 수는 없습니다."),
        ("교통약자 집계의 중복성", "'교통약자 비율'은 65세 이상 고령자와 등록장애인을 단순 합산하여 고령 장애인이 중복 집계되었을 가능성이 있습니다."),
        ("공급 지표 정의의 차이", "전국은 '저상버스 차량 대수 비율(%)'을, 경기도는 '저상버스 운행 노선 비율(%)'을 사용하여 상호 직접 비교 시 유의가 필요합니다."),
        ("소표본 지자체 해석 주의", "여주시의 경우 분석 노선 수가 2개(운행 노선 0개)로 표본 규모가 매우 작음에 유의해야 합니다."),
        ("우선순위 평가 모델의 탐색적 성격", "제안된 산식은 정책 대안으로서의 시뮬레이션 지표이며 실제 정책 적용 시 다속성 의사결정(AHP) 검증이 선행되어야 합니다.")
    ]
    for l_idx, (lt, ld) in enumerate(limits):
        rlt = pl.add_run(f"• {lt}: ")
        rlt.font.bold = True
        rlt.font.size = Pt(8.0)
        rld = pl.add_run(ld + ("\n" if l_idx < len(limits)-1 else ""))
        rld.font.size = Pt(8.0)

    doc.add_page_break()

    # ==========================================
    # PAGE 6: 부록 및 참고문헌
    # ==========================================
    p_hdr6 = doc.add_paragraph()
    r_h6 = p_hdr6.add_run("Appendix. 데이터 원천 출처 및 참고문헌")
    r_h6.font.bold = True
    r_h6.font.size = Pt(13)
    r_h6.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    p_hdr6.paragraph_format.space_after = Pt(6)

    p_s8 = doc.add_paragraph()
    r_s8 = p_s8.add_run("8. 데이터 출처 및 참고문헌 (공식 원문 출처)")
    r_s8.font.bold = True
    r_s8.font.size = Pt(11)
    r_s8.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    refs = [
        ("1. 국토교통부 · 한국교통안전공단 (2024.06)", "『2023년도 교통약자 이동편의 실태조사 연구보고서』\n(전국 17개 시·도 저상버스 도입 대수, 노선버스 인가 대수, 보급률 확정 통계)\n출처: TMACS 교통안전정보관리시스템 (tmacs.kotsa.or.kr) | 공공데이터포털"),
        ("2. 통계청 국가통계포털(KOSIS)", "시군구별 주민등록인구 및 고령인구비율 (2023년 말 기준, 통계표ID: DT_1YL20631)\n출처: KOSIS 국가통계포털 (kosis.kr)"),
        ("3. 보건복지부 · 통계청 KOSIS", "전국 시·군·구별 등록장애인수 현황 (2023년 말 기준, 통계표ID: DT_1YL202003E)\n출처: 보건복지통계연보 및 KOSIS 통계표"),
        ("4. 행정안전부 · 지방재정365", "전국 지방자치단체 재정자립도 및 재정자주도 결산 통계 (2023년 당초예산 기준, 통계표ID: DT_1YL20921)\n출처: 지방재정통합공개시스템 (lofin.mois.go.kr)"),
        ("5. 경기교통정보센터 · 경기데이터드림", "경기도 시·군별 시내버스 및 마을버스 인가 노선별 저상버스 운행정보 전수 원장 (6,431개 노선 전수, 2023년 12월 기준)\n출처: 경기데이터드림 (data.gg.go.kr)"),
        ("6. 대한민국 법령정보", "「교통약자의 이동편의 증진법」(법률 제18738호, 2023.01.19 시행) 제14조 및 동법 시행령 제14조의2\n출처: 국가법령정보센터 (law.go.kr)"),
        ("7. 국토교통부 고시 제2023-38호", "『저상버스 도입 예외 승인 기준에 관한 고시』")
    ]

    for ref_title, ref_desc in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(5)
        rr_t = p_ref.add_run(ref_title + "\n")
        rr_t.font.bold = True
        rr_t.font.size = Pt(8.5)
        rr_d = p_ref.add_run(ref_desc)
        rr_d.font.size = Pt(7.8)
        rr_d.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    tbl_repo = doc.add_table(rows=1, cols=1)
    tbl_repo.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_repo, color="cbd5e1")
    cr = tbl_repo.rows[0].cells[0]
    set_cell_background(cr, "f1f5f9")
    set_cell_margins(cr, top=120, bottom=120, left=160, right=160)
    pr = cr.paragraphs[0]
    rr_t = pr.add_run("온라인 검증 및 재현성 안내\n")
    rr_t.font.bold = True
    rr_t.font.size = Pt(8.8)
    rr_t.font.color.rgb = RGBColor(0x03, 0x69, 0xa1)
    rr_b = pr.add_run(
        "본 보고서에 수록된 모든 분석 코드(Jupyter Notebook, Python 스크립트) 및 시각화 생성 스크립트는 오픈 소스로 완전 공개되어 있습니다.\n"
        "• 분석 코드 GitHub 저장소: https://github.com/contest-lab/contest\n"
        "• 웹 인터랙티브 보고서: https://contest-lab.github.io/contest/"
    )
    rr_b.font.size = Pt(8.2)

    out_path = "c:/Users/hani/Desktop/antigravity/contest/results/contest_report_editable.docx"
    doc.save(out_path)
    print(f"[SUCCESS] Saved A4 Portrait editable docx to {out_path}")

if __name__ == "__main__":
    build_docx()
