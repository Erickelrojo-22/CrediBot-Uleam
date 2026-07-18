"""Página principal del panel de administración de CrediBot."""
from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st

from components.auth import require_auth
from components.navigation import render_sidebar
from components.presentation import (
    case_priority,
    comparison_delta,
    count_previous_period,
    filter_by_period,
    format_datetime,
    now_local,
    percentage,
    relative_time,
    translate_case_reason,
    translate_case_status,
    translate_request_status,
    translate_result,
)
from components.ui import render_empty_state, render_page_header, render_period_selector
from services.supabase_dashboard import (
    DashboardConfigError,
    obtener_casos_derivados,
    obtener_contadores_navegacion,
    obtener_solicitudes,
    obtener_usuarios,
)
from styles import apply_dashboard_styles


st.set_page_config(page_title="CrediBot Dashboard", page_icon="CB", layout="wide")
apply_dashboard_styles()
require_auth()

try:
    usuarios = obtener_usuarios()
    solicitudes = obtener_solicitudes()
    casos_derivados = obtener_casos_derivados()
except DashboardConfigError as exc:
    render_sidebar(counts={})
    st.warning(str(exc))
    st.stop()
except Exception as exc:
    render_sidebar(counts={})
    st.error(f"No se pudo consultar Supabase: {exc}")
    st.stop()

df_usuarios_all = pd.DataFrame(usuarios)
df_solicitudes_all = pd.DataFrame(solicitudes)
df_casos_all = pd.DataFrame(casos_derivados)

pending_all = (
    int((df_casos_all["status"] == "pending").sum())
    if not df_casos_all.empty and "status" in df_casos_all
    else 0
)
render_sidebar(
    counts={
        "solicitudes": len(df_solicitudes_all),
        "casos_pendientes": pending_all,
    }
)

render_page_header(
    "Centro de operaciones · Entorno académico",
    "Panel Administrativo CrediBot",
    "Supervisa solicitudes de crédito, resultados del agente y casos que necesitan atención humana.",
)

toolbar_period, toolbar_status, toolbar_simulator, toolbar_refresh = st.columns(
    [1.55, 1.35, 1.35, 0.85], vertical_alignment="bottom"
)
with toolbar_period:
    period = render_period_selector("dashboard_period")
with toolbar_status:
    st.markdown(
        f"""
        <div class="cb-toolbar-status">
          <span class="cb-sidebar-live"></span>
          <div><strong>Supabase conectado</strong><small>Consulta {now_local().strftime('%H:%M')}</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with toolbar_simulator:
    st.page_link(
        "pages/1_Simulador.py",
        label="Probar conversación",
        icon="💬",
        width="stretch",
    )
with toolbar_refresh:
    if st.button("Actualizar", width="stretch"):
        obtener_contadores_navegacion.clear()

st.session_state["dashboard_last_query"] = now_local().isoformat()

df_usuarios = filter_by_period(df_usuarios_all, period)
df_solicitudes = filter_by_period(df_solicitudes_all, period)
df_casos = filter_by_period(df_casos_all, period)

total_usuarios = len(df_usuarios)
total_solicitudes = len(df_solicitudes)
total_casos = len(df_casos)
casos_pendientes = (
    int((df_casos["status"] == "pending").sum())
    if not df_casos.empty and "status" in df_casos
    else 0
)
casos_asignados = (
    int((df_casos["status"] == "assigned").sum())
    if not df_casos.empty and "status" in df_casos
    else 0
)

if df_solicitudes.empty or "result" not in df_solicitudes:
    preaprobadas = observadas = no_cumplen = 0
else:
    preaprobadas = int((df_solicitudes["result"] == "preaprobado").sum())
    observadas = int((df_solicitudes["result"] == "observado").sum())
    no_cumplen = int((df_solicitudes["result"] == "no_cumple").sum())

resultados_completos = preaprobadas + observadas + no_cumplen
previous_users = count_previous_period(df_usuarios_all, period)
previous_requests = count_previous_period(df_solicitudes_all, period)

st.markdown('<div class="cb-kpi-label">Resumen operativo</div>', unsafe_allow_html=True)
metric_cols = st.columns(4, gap="medium")
metric_cols[0].metric(
    "Usuarios",
    total_usuarios,
    delta=comparison_delta(total_usuarios, previous_users),
    delta_color="off",
)
metric_cols[1].metric(
    "Solicitudes",
    total_solicitudes,
    delta=comparison_delta(total_solicitudes, previous_requests),
    delta_color="off",
)
metric_cols[2].metric("Casos abiertos", total_casos)
metric_cols[3].metric("Pendientes", casos_pendientes)

st.markdown(
    '<div class="cb-kpi-label cb-kpi-status">Resultado de solicitudes</div>',
    unsafe_allow_html=True,
)
status_cols = st.columns(4, gap="medium")
status_cols[0].metric(
    f"Preaprobadas · {percentage(preaprobadas, resultados_completos):.1f}%",
    preaprobadas,
)
status_cols[1].metric(
    f"Observadas · {percentage(observadas, resultados_completos):.1f}%",
    observadas,
)
status_cols[2].metric(
    f"No cumplen · {percentage(no_cumplen, resultados_completos):.1f}%",
    no_cumplen,
)
status_cols[3].metric("En atención", casos_asignados)

with st.container(key="dashboard_operations"):
    left, right = st.columns([1.35, 0.65], gap="large")

    with left:
        st.markdown(
            '<div class="cb-section-head"><div class="cb-section-title">Solicitudes recientes</div><div class="cb-section-note">Últimos 8 registros</div></div>',
            unsafe_allow_html=True,
        )
        if df_solicitudes.empty:
            render_empty_state("No existen solicitudes en el periodo seleccionado.")
        else:
            recent_columns = [
                column
                for column in ["created_at", "cedula", "requested_amount", "result", "status"]
                if column in df_solicitudes
            ]
            display_df = df_solicitudes[recent_columns].head(8).copy()
            if "created_at" in display_df:
                display_df["created_at"] = display_df["created_at"].map(format_datetime)
            if "requested_amount" in display_df:
                display_df["requested_amount"] = pd.to_numeric(
                    display_df["requested_amount"], errors="coerce"
                )
            if "result" in display_df:
                display_df["result"] = display_df["result"].map(translate_result)
            if "status" in display_df:
                display_df["status"] = display_df["status"].map(translate_request_status)
            display_df = display_df.rename(
                columns={
                    "created_at": "Fecha",
                    "cedula": "Cédula",
                    "requested_amount": "Monto",
                    "result": "Resultado",
                    "status": "Estado",
                }
            )
            st.dataframe(
                display_df,
                width="stretch",
                height=318,
                hide_index=True,
                column_config={
                    "Fecha": st.column_config.TextColumn("Fecha", width="medium"),
                    "Cédula": st.column_config.TextColumn("Cédula", width="small"),
                    "Monto": st.column_config.NumberColumn("Monto", format="$ %.0f"),
                    "Resultado": st.column_config.TextColumn("Resultado", width="small"),
                    "Estado": st.column_config.TextColumn("Estado", width="small"),
                },
            )
        st.page_link(
            "pages/2_Solicitudes.py",
            label="Ver todas las solicitudes",
            icon="↗",
            width="stretch",
        )

    with right:
        st.markdown(
            f'<div class="cb-section-head"><div class="cb-section-title">Atención humana</div><div class="cb-section-note">{casos_pendientes} pendientes</div></div>',
            unsafe_allow_html=True,
        )
        if df_casos.empty:
            render_empty_state("No hay casos abiertos en el periodo seleccionado.")
        else:
            for _, case in df_casos.head(4).iterrows():
                case_id = str(case.get("id") or "")
                priority, priority_class = case_priority(case.get("reason"))
                status_raw = str(case.get("status") or "pending")
                status_class = "cb-pill-yellow" if status_raw == "pending" else "cb-pill-green"
                with st.container(border=True, key=f"summary_case_{case_id}"):
                    st.markdown(
                        f"""
                        <div class="cb-case-summary">
                          <div><strong>Caso {escape(case_id[:8])}</strong><small>{escape(translate_case_reason(case.get('reason')))}</small></div>
                          <div class="cb-case-pills">
                            <span class="cb-pill {priority_class}">Prioridad {priority}</span>
                            <span class="cb-pill {status_class}">{escape(translate_case_status(status_raw))}</span>
                          </div>
                          <span class="cb-case-age">{escape(relative_time(case.get('created_at')))}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("Abrir caso", key=f"open_summary_{case_id}", width="stretch"):
                        st.session_state["selected_handoff_case_id"] = case_id
                        st.switch_page("pages/3_Casos_Derivados.py")
        st.page_link(
            "pages/3_Casos_Derivados.py",
            label="Ver todos los casos",
            icon="↗",
            width="stretch",
        )

st.markdown(
    '<div class="cb-section-head"><div class="cb-section-title">Distribución de resultados</div><div class="cb-section-note">Total y participación del periodo</div></div>',
    unsafe_allow_html=True,
)
summary = pd.DataFrame(
    [
        {"Resultado": "Preaprobadas", "Total": preaprobadas},
        {"Resultado": "Observadas", "Total": observadas},
        {"Resultado": "No cumplen", "Total": no_cumplen},
    ]
)
summary["Porcentaje"] = summary["Total"].map(
    lambda value: percentage(value, resultados_completos)
)
summary["Etiqueta"] = summary.apply(
    lambda row: f"{int(row['Total'])} · {row['Porcentaje']:.1f}%", axis=1
)
chart = px.bar(
    summary.sort_values("Total", ascending=True),
    x="Total",
    y="Resultado",
    orientation="h",
    color="Resultado",
    color_discrete_map={
        "Preaprobadas": "#19a96b",
        "Observadas": "#e6a23c",
        "No cumplen": "#d64545",
    },
    text="Etiqueta",
    custom_data=["Porcentaje"],
)
maximum = max(int(summary["Total"].max()), 1)
chart.update_traces(
    textposition="outside",
    textfont={"size": 13, "color": "#14251d"},
    marker_line_width=0,
    cliponaxis=False,
    hovertemplate="<b>%{y}</b><br>Solicitudes: %{x}<br>Participación: %{customdata[0]:.1f}%<extra></extra>",
    hoverlabel={"bgcolor": "#14251d", "font": {"color": "#ffffff"}},
)
chart.update_layout(
    height=280,
    margin={"l": 12, "r": 50, "t": 16, "b": 10},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"family": "Manrope, sans-serif", "color": "#14251d"},
    showlegend=False,
    bargap=0.42,
    transition={"duration": 550, "easing": "cubic-in-out"},
    xaxis={
        "title": None,
        "range": [0, maximum * 1.22],
        "showgrid": True,
        "gridcolor": "#e7eee9",
        "zeroline": False,
        "showticklabels": False,
        "fixedrange": True,
    },
    yaxis={"title": None, "showgrid": False, "fixedrange": True},
)
st.plotly_chart(chart, width="stretch", config={"displayModeBar": False, "responsive": True})
