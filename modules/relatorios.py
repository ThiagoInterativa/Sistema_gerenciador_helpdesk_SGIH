
# ==========================================================
# VISÃO GERAL
# ==========================================================

if st.session_state.menu == "visao_geral":

    from modules import visao_geral

    visao_geral.render(
        st.session_state.refresh_rate
    )


# ==========================================================
# CHAMADAS
# ==========================================================

elif st.session_state.menu == "chamadas":

    # ------------------------------------------------------
    # Se nenhum card foi selecionado
    # ------------------------------------------------------

    if st.session_state.card is None:

        st.title("📞 Chamadas")

        st.caption(
            "Selecione um módulo para carregar"
        )


        # --------------------------------------------------
        # CARDS
        # --------------------------------------------------

        c1, c2, c3 = st.columns(3)


        # ==================================================
        # CHAMADA RECUSADA
        # ==================================================

        with c1:

            st.markdown(
                "#### 🚫 Chamada Recusada"
            )

            if st.button(
                "Abrir",
                key="card_recusada",
                use_container_width=True
            ):

                st.session_state.card = "recusada"

                st.rerun()


        # ==================================================
        # ANÁLISE DE CHAMADAS
        # ==================================================

        with c2:

            st.markdown(
                "#### 📊 Análise de Chamadas"
            )

            job = st.session_state.jobs.get(
                "analise_chamadas"
            )

            if (
                job
                and job["status"] == "running"
            ):

                st.caption(
                    f"🔄 Rodando em segundo plano "
                    f"({int(job['progresso'] * 100)}%)"
                )

            elif (
                job
                and job["status"] == "done"
            ):

                st.caption(
                    "✅ Resultado pronto"
                )


            if st.button(
                "Abrir",
                key="card_analise",
                use_container_width=True
            ):

                st.session_state.card = "analise"

                st.rerun()


        # ==================================================
        # LIGAÇÃO POR RAMAL
        # ==================================================

        with c3:

            st.markdown(
                "#### ☎️ Ligação por Ramal"
            )

            if st.button(
                "Abrir",
                key="card_ramal",
                use_container_width=True
            ):

                st.session_state.card = "ramal"

                st.rerun()


    # ------------------------------------------------------
    # CARD FOI SELECIONADO
    # ------------------------------------------------------

    else:

        if st.button(
            "← Voltar para os cards"
        ):

            st.session_state.card = None

            st.rerun()

