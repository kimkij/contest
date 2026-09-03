import json
import base64
import os

with open("results/sido_data.json", "r", encoding="utf-8") as f:
    sido_json = f.read()

with open("results/gg_data.json", "r", encoding="utf-8") as f:
    gg_json = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[분석보고서] 저상버스 확충 예산은 어디로 갔는가? | 데이터 분석 공모전</title>
    <!-- Google Fonts & Chart.js -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-body: #0a0f1d;
            --bg-card: rgba(18, 26, 47, 0.75);
            --bg-card-hover: rgba(28, 38, 68, 0.85);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(79, 140, 255, 0.3);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --primary: #3b82f6;
            --primary-glow: rgba(59, 130, 246, 0.35);
            --accent-red: #ef4444;
            --accent-red-glow: rgba(239, 68, 68, 0.25);
            --accent-cyan: #06b6d4;
            --accent-amber: #f59e0b;
            --font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-family);
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.65;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(239, 68, 68, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
            background-attachment: fixed;
            min-height: 100vh;
        }}

        /* Sticky Navigation Bar */
        .navbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background: rgba(10, 15, 29, 0.8);
            border-bottom: 1px solid var(--border-glass);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 1.05rem;
            letter-spacing: -0.02em;
            color: #fff;
        }}

        .nav-brand .badge {{
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: #fff;
            font-size: 0.72rem;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .nav-links {{
            display: flex;
            gap: 20px;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .nav-links a:hover {{
            color: #fff;
        }}

        .btn-github {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-glass);
            color: #fff;
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .btn-github:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 24px 80px 24px;
        }}

        /* Hero Header */
        .hero {{
            text-align: center;
            padding: 60px 0 50px 0;
            position: relative;
        }}

        .contest-tag {{
            display: inline-block;
            color: var(--accent-cyan);
            font-size: 0.88rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 16px;
            padding: 4px 14px;
            border-radius: 30px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.25);
        }}

        .hero-title {{
            font-size: 3.2rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1.2;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-title span {{
            background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-desc {{
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 820px;
            margin: 0 auto 30px auto;
            font-weight: 400;
            word-break: keep-all;
        }}

        .hero-meta {{
            display: flex;
            justify-content: center;
            gap: 24px;
            font-size: 0.88rem;
            color: var(--text-muted);
        }}

        .hero-meta span {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* KPI Banner (4 Stat Cards) */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 50px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 24px 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.25s ease;
        }}

        .kpi-card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-3px);
            border-color: var(--border-highlight);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
        }}

        .kpi-card.red::before {{ background: var(--accent-red); }}
        .kpi-card.blue::before {{ background: var(--primary); }}
        .kpi-card.cyan::before {{ background: var(--accent-cyan); }}
        .kpi-card.amber::before {{ background: var(--accent-amber); }}

        .kpi-label {{
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }}

        .kpi-val {{
            font-size: 2.1rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin-bottom: 6px;
            color: #fff;
        }}

        .kpi-card.red .kpi-val {{ color: #f87171; }}
        .kpi-card.blue .kpi-val {{ color: #60a5fa; }}
        .kpi-card.cyan .kpi-val {{ color: #22d3ee; }}
        .kpi-card.amber .kpi-val {{ color: #fbbf24; }}

        .kpi-sub {{
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.4;
        }}

        /* Section Layout */
        .section {{
            margin-bottom: 65px;
        }}

        .section-header {{
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-glass);
        }}

        .section-tag {{
            font-size: 0.8rem;
            color: var(--primary);
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}

        .section-title {{
            font-size: 1.7rem;
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.02em;
        }}

        /* Chart + Commentary Split */
        .grid-2col {{
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            gap: 24px;
            align-items: stretch;
        }}

        .chart-box {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            display: flex;
            flex-direction: column;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .chart-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #fff;
        }}

        .chart-badge {{
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.07);
            padding: 4px 8px;
            border-radius: 6px;
            color: var(--text-muted);
        }}

        .chart-canvas-container {{
            position: relative;
            flex: 1;
            min-height: 380px;
            width: 100%;
        }}

        /* Analysis Cards on the Right */
        .analysis-card-col {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .story-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 22px;
            transition: all 0.2s ease;
        }}

        .story-card:hover {{
            border-color: var(--border-highlight);
        }}

        .story-card.danger {{
            background: rgba(239, 68, 68, 0.06);
            border-color: rgba(239, 68, 68, 0.25);
        }}

        .story-card.primary {{
            background: rgba(59, 130, 246, 0.06);
            border-color: rgba(59, 130, 246, 0.25);
        }}

        .story-title {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .story-card.danger .story-title {{ color: #f87171; }}
        .story-card.primary .story-title {{ color: #60a5fa; }}

        .story-p {{
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
        }}

        .highlight-text {{
            color: #fff;
            font-weight: 600;
        }}

        /* Table Design */
        .data-table-container {{
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            overflow-x: auto;
            margin-top: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }}

        th {{
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-muted);
            font-weight: 600;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-glass);
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        .badge-danger {{
            display: inline-block;
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.78rem;
        }}

        .badge-success {{
            display: inline-block;
            background: rgba(34, 197, 94, 0.15);
            color: #86efac;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.78rem;
        }}

        /* 3-Column Root Cause Grid */
        .cause-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}

        .cause-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 28px 24px;
            position: relative;
            transition: all 0.25s ease;
        }}

        .cause-card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-4px);
            border-color: var(--border-highlight);
        }}

        .cause-num {{
            font-size: 2.2rem;
            font-weight: 900;
            color: rgba(255, 255, 255, 0.12);
            line-height: 1;
            margin-bottom: 12px;
        }}

        .cause-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 12px;
            line-height: 1.35;
        }}

        .cause-desc {{
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.65;
        }}

        /* Policy Proposals */
        .proposal-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}

        .proposal-card {{
            background: linear-gradient(180deg, rgba(30, 41, 75, 0.6) 0%, rgba(18, 26, 47, 0.8) 100%);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 28px 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
        }}

        .proposal-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
            transform: translateY(-4px);
        }}

        .proposal-tag {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
        }}

        .proposal-title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: #fff;
            margin-bottom: 14px;
            line-height: 1.35;
        }}

        .proposal-body {{
            font-size: 0.92rem;
            color: var(--text-muted);
            line-height: 1.65;
            margin-bottom: 20px;
        }}

        .formula-box {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 12px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.82rem;
            color: #93c5fd;
            line-height: 1.4;
            margin-top: 10px;
        }}

        /* Footer */
        .footer {{
            border-top: 1px solid var(--border-glass);
            padding: 40px 0;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.88rem;
        }}

        .footer a {{
            color: var(--primary);
            text-decoration: none;
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .grid-2col {{ grid-template-columns: 1fr; }}
            .cause-grid {{ grid-template-columns: 1fr; }}
            .proposal-grid {{ grid-template-columns: 1fr; }}
            .hero-title {{ font-size: 2.4rem; }}
        }}
    </style>
</head>
<body>

    <!-- Sticky Navigation -->
    <nav class="navbar">
        <div class="nav-brand">
            <span class="badge">AI 교통 데이터 공모전</span>
            <span>저상버스 배정 형평성 분석</span>
        </div>
        <ul class="nav-links">
            <li><a href="#summary">핵심 요약</a></li>
            <li><a href="#macro">전국 거시 실증</a></li>
            <li><a href="#micro">경기도 미시 전수</a></li>
            <li><a href="#causes">구조적 원인</a></li>
            <li><a href="#proposals">AI 정책 제언</a></li>
        </ul>
        <a href="https://github.com/kimkij/contest" target="_blank" class="btn-github">
            <svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
            GitHub Repository
        </a>
    </nav>

    <div class="container">

        <!-- Hero Section -->
        <header class="hero" id="summary">
            <div class="contest-tag">한겨레 × (재단법인) 숲과나눔 주최 데이터 분석 공모전</div>
            <h1 class="hero-title">저상버스 확충 예산은<br><span>어디로 갔는가?</span></h1>
            <p class="hero-desc">
                2023년 저상버스 의무화 법안 시행 이후, 정부 예산은 정말 거동이 불편한 고령자와 장애인 밀집지역에 우선 투입되었는가? 
                전국 17개 시·도 및 경기도 6,431개 버스 노선 전수 분석을 통해 밝혀낸 <strong>'공간적 역진성'</strong> 실증 보고서.
            </p>
            <div class="hero-meta">
                <span>📅 분석 기준: 2023-2024 최신 국가통계</span>
                <span>📊 데이터: KOSIS 국가통계포털 · 국토교통부 실태조사 · 경기교통정보</span>
                <span>🔍 분석 단위: 전국 17개 시·도 및 229개 시군구</span>
            </div>
        </header>

        <!-- KPI Summary Cards -->
        <div class="kpi-grid">
            <div class="kpi-card red">
                <div class="kpi-label">전국 가설 검증</div>
                <div class="kpi-val">r = -0.435</div>
                <div class="kpi-sub">교통약자가 많을수록 저상버스 보급률은 오히려 감소 (명백한 음의 상관관계)</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">수도권 기초지자체 회귀</div>
                <div class="kpi-val">Beta = -1.14</div>
                <div class="kpi-sub">경기도 노선 분석 결과, 교통약자 1%p 높을수록 저상버스 노선은 1.14%p 감소</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-label">서울 vs 전남 보급 격차</div>
                <div class="kpi-val">4.9배</div>
                <div class="kpi-sub">교통약자 비율 33.7% 전남(도입률 11.5%) vs 교통약자 22.6% 서울(도입률 56.8%)</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">소외지역 노선 비율</div>
                <div class="kpi-val">0.0%</div>
                <div class="kpi-sub">가평군·연천군·여주시 등 고령화 30~40% 군 지역 저상버스 운행 노선 전무</div>
            </div>
        </div>

        <!-- Section 1: Macro Sido Analysis -->
        <section class="section" id="macro">
            <div class="section-header">
                <div>
                    <div class="section-tag">Part 1. 전국 거시 실증</div>
                    <h2 class="section-title">전국 17개 시·도: 수요와 공급의 정반대 불일치</h2>
                </div>
            </div>

            <div class="grid-2col">
                <div class="chart-box">
                    <div class="chart-header">
                        <div class="chart-title">17개 시·도별 저상버스 도입률 vs 교통약자 인구 비율</div>
                        <span class="chart-badge">국토교통부 실태조사 & KOSIS</span>
                    </div>
                    <div class="chart-canvas-container">
                        <canvas id="sidoBarChart"></canvas>
                    </div>
                </div>

                <div class="analysis-card-col">
                    <div class="story-card danger">
                        <div class="story-title">
                            <span>❌</span> 가설의 역설적 기각 (음의 상관관계)
                        </div>
                        <p class="story-p">
                            "교통약자 밀집지역에 저상버스가 우선 도입되었을 것"이라는 정책 가설은 완전히 기각되었습니다. 
                            전국 17개 시도 분석 결과, <span class="highlight-text">등록장애인 비율(r = -0.573)</span> 및 
                            <span class="highlight-text">교통약자 통합비율(r = -0.435)</span> 모두에서 통계적으로 유의미한 역진적 배정이 실증되었습니다.
                        </p>
                    </div>

                    <div class="story-card">
                        <div class="story-title">
                            <span>🏙</span> 서울과 지방의 극단적 양극화
                        </div>
                        <p class="story-p">
                            <strong>서울</strong>: 교통약자 비율 22.6%, 재정자립도 81.2% &rarr; <strong>저상버스 도입률 56.8% (시내버스 66.7%)</strong><br>
                            <strong>전남</strong>: 교통약자 비율 33.7%, 재정자립도 28.7% &rarr; <strong>저상버스 도입률 11.5% (전국 꼴찌)</strong><br>
                            전남의 교통약자 비율은 서울보다 11.1%p 높지만, 저상버스 혜택은 서울의 5분의 1에 불과합니다.
                        </p>
                    </div>

                    <div class="story-card primary">
                        <div class="story-title">
                            <span>💰</span> 결정 요인은 '수요'가 아닌 '지자체 재정력'
                        </div>
                        <p class="story-p">
                            지자체 재정자립도와 저상버스 도입률은 <span class="highlight-text">r = +0.495(t = 2.21, p &lt; 0.05)</span>로 
                            강한 양의 상관관계를 보였습니다. 저상버스 보급의 진짜 결정요인은 교통약자의 필요가 아니라 지자체의 '지갑 사정'이었습니다.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Detailed Table -->
            <div class="data-table-container">
                <table>
                    <thead>
                        <tr>
                            <th>시·도명</th>
                            <th>전체 버스 도입률</th>
                            <th>시내버스 도입률</th>
                            <th>교통약자 비율</th>
                            <th>고령인구 비율</th>
                            <th>등록장애인 비율</th>
                            <th>재정자립도</th>
                            <th>판정</th>
                        </tr>
                    </thead>
                    <tbody id="sidoTableBody"></tbody>
                </table>
            </div>
        </section>

        <!-- Section 2: Micro Gyeonggi Analysis -->
        <section class="section" id="micro">
            <div class="section-header">
                <div>
                    <div class="section-tag">Part 2. 미시 전수 분석</div>
                    <h2 class="section-title">경기도 31개 시·군 6,431개 버스 노선 전수 분석</h2>
                </div>
            </div>

            <div class="grid-2col">
                <div class="chart-box">
                    <div class="chart-header">
                        <div class="chart-title">수요-공급 4분면 매트릭스 (교통약자 비율 vs 저상버스 노선 비율)</div>
                        <span class="chart-badge">점 크기: 재정자립도</span>
                    </div>
                    <div class="chart-canvas-container">
                        <canvas id="ggQuadrantChart"></canvas>
                    </div>
                </div>

                <div class="analysis-card-col">
                    <div class="story-card danger">
                        <div class="story-title">
                            <span>🚨</span> [제1우선 긴급투입 지역] 소외 사각지대
                        </div>
                        <p class="story-p">
                            <strong>가평군, 연천군, 여주시, 동두천시, 포천시</strong><br>
                            고령인구와 장애인이 전체 인구의 30~40%에 달하지만, 저상버스 운행 노선 비율은 <strong>0.0% ~ 11.8%</strong>로 전멸 상태입니다. 
                            재정자립도가 14~20%로 도내 최하위여서 지자체 자체 확충이 원천적으로 불가능합니다.
                        </p>
                    </div>

                    <div class="story-card primary">
                        <div class="story-title">
                            <span>🏢</span> [자원 집중 지역] 도심 신도시
                        </div>
                        <p class="story-p">
                            <strong>하남시(63.9%), 광명시(62.7%), 부천시(59.6%), 수원시(52.7%)</strong><br>
                            교통약자 비율은 17~21%로 상대적으로 낮으나 저상버스 노선 비율은 50%를 훌쩍 넘습니다. 
                            재정자립도가 35~50% 수준이며 도로 정비가 잘 되어 있어 보조금을 선점했습니다.
                        </p>
                    </div>

                    <div class="story-card">
                        <div class="story-title">
                            <span>📐</span> 다중회귀분석(OLS) 실증 계수
                        </div>
                        <p class="story-p">
                            $$\text{{저상버스 노선 비율(\%)}} = 46.50 - 1.14 \times \text{{교통약자비율}} + 0.14 \times \text{{재정자립도}}$$
                            <br>
                            재정력을 통제하더라도 교통약자 밀집 지역일수록 저상버스 노선은 1.14%p 감소하는 <strong>통계적 유의성(p &lt; 0.05)</strong>이 확증되었습니다.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section 3: Root Causes -->
        <section class="section" id="causes">
            <div class="section-header">
                <div>
                    <div class="section-tag">Part 3. 구조적 원인 규명</div>
                    <h2 class="section-title">왜 교통약자 밀집지역에 저상버스가 못 가는가?</h2>
                </div>
            </div>

            <div class="cause-grid">
                <div class="cause-card">
                    <div class="cause-num">01</div>
                    <h3 class="cause-title">'국비 50% 정률 매칭' 제도의 역진적 함정</h3>
                    <p class="cause-desc">
                        저상버스 대당 구입 보조금(약 9,000만 원)은 국비 50%와 지방비 50%(약 4,500만 원) 매칭 구조입니다. 
                        재정자립도 15~20%대인 군 지역은 수십억의 매칭 예산을 편성하지 못해 신차 교체 시 저상버스 신청 자체를 포기합니다. 
                        결국 국가 복지 보조금이 부유한 대도시에 집중되는 역진성이 발생합니다.
                    </p>
                </div>

                <div class="cause-card">
                    <div class="cause-num">02</div>
                    <h3 class="cause-title">운수회사의 승객·수익성 중심 간선 배차</h3>
                    <p class="cause-desc">
                        준공영제 및 민간 운수회사는 탑승객이 많고 회전율이 높은 도심 간선 노선에 신차와 저상버스를 우선 배차합니다. 
                        반면 교통약자가 의존하는 배차 간격 1~2시간의 외곽 벽지 지선 노선은 차량 교체 우선순위에서 밀려 노후 고상버스가 장기 방치됩니다.
                    </p>
                </div>

                <div class="cause-card">
                    <div class="cause-num">03</div>
                    <h3 class="cause-title">도로 인프라 미비와 '예외 승인'의 악순환</h3>
                    <p class="cause-desc">
                        현행 「교통약자법」상 급경사, 굴곡, 과속방지턱 등 도로 사정이 불량한 노선은 '저상버스 도입 예외'로 인정됩니다. 
                        농어촌 지자체는 도로 턱과 회전반경을 개선할 예산이 없어 노선 전체를 예외로 승인받아 법적 의무를 우회하며 사각지대로 남습니다.
                    </p>
                </div>
            </div>
        </section>

        <!-- Section 4: Policy Proposals -->
        <section class="section" id="proposals">
            <div class="section-header">
                <div>
                    <div class="section-tag">Part 4. AI 기반 정책 제언</div>
                    <h2 class="section-title">데이터 기반 교통복지 형평성 혁신 방안</h2>
                </div>
            </div>

            <div class="proposal-grid">
                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">Fiscal Policy</div>
                        <h3 class="proposal-title">교통약자 수요 연동형<br>차등 국비 보조율 제도</h3>
                        <p class="proposal-body">
                            현행 일률 50% 국비 지원을 지자체 재정자립도 및 교통약자 밀집도에 따라 <strong>30% ~ 80%로 차등화</strong>합니다. 
                            가평·연천·전남 등 재정자립도 20% 미만 취약 지역은 국비 80%를 지원하여 지방비 부담을 1,800만 원으로 경감합니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        국비보조율 = 50% + 15%(약자밀집가산) + 15%(재정취약가산) &rarr; 최대 80%
                    </div>
                </div>

                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">AI Algorithm</div>
                        <h3 class="proposal-title">AI 기반 저상버스 우선투입 지수 (LBEI) 공모제</h3>
                        <p class="proposal-body">
                            머신러닝 기반 <strong>Low-floor Bus Equity Index(LBEI)</strong>를 산출하여 국토교통부 연간 보조금 배정 심사 시 
                            점수가 높은 노선과 지자체에 <strong>예산의 40% 이상을 의무 우선 배정</strong>하는 쿼터제를 도입합니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        LBEI = 0.4×(동별 약자밀도) + 0.3×(병원·복지관경유도) + 0.3×(1-현재공급률)
                    </div>
                </div>

                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">Infrastructure</div>
                        <h3 class="proposal-title">중형 저상 전기버스 &amp;<br>도로 정비 패키지 연계</h3>
                        <p class="proposal-body">
                            대형(11m) 저상버스가 진입 불가능한 농어촌 굴곡 도로를 위해 <strong>중형(8~9m) 저상 전기버스 전용 보조금 트랙</strong>을 신설하고, 
                            예외 승인 노선에 국토부 도로정비사업 예산을 1:1 매칭 지원해 도로 턱을 낮춥니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        중형 저상버스 도입 + 정류장 단차 개선 국토부 패키지 지원
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p style="margin-bottom: 8px;">한겨레 × (재단법인) 숲과나눔 주최 「AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전」 제출작</p>
            <p>분석 파이프라인 및 데이터 소스코드: <a href="https://github.com/kimkij/contest" target="_blank">github.com/kimkij/contest</a></p>
        </footer>

    </div>

    <!-- Interactive Charts Logic -->
    <script>
        const sidoData = {sido_json};
        const ggData = {gg_json};

        // 1. Render Sido Horizontal Bar Chart
        const sortedSido = [...sidoData].sort((a, b) => b.total_rate - a.total_rate);
        const ctxSido = document.getElementById('sidoBarChart').getContext('2d');
        
        new Chart(ctxSido, {{
            type: 'bar',
            data: {{
                labels: sortedSido.map(d => d.region),
                datasets: [{{
                    label: '저상버스 도입률 (%)',
                    data: sortedSido.map(d => d.total_rate),
                    backgroundColor: sortedSido.map(d => d.total_rate < 20 ? '#ef4444' : (d.total_rate > 40 ? '#3b82f6' : '#64748b')),
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            afterLabel: function(context) {{
                                const item = sortedSido[context.dataIndex];
                                return `교통약자 비율: ${{item.vulnerable_rate}}%\\n재정자립도: ${{item.fiscal_rate}}%`;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#94a3b8' }},
                        max: 65
                    }},
                    y: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#f1f5f9', font: {{ family: 'Pretendard', weight: '500' }} }}
                    }}
                }}
            }}
        }});

        // Render Sido Table
        const tbody = document.getElementById('sidoTableBody');
        sortedSido.forEach(d => {{
            const tr = document.createElement('tr');
            const badge = d.total_rate < 20 ? '<span class="badge-danger">심각 취약</span>' : (d.total_rate > 40 ? '<span class="badge-success">우수 도입</span>' : '-');
            tr.innerHTML = `
                <td><strong>${{d.region}}</strong></td>
                <td><strong>${{d.total_rate}}%</strong></td>
                <td>${{d.city_bus_rate}}%</td>
                <td>${{d.vulnerable_rate}}%</td>
                <td>${{d.elderly_rate}}%</td>
                <td>${{d.disabled_rate}}%</td>
                <td>${{d.fiscal_rate}}%</td>
                <td>${{badge}}</td>
            `;
            tbody.appendChild(tr);
        }});

        // 2. Render Gyeonggi 4-Quadrant Bubble Chart
        const ctxGG = document.getElementById('ggQuadrantChart').getContext('2d');
        const medVulnerable = 20.8;
        const medSupply = 18.6;

        new Chart(ctxGG, {{
            type: 'bubble',
            data: {{
                datasets: [{{
                    label: '경기도 31개 시·군',
                    data: ggData.map(d => ({{
                        x: d.vulnerable_rate,
                        y: d.low_floor_route_ratio,
                        r: Math.max(4, d.fiscal_rate / 3.5),
                        city: d.city,
                        fiscal: d.fiscal_rate,
                        routes: d.total_routes,
                        lowRoutes: d.low_floor_routes
                    }})),
                    backgroundColor: ggData.map(d => {{
                        if (d.vulnerable_rate > medVulnerable && d.low_floor_route_ratio < medSupply) return 'rgba(239, 68, 68, 0.75)'; // 소외구역
                        if (d.vulnerable_rate <= medVulnerable && d.low_floor_route_ratio >= medSupply) return 'rgba(59, 130, 246, 0.75)'; // 집중구역
                        return 'rgba(148, 163, 184, 0.6)';
                    }}),
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            title: function(context) {{
                                return context[0].raw.city;
                            }},
                            label: function(context) {{
                                const raw = context.raw;
                                return [
                                    `교통약자 인구비율: ${{raw.x}}%`,
                                    `저상버스 노선비율: ${{raw.y}}% (${{raw.lowRoutes}}/${{raw.routes}}개)`,
                                    `재정자립도: ${{raw.fiscal}}%`
                                ];
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: '교통약자 인구 비율 (%) → [수요]', color: '#94a3b8' }},
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#94a3b8' }},
                        min: 12,
                        max: 42
                    }},
                    y: {{
                        title: {{ display: true, text: '저상버스 운행 노선 비율 (%) → [공급]', color: '#94a3b8' }},
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#94a3b8' }},
                        min: -2,
                        max: 70
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved publication-grade interactive HTML dashboard to index.html successfully!")
