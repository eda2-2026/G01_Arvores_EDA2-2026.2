"""
Entidades de domínio do Orquestrador.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    doc_id: int
    title: str
    urgency: int  # 1 (Alta) a 5 (Baixa)
    size_mb: float
    
    @property
    def priority(self) -> int:
        """
        Cálculo de prioridade para a Min-Heap.
        Menor valor numérico = Maior prioridade no topo da fila.
        Ex: Urgência 1 (Alta) com 2MB -> Prioridade 12
        """
        return (self.urgency * 10) + int(self.size_mb)

@dataclass
class Worker:
    worker_id: int
    name: str
    current_doc: Optional[Document] = None