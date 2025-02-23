import time
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

# ========== BASE DE CONHECIMENTO CORRIGIDA ==========
MANUAL_INFO = {
    "titulo": "Manual de Alta Performance com IA",
    "autor": "Rodrigo Carvalho",
    "conteudo": {
        "capitulos": [
            "1. Fundamentos da Inteligência Aumentada",
            "2. Automação Inteligente de Tarefas",
            "3. Ferramentas exclusivas para produtividade",
            "4. Análise de Dados com IA",
            "5. Estratégias de Produtividade Avançadas",
            "6. Atualização constante do Manual com novas ferramentas",
            "7. Otimização de Processos Empresariais",
            "8. Técnicas Avançadas de Produtividade",
            "9. Breve crítica ao modo de usar a Inteligência Artificial e seus prejuízos",
            "10.Papo filosófico sobre I.A e consciência humana",
            "11.Inteligência artificial na Educação"
        ],
        "ferramentas": [
            "Automações para negócios",
            "Assistentes  Inteligentes e Personalizados",
            "Sistemas de Gestão Inteligente"
        ],
        "beneficios": [
            "Redução de 40% no tempo de tarefas operacionais",
            "O livro oferece atualização vitalícia"
            "Melhor aproveitamento nos estudos",
            "Aumento de produtividade e eficiência"
            "Aumento de receita nas vendas"
            "Aumento de 60% na precisão de análises",
            "Checklist de implementação passo a passo"
            "Valor do Livro é por tempo ilimitado e está 19,90"
        ]
    }
}

# ========== CLASSE DE MEMÓRIA CORRIGIDA ==========
class ManualMemory:
    def __init__(self):
        self.context = []
    
    def add_context(self, user_input: str, response: str):
        self.context.append(f"Usuário: {user_input}\nAssistente: {response}")
    
    def get_relevant_info(self, query: str) -> str:
        keywords = ["ferramenta", "capítulo", "benefício", "como funciona", "exemplo"]
        if any(kw in query.lower() for kw in keywords):
            return (
                f"Informações do Manual:\n"
                # CORREÇÃO DOS PARÊNTESES AQUI
                f"Capítulos: {', '.join(MANUAL_INFO['conteudo']['capitulos'])}\n"
                f"Ferramentas: {', '.join(MANUAL_INFO['conteudo']['ferramentas'])}\n"
                f"Benefícios: {', '.join(MANUAL_INFO['conteudo']['beneficios'])}"
            )
        return ""

# ========== CONFIGURAÇÃO DO PROMPT ==========
def get_enhanced_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", 
         f"""Você é o assistente especialista no {MANUAL_INFO['titulo']}. 
         Use estas informações em suas respostas:
         Autor: {MANUAL_INFO['autor']}
         Capítulos: {MANUAL_INFO['conteudo']['capitulos']}
         Ferramentas: {MANUAL_INFO['conteudo']['ferramentas']}
         Benefícios: {MANUAL_INFO['conteudo']['beneficios']}
         Sempre seja amigável e profissional."""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

# ========== LÓGICA PRINCIPAL ==========
class SalesFunnel:
    def __init__(self):
        self.memory = ManualMemory()
        self.llm_chain = LLMChain(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
            prompt=get_enhanced_prompt(),
            memory=ConversationBufferWindowMemory(
                memory_key="chat_history",
                input_key="input",
                k=5,
                return_messages=True
            )
        )
    
    def generate_response(self, user_input: str) -> str:
        context = self.memory.get_relevant_info(user_input)
        response = self.llm_chain.invoke({
            "input": f"{context}\nPergunta: {user_input}"
        })
        self.memory.add_context(user_input, response['text'])
        return response['text']

# ========== INTERFACE ==========
st.set_page_config(
    page_title=f"Especialista em {MANUAL_INFO['titulo']}",
    page_icon="🤖",
    layout="centered"
)

# --- Modificações Pontuais ---
# 1. Inclusão de espaço para imagem
st.image("Design sem nome (5).png", caption=MANUAL_INFO['titulo'])

# 2. Ajuste da janela de contexto para caber em telas menores (CSS responsivo)
st.markdown(
    """
    <style>
    /* Ajusta a largura do conteúdo para telas menores */
    .css-1d391kg, .css-1kyxreq {
        max-width: 100% !important;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- Fim das Modificações ---

if "funnel" not in st.session_state:
    st.session_state.funnel = SalesFunnel()
    st.session_state.chat_history = [
        AIMessage(content=f"🌟 Olá! Sou o especialista em {MANUAL_INFO['titulo']}. Como posso ajudá-lo hoje? 😊")
    ]

for msg in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(msg, AIMessage) else "Human"):
        st.write(msg.content)

user_input = st.chat_input("Escreva sua pergunta sobre IA aqui...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    
    with st.chat_message("Human"):
        st.write(user_input)
    
    with st.chat_message("AI"):
        response = st.session_state.funnel.generate_response(user_input)
        response_placeholder = st.empty()
        full_response = ""
        
        for char in response:
            full_response += char
            response_placeholder.markdown(full_response)
            time.sleep(0.03)
        
    st.session_state.chat_history.append(AIMessage(content=full_response))
    
    if "compra" in full_response.lower():
        st.markdown("### 🚀 Garanta Seu Acesso Imediato! Por apenas 19.90")
        st.link_button("Adquirir Manual Completo", "https://pay.cakto.com.br/5dUKrWD")
