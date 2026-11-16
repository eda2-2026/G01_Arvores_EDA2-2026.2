"""
Interface Visual Avançada do Orquestrador.
Execute com: streamlit run app.py
"""
import streamlit as st
import random
from src.entities import Document, Worker
from src.orchestrator import PipelineOrchestrator

st.set_page_config(page_title="Pipeline de IA", layout="wide")

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'pipeline' not in st.session_state:
    st.session_state.pipeline = PipelineOrchestrator()
    st.session_state.doc_id_seq = 100
    st.session_state.worker_id_seq = 1

pipeline = st.session_state.pipeline

def get_active_workers(node, pool):
    if node == pool.TNULL or node.value is None: return []
    return get_active_workers(node.left, pool) + [node] + get_active_workers(node.right, pool)

def get_cache(node):
    if not node: return []
    return get_cache(node.left) + [node.value] + get_cache(node.right)

with st.sidebar:
    st.header("Controles do Pipeline")
    st.divider()
    
    if st.button("1. Inserir Documento", use_container_width=True):
        doc = Document(
            doc_id=st.session_state.doc_id_seq, 
            title=f"Doc_{st.session_state.doc_id_seq}", 
            urgency=random.choice([1, 3, 5]), 
            size_mb=round(random.uniform(1.0, 15.0), 1)
        )
        if pipeline.receive_document(doc):
            st.toast(f"Documento {doc.doc_id} adicionado à fila.")
            st.session_state.doc_id_seq += 1
            
    if st.button("2. Alocar Worker", use_container_width=True):
        if len(pipeline.doc_queue) > 0:
            w = Worker(st.session_state.worker_id_seq, f"Worker-{st.session_state.worker_id_seq}")
            pipeline.assign_worker(w)
            st.toast(f"{w.name} iniciou o processamento.")
            st.session_state.worker_id_seq += 1
            
    if st.button("3. Finalizar Processo", use_container_width=True):
        ativos = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if ativos:
            w_node = random.choice(ativos)
            worker_name = w_node.value.name
            worker_id = w_node.value.worker_id
            
            pipeline.finish_processing(worker_id)
            st.toast(f"{worker_name} finalizado com sucesso.")

st.title("Orquestrador de Processamento de Documentos")
st.markdown("Monitoramento de estruturas de dados em tempo real.")

kpi_ph = st.empty()
board_ph = st.empty()

def render_ui():
    """Desenha a interface baseada no estado atual das árvores."""
    ativos = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
    processados = get_cache(pipeline.cache_root)
    
    with kpi_ph.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Fila (Min-Heap)", len(pipeline.doc_queue))
        c2.metric("Workers (Red-Black)", len(ativos))
        c3.metric("Cache (AVL)", len(processados))
        st.divider()

    with board_ph.container():
        col_heap, col_rb, col_avl = st.columns(3)
        
        with col_heap:
            st.subheader("Aguardando")
            for prio, doc in sorted(pipeline.doc_queue.heap, key=lambda x: x[0]):
                css_class = f"urgency-{doc.urgency}"
                ind_class = "ind-urgent" if doc.urgency == 1 else ("ind-normal" if doc.urgency == 3 else "ind-low")
                badge = "Urgente" if doc.urgency == 1 else ("Normal" if doc.urgency == 3 else "Baixa")
                
                st.markdown(f"""
                <div class="kanban-card {css_class}">
                    <h4>{doc.title}</h4>
                    <p><b>Prioridade: {prio}</b> | {doc.size_mb}MB</p>
                    <p><span class="indicator {ind_class}"></span>{badge}</p>
                </div>
                """, unsafe_allow_html=True)
                
        with col_rb:
            st.subheader("Processando")
            for node in ativos:
                w = node.value
                rb_class = "rb-red" if node.color == "RED" else "rb-black"
                ind_class = "ind-urgent" if node.color == "RED" else "ind-black"
                cor_label = "Nó Vermelho" if node.color == "RED" else "Nó Preto"
                
                if w.current_doc:
                    st.markdown(f"""
                    <div class="kanban-card {rb_class}">
                        <h4>{w.name}</h4>
                        <p>Processando: {w.current_doc.title}</p>
                        <p><span class="indicator {ind_class}"></span>{cor_label}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with col_avl:
            st.subheader("Finalizados")
            for doc in processados[::-1]:
                st.markdown(f"""
                <div class="kanban-card avl-node">
                    <h4>{doc.title}</h4>
                    <p><span class="indicator ind-green"></span>ID: {doc.doc_id} | Cache salvo</p>
                </div>
                """, unsafe_allow_html=True)

render_ui()