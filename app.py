"""
Interface Visual Avançada do Orquestrador.
Execute com: streamlit run app.py
"""
import streamlit as st
import random
import time
from src.entities import Document, Worker
from src.orchestrator import PipelineOrchestrator

# 1. Configuração da Página e CSS Customizado (Tema Escuro/Claro)
st.set_page_config(page_title="Pipeline de IA", layout="wide", page_icon="🧠")

st.markdown("""
<style>
    /* Estilos dos Cards do Kanban */
    .kanban-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background-color: #262730; /* Fundo escuro padrão Streamlit */
        color: white;
        font-family: sans-serif;
    }
    .kanban-card h4 { margin: 0 0 10px 0; font-size: 16px; }
    .kanban-card p { margin: 0; font-size: 14px; color: #cccccc; }
    
    /* Cores de Prioridade da Min-Heap */
    .urgency-1 { border-left: 6px solid #ff4b4b; } /* Urgente (Vermelho) */
    .urgency-3 { border-left: 6px solid #ffa421; } /* Normal (Laranja) */
    .urgency-5 { border-left: 6px solid #00c0f2; } /* Baixa (Azul) */
    
    /* Cores da Árvore Red-Black */
    .rb-red { border: 2px solid #ff4b4b; background-color: #3b2020; }
    .rb-black { border: 2px solid #555555; background-color: #1e1e1e; }
    
    /* Cor do Cache (AVL) */
    .avl-node { border-left: 6px solid #18B551; } /* Verde estilo Neoenergia */
</style>
""", unsafe_allow_html=True)

# 2. Inicialização do Estado
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = PipelineOrchestrator()
    st.session_state.doc_id_seq = 100
    st.session_state.worker_id_seq = 1

pipeline = st.session_state.pipeline

# 3. Funções Auxiliares de Varredura (Traversal)
def get_active_workers(node, pool):
    if node == pool.TNULL or node.value is None: return []
    return get_active_workers(node.left, pool) + [node] + get_active_workers(node.right, pool)

def get_cache(node):
    if not node: return []
    return get_cache(node.left) + [node.value] + get_cache(node.right)

# 4. Sidebar (Painel de Controle)
with st.sidebar:
    st.header("🎛️ Controles")
    
    st.subheader("Modo Manual")
    if st.button("📥 1. Inserir Documento", use_container_width=True):
        doc = Document(
            doc_id=st.session_state.doc_id_seq, 
            title=f"Doc_{st.session_state.doc_id_seq}", 
            urgency=random.choice([1, 3, 5]), 
            size_mb=round(random.uniform(1.0, 15.0), 1)
        )
        if pipeline.receive_document(doc):
            st.toast(f"📄 Doc_{doc.doc_id} na Fila!", icon="📥")
            st.session_state.doc_id_seq += 1
            
    if st.button("⚙️ 2. Alocar Worker", use_container_width=True):
        if len(pipeline.doc_queue) > 0:
            w = Worker(st.session_state.worker_id_seq, f"Worker-{st.session_state.worker_id_seq}")
            pipeline.assign_worker(w)
            st.toast(f"🤖 {w.name} iniciou processamento.", icon="⚙️")
            st.session_state.worker_id_seq += 1
            
    if st.button("💾 3. Finalizar Processo", use_container_width=True):
        ativos = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if ativos:
            w_node = random.choice(ativos)
            
            # 1. Salva os dados ANTES de limpar o nó da Red-Black
            worker_name = w_node.value.name
            worker_id = w_node.value.worker_id
            
            # 2. Executa a finalização (que seta value = None internamente)
            pipeline.finish_processing(worker_id)
            
            # 3. Exibe o toast usando a string salva
            st.toast(f"✅ {worker_name} concluído!", icon="💾")
            
    st.divider()
    st.subheader("Modo Automático")
    auto_run = st.button("🚀 Rodar Simulação (10 Ticks)", type="primary", use_container_width=True)

# 5. Área Principal (Dashboard e Kanban)
st.title("Orquestrador de Processamento IA")

# Placeholders para atualização dinâmica
kpi_ph = st.empty()
board_ph = st.empty()

def render_ui():
    """Função que desenha a interface baseada no estado atual das árvores."""
    ativos = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
    processados = get_cache(pipeline.cache_root)
    
    # Renderiza KPIs
    with kpi_ph.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Docs na Fila (Heap)", len(pipeline.doc_queue))
        c2.metric("Workers Ativos (RB-Tree)", len(ativos))
        c3.metric("Concluídos (AVL-Tree)", len(processados))
        st.divider()

    # Renderiza Quadro Kanban
    with board_ph.container():
        col_heap, col_rb, col_avl = st.columns(3)
        
        with col_heap:
            st.subheader("📥 Aguardando (Min-Heap)")
            for prio, doc in sorted(pipeline.doc_queue.heap, key=lambda x: x[0]):
                css_class = f"urgency-{doc.urgency}"
                badge = "🔴 Urgente" if doc.urgency == 1 else ("🟠 Normal" if doc.urgency == 3 else "🔵 Baixa")
                st.markdown(f"""
                <div class="kanban-card {css_class}">
                    <h4>{doc.title}</h4>
                    <p><b>Prio: {prio}</b> | {doc.size_mb}MB</p>
                    <p>{badge}</p>
                </div>
                """, unsafe_allow_html=True)
                
        with col_rb:
            st.subheader("⚙️ Processando (Red-Black)")
            for node in ativos:
                w = node.value
                # Mostra visualmente a cor do nó na árvore
                rb_class = "rb-red" if node.color == "RED" else "rb-black"
                cor_label = "🔴 Nó Vermelho" if node.color == "RED" else "⚫ Nó Preto"
                if w.current_doc:
                    st.markdown(f"""
                    <div class="kanban-card {rb_class}">
                        <h4>🤖 {w.name}</h4>
                        <p>Processando: {w.current_doc.title}</p>
                        <p><i>{cor_label}</i></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with col_avl:
            st.subheader("💾 Histórico (AVL)")
            for doc in processados[::-1]: # Mostra os mais recentes no topo
                st.markdown(f"""
                <div class="kanban-card avl-node">
                    <h4>✅ {doc.title}</h4>
                    <p>ID: {doc.doc_id} | Finalizado</p>
                </div>
                """, unsafe_allow_html=True)

# Primeira renderização (estado atual)
render_ui()

# 6. Motor de Simulação (se o botão automático for clicado)
if auto_run:
    for tick in range(1, 11):
        # Lógica de inserção (50% chance)
        if random.random() > 0.5:
            doc = Document(st.session_state.doc_id_seq, f"Doc_{st.session_state.doc_id_seq}", random.choice([1,3,5]), 5.0)
            if pipeline.receive_document(doc): st.session_state.doc_id_seq += 1
            
        # Lógica de alocação
        ativos_atuais = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if len(pipeline.doc_queue) > 0 and len(ativos_atuais) < 4:
            w = Worker(st.session_state.worker_id_seq, f"Worker-{st.session_state.worker_id_seq}")
            pipeline.assign_worker(w)
            st.session_state.worker_id_seq += 1
            
        # Lógica de conclusão (40% chance)
        ativos_atuais = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if ativos_atuais and random.random() > 0.6:
            pipeline.finish_processing(random.choice(ativos_atuais).value.worker_id)

        # Atualiza a UI e pausa
        render_ui()
        time.sleep(1.2)