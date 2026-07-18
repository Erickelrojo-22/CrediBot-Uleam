"""Página del dashboard que lista y filtra solicitudes de crédito."""
import pandas as pd
import streamlit as st

from components.auth import require_auth
from components.navigation import render_sidebar
from components.presentation import (
    filter_by_period,
    format_datetime,
    format_money,
    format_term,
    safe_value,
    translate_request_status,
    translate_result,
)
from components.ui import (
    render_data_toolbar,
    render_empty_state,
    render_page_header,
    render_period_selector,
)
from services.supabase_dashboard import (
    DashboardConfigError,
    obtener_casos_derivados,
    obtener_solicitudes,
)
from styles import apply_dashboard_styles


st.set_page_config(page_title="Solicitudes - CrediBot", page_icon="CB", layout="wide")
apply_dashboard_styles()
require_auth()
render_sidebar()

render_page_header(
    "Gestión crediticia",
    "Solicitudes de Crédito",
    "Consulta, filtra y revisa las precalificaciones procesadas por CrediBot.",
)

try:
    solicitudes = obtener_solicitudes()
    casos_derivados = obtener_casos_derivados()
except DashboardConfigError as exc:
    st.warning(str(exc))
    st.stop()
except Exception as exc:
    st.error(f"No se pudo consultar Supabase: {exc}")
    st.stop()

df_all = pd.DataFrame(solicitudes)
df_casos = pd.DataFrame(casos_derivados)
if df_all.empty:
    render_empty_state("No existen solicitudes registradas.")
    st.stop()

render_data_toolbar("requests")

derived_request_ids: set[str] = set()
if not df_casos.empty and "credit_request_id" in df_casos:
    derived_request_ids = set(df_casos["credit_request_id"].dropna().astype(str))
df_all["derivado_asesor"] = (
    df_all["id"].astype(str).isin(derived_request_ids) if "id" in df_all else False
)

st.markdown('<div class="cb-section-title">Filtros</div>', unsafe_allow_html=True)
with st.container(key="requests_filters"):
    filter_period, filter_search, filter_result = st.columns([1.3, 1.6, 1])
    with filter_period:
        period = render_period_selector("requests_period")
    search = filter_search.text_input(
        "Buscar",
        placeholder="Cédula, solicitud o usuario",
    ).strip().lower()
    result_label = filter_result.selectbox(
        "Resultado",
        ["Todos", "Preaprobada", "Observada", "No cumple"],
    )
    filter_status, filter_handoff = st.columns(2)
    status_label = filter_status.selectbox(
        "Estado",
        ["Todos", "En progreso", "Completada"],
    )
    handoff_label = filter_handoff.selectbox(
        "Derivación",
        ["Todos", "Derivadas", "No derivadas"],
    )

filtered_df = filter_by_period(df_all, period)
if search:
    searchable = pd.Series(False, index=filtered_df.index)
    for column in ("cedula", "id", "user_id"):
        if column in filtered_df:
            searchable = searchable | filtered_df[column].fillna("").astype(str).str.lower().str.contains(
                search, regex=False
            )
    filtered_df = filtered_df[searchable]

result_values = {"Preaprobada": "preaprobado", "Observada": "observado", "No cumple": "no_cumple"}
status_values = {"En progreso": "draft", "Completada": "completed"}
if result_label != "Todos" and "result" in filtered_df:
    filtered_df = filtered_df[filtered_df["result"] == result_values[result_label]]
if status_label != "Todos" and "status" in filtered_df:
    filtered_df = filtered_df[filtered_df["status"] == status_values[status_label]]
if handoff_label == "Derivadas":
    filtered_df = filtered_df[filtered_df["derivado_asesor"]]
elif handoff_label == "No derivadas":
    filtered_df = filtered_df[~filtered_df["derivado_asesor"]]

metric_cols = st.columns(4)
metric_cols[0].metric("Solicitudes mostradas", len(filtered_df))
metric_cols[1].metric(
    "Preaprobadas",
    int((filtered_df["result"] == "preaprobado").sum()) if "result" in filtered_df else 0,
)
metric_cols[2].metric(
    "Observadas",
    int((filtered_df["result"] == "observado").sum()) if "result" in filtered_df else 0,
)
metric_cols[3].metric(
    "Derivadas",
    int(filtered_df["derivado_asesor"].sum()) if "derivado_asesor" in filtered_df else 0,
)

st.markdown(
    '<div class="cb-section-head"><div class="cb-section-title">Listado</div><div class="cb-section-note">Selecciona una fila para revisar el detalle</div></div>',
    unsafe_allow_html=True,
)
if filtered_df.empty:
    render_empty_state("No hay solicitudes que coincidan con los filtros.")
else:
    visible_columns = [
        column
        for column in (
            "id",
            "cedula",
            "requested_amount",
            "term_months",
            "result",
            "status",
            "derivado_asesor",
            "created_at",
        )
        if column in filtered_df
    ]
    display_df = filtered_df[visible_columns].copy().reset_index(drop=True)
    if "id" in display_df:
        display_df["id"] = display_df["id"].astype(str).str[:8]
    if "created_at" in display_df:
        display_df["created_at"] = display_df["created_at"].map(format_datetime)
    if "requested_amount" in display_df:
        display_df["requested_amount"] = pd.to_numeric(display_df["requested_amount"], errors="coerce")
    if "term_months" in display_df:
        display_df["term_months"] = pd.to_numeric(display_df["term_months"], errors="coerce")
    if "result" in display_df:
        display_df["result"] = display_df["result"].map(translate_result)
    if "status" in display_df:
        display_df["status"] = display_df["status"].map(translate_request_status)
    if "derivado_asesor" in display_df:
        display_df["derivado_asesor"] = display_df["derivado_asesor"].map({True: "Sí", False: "No"})
    display_df = display_df.rename(
        columns={
            "id": "Solicitud",
            "cedula": "Cédula",
            "requested_amount": "Monto",
            "term_months": "Plazo",
            "result": "Resultado",
            "status": "Estado",
            "derivado_asesor": "Derivada",
            "created_at": "Fecha",
        }
    )
    event = st.dataframe(
        display_df,
        width="stretch",
        height=420,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="requests_table",
        column_config={
            "Solicitud": st.column_config.TextColumn(width="small"),
            "Cédula": st.column_config.TextColumn(width="small"),
            "Monto": st.column_config.NumberColumn(format="$ %.0f", width="small"),
            "Plazo": st.column_config.NumberColumn(format="%d meses", width="small"),
            "Fecha": st.column_config.TextColumn(width="medium"),
        },
    )

    selected_rows = event.selection.rows if event and hasattr(event, "selection") else []
    if selected_rows:
        selected = filtered_df.reset_index(drop=True).iloc[selected_rows[0]]
        with st.container(border=True, key="request_detail"):
            st.markdown('<div class="cb-section-title">Detalle de la solicitud</div>', unsafe_allow_html=True)
            detail_a, detail_b, detail_c = st.columns(3)
            detail_a.markdown(f"**Solicitud**  \n{safe_value(selected.get('id'))}")
            detail_a.markdown(f"**Usuario**  \n{safe_value(selected.get('user_id'))}")
            detail_a.markdown(f"**Creada**  \n{format_datetime(selected.get('created_at'))}")
            detail_b.markdown(f"**Monto solicitado**  \n{format_money(selected.get('requested_amount'))}")
            detail_b.markdown(f"**Plazo**  \n{format_term(selected.get('term_months'))}")
            detail_b.markdown(f"**Ingreso mensual**  \n{format_money(selected.get('monthly_income'))}")
            detail_c.markdown(f"**Resultado**  \n{translate_result(selected.get('result'))}")
            detail_c.markdown(f"**Estado**  \n{translate_request_status(selected.get('status'))}")
            detail_c.markdown(f"**Cuota estimada**  \n{format_money(selected.get('estimated_payment'))}")

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar resultados filtrados",
        data=csv,
        file_name="solicitudes_creditbot.csv",
        mime="text/csv",
    )
