# -*- coding: utf-8 -*-
"""
Generate a fully editable PowerPoint presentation (.pptx)
strictly formatted in A4 Portrait (210mm x 297mm) matching contest_report_final.pdf.
Every page mirrors the exact layout of the 7-page PDF report with native text boxes,
shapes, tables, and inserted charts.
"""
import os
import pptx
from pptx.util import Mm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def add_header(slide, title_text, page_num_str):
    # Header container
    tb = slide.shapes.add_textbox(Mm(15), Mm(10), Mm(180), Mm(9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    
    r1 = p.add_run()
    r1.text = title_text
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = RGBColor(3, 105, 161)
    
    r2 = p.add_run()
    r2.text = f"                                                AI 교통 데이터 공모전 심층보고서 [{page_num_str}]"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = RGBColor(100, 116, 139)

    # Dividing line under header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(15), Mm(18), Mm(180), Mm(0.4))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(2, 132, 199)
    line.line.color.rgb = RGBColor(2, 132, 199)

def add_footer(slide, note_text, page_num_str):
    # Dividing line above footer
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(15), Mm(282), Mm(180), Mm(0.3))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(226, 232, 240)
    line.line.color.rgb = RGBColor(226, 232, 240)

    tb = slide.shapes.add_textbox(Mm(15), Mm(283.5), Mm(180), Mm(8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    
    r1 = p.add_run()
    r1.text = note_text
    r1.font.size = Pt(7.5)
    r1.font.color.rgb = RGBColor(148, 163, 184)
    
    r2 = p.add_run()
    r2.text = f"                                                                               {page_num_str}"
    r2.font.size = Pt(7.5)
    r2.font.color.rgb = RGBColor(148, 163, 184)

def build_a4_portrait_pptx():
    prs = pptx.Presentation()
    # A4 Portrait: 210mm x 297mm
    prs.slide_width = Mm(210)
    prs.slide_height = Mm(297)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 0: 표지 (COVER PAGE)
    # =========================================================================
    s0 = prs.slides.add_slide(blank_layout)

    # Competition Tag
    sh_tag = s0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(25), Mm(35), Mm(160), Mm(10))
    sh_tag.fill.solid()
    sh_tag.fill.fore_color.rgb = RGBColor(224, 242, 254)
    sh_tag.line.color.rgb = RGBColor(186, 230, 253)
    p_tag = sh_tag.text_frame.paragraphs[0]
    p_tag.alignment = PP_ALIGN.CENTER
    r_tag = p_tag.add_run()
    r_tag.text = "한겨레 × (재단법인) 숲과나눔 「AI와 함께하는 교통문제 해결 데이터 분석 공모전」 제출작"
    r_tag.font.bold = True
    r_tag.font.size = Pt(9.5)
    r_tag.font.color.rgb = RGBColor(2, 132, 199)

    # Main Title
    tb_title = s0.shapes.add_textbox(Mm(15), Mm(58), Mm(180), Mm(38))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.alignment = PP_ALIGN.CENTER
    r_t1 = p_t1.add_run()
    r_t1.text = "교통약자가 많은 지역에\n"
    r_t1.font.bold = True
    r_t1.font.size = Pt(24)
    r_t1.font.color.rgb = RGBColor(15, 23, 42)
    
    r_t2 = p_t1.add_run()
    r_t2.text = "저상버스가 더 많이 다니고 있는가?"
    r_t2.font.bold = True
    r_t2.font.size = Pt(24)
    r_t2.font.color.rgb = RGBColor(2, 132, 199)

    # Subtitle
    tb_sub = s0.shapes.add_textbox(Mm(20), Mm(98), Mm(170), Mm(22))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.CENTER
    r_sub = p_sub.add_run()
    r_sub.text = "전국 17개 시·도 및 경기도 31개 시·군 6,431개 버스 노선 전수 분석을 통해 본\n저상버스 도입의 공간적 역진성(Regressive Allocation)과 정책 개선 방안"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Metadata Box
    sh_box = s0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(25), Mm(135), Mm(160), Mm(65))
    sh_box.fill.solid()
    sh_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    sh_box.line.color.rgb = RGBColor(226, 232, 240)
    
    tb_meta = s0.shapes.add_textbox(Mm(30), Mm(138), Mm(150), Mm(58))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True
    
    p0 = tf_meta.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "보고서 핵심 메타데이터 & 접속 채널\n"
    r0.font.bold = True
    r0.font.size = Pt(9.5)
    r0.font.color.rgb = RGBColor(15, 23, 42)

    meta_items = [
        ("분석 기준연도: ", "2023년 (국토교통부 실태조사 공인 확정 통계)"),
        ("전수 분석 대상: ", "전국 17개 시·도 및 경기도 31개 시·군 6,431개 버스 노선"),
        ("온라인 웹 보고서: ", "https://contest-lab.github.io/contest/"),
        ("GitHub 소스코드: ", "https://github.com/contest-lab/contest")
    ]
    for lbl, val in meta_items:
        p = tf_meta.add_paragraph()
        p.space_before = Pt(4)
        rl = p.add_run()
        rl.text = lbl
        rl.font.bold = True
        rl.font.size = Pt(8.5)
        rl.font.color.rgb = RGBColor(100, 116, 139)
        
        rv = p.add_run()
        rv.text = val
        rv.font.size = Pt(8.5)
        if "http" in val:
            rv.font.color.rgb = RGBColor(2, 132, 199)
            rv.font.bold = True
        else:
            rv.font.color.rgb = RGBColor(15, 23, 42)

    # Author
    tb_auth = s0.shapes.add_textbox(Mm(20), Mm(225), Mm(170), Mm(25))
    tf_auth = tb_auth.text_frame
    p_auth = tf_auth.paragraphs[0]
    p_auth.alignment = PP_ALIGN.CENTER
    r_a1 = p_auth.add_run()
    r_a1.text = "제출자: "
    r_a1.font.bold = True
    r_a1.font.size = Pt(11)
    r_a1.font.color.rgb = RGBColor(100, 116, 139)
    r_a2 = p_auth.add_run()
    r_a2.text = "김일중\n"
    r_a2.font.bold = True
    r_a2.font.size = Pt(11)
    r_a2.font.color.rgb = RGBColor(15, 23, 42)
    
    p_date = tf_auth.add_paragraph()
    p_date.alignment = PP_ALIGN.CENTER
    p_date.space_before = Pt(3)
    r_d1 = p_date.add_run()
    r_d1.text = "제출일자: "
    r_d1.font.bold = True
    r_d1.font.size = Pt(10)
    r_d1.font.color.rgb = RGBColor(100, 116, 139)
    r_d2 = p_date.add_run()
    r_d2.text = "2026년 9월"
    r_d2.font.size = Pt(10)
    r_d2.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # SLIDE 1 (본문 1/5): 서론 및 전국 17개 시도 거시 실증
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_header(s1, "Part 1. 서론 및 전국 17개 시·도 거시 실증", "1/5")
    add_footer(s1, "본 보고서의 데이터는 KOSIS 및 국토교통부 실태조사 공인 원장을 기반으로 집계되었습니다.", "본문 1 / 5")

    # Section 1 Heading
    tb_s1 = s1.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(24))
    tf_s1 = tb_s1.text_frame
    tf_s1.word_wrap = True
    tf_s1.margin_left = tf_s1.margin_right = tf_s1.margin_top = tf_s1.margin_bottom = 0
    p = tf_s1.paragraphs[0]
    r = p.add_run()
    r.text = "1. 문제 제기: \"진짜 필요한 곳에 저상버스가 더 많이 가고 있는가?\"\n"
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p2 = tf_s1.add_paragraph()
    p2.space_before = Pt(2)
    r2 = p2.add_run()
    r2.text = (
        "2023년 1월부터 노선버스 대폐차 시 저상버스 도입 의무화가 시행되었으나, 막대한 국가 재정(대당 약 9,000만 원)이 "
        "투입되는 저상버스가 정작 고령자와 등록장애인 등 교통약자 밀집 지역에 우선 공급되고 있는지에 대한 실증 연구는 부재했습니다. "
        "이에 본 연구는 국토교통부 실태조사 및 전국 인가 노선 전수 데이터를 활용하여 교통약자 이동권의 공간적 배분 실태를 검증했습니다."
    )
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(30, 41, 59)

    # 4 KPI Cards in a row
    kpi_cards = [
        ("[전국 거시] 17개 시·도", "r = -0.432", "약자비율 높은 곳일수록 도입률 낮음", RGBColor(220, 38, 38)),
        ("경기도 31개 시·군", "r = -0.430", "취약지역 저상노선 결핍 확인", RGBColor(37, 99, 235)),
        ("전국 광역 도입률 격차", "4.9배", "전남(11.5%) vs 서울(56.8%)", RGBColor(217, 119, 6)),
        ("고령 취약지 저상노선", "0.0%", "가평·연천 등 0개 노선", RGBColor(8, 145, 178))
    ]
    card_w = Mm(43)
    card_gap = Mm(2.6)
    for i, (k_t, k_v, k_d, col) in enumerate(kpi_cards):
        cx = Mm(15) + i * (card_w + card_gap)
        cy = Mm(47)
        sh = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, card_w, Mm(22))
        sh.fill.solid()
        sh.fill.fore_color.rgb = RGBColor(248, 250, 252)
        sh.line.color.rgb = RGBColor(226, 232, 240)
        
        tb = s1.shapes.add_textbox(cx + Mm(1.5), cy + Mm(1.5), card_w - Mm(3), Mm(19))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        pt = tf.paragraphs[0]
        rt = pt.add_run()
        rt.text = k_t + "\n"
        rt.font.bold = True
        rt.font.size = Pt(7.0)
        rt.font.color.rgb = RGBColor(100, 116, 139)
        
        pv = tf.add_paragraph()
        rv = pv.add_run()
        rv.text = k_v + "\n"
        rv.font.bold = True
        rv.font.size = Pt(12)
        rv.font.color.rgb = col
        
        pd = tf.add_paragraph()
        rd = pd.add_run()
        rd.text = k_d
        rd.font.size = Pt(6.5)
        rd.font.color.rgb = RGBColor(71, 85, 105)

    # Section 2 Heading
    tb_s2 = s1.shapes.add_textbox(Mm(15), Mm(71), Mm(180), Mm(15))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_right = tf_s2.margin_top = tf_s2.margin_bottom = 0
    p = tf_s2.paragraphs[0]
    r = p.add_run()
    r.text = "2. [전국 거시 실증] 17개 시·도: 교통약자 비율 vs 저상버스 도입률\n"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p2 = tf_s2.add_paragraph()
    r2 = p2.add_run()
    r2.text = "전국 17개 시·도 분석 결과, 교통약자가 많은 곳에 저상버스가 많을 것이라는 상식과 달리 r = -0.432(등록장애인 기준 r = -0.571, p < 0.05)의 음(-)의 상관관계가 관찰되었습니다."
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(30, 41, 59)

    # Chart 1 Image
    chart1_path = "c:/Users/hani/Desktop/antigravity/contest/results/pdf_chart1_sido.png"
    if os.path.exists(chart1_path):
        s1.shapes.add_picture(chart1_path, Mm(15), Mm(89), width=Mm(180))

    # Caption
    tb_c1 = s1.shapes.add_textbox(Mm(15), Mm(226), Mm(180), Mm(6))
    p_c1 = tb_c1.text_frame.paragraphs[0]
    p_c1.alignment = PP_ALIGN.CENTER
    rc1 = p_c1.add_run()
    rc1.text = "[그림 1] 전국 17개 시·도 저상버스 도입률 산점도 (점 크기: 재정자립도, 주요 지자체 실측 수치 라벨링 반영)"
    rc1.font.size = Pt(7.4)
    rc1.font.color.rgb = RGBColor(100, 116, 139)

    # Callout Box 1
    sh_call1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(15), Mm(234), Mm(180), Mm(44))
    sh_call1.fill.solid()
    sh_call1.fill.fore_color.rgb = RGBColor(241, 245, 249)
    sh_call1.line.color.rgb = RGBColor(2, 132, 199)
    
    tb_cb1 = s1.shapes.add_textbox(Mm(18), Mm(236), Mm(174), Mm(40))
    tf_cb1 = tb_cb1.text_frame
    tf_cb1.word_wrap = True
    tf_cb1.margin_left = tf_cb1.margin_right = tf_cb1.margin_top = tf_cb1.margin_bottom = 0
    pc1_t = tf_cb1.paragraphs[0]
    rc1_t = pc1_t.add_run()
    rc1_t.text = "재정자립도와의 상관성 비교 실증 (Part 3 가설 연계):\n"
    rc1_t.font.bold = True
    rc1_t.font.size = Pt(8.5)
    rc1_t.font.color.rgb = RGBColor(3, 105, 161)
    
    rc1_b = pc1_t.add_run()
    rc1_b.text = (
        "저상버스 도입률은 교통약자 비율(r = -0.432)과는 반대로, 지자체 재정자립도(r = +0.619, t = 3.05, p = 0.008 < 0.05)와 "
        "뚜렷한 양(+)의 상관관계를 보였습니다. 이는 현행 제도의 취지가 '수요자 중심 복지'여야 함에도, 실제 도입 현장에서는 "
        "지자체의 재정 부담 능력(지방비 50% 매칭)이 저상버스 보급 여부를 가르는 결정적 진입 장벽으로 작동하고 있음을 강력히 시사합니다."
    )
    rc1_b.font.size = Pt(8.0)
    rc1_b.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # SLIDE 2 (본문 2/5): 경기도 미시 전수 분석 및 4분면 매트릭스
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Part 2. 경기도 31개 기초지자체 6,431개 노선 미시 전수 분석", "2/5")
    add_footer(s2, "단위: 인가 노선수 대비 저상버스 투입 노선 비율 (단순 대수 집계 한계 극복)", "본문 2 / 5")

    tb_s3 = s2.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(16))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    tf_s3.margin_left = tf_s3.margin_right = tf_s3.margin_top = tf_s3.margin_bottom = 0
    p = tf_s3.paragraphs[0]
    r = p.add_run()
    r.text = "3. [기초단체 미시 전수] 경기도 31개 시·군 6,431개 버스 노선 검증\n"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p2 = tf_s3.add_paragraph()
    r2 = p2.add_run()
    r2.text = "광역 단위 집계의 왜곡을 방지하기 위해 전국 축소판인 경기도 31개 시·군의 시내·마을버스 6,431개 노선 원장을 전수 분석했습니다. 그 결과 경기도 기초자치단체 단위에서도 r = -0.430 (df = 29, t = -2.56, p = 0.016 < 0.05)으로 통계적으로 유의미한 역진적 배정이 입증되었습니다."
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(30, 41, 59)

    # Chart 2 Image
    chart2_path = "c:/Users/hani/Desktop/antigravity/contest/results/pdf_chart2_gyeonggi.png"
    if os.path.exists(chart2_path):
        s2.shapes.add_picture(chart2_path, Mm(15), Mm(39), width=Mm(180))

    # Caption
    tb_c2 = s2.shapes.add_textbox(Mm(15), Mm(176), Mm(180), Mm(6))
    p_c2 = tb_c2.text_frame.paragraphs[0]
    p_c2.alignment = PP_ALIGN.CENTER
    rc2 = p_c2.add_run()
    rc2.text = "[그림 2] 경기도 31개 시·군 수요-공급 4분면 매트릭스 (중앙값 기준 분할, 주요 시·군 실측 데이터 라벨링)"
    rc2.font.size = Pt(7.4)
    rc2.font.color.rgb = RGBColor(100, 116, 139)

    # 2 Comparison Boxes Side-by-Side
    # Left Danger Box
    sh_danger = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(15), Mm(184), Mm(88), Mm(45))
    sh_danger.fill.solid()
    sh_danger.fill.fore_color.rgb = RGBColor(254, 242, 242)
    sh_danger.line.color.rgb = RGBColor(239, 68, 68)
    tb_d = s2.shapes.add_textbox(Mm(17), Mm(186), Mm(84), Mm(41))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    p = tf_d.paragraphs[0]
    rd_t = p.add_run()
    rd_t.text = "[제1우선 소외구역] 수요 극대, 공급 바닥\n"
    rd_t.font.bold = True
    rd_t.font.size = Pt(8.5)
    rd_t.font.color.rgb = RGBColor(185, 28, 28)
    rd_b = p.add_run()
    rd_b.text = (
        "가평군(0%), 연천군(0%), 여주시(0%), 동두천시(5.0%), 포천시(11.8%): 고령자·장애인 인구가 31~39%에 달하지만 저상버스는 전무합니다. "
        "이들 지역의 재정자립도는 14.7% ~ 25.8%로 최하위권입니다."
    )
    rd_b.font.size = Pt(7.8)
    rd_b.font.color.rgb = RGBColor(30, 41, 59)

    # Right Success Box
    sh_succ = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(107), Mm(184), Mm(88), Mm(45))
    sh_succ.fill.solid()
    sh_succ.fill.fore_color.rgb = RGBColor(240, 253, 244)
    sh_succ.line.color.rgb = RGBColor(34, 197, 94)
    tb_s = s2.shapes.add_textbox(Mm(109), Mm(186), Mm(84), Mm(41))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p = tf_s.paragraphs[0]
    rs_t = p.add_run()
    rs_t.text = "[자원 집중구역] 도심권 신도시\n"
    rs_t.font.bold = True
    rs_t.font.size = Pt(8.5)
    rs_t.font.color.rgb = RGBColor(21, 128, 61)
    rs_b = p.add_run()
    rs_b.text = (
        "하남시(63.9%), 광명시(62.7%), 부천시(59.6%), 수원시(52.7%): 교통약자 비율은 16.8% ~ 22.0% 수준이나, "
        "저상노선 비율은 52~64%에 달합니다. 재정자립도가 33~52%이며 평지 위주 인프라를 향유합니다."
    )
    rs_b.font.size = Pt(7.8)
    rs_b.font.color.rgb = RGBColor(30, 41, 59)

    # Callout Box OLS
    sh_call2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(15), Mm(233), Mm(180), Mm(45))
    sh_call2.fill.solid()
    sh_call2.fill.fore_color.rgb = RGBColor(241, 245, 249)
    sh_call2.line.color.rgb = RGBColor(2, 132, 199)
    tb_cb2 = s2.shapes.add_textbox(Mm(18), Mm(235), Mm(174), Mm(41))
    tf_cb2 = tb_cb2.text_frame
    tf_cb2.word_wrap = True
    tf_cb2.margin_left = tf_cb2.margin_right = tf_cb2.margin_top = tf_cb2.margin_bottom = 0
    p = tf_cb2.paragraphs[0]
    ro_t = p.add_run()
    ro_t.text = "재정자립도를 통제해도 교통약자 소외는 유지되는가? (다중회귀 OLS 분석)\n"
    ro_t.font.bold = True
    ro_t.font.size = Pt(8.5)
    ro_t.font.color.rgb = RGBColor(3, 105, 161)
    ro_b = p.add_run()
    ro_b.text = (
        "종속변수를 저상버스 노선 비율로 두고 재정자립도와 교통약자 비율을 동시 투입한 다중회귀분석 결과, "
        "재정자립도의 영향(β = +0.601, p = 0.0003)을 엄밀히 통제한 상태에서도 교통약자 비율의 회귀계수는 음(-)의 방향(β = -0.199, p = 0.178)을 유지했습니다. "
        "이는 지자체의 재정 여력만으로는 설명되지 않는 제도적·지형적 장벽이 취약지역에 복합적으로 작용하고 있음을 보여줍니다."
    )
    ro_b.font.size = Pt(8.0)
    ro_b.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # SLIDE 3 (본문 3/5): 실증 분석 원자료 상세 현황 표
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Part 2 (부록 표). 전국 및 경기도 기초지자체 전수 통계 데이터", "3/5")
    add_footer(s3, "31개 시·군 전체 원시 데이터는 GitHub 저장소 (`data/gyeonggi_master_analysis.csv`)에서 조회 가능합니다.", "본문 3 / 5")

    tb_s4 = s3.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(13))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True
    tf_s4.margin_left = tf_s4.margin_right = tf_s4.margin_top = tf_s4.margin_bottom = 0
    p = tf_s4.paragraphs[0]
    r = p.add_run()
    r.text = "4. 실증 분석 원자료 상세 현황 표 (전국 17개 시·도 및 경기도 31개 시·군)\n"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)
    p2 = tf_s4.add_paragraph()
    r2 = p2.add_run()
    r2.text = "※ 화면 및 본문에는 가독성을 위해 소수점 첫째자리 표기값을 적용하였으며, 저상버스 도입률 기준 내림차순 정렬되었습니다."
    r2.font.size = Pt(7.5)
    r2.font.color.rgb = RGBColor(100, 116, 139)

    # 17 Sido Table
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
    t1_rows = len(sido_data)
    t1_cols = 8
    tbl1 = s3.shapes.add_table(t1_rows, t1_cols, Mm(15), Mm(35), Mm(180), Mm(115)).table
    col_w1 = [Mm(26), Mm(22), Mm(22), Mm(22), Mm(22), Mm(22), Mm(22), Mm(22)]
    for ci, w in enumerate(col_w1):
        tbl1.columns[ci].width = w

    for ri, rvals in enumerate(sido_data):
        for ci, val in enumerate(rvals):
            c = tbl1.cell(ri, ci)
            c.text = val
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.runs[0].font.size = Pt(6.8)
            if ri == 0:
                p.runs[0].font.bold = True
                c.fill.solid()
                c.fill.fore_color.rgb = RGBColor(241, 245, 249)
            else:
                if ci == 0:
                    p.runs[0].font.bold = True
                if ci == 7:
                    p.runs[0].font.bold = True
                    if "우수" in val:
                        p.runs[0].font.color.rgb = RGBColor(29, 78, 216)
                    elif "취약" in val or "최하위" in val:
                        p.runs[0].font.color.rgb = RGBColor(185, 28, 28)

    # Gyeonggi Section Sub-heading
    tb_gsub = s3.shapes.add_textbox(Mm(15), Mm(155), Mm(180), Mm(6))
    p_gsub = tb_gsub.text_frame.paragraphs[0]
    rg = p_gsub.add_run()
    rg.text = "경기도 주요 기초지자체(저상버스 노선 비율 기준 내림차순 정렬)"
    rg.font.bold = True
    rg.font.size = Pt(8.8)
    rg.font.color.rgb = RGBColor(30, 41, 59)

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
    t2_rows = len(gg_data)
    tbl2 = s3.shapes.add_table(t2_rows, 8, Mm(15), Mm(163), Mm(180), Mm(115)).table
    col_w2 = [Mm(24), Mm(26), Mm(24), Mm(21), Mm(21), Mm(21), Mm(21), Mm(22)]
    for ci, w in enumerate(col_w2):
        tbl2.columns[ci].width = w

    for ri, rvals in enumerate(gg_data):
        for ci, val in enumerate(rvals):
            c = tbl2.cell(ri, ci)
            c.text = val
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.runs[0].font.size = Pt(6.8)
            if ri == 0:
                p.runs[0].font.bold = True
                c.fill.solid()
                c.fill.fore_color.rgb = RGBColor(241, 245, 249)
            else:
                if ci in (0, 1):
                    p.runs[0].font.bold = True
                if "자원 집중지" in rvals[7]:
                    c.fill.solid()
                    c.fill.fore_color.rgb = RGBColor(239, 246, 255)
                    if ci == 7:
                        p.runs[0].font.color.rgb = RGBColor(29, 78, 216)
                        p.runs[0].font.bold = True
                elif "제1우선 소외지" in rvals[7]:
                    c.fill.solid()
                    c.fill.fore_color.rgb = RGBColor(254, 242, 242)
                    if ci == 7:
                        p.runs[0].font.color.rgb = RGBColor(185, 28, 28)
                        p.runs[0].font.bold = True

    # =========================================================================
    # SLIDE 4 (본문 4/5): 구조적 원인 진단 (3대 설명 가설)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Part 3. 구조적 원인 진단: 왜 역진적 배정이 일어나는가? (해석 가설)", "4/5")
    add_footer(s4, "제도적 법령 근거: 「교통약자의 이동편의 증진법」 제14조 및 동법 시행령 제14조의2", "본문 4 / 5")

    tb_s5 = s4.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(15))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True
    tf_s5.margin_left = tf_s5.margin_right = tf_s5.margin_top = tf_s5.margin_bottom = 0
    p = tf_s5.paragraphs[0]
    r = p.add_run()
    r.text = "5. 구조적 설명 가설: 교통약자 밀집지에 저상버스가 적은 3대 메커니즘\n"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)
    p2 = tf_s5.add_paragraph()
    r2 = p2.add_run()
    r2.text = "※ 본 항목들은 통계 분석에서 규명된 공간적 격차를 제도적·운영적 맥락에서 해석하기 위해 도출한 '설명 가설'입니다."
    r2.font.size = Pt(8.0)
    r2.font.color.rgb = RGBColor(100, 116, 139)

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

    for i, (h_tag, h_title, h_body, h_match) in enumerate(hypotheses):
        hy = Mm(39 + i * 80)
        sh_h = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(15), hy, Mm(180), Mm(76))
        sh_h.fill.solid()
        sh_h.fill.fore_color.rgb = RGBColor(248, 250, 252)
        sh_h.line.color.rgb = RGBColor(203, 213, 225)
        
        tb_h = s4.shapes.add_textbox(Mm(18), hy + Mm(3), Mm(174), Mm(70))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        
        pt = tf_h.paragraphs[0]
        rt1 = pt.add_run()
        rt1.text = f"[{h_tag}] "
        rt1.font.bold = True
        rt1.font.size = Pt(10.5)
        rt1.font.color.rgb = RGBColor(2, 132, 199)
        rt2 = pt.add_run()
        rt2.text = h_title + "\n"
        rt2.font.bold = True
        rt2.font.size = Pt(9.5)
        rt2.font.color.rgb = RGBColor(15, 23, 42)
        
        pb = tf_h.add_paragraph()
        pb.space_before = Pt(3)
        rb = pb.add_run()
        rb.text = h_body + "\n"
        rb.font.size = Pt(8.0)
        rb.font.color.rgb = RGBColor(51, 65, 85)
        
        pm = tf_h.add_paragraph()
        pm.space_before = Pt(2)
        rm = pm.add_run()
        rm.text = h_match
        rm.font.bold = True
        rm.font.size = Pt(7.4)
        rm.font.color.rgb = RGBColor(3, 105, 161)

    # =========================================================================
    # SLIDE 5 (본문 5/5): 데이터 기반 정책 제언(안) 및 연구 한계
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Part 4 & 5. 데이터 기반 정책 제언(안) 및 연구의 한계", "5/5")
    add_footer(s5, "온라인 배포 링크: contest-lab.github.io/contest/ | GitHub: github.com/contest-lab/contest", "본문 5 / 5")

    tb_s6 = s5.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(15))
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True
    tf_s6.margin_left = tf_s6.margin_right = tf_s6.margin_top = tf_s6.margin_bottom = 0
    p = tf_s6.paragraphs[0]
    r = p.add_run()
    r.text = "6. 데이터 기반 3대 정책 제언(안): 역진성 극복 로드맵\n"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)
    p2 = tf_s6.add_paragraph()
    r2 = p2.add_run()
    r2.text = "단순 문제 제기에 그치지 않고, 본 실증 분석 결과를 바탕으로 교통약자 이동 형평성을 실질적으로 회복하기 위한 3단계 정책 대안을 제안합니다."
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(30, 41, 59)

    # 3 Policy Cards Vertical Layout (stacked)
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

    for i, (tag, p_title, p_desc, p_form) in enumerate(policies):
        py = Mm(38 + i * 44)
        sh_p = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(15), py, Mm(180), Mm(41))
        sh_p.fill.solid()
        sh_p.fill.fore_color.rgb = RGBColor(248, 250, 252)
        sh_p.line.color.rgb = RGBColor(203, 213, 225)
        
        tb_p = s5.shapes.add_textbox(Mm(18), py + Mm(2), Mm(174), Mm(37))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        
        p = tf_p.paragraphs[0]
        rt = p.add_run()
        rt.text = f"[{tag}] "
        rt.font.bold = True
        rt.font.size = Pt(7.5)
        rt.font.color.rgb = RGBColor(2, 132, 199)
        rh = p.add_run()
        rh.text = p_title + "\n"
        rh.font.bold = True
        rh.font.size = Pt(8.8)
        rh.font.color.rgb = RGBColor(15, 23, 42)
        
        pd = tf_p.add_paragraph()
        pd.space_before = Pt(2)
        rd = pd.add_run()
        rd.text = p_desc + "\n"
        rd.font.size = Pt(7.6)
        rd.font.color.rgb = RGBColor(51, 65, 85)
        
        pf = tf_p.add_paragraph()
        rf = pf.add_run()
        rf.text = p_form
        rf.font.bold = True
        rf.font.size = Pt(7.0)
        rf.font.color.rgb = RGBColor(3, 105, 161)

    # Limitations Heading & Box
    tb_s7 = s5.shapes.add_textbox(Mm(15), Mm(174), Mm(180), Mm(8))
    p = tb_s7.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "7. 본 분석의 방법론적 한계 및 향후 연구 과제"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)

    sh_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Mm(15), Mm(183), Mm(180), Mm(95))
    sh_l.fill.solid()
    sh_l.fill.fore_color.rgb = RGBColor(248, 250, 252)
    sh_l.line.color.rgb = RGBColor(203, 213, 225)
    
    tb_l = s5.shapes.add_textbox(Mm(18), Mm(186), Mm(174), Mm(89))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    
    limits = [
        ("횡단면 데이터의 한계", "본 연구는 2023년 시점의 데이터를 비교한 것으로, 통계적 관련성을 확인한 것이며 인과관계로 단정할 수는 없습니다."),
        ("교통약자 집계의 중복성", "'교통약자 비율'은 65세 이상 고령자와 등록장애인을 단순 합산하여 고령 장애인이 중복 집계되었을 가능성이 있습니다."),
        ("공급 지표 정의의 차이", "전국은 '저상버스 차량 대수 비율(%)'을, 경기도는 '저상버스 운행 노선 비율(%)'을 사용하여 상호 직접 비교 시 유의가 필요합니다."),
        ("소표본 지자체 해석 주의", "여주시의 경우 분석 노선 수가 2개(운행 노선 0개)로 표본 규모가 매우 작음에 유의해야 합니다."),
        ("우선순위 평가 모델의 탐색적 성격", "제안된 산식은 정책 대안으로서의 시뮬레이션 지표이며 실제 정책 적용 시 다속성 의사결정(AHP) 검증이 선행되어야 합니다.")
    ]
    for idx, (lt, ld) in enumerate(limits):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        if idx > 0:
            p.space_before = Pt(4)
        rlt = p.add_run()
        rlt.text = f"• {lt}: "
        rlt.font.bold = True
        rlt.font.size = Pt(8.0)
        rlt.font.color.rgb = RGBColor(15, 23, 42)
        rld = p.add_run()
        rld.text = ld
        rld.font.size = Pt(8.0)
        rld.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # SLIDE 6 (참고자료): 부록 및 참고문헌
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Appendix. 데이터 원천 출처 및 참고문헌", "참고자료")
    add_footer(s6, "본 보고서의 데이터는 KOSIS 및 국토교통부 실태조사 공인 원장을 기반으로 집계되었습니다.", "참고자료")

    tb_s8 = s6.shapes.add_textbox(Mm(15), Mm(21), Mm(180), Mm(10))
    p = tb_s8.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "8. 데이터 출처 및 참고문헌 (공식 원문 출처)"
    r.font.bold = True
    r.font.size = Pt(10.4)
    r.font.color.rgb = RGBColor(15, 23, 42)

    refs = [
        ("1. 국토교통부 · 한국교통안전공단 (2024.06)", "『2023년도 교통약자 이동편의 실태조사 연구보고서』 (전국 17개 시·도 저상버스 도입 대수, 노선버스 인가 대수 확정 통계)\n출처: TMACS 교통안전정보관리시스템 (tmacs.kotsa.or.kr) | 공공데이터포털"),
        ("2. 통계청 국가통계포털(KOSIS)", "시군구별 주민등록인구 및 고령인구비율 (2023년 말 기준, 통계표ID: DT_1YL20631)\n출처: KOSIS 국가통계포털 (kosis.kr)"),
        ("3. 보건복지부 · 통계청 KOSIS", "전국 시·군·구별 등록장애인수 현황 (2023년 말 기준, 통계표ID: DT_1YL202003E)\n출처: 보건복지통계연보 및 KOSIS 통계표"),
        ("4. 행정안전부 · 지방재정365", "전국 지방자치단체 재정자립도 및 재정자주도 결산 통계 (2023년 당초예산 기준, 통계표ID: DT_1YL20921)\n출처: 지방재정통합공개시스템 (lofin.mois.go.kr)"),
        ("5. 경기교통정보센터 · 경기데이터드림", "경기도 시·군별 시내버스 및 마을버스 인가 노선별 저상버스 운행정보 전수 원장 (6,431개 노선 전수, 2023년 12월 기준)\n출처: 경기데이터드림 (data.gg.go.kr)"),
        ("6. 대한민국 법령정보", "「교통약자의 이동편의 증진법」(법률 제18738호, 2023.01.19 시행) 제14조 및 동법 시행령 제14조의2\n출처: 국가법령정보센터 (law.go.kr)"),
        ("7. 국토교통부 고시 제2023-38호", "『저상버스 도입 예외 승인 기준에 관한 고시』")
    ]

    tb_ref = s6.shapes.add_textbox(Mm(15), Mm(32), Mm(180), Mm(160))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = tf_ref.margin_right = tf_ref.margin_top = tf_ref.margin_bottom = 0
    
    for idx, (rtit, rdesc) in enumerate(refs):
        p = tf_ref.paragraphs[0] if idx == 0 else tf_ref.add_paragraph()
        if idx > 0:
            p.space_before = Pt(6)
        rt = p.add_run()
        rt.text = rtit + "\n"
        rt.font.bold = True
        rt.font.size = Pt(8.3)
        rt.font.color.rgb = RGBColor(15, 23, 42)
        
        rd = p.add_run()
        rd.text = rdesc
        rd.font.size = Pt(7.6)
        rd.font.color.rgb = RGBColor(71, 85, 105)

    # Verification Box
    sh_rep = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(15), Mm(205), Mm(180), Mm(68))
    sh_rep.fill.solid()
    sh_rep.fill.fore_color.rgb = RGBColor(241, 245, 249)
    sh_rep.line.color.rgb = RGBColor(2, 132, 199)
    
    tb_rep = s6.shapes.add_textbox(Mm(18), Mm(208), Mm(174), Mm(62))
    tf_rep = tb_rep.text_frame
    tf_rep.word_wrap = True
    tf_rep.margin_left = tf_rep.margin_right = tf_rep.margin_top = tf_rep.margin_bottom = 0
    
    p = tf_rep.paragraphs[0]
    rt = p.add_run()
    rt.text = "온라인 검증 및 재현성 안내\n"
    rt.font.bold = True
    rt.font.size = Pt(9.0)
    rt.font.color.rgb = RGBColor(3, 105, 161)
    
    rb = p.add_run()
    rb.text = (
        "본 보고서에 수록된 모든 분석 코드(Jupyter Notebook, Python 스크립트) 및 시각화 생성 스크립트는 오픈 소스로 완전 공개되어 있습니다. "
        "아래 저장소에서 원본 데이터와 소스코드를 내려받아 동일한 결과를 100% 재현할 수 있습니다.\n\n"
        "• 분석 코드 GitHub 저장소: https://github.com/contest-lab/contest\n"
        "• 웹 인터랙티브 보고서: https://contest-lab.github.io/contest/"
    )
    rb.font.size = Pt(8.2)
    rb.font.color.rgb = RGBColor(30, 41, 59)

    out_path = "c:/Users/hani/Desktop/antigravity/contest/results/contest_report_editable.pptx"
    prs.save(out_path)
    print(f"[SUCCESS] Saved A4 Portrait editable pptx to {out_path}")

if __name__ == "__main__":
    build_a4_portrait_pptx()
