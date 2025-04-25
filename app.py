import streamlit as st
import pandas as pd
from docx import Document

# --- CONFIG PÁGINA ---
st.set_page_config(page_title="Segmentador de Público Meta Ads", layout="centered")
st.title("🎯 Segmentador de Público Meta Ads Sniper")

# --- CARREGAR PLANILHA PADRÃO (3 COLUNAS: Cargos, Comportamento, Interesses) ---
@st.cache_data

def carregar_segmentacoes():
    df = pd.read_excel("Cargo, Comportamentos e Interesses.xlsx")
    dados = []
    for tipo in ["CARGOS", "COMPORTAMENTO", "INTERESSES"]:
        col = df.columns[df.columns.str.upper().str.contains(tipo)].tolist()
        if col:
            for item in df[col[0]].dropna().unique():
                dados.append({"NOME": str(item).strip(), "TIPO": tipo[:-1] if tipo.endswith("S") else tipo})
    return pd.DataFrame(dados)

segmentacoes = carregar_segmentacoes()

# --- UPLOAD DO BRIEFING ---
briefing = st.file_uploader("📝 Faça upload do briefing do cliente (.txt ou .docx)", type=["txt", "docx"])

# --- FUNÇÕES ---
def limpar_texto(texto):
    return texto.strip().lower().replace("\n", " ")

def buscar_segmentacoes(texto, base):
    resultados = {"INTERESSE": [], "CARGO": [], "COMPORTAMENTO": []}
    texto_limpo = limpar_texto(texto)
    for _, row in base.iterrows():
        if row["NOME"].lower() in texto_limpo:
            resultados[row["TIPO"]].append(row["NOME"])
    return resultados

# --- PROCESSAMENTO ---
if briefing:
    if briefing.name.endswith(".txt"):
        texto_briefing = briefing.read().decode("utf-8")
    elif briefing.name.endswith(".docx"):
        doc = Document(briefing)
        texto_briefing = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
    else:
        st.error("Formato de arquivo não suportado.")
        st.stop()

    segmentacoes_encontradas = buscar_segmentacoes(texto_briefing, segmentacoes)

    st.success("✅ Segmentações encontradas com sucesso!")
    st.markdown("---")

    st.header("🎯 Públicos Gerados")

    with st.expander("Público 01: INTERESSE + CARGO + COMPORTAMENTO"):
        for tipo in segmentacoes_encontradas:
            for item in segmentacoes_encontradas[tipo]:
                st.markdown(f"- **{tipo.title()}**: {item}")

    with st.expander("Público 02: Apenas INTERESSES"):
        for i in segmentacoes_encontradas["INTERESSE"]:
            st.markdown(f"- {i}")

    with st.expander("Público 03: Apenas CARGOS"):
        for i in segmentacoes_encontradas["CARGO"]:
            st.markdown(f"- {i}")

    with st.expander("Público 04: Apenas COMPORTAMENTOS"):
        for i in segmentacoes_encontradas["COMPORTAMENTO"]:
            st.markdown(f"- {i}")

else:
    st.warning("⚡ Envie o briefing para gerar os públicos.")
