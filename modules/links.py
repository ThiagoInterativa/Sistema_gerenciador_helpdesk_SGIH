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
        "nome": "Escala",
        "descricao": "Planilha de escala da equipe.",
        "icone": "📅",
        "url": "COLOQUE_AQUI_A_URL",
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

    {
        "categoria": "Formulários",
        "nome": "Pesquisa",
        "descricao": "Pesquisa de satisfação.",
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

    # Título
    st.markdown(
        f"""
        <div class="link-titulo">
            {link["icone"]} {link["nome"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Descrição
    st.markdown(
        f"""
        <div class="link-descricao">
            {link["descricao"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Botão
    st.link_button(
        link["tipo_botao"],
        link["url"],
        use_container_width=True
    )


# ==========================================================
# MOSTRAR VÁRIOS LINKS EM 3 COLUNAS
# ==========================================================

def mostrar_links_em_colunas(lista_links):

    colunas = st.columns(3)

    for indice, link in enumerate(lista_links):

        coluna = colunas[indice % 3]

        with coluna:

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

        .link-titulo {

            height: 55px;

            display: flex;

            align-items: flex-start;

            font-size: 18px;

            font-weight: 600;

            color: #ffffff;

            line-height: 24px;

        }


        .link-descricao {

            height: 55px;

            color: #9ca3af;

            font-size: 13px;

            line-height: 19px;

        }


        div.stLinkButton {

            margin-top: 5px;

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

        for link in LINKS:

            nome = normalizar(link["nome"])
            descricao = normalizar(link["descricao"])
            categoria = normalizar(link["categoria"])

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

        mostrar_links_em_colunas(
            links_filtrados
        )

        return



    # ======================================================
    # SEPARADOR
    # ======================================================

    st.divider()


    # ======================================================
    # PLANILHAS
    # ======================================================

    planilhas = []

    for link in LINKS:

        if link["categoria"] == "Planilhas":

            planilhas.append(link)


    if planilhas:

        st.subheader("📊 Planilhas")

        mostrar_links_em_colunas(
            planilhas
        )


    # ======================================================
    # SEPARADOR
    # ======================================================

    st.divider()


    # ======================================================
    # FORMULÁRIOS
    # ======================================================

    formularios = []

    for link in LINKS:

        if link["categoria"] == "Formulários":

            formularios.append(link)


    if formularios:

        st.subheader("📝 Formulários")

        mostrar_links_em_colunas(
            formularios
        )


    # ======================================================
    # SEPARADOR
    # ======================================================

    st.divider()


    # ======================================================
    # SISTEMAS
    # ======================================================

    sistemas = []

    for link in LINKS:

        if link["categoria"] == "Sistemas":

            sistemas.append(link)


    if sistemas:

        st.subheader("🌐 Sistemas")

        mostrar_links_em_colunas(
            sistemas
        )


    # ======================================================
    # SEPARADOR
    # ======================================================

    st.divider()


    # ======================================================
    # DOCUMENTAÇÃO
    # ======================================================

    documentacao = []

    for link in LINKS:

        if link["categoria"] == "Documentação":

            documentacao.append(link)


    if documentacao:

        st.subheader("📚 Documentação")

        mostrar_links_em_colunas(
            documentacao
        )
