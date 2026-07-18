"""Sistema visual compartido del dashboard de CrediBot."""
import streamlit as st


def apply_dashboard_styles() -> None:
    """Aplica la identidad visual verde inspirada en WhatsApp."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --cb-bg: #f4f8f5;
            --cb-panel: #ffffff;
            --cb-panel-soft: #f7faf8;
            --cb-line: #dce8e1;
            --cb-text: #14251d;
            --cb-muted: #6b7e74;
            --cb-brand: #19a96b;
            --cb-brand-dark: #075e54;
            --cb-brand-deep: #043d38;
            --cb-brand-soft: #e8f7ef;
            --cb-lime: #b8e986;
            --cb-warn: #e6a23c;
            --cb-danger: #d64545;
            --cb-chat-bg: #efeae2;
            --cb-bubble-in: #ffffff;
            --cb-bubble-out: #d9fdd3;
            --cb-shadow: 0 12px 34px rgba(7, 94, 84, 0.08);
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Manrope', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 90% 0%, rgba(37, 211, 102, .08), transparent 30%),
                var(--cb-bg);
            color: var(--cb-text);
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] { display: none; }
        [data-testid="stDecoration"] { display: none; }
        [data-testid="InputInstructions"] { display: none !important; }

        section[data-testid="stSidebar"] {
            background: #075e54;
            border-right: 0;
            box-shadow: 7px 0 24px rgba(4, 61, 56, .10);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.15rem;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            display: none;
        }

        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            border: 1px solid rgba(255,255,255,.16);
            background: rgba(255,255,255,.07);
            color: #ecfff6;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            border-color: rgba(255,255,255,.35);
            background: rgba(255,255,255,.13);
            color: #ffffff;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            border-radius: 10px;
            color: #f4fffa !important;
            font-size: 14px;
            font-weight: 650;
            padding: .7rem .78rem;
            margin: .18rem 0;
            transition: all .18s ease;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
        section[data-testid="stSidebar"] [data-testid="stPageLink"] *,
        section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
            color: #f4fffa !important;
            opacity: 1 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            background: rgba(255,255,255,.11);
            color: #ffffff;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
            background: rgba(255,255,255,.14);
            box-shadow: inset 3px 0 0 #52df98;
        }

        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] *,
        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
            color: #ffffff !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1440px;
        }

        h1, h2, h3, h4 {
            color: var(--cb-text);
            letter-spacing: -.025em;
        }

        .cb-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 4px 22px;
            border-bottom: 1px solid rgba(255,255,255,.12);
            margin-bottom: 14px;
        }

        .cb-brand-mark {
            width: 45px;
            height: 45px;
            display: grid;
            place-items: center;
            border-radius: 14px;
            background: linear-gradient(145deg, #35e087, #18a968);
            color: #043d38;
            font-size: 23px;
            font-weight: 900;
            box-shadow: 0 9px 22px rgba(37,211,102,.25);
        }

        .cb-brand-name { color: #ffffff; font-size: 18px; font-weight: 800; line-height: 1.1; }
        .cb-brand-tagline { color: #c4e1d6; font-size: 10px; font-weight: 600; margin-top: 4px; }
        .cb-nav-label { color: #b9d9cc; font-size: 10px; font-weight: 800; letter-spacing: .12em; margin: 18px 8px 8px; }
        .cb-sidebar-footer { color: #c4e1d6; font-size: 10px; line-height: 1.5; border-top: 1px solid rgba(255,255,255,.16); padding: 16px 5px 10px; margin-top: 20px; }
        .cb-sidebar-live { display:inline-block; width:7px; height:7px; border-radius:50%; background:#35e087; box-shadow:0 0 0 4px rgba(53,224,135,.12); margin-right:7px; }

        .cb-login-card { text-align:center; padding:8px 12px 24px; }
        .cb-login-mark { width:58px; height:58px; border-radius:18px; display:grid; place-items:center; background:#e6f7ed; color:#087b50; font-size:28px; font-weight:900; box-shadow:0 9px 22px rgba(25,169,107,.13); margin:0 auto 20px; }
        .cb-login-eyebrow { color:#15945d; letter-spacing:.14em; font-size:10px; font-weight:800; }
        .cb-login-card h1 { color:var(--cb-text); font-size:30px; line-height:1.18; margin:11px 0 10px; font-weight:800; white-space:nowrap; }
        .cb-login-card p { color:var(--cb-muted); line-height:1.6; max-width:370px; margin:0 auto; font-size:13px; }
        div[data-testid="stForm"]:has(#admin_login_form) { border:1px solid #dcebe2; border-radius:20px; padding:25px; background:#fff; box-shadow:0 16px 38px rgba(20,70,47,.08); }
        div[data-testid="stFormSubmitButton"] > button {
            background: #109b63 !important;
            border-color: #109b63 !important;
            color: #ffffff !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background: #087b50 !important;
            border-color: #087b50 !important;
        }

        .cb-hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(125deg, #075e54 0%, #08786b 58%, #109866 100%);
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 22px;
            padding: 26px 30px;
            margin-bottom: 16px;
            box-shadow: var(--cb-shadow);
            color: #ffffff;
        }

        .cb-hero::after {
            content: '$';
            position: absolute;
            right: 34px;
            top: -34px;
            font-size: 150px;
            font-weight: 900;
            color: rgba(255,255,255,.065);
            transform: rotate(10deg);
        }

        .cb-eyebrow { color: #c9f4dc; font-size: 10px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 8px; }
        .cb-hero-title { color:#ffffff; font-size: 31px; line-height: 1.2; font-weight: 800; margin-bottom: 7px; letter-spacing: -.035em; }
        .cb-hero-subtitle { color: #d4eee5; font-size: 13px; margin: 0; max-width: 720px; }
        .cb-section-title { font-size: 17px; font-weight: 800; margin: 16px 0 10px; color:var(--cb-text); }
        .cb-section-head { display:flex; align-items:baseline; justify-content:space-between; gap:12px; margin-top: 12px; }
        .cb-section-head .cb-section-title { margin: 0 0 10px; }
        .cb-section-note { color:var(--cb-muted); font-size:11px; }
        .cb-muted { color: var(--cb-muted); font-size: 12px; }
        .cb-kpi-label { color:var(--cb-muted); font-size:11px; font-weight:800; letter-spacing:.10em; text-transform:uppercase; margin: 18px 0 9px; }
        .cb-kpi-label.cb-kpi-status { margin-top: 14px; }
        .cb-action-strip { display:flex; align-items:center; gap:14px; min-height:40px; padding: 0 4px 4px; }
        .cb-action-strip .cb-action-note { color:var(--cb-muted); font-size:12px; }
        .cb-action-strip .stPageLink { margin:0; }
        .cb-toolbar-status {
            min-height:42px;
            display:flex;
            align-items:center;
            gap:10px;
            padding:8px 12px;
            border:1px solid var(--cb-line);
            border-radius:11px;
            background:rgba(255,255,255,.82);
        }
        .cb-toolbar-status strong { display:block; color:var(--cb-text); font-size:11px; line-height:1.25; }
        .cb-toolbar-status small { display:block; color:var(--cb-muted); font-size:9px; margin-top:2px; }
        .cb-toolbar-error { background:#fff7f6; border-color:#efc8c5; }
        .cb-status-dot-error { width:8px; height:8px; border-radius:50%; background:var(--cb-danger); box-shadow:0 0 0 4px rgba(214,69,69,.1); flex:0 0 auto; }

        div[data-testid="stMetric"] {
            background: var(--cb-panel);
            border: 1px solid var(--cb-line);
            border-radius: 16px;
            min-height: 96px;
            padding: 15px 18px;
            box-shadow: 0 7px 22px rgba(27, 80, 58, .05);
            transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
        }

        div[data-testid="stMetric"]:hover { transform: translateY(-2px); border-color:#b9d9c9; box-shadow: 0 12px 28px rgba(27,80,58,.09); }

        div[data-testid="stMetric"] label { color: var(--cb-muted); font-weight: 650; }
        div[data-testid="stMetricValue"] { color: var(--cb-brand-dark); font-weight: 800; font-size: 2rem; line-height:1.1; }
        div[data-testid="stDataFrame"] { border: 1px solid var(--cb-line); border-radius: 16px; overflow: hidden; box-shadow: 0 7px 22px rgba(27,80,58,.04); }
        div[data-testid="stPlotlyChart"] { border: 1px solid var(--cb-line); border-radius: 16px; background: var(--cb-panel); padding: 8px 10px 4px; box-shadow: 0 7px 22px rgba(27,80,58,.04); }
        div[data-testid="stForm"] { border: 1px solid var(--cb-line); border-radius: 16px; padding: 14px; background: var(--cb-panel); }

        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
            border-radius: 11px;
            font-weight: 750;
            min-height: 42px;
        }

        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
            background: var(--cb-brand);
            border-color: var(--cb-brand);
        }

        .cb-panel { background:var(--cb-panel); border:1px solid var(--cb-line); border-radius:16px; overflow:hidden; box-shadow:0 7px 22px rgba(27,80,58,.05); }
        .cb-panel-pad { padding: 16px; }
        .cb-contact { border:1px solid var(--cb-line); border-radius:14px; padding:12px 14px; background:var(--cb-panel); margin-bottom:9px; }
        .cb-contact-active { border-color:var(--cb-brand); background:var(--cb-brand-soft); box-shadow:0 5px 15px rgba(25,169,107,.08); }
        .cb-contact-name { font-weight:750; font-size:13px; margin-bottom:3px; }
        .cb-contact-meta { color:var(--cb-muted); font-size:11px; line-height:1.4; }
        .cb-pill { display:inline-block; border-radius:999px; padding:4px 9px; font-size:10px; font-weight:800; border:1px solid var(--cb-line); background:var(--cb-panel-soft); }
        .cb-pill-green { background:#e8f8ef; color:#087347; border-color:#b7e5ca; }
        .cb-pill-yellow { background:#fff7e6; color:#9b6100; border-color:#f3d79b; }
        .cb-pill-red { background:#fff0ef; color:#ae302b; border-color:#efc0bd; }
        .cb-empty-state { border:1px dashed #bdd8ca; border-radius:14px; padding:20px; text-align:center; color:var(--cb-muted); background:rgba(255,255,255,.55); font-size:12px; }
        .cb-case-summary { display:flex; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:8px 10px; }
        .cb-case-summary strong { display:block; color:var(--cb-text); font-size:12px; }
        .cb-case-summary small { display:block; color:var(--cb-muted); font-size:10px; margin-top:3px; line-height:1.35; }
        .cb-case-pills { display:flex; flex-wrap:wrap; justify-content:flex-end; gap:5px; }
        .cb-case-age { width:100%; color:var(--cb-muted); font-size:10px; }
        [class*="st-key-summary_case_"] { background:rgba(255,255,255,.88); box-shadow:0 5px 16px rgba(27,80,58,.04); }

        .cb-chat-header { display:flex; align-items:center; justify-content:space-between; gap:10px; background:linear-gradient(100deg,#075e54,#08796c); color:#fff; padding:14px 16px; }
        .cb-chat-name { font-weight:800; font-size:15px; margin:0; }
        .cb-chat-phone { font-size:10px; color:#c9e9dc; margin:2px 0 0; }
        .cb-chat-window { background-color:var(--cb-chat-bg); background-image:radial-gradient(rgba(7,94,84,.045) 1px,transparent 1px); background-size:18px 18px; border-left:1px solid var(--cb-line); border-right:1px solid var(--cb-line); min-height:500px; max-height:610px; overflow-y:auto; padding:18px 16px; }
        .cb-message-row { display:flex; margin:7px 0; }
        .cb-message-in { justify-content:flex-start; }
        .cb-message-out { justify-content:flex-end; }
        .cb-bubble { width:fit-content; max-width:min(80%,640px); border-radius:10px; padding:9px 11px; box-shadow:0 1px 2px rgba(16,24,40,.12); font-size:13px; line-height:1.45; white-space:pre-wrap; overflow-wrap:anywhere; }
        .cb-bubble-in { background:var(--cb-bubble-in); border-top-left-radius:3px; }
        .cb-bubble-out { background:var(--cb-bubble-out); border-top-right-radius:3px; }
        .cb-message-author { font-weight:800; font-size:10px; color:var(--cb-brand-dark); margin-bottom:3px; }
        .cb-message-time { color:#708078; font-size:9px; text-align:right; margin-top:4px; }
        .cb-chat-compose { background:#f0f4f2; border:1px solid var(--cb-line); border-top:0; padding:12px; border-radius:0 0 16px 16px; }
        .cb-chat-empty { text-align:center; color:#667a70; font-size:12px; background:rgba(255,255,255,.75); border-radius:12px; padding:12px 16px; max-width:300px; margin:160px auto 0; box-shadow:0 2px 10px rgba(7,94,84,.06); }
        .cb-date-chip { width:max-content; margin:0 auto 16px; background:rgba(255,255,255,.82); color:#667a70; border-radius:999px; padding:5px 10px; font-size:9px; font-weight:750; box-shadow:0 1px 3px rgba(0,0,0,.07); }

        .cb-simulator-shell { max-width:880px; margin:0 auto; border-radius:20px; overflow:hidden; box-shadow:0 18px 48px rgba(7,94,84,.14); border:1px solid #cfddd6; }
        .cb-sim-header { display:flex; align-items:center; gap:11px; background:#075e54; color:#fff; padding:14px 18px; }
        .cb-avatar { width:38px; height:38px; border-radius:50%; display:grid; place-items:center; background:#25d366; color:#064f49; font-weight:900; }
        .cb-sim-name { font-weight:800; font-size:14px; }
        .cb-sim-status { color:#bfe7d7; font-size:10px; margin-top:2px; }
        .cb-sim-window { min-height:480px; max-height:570px; overflow:auto; background-color:#efeae2; background-image:radial-gradient(rgba(7,94,84,.05) 1px,transparent 1px); background-size:19px 19px; padding:20px; }
        .cb-sim-note { background:#e7f5ef; border:1px solid #c1e5d2; color:#39705a; border-radius:12px; padding:11px 14px; font-size:11px; margin-bottom:14px; }

        .cb-detail-item { border-bottom:1px solid var(--cb-line); padding:10px 0; }
        .cb-detail-item:last-child { border-bottom:0; }
        .cb-detail-label { color:var(--cb-muted); font-size:10px; margin-bottom:3px; }
        .cb-detail-value { font-size:13px; font-weight:700; }

        @media (max-width: 1180px) {
            .block-container { padding-left:1.35rem; padding-right:1.35rem; }
            .st-key-dashboard_operations div[data-testid="stHorizontalBlock"]:first-of-type,
            .st-key-handoff_workspace > div > div[data-testid="stHorizontalBlock"] {
                flex-direction:column;
                gap:1rem;
            }
            .st-key-dashboard_operations div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"],
            .st-key-handoff_workspace > div > div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
                width:100% !important;
                flex:1 1 100% !important;
            }
            div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) {
                flex-wrap:wrap;
            }
            div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) > div[data-testid="stColumn"] {
                flex:1 1 calc(50% - 1rem) !important;
                width:auto !important;
                min-width:180px;
            }
        }

        @media (max-width: 900px) {
            .block-container { padding-top:1rem; }
            .cb-hero { padding:22px 20px; border-radius:17px; }
            .cb-hero-title { font-size:25px; }
            .cb-hero::after { display:none; }
            .cb-chat-window { min-height:430px; }
            .cb-login-card h1 { font-size:27px; }
            .cb-action-strip { align-items:flex-start; flex-direction:column; gap:4px; }
            .cb-section-head { align-items:flex-start; flex-direction:column; gap:2px; }
            .cb-simulator-shell { border-radius:16px; }
            .cb-sim-window { min-height:400px; }
        }

        @media (max-width: 620px) {
            .block-container { padding-left:.85rem; padding-right:.85rem; }
            section[data-testid="stSidebar"] { box-shadow:none; }
            div[data-testid="stHorizontalBlock"] { flex-direction:column; gap:.65rem; }
            div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
                width:100% !important;
                flex:1 1 100% !important;
                min-width:0 !important;
            }
            .cb-hero { padding:19px 17px; margin-bottom:12px; }
            .cb-hero-title { font-size:22px; }
            .cb-hero-subtitle { font-size:12px; }
            div[data-testid="stMetric"] { min-height:84px; }
            div[data-testid="stMetricValue"] { font-size:1.75rem; }
            .cb-chat-window, .cb-sim-window { min-height:350px; padding:14px 11px; }
            .cb-case-pills { justify-content:flex-start; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
