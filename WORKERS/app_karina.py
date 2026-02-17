
import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Leads AI - Gerador de Comandos", page_icon="🌹", layout="centered")

st.markdown("""
<style>
    .reportview-container { background: #ffffff }
    .sidebar .sidebar-content { background: #f0f2f6 }
    h1 { font-family: 'Helvetica Neue', sans-serif; color: #333; }
    .stButton>button {
        width: 100%;
        background-color: #10a37f; /* Cor do ChatGPT */
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌹 Leads AI: Gerador de Prompt Mestre")
st.write("Como estamos sem créditos na API, vamos usar o modo **'Cérebro Portátil'**.")
st.info("👇 1. Digite o que você quer. 2. Copie o Texto Mágico. 3. Cole no seu ChatGPT.")

# --- 1. DEFINIÇÃO DA ESTRATÉGIA (O Segredo) ---
SYSTEM_PROMPT_TEMPLATE = """
# ATUE COMO O ESTRATEGISTA "KARINA BOTTI AI"

## 1. SUA PERSONA (QUEM VOCÊ É)
Você é a versão digital da terapeuta Karina Botti.
- **Tom de Voz:** Poético, vulnerável, "pé no chão", usa metáforas (rosas com espinhos, casa interior).
- **Filosofia:** "Legitimar a vida possível". Trocar perfeição por presença.
- **Público:** Mães sobrecarregadas, esposas, mulheres cristãs.

## 2. O MÉTODO C.A.S.A. (Sua Bússola)
Todo conteúdo deve passar por um destes pilares:
1. **Consciência:** Sair do automático.
2. **Aceitação:** Validar a dor sem julgar.
3. **Sentido:** Encontrar Deus/Propósito no caos.
4. **Ação:** Pequeno passo prático.

## 3. SUA TAREFA AGORA
Crie o seguinte conteúdo com ALMA (nada robótico):
**Formato:** {formato}
**Tema/Dor:** {tema}

{detalhes_extras}

---
Capriche na resposta, use quebras de linha e emojis suaves (🌹, ✨, 🤍).
"""

# --- 2. INTERFACE DE COMANDO ---

col1, col2 = st.columns(2)
with col1:
    formato = st.selectbox("Formato do Conteúdo:", 
        ["Post Instagram (Reels/Feed)", "Roteiro de Live/Aula", "Sequência de Stories", "E-mail para Lista", "Brainstorm Livre"])

with col2:
    tom = st.selectbox("Tom da mensagem:", ["Acolhedor (Abraço)", "Firme (Guia)", "Vulnerável (Amiga)", "Inspirador (Fé)"])

tema = st.text_area("O que vamos criar? (Descreva o tema, dor ou ideia)", height=100, placeholder="Ex: Quero falar sobre a culpa de gritar com os filhos...")

# --- 3. GERADOR DE MÁGICA ---
if st.button("✨ GERAR COMANDO MÁGICO"):
    if not tema:
        st.warning("Escreva um tema primeiro!")
    else:
        # Montar o Prompt
        detalhes = f"Use um tom {tom}."
        prompt_final = SYSTEM_PROMPT_TEMPLATE.format(
            formato=formato,
            tema=tema,
            detalhes_extras=detalhes
        )

        st.success("✅ Comando Gerado! Agora é só copiar e colar.")
        
        # Exibir o prompt para cópia fácil
        st.code(prompt_final, language="markdown")
        
        st.markdown("---")
        st.markdown("### 🚀 Próximo Passo:")
        st.markdown("1. Clique no cantinho do bloco acima para **Copiar**.")
        st.markdown("2. Clique no botão abaixo para abrir o ChatGPT.")
        st.link_button("Abrir ChatGPT (chat.openai.com)", "https://chat.openai.com")
