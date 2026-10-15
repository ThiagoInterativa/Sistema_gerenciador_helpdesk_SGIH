"""
Módulo: Visão Geral do SGIH
===========================
Monitoramento do PABX, Kanban e WhatsApp.

O PABX utiliza autenticação HTTP com CSRF e consulta
a tabela real de agentes.

As áreas Kanban e WhatsApp mantêm os dados de exemplo
do módulo original até a integração de suas funções reais.
"""

import re
import time
import unicodedata

import requests
import streamlit as st
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURAÇÕES DO PABX
# ============================================================

LOGIN_URL = "https://pabx.evence.com.br/login"

MONITOR_URL = (
    "https://pabx.evence.com.br/"
    "callcenter/monitoramentoAgentes/detalhes"
    "?agentes=46,47,49,50,52,53"
)

REQUEST_TIMEOUT = 15
CACHE_TTL = 30


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def remover_acentos(texto):
    """Remove acentos e converte o texto para minúsculas."""
    texto = str(texto or "")

    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )


def normalizar_status(texto):
    """
    Converte o status recebido do PABX para:
    livre, ocupado, pausa ou offline.
    """
    texto = remover_acentos(texto)

    if any(p in texto for p in (
        "indisponivel",
        "offline",
        "desconectado",
        "deslogado",
    )):
        return "offline"

    if "pausa" in texto:
        return "pausa"

    if any(p in texto for p in (
        "ocupado",
        "falando",
        "em ligacao",
        "em chamada",
        "atendimento",
    )):
        return "ocupado"

    if "livre" in texto or "disponivel" in texto:
        return "livre"

    # Não presumir que um status desconhecido seja livre.
    return "offline"


# ============================================================
# LOGIN NO PABX
# ============================================================

def login():
    """
    Autentica no PABX usando EMAIL e SENHA do st.secrets.

    Retorna:
        (sessao, None) se o login aparentar sucesso.
        (None, mensagem) em caso de erro.
    """
    session = requests.Session()

    try:
        # Credenciais configuradas no Streamlit.
        email = st.secrets["EMAIL"]
        senha = st.secrets["SENHA"]

        # Identifica o cliente HTTP.
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })

        # Abre a página de login para obter o CSRF.
        resposta = session.get(
            LOGIN_URL,
            timeout=REQUEST_TIMEOUT,
        )
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        campo_token = soup.find(
            "input",
            {"name": "_token"},
        )

        if campo_token is None or not campo_token.get("value"):
            session.close()
            return None, (
                "O PABX não retornou o token CSRF. "
                "Verifique a página de login."
            )

        token = campo_token["value"]

        # Dados enviados ao formulário de autenticação.
        payload = {
            "login": email,
            "senha": senha,
            "_token": token,
        }

        resposta_login = session.post(
            LOGIN_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        resposta_login.raise_for_status()

        # Verificação básica para detectar se continuamos
        # na página de login depois do envio do formulário.
        url_final = resposta_login.url.rstrip("/")

        pagina_final = BeautifulSoup(
            resposta_login.text,
            "html.parser",
        )

        campo_login = pagina_final.find(
            "input",
            {"name": "_token"},
        )

        ainda_no_login = (
            url_final == LOGIN_URL.rstrip("/")
            and campo_login is not None
        )

        if ainda_no_login:
            session.close()
            return None, (
                "Falha de autenticação no PABX. "
                "Confira as credenciais."
            )

        return session, None

    except KeyError:
        session.close()
        return None, (
            "Configure EMAIL e SENHA em "
            ".streamlit/secrets.toml."
        )

    except requests.Timeout:
        session.close()
        return None, "Tempo limite excedido no login do PABX."

    except requests.RequestException:
        session.close()
        return None, "Falha de conexão durante o login no PABX."

    except Exception:
        session.close()
        return None, "Erro inesperado durante o login no PABX."


# ============================================================
# CONSULTA DOS AGENTES
# ============================================================

def get_agentes(session):
    """
    Consulta a página de monitoramento dos técnicos.

    A lógica fornecida utiliza:
        Coluna 0: nome do técnico.
        Coluna 2: status do técnico.

    Retorna uma lista de tuplas:
        [("Leonardo", "livre"), ("Matheus", "pausa")]
    """
    resposta = session.get(
        MONITOR_URL,
        timeout=REQUEST_TIMEOUT,
    )
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")
    tabela = soup.find("table")

    if tabela is None:
        raise ValueError(
            "Tabela de agentes não encontrada. "
            "Verifique a sessão ou o HTML do PABX."
        )

    agentes = []

    for linha in tabela.find_all("tr"):
        colunas = linha.find_all("td")

        # Ignora cabeçalhos e linhas incompletas.
        if len(colunas) < 3:
            continue

        # Extrai o nome.
        nome = colunas[0].get_text(" ", strip=True)

        # Remove o texto auxiliar que pode aparecer no nome.
        nome = re.split(
            r"Última chamada",
            nome,
            flags=re.IGNORECASE,
        )[0].strip()

        # Extrai o texto da terceira coluna.
        texto_status = colunas[2].get_text(
            " ",
            strip=True,
        )

        if not nome:
            continue

        status = normalizar_status(texto_status)
        agentes.append((nome, status))

    return agentes


# ============================================================
# CONSULTA PABX COM CACHE
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_pabx_cache(ttl_marker):
    """
    Armazena temporariamente os dados do PABX.

    ttl_marker integra a chave do cache, permitindo renovar
    a consulta quando o intervalo de atualização muda.
    """
    _ = ttl_marker

    session, erro = login()

    if session is None:
        return {
            "ok": False,
            "agentes": [],
            "erro": erro,
        }

    try:
        agentes = get_agentes(session)

        return {
            "ok": True,
            "agentes": agentes,
            "erro": None,
        }

    except requests.Timeout:
        return {
            "ok": False,
            "agentes": [],
            "erro": "Tempo limite excedido na consulta do PABX.",
        }

    except requests.RequestException:
        return {
            "ok": False,
            "agentes": [],
            "erro": "Falha de conexão ao consultar os técnicos.",
        }

    except ValueError as erro:
        return {
            "ok": False,
            "agentes": [],
            "erro": str(erro),
        }

    except Exception:
        return {
            "ok": False,
            "agentes": [],
            "erro": "Erro inesperado ao consultar os técnicos.",
        }

    finally:
        session.close()


# ============================================================
# KANBAN — DADOS PROVISÓRIOS
# Substitua pelo método real de consulta do seu sistema.
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_kanban_cache(ttl_marker):
    """Mantém o formato de dados do módulo original."""
    _ = ttl_marker

    return [
        {
            "titulo": "Configurar",
            "coluna": "Em andamento",
        }
    ]


# ============================================================
# WHATSAPP — DADOS PROVISÓRIOS
# Substitua pelo método real de consulta do seu sistema.
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_whatsapp_cache(ttl_marker):
    """Mantém o formato de dados do módulo original."""
    _ = ttl_marker

    return {
        "Leonardo": "online",
        "Matheus": "offline",
    }


# ============================================================
# INTERFACE DA VISÃO GERAL
# ============================================================

def render(refresh_rate=30):
    """
    Renderiza o painel de monitoramento.

    O PABX recebe mais espaço que as outras colunas.
    O resumo de status usa texto sem quebra de linha.

    refresh_rate:
        Intervalo de atualização automática em segundos.
    """
    refresh_rate = max(5, min(300, int(refresh_rate)))

    @st.fragment(run_every=refresh_rate)
    def painel_monitoramento():

        # Cabeçalho original do SGIH.
        st.title("Visão Geral")
        st.caption(
            "Monitoramento do ambiente e ferramentas - Service Desk"
        )

        # Muda a chave de consulta a cada intervalo.
        ttl_marker = int(time.time() // refresh_rate)

        resultado_pabx = _status_pabx_cache(ttl_marker)
        tarefas = _status_kanban_cache(ttl_marker)
        whatsapp = _status_whatsapp_cache(ttl_marker)

        # Layout de três colunas.
        # O PABX recebe uma proporção maior.
        col1, col2, col3 = st.columns(
            [1.8, 1, 1],
            gap="medium",
        )

        # ----------------------------------------------------
        # COLUNA 1 — PABX
        # ----------------------------------------------------
        with col1:
            st.subheader("☎️ Status PABX")

            if not resultado_pabx["ok"]:
                # Exibe o erro sem inventar status dos técnicos.
                st.error(resultado_pabx["erro"])

            else:
                agentes = resultado_pabx["agentes"]

                if not agentes:
                    st.warning(
                        "Nenhum técnico encontrado na tabela "
                        "retornada pelo PABX."
                    )

                else:
                    # Calcula os totais por status.
                    livres = sum(
                        status == "livre"
                        for _, status in agentes
                    )

                    ocupados = sum(
                        status == "ocupado"
                        for _, status in agentes
                    )

                    pausas = sum(
                        status == "pausa"
                        for _, status in agentes
                    )

                    offline = sum(
                        status == "offline"
                        for _, status in agentes
                    )

                    # Indicadores em uma linha.
                    # white-space: nowrap evita que o texto
                    # seja dividido em várias linhas.
                    # A fonte compacta ajuda a caber na coluna.
                    st.markdown(
                        f"""
                        <div style="
                            white-space: nowrap;
                            width: max-content;
                            max-width: none;
                            font-size: 12px;
                            padding: 6px 0;
                            line-height: 1.5;
                        ">
                            🟢 {livres} livres
                            &nbsp;|&nbsp;
                            🔴 {ocupados} ocupados
                            &nbsp;|&nbsp;
                            🟡 {pausas} em pausa
                            &nbsp;|&nbsp;
                            ⚪ {offline} offline
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Lista individual dos técnicos.
                    for nome, status in agentes:
                        cor = {
                            "livre": "🟢",
                            "ocupado": "🔴",
                            "pausa": "🟡",
                            "offline": "⚪",
                        }.get(status, "⚪")

                        st.write(f"{cor} {nome} — {status}")

        # ----------------------------------------------------
        # COLUNA 2 — KANBAN
        # ----------------------------------------------------
        with col2:
            st.subheader("🗂️ Tarefas Kanban")

            for tarefa in tarefas:
                st.write(
                    f"• {tarefa['titulo']} "
                    f"({tarefa['coluna']})"
                )

        # ----------------------------------------------------
        # COLUNA 3 — WHATSAPP
        # ----------------------------------------------------
        with col3:
            st.subheader("💬 WhatsApp")

            for nome, status in whatsapp.items():
                cor = "🟢" if status == "online" else "⚪"
                st.write(f"{cor} {nome} — {status}")

    # Executa o painel com atualização automática.
    painel_monitoramento()
