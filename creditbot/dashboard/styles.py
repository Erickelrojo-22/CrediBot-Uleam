"""Estilos compartidos para el dashboard de Streamlit."""
import streamlit as st


def apply_dashboard_styles() -> None:
    """Aplica CSS global para un panel administrativo más compacto."""
    st.markdown(
        """
        <style>
        :root {
            --cb-bg: #f5f7fb;
            --cb-panel: #ffffff;
            --cb-panel-soft: #f8fafc;
            --cb-line: #d7dee9;
            --cb-text: #172033;
            --cb-muted: #667085;
            --cb-brand: #0f766e;
            --cb-brand-dark: #0b5f59;
            --cb-blue: #1d4ed8;
            --cb-warn: #b45309;
            --cb-danger: #b42318;
            --cb-bubble-in: #ffffff;
            --cb-bubble-out: #dcf8c6;
            --cb-chat-bg: #efeae2;
        }

        .stApp {
            background: var(--cb-bg);
            color: var(--cb-text);
        }

        section[data-testid="stSidebar"] {
            background: #e9edf4;
            border-right: 1px solid var(--cb-line);
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2rem;
            max-width: 1380px;
        }

        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--cb-text);
        }

        div[data-testid="stMetric"] {
            background: var(--cb-panel);
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            padding: 16px 18px;
        }

        div[data-testid="stMetric"] label {
            color: var(--cb-muted);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            overflow: hidden;
        }

        div[data-testid="stForm"] {
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            padding: 14px;
            background: var(--cb-panel);
        }

        .cb-hero {
            background: var(--cb-panel);
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            padding: 22px 24px;
            margin-bottom: 18px;
        }

        .cb-hero-title {
            font-size: 30px;
            line-height: 1.2;
            font-weight: 750;
            margin-bottom: 6px;
        }

        .cb-hero-subtitle {
            color: var(--cb-muted);
            font-size: 14px;
            margin: 0;
        }

        .cb-section-title {
            font-size: 18px;
            font-weight: 720;
            margin: 8px 0 10px;
        }

        .cb-muted {
            color: var(--cb-muted);
            font-size: 13px;
        }

        .cb-kpi-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 16px;
        }

        .cb-mini-card {
            background: var(--cb-panel);
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            padding: 14px;
        }

        .cb-mini-label {
            color: var(--cb-muted);
            font-size: 12px;
            margin-bottom: 6px;
        }

        .cb-mini-value {
            font-size: 26px;
            font-weight: 760;
            line-height: 1;
        }

        .cb-inbox-shell {
            display: grid;
            grid-template-columns: 320px minmax(420px, 1fr) 300px;
            gap: 14px;
            align-items: start;
        }

        .cb-panel {
            background: var(--cb-panel);
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            overflow: hidden;
        }

        .cb-panel-pad {
            padding: 14px;
        }

        .cb-contact {
            border: 1px solid var(--cb-line);
            border-radius: 8px;
            padding: 10px 12px;
            background: var(--cb-panel);
            margin-bottom: 8px;
        }

        .cb-contact-active {
            border-color: var(--cb-brand);
            background: #ecfdf5;
        }

        .cb-contact-name {
            font-weight: 720;
            font-size: 14px;
            margin-bottom: 2px;
        }

        .cb-contact-meta {
            color: var(--cb-muted);
            font-size: 12px;
            line-height: 1.35;
        }

        .cb-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 700;
            border: 1px solid var(--cb-line);
            background: var(--cb-panel-soft);
            color: var(--cb-text);
        }

        .cb-pill-green {
            background: #ecfdf3;
            color: #027a48;
            border-color: #abefc6;
        }

        .cb-pill-yellow {
            background: #fffaeb;
            color: #b54708;
            border-color: #fedf89;
        }

        .cb-pill-red {
            background: #fef3f2;
            color: #b42318;
            border-color: #fecdca;
        }

        .cb-chat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            background: #075e54;
            color: #ffffff;
            padding: 14px 16px;
        }

        .cb-chat-name {
            font-weight: 760;
            font-size: 16px;
            margin: 0;
        }

        .cb-chat-phone {
            font-size: 12px;
            color: #d8f3ed;
            margin: 2px 0 0;
        }

        .cb-chat-window {
            background: var(--cb-chat-bg);
            border-left: 1px solid var(--cb-line);
            border-right: 1px solid var(--cb-line);
            min-height: 520px;
            max-height: 620px;
            overflow-y: auto;
            padding: 18px 16px;
        }

        .cb-message-row {
            display: flex;
            margin: 7px 0;
        }

        .cb-message-in {
            justify-content: flex-start;
        }

        .cb-message-out {
            justify-content: flex-end;
        }

        .cb-bubble {
            width: fit-content;
            max-width: min(78%, 640px);
            border-radius: 8px;
            padding: 8px 10px;
            box-shadow: 0 1px 1px rgba(16, 24, 40, 0.08);
            font-size: 14px;
            line-height: 1.42;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .cb-bubble-in {
            background: var(--cb-bubble-in);
        }

        .cb-bubble-out {
            background: var(--cb-bubble-out);
        }

        .cb-message-author {
            font-weight: 720;
            font-size: 11px;
            color: var(--cb-brand-dark);
            margin-bottom: 3px;
        }

        .cb-message-time {
            color: #667085;
            font-size: 10px;
            text-align: right;
            margin-top: 4px;
        }

        .cb-chat-compose {
            background: #f0f2f5;
            border: 1px solid var(--cb-line);
            border-top: 0;
            padding: 12px;
            border-radius: 0 0 8px 8px;
        }

        .cb-detail-item {
            border-bottom: 1px solid var(--cb-line);
            padding: 10px 0;
        }

        .cb-detail-item:last-child {
            border-bottom: 0;
        }

        .cb-detail-label {
            color: var(--cb-muted);
            font-size: 12px;
            margin-bottom: 3px;
        }

        .cb-detail-value {
            font-size: 14px;
            font-weight: 680;
        }

        @media (max-width: 1100px) {
            .cb-inbox-shell {
                grid-template-columns: 1fr;
            }
            .cb-chat-window {
                min-height: 460px;
            }
            .cb-kpi-row {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
