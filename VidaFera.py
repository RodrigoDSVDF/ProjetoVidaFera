# 🚀 Atualização: Treinamento do Chatbot com Objetivos da Mentoria
# ✅ O Chatbot agora é treinado com base nos objetivos contidos no documento da mentoria

import streamlit as st
import openai
import os
from configparser import ConfigParser
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ---------------------------
# 🟡 Configuração da API OpenAI a partir de .ini
# ---------------------------
config = ConfigParser()
config.read('config.ini')

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
# 🟠 Descrição da Mentoria com Base no Documento
# ---------------------------
st.subheader("📌 Sobre a Mentoria:")
st.write("""
- ✅ **Alta demanda:** Orientação personalizada e aceleração de resultados.
- ✅ **Autoridade:** Fortaleça sua marca pessoal e torne-se referência.
- ✅ **Monetização:** Atenda vários mentorados simultaneamente.
- ✅ **Tecnologia:** Use IA e automação para otimizar seu processo.
""")

# ---------------------------
# 💬 Janela de Conversação - Chatbot IA Treinado com Objetivos
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

# ---------------------------
# 🟣 Botão de Contato via WhatsApp
# ---------------------------
if st.button("📲 Fale Conosco via WhatsApp"):
    st.markdown("""
    <a href="https://api.whatsapp.com/send?phone=5561991151740&text=Quero saber mais sobre a mentoria!" target="_blank">
        <button style="background-color:#4CAF50; color:white; padding:10px 20px; font-size:16px; border-radius:10px; cursor:pointer;">
            💬 Abrir WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

# ✅ Atualizações:
# - 🚀 Treinamento do Chatbot com os objetivos descritos no documento
# - 💡 Ajustes para que o agente forneça respostas direcionadas
# - 🛡️ Compatibilidade com API OpenAI versão atualizada





