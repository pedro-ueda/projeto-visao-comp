import streamlit as st
import pandas as pd
from typing import List
from models.analysis import AnalysisModel

def render_dashboard(records: List[AnalysisModel]):
    st.header("📊 Dashboard de Métricas Analíticas")
    
    if not records:
        st.warning("Sem dados suficientes para geração do Dashboard.")
        return

    # Construção de DataFrame Unificado para Otimização de Filtros
    data = [{
        "ID": r.id,
        "Data": r.created_at,
        "Pessoas": r.quantidade_pessoas,
        "Rostos": r.rostos,
        "Luminosidade": r.luminosidade,
        "Nitidez": r.nitidez
    } for r in records]
    
    df = pd.DataFrame(data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Análises", len(df))
    col2.metric("Total Rostos", int(df["Rostos"].sum()))
    col3.metric("Média Luminosidade", f"{df['Luminosidade'].mean():.1f}")
    col4.metric("Média Nitidez", f"{df['Nitidez'].mean():.1f}")

    st.markdown("### Tendência de Nitidez e Luminosidade")
    st.line_chart(df.set_index("Data")[["Luminosidade", "Nitidez"]])