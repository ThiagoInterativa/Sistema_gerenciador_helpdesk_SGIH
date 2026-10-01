import streamlit as st


def render():

    # ==========================================================
    # CSS DOS CARDS
    # ==========================================================

    st.markdown("""
    <style>

    /* --------------------------------------------------------
       CARD DOS LINKS
       -------------------------------------------------------- */

    .link-card {
        background-color: #111827;
        border: 1px solid #263244;
        border-radius: 10px;
        padding: 18px;
        height: 210px;
        margin-bottom: 10px;
        box-sizing: border-box;
    }


    /* --------------------------------------------------------
       TÍTULO DO CARD
       Todos terão a mesma altura.
       -------------------------------------------------------- */

    .link-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        height: 50px;
        line-height: 25px;
        margin-bottom: 5px;
    }


    /* --------------------------------------------------------
       DESCRIÇÃO
       Todos terão a mesma altura.
       -------------------------------------------------------- */

    .link-description {
        color: #9ca3af;
        font-size: 13px;
        line-height: 20px;
        height: 60px;
        margin-bottom: 12px;
    }


    /* --------------------------------------------------------
       BOTÃO
       -------------------------------------------------------- */

    .link-button {
        width: 100%;
    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================================
    # PLANILHAS
    # ==========================================================

    st.subheader("📊 Planilhas")

    col1, col2, col3 = st.columns(3)


    # ==========================================================
    # COLUNA 1
    # ==========================================================

    with col1:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📊 Controle de Atendimentos
            </div>

            <div class="link-description">
                Acompanhamento dos atendimentos do ServiceDesk.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Abrir planilha ↗",
            "https://docs.google.com/spreadsheets/d/1Bu53-IPht9-Z4bn1bfXXMBHVeM2sOTQ_NQ3YjyUBF94/edit?gid=1048802781#gid=1048802781",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 2
    # ==========================================================

    with col2:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📊 Escala
            </div>

            <div class="link-description">
                Planilha de escala da equipe.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Abrir planilha ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 3
    # ==========================================================

    with col3:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📊 Indicadores
            </div>

            <div class="link-description">
                Indicadores e acompanhamento.
            </div>

        </div>
        """, unsafe_allow_html=True)

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


    # ==========================================================
    # FORMULÁRIO 1
    # ==========================================================

    with col1:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📝 Solicitação
            </div>

            <div class="link-description">
                Formulário para abertura de solicitações.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # FORMULÁRIO 2
    # ==========================================================

    with col2:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📝 Atendimento
            </div>

            <div class="link-description">
                Formulário de registro de atendimento.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # FORMULÁRIO 3
    # ==========================================================

    with col3:

        st.markdown("""
        <div class="link-card">

            <div class="link-title">
                📝 Pesquisa
            </div>

            <div class="link-description">
                Pesquisa de satisfação.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )
