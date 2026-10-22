
import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# ==========================================
# 1. CONFIGURAÇÃO DO PROJETO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# Carregar chave IBM do arquivo .env
load_dotenv(BASE_DIR / ".env")

# No Streamlit Cloud, usar Secrets.
# Localmente, se não existir secrets.toml,
# continuar utilizando o arquivo .env.
try:
    if "IBM_API_KEY" in st.secrets:
        os.environ["IBM_API_KEY"] = st.secrets["IBM_API_KEY"]
except FileNotFoundError:
    pass


# ==========================================
# 2. CONFIGURAÇÃO DO STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Granite AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==========================================
# 3. VERIFICAR CONFIGURAÇÃO IBM
# ==========================================

if not os.getenv("IBM_API_KEY"):
    st.error(
        "A chave IBM_API_KEY não foi encontrada. "
        "Configure o arquivo .env ou os Secrets "
        "do Streamlit Cloud."
    )
    st.stop()


# ==========================================
# 4. IMPORTAR NOSSO AGENTE
# ==========================================

AGENT_DIR = BASE_DIR / "examples" / "basic"

sys.path.insert(0, str(AGENT_DIR))

try:
    from tools import run_agent
except Exception as error:
    st.error("Erro ao carregar o agente IBM Granite.")
    st.exception(error)
    st.stop()


# ==========================================
# 5. ESTILO DA INTERFACE
# ==========================================

st.markdown(
    """
    <style>
        .block-container {
            max-width: 850px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        h1 {
            text-align: center;
        }

        .subtitle {
            text-align: center;
            color: #888888;
            margin-bottom: 25px;
        }

        [data-testid="stChatMessage"] {
            border-radius: 12px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 6. TÍTULO
# ==========================================

st.title("🤖 Chris AI Assistant")

st.markdown(
    '<p class="subtitle">'
    'Agentic AI • IBM Granite • Weather API • Web Search'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 7. MEMÓRIA DE CONVERSA
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_history" not in st.session_state:
    st.session_state.agent_history = []


# ==========================================
# 8. MENU LATERAL
# ==========================================

with st.sidebar:

    st.title("🤖 Chris AI Assistant")

    st.write(
        "Assistente inteligente desenvolvido por Chrinovic com IBM Granite e Python, capaz de tomar decisões e utilizar ferramentas de forma autônoma."
    )

    st.divider()

    st.subheader("Ferramentas")

    st.write(" Weather API : Open-Meteo")
    st.write(" Web Search : DuckDuckGo")

    st.divider()

    st.subheader(" Funcionalidades")

    st.write(" Generative AI")
    st.write(" Agentic AI")
    st.write(" Tool Calling")
    st.write(" Memória de conversa")

    st.divider()

    if st.button(
        "🗑️ Limpar conversa",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.agent_history = []
        st.rerun()


# ==========================================
# 9. MENSAGEM INICIAL
# ==========================================

if not st.session_state.messages:

    with st.chat_message("assistant"):

        st.markdown(
            """
            Olá! 👋 Sou o **Chris AI Assistant**.

            Posso ajudar você a:

            - Consultar o clima em qualquer cidade.
            - Comparar temperaturas entre cidades.
            - Pesquisar informações na internet.
            - Responder perguntas gerais.

            **Como posso ajudar você hoje?**
            """
        )


# ==========================================
# 10. HISTÓRICO VISUAL
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# 11. CHAT DO USUÁRIO
# ==========================================

question = st.chat_input(
    "Digite sua pergunta aqui..."
)

if question:

    # Exibir pergunta do usuário
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Executar agente IBM Granite
    with st.chat_message("assistant"):

        with st.spinner(
            "Granite está processando sua pergunta..."
        ):

            try:

                answer = run_agent(
                    question,
                    st.session_state.agent_history
                )

            except Exception as error:

                answer = (
                    "Desculpe, ocorreu um erro ao "
                    "processar sua pergunta. "
                    "Tente novamente."
                )

                # Exibir detalhes apenas no log
                # do servidor, não ao usuário.
                print(
                    f"[ERROR] Falha no agente: "
                    f"{type(error).__name__}: {error}"
                )

        st.markdown(answer)

    # Guardar resposta na interface
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
