import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração e Carregamento
st.set_page_config(page_title="Treinador SMART", layout="wide")
DATA_FILE = "metas.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Meta", "Categoria", "Prazo", "Status", "Especifico", "Mensuravel", "Atingivel", "Relevante"])
    return pd.read_csv(DATA_FILE)

# Interface
st.title("🚀 Treinador de Metas SMART")
st.write("Bem-vindo! Este app vai te guiar para que suas metas sejam inabaláveis.")

# Dicionário de conceitos
conceitos = {
    "S": "Específica: O que exatamente? Quem? Onde? Evite ambiguidades.",
    "M": "Mensurável: Qual o número/indicador de sucesso? Como você vai medir?",
    "A": "Atingível: É realista com seus recursos e tempo atuais?",
    "R": "Relevante: Por que importa? Conecta-se com seu propósito?",
    "T": "Temporal: Qual a data limite exata (Dia/Mês/Ano)?"
}

df = load_data()

with st.form("smart_form"):
    st.subheader("Cadastro Assistido")
    
    categoria = st.selectbox("Categoria", ["Pessoal", "Profissional", "Saúde", "Financeiro", "Educacional", "Outros"])
    
    # Validação de Categoria (Limite de 3)
    if len(df[df['Categoria'] == categoria]) >= 3:
        st.error(f"Limite de 3 metas atingido para {categoria}. Focar é essencial para o sucesso!")
        st.stop()

    meta = st.text_input("Nome da Meta")
    
    # Campos SMART com ajuda
    with st.expander("📝 Detalhando a metodologia SMART"):
        esp = st.text_area("S - O que exatamente você quer alcançar?")
        med = st.text_input("M - Qual o indicador numérico/físico?")
        atg = st.text_area("A - Por que essa meta é possível para você hoje?")
        rel = st.text_area("R - Por que essa meta é prioritária?")
        prazo = st.date_input("T - Qual a data limite?")
        
        # Validação de Prazo (Limite de 3)
        if len(df[df['Prazo'] == str(prazo)]) >= 3:
            st.error("Já existem 3 metas para esta data. Escolha outro prazo para garantir foco total.")
            st.stop()

    if st.form_submit_button("Validar e Cadastrar"):
        # Modal de Confirmação (Simulação via st.warning)
        st.warning("⚖️ Tribunal da Meta: Você respondeu tudo com honestidade? Se a meta for grande, quebre-a em menores. Se for vaga, especifique.")
        
        nova_meta = pd.DataFrame([{
            "Meta": meta, "Categoria": categoria, "Prazo": str(prazo), 
            "Status": "A iniciar", "Especifico": esp, "Mensuravel": med,
            "Atingivel": atg, "Relevante": rel
        }])
        
        df = pd.concat([df, nova_meta], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Meta SMART registrada com sucesso!")

# Exibição
st.dataframe(df, use_container_width=True)
