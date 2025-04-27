import streamlit as st
import pandas as pd
import requests
import docx
import os

# Configurar HuggingFace API
huggingface_token = os.getenv("HF_TOKEN")
model_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

headers = {
    "Authorization": f"Bearer {huggingface_token}",
    "Content-Type": "application/json"
}

# Função para extrair texto de DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# Função para gerar públicos
def gerar_publicos(texto):
    prompt = f"""
Você é um especialista em Marketing Digital e Meta Ads.

Com base nesse briefing de cliente:

\"\"\"{texto}\"\"\"

Gere 4 sugestões de públicos para campanha de conversão:

- Público 1: Misturando Interesses + Cargos + Comportamentos
- Público 2: Só Interesses
- Público 3: Só Cargos
- Público 4: Só Comportamentos

Formatar a resposta usando Markdown para facilitar a leitura.

Importante: Seja estratégico, escolha segmentações que combinam com a persona do briefing.
    """

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 800}
    }
    response = requests.post(model_url, headers=headers, json=payload)
    resposta = response.json()

    if isinstance(resposta, list) and "generated_text" in resposta[0]:
        return resposta[0]["generated_text"]
    else:
        raise Exception(f"Erro inesperado: {resposta}")

# Streamlit App
st.set_page_config(page_title="Segmentador de Público Meta Ads com IA", layout="wide")
st.title("🎯 Segmentador de Público Meta Ads com IA")
st.caption("Faça upload do briefing do cliente (.txt ou .docx)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["txt", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        briefing_texto = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        briefing_texto = extract_text_from_docx(uploaded_file)
    else:
        st.error("Formato de arquivo não suportado.")
        st.stop()

    try:
        with st.spinner("Carregando e gerando públicos..."):
            publicos_gerados = gerar_publicos(briefing_texto)
        st.success("Públicos gerados com sucesso!")
        st.markdown(publicos_gerados)
    except Exception as e:
        st.error(f"Erro ao gerar públicos: {str(e)}")
