import streamlit as st
import pandas as pd

# --- CONFIG PÁGINA ---
st.set_page_config(page_title="Gerador de Públicos Meta", layout="centered")

st.title("🎯 Segmentador de Público Meta Ads Sniper")

# --- CARREGAR PLANILHA EMBUTIDA ---
@st.cache_data

def carregar_segmentacoes():
    df = pd.read_excel("Cargo, Comportamentos e Interesses.xlsx")
    df.columns = df.columns.str.upper()
    return df

segmentacoes = carregar_segmentacoes()

# --- UPLOAD DO BRIEFING ---
briefing = st.file_uploader("📝 Faça upload do briefing do cliente (.txt)", type=["txt"])

# --- FUNÇÕES AUXILIARES ---
def limpar_texto(texto):
    return texto.strip().lower().replace("\n", " ")

def buscar_segmentacoes(texto, df_segmentacoes):
    resultados = {"INTERESSES": [], "CARGOS": [], "COMPORTAMENTOS": []}
    texto_limpo = limpar_texto(texto)
    for tipo in resultados.keys():
        segmentos = df_segmentacoes[df_segmentacoes["TIPO"] == tipo]["NOME"].tolist()
        for s in segmentos:
            if s.lower() in texto_limpo:
                resultados[tipo].append(s)
    return resultados

# --- PROCESSAR ---
if briefing:
    texto_briefing = briefing.read().decode("utf-8")
    segmentacoes_encontradas = buscar_segmentacoes(texto_briefing, segmentacoes)

    st.success("✅ Segmentações encontradas!")

    st.markdown("---")
    st.header("🎯 Públicos Gerados")

    with st.expander("🎯 Público 01: INTERESSES + CARGOS + COMPORTAMENTOS"):
        for tipo in segmentacoes_encontradas:
            for item in segmentacoes_encontradas[tipo]:
                st.markdown(f"- **{tipo.title()}**: {item}")

    with st.expander("🎯 Público 02: Apenas INTERESSES"):
        for i in segmentacoes_encontradas["INTERESSES"]:
            st.markdown(f"- {i}")

    with st.expander("🎯 Público 03: Apenas CARGOS"):
        for i in segmentacoes_encontradas["CARGOS"]:
            st.markdown(f"- {i}")

    with st.expander("🎯 Público 04: Apenas COMPORTAMENTOS"):
        for i in segmentacoes_encontradas["COMPORTAMENTOS"]:
            st.markdown(f"- {i}")

else:
    st.warning("⚡ Envie o briefing para gerar os públicos.")
