"""Trazabilidad de invocaciones de herramientas y decisiones automatizadas."""
import json

import pandas as pd
import streamlit as st

from components.auth import require_auth
from components.navigation import render_sidebar
from components.presentation import (
    filter_by_period,
    format_datetime,
    percentage,
    redact_payload,
    safe_value,
)
from components.ui import (
    render_data_toolbar,
    render_empty_state,
    render_page_header,
    render_period_selector,
)
from services.supabase_dashboard import DashboardConfigError, obtener_auditoria_ia
from styles import apply_dashboard_styles


def _payload_value(value: object) -> object:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return value
    return redact_payload(value)


st.set_page_config(page_title="Auditoría IA - CrediBot", page_icon="🛡️", layout="wide")
apply_dashboard_styles()
require_auth()
render_sidebar()

render_page_header(
    "Control y trazabilidad",
    "Auditoría IA",
    "Revisa herramientas, resultados y tiempos de respuesta sin exponer credenciales ni datos sensibles.",
)

try:
    logs = obtener_auditoria_ia()
except DashboardConfigError as exc:
    st.warning(str(exc))
    st.stop()
except Exception as exc:
    st.error(f"No se pudo consultar la auditoría: {exc}")
    st.stop()

df_all = pd.DataFrame(logs)
if df_all.empty:
    render_empty_state("Todavía no existen eventos de auditoría.")
    st.stop()

render_data_toolbar("audit")

st.markdown('<div class="cb-section-title">Filtros</div>', unsafe_allow_html=True)
with st.container(key="audit_filters"):
    period_col, tool_col, result_col = st.columns([1.3, 1.2, 1])
    with period_col:
        period = render_period_selector("audit_period")
    tools = sorted(df_all["tool_name"].dropna().astype(str).unique()) if "tool_name" in df_all else []
    selected_tool = tool_col.selectbox("Herramienta", ["Todas", *tools])
    selected_status = result_col.selectbox("Resultado", ["Todos", "Correctos", "Con error"])

filtered = filter_by_period(df_all, period)
if selected_tool != "Todas" and "tool_name" in filtered:
    filtered = filtered[filtered["tool_name"] == selected_tool]
if selected_status == "Correctos" and "success" in filtered:
    filtered = filtered[filtered["success"].fillna(False)]
elif selected_status == "Con error" and "success" in filtered:
    filtered = filtered[~filtered["success"].fillna(False)]

success_count = int(filtered["success"].fillna(False).sum()) if "success" in filtered else 0
error_count = len(filtered) - success_count
average_latency = (
    filtered["latency_ms"].dropna().mean()
    if "latency_ms" in filtered and not filtered["latency_ms"].dropna().empty
    else None
)
metric_cols = st.columns(4)
metric_cols[0].metric("Invocaciones", len(filtered))
metric_cols[1].metric(
    f"Correctas · {percentage(success_count, len(filtered)):.1f}%",
    success_count,
)
metric_cols[2].metric("Con error", error_count)
metric_cols[3].metric(
    "Latencia promedio",
    f"{average_latency:.0f} ms" if average_latency is not None else "—",
)

st.markdown(
    '<div class="cb-section-head"><div class="cb-section-title">Registro de actividad</div><div class="cb-section-note">Selecciona un evento para inspeccionar sus payloads protegidos</div></div>',
    unsafe_allow_html=True,
)
if filtered.empty:
    render_empty_state("No hay eventos que coincidan con los filtros.")
else:
    visible = [
        column
        for column in ("created_at", "tool_name", "success", "latency_ms", "conversation_id")
        if column in filtered
    ]
    display_df = filtered[visible].copy().reset_index(drop=True)
    if "created_at" in display_df:
        display_df["created_at"] = display_df["created_at"].map(format_datetime)
    if "success" in display_df:
        display_df["success"] = display_df["success"].fillna(False).map({True: "Correcto", False: "Error"})
    if "conversation_id" in display_df:
        display_df["conversation_id"] = display_df["conversation_id"].fillna("—").astype(str).str[:8]
    display_df = display_df.rename(
        columns={
            "created_at": "Fecha",
            "tool_name": "Herramienta",
            "success": "Resultado",
            "latency_ms": "Latencia",
            "conversation_id": "Conversación",
        }
    )
    event = st.dataframe(
        display_df,
        width="stretch",
        height=430,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="audit_table",
        column_config={
            "Fecha": st.column_config.TextColumn(width="medium"),
            "Herramienta": st.column_config.TextColumn(width="medium"),
            "Latencia": st.column_config.NumberColumn(format="%d ms", width="small"),
            "Conversación": st.column_config.TextColumn(width="small"),
        },
    )
    selected_rows = event.selection.rows if event and hasattr(event, "selection") else []
    if selected_rows:
        selected = filtered.reset_index(drop=True).iloc[selected_rows[0]]
        with st.container(border=True, key="audit_detail"):
            st.markdown('<div class="cb-section-title">Detalle del evento</div>', unsafe_allow_html=True)
            detail_left, detail_right = st.columns(2)
            detail_left.markdown(f"**Herramienta**  \n{safe_value(selected.get('tool_name'))}")
            detail_left.markdown(f"**Fecha**  \n{format_datetime(selected.get('created_at'))}")
            selected_success = selected.get("success")
            success_label = (
                "Correcto"
                if selected_success is not None and not pd.isna(selected_success) and bool(selected_success)
                else "Error"
            )
            detail_right.markdown(f"**Resultado**  \n{success_label}")
            detail_right.markdown(f"**Latencia**  \n{safe_value(selected.get('latency_ms'), '—')} ms")
            with st.expander("Payload de entrada"):
                st.json(_payload_value(selected.get("input_payload")), expanded=True)
            with st.expander("Payload de salida"):
                st.json(_payload_value(selected.get("output_payload")), expanded=True)
