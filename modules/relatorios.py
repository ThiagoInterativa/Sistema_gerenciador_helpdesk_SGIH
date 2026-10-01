import streamlit as st


def render():

    

    # ==========================================================
    # CRIA 3 COLUNAS
    # ==========================================================

    col1, col2, col3 = st.columns(3)


    # ==========================================================
    # RELATÓRIO 1
    # ==========================================================

    with col1:

        st.markdown("### 📊 Rel 1")

        if st.button(
            "Abrir",
            key="btn_rel1",
            use_container_width=True
        ):

            st.session_state["relatorio_selecionado"] = "rel1"

            st.rerun()


    # ==========================================================
    # RELATÓRIO 2
    # ==========================================================

    with col2:

        st.markdown("### 📊 Rel 2")

        if st.button(
            "Abrir",
            key="btn_rel2",
            use_container_width=True
        ):

            st.session_state["relatorio_selecionado"] = "rel2"

            st.rerun()


    # ==========================================================
    # RELATÓRIO 3
    # ==========================================================

    with col3:

        st.markdown("### 📊 Rel 3")

        if st.button(
            "Abrir",
            key="btn_rel3",
            use_container_width=True
        ):

            st.session_state["relatorio_selecionado"] = "rel3"

            st.rerun()


    # ==========================================================
    # CONTEÚDO DO RELATÓRIO SELECIONADO
    # ==========================================================

    relatorio = st.session_state.get(
        "relatorio_selecionado"
    )


    # ----------------------------------------------------------
    # RELATÓRIO 1
    # ----------------------------------------------------------

    if relatorio == "rel1":

        st.divider()

        st.subheader("📊 Relatório 1")

        st.write(
            "Aqui entrará o conteúdo do Relatório 1."
        )


    # ----------------------------------------------------------
    # RELATÓRIO 2
    # ----------------------------------------------------------

    elif relatorio == "rel2":

        st.divider()

        st.subheader("📊 Relatório 2")

        st.write(
            "Aqui entrará o conteúdo do Relatório 2."
        )


    # ----------------------------------------------------------
    # RELATÓRIO 3
    # ----------------------------------------------------------

    elif relatorio == "rel3":

        st.divider()

        st.subheader("📊 Relatório 3")

        st.write(
            "Aqui entrará o conteúdo do Relatório 3."
        )
