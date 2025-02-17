# 🚀 Atualização: Treinamento do Chatbot com Objetivos da Mentoria
# ✅ Corrigido erro de leitura do arquivo config.ini

import streamlit as st
import openai
import os
from configparser import ConfigParser
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ---------------------------
# 🟡 Configuração da API OpenAI com validação e fallback
# ---------------------------
config = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Arquivo config.ini não encontrado em: {config_path}")

config.read(config_path)

if 'openai' not in config or not config.has_option('openai', 'api_key'):
    raise ValueError("Seção [openai] ou chave 'api_key' não encontrada no arquivo config.ini")

openai.api_key = config.get('openai', 'api_key')

# ---------------------------
# 🟡 Título da Página
# ---------------------------
st.title("🚀 Página da Mentoria - Instituto Vida FERA")

# ---------------------------
# 🟢 Exibindo Imagem da Mentoria
# ---------------------------
st.image(r"C:/Users/Rodrigo_df/Downloads/WhatsApp Image 2025-02-16 at 22.40.14.jpeg", use_container_width=True)

# ---------------------------
# 💬 Janela de Conversação - Chatbot IA Treinado
# ---------------------------
st.subheader("💬 Converse com nosso Agente Inteligente sobre a Mentoria")
model = ChatOpenAI(model="gpt-4o", openai_api_key=openai.api_key)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

usuario_input = st.chat_input("Pergunte sobre a mentoria ou como aplicar seus objetivos:")
if usuario_input:
    st.session_state.mensagens.append({"role": "user", "content": usuario_input})
    with st.chat_message("user"):
        st.write(usuario_input)
    
    messages = [
        SystemMessage(content="Você é um assistente especializado em mentorias. Responda com base nos objetivos descritos no documento: alta demanda, autoridade, monetização e uso de IA."),
        HumanMessage(content=usuario_input)
    ]

    response = model.invoke(messages)
    resposta = response.content

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.write(resposta)
