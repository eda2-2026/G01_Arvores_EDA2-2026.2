"""
Interface Visual do Orquestrador utilizando Streamlit.
Execute com: streamlit run app.py
"""
import streamlit as st
import random
import time
from src.entities import Document, Worker
from src.orchestrator import PipelineOrchestrator

# 1. Configuração da Página
st.set_page_config(page_title="Pipeline de IA", layout="wide")

# 2. Inicialização do Estado (Singleton do Orquestrador)
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = PipelineOrchestrator()
    st.session_state.doc_id_seq = 100
    st.session_state.worker_id_seq = 1

pipeline = st.session_state.pipeline

st.title("🧠 Orquestrador de Processamento de Documentos")
st.markdown("Fluxo automatizado. O sistema decide quando novos documentos entram, são alocados e finalizados.")

# 3. Preparação dos "Placeholders" para renderização em tempo real
log_ph = st.empty()
st.divider()

col_heap, col_rb, col_avl = st.columns(3)
heap_ph = col_heap.empty()
rb_ph = col_rb.empty()
avl_ph = col_avl.empty()

# Função auxiliar para extrair workers da Red-Black Tree
def get_active_workers(node, pool):
    if node == pool.TNULL or node.value is None:
        return []
    return get_active_workers(node.left, pool) + [node.value] + get_active_workers(node.right, pool)

# Função auxiliar para extrair docs da AVL Tree
def get_cache(node):
    if not node:
        return []
    return get_cache(node.left) + [node.value] + get_cache(node.right)

# 4. Motor de Simulação
if st.button("🚀 Iniciar Simulação Automática (15 Ticks)", use_container_width=True):
    
    for tick in range(1, 16):
        logs_do_tick = []
        
        # AÇÃO 1: 60% de chance de receber um novo documento
        if random.random() > 0.4:
            urgency = random.randint(1, 5)
            size = round(random.uniform(1.0, 15.0), 1)
            doc_id = st.session_state.doc_id_seq if random.random() > 0.1 else random.randint(100, st.session_state.doc_id_seq)
            doc = Document(doc_id=doc_id, title=f"Doc_{doc_id}", urgency=urgency, size_mb=size)
            
            if pipeline.receive_document(doc):
                logs_do_tick.append(f"📥 Doc_{doc.doc_id} entrou na Heap.")
                if doc_id == st.session_state.doc_id_seq:
                    st.session_state.doc_id_seq += 1
            else:
                logs_do_tick.append(f"🚫 Doc_{doc.doc_id} barrado (já na AVL).")

        # AÇÃO 2: Sempre tenta alocar worker se houver fila e não houver muitos workers ativos (máx 3 simultâneos)
        ativos_atuais = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if len(pipeline.doc_queue) > 0 and len(ativos_atuais) < 3:
            wid = st.session_state.worker_id_seq
            w = Worker(worker_id=wid, name=f"Worker-{wid}")
            pipeline.assign_worker(w)
            st.session_state.worker_id_seq += 1
            logs_do_tick.append(f"⚙️ Worker-{wid} foi para a Red-Black.")

        # AÇÃO 3: 50% de chance de finalizar um worker que já está ativo
        ativos_atuais = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
        if ativos_atuais and random.random() > 0.5:
            w_concluido = random.choice(ativos_atuais)
            pipeline.finish_processing(w_concluido.worker_id)
            logs_do_tick.append(f"💾 Worker-{w_concluido.worker_id} finalizou (salvo na AVL).")

        # RENDERIZAÇÃO DA UI (Sobrescrevendo os placeholders)
        if not logs_do_tick:
            log_ph.info(f"**Tick {tick}/15**: Ociosidade...")
        else:
            log_ph.success(f"**Tick {tick}/15**: " + " | ".join(logs_do_tick))

        with heap_ph.container():
            st.subheader("📥 Fila de Prioridade")
            st.caption("Estrutura: Min-Heap")
            st.metric("Docs Aguardando", len(pipeline.doc_queue))
            for prio, doc in sorted(pipeline.doc_queue.heap, key=lambda x: x[0]):
                st.info(f"Prio: **{prio}** | {doc.title} ({doc.size_mb}MB)")

        with rb_ph.container():
            st.subheader("⚙️ Workers Ativos")
            st.caption("Estrutura: Red-Black Tree")
            ativos = get_active_workers(pipeline.worker_pool.root, pipeline.worker_pool)
            st.metric("Processando Agora", len(ativos))
            for w in ativos:
                if w.current_doc:
                    st.warning(f"**{w.name}** processando {w.current_doc.title}")

        with avl_ph.container():
            st.subheader("💾 Histórico (Cache)")
            st.caption("Estrutura: Árvore AVL")
            processados = get_cache(pipeline.cache_root)
            st.metric("Docs Finalizados", len(processados))
            for doc in processados:
                st.success(f"✅ {doc.title} (ID: {doc.doc_id})")

        # Pausa para o usuário ver os dados mudando de coluna
        time.sleep(1.5)
    
    log_ph.warning("Simulação de 15 Ticks concluída! Clique no botão novamente para rodar mais ciclos.")