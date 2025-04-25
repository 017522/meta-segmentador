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

def gerar_padroes_para_persona(texto, base):
    texto = limpar_texto(texto)
    interesses = [x for x in base[base["TIPO"] == "INTERESSE"]["NOME"] if x.lower() in texto]
    cargos = [x for x in base[base["TIPO"] == "CARGO"]["NOME"] if x.lower() in texto]
    comportamentos = [x for x in base[base["TIPO"] == "COMPORTAMENTO"]["NOME"] if x.lower() in texto]

    # fallback se algum grupo ficar vazio
    if not interesses:
        interesses = base[base["TIPO"] == "INTERESSE"]["NOME"].sample(3).tolist()
    if not cargos:
        cargos = base[base["TIPO"] == "CARGO"]["NOME"].sample(3).tolist()
    if not comportamentos:
        comportamentos = base[base["TIPO"] == "COMPORTAMENTO"]["NOME"].sample(3).tolist()

    return interesses, cargos, comportamentos

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

    interesses, cargos, comportamentos = gerar_padroes_para_persona(texto_briefing, segmentacoes)

    st.success("✅ Segmentações geradas com base no briefing!")
    st.markdown("---")

    # Público 01
    st.subheader("Público 01: Interesses + Cargos + Comportamentos")
    min_len = min(len(interesses), len(cargos), len(comportamentos))
    df_p1 = pd.DataFrame({
        "INTERESSES": interesses[:min_len],
        "CARGOS": cargos[:min_len],
        "COMPORTAMENTOS": comportamentos[:min_len]
    })
    st.dataframe(df_p1, use_container_width=True)

    # Público 02
    st.subheader("Público 02: Apenas INTERESSES")
    st.dataframe(pd.DataFrame(interesses, columns=["INTERESSES"]))

    # Público 03
    st.subheader("Público 03: Apenas CARGOS")
    st.dataframe(pd.DataFrame(cargos, columns=["CARGOS"]))

    # Público 04
    st.subheader("Público 04: Apenas COMPORTAMENTOS")
    st.dataframe(pd.DataFrame(comportamentos, columns=["COMPORTAMENTOS"]))

else:
    st.warning("⚡ Envie o briefing para gerar os públicos.")
