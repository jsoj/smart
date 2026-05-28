import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

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

# --- SIDEBAR ---
with st.sidebar:
    try:
        image = Image.open('2M5A9622-Editar.jpg') 
        st.image(image, width=300)
    except:
        st.warning("Foto da mentora não encontrada.")
    st.markdown("---")
    st.link_button("Acesse o Arte em Vender", "https://arteemvender.com/", use_container_width=True)

# --- CORPO ---
st.title("🎯 Treinador de Metas SMART")
df = load_data()

# Validações prévias fora do form
categorias_disponiveis = ["Pessoal", "Profissional", "Saúde", "Financeiro", "Educacional", "Outros"]
st.subheader("Cadastro Assistido")

with st.form("smart_form"):
    categoria = st.selectbox("Categoria", categorias_disponiveis)
    meta = st.text_input("Nome da Meta")
    
    with st.expander("📝 Detalhando a metodologia SMART"):
        esp = st.text_area("S - O que exatamente você quer alcançar?")
        med = st.text_input("M - Qual o indicador numérico/físico?")
        atg = st.text_area("A - Por que essa meta é possível para você hoje?")
        rel = st.text_area("R - Por que essa meta é prioritária?")
        prazo = st.date_input("T - Qual a data limite?")
        
    submitted = st.form_submit_button("Validar e Cadastrar")

    if submitted:
        # Lógica de validação pós-clique
        limite_cat = len(df[df['Categoria'] == categoria]) >= 3
        limite_prazo = len(df[df['Prazo'] == str(prazo)]) >= 3
        
        if limite_cat:
            st.error(f"⚠️ Limite de 3 metas atingido para {categoria}. Focar é essencial!")
        elif limite_prazo:
            st.error("⚠️ Já existem 3 metas para esta data. Escolha outro prazo para garantir foco.")
        else:
            nova_meta = pd.DataFrame([{
                "Meta": meta, "Categoria": categoria, "Prazo": str(prazo), 
                "Status": "A iniciar", "Especifico": esp, "Mensuravel": med,
                "Atingivel": atg, "Relevante": rel
            }])
            df = pd.concat([df, nova_meta], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Meta SMART registrada com sucesso!")
            st.rerun()

st.subheader("Suas Metas Cadastradas")
st.dataframe(df, use_container_width=True)
