import streamlit as st
import pandas as pd
import json
from datetime import datetime
from config.config import Config
from database.connection import init_db
from controllers.analysis_controller import AnalysisController
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from PIL import Image

# Configurações globais da interface Streamlit
st.set_page_config(page_title="VisionStream Pro", layout="wide", initial_sidebar_state="expanded")

# Inicialização de dependências críticas de infraestrutura
Config.init_app()
init_db()

controller = AnalysisController()

st.title("👁️ VisionStream Pro — Visão Computacional Enterprise")
render_sidebar()

# Abas funcionais do Core App
tab_capture, tab_history, tab_dash = st.tabs(["📷 Captura em Tempo Real", "📜 Histórico de Análises", "📊 Analytics"])

with tab_capture:
    st.subheader("Dispositivo de Entrada de Vídeo")
    
    # Utilização do hardware do client para evitar custos de infraestrutura do servidor
    camera_image = st.camera_input("Alinhe a câmera para execução do pipeline automático")

    if camera_image is not None:
        st.success("Imagem ingerida com sucesso pelo buffer!")
        bytes_data = camera_image.getvalue()
        
        with st.spinner("Executando extração matricial OpenCV..."):
            try:
                record = controller.process_and_store(bytes_data)
                st.balloons()
                
                st.markdown("### ⚡ Resultados do Processamento Automático")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(record.image_path, caption="Captura Armazenada Localmente", use_container_width=True)
                
                with col2:
                    st.markdown(f"**📝 Descrição:** {record.descricao}")
                    st.markdown(f"**👥 Quantidade de Pessoas:** {record.quantidade_pessoas}")
                    st.markdown(f"**👤 Rostos Identificados:** {record.rostos}")
                    st.markdown(f"**💡 Nível de Luminosidade:** {record.luminosidade}")
                    st.markdown(f"**🎯 Nível de Nitidez:** {record.nitidez}")
                    st.markdown(f"**🎨 Espectro Cromático:** {record.cores}")
                    st.markdown(f"**📅 Data Registro (UTC):** {record.created_at}")
                    
            except Exception as e:
                st.error(f"Falha de execução crítica na ingestão: {str(e)}")

with tab_history:
    st.subheader("🔍 Filtros Avançados e Logs de Auditoria")
    records = controller.fetch_all_records()
    
    if not records:
        st.info("Nenhuma análise catalogada no banco de dados até o momento.")
    else:
        # Ferramentas de busca e exportação massiva
        search_query = st.text_input("Filtrar por descrição ou objetos identificados")
        
        filtered_records = [
            r for r in records 
            if search_query.lower() in r.descricao.lower() or search_query.lower() in (r.objetos or "").lower()
        ]
        
        # Exportações Corporativas Gratuitas
        col_exp1, col_exp2 = st.columns(2)
        raw_export_data = [{
            "id": r.id, "created_at": str(r.created_at), "descricao": r.descricao,
            "luminosidade": r.luminosidade, "nitidez": r.nitidez, "rostos": r.rostos
        } for r in filtered_records]
        
        with col_exp1:
            st.download_button(
                label="📥 Exportar Seleção para CSV",
                data=pd.DataFrame(raw_export_data).to_csv(index=False),
                file_name="vision_export.csv",
                mime="text/csv"
            )
        with col_exp2:
            st.download_button(
                label="📥 Exportar Seleção para JSON",
                data=json.dumps(raw_export_data, indent=4),
                file_name="vision_export.json",
                mime="application/json"
            )
            
        st.markdown("---")
        
        # Renderização do Feed Histórico Dinâmico
        for r in filtered_records:
            with st.container():
                c1, c2, c3 = st.columns([1, 2, 1])
                with c1:
                    try:
                        st.image(r.image_path, width=150)
                    except:
                        st.warning("Imagem indisponível localmente.")
                with c2:
                    st.markdown(f"##### Registro #{r.id} — {r.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                    st.markdown(f"**Descrição:** {r.descricao} | **Objetos:** {r.objetos}")
                    st.markdown(f"📊 *Luminosidade*: {r.luminosidade} | *Nitidez*: {r.nitidez} | *Rostos*: {r.rostos}")
                with c3:
                    with open(r.image_path, "rb") as file:
                        st.download_button(
                            label="Download",
                            data=file,
                            file_name=f"download_{r.id}.jpg",
                            mime="image/jpeg",
                            key=f"dl_{r.id}"
                        )
                    if st.button("Excluir", key=f"del_{r.id}"):
                        if controller.remove_record(r.id, r.image_path):
                            st.toast(f"Registro {r.id} deletado com sucesso!")
                            st.rerun()
                st.markdown("---")

with tab_dash:
    all_records = controller.fetch_all_records()
    render_dashboard(all_records)