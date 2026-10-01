import streamlit as st


# ==========================================================
# CONFIGURAÇÃO DOS LINKS
# ==========================================================

LINKS = [

    # ======================================================
    # PLANILHAS
    # ======================================================

    {
        "categoria": "Planilhas",
        "nome": "Controle de desempenho",
        "descricao": "Acompanhamento de indicador por Tecnico",
        "icone": "📊",
        "url": "https://docs.google.com/spreadsheets/d/1Bu53-IPht9-Z4bn1bfXXMBHVeM2sOTQ_NQ3YjyUBF94/edit?gid=1048802781#gid=1048802781",
        "tipo_botao": "Abrir planilha ↗",
        "favorito": True,
    },

    {
        "categoria": "Planilhas",
        "nome": "Ocorrências",
        "descricao": "Planilha de escala da equipe.",
        "icone": "📅",
        "url": "https://docs.google.com/spreadsheets/d/14GuZyNnFwCKFoMg6ZE0j7eojFNK4QBFvImgc-mT2e1o/edit?gid=2108239952#gid=2108239952",
        "tipo_botao": "Abrir planilha ↗",
        "favorito": False,
    },

    {
        "categoria": "Planilhas",
        "nome": "Indicadores",
        "descricao": "Indicadores e acompanhamento.",
        "icone": "📈",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir planilha ↗",
        "favorito": False,
    },


    # ======================================================
    # FORMULÁRIOS
    # ======================================================

    {
        "categoria": "Formulários",
        "nome": "Formulário Kanban",
        "descricao": "Formulário para atualização do Kanban.",
        "icone": "📝",
        "url": "https://form.jotform.com/230283726737663",
        "tipo_botao": "Abrir formulário ↗",
        "favorito": True,
    },

    {
        "categoria": "Formulários",
        "nome": "Solicitação",
        "descricao": "Formulário para abertura de solicitações.",
        "icone": "📝",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir formulário ↗",
        "favorito": False,
    },

    {
        "categoria": "Formulários",
        "nome": "Atendimento",
        "descricao": "Formulário de registro de atendimento.",
        "icone": "📝",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir formulário ↗",
        "favorito": False,
    },


    # ======================================================
    # SISTEMAS
    # ======================================================

    {
        "categoria": "Sistemas",
        "nome": "Sistema de Chamados",
        "descricao": "Acesso ao sistema de chamados.",
        "icone": "🖥️",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir sistema ↗",
        "favorito": True,
    },

    {
        "categoria": "Sistemas",
        "nome": "Portal Corporativo",
        "descricao": "Acesso ao portal corporativo.",
        "icone": "🌐",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir sistema ↗",
        "favorito": False,
    },


    # ======================================================
    # DOCUMENTAÇÃO
    # ======================================================

    {
        "categoria": "Documentação",
        "nome": "Base de Conhecimento",
        "descricao": "Manuais e procedimentos do ServiceDesk.",
        "icone": "📚",
        "url": "COLOQUE_AQUI_A_URL",
        "tipo_botao": "Abrir documentação ↗",
        "favorito": False,
    },

]


# ==========================================================
# NORMALIZAR TEXTO
# ==========================================================

def normalizar(texto):

    return texto.lower().strip()


# ==========================================================
# MOSTRAR UM LINK
# ==========================================================

def mostrar_link(link):

    # ------------------------------------------------------
    # TÍTULO
    # ------------------------------------------------------

    st.markdown(
        f"""
        <div class="link-titulo">
            {link["icone"]} {link["nome"]}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ------------------------------------------------------
    # DESCRIÇÃO
    # ------------------------------------------------------

    st.markdown(
        f"""
        <div class="link-descricao">
            {link["descricao"]}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ------------------------------------------------------
    # BOTÃO
    # ------------------------------------------------------

    st.link_button(
        link["tipo_botao"],
        link["url"],
        use_container_width=True
    )


# ==========================================================
# MOSTRAR LINKS EM 4 COLUNAS
# ==========================================================
#
# Esta é a principal mudança do layout.
#
# Antes:
#
#     3 colunas
#
# Agora:
#
#     Planilhas | Formulários | Sistemas | Documentação
#
# ==========================================================

def mostrar_categorias_em_colunas(
    planilhas,
    formularios,
    sistemas,
    documentacao
):

    # ------------------------------------------------------
    # CRIA AS 4 COLUNAS
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    # ======================================================
    # COLUNA 1 - PLANILHAS
    # ======================================================

    with col1:

        st.markdown(
            "### 📊 Planilhas"
        )

        st.divider()

        for link in planilhas:

            mostrar_link(link)

            st.markdown(
                "<div class='espaco-link'></div>",
                unsafe_allow_html=True
            )


    # ======================================================
    # COLUNA 2 - FORMULÁRIOS
    # ======================================================

    with col2:

        st.markdown(
            "### 📝 Formulários"
        )

        st.divider()

        for link in formularios:

            mostrar_link(link)

            st.markdown(
                "<div class='espaco-link'></div>",
                unsafe_allow_html=True
            )


    # ======================================================
    # COLUNA 3 - SISTEMAS
    # ======================================================

    with col3:

        st.markdown(
            "### 🌐 Sistemas"
        )

        st.divider()

        for link in sistemas:

            mostrar_link(link)

            st.markdown(
                "<div class='espaco-link'></div>",
                unsafe_allow_html=True
            )


    # ======================================================
    # COLUNA 4 - DOCUMENTAÇÃO
    # ======================================================

    with col4:

        st.markdown(
            "### 📚 Documentação"
        )

        st.divider()

        for link in documentacao:

            mostrar_link(link)

            st.markdown(
                "<div class='espaco-link'></div>",
                unsafe_allow_html=True
            )


# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def render():


    # ======================================================
    # CSS
    # ======================================================

    st.markdown(
        """
        <style>

        /* ==================================================
           TÍTULO DO LINK
           ================================================== */

        .link-titulo {

            min-height: 45px;

            display: flex;

            align-items: flex-start;

            font-size: 16px;

            font-weight: 600;

            color: #ffffff;

            line-height: 22px;

        }


        /* ==================================================
           DESCRIÇÃO
           ================================================== */

        .link-descricao {

            min-height: 50px;

            color: #9ca3af;

            font-size: 12px;

            line-height: 18px;

            margin-bottom: 5px;

        }


        /* ==================================================
           ESPAÇO ENTRE OS LINKS
           ================================================== */

        .espaco-link {

            height: 22px;

        }


        /* ==================================================
           BOTÕES
           ================================================== */

        div.stLinkButton {

            margin-top: 4px;

        }


        /* ==================================================
           TÍTULOS DAS CATEGORIAS
           ================================================== */

        h3 {

            margin-bottom: 0px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ======================================================
    # BUSCA
    # ======================================================

    busca = st.text_input(
        "🔎 Pesquisar links",
        placeholder=(
            "Digite o nome do link, sistema, "
            "planilha ou formulário..."
        ),
        key="busca_links"
    )


    # ======================================================
    # SE EXISTE BUSCA
    # ======================================================

    if busca:

        termo = normalizar(busca)

        links_filtrados = []


        # --------------------------------------------------
        # PROCURA EM TODOS OS LINKS
        # --------------------------------------------------

        for link in LINKS:

            nome = normalizar(
                link["nome"]
            )

            descricao = normalizar(
                link["descricao"]
            )

            categoria = normalizar(
                link["categoria"]
            )


            if (
                termo in nome
                or termo in descricao
                or termo in categoria
            ):

                links_filtrados.append(link)


        # --------------------------------------------------
        # NENHUM RESULTADO
        # --------------------------------------------------

        if not links_filtrados:

            st.warning(
                f'Nenhum link encontrado para "{busca}".'
            )

            return


        # --------------------------------------------------
        # RESULTADOS
        # --------------------------------------------------

        st.subheader("🔎 Resultados")

        st.caption(
            f"{len(links_filtrados)} link(s) encontrado(s)."
        )


        # --------------------------------------------------
        # RESULTADOS EM 4 COLUNAS
        # --------------------------------------------------

        colunas = st.columns(4)


        for indice, link in enumerate(
            links_filtrados
        ):

            coluna = colunas[
                indice % 4
            ]

            with coluna:

                mostrar_link(link)


        return


    # ======================================================
    # SEPARADOR
    # ======================================================

    st.divider()


    # ======================================================
    # SEPARAR OS LINKS POR CATEGORIA
    # ======================================================

    planilhas = []

    formularios = []

    sistemas = []

    documentacao = []


    for link in LINKS:

        if link["categoria"] == "Planilhas":

            planilhas.append(link)

        elif link["categoria"] == "Formulários":

            formularios.append(link)

        elif link["categoria"] == "Sistemas":

            sistemas.append(link)

        elif link["categoria"] == "Documentação":

            documentacao.append(link)


    # ======================================================
    # MOSTRAR AS 4 CATEGORIAS LADO A LADO
    # ======================================================

    mostrar_categorias_em_colunas(
        planilhas,
        formularios,
        sistemas,
        documentacao
    )
