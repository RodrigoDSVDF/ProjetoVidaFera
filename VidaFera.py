
import streamlit as st
import time
import random
import re

# -----------------------------------------------------
# Configuração da Página
# -----------------------------------------------------
st.set_page_config(
    page_title="FERA Mentoria",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ✅ CSS Personalizado para Responsividade no Celular e Chat Estável
st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none; }
    .stChatInput { position: fixed; bottom: 20px; width: 100%; }
    .stChatMessage { word-wrap: break-word; overflow-wrap: break-word; font-size: 16px; }
    .stTextArea { font-size: 14px; }
    @media (max-width: 768px) {
        .stChatMessage { font-size: 14px !important; line-height: 1.4; padding: 10px; }
        .stTextArea { font-size: 12px; }
    }
    .st-emotion-cache-1d391kg { padding-bottom: 100px !important; }
    /* Classe para manter uma altura mínima e evitar reposicionamento durante a digitação */
    .mensagem-fixa {
        min-height: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# Layout Superior (Título e Imagem)
# -----------------------------------------------------
st.title("👋 Olá! Sou o FeraBot, seu parceiro em estratégias digitais")
st.image("Fera.jpeg", use_container_width=True)

# -----------------------------------------------------
# Banco de Empatia Aprimorado
# -----------------------------------------------------
EMPATIA = {
    "entusiasmo": [
        "Parabéns por ter feito essa escolha! A sua evolução no mercado digital não é só um objetivo, é o nosso compromisso! Vamos construir esse caminho juntos! 🎉",
        "Você está no lugar certo, vou te ajudar a desenvolver seu negócio digital de forma estratégica e eficiente 💡",
        "Parabéns pela escolha, e aí podemos começar? 🚀",
        "Estou super animado para te ajudar! 🔥"
    ],
    "diferencial": [
        "O que nos diferencia? Elaboramos estratégias que geram resultados em 72h! ⏱️",
        "Oferecemos soluções personalizadas para seu Negócio digital 🧬",
        "Tecnologia de ponta + Mentoria especializada = Resultado garantido ✅"
    ],
    "urgencia": [
        "Essa oportunidade é exclusiva! 🌟",
        "Últimos dias com condições especiais! ⏳",
        "Sua concorrência já está agindo... 🚀"
    ],
    "personalizacao": [
        "Para criarmos uma estratégia sob medida...",
        "Isso vai me ajudar a potencializar seus resultados...",
        "Quanto mais detalhes, mais preciso serei... 🎯"
    ]
}

# -----------------------------------------------------
# Função de Digitação Humana
# -----------------------------------------------------
def efeito_humano(texto: str):
    container = st.empty()
    mensagem = ""
    # Pré-aloca espaço para evitar reposicionamento durante a digitação
    container.markdown('<div class="mensagem-fixa"></div>', unsafe_allow_html=True)
    for char in texto:
        mensagem += char
        container.markdown(
            f'<div class="stChatMessage mensagem-fixa">{mensagem}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.04)

# -----------------------------------------------------
# Extração de Nome Aprimorada
# -----------------------------------------------------
def extrair_nome(user_input: str) -> str:
    patterns = [
        r"(?:meu nome é|sou o|sou a|me chamo)\s*([A-Za-zÀ-ÿ]+)",
        r"^[Oo]l[aá],?\s*([A-Za-zÀ-ÿ]+)",
        r"^([A-Za-zÀ-ÿ]{3,})"
    ]
    for pattern in patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    return ""

# -----------------------------------------------------
# Fluxo Conversacional Aprimorado
# -----------------------------------------------------
def gerar_resposta(step: int, input_user: str = "") -> str:
    nome = st.session_state.get('nome', '')
    respostas = {
        1: lambda: (
            f"{random.choice(EMPATIA['entusiasmo'])} {nome}, vamos criar uma estratégia vencedora juntos! 💼\n\n"
            "Você já tem um negócio digital em operação ou está planejando começar? Me conte mais sobre mais detalhes para podermos continuar"
        ),
        2: lambda: (
            f"🌟 {nome}, {random.choice(EMPATIA['diferencial'])}\n\n"
            "Bora lá! Agora me diga, a quanto tempo você decidiu  tomar essa decisão de entrar nesse mercado ou se pensou em uma estratégia préviamente para iniciar?"
        ),
        3: lambda: (
            f"💸 {random.choice(EMPATIA['personalizacao'])} Me responda, como você pretende monetizar? escolha uma opção que mais se aproxima do que você pretende fazer\n\n"
            "1. Mentoria Premium\n2. Produtos Digitais\n3. Serviços\n4. Assinaturas"
        ),
        4: lambda: (
            f"🎯 {nome}, Me diga qual seu maior desafio atualmente com algumas dessas opções?\n\n"
            "🔥 Atrair mais clientes\n🔄 Converter visitantes\n💎 Fidelizar clientes\n🚀 Escalar operações"
        ),
        5: lambda: (
            f"📈 {random.choice(EMPATIA['urgencia'])} {nome}, análise rápida:\n\n"
            "Me responda com uma das opções, se sua operação tem :\n✅ Site profissional\n✅ Funil de vendas\n✅ Automações\n✅ Métricas precisas?"
        ),
        6: lambda: (
            f"🚨 {nome}, {random.choice(EMPATIA['urgencia'])}\n\n"
            "Posso desenvolver seu plano estratégico de ação VIP em até 72h! O que você acha disso? Aceita esse desafio? 😎"
        ),
        7: lambda: (
            f"📅 {nome}, quando devemos começar?\n\n"
            "⏰ Imediatamente, quero começar  a lucrar nesse mercado o mais rápido possível\n🗓 Pretendo começar nos próximos 7 dias\n🎯 Vou planejar para daqui 1 mês"
        ),
        8: lambda: (
            f"🎉 {nome}, tudo pronto!Agora vou liberar seu acesso VIP:\n\n"
            "[Agendar Consultoria Estratégica](https://api.whatsapp.com/send?phone=5561991151740&text=Quero%20falar%20com%20o%20atendimento%20sobre%20a%20mentoria)\n\n"
            "⚠️ Link válido por 24 horas!"
        )
    }
    return respostas.get(step, "Vamos para o próximo nível!")()

# -----------------------------------------------------
# Lógica Principal
# -----------------------------------------------------
def main():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "nome" not in st.session_state:
        st.session_state.nome = ""
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    # ✅ Exibir histórico de mensagens
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ Saudação inicial com atraso
    if st.session_state.step == 0 and not st.session_state.mensagens:
        time.sleep(4)  # Reduzi para 2 segundos (pode ajustar)
        saudacao = (
            "🌟 **Bem-vindo(a) à FERA Mentoria!**\n\n"
            "Sou seu Ferabot, especialista em crescimento digital. Vamos criar uma estratégia sob medida?\n\n"
            "Primeiro, como posso te chamar? 😊"
        )
        with st.chat_message("assistant"):
            efeito_humano(saudacao)
        st.session_state.mensagens.append({"role": "assistant", "content": saudacao})

    # ✅ Entrada do usuário
    user_input = st.chat_input("Digite sua resposta aqui...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.mensagens.append({"role": "user", "content": user_input})

        # ✅ Captura de nome
        if st.session_state.step == 0:
            nome = extrair_nome(user_input)
            if nome:
                st.session_state.nome = nome
                st.session_state.step = 1
                resposta = (
                    f"Muito prazer em te conhecer, {nome}! {random.choice(EMPATIA['entusiasmo'])}\n\n"
                    "Seu caminho para o topo já começou! Saiba que você não está sozinho estou aqui com você nessa jornada 💪"
                )
            else:
                resposta = "✨ Quero te oferecer o melhor atendimento! Como devo te chamar?"
        else:
            st.session_state.step += 1
            resposta = gerar_resposta(st.session_state.step, user_input)

        # ✅ Exibir resposta do bot
        with st.chat_message("assistant"):
            efeito_humano(resposta)
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})

# -----------------------------------------------------
# Execução
# -----------------------------------------------------
if __name__ == "__main__":
    main()
