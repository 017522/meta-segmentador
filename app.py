import streamlit as st
import pandas as pd
import openai
import docx

# Usa a chave que está nas secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Carregar a base de segmentações embutida
@st.cache_data
def carregar_segmentacoes():
    return pd.read_excel("Cargo, Comportamentos e Interesses.xlsx")

# Função para ler arquivo .txt ou .docx
def ler_arquivo(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return None

# Função para conversar com a API OpenAI
def gerar_publicos(texto_briefing):
    prompt = f"""
Você é um especialista em tráfego pago.

Baseado no briefing abaixo:
\"\"\"{texto_briefing}\"\"\"

Analise a persona descrita e cruze com a nossa lista de segmentações.

Monte 4 públicos:

- Público 01: Interesses + Cargos + Comportamentos
- Público 02: Apenas Interesses
- Público 03: Apenas Cargos
- Público 04: Apenas Comportamentos

Utilize somente segmentações disponíveis. NÃO invente nada.

Responda estruturado, separado por tópicos.

Capriche para ser estratégico!

"""

    resposta = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um especialista em segmentação para Meta Ads."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return resposta.choices[0].message.content

# --- Interface no Streamlit ---

st.title("🎯 Segmentador de Público Meta Ads com IA")
st.caption("Faça upload do briefing (.txt ou .docx)")

arquivo_briefing = st.file_uploader("Drag and drop file here", type=["txt", "docx"])

if arquivo_briefing:
    briefing_texto = ler_arquivo(arquivo_briefing)

    st.success("Briefing carregado com sucesso! Gerando públicos...")

    segmentacoes_df = carregar_segmentacoes()

    try:
        publicos_gerados = gerar_publicos(briefing_texto)

        st.subheader("Públicos Gerados:")
        st.write(publicos_gerados)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
