import pytest
from src.structures.min_heap import MinHeap

def test_min_heap_insert_and_extract():
    heap = MinHeap()
    heap.insert(3, "Contrato Padrão")
    heap.insert(1, "Documento Judicial Urgente")
    heap.insert(2, "Fatura")

    assert len(heap) == 3
    assert heap.extract_min() == (1, "Documento Judicial Urgente")
    assert heap.extract_min() == (2, "Fatura")
    assert heap.extract_min() == (3, "Contrato Padrão")
    assert len(heap) == 0

def test_extract_from_empty_heap():
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.extract_min()