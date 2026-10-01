import streamlit as st


def render():

    st.title("📑 Links úteis")

    st.caption(
        "Acesso rápido às ferramentas utilizadas pelo ServiceDesk"
    )

    # ==========================================================
    # PLANILHAS
    # ==========================================================

    st.subheader("📊 Planilhas")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 📊 Controle de atendimentos")

        st.caption(
            "Acompanhamento dos atendimentos do ServiceDesk."
        )

        st.link_button(
            "Abrir planilha ↗",
            "https://docs.google.com/spreadsheets/d/1Bu53-IPht9-Z4bn1bfXXMBHVeM2sOTQ_NQ3YjyUBF94/edit?gid=1048802781#gid=1048802781",
            use_container_width=True
        )

    with col2:

        st.markdown("### 📊 Escala")

        st.caption(
            "Planilha de escala da equipe."
        )

        st.link_button(
            "Abrir planilha ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )

    with col3:

        st.markdown("### 📊 Indicadores")

        st.caption(
            "Indicadores e acompanhamento."
        )

        st.link_button(
            "Abrir planilha ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # FORMULÁRIOS
    # ==========================================================

    st.divider()

    st.subheader("📝 Formulários")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 📝 Solicitação")

        st.caption(
            "Formulário para abertura de solicitações."
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )

    with col2:

        st.markdown("### 📝 Atendimento")

        st.caption(
            "Formulário de registro de atendimento."
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )

    with col3:

        st.markdown("### 📝 Pesquisa")

        st.caption(
            "Pesquisa de satisfação."
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )
