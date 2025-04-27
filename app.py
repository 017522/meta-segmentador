import streamlit as st
import pandas as pd
import requests

# Configuração da página
st.set_page_config(page_title="Segmentador de Público Meta Ads com IA", page_icon="🎯", layout="wide")

# Função para gerar públicos usando Hugging Face
def gerar_publicos_huggingface(texto):
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": "Bearer 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"
    }
    payload = {
        "inputs": f"""Leia atentamente o briefing abaixo e com base nele, gere 4 tipos de públicos diferentes para anúncios no Meta Ads:
        
        1. Público 01: INTERESSES + CARGOS + COMPORTAMENTOS combinados.
        2. Público 02: Somente INTERESSES mais relevantes.
        3. Público 03: Somente CARGOS relevantes.
        4. Público 04: Somente COMPORTAMENTOS relevantes.

        Atenção: Use segmentações existentes dentro do Meta Ads, seja fiel ao briefing, seja estratégico e assertivo.

        Briefing: {texto}
        """
    }
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Interface do Streamlit
st.title("🎯 Segmentador de Público Meta Ads com IA")

st.caption("Faça upload do briefing do cliente (.txt ou .docx)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["txt", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "txt":
        texto_briefing = uploaded_file.read().decode("utf-8")
    elif file_extension == "docx":
        from docx import Document
        doc = Document(uploaded_file)
        texto_briefing = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
    else:
        st.error("Formato de arquivo não suportado. Envie um arquivo .txt ou .docx.")
        st.stop()

    st.success("Briefing carregado com sucesso! Gerando públicos...")

    try:
        resposta = gerar_publicos_huggingface(texto_briefing)
        resposta_texto = resposta[0]['generated_text']

        st.markdown("---")
        st.subheader("🔎 Públicos Gerados:")
        st.markdown(f"```{resposta_texto}```")

    except Exception as e:
        st.error(f"Erro ao gerar públicos: {e}")
