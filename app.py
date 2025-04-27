import streamlit as st
import pandas as pd
import openai
import os

# Carregar a planilha embutida
planilha = pd.read_excel("Cargo, Comportamentos e Interesses.xlsx")

# Configurar a API KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar públicos usando o GPT
def gerar_publicos(briefing):
    prompt = f"""
Você é um especialista em Meta Ads. Baseado nesse briefing de cliente:
\"\"\"{briefing}\"\"\"
e usando apenas os INTERESSES, CARGOS e COMPORTAMENTOS da planilha que te fornecerei, 
estruture 4 públicos:

Público 01: Interesses + Cargos + Comportamentos combinados
Público 02: Apenas Interesses
Público 03: Apenas Cargos
Público 04: Apenas Comportamentos

A lista disponível é: {planilha.to_string(index=False)}

Importante: use apenas termos da lista. Não invente nada novo.
Retorne organizado.

"""

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500
    )

    return resposta['choices'][0]['message']['content']

# Interface Streamlit
st.set_page_config(page_title="Segmentador de Público Meta Ads", page_icon="🎯")
st.title("🎯 Segmentador de Público Meta Ads com IA")

uploaded_file = st.file_uploader("Faça upload do briefing (.txt ou .docx)", type=["txt", "docx"])

if uploaded_file is not None:
    briefing_texto = uploaded_file.read()

    if uploaded_file.name.endswith(".docx"):
        import docx
        from io import BytesIO

        doc = docx.Document(BytesIO(briefing_texto))
        briefing_texto = "\n".join([p.text for p in doc.paragraphs])

    else:
        briefing_texto = briefing_texto.decode("utf-8")

    st.success("Briefing carregado com sucesso! Gerando públicos...")

    # Gera os públicos
    publicos_gerados = gerar_publicos(briefing_texto)

    st.markdown("---")
    st.subheader("🎯 Públicos Gerados")
    st.markdown(publicos_gerados)
