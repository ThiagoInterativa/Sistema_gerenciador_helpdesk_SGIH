"""
Módulo: Ligação por Ramal (placeholder)
=========================================
"""

import streamlit as st


def render():
    st.title("☎️ Ligação por Ramal")
    st.caption("Consulta de chamadas de um ramal específico")

    ramal = st.text_input("Número do ramal")

    if st.button("Buscar") and ramal:
        with st.spinner(f"Consultando chamadas do ramal {ramal}..."):
            # TODO: reaproveitar buscar_cdr filtrando ramal_origem=ramal
            st.info("Implementar consulta real aqui.")
