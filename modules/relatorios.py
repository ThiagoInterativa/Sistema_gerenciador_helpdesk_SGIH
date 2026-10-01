"""
Módulo: Visão Geral
====================
Esta é a ÚNICA tela que roda automaticamente ao abrir o SGIH.
Deve conter só o que é "leve" e realmente precisa ser monitorado
o tempo todo: status dos agentes no PABX, tarefas do Kanban e
status do WhatsApp.

Use st.cache_data(ttl=...) para não bater no servidor de origem
a cada rerender/clique do usuário - só quando o tempo (ttl) expira.
"""

import streamlit as st

# Importe aqui as funções reais do seu app.py atual:
# from core.pabx import login, get_agentes
# from core.kanban import login_kanban, get_tarefas_kanban
# from core.whatsflux import login_e_get_status_whatsflux


def render(refresh_rate: int):
    st.title("Relatórios")
   
    # o refresh_rate entra como parte da "chave" do cache: quando o
    # usuário muda o slider, o cache é invalidado e busca de novo.
    agentes = _status_pabx_cache(refresh_rate)
    tarefas = _status_kanban_cache(refresh_rate)
    whatsapp = _status_whatsapp_cache(refresh_rate)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("☎️ Status PABX")
        for nome, status in agentes:
            cor = {"livre": "🟢", "ocupado": "🔴", "pausa": "🟡"}.get(status, "⚪")
            st.write(f"{cor} {nome} — {status}")

    with col2:
        st.subheader("🗂️ Tarefas Kanban")
        for t in tarefas:
            st.write(f"• {t['titulo']} ({t['coluna']})")

    with col3:
        st.subheader("💬 WhatsApp")
        for nome, status in whatsapp.items():
            cor = "🟢" if status == "online" else "⚪"
            st.write(f"{cor} {nome} — {status}")
