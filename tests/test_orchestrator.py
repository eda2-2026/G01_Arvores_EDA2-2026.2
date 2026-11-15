import pytest
from src.entities import Document, Worker
from src.orchestrator import PipelineOrchestrator

def test_full_pipeline_flow():
    orchestrator = PipelineOrchestrator()
    
    doc1 = Document(doc_id=101, title="Contrato Social", urgency=2, size_mb=5.0)
    doc2 = Document(doc_id=102, title="RG - Urgente", urgency=1, size_mb=1.0)
    
    # 1. Entrada: Documentos vão para a Heap
    assert orchestrator.receive_document(doc1) is True
    assert orchestrator.receive_document(doc2) is True
    assert len(orchestrator.doc_queue) == 2
    
    # 2. Alocação: Worker pega o mais urgente da Heap (doc2 tem urgency=1)
    w1 = Worker(worker_id=1, name="Worker-GPU-1")
    assert orchestrator.assign_worker(w1) is True
    assert w1.current_doc.doc_id == 102
    
    # Worker deve estar ativo na Red-Black
    rb_node = orchestrator.worker_pool.search(1)
    assert rb_node.value == w1
    
    # 3. Finalização: Worker conclui o processo
    assert orchestrator.finish_processing(1) is True
    assert w1.current_doc is None  # Worker liberado
    
    # 4. Cache: Documento 102 deve estar salvo na AVL
    avl_node = orchestrator.processed_cache.search(orchestrator.cache_root, 102)
    assert avl_node is not None
    assert avl_node.key == 102
    
    # 5. Prevenção de Duplicidade: Tentar reenviar o doc 102 deve ser barrado
    assert orchestrator.receive_document(doc2) is False