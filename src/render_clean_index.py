import json

with open("results/sido_data.json", "r", encoding="utf-8") as f:
    sido_json = f.read()

with open("results/gg_data.json", "r", encoding="utf-8") as f:
    gg_json = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[분석보고서] 교통약자가 많은 지역에 저상버스가 더 많이 다니고 있는가? | 데이터 분석 공모전</title>
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

        /* Responsive Navigation Bar with Hamburger Menu */
        .navbar {{
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background: rgba(10, 15, 29, 0.88);
            border-bottom: 1px solid var(--border-glass);
            padding: 12px 24px;
        }}

        .nav-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 800;
            font-size: 1.0rem;
            color: #fff;
            text-decoration: none;
        }}

        .nav-brand .badge {{
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: #fff;
            font-size: 0.72rem;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
        }}

        .nav-menu {{
            display: flex;
            align-items: center;
            gap: 20px;
            list-style: none;
        }}

        .nav-menu a {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .nav-menu a:hover {{
            color: #fff;
        }}

        .nav-actions {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .btn-code {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid var(--border-glass);
            color: #e2e8f0;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .btn-code:hover {{
            background: rgba(255, 255, 255, 0.14);
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-1px);
        }}

        .btn-code.primary {{
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.35);
            color: #93c5fd;
        }}

        .btn-code.primary:hover {{
            background: rgba(59, 130, 246, 0.25);
            color: #bfdbfe;
        }}

        /* Mobile Hamburger Toggle */
        .nav-toggle {{
            display: none;
            background: none;
            border: none;
            color: #fff;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 4px;
        }}

        .mobile-only {{
            display: none;
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px 80px 20px;
        }}

        /* Hero Header */
        .hero {{
            text-align: center;
            padding: 50px 0 45px 0;
        }}

        .contest-tag {{
            display: inline-block;
            color: var(--accent-cyan);
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 14px;
            padding: 4px 14px;
            border-radius: 30px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.25);
        }}

        .hero-title {{
            font-size: 2.8rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1.25;
            margin-bottom: 20px;
            color: #fff;
        }}

        .hero-title span {{
            background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-desc {{
            font-size: 1.15rem;
            color: var(--text-muted);
            max-width: 860px;
            margin: 0 auto 26px auto;
            word-break: keep-all;
            line-height: 1.7;
        }}

        .hero-meta {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 0.84rem;
            color: var(--text-muted);
        }}

        .hero-meta span {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-glass);
            padding: 5px 12px;
            border-radius: 20px;
        }}

        /* Notice / Methodology Box */
        .notice-box {{
            background: rgba(59, 130, 246, 0.06);
            border: 1px solid rgba(59, 130, 246, 0.25);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 35px;
            font-size: 0.88rem;
            color: #cbd5e1;
            line-height: 1.6;
        }}

        .notice-box strong {{
            color: #93c5fd;
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
            padding: 22px 18px;
            position: relative;
            overflow: hidden;
            transition: all 0.25s ease;
        }}

        .kpi-card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-2px);
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
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}

        .kpi-val {{
            font-size: 2.0rem;
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
            line-height: 1.45;
        }}

        /* Section Layout */
        .section {{
            margin-bottom: 65px;
        }}

        .section-header {{
            margin-bottom: 22px;
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
            font-size: 1.65rem;
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.02em;
        }}

        /* Grid 2 Column */
        .grid-2col {{
            display: grid;
            grid-template-columns: 1.35fr 1fr;
            gap: 24px;
            align-items: stretch;
        }}

        .chart-box {{
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 22px;
            display: flex;
            flex-direction: column;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .chart-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #fff;
        }}

        .chart-subtitle {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 2px;
        }}

        .chart-legend-box {{
            display: flex;
            gap: 12px;
            font-size: 0.78rem;
            color: #cbd5e1;
            margin-bottom: 12px;
            flex-wrap: wrap;
            background: rgba(0, 0, 0, 0.25);
            padding: 8px 12px;
            border-radius: 8px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }}

        .chart-canvas-container {{
            position: relative;
            flex: 1;
            min-height: 420px;
            width: 100%;
        }}

        /* Fallback alert if Chart.js fails */
        .chart-fallback {{
            display: none;
            padding: 20px;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            color: #fca5a5;
            font-size: 0.9rem;
        }}

        /* Commentary Cards */
        .analysis-card-col {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .story-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 20px;
            transition: all 0.2s ease;
        }}

        .story-card:hover {{
            border-color: var(--border-highlight);
        }}

        .story-card.danger {{
            background: rgba(239, 68, 68, 0.05);
            border-color: rgba(239, 68, 68, 0.22);
        }}

        .story-card.primary {{
            background: rgba(59, 130, 246, 0.05);
            border-color: rgba(59, 130, 246, 0.22);
        }}

        .story-title {{
            font-size: 1.0rem;
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
            font-size: 0.88rem;
            color: var(--text-muted);
            line-height: 1.65;
        }}

        .stat-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 0.8rem;
            color: #e2e8f0;
            font-family: monospace;
        }}

        /* Clean Regression Code Block Box */
        .math-code-box {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            padding: 12px 14px;
            margin: 10px 0;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.84rem;
            color: #93c5fd;
            line-height: 1.5;
        }}

        /* Table Design with Sticky First Column */
        .table-wrap {{
            margin-top: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            overflow: hidden;
        }}

        .table-scroll {{
            overflow-x: auto;
            max-height: 480px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            text-align: left;
            white-space: nowrap;
        }}

        th {{
            background: #151f38;
            color: var(--text-muted);
            font-weight: 600;
            padding: 10px 14px;
            border-bottom: 1px solid var(--border-glass);
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        td {{
            padding: 9px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
        }}

        /* Sticky first column */
        th.sticky-col, td.sticky-col {{
            position: sticky;
            left: 0;
            background: #111a30;
            z-index: 5;
            font-weight: 600;
            border-right: 1px solid var(--border-glass);
        }}

        th.sticky-col {{
            z-index: 15;
            background: #17233f;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.03);
        }}

        .badge-danger {{
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.75rem;
        }}

        .badge-success {{
            background: rgba(34, 197, 94, 0.15);
            color: #86efac;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.75rem;
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
            padding: 26px 22px;
            transition: all 0.25s ease;
        }}

        .cause-card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-3px);
            border-color: var(--border-highlight);
        }}

        .cause-num {{
            font-size: 2.0rem;
            font-weight: 900;
            color: rgba(255, 255, 255, 0.12);
            line-height: 1;
            margin-bottom: 12px;
        }}

        .cause-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
            line-height: 1.35;
        }}

        .cause-desc {{
            font-size: 0.88rem;
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
            padding: 26px 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
        }}

        .proposal-card:hover {{
            border-color: var(--primary);
            transform: translateY(-3px);
        }}

        .proposal-tag {{
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }}

        .proposal-title {{
            font-size: 1.2rem;
            font-weight: 800;
            color: #fff;
            margin-bottom: 12px;
            line-height: 1.35;
        }}

        .proposal-body {{
            font-size: 0.88rem;
            color: var(--text-muted);
            line-height: 1.65;
            margin-bottom: 18px;
        }}

        .formula-box {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px 12px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.8rem;
            color: #93c5fd;
            line-height: 1.45;
        }}

        /* Limitations Box */
        .limitations-box {{
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 24px;
            margin-top: 40px;
        }}

        .limitations-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #cbd5e1;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .limitations-list {{
            padding-left: 20px;
            font-size: 0.86rem;
            color: var(--text-muted);
            line-height: 1.7;
        }}

        .limitations-list li {{
            margin-bottom: 6px;
        }}

        /* Footer */
        .footer {{
            border-top: 1px solid var(--border-glass);
            padding: 40px 0;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.86rem;
            line-height: 1.8;
        }}

        .footer a {{
            color: var(--primary);
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        /* Responsive Breakpoints */
        @media (max-width: 960px) {{
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .grid-2col {{ grid-template-columns: 1fr; }}
            .cause-grid {{ grid-template-columns: 1fr; }}
            .proposal-grid {{ grid-template-columns: 1fr; }}
            .hero-title {{ font-size: 2.2rem; }}
            
            .nav-menu {{
                display: none;
                flex-direction: column;
                position: absolute;
                top: 100%;
                left: 0;
                width: 100%;
                background: #0d1527;
                padding: 20px;
                border-bottom: 1px solid var(--border-glass);
                gap: 15px;
            }}
            .nav-menu.open {{
                display: flex;
            }}
            .nav-toggle {{
                display: block;
            }}
            .nav-actions {{
                display: none;
            }}
            .mobile-only {{
                display: block;
            }}
        }}

        @media (max-width: 600px) {{
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .hero-title {{ font-size: 1.85rem; }}
            .chart-canvas-container {{ min-height: 340px; }}
        }}
    </style>
</head>
<body>

    <!-- Sticky Navigation Bar -->
    <nav class="navbar">
        <div class="nav-inner">
            <a href="#" class="nav-brand">
                <span class="badge">AI 교통 데이터 공모전</span>
                <span>교통약자 이동권 실증 분석</span>
            </a>

            <ul class="nav-menu" id="navMenu">
                <li><a href="#macro" onclick="closeMenu()">전국 거시 실증</a></li>
                <li><a href="#micro" onclick="closeMenu()">경기도 미시 전수</a></li>
                <li><a href="#causes" onclick="closeMenu()">원인 진단</a></li>
                <li><a href="#proposals" onclick="closeMenu()">정책 제언</a></li>
                <li><a href="#limitations" onclick="closeMenu()">연구 한계</a></li>
                <!-- Mobile Only Links -->
                <li style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);" class="mobile-only">
                    <a href="https://github.com/kimkij/contest/blob/main/notebooks/low_floor_bus_equity_analysis.ipynb" target="_blank" style="color: #93c5fd;">
                        📓 분석 노트북 (.ipynb)
                    </a>
                </li>
                <li class="mobile-only">
                    <a href="https://github.com/kimkij/contest/tree/main/src" target="_blank" style="color: #cbd5e1;">
                        💻 Python 소스코드 (src/)
                    </a>
                </li>
            </ul>

            <div class="nav-actions">
                <a href="https://github.com/kimkij/contest/blob/main/notebooks/low_floor_bus_equity_analysis.ipynb" target="_blank" class="btn-code primary">
                    📓 분석 노트북 (.ipynb)
                </a>
                <a href="https://github.com/kimkij/contest/tree/main/src" target="_blank" class="btn-code">
                    <svg height="14" width="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
                    소스코드 (src/)
                </a>
            </div>

            <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기">☰</button>
        </div>
    </nav>

    <div class="container">

        <!-- Hero Section -->
        <header class="hero">
            <div class="contest-tag">한겨레 × (재단법인) 숲과나눔 주최 「AI와 함께하는 교통문제 해결 데이터 분석 공모전」</div>
            <h1 class="hero-title">교통약자가 많은 지역에<br><span>저상버스가 더 많이 다니고 있는가?</span></h1>
            <p class="hero-desc">
                2023년 노선버스 대폐차 시 저상버스 도입 의무화가 시행되었습니다. 
                그러나 실제 차량 도입과 운행 노선이 고령자와 장애인이 밀집한 취약 지역에 우선 배정되고 있는지, 
                전국 17개 시·도 및 경기도 31개 시·군(6,431개 버스 노선) 공공데이터를 전수 분석하여 검증했습니다.
            </p>
            <div class="hero-meta">
                <span>📅 기준연도: 2023년 (공식 확정 통계)</span>
                <span>📊 출처: 국토교통부 실태조사 · 통계청 KOSIS · 경기교통정보</span>
                <span>🔍 대상: 전국 17개 시·도 및 경기도 31개 시·군 6,431개 노선 전수</span>
            </div>
        </header>

        <!-- 지표 정의 및 유의사항 배너 -->
        <div class="notice-box">
            <strong>📌 데이터 지표 정의 및 사전 유의사항</strong><br>
            • <strong>전국 단위 공급 지표</strong>: 전체 인가 노선버스 중 저상버스 차량 대수 비율 (<strong>저상버스 도입률, %</strong>)<br>
            • <strong>기초지자체 공급 지표</strong>: 관할 노선 중 저상버스가 1대 이상 운행 중인 노선의 비율 (<strong>저상버스 운행 노선 비율, %</strong>)<br>
            • <strong>수요 지표 (교통약자 비율)</strong>: 65세 이상 고령인구와 등록장애인 수를 단순 합산한 비율이며, 고령 장애인의 중복 집계는 공공데이터 특성상 분리하지 않았습니다.
        </div>

        <!-- KPI Summary Cards -->
        <div class="kpi-grid">
            <div class="kpi-card red">
                <div class="kpi-label">전국 17개 시·도 상관성</div>
                <div class="kpi-val">r = -0.435</div>
                <div class="kpi-sub">음(-)의 상관관계 관찰 (t = -1.87, p = 0.081). 등록장애인 기준 r = -0.573 (p = 0.016, 유의수준 5% 만족)</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">경기도 31개 시·군 상관성</div>
                <div class="kpi-val">r = -0.430</div>
                <div class="kpi-sub">통계적으로 유의미한 음(-)의 상관관계 확증 (t = -2.56, p = 0.016 &lt; 0.05)</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-label">전국 광역 격차 비교</div>
                <div class="kpi-val">4.9배</div>
                <div class="kpi-sub">전남(교통약자 33.7%, 도입률 11.5%) vs 서울(교통약자 22.6%, 도입률 56.8%)</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">소외 군 지역 노선 비율</div>
                <div class="kpi-val">0.0%</div>
                <div class="kpi-sub">가평군·연천군·여주시 등 고령화율 30~40% 군 지역 저상버스 운행 노선 전무</div>
            </div>
        </div>

        <!-- Section 1: Macro Sido Analysis -->
        <section class="section" id="macro">
            <div class="section-header">
                <div class="section-tag">Part 1. 전국 거시 실증</div>
                <h2 class="section-title">전국 17개 시·도: 저상버스 도입률과 교통약자 비율</h2>
            </div>

            <div class="grid-2col">
                <div class="chart-box">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">전국 17개 시·도: 교통약자 비율 vs 저상버스 도입률</div>
                            <div class="chart-subtitle">X축: 교통약자(고령자+장애인) 비율 (%) | Y축: 저상버스 차량 도입률 (%)</div>
                        </div>
                    </div>
                    
                    <div class="chart-legend-box">
                        <div class="legend-item"><span class="legend-dot" style="background: #3b82f6;"></span> 지자체별 현황 (점 크기: 재정자립도)</div>
                        <div class="legend-item"><span class="legend-dot" style="background: #ef4444;"></span> 음(-)의 추세선 (r = -0.435)</div>
                    </div>

                    <div class="chart-canvas-container">
                        <canvas id="sidoScatterChart"></canvas>
                    </div>
                    <div class="chart-fallback" id="sidoFallback">
                        ⚠️ 네트워크 문제로 외부 차트 라이브러리가 로드되지 않았습니다. 하단 상세 표의 데이터를 확인해 주세요.
                    </div>
                </div>

                <div class="analysis-card-col">
                    <div class="story-card danger">
                        <div class="story-title">
                            <span>📉</span> 가설과 다른 음(-)의 상관관계 관찰
                        </div>
                        <p class="story-p">
                            "교통약자가 많은 지역에 저상버스가 더 많이 다닐 것"이라는 기대와 달리, 
                            전국 17개 시·도에서 <span class="stat-badge">r = -0.435 (t = -1.87, p = 0.081)</span>의 
                            음(-)의 관계가 관찰되었습니다. 표본 수가 17개로 적어 5% 유의수준에는 미치지 못하지만(p &lt; 0.10 경향성), 
                            <span class="stat-badge">등록장애인 비율(r = -0.573, t = -2.71, p = 0.016)</span> 기준으로는 통계적으로 유의미한 음의 관계가 확증되었습니다.
                        </p>
                    </div>

                    <div class="story-card">
                        <div class="story-title">
                            <span>🏙</span> 수도권 도심과 비수도권 농어촌의 격차
                        </div>
                        <p class="story-p">
                            • <strong>서울특별시</strong>: 교통약자 22.6%, 재정자립도 81.2% &rarr; <strong>저상버스 도입률 56.8% (시내버스 66.7%)</strong><br>
                            • <strong>전라남도</strong>: 교통약자 33.7%, 재정자립도 28.7% &rarr; <strong>저상버스 도입률 11.5% (전국 최하위)</strong><br>
                            교통약자 인구 비율이 전국에서 가장 높은 전남의 저상버스 도입률은 서울의 1/5 수준에 머물러 있습니다.
                        </p>
                    </div>

                    <div class="story-card primary">
                        <div class="story-title">
                            <span>💰</span> 지자체 재정자립도와의 밀접한 관계
                        </div>
                        <p class="story-p">
                            저상버스 도입률은 교통약자 비율보다 <strong>지자체 재정자립도(<span class="stat-badge">r = +0.495, t = 2.21, p = 0.043 &lt; 0.05</span>)</strong>와 
                            더 밀접한 양의 상관관계를 보이는 것으로 나타났습니다.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Detailed Table with Sticky Column -->
            <div class="table-wrap">
                <div class="table-scroll">
                    <table>
                        <thead>
                            <tr>
                                <th class="sticky-col">시·도명</th>
                                <th>저상버스 도입률</th>
                                <th>시내버스 도입률</th>
                                <th>교통약자 비율</th>
                                <th>고령인구 비율</th>
                                <th>등록장애인 비율</th>
                                <th>재정자립도</th>
                                <th>참고 판정</th>
                            </tr>
                        </thead>
                        <tbody id="sidoTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Section 2: Micro Gyeonggi Analysis -->
        <section class="section" id="micro">
            <div class="section-header">
                <div class="section-tag">Part 2. 기초지자체 미시 전수 분석</div>
                <h2 class="section-title">경기도 31개 시·군 6,431개 버스 노선 전수 분석</h2>
            </div>

            <div class="grid-2col">
                <div class="chart-box">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">수요-공급 4분면 매트릭스 (교통약자 비율 vs 저상버스 노선 비율)</div>
                            <div class="chart-subtitle">십자선: 각 지표의 중앙값 (교통약자 20.8%, 저상노선 18.6%) | 점 크기: 재정자립도</div>
                        </div>
                    </div>

                    <div class="chart-legend-box">
                        <div class="legend-item"><span class="legend-dot" style="background: #ef4444;"></span> 제1우선 소외구역 (수요 高, 공급 低)</div>
                        <div class="legend-item"><span class="legend-dot" style="background: #3b82f6;"></span> 자원 집중구역 (수요 低, 공급 高)</div>
                        <div class="legend-item"><span class="legend-dot" style="background: #64748b;"></span> 일반 구역</div>
                    </div>

                    <div class="chart-canvas-container">
                        <canvas id="ggQuadrantChart"></canvas>
                    </div>
                    <div class="chart-fallback" id="ggFallback">
                        ⚠️ 네트워크 문제로 외부 차트 라이브러리가 로드되지 않았습니다. 하단 표를 참조해 주세요.
                    </div>
                </div>

                <div class="analysis-card-col">
                    <div class="story-card danger">
                        <div class="story-title">
                            <span>🚨</span> [제1우선 소외 사각지대] 수요 극대, 공급 바닥
                        </div>
                        <p class="story-p">
                            <strong>가평군(0%), 연천군(0%), 여주시(0%), 동두천시(5.0%), 포천시(11.8%)</strong><br>
                            고령자와 장애인 인구가 30~40%에 달하지만 저상버스가 다니는 노선은 거의 전무합니다. 
                            이들 지역의 재정자립도는 14~20% 수준으로 도내 최하위권에 해당합니다.
                        </p>
                    </div>

                    <div class="story-card primary">
                        <div class="story-title">
                            <span>🏢</span> [자원 집중구역] 도심권 신도시
                        </div>
                        <p class="story-p">
                            <strong>하남시(63.9%), 광명시(62.7%), 부천시(59.6%), 수원시(52.7%)</strong><br>
                            교통약자 비율은 17~21%로 도내에서 상대적으로 낮으나 저상버스 운행 노선 비율은 50~64%에 달합니다. 
                            재정자립도가 35~50% 수준이며 평지 위주의 신도시 인프라를 갖추고 있습니다.
                        </p>
                    </div>

                    <div class="story-card">
                        <div class="story-title">
                            <span>📐</span> 다중회귀분석(OLS) 추정 결과 및 해석
                        </div>
                        <p class="story-p">
                            종속변수를 시군별 '저상버스 운행 노선 비율(%)'로 하여 OLS 다중회귀분석을 실시한 결과는 다음과 같습니다:
                        </p>
                        <div class="math-code-box">
                            저상노선비율(%) = 46.50 - 1.1366*(교통약자비율) + 0.1395*(재정자립도)<br>
                            • 결정계수 R² = 0.1875 (수정 R² = 0.1294, F = 3.23)<br>
                            • 교통약자비율: 계수 B = -1.1366 (SE = 0.8027, t = -1.416, p = 0.168)<br>
                            • 재정자립도:   계수 B = +0.1395 (SE = 0.4426, t = 0.315, p = 0.755)
                        </div>
                        <p class="story-p" style="font-size: 0.84rem;">
                            ※ <strong>통계적 유의성 해석</strong>: 경기도 31개 시군의 단순 상관분석에서는 <span class="stat-badge">r = -0.430 (p = 0.016 &lt; 0.05)</span>로 
                            통계적 유의성이 확인되었으나, 재정력을 함께 투입한 다중회귀모형에서는 표본 수(n=31)의 제약으로 교통약자 계수(-1.14)의 p값이 0.168로 나타나 
                            유의수준 5%에는 미치지 못했습니다. 따라서 '통계적으로 유의미하다'는 단정 대신 <strong>'음(-)의 회귀계수(-1.14)가 추정되었다'</strong>로 해석합니다.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Gyeonggi 31 Municipalities Full Table -->
            <div class="table-wrap">
                <div class="table-scroll">
                    <table>
                        <thead>
                            <tr>
                                <th class="sticky-col">시·군명</th>
                                <th>저상버스 노선 비율</th>
                                <th>운행 노선수 / 전체</th>
                                <th>교통약자 비율</th>
                                <th>고령인구 비율</th>
                                <th>등록장애인 비율</th>
                                <th>재정자립도</th>
                                <th>4분면 분류</th>
                            </tr>
                        </thead>
                        <tbody id="ggTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Section 3: Root Causes -->
        <section class="section" id="causes">
            <div class="section-header">
                <div class="section-tag">Part 3. 구조적 요인 진단</div>
                <h2 class="section-title">왜 교통약자 밀집지역에 저상버스가 적게 다니는가?</h2>
            </div>

            <div class="cause-grid">
                <div class="cause-card">
                    <div class="cause-num">01</div>
                    <h3 class="cause-title">'국비 50% 정률 매칭' 제도의 재정적 장벽</h3>
                    <p class="cause-desc">
                        저상버스 대당 구입 보조금(약 9,000만 원)은 국비 50%와 지자체 지방비 50%(약 4,500만 원)를 매칭해야 교부됩니다. 
                        재정자립도가 15~20%대에 불과한 군 지역은 매칭 예산을 대규모로 확보하기 어려워 버스 교체 시 저상버스 신청 자체를 포기하는 경향이 발생합니다.
                    </p>
                </div>

                <div class="cause-card">
                    <div class="cause-num">02</div>
                    <h3 class="cause-title">운수회사의 승객 수요 및 효율성 중심 배차</h3>
                    <p class="cause-desc">
                        민간 운수회사 및 준공영제 체계에서는 승객 회전율이 높고 운송 수입이 많은 도심 간선 노선에 신차와 저상버스를 우선 배치합니다. 
                        반면 교통약자가 주로 이용하는 외곽 농어촌 지선 노선은 승객 수가 적어 차량 교체 우선순위에서 밀리기 쉽습니다.
                    </p>
                </div>

                <div class="cause-card">
                    <div class="cause-num">03</div>
                    <h3 class="cause-title">도로 인프라 조건과 '도입 예외 승인'의 구조</h3>
                    <p class="cause-desc">
                        현행 「교통약자법」상 급경사, 굴곡, 과속방지턱 등 도로 환경이 부적합한 노선은 지자체 승인을 통해 저상버스 도입 의무에서 제외될 수 있습니다. 
                        도로 정비 예산이 부족한 외곽 지역일수록 예외 승인을 받는 노선이 늘어나 제도적 공백이 발생합니다.
                    </p>
                </div>
            </div>
        </section>

        <!-- Section 4: Policy Proposals -->
        <section class="section" id="proposals">
            <div class="section-header">
                <div class="section-tag">Part 4. 데이터 기반 정책 제언</div>
                <h2 class="section-title">교통복지 형평성 개선을 위한 정책 제언</h2>
            </div>

            <div class="proposal-grid">
                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">Fiscal System</div>
                        <h3 class="proposal-title">교통약자 수요 연동형<br>차등 국비 보조율 제도</h3>
                        <p class="proposal-body">
                            현행 일률 50% 국비 지원 방식을 지자체 재정자립도와 교통약자 비율에 따라 <strong>30% ~ 80%로 차등화</strong>할 것을 제안합니다. 
                            재정이 열악한 농어촌 지자체의 지방비 부담을 1,800만 원 선으로 낮추어 도입 장벽을 해소합니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        국비보조율 = 기본 50% + 교통약자 가산(최대 15%) + 재정취약 가산(최대 15%) &rarr; 최대 80%
                    </div>
                </div>

                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">Data-Driven Scoring</div>
                        <h3 class="proposal-title">데이터 기반 저상버스<br>우선순위 산정 모델 (LBEI)</h3>
                        <p class="proposal-body">
                            주관적 신청에 의존하지 않고, 행정동별 약자 밀도와 노선 내 병원·복지관 경유도, 현재 공급 부족도를 결합한 
                            <strong>Low-floor Bus Equity Index(LBEI)</strong>를 산출하여 중앙정부 공모 평가 시 우선 배정 가점을 부여합니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        LBEI = 0.4×(동별 약자밀도) + 0.3×(병원·복지관 경유도) + 0.3×(1 - 현재노선 공급률)
                    </div>
                </div>

                <div class="proposal-card">
                    <div>
                        <div class="proposal-tag">Infrastructure Package</div>
                        <h3 class="proposal-title">중형 저상 전기버스 &amp;<br>도로 환경 개선 패키지</h3>
                        <p class="proposal-body">
                            대형(11m) 저상버스가 진입하기 어려운 굴곡진 도로를 위해 <strong>중형(8~9m) 저상 전기버스 전용 지원 트랙</strong>을 마련하고, 
                            도입 예외 노선에 대해 도로 단차 및 턱 낮춤 정비 예산을 국토부 도로사업과 1:1 패키지로 지원합니다.
                        </p>
                    </div>
                    <div class="formula-box">
                        중형 저상버스 보조금 신설 + 도로 굴곡·단차 정비 국비 패키지 연계
                    </div>
                </div>
            </div>
        </section>

        <!-- Section 5: Limitations of Research -->
        <section class="section" id="limitations">
            <div class="limitations-box">
                <div class="limitations-title">
                    <span>⚠️</span> 본 분석의 방법론적 한계 및 향후 과제
                </div>
                <ul class="limitations-list">
                    <li><strong>인과관계 추정의 한계</strong>: 본 연구는 2023년 시점의 횡단면 데이터(Cross-sectional Data)를 비교한 분석입니다. 따라서 재정자립도와 저상버스 도입 간의 '통계적 관련성'을 확인한 것이며, 도시 밀도, 버스 준공영제 여부, 노선 굴곡도 등 다른 미관측 변수가 통제되지 않아 엄밀한 인과관계로 단정하기는 어렵습니다.</li>
                    <li><strong>교통약자 집계의 중복성</strong>: 본 분석의 '교통약자 비율'은 65세 이상 고령자와 등록장애인을 단순 합산한 값으로, 고령 장애인이 양쪽 집계에 중복 포함되었을 가능성이 있습니다.</li>
                    <li><strong>공급 지표 정의의 상이성</strong>: 전국 분석은 '저상버스 차량 도입 대수 비율(%)'을 사용한 반면, 경기도 분석은 '저상버스가 1대 이상 투입된 노선의 비율(%)'을 사용하였으므로 두 지표 간 수치를 직접 비교할 때는 주의가 필요합니다.</li>
                    <li><strong>실제 예산 집행 데이터의 부재</strong>: 본 연구는 도입 결과(차량 및 노선)를 바탕으로 분석을 진행하였으며, 지자체별 실제 국비·지방비 집행 총액 데이터를 직접 추적하지는 못했습니다. 차후 재정 통계의 연계 분석이 요구됩니다.</li>
                </ul>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p><strong>한겨레 × (재단법인) 숲과나눔 주최 「AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전」 제출작</strong></p>
            <p>
                분석 소스코드 디렉토리: <a href="https://github.com/kimkij/contest/tree/main/src" target="_blank">github.com/kimkij/contest/tree/main/src</a> | 
                분석 노트북: <a href="https://github.com/kimkij/contest/blob/main/notebooks/low_floor_bus_equity_analysis.ipynb" target="_blank">low_floor_bus_equity_analysis.ipynb</a>
            </p>
            <p style="color: #64748b; font-size: 0.8rem; margin-top: 6px;">
                데이터 원천: 국토교통부·한국교통안전공단 『2023년 교통약자 이동편의 실태조사 보고서』, 통계청 KOSIS 시군구 통계, 경기교통정보
            </p>
        </footer>

    </div>

    <!-- JavaScript: Menu Toggle & Interactive Chart.js Rendering -->
    <script>
        // Mobile Hamburger Menu
        const navToggle = document.getElementById('navToggle');
        const navMenu = document.getElementById('navMenu');
        navToggle.addEventListener('click', () => {{
            navMenu.classList.toggle('open');
        }});
        function closeMenu() {{
            navMenu.classList.remove('open');
        }}

        const sidoData = {sido_json};
        const ggData = {gg_json};

        // Render Sido Table
        const sortedSido = [...sidoData].sort((a, b) => b.total_rate - a.total_rate);
        const tbodySido = document.getElementById('sidoTableBody');
        sortedSido.forEach(d => {{
            const tr = document.createElement('tr');
            const badge = d.total_rate < 20 ? '<span class="badge-danger">취약 지역</span>' : (d.total_rate > 40 ? '<span class="badge-success">우수 도입</span>' : '-');
            tr.innerHTML = `
                <td class="sticky-col"><strong>${{d.region}}</strong></td>
                <td><strong>${{d.total_rate}}%</strong></td>
                <td>${{d.city_bus_rate}}%</td>
                <td>${{d.vulnerable_rate}}%</td>
                <td>${{d.elderly_rate}}%</td>
                <td>${{d.disabled_rate}}%</td>
                <td>${{d.fiscal_rate}}%</td>
                <td>${{badge}}</td>
            `;
            tbodySido.appendChild(tr);
        }});

        // Render Gyeonggi Table
        const medVul = 20.8;
        const medSup = 18.6;
        const sortedGG = [...ggData].sort((a, b) => b.low_floor_route_ratio - a.low_floor_route_ratio);
        const tbodyGG = document.getElementById('ggTableBody');
        sortedGG.forEach(d => {{
            const tr = document.createElement('tr');
            let quadBadge = '<span style="color:#94a3b8;">일반</span>';
            if (d.vulnerable_rate > medVul && d.low_floor_route_ratio < medSup) {{
                quadBadge = '<span class="badge-danger">제1우선 소외지</span>';
            }} else if (d.vulnerable_rate <= medVul && d.low_floor_route_ratio >= medSup) {{
                quadBadge = '<span class="badge-success">자원 집중지</span>';
            }}
            tr.innerHTML = `
                <td class="sticky-col"><strong>${{d.city}}</strong></td>
                <td><strong>${{d.low_floor_route_ratio}}%</strong></td>
                <td>${{d.low_floor_routes}} / ${{d.total_routes}}개</td>
                <td>${{d.vulnerable_rate}}%</td>
                <td>${{d.elderly_rate}}%</td>
                <td>${{d.disabled_rate}}%</td>
                <td>${{d.fiscal_rate}}%</td>
                <td>${{quadBadge}}</td>
            `;
            tbodyGG.appendChild(tr);
        }});

        // Chart.js Rendering with try-catch fallback
        try {{
            if (typeof Chart !== 'undefined') {{
                // 1. 전국 17개 시도 산점도 (Scatter Chart with Trendline)
                const ctxSido = document.getElementById('sidoScatterChart').getContext('2d');
                
                // Polyfit trendline points (x from 14 to 34)
                // y = -1.0664 * x + 58.07
                const trendPoints = [
                    {{ x: 14.0, y: 47.0 }},
                    {{ x: 34.0, y: 25.7 }}
                ];

                new Chart(ctxSido, {{
                    type: 'scatter',
                    data: {{
                        datasets: [
                            {{
                                label: '17개 시·도 지자체',
                                data: sidoData.map(d => ({{
                                    x: d.vulnerable_rate,
                                    y: d.total_rate,
                                    region: d.region,
                                    fiscal: d.fiscal_rate,
                                    cityBusRate: d.city_bus_rate
                                }})),
                                backgroundColor: sidoData.map(d => d.total_rate < 20 ? 'rgba(239, 68, 68, 0.85)' : 'rgba(59, 130, 246, 0.8)'),
                                borderColor: '#ffffff',
                                borderWidth: 1,
                                pointRadius: sidoData.map(d => Math.max(5, d.fiscal_rate / 9))
                            }},
                            {{
                                label: '음(-)의 추세선 (r = -0.435)',
                                type: 'line',
                                data: trendPoints,
                                borderColor: '#ef4444',
                                borderWidth: 2,
                                borderDash: [6, 4],
                                fill: false,
                                pointRadius: 0
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const raw = context.raw;
                                        if (!raw.region) return '추세선';
                                        return [
                                            `[${{raw.region}}]`,
                                            `교통약자 비율: ${{raw.x}}%`,
                                            `저상버스 도입률: ${{raw.y}}% (시내버스 ${{raw.cityBusRate}}%)`,
                                            `재정자립도: ${{raw.fiscal}}%`
                                        ];
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                title: {{ display: true, text: '교통약자(고령자+등록장애인) 인구 비율 (%)', color: '#94a3b8' }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                                ticks: {{ color: '#94a3b8' }},
                                min: 12,
                                max: 36
                            }},
                            y: {{
                                title: {{ display: true, text: '저상버스 도입률 (%)', color: '#94a3b8' }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                                ticks: {{ color: '#94a3b8' }},
                                min: 5,
                                max: 65
                            }}
                        }}
                    }}
                }});

                // 2. 경기도 31개 시·군 4분면 버블 차트 (with city name labels)
                const ctxGG = document.getElementById('ggQuadrantChart').getContext('2d');

                new Chart(ctxGG, {{
                    type: 'bubble',
                    data: {{
                        datasets: [
                            {{
                                label: '제1우선 소외구역 (수요 高, 공급 低)',
                                data: ggData.filter(d => d.vulnerable_rate > medVul && d.low_floor_route_ratio < medSup).map(d => ({{
                                    x: d.vulnerable_rate,
                                    y: d.low_floor_route_ratio,
                                    r: Math.max(5, d.fiscal_rate / 3.8),
                                    city: d.city,
                                    fiscal: d.fiscal_rate,
                                    routes: d.total_routes,
                                    lowRoutes: d.low_floor_routes
                                }})),
                                backgroundColor: 'rgba(239, 68, 68, 0.85)',
                                borderColor: '#ffffff',
                                borderWidth: 1.2
                            }},
                            {{
                                label: '자원 집중구역 (수요 低, 공급 高)',
                                data: ggData.filter(d => d.vulnerable_rate <= medVul && d.low_floor_route_ratio >= medSup).map(d => ({{
                                    x: d.vulnerable_rate,
                                    y: d.low_floor_route_ratio,
                                    r: Math.max(5, d.fiscal_rate / 3.8),
                                    city: d.city,
                                    fiscal: d.fiscal_rate,
                                    routes: d.total_routes,
                                    lowRoutes: d.low_floor_routes
                                }})),
                                backgroundColor: 'rgba(59, 130, 246, 0.85)',
                                borderColor: '#ffffff',
                                borderWidth: 1.2
                            }},
                            {{
                                label: '일반 구역',
                                data: ggData.filter(d => !(d.vulnerable_rate > medVul && d.low_floor_route_ratio < medSup) && !(d.vulnerable_rate <= medVul && d.low_floor_route_ratio >= medSup)).map(d => ({{
                                    x: d.vulnerable_rate,
                                    y: d.low_floor_route_ratio,
                                    r: Math.max(5, d.fiscal_rate / 3.8),
                                    city: d.city,
                                    fiscal: d.fiscal_rate,
                                    routes: d.total_routes,
                                    lowRoutes: d.low_floor_routes
                                }})),
                                backgroundColor: 'rgba(148, 163, 184, 0.65)',
                                borderColor: 'rgba(255, 255, 255, 0.4)',
                                borderWidth: 1
                            }}
                        ]
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
                                            `[${{raw.city}}]`,
                                            `교통약자 비율: ${{raw.x}}%`,
                                            `저상버스 운행노선: ${{raw.y}}% (${{raw.lowRoutes}}/${{raw.routes}}개)`,
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
                                min: -3,
                                max: 70
                            }}
                        }}
                    }}
                }});
            }}
        }} catch(e) {{
            console.error("Chart load error:", e);
            document.getElementById('sidoFallback').style.display = 'block';
            document.getElementById('ggFallback').style.display = 'block';
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Properly formatted index.html written!")
