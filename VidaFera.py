import streamlit as st
import openai
import os
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ---------------------------
# 🟡 Configuração da API OpenAI (via Render)
# ---------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("A chave da API OpenAI não foi encontrada. Verifique as variáveis de ambiente no Render.")

# ---------------------------
# 🟡 Título da Página
# ---------------------------
st.title("🚀 Página da Mentoria - Instituto Vida FERA")

# ---------------------------
# 🟢 Exibindo Imagem da Mentoria (caminho relativo)
# ---------------------------
st.image("Fera.jpeg", use_column_width=True)

# ---------------------------
# 💬 Janela de Conversação - Chatbot IA Treinado
# ---------------------------
st.subheader("💬 Converse com nosso Agente Inteligente sobre a Mentoria")
model = ChatOpenAI(model="gpt-4o", openai_api_key=openai.api_key)

# Histórico de mensagens
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
        SystemMessage(content="Você é um assistente especializado em mentorias. Responda com base nos objetivos descritos: alta demanda, autoridade, monetização e uso de IA."),
        HumanMessage(content=usuario_input)
    ]

    response = model.invoke(messages)
    resposta = response.content

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.write(resposta)
