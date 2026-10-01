import streamlit as st


# ==========================================================
# CONFIGURAÇÃO DOS LINKS
# ==========================================================
#
# Aqui você cadastra os links do seu sistema.
#
# Para adicionar um novo link, basta copiar um dos blocos
# e alterar:
#
# - nome
# - descricao
# - icone
# - urlf
# - favorito
#
# categoria:
#   "Planilhas"
#   "Formulários"
#   "Sistemas"
#   "Documentação"
#
# favorito:
#   True  = aparece em "⭐ Favoritos"
#   False = não aparece nos favoritos
#
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
# FUNÇÃO PARA NORMALIZAR TEXTO
# ==========================================================
#
# Usada pela busca.
#
# Exemplo:
#
# "Controle de Atendimentos"
#
# pode ser encontrado digitando:
#
# "controle"
# "atendimento"
# "ATENDIMENTO"
#
# ==========================================================

def normalizar(texto):

    return texto.lower().strip()


# ==========================================================
# FUNÇÃO PARA MOSTRAR UM LINK
# ==========================================================
#
# Essa função cria:
#
# 📊 Nome
#
# Descrição
#
# [ Abrir ↗ ]
#
# Mantendo o tamanho dos textos alinhado.
# ==========================================================

def mostrar_link(link, indice):

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
           TÍTULO DOS LINKS
           ================================================== */

        .link-titulo {

            height: 55px;

            display: flex;

            align-items: flex-start;

            font-size: 18px;

            font-weight: 600;

            color: #ffffff;

            line-height: 24px;

        }


        /* ==================================================
           DESCRIÇÃO DOS LINKS
           ================================================== */

        .link-descricao {

            height: 55px;

            color: #9ca3af;

            font-size: 13px;

            line-height: 19px;

        }


        /* ==================================================
           ESPAÇAMENTO ENTRE OS BOTÕES
           ================================================== */

        div.stLinkButton {

            margin-top: 5px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )



    # ======================================================
    # CAMPO DE BUSCA
    # ======================================================
    #
    # O usuário pode pesquisar:
    #
    # Controle
    # Kanban
    # Escala
    # Chamados
    # etc.
    #
    # ======================================================

    busca = st.text_input(
        "🔎 Pesquisar links",
        placeholder="Digite o nome do link, sistema, planilha ou formulário...",
        key="busca_links"
    )


    # ======================================================
    # FILTRAR LINKS
    # ======================================================

    if busca:

        termo = normalizar(busca)

        links_filtrados = [

            link

            for link in LINKS

            if (
                termo in normalizar(link["nome"])
                or termo in normalizar(link["descricao"])
                or termo in normalizar(link["categoria"])
            )

        ]

    else:

        links_filtrados = LINKS


    # ======================================================
    # FAVORITOS
    # ======================================================
    #
    # Só mostramos favoritos quando o usuário não está
    # pesquisando.
    #
    # Isso mantém a tela organizada.
    #
    # ======================================================

    favoritos = [

        link

        for link in LINKS

        if link["favorito"]

    ]


    if not busca and favoritos:


        # --------------------------------------------------
        # QUANTIDADE DE COLUNAS
        # --------------------------------------------------

        colunas_favoritos = st.columns(3)


        # --------------------------------------------------
        # MOSTRA FAVORITOS
        # --------------------------------------------------

        for indice, link in enumerate(favoritos):

            coluna = colunas_favoritos[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"favorito_{indice}"
                )


        st.divider()


    # ======================================================
    # CASO A BUSCA NÃO ENCONTRE NADA
    # ======================================================

    if busca and not links_filtrados:

        st.warning(
            f'Nenhum link encontrado para "{busca}".'
        )

        return


    # ======================================================
    # MOSTRAR RESULTADO DA BUSCA
    # ======================================================

    if busca:

        st.subheader("🔎 Resultados")

        st.caption(
            f"{len(links_filtrados)} link(s) encontrado(s)."
        )


        # --------------------------------------------------
        # RESULTADOS EM 3 COLUNAS
        # --------------------------------------------------

        colunas = st.columns(3)


        for indice, link in enumerate(
            links_filtrados
        ):

            coluna = colunas[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"busca_{indice}"
                )


        return


    # ======================================================
    # PLANILHAS
    # ======================================================

    planilhas = [

        link

        for link in LINKS

        if link["categoria"] == "Planilhas"

    ]


    if planilhas:

        st.subheader("📊 Planilhas")


        colunas = st.columns(3)


        for indice, link in enumerate(
            planilhas
        ):

            coluna = colunas[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"planilha_{indice}"
                )


    # ======================================================
    # FORMULÁRIOS
    # ======================================================

    formularios = [

        link

        for link in LINKS

        if link["categoria"] == "Formulários"

    ]


    if formularios:

        st.divider()

        st.subheader("📝 Formulários")


        colunas = st.columns(3)


        for indice, link in enumerate(
            formularios
        ):

            coluna = colunas[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"formulario_{indice}"
                )


    # ======================================================
    # SISTEMAS
    # ======================================================

    sistemas = [

        link

        for link in LINKS

        if link["categoria"] == "Sistemas"

    ]


    if sistemas:

        st.divider()

        st.subheader("🌐 Sistemas")


        colunas = st.columns(3)


        for indice, link in enumerate(
            sistemas
        ):

            coluna = colunas[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"sistema_{indice}"
                )


    # ======================================================
    # DOCUMENTAÇÃO
    # ======================================================

    documentacao = [

        link

        for link in LINKS

        if link["categoria"] == "Documentação"

    ]


    if documentacao:

        st.divider()

        st.subheader("📚 Documentação")


        colunas = st.columns(3)


        for indice, link in enumerate(
            documentacao
        ):

            coluna = colunas[
                indice % 3
            ]

            with coluna:

                mostrar_link(
                    link,
                    f"documentacao_{indice}"
                )
