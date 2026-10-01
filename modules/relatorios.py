"""
Módulo: Ligação por Ramal (placeholder)
=========================================
"""

import streamlit as st


def render():
    st.title("📈 Relatórios")
    st.caption("Área de relatórios do sistema")

    ramal = st.text_input("Número do ramal")

    if st.button("Buscar") and ramal:
        with st.spinner(f"Consultando chamadas do ramal {ramal}..."):
            # TODO: reaproveitar buscar_cdr filtrando ramal_origem=ramal
            st.info("Implementar consulta real aqui.")
