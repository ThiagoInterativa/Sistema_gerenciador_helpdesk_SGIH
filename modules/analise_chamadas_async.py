"""
Módulo: Análise de Chamadas — VARIANTE 2 (segundo plano)
==========================================================
A busca do CDR roda numa threading.Thread separada. Enquanto isso,
o usuário pode clicar em "Visão Geral" ou fechar o card e voltar
depois - o job continua rodando e escrevendo progresso em
st.session_state.jobs["analise_chamadas"].

Ponto técnico chave: add_script_run_ctx()
------------------------------------------
Por padrão, uma thread criada "na mão" (threading.Thread) NÃO tem
acesso seguro ao contexto do Streamlit. Anexamos o contexto da
thread principal a ela para que escrever em st.session_state de
dentro da thread funcione de forma confiável. Dentro da thread,
NUNCA chame st.write/st.progress/etc — só leia/escreva variáveis.
"""

import threading
import time
from collections import defaultdict
from datetime import datetime

import requests
import streamlit as st
from bs4 import BeautifulSoup
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

LOGIN_URL = "https://pabx.evence.com.br/login"
CDR_URL = "https://pabx.evence.com.br/cdr/pesquisar"

EMAIL = st.secrets["EMAIL"]
SENHA = st.secrets["SENHA"]

JOB_KEY = "analise_chamadas"


@st.cache_resource
def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session


def login_pabx():
    session = get_session()
    r = session.get(LOGIN_URL, timeout=120)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_input = soup.find("input", {"name": "_token"})
    csrf_token = csrf_input["value"] if csrf_input else ""
    payload = {"login": EMAIL, "senha": SENHA, "_token": csrf_token}
    response = session.post(LOGIN_URL, data=payload, timeout=120)
    if response.url != LOGIN_URL:
        return session
    raise Exception("Erro no login do PABX")


def _atualizar_job(session_state, **kwargs):
    """Atualiza o dicionário do job com segurança dentro da thread."""
    job = session_state.jobs.get(JOB_KEY, {})
    job.update(kwargs)
    session_state.jobs[JOB_KEY] = job


def _worker_buscar_cdr(session_state, data_inicio, data_fim):
    """
    Função que roda DENTRO da thread. Não chama nenhuma função st.*
    de UI — só requests/BeautifulSoup e escrita em session_state.
    """
    try:
        session = login_pabx()

        d_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        d_fim = datetime.strptime(data_fim, "%Y-%m-%d")
        if d_inicio > d_fim:
            d_inicio, d_fim = d_fim, d_inicio

        payload_base = {
            "ramal_origem": "", "numero_origem": "", "ramal_destino": "",
            "numero_destino": "", "did": "", "status_chamada": "",
            "centrocusto_id": "", "tipo_chamada": "IN", "gravacao": "",
            "discador": "0",
            "data_inicial": d_inicio.strftime("%d-%m-%Y"),
            "data_final": d_fim.strftime("%d-%m-%Y"),
        }
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://pabx.evence.com.br/cdr"}

        dados = []
        pagina = 1
        total_estimado = 70

        while True:
            payload = {**payload_base, "page": pagina}

            _atualizar_job(
                session_state,
                status="running",
                progresso=min(pagina / total_estimado, 0.99),
                texto=f"Página {pagina}",
            )

            r = session.get(CDR_URL, params=payload, headers=headers, timeout=120)
            soup = BeautifulSoup(r.text, "html.parser")
            rows = soup.select("table tbody tr")

            if not rows:
                break

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 8:
                    tecnico = cols[4].get_text(strip=True)
                    duracao = cols[5].get_text(strip=True)
                    try:
                        h, m, s = duracao.split(":")
                        segundos = int(h) * 3600 + int(m) * 60 + int(s)
                    except ValueError:
                        segundos = 0
                    dados.append({"tecnico": tecnico, "segundos": segundos})

            pagina += 1
            time.sleep(0.3)

        resultado = _analisar(dados)
        _atualizar_job(
            session_state, status="done", progresso=1.0,
            texto="Concluído", resultado=resultado,
        )

    except Exception as e:
        _atualizar_job(session_state, status="error", texto=str(e))


def _analisar(dados):
    if not dados:
        return None
    dados_validos = [d for d in dados if "Fila" not in d["tecnico"]]
    ranking = defaultdict(lambda: {"chamadas": 0, "segundos": 0})
    for d in dados_validos:
        ranking[d["tecnico"]]["chamadas"] += 1
        ranking[d["tecnico"]]["segundos"] += d["segundos"]

    ranking_lista = [
        {"Técnico": t, "Total Chamadas": v["chamadas"]}
        for t, v in ranking.items()
    ]
    ranking_lista.sort(key=lambda x: x["Total Chamadas"], reverse=True)
    return {"total": len(dados_validos), "ranking": ranking_lista}


def iniciar_job(data_inicio, data_fim):
    """Chamado pela UI (thread principal) para disparar o worker."""
    st.session_state.jobs[JOB_KEY] = {
        "status": "running", "progresso": 0.0, "texto": "Iniciando...", "resultado": None,
    }

    thread = threading.Thread(
        target=_worker_buscar_cdr,
        args=(st.session_state, data_inicio, data_fim),
        daemon=True,
    )
    # Anexa o contexto do script atual à thread - necessário para
    # que escrever em st.session_state de dentro dela seja seguro.
    ctx = get_script_run_ctx()
    add_script_run_ctx(thread, ctx)
    thread.start()


def render():
    """UI do módulo - chamada toda vez que o usuário está nesse card."""
    st.title("📊 Análise de Chamadas")
    st.caption("Esta consulta roda em segundo plano — você pode navegar para outros menus enquanto espera.")

    job = st.session_state.jobs.get(JOB_KEY)

    col_ini, col_fim, col_btn = st.columns([2, 2, 1])
    with col_ini:
        data_inicio = st.date_input("Data inicial", key="async_data_inicio")
    with col_fim:
        data_fim = st.date_input("Data final", key="async_data_fim")
    with col_btn:
        st.write("")
        job_rodando = job and job["status"] == "running"
        if st.button("Buscar", use_container_width=True, disabled=bool(job_rodando)):
            iniciar_job(str(data_inicio), str(data_fim))
            st.rerun()

    if not job:
        st.info("Escolha o período e clique em Buscar.")
        return

    if job["status"] == "running":
        st.progress(job["progresso"], text=job["texto"])
        st.caption("Pode sair dessa tela — o progresso continua e aparece na barra lateral.")

    elif job["status"] == "error":
        st.error(f"Falha na consulta: {job['texto']}")

    elif job["status"] == "done":
        resultado = job["resultado"]
        if not resultado:
            st.warning("Nenhuma chamada encontrada no período.")
            return
        st.metric("Total de chamadas atendidas", resultado["total"])
        st.subheader("Ranking de técnicos")
        st.dataframe(resultado["ranking"], use_container_width=True)
