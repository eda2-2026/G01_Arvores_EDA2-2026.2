"""
Implementação de uma Min-Heap (Fila de Prioridade).
O nó raiz sempre conterá o elemento de menor valor numérico.
"""
from typing import Any, Tuple

class MinHeap:
    def __init__(self):
        self.heap: list[Tuple[int, Any]] = []

    def __len__(self) -> int:
        return len(self.heap)

    def _parent(self, index: int) -> int:
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, priority: int, item: Any) -> None:
        """
        Insere um novo item na heap e refaz o balanceamento para cima (heapify up).
        """
        self.heap.append((priority, item))
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self) -> Tuple[int, Any]:
        """
        Remove e retorna o item com a menor prioridade (o mais urgente).
        Levanta IndexError se a heap estiver vazia.
        """
        if not self.heap:
            raise IndexError("extract_min() called on empty heap")
        
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return root

    def _heapify_up(self, index: int) -> None:
        """
        Move o elemento para cima até restaurar a propriedade da Min-Heap.
        """
        parent = self._parent(index)
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        """
        Move o elemento para baixo até restaurar a propriedade da Min-Heap.
        """
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left

        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)