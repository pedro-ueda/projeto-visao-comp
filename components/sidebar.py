import streamlit as st
from database.connection import engine
from sqlalchemy import text

def render_sidebar():
    st.sidebar.title("Configurações & Status")
    st.sidebar.markdown("---")
    
    # Status da Conexão em Tempo Real com o Neon.tech
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.sidebar.success("● Conectado ao Neon.tech")
    except Exception:
        st.sidebar.error("○ Desconectado do Banco")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Arquitetura do Sistema")
    st.sidebar.info(
        "Este ecossistema opera de modo distribuído. Capturas de imagem locais "
        "são ingeridas, indexadas em nuvem e prontas para acoplamento de LLMs."
    )