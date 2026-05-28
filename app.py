import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Treinador SMART", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FDFBF8; }
    h1, h2, h3 { color: #8B5E3C; font-family: 'Helvetica', sans-serif; }
    .stButton>button { background-color: #8B5E3C; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "metas.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Meta", "Categoria", "Prazo", "Status", "Especifico", "Mensuravel", "Atingivel", "Relevante"])
    return pd.read_csv(DATA_FILE)

# --- SIDEBAR (Correção da Foto via URL do GitHub) ---
with st.sidebar:
    try:
        # A URL precisa ser o link "raw" do GitHub para baixar o arquivo diretamente
        raw_url = "https://raw.githubusercontent.com/jsoj/smart/main/2M5A9622-Editar.jpg.jpeg"
        response = requests.get(raw_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, width=300)
    except:
        st.warning("Erro ao carregar foto. Verifique a URL.")
    
    st.markdown("---")
    st.link_button("Acesse o Arte em Vender", "https://arteemvender.com/", use_container_width=True)

# --- CORPO ---
st.title("🎯 Treinador de Metas SMART")
df = load_data()

# Formulário: O Streamlit limpa os campos automaticamente após o rerun se estiver dentro do form
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
        limite_cat = len(df[df['Categoria'] == categoria]) >= 3
        limite_prazo = len(df[df['Prazo'] == str(prazo)]) >= 3
        
        if limite_cat:
            st.error(f"⚠️ Limite de 3 metas atingido para {categoria}.")
        elif limite_prazo:
            st.error("⚠️ Já existem 3 metas para esta data.")
        else:
            nova_meta = pd.DataFrame([{
                "Meta": meta, "Categoria": categoria, "Prazo": str(prazo), 
                "Status": "A iniciar", "Especifico": esp, "Mensuravel": med,
                "Atingivel": atg, "Relevante": rel
            }])
            df = pd.concat([df, nova_meta], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Meta registrada!")

# --- EXIBIÇÃO E DOWNLOAD ---
st.subheader("Suas Metas Cadastradas")
st.dataframe(df, use_container_width=True)

if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Metas em Excel (CSV)",
        data=csv,
        file_name="minhas_metas_smart.csv",
        mime="text/csv"
    )
