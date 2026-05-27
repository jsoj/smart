import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(page_title="Gestão de Metas SMART", layout="wide")

DATA_FILE = "metas.csv"

# Função para carregar ou criar o arquivo
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Meta", "Categoria", "Prazo", "Status"])
    return pd.read_csv(DATA_FILE)

# Categorias SMART
categorias = ["Pessoal", "Profissional", "Atividade Física", "Saúde", "Estética", 
              "Familiar", "Espiritual", "Educacional", "Viagem", "Entretenimento", "Diversos"]

st.title("🎯 Gestão de Metas SMART")

# Formulário de Cadastro
with st.form("nova_meta"):
    col1, col2 = st.columns(2)
    meta_desc = col1.text_input("Descrição da Meta (Específica)")
    categoria = col2.selectbox("Categoria", categorias)
    prazo = col1.date_input("Prazo Final")
    status = col2.selectbox("Status", ["A iniciar", "Em andamento", "Atingida"])
    
    if st.form_submit_button("Cadastrar Meta"):
        df = load_data()
        nova_meta = pd.DataFrame([{"Meta": meta_desc, "Categoria": categoria, "Prazo": str(prazo), "Status": status}])
        df = pd.concat([df, nova_meta], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Meta cadastrada!")

# Exibição e Lógica de Cores
st.subheader("Suas Metas")
df = load_data()

if not df.empty:
    def highlight_expired(row):
        is_expired = datetime.strptime(row['Prazo'], '%Y-%m-%d').date() < datetime.now().date()
        if is_expired and row['Status'] != "Atingida":
            return ['color: red'] * len(row)
        return [''] * len(row)

    st.dataframe(df.style.apply(highlight_expired, axis=1), use_container_width=True)

    # Botão de Exportação
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Metas (CSV)", csv, "metas.csv", "text/csv")
else:
    st.info("Nenhuma meta cadastrada ainda.")
