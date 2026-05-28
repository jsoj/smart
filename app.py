import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Treinador SMART", layout="wide")

# Estilização
st.markdown("""
    <style>
    .main { background-color: #FDFBF8; }
    h1, h2, h3 { color: #8B5E3C; }
    .stButton>button { background-color: #8B5E3C; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- ISOLAMENTO DE USUÁRIO ---
# O Streamlit cria um ID de sessão único para cada usuário/aba do navegador.
if 'user_id' not in st.session_state:
    st.session_state.user_id = st.runtime.scriptrunner.get_script_run_ctx().session_id

DATA_FILE = f"metas_{st.session_state.user_id}.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Meta", "Categoria", "Prazo", "Status", "Especifico", "Mensuravel", "Atingivel", "Relevante"])
    return pd.read_csv(DATA_FILE)

# --- SIDEBAR ---
with st.sidebar:
    try:
        raw_url = "https://raw.githubusercontent.com/jsoj/smart/main/2M5A9622-Editar.jpg.jpeg"
        image = Image.open(BytesIO(requests.get(raw_url).content))
        st.image(image, width=300)
    except:
        st.warning("Foto da mentora não carregada.")
    st.markdown("---")
    st.link_button("Acesse o Arte em Vender", "https://arteemvender.com/", use_container_width=True)

# --- CORPO ---
st.title("🎯 Treinador de Metas Infalíveis")
df = load_data()

with st.form("smart_form", clear_on_submit=True):
    categoria = st.selectbox("Categoria", ["Pessoal", "Profissional", "Saúde", "Financeiro", "Educacional", "Outros"])
    meta = st.text_input("Nome da Meta")
    with st.expander("📝 Detalhando a metodologia SMART"):
        esp = st.text_area("S - O que exatamente você quer alcançar?")
        med = st.text_input("M - Qual o indicador numérico/físico?")
        atg = st.text_area("A - Por que essa meta é possível para você hoje?")
        rel = st.text_area("R - Por que essa meta é prioritária?")
        prazo = st.date_input("T - Qual a data limite?")
    submitted = st.form_submit_button("Validar e Cadastrar")

    if submitted:
        nova_meta = pd.DataFrame([{
            "Meta": meta, "Categoria": categoria, "Prazo": str(prazo), 
            "Status": "A iniciar", "Especifico": esp, "Mensuravel": med,
            "Atingivel": atg, "Relevante": rel
        }])
        df = pd.concat([df, nova_meta], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.rerun()

# --- GESTÃO DA LISTA ---
st.subheader("Suas Metas Cadastradas")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    # Opção para deletar todas as metas
    if st.button("🗑️ Apagar todas as minhas metas"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()
    
    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Metas (CSV)", csv, "metas.csv", "text/csv")
else:
    st.info("Nenhuma meta registrada.")
