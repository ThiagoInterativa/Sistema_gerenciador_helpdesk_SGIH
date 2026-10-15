"""
Módulo: Visão Geral do SGIH
--------------------------
Tela inicial de monitoramento do Service Desk.

Funcionalidades:
- Consulta real dos agentes no PABX Evence.
- Autenticação com token CSRF.
- Cache para reduzir requisições ao servidor.
- Atualização periódica da tela.
- Status coloridos dos técnicos.
- Tratamento de falhas de conexão e autenticação.
- Manutenção do layout de três colunas:
  PABX, Kanban e WhatsApp.

Requisitos:
    pip install streamlit requests beautifulsoup4

Credenciais necessárias em .streamlit/secrets.toml:
    EMAIL = "seu_usuario"
    SENHA = "sua_senha"

Observação:
    As áreas Kanban e WhatsApp abaixo mantêm os exemplos
    anteriores até que suas funções reais sejam integradas.
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

# Tempo máximo de espera por resposta do servidor, em segundos.
REQUEST_TIMEOUT = 15

# Cache máximo dos resultados consultados.
CACHE_TTL = 30


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def remover_acentos(texto: str) -> str:
    """
    Remove acentos e normaliza o texto para facilitar
    a comparação de status, mesmo quando o PABX retorna
    palavras com diferenças de acentuação.
    """
    texto = str(texto or "")

    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )


def obter_status_padronizado(texto: str) -> str:
    """
    Converte o texto retornado pelo PABX em um dos
    quatro status utilizados pela interface.

    Retorno:
        livre, ocupado, pausa ou offline.
    """
    texto = remover_acentos(texto)

    # Verifica primeiro estados que indicam indisponibilidade.
    if any(palavra in texto for palavra in (
        "indisponivel",
        "offline",
        "desconectado",
        "deslogado",
    )):
        return "offline"

    # Estados de pausa.
    if "pausa" in texto:
        return "pausa"

    # Estados em que o técnico está atendendo.
    if any(palavra in texto for palavra in (
        "ocupado",
        "falando",
        "em ligacao",
        "em chamada",
        "atendimento",
    )):
        return "ocupado"

    # Estado disponível para atendimento.
    if "livre" in texto or "disponivel" in texto:
        return "livre"

    # Não presumimos que um status desconhecido seja livre.
    return "offline"


# ============================================================
# AUTENTICAÇÃO NO PABX
# ============================================================

def login_pabx():
    """
    Abre uma sessão HTTP, obtém o token CSRF e realiza
    o login no PABX.

    Retorna:
        (session, None) em caso de sucesso.
        (None, mensagem_de_erro) em caso de falha.

    As credenciais são lidas de st.secrets e não ficam
    gravadas no código-fonte.
    """
    try:
        # Recupera as credenciais configuradas no Streamlit.
        email = st.secrets["EMAIL"]
        senha = st.secrets["SENHA"]

        # Uma sessão mantém cookies entre GET e POST.
        session = requests.Session()

        # Identifica a aplicação como um cliente HTTP normal.
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })

        # Abre a página para obter o token CSRF.
        resposta = session.get(
            LOGIN_URL,
            timeout=REQUEST_TIMEOUT,
        )
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")

        # Procura o campo CSRF do formulário de login.
        campo_token = soup.find("input", {"name": "_token"})

        if not campo_token or not campo_token.get("value"):
            return None, (
                "O PABX não retornou o token CSRF. "
                "Verifique se a página de login mudou."
            )

        token = campo_token["value"]

        # Dados enviados para autenticação.
        payload = {
            "login": email,
            "senha": senha,
            "_token": token,
        }

        # Realiza o login mantendo os cookies da sessão.
        resposta_login = session.post(
            LOGIN_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        resposta_login.raise_for_status()

        # Valida a autenticação sem depender somente da URL:
        # alguns sistemas retornam HTTP 200 mesmo após falha.
        url_final = resposta_login.url.rstrip("/")

        pagina_final = BeautifulSoup(
            resposta_login.text,
            "html.parser",
        )

        formulario_login = pagina_final.find(
            "input",
            {"name": "_token"},
        )

        ainda_na_tela_login = (
            url_final == LOGIN_URL.rstrip("/")
            and formulario_login is not None
        )

        # Se o sistema continuar na página de login,
        # não devemos consultar o monitoramento.
        if ainda_na_tela_login:
            return None, (
                "Falha na autenticação do PABX. "
                "Confira EMAIL e SENHA no secrets.toml."
            )

        return session, None

    except KeyError:
        return None, (
            "Credenciais ausentes. Configure EMAIL e SENHA "
            "em .streamlit/secrets.toml."
        )

    except requests.Timeout:
        return None, "Tempo limite excedido durante o login no PABX."

    except requests.RequestException:
        # Evita expor cookies, credenciais ou detalhes
        # internos da requisição na interface.
        return None, "Falha de conexão durante o login no PABX."

    except Exception:
        return None, "Não foi possível concluir o login no PABX."


# ============================================================
# CONSULTA DOS TÉCNICOS
# ============================================================

def get_agentes(session):
    """
    Consulta a página de monitoramento dos agentes.

    A estrutura esperada é uma tabela HTML com:
        coluna 0: nome do técnico
        coluna 2: status do técnico

    Retorna uma lista de tuplas:
        [("Leonardo", "livre"), ("Matheus", "pausa")]

    Levanta uma exceção se a consulta falhar, para que
    a interface não confunda erro de servidor com lista vazia.
    """
    resposta = session.get(
        MONITOR_URL,
        timeout=REQUEST_TIMEOUT,
    )
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    tabela = soup.find("table")

    # Sem tabela pode significar sessão expirada ou mudança
    # no HTML. Não apresentamos isso como ausência de agentes.
    if tabela is None:
        raise ValueError(
            "A página de monitoramento não contém uma tabela."
        )

    agentes = []

    for linha in tabela.find_all("tr"):
        colunas = linha.find_all("td")

        # Ignora linhas de cabeçalho ou linhas incompletas.
        if len(colunas) < 3:
            continue

        # Extrai e limpa o nome.
        nome = colunas[0].get_text(" ", strip=True)

        # Remove o texto auxiliar, caso apareça junto ao nome.
        nome = re.split(
            r"Última chamada",
            nome,
            flags=re.IGNORECASE,
        )[0].strip()

        # Obtém o texto da coluna de status.
        texto_status = colunas[2].get_text(" ", strip=True)

        # Ignora linhas sem identificação.
        if not nome:
            continue

        status = obter_status_padronizado(texto_status)

        agentes.append((nome, status))

    return agentes


# ============================================================
# CONSULTA COMPLETA COM CACHE
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_pabx_cache(ttl_marker):
    """
    Faz login e consulta os agentes.

    ttl_marker é usado como parte da chave do cache.
    O valor muda conforme o intervalo selecionado na tela.

    O TTL de 30 segundos limita o tempo de armazenamento
    de cada resultado, enquanto o marcador permite gerar
    uma nova chave quando o intervalo muda.

    O resultado é um dicionário:
        {
            "ok": True ou False,
            "agentes": lista de agentes,
            "erro": mensagem ou None
        }
    """
    # O argumento é utilizado intencionalmente como chave.
    _ = ttl_marker

    session, erro_login = login_pabx()

    if session is None:
        return {
            "ok": False,
            "agentes": [],
            "erro": erro_login,
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
            "erro": "Tempo limite excedido na consulta dos agentes.",
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
            "erro": "Erro inesperado ao consultar o PABX.",
        }

    finally:
        # Fecha a sessão mesmo quando ocorre uma falha.
        session.close()


# ============================================================
# KANBAN E WHATSAPP
# ============================================================
# Estes dois blocos preservam os dados de exemplo do módulo
# original. Substitua-os pelas funções reais do seu sistema
# quando for integrar as respectivas APIs.
# ============================================================

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_kanban_cache(ttl_marker):
    """Dados provisórios do Kanban."""
    _ = ttl_marker

    return [
        {
            "titulo": "Configurar",
            "coluna": "Em andamento",
        }
    ]


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _status_whatsapp_cache(ttl_marker):
    """Dados provisórios do WhatsApp."""
    _ = ttl_marker

    return {
        "Leonardo": "online",
        "Matheus": "offline",
    }


# ============================================================
# INTERFACE DA VISÃO GERAL
# ============================================================

def render(refresh_rate: int = 30):
    """
    Renderiza a Visão Geral mantendo o layout original.

    refresh_rate:
        Intervalo de atualização em segundos.

    Requer uma versão do Streamlit compatível com
    st.fragment(run_every=...).
    """

    # Garante um intervalo válido.
    refresh_rate = max(5, int(refresh_rate))

    # --------------------------------------------------------
    # Atualização periódica
    # --------------------------------------------------------
    # O fragmento é reexecutado automaticamente pelo Streamlit.
    # O marcador muda a cada intervalo, provocando uma nova
    # consulta ao PABX sem depender de um clique do usuário.
    #
    # O restante do aplicativo não precisa ser redesenhado
    # a cada atualização deste painel.
    # --------------------------------------------------------

    @st.fragment(run_every=refresh_rate)
    def painel_monitoramento():

        st.title("Visão Geral")
        st.caption(
            "Monitoramento do ambiente e ferramentas - Service Desk"
        )

        # Marcador de cache baseado no intervalo escolhido.
        # Exemplo: com refresh_rate=30, o marcador muda
        # a cada 30 segundos.
        ttl_marker = int(time.time() // refresh_rate)

        # Consulta os dados das três áreas.
        resultado_pabx = _status_pabx_cache(ttl_marker)
        tarefas = _status_kanban_cache(ttl_marker)
        whatsapp = _status_whatsapp_cache(ttl_marker)

        # Mantém o layout original de três colunas.
        col1, col2, col3 = st.columns(3)

        # ====================================================
        # COLUNA 1 — PABX
        # ====================================================
        with col1:
            st.subheader("☎️ Status PABX")

            if not resultado_pabx["ok"]:
                # Falhas são exibidas explicitamente, em vez
                # de serem apresentadas como técnicos offline.
                st.error(resultado_pabx["erro"])

            else:
                agentes = resultado_pabx["agentes"]

                if not agentes:
                    st.warning(
                        "Consulta concluída, mas nenhum técnico "
                        "foi encontrado na tabela do PABX."
                    )

                else:
                    # Contadores calculados a partir dos dados reais.
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

                    # Indicadores compactos acima da lista.
                    st.caption(
                        f"🟢 {livres} livres  |  "
                        f"🔴 {ocupados} ocupados  |  "
                        f"🟡 {pausas} em pausa  |  "
                        f"⚪ {offline} offline"
                    )

                    # Lista de agentes e status.
                    for nome, status in agentes:
                        cor = {
                            "livre": "🟢",
                            "ocupado": "🔴",
                            "pausa": "🟡",
                            "offline": "⚪",
                        }.get(status, "⚪")

                        st.write(
                            f"{cor} {nome} — {status}"
                        )

        # ====================================================
        # COLUNA 2 — KANBAN
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

                st.write(f"{cor} {nome} — {status}")

    # Executa o painel.
    painel_monitoramento()
2. Configure as credenciais
Crie ou edite o arquivo .streamlit/secrets.toml na raiz do projeto:

toml

# Credenciais do sistema PABX Evence.
# Preencha com os dados reais de acesso.

EMAIL = "SEU_USUARIO_DO_PABX"
SENHA = "SUA_SENHA_DO_PABX"
Não coloque esse arquivo no Git. Adicione .streamlit/secrets.toml ao .gitignore para evitar publicar as credenciais.

3. Instale as dependências
No terminal do ambiente em que o SGIH roda, execute:

bash
pip install -U "streamlit>=1.37" requests beautifulsoup4
O Streamlit 1.37 ou superior é necessário para usar st.fragment com atualização automática.

4. Integre ao seu app.py
No ponto em que seu aplicativo já chama a tela de Visão Geral, mantenha a chamada ao módulo e passe o intervalo de atualização.

python
import streamlit as st
from visao_geral import render

# Intervalo de atualização em segundos.
# Se você já possui um slider no SGIH, reutilize o valor dele.
refresh_rate = st.sidebar.slider(
    "Atualização do monitoramento (segundos)",
    min_value=5,
    max_value=60,
    value=30,
    step=5,
)

# Renderiza a tela inicial de monitoramento.
render(refresh_rate=refresh_rate)
