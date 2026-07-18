"""Página del dashboard para buscar y revisar usuarios."""
import pandas as pd
import streamlit as st

from components.auth import require_auth
from components.navigation import render_sidebar
from components.presentation import (
    filter_by_period,
    format_datetime,
    mask_cedula,
    mask_phone,
    safe_value,
)
from components.ui import (
    render_data_toolbar,
    render_empty_state,
    render_page_header,
    render_period_selector,
)
from services.supabase_dashboard import DashboardConfigError, obtener_usuarios
from styles import apply_dashboard_styles


st.set_page_config(page_title="Usuarios - CrediBot", page_icon="CB", layout="wide")
apply_dashboard_styles()
require_auth()
render_sidebar()

render_page_header(
    "Base de clientes",
    "Usuarios",
    "Consulta los clientes que han interactuado con CrediBot y revisa su consentimiento.",
)

try:
    usuarios = obtener_usuarios()
except DashboardConfigError as exc:
    st.warning(str(exc))
    st.stop()
except Exception as exc:
    st.error(f"No se pudo consultar Supabase: {exc}")
    st.stop()

df_all = pd.DataFrame(usuarios)
if df_all.empty:
    render_empty_state("No existen usuarios registrados.")
    st.stop()

render_data_toolbar("users")

st.markdown('<div class="cb-section-title">Búsqueda y filtros</div>', unsafe_allow_html=True)
with st.container(key="users_filters"):
    period_col, search_col = st.columns([1.2, 1.8])
    with period_col:
        period = render_period_selector("users_period")
    search = search_col.text_input(
        "Buscar usuario",
        placeholder="Nombre, teléfono o cédula",
    ).strip().lower()
    consent_col, cedula_col = st.columns(2)
    consent_filter = consent_col.selectbox(
        "Consentimiento",
        ["Todos", "Otorgado", "No otorgado"],
    )
    cedula_filter = cedula_col.selectbox(
        "Cédula registrada",
        ["Todos", "Con cédula", "Sin cédula"],
    )

filtered_df = filter_by_period(df_all, period)
if search:
    searchable = pd.Series(False, index=filtered_df.index)
    for column in ("full_name", "phone", "cedula"):
        if column in filtered_df:
            searchable = searchable | filtered_df[column].fillna("").astype(str).str.lower().str.contains(
                search, regex=False
            )
    filtered_df = filtered_df[searchable]

if consent_filter != "Todos" and "consent_given" in filtered_df:
    consent = filtered_df["consent_given"].fillna(False).astype(bool)
    filtered_df = filtered_df[consent] if consent_filter == "Otorgado" else filtered_df[~consent]
if cedula_filter != "Todos" and "cedula" in filtered_df:
    has_cedula = filtered_df["cedula"].fillna("").astype(str).str.strip().ne("")
    filtered_df = filtered_df[has_cedula] if cedula_filter == "Con cédula" else filtered_df[~has_cedula]

metric_cols = st.columns(3)
metric_cols[0].metric("Usuarios mostrados", len(filtered_df))
metric_cols[1].metric(
    "Con cédula",
    int(filtered_df["cedula"].notna().sum()) if "cedula" in filtered_df else 0,
)
metric_cols[2].metric(
    "Con consentimiento",
    int(filtered_df["consent_given"].fillna(False).sum()) if "consent_given" in filtered_df else 0,
)

st.markdown(
    '<div class="cb-section-head"><div class="cb-section-title">Directorio</div><div class="cb-section-note">Datos sensibles protegidos en el listado</div></div>',
    unsafe_allow_html=True,
)
if filtered_df.empty:
    render_empty_state("No hay usuarios que coincidan con los filtros.")
else:
    visible_columns = [
        column for column in ("full_name", "phone", "cedula", "consent_given", "created_at") if column in filtered_df
    ]
    display_df = filtered_df[visible_columns].copy().reset_index(drop=True)
    if "phone" in display_df:
        display_df["phone"] = display_df["phone"].map(mask_phone)
    if "cedula" in display_df:
        display_df["cedula"] = display_df["cedula"].map(mask_cedula)
    if "consent_given" in display_df:
        display_df["consent_given"] = display_df["consent_given"].fillna(False).map({True: "Sí", False: "No"})
    if "created_at" in display_df:
        display_df["created_at"] = display_df["created_at"].map(format_datetime)
    display_df = display_df.rename(
        columns={
            "full_name": "Nombre",
            "phone": "Teléfono",
            "cedula": "Cédula",
            "consent_given": "Consentimiento",
            "created_at": "Registro",
        }
    )
    event = st.dataframe(
        display_df,
        width="stretch",
        height=430,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="users_table",
        column_config={
            "Nombre": st.column_config.TextColumn(width="medium"),
            "Teléfono": st.column_config.TextColumn(width="small"),
            "Cédula": st.column_config.TextColumn(width="small"),
            "Registro": st.column_config.TextColumn(width="medium"),
        },
    )
    selected_rows = event.selection.rows if event and hasattr(event, "selection") else []
    if selected_rows:
        selected = filtered_df.reset_index(drop=True).iloc[selected_rows[0]]
        with st.container(border=True, key="user_detail"):
            st.markdown('<div class="cb-section-title">Ficha del usuario</div>', unsafe_allow_html=True)
            detail_left, detail_right = st.columns(2)
            detail_left.markdown(f"**Nombre**  \n{safe_value(selected.get('full_name'))}")
            detail_left.markdown(f"**Teléfono**  \n{safe_value(selected.get('phone'))}")
            detail_left.markdown(f"**Cédula**  \n{safe_value(selected.get('cedula'))}")
            consent_value = selected.get("consent_given")
            consent = "Otorgado" if consent_value is not None and not pd.isna(consent_value) and bool(consent_value) else "No otorgado"
            detail_right.markdown(f"**Consentimiento**  \n{consent}")
            detail_right.markdown(f"**Fecha de consentimiento**  \n{format_datetime(selected.get('consent_at'))}")
            detail_right.markdown(f"**Registrado**  \n{format_datetime(selected.get('created_at'))}")
