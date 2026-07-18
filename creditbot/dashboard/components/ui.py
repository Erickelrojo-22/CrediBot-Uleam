"""Componentes pequeños y reutilizables del dashboard."""
from datetime import timedelta

import streamlit as st

from components.presentation import (
    PERIOD_ALL,
    PERIOD_CUSTOM,
    PERIOD_OPTIONS,
    PeriodRange,
    build_period_range,
    now_local,
)


def render_page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="cb-hero">
          <div class="cb-eyebrow">{eyebrow}</div>
          <div class="cb-hero-title">{title}</div>
          <p class="cb-hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_period_selector(key: str, *, label: str = "Periodo") -> PeriodRange:
    option = st.selectbox(label, PERIOD_OPTIONS, index=0, key=f"{key}_option")
    custom_dates = None
    if option == PERIOD_CUSTOM:
        today = now_local().date()
        custom_dates = st.date_input(
            "Rango de fechas",
            value=(today - timedelta(days=29), today),
            max_value=today,
            key=f"{key}_dates",
        )
    return build_period_range(option or PERIOD_ALL, custom_dates)


def render_empty_state(message: str) -> None:
    st.markdown(f'<div class="cb-empty-state">{message}</div>', unsafe_allow_html=True)


def render_data_toolbar(key: str, *, show_simulator: bool = True) -> bool:
    """Muestra estado de consulta, acceso rápido y actualización manual."""
    status_col, simulator_col, refresh_col = st.columns(
        [2.3, 1.2, 0.8] if show_simulator else [3.2, 0.8],
        vertical_alignment="center",
    )
    with status_col:
        st.markdown(
            f"""
            <div class="cb-toolbar-status">
              <span class="cb-sidebar-live"></span>
              <div><strong>Datos sincronizados</strong><small>Última consulta {now_local().strftime('%H:%M')}</small></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if show_simulator:
        with simulator_col:
            st.page_link(
                "pages/1_Simulador.py",
                label="Abrir simulador",
                icon="💬",
                width="stretch",
            )
    with refresh_col:
        return st.button("Actualizar", key=f"{key}_refresh", width="stretch")
