"""
Módulo: Visão Geral do SGIH
===========================
Tela inicial de monitoramento do Service Desk.

Funcionalidades:
- Consulta real dos técnicos no PABX Evence.
- Autenticação com token CSRF.
- Cache dos resultados para reduzir requisições.
- Atualização automática do monitoramento.
- Indicadores coloridos para os status dos técnicos.
- Layout original com três colunas:
    1. PABX
    2. Kanban
    3. WhatsApp

Credenciais esperadas em .streamlit/secrets.toml:
    EMAIL = "usuario_pabx"
    SENHA = "senha_pabx"

Dependências:
    streamlit
    requests
    beautifulsoup4
"""

import re
import time
import unicodedata

import requests
import streamlit as st
from bs4 import BeautifulSoup


# ============================================================
# 1. CONFIGURAÇÕES DO PABX
# ============================================================

LOGIN_URL = "https://pabx.evence.com.br/login"

MONITOR_URL = (
    "https://pabx.evence.com.br/"
    "callcenter/monitoramentoAgentes/detalhes"
    "?agentes=46,47,49,50,52,53"
)

# Tempo máximo de espera das requisições HTTP, em segundos.
REQUEST_TIMEOUT = 15

# Tempo máximo de armazenamento dos resultados no cache.
CACHE_TTL = 30


# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def remover_acentos(texto):
    """
    Remove os acentos e converte o texto para minúsculas.

    Exemplos:
        'Disponível' -> 'disponivel'
        'Ocupado'    -> 'ocupado'
        'Pausa'      -> 'pausa'
    """
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
    Converte o texto recebido do PABX para um status conhecido.

    Status possíveis:
        livre
        ocupado
        pausa
        offline

    Caso o texto seja desconhecido, retorna offline para
    não indicar disponibilidade sem confirmação.
    """
    texto = remover_acentos(texto)

    # Verifica primeiro os estados de indisponibilidade.
    if any(palavra in texto for palavra in (
        "indisponivel",
        "offline",
        "desconectado",
        "deslogado",
    )):
        return "offline"

    # Técnico em pausa.
    if "pausa" in texto:
        return "pausa"

    # Técnico em ligação ou atendimento.
    if any(palavra in texto for palavra in (
        "ocupado",
        "falando",
        "em ligacao",
        "em chamada",
        "atendimento",
    )):
        return "ocupado"

    # Técnico disponível.
    if "livre" in texto or "disponivel" in texto:
        return "livre"

    return "offline"


# ============================================================
# 3. AUTENTICAÇÃO NO PABX
# ============================================================

def login():
    """
    Realiza a autenticação no PABX.

    Etapas:
    1. Lê EMAIL e SENHA do st.secrets.
    2. Abre uma sessão HTTP.
    3. Acessa a página de login.
    4. Obtém o token CSRF.
    5. Envia as credenciais.
    6. Verifica se a autenticação aparenta ter sido concluída.

    Retorna:
        (session, None) se a autenticação funcionar.
        (None, mensagem) se ocorrer uma falha.

    A sessão mantém os cookies necessários para consultar
    posteriormente a página de monitoramento.
    """
    session = requests.Session()

    try:
        # Obtém as credenciais armazenadas no Streamlit.
        email = st.secrets["EMAIL"]
        senha = st.secrets["SENHA"]

        # Define um User-Agent para a sessão HTTP.
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })

        # Acessa o formulário de login para obter o CSRF.
        resposta = session.get(
            LOGIN_URL,
            timeout=REQUEST_TIMEOUT,
        )
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        # Procura o campo oculto _token.
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

        # Monta os dados enviados ao formulário.
        payload = {
            "login": email,
            "senha": senha,
            "_token": token,
        }

        # Envia o formulário de autenticação.
        resposta_login = session.post(
            LOGIN_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        resposta_login.raise_for_status()

        # Verifica a página final para detectar se o formulário
        # de login continua visível após o envio.
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
                "Não foi possível autenticar no PABX. "
                "Confira as credenciais e o formulário de login."
            )

        return session, None

    except KeyError:
        session.close()

        return None, (
            "Credenciais não configuradas. "
            "Adicione EMAIL e SENHA em .streamlit/secrets.toml."
        )

    except requests.Timeout:
        session.close()

        return None, "Tempo limite excedido ao conectar ao PABX."

    except requests.RequestException:
        session.close()

        return None, "Falha de comunicação durante o login no PABX."

    except Exception:
        session.close()

        return None, "Erro inesperado durante a autenticação no PABX."


# ============================================================
# 4. CONSULTA DOS AGENTES
# ============================================================

def get_agentes(session):
    """
    Consulta os agentes no endereço de monitoramento.

    A lógica segue a estrutura informada:
        - primeira coluna: nome do técnico
        - terceira coluna: status do técnico

    Retorna:
        Lista de tuplas:
        [
            ("Leonardo", "livre"),
            ("Matheus", "pausa"),
        ]

    Se o servidor falhar ou a tabela não for encontrada,
    gera uma exceção para que a interface informe o problema.
    """
    resposta = session.get(
        MONITOR_URL,
        timeout=REQUEST_TIMEOUT,
    )
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    # Localiza a tabela de monitoramento.
    tabela = soup.find("table")

    if tabela is None:
        raise ValueError(
            "A tabela de agentes não foi encontrada. "
            "Verifique a sessão ou a estrutura HTML do PABX."
        )

    agentes = []

    # Percorre todas as linhas da tabela.
    for linha in tabela.find_all("tr"):
        colunas = linha.find_all("td")

        # Ignora cabeçalhos e linhas incompletas.
        if len(colunas) < 3:
            continue

        # Obtém o nome do técnico.
        nome = colunas[0].get_text(" ", strip=True)

        # Remove o texto auxiliar que pode vir junto ao nome.
        nome = re.split(
            r"Última chamada",
            nome,
            flags=re.IGNORECASE,
        )[0].strip()

        # Obtém o texto do status na terceira coluna.
        texto_status = colunas[2].get_text(" ", strip=True)

        if not nome:
            continue

        # Normaliza o status para os valores da interface.
        status = normalizar_status(texto_status)

        agentes.append((nome, status))

    return agentes


# ============================================================
# 5. CONSULTA REAL COM CACHE
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_pabx_cache(ttl_marker):
    """
    Faz login e consulta os agentes do PABX.

    ttl_marker faz parte da chave do cache e permite uma
    nova consulta quando o intervalo de atualização muda.

    O cache armazena somente o resultado, não a sessão HTTP.

    Retorno:
        {
            "ok": True/False,
            "agentes": [...],
            "erro": None ou mensagem
        }
    """
    # O marcador é utilizado intencionalmente como chave.
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
            "erro": "Falha de conexão ao consultar os agentes.",
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
            "erro": "Erro inesperado ao consultar os agentes.",
        }

    finally:
        # Encerra a sessão HTTP após a consulta.
        session.close()


# ============================================================
# 6. KANBAN — DADOS PROVISÓRIOS
# ============================================================
# Mantemos o mesmo formato do módulo original.
# Substitua esta função pela integração real do Kanban
# quando quiser conectar a API ou o scraping correspondente.
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_kanban_cache(ttl_marker):
    """Retorna os dados provisórios do Kanban."""
    _ = ttl_marker

    return [
        {
            "titulo": "Configurar",
            "coluna": "Em andamento",
        }
    ]


# ============================================================
# 7. WHATSAPP — DADOS PROVISÓRIOS
# ============================================================
# Mantemos o mesmo formato do módulo original.
# A integração real do WhatsApp deve ser adicionada aqui.
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_whatsapp_cache(ttl_marker):
    """Retorna os dados provisórios do WhatsApp."""
    _ = ttl_marker

    return {
        "Leonardo": "online",
        "Matheus": "offline",
    }


# ============================================================
# 8. INTERFACE DA VISÃO GERAL
# ============================================================

def render(refresh_rate=30):
    """
    Desenha a tela Visão Geral.

    Mantém as três colunas do layout original:
        PABX | Kanban | WhatsApp

    refresh_rate:
        Intervalo de atualização automática em segundos.

    st.fragment permite atualizar apenas o painel, sem
    precisar redesenhar o aplicativo inteiro.
    """

    # Garante que o intervalo esteja dentro de um limite seguro.
    refresh_rate = max(5, min(300, int(refresh_rate)))

    @st.fragment(run_every=refresh_rate)
    def painel_monitoramento():

        # ----------------------------------------------------
        # Cabeçalho original
        # ----------------------------------------------------
        st.title("Visão Geral")

        st.caption(
            "Monitoramento do ambiente e ferramentas - Service Desk"
        )

        # Cria um marcador que muda a cada intervalo.
        # Isso permite uma nova chave para o cache a cada ciclo.
        ttl_marker = int(time.time() // refresh_rate)

        # Consulta os dados das três áreas.
        resultado_pabx = _status_pabx_cache(ttl_marker)

        tarefas = _status_kanban_cache(ttl_marker)

        whatsapp = _status_whatsapp_cache(ttl_marker)

        # Mantém as três colunas originais.
        col1, col2, col3 = st.columns(3)

        # ====================================================
        # COLUNA 1 — STATUS PABX
        # ====================================================
        with col1:

            st.subheader("☎️ Status PABX")

            if not resultado_pabx["ok"]:

                # Erro explícito, sem apresentar dados falsos.
                st.error(resultado_pabx["erro"])

            else:

                agentes = resultado_pabx["agentes"]

                if not agentes:

                    st.warning(
                        "Nenhum técnico encontrado na tabela "
                        "retornada pelo PABX."
                    )

                else:

                    # Calcula os totais dos técnicos por status.
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

                    # O HTML controla a exibição em uma única linha.
st.markdown(
    f"""
    <div style="
        width: max-content;
        max-width: none;
        white-space: nowrap;
        font-size: 13px;
        padding: 6px 0;
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

        # ====================================================
        # COLUNA 2 — TAREFAS KANBAN
        # ====================================================
        with col2:

            st.subheader("🗂️ Tarefas Kanban")

            for tarefa in tarefas:

                st.write(
                    f"• {tarefa['titulo']} "
                    f"({tarefa['coluna']})"
                )

        # ====================================================
        # COLUNA 3 — WHATSAPP
        # ====================================================
        with col3:

            st.subheader("💬 WhatsApp")

            for nome, status in whatsapp.items():

                cor = (
                    "🟢"
                    if status == "online"
                    else "⚪"
                )

                st.write(
                    f"{cor} {nome} — {status}"
                )

    # Executa o fragmento de monitoramento.
    painel_monitoramento()
