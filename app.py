import streamlit as st
import pandas as pd
import os  # <--- A IMPORTAÇÃO QUE FALTAVA
from datetime import datetime
from PIL import Image

# --- CONFIGURAÇÃO DE ESTILO ---
st.set_page_config(page_title="Treinador SMART", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FDFBF8; }
    h1, h2, h3 { color: #8B5E3C; font-family: 'Helvetica', sans-serif; }
    .stButton>button { background-color: #8B5E3C; color: white; border-radius: 5px; }
    .stDownloadButton>button { background-color: #D4A373; color: white; }
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
        # Certifique-se que o arquivo 2M5A9622-Editar.jpg esteja na pasta raiz
        image = Image.open('2M5A9622-Editar.jpg.jpeg') 
        st.image(image, use_column_width=True)
    except:
        st.warning("Foto da mentora não encontrada na pasta raiz.")
    
    st.markdown("---")
    if st.button("Ir para Arte em Vender"):
        st.link_button("Acesse o site oficial", "https://arteemvender.com/")

# --- CORPO DO APP ---
st.title("🎯 Treinador de Metas SMART")
st.write("Bem-vindo! Este app vai te guiar para que suas metas sejam inabaláveis.")

df = load_data()

with st.form("smart_form"):
    st.subheader("Cadastro Assistido")
    
    categoria = st.selectbox("Categoria", ["Pessoal", "Profissional", "Saúde", "Financeiro", "Educacional", "Outros"])
    
    # Validação: Limite de 3 metas por categoria
    if len(df[df['Categoria'] == categoria]) >= 3:
        st.error(f"Limite de 3 metas atingido para {categoria}. Focar é essencial!")
        st.stop()

    meta = st.text_input("Nome da Meta")
    
    with st.expander("📝 Detalhando a metodologia SMART"):
        esp = st.text_area("S - O que exatamente você quer alcançar?")
        med = st.text_input("M - Qual o indicador numérico/físico?")
        atg = st.text_area("A - Por que essa meta é possível para você hoje?")
        rel = st.text_area("R - Por que essa meta é prioritária?")
        prazo = st.date_input("T - Qual a data limite?")
        
    if st.form_submit_button("Validar e Cadastrar"):
        # Validação: Limite de 3 metas por data
        if len(df[df['Prazo'] == str(prazo)]) >= 3:
            st.error("Já existem 3 metas para esta data. Escolha outro prazo para garantir foco.")
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

st.subheader("Suas Metas")
st.dataframe(df, use_container_width=True)
