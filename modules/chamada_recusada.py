"""
Módulo: Chamada Recusada (placeholder)
========================================
Estrutura de exemplo — troque o corpo de render() pela sua lógica
real de consulta (provavelmente uma variação do buscar_cdr filtrando
por status "Recusada"/"Perdida").
"""

import streamlit as st


def render():
    st.title("🚫 Chamada Recusada")
    st.caption("Chamadas não atendidas por período/fila")

    data_inicio = st.date_input("Data inicial", key="rec_data_inicio")
    data_fim = st.date_input("Data final", key="rec_data_fim")

    if st.button("Buscar"):
        with st.spinner("Consultando chamadas recusadas..."):
            # TODO: reaproveitar a função buscar_cdr do módulo
            # analise_chamadas.py, filtrando status == "Recusada"
            st.info("Implementar consulta real aqui.")
