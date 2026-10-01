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
#
# Cada link possui uma estrutura fixa:
#
# ┌──────────────────────────┐
# │ 📊 Nome                  │ ← altura fixa
# │ Descrição                │ ← altura fixa
# │                          │
# │ [      Abrir ↗       ]   │ ← botão
# └──────────────────────────┘
#
# Isso mantém todos os elementos alinhados.
# ==========================================================

def mostrar_link(link):

    # ------------------------------------------------------
    # CONTAINER DO LINK
    # ------------------------------------------------------

    st.markdown(
        '<div class="link-card">',
        unsafe_allow_html=True
    )


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


    # ------------------------------------------------------
    # FECHA CONTAINER
    # ------------------------------------------------------

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==========================================================
# MOSTRAR LINKS DE UMA CATEGORIA
# ==========================================================

def mostrar_links_categoria(lista_links):

    for link in lista_links:

        mostrar_link(link)


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
           CONTAINER DE CADA LINK
           ================================================== */

        .link-card {

            width: 100%;

            margin-bottom: 24px;

        }


        /* ==================================================
           TÍTULO DO LINK
           ==================================================
           
           ALTURA FIXA.

           Isso garante que:
           
           "Sistema de Chamados"

           e

           "Base de Conhecimento"

           ocupem exatamente o mesmo espaço.
        */

        .link-titulo {

            height: 48px;

            display: flex;

            align-items: flex-start;

            font-size: 16px;

            font-weight: 600;

            color: #ffffff;

            line-height: 22px;

            overflow: hidden;

            padding-right: 5px;

        }


        /* ==================================================
           DESCRIÇÃO
           ==================================================
           
           Também possui altura fixa.
        */

        .link-descricao {

            height: 52px;

            color: #9ca3af;

            font-size: 12px;

            line-height: 18px;

            overflow: hidden;

            padding-right: 5px;

        }


        /* ==================================================
           BOTÕES
           ================================================== */

        div.stLinkButton {

            width: 100%;

            margin-top: 4px;

        }


        div.stLinkButton > a {

            width: 100%;

        }


        /* ==================================================
           TÍTULOS DAS CATEGORIAS
           ================================================== */

        .categoria-titulo {

            height: 42px;

            display: flex;

            align-items: center;

            font-size: 18px;

            font-weight: 600;

            color: #ffffff;

        }


        /* ==================================================
           LINHA ABAIXO DA CATEGORIA
           ================================================== */

        .categoria-linha {

            height: 1px;

            background-color: #374151;

            margin-top: 4px;

            margin-bottom: 22px;

        }


        /* ==================================================
           SEPARADOR PRINCIPAL
           ================================================== */

        hr {

            border-color: #374151;

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
    # BUSCA ATIVA
    # ======================================================

    if busca:

        termo = normalizar(busca)

        links_filtrados = []


        # --------------------------------------------------
        # PROCURA
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
    # SEPARAR LINKS POR CATEGORIA
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
    # LAYOUT PRINCIPAL
    # ======================================================
    #
    # 4 colunas:
    #
    # PLANILHAS | FORMULÁRIOS | SISTEMAS | DOCUMENTAÇÃO
    #
    # ======================================================

    col1, col2, col3, col4 = st.columns(
        [1, 1, 1, 1],
        gap="medium"
    )


    # ======================================================
    # COLUNA 1
    # ======================================================

    with col1:

        st.markdown(
            """
            <div class="categoria-titulo">
                📊 Planilhas
            </div>

            <div class="categoria-linha"></div>
            """,
            unsafe_allow_html=True
        )


        mostrar_links_categoria(
            planilhas
        )


    # ======================================================
    # COLUNA 2
    # ======================================================

    with col2:

        st.markdown(
            """
            <div class="categoria-titulo">
                📝 Formulários
            </div>

            <div class="categoria-linha"></div>
            """,
            unsafe_allow_html=True
        )


        mostrar_links_categoria(
            formularios
        )


    # ======================================================
    # COLUNA 3
    # ======================================================

    with col3:

        st.markdown(
            """
            <div class="categoria-titulo">
                🌐 Sistemas
            </div>

            <div class="categoria-linha"></div>
            """,
            unsafe_allow_html=True
        )


        mostrar_links_categoria(
            sistemas
        )


    # ======================================================
    # COLUNA 4
    # ======================================================

    with col4:

        st.markdown(
            """
            <div class="categoria-titulo">
                📚 Documentação
            </div>

            <div class="categoria-linha"></div>
            """,
            unsafe_allow_html=True
        )


        mostrar_links_categoria(
            documentacao
        )
