"""
Motor principal que conecta as três estruturas de dados.
"""
from src.structures.min_heap import MinHeap
from src.structures.avl_tree import AVLTree
from src.structures.red_black_tree import RedBlackTree
from src.entities import Document, Worker

class PipelineOrchestrator:
    def __init__(self):
        self.doc_queue = MinHeap()
        self.worker_pool = RedBlackTree()
        
        self.processed_cache = AVLTree()
        self.cache_root = None

    def receive_document(self, doc: Document) -> bool:
        """
        Tenta adicionar um documento ao pipeline.
        Retorna False se o documento já constar no cache (AVL).
        """
        # Busca O(log n) ultra-rápida no histórico
        if self.processed_cache.search(self.cache_root, doc.doc_id):
            return False
            
        # Insere O(log n) na fila de prioridade
        self.doc_queue.insert(doc.priority, doc)
        return True

    def assign_worker(self, worker: Worker) -> bool:
        """
        Atribui o documento mais prioritário a um worker livre.
        """
        if len(self.doc_queue) == 0:
            return False
            
        # Pega O(1) da Heap
        _, doc = self.doc_queue.extract_min()
        worker.current_doc = doc
        
        # Insere O(log n) na Red-Black (Pool de processos ativos)
        self.worker_pool.insert(worker.worker_id, worker)
        return True

    def finish_processing(self, worker_id: int) -> bool:
        """
        Conclui o processamento, limpa o worker e salva o documento no cache.
        """
        node = self.worker_pool.search(worker_id)
        if node and node != self.worker_pool.TNULL:
            worker = node.value
            doc = worker.current_doc
            
            if doc:
                # Salva O(log n) no histórico
                self.cache_root = self.processed_cache.insert(self.cache_root, doc.doc_id, doc)
            
            # Limpa o estado do worker
            worker.current_doc = None
            
            # Soft-delete na Red-Black para simplificar o simulador
            # (Em produção, aqui entraria o método completo delete() com os 6 casos de balanceamento)
            node.value = None 
            return True
            
        return False