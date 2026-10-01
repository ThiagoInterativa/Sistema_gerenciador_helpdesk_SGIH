import streamlit as st


# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def render():

    # ==========================================================
    # CSS
    # ==========================================================
    #
    # Aqui alteramos somente a aparência dos componentes.
    #
    # IMPORTANTE:
    # Não estamos colocando HTML dos cards aqui.
    # Os textos serão criados usando st.markdown(),
    # st.caption() e st.link_button().
    # ==========================================================

    st.markdown("""
    <style>

    /* ======================================================
       TÍTULO DOS CARDS
       ====================================================== */

    .link-titulo {
        height: 55px;
        display: flex;
        align-items: flex-start;
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        line-height: 24px;
    }


    /* ======================================================
       DESCRIÇÃO DOS CARDS
       ====================================================== */

    .link-descricao {
        height: 55px;
        color: #9ca3af;
        font-size: 13px;
        line-height: 19px;
    }


    /* ======================================================
       ESPAÇAMENTO DOS BOTÕES
       ====================================================== */

    div.stLinkButton {
        margin-top: 5px;
    }

    </style>
    """, unsafe_allow_html=True)



    # ==========================================================
    # ==========================================================
    # PLANILHAS
    # ==========================================================
    # ==========================================================

    st.subheader("📊 Planilhas")


    # ----------------------------------------------------------
    # CRIA AS 3 COLUNAS
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    # ==========================================================
    # COLUNA 1
    # CONTROLE DE ATENDIMENTOS
    # ==========================================================

    with col1:

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        st.markdown(
            '<div class="link-titulo">'
            '📊 Controle de Atendimentos'
            '</div>',
            unsafe_allow_html=True
        )

        # ------------------------------------------------------
        # DESCRIÇÃO
        # ------------------------------------------------------

        st.markdown(
            '<div class="link-descricao">'
            'Acompanhamento dos atendimentos do ServiceDesk.'
            '</div>',
            unsafe_allow_html=True
        )

        # ------------------------------------------------------
        # BOTÃO
        # ------------------------------------------------------

        st.link_button(
            "Abrir planilha ↗",
            "https://docs.google.com/spreadsheets/d/1Bu53-IPht9-Z4bn1bfXXMBHVeM2sOTQ_NQ3YjyUBF94/edit?gid=1048802781#gid=1048802781",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 2
    # ESCALA
    # ==========================================================

    with col2:

        st.markdown(
            '<div class="link-titulo">'
            '📊 Escala'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="link-descricao">'
            'Planilha de escala da equipe.'
            '</div>',
            unsafe_allow_html=True
        )

        st.link_button(
            "Abrir planilha ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 3
    # INDICADORES
    # ==========================================================

    with col3:

        st.markdown(
            '<div class="link-titulo">'
            '📊 Indicadores'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="link-descricao">'
            'Indicadores e acompanhamento.'
            '</div>',
            unsafe_allow_html=True
        )

        st.link_button(
            "Abrir planilha ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # SEPARADOR
    # ==========================================================

    st.divider()


    # ==========================================================
    # ==========================================================
    # FORMULÁRIOS
    # ==========================================================
    # ==========================================================

    st.subheader("📝 Formulários")


    # ----------------------------------------------------------
    # CRIA NOVAMENTE 3 COLUNAS
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    # ==========================================================
    # COLUNA 1
    # SOLICITAÇÃO
    # ==========================================================

    with col1:

        st.markdown(
            '<div class="link-titulo">'
            '📝 Solicitação'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="link-descricao">'
            'Formulário para abertura de solicitações.'
            '</div>',
            unsafe_allow_html=True
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 2
    # ATENDIMENTO
    # ==========================================================

    with col2:

        st.markdown(
            '<div class="link-titulo">'
            '📝 Atendimento'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="link-descricao">'
            'Formulário de registro de atendimento.'
            '</div>',
            unsafe_allow_html=True
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )


    # ==========================================================
    # COLUNA 3
    # PESQUISA
    # ==========================================================

    with col3:

        st.markdown(
            '<div class="link-titulo">'
            '📝 Pesquisa'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="link-descricao">'
            'Pesquisa de satisfação.'
            '</div>',
            unsafe_allow_html=True
        )

        st.link_button(
            "Abrir formulário ↗",
            "COLOQUE_AQUI_A_URL",
            use_container_width=True
        )
