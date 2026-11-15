import pytest
from src.structures.avl_tree import AVLTree

def test_avl_left_left_rotation():
    tree = AVLTree()
    root = None
    for key in [30, 20, 10]:
        root = tree.insert(root, key, f"Doc_{key}")
    
    assert root.key == 20
    assert root.left.key == 10
    assert root.right.key == 30

def test_avl_right_right_rotation():
    tree = AVLTree()
    root = None
    for key in [10, 20, 30]:
        root = tree.insert(root, key, f"Doc_{key}")
    
    assert root.key == 20
    assert root.left.key == 10
    assert root.right.key == 30

def test_avl_left_right_rotation():
    tree = AVLTree()
    root = None
    for key in [30, 10, 20]:
        root = tree.insert(root, key, f"Doc_{key}")
    
    assert root.key == 20
    assert root.left.key == 10
    assert root.right.key == 30

def test_avl_search():
    tree = AVLTree()
    root = None
    keys = [15, 10, 20, 8, 12, 18, 25]
    for key in keys:
        root = tree.insert(root, key, f"Processed_{key}")
    
    node = tree.search(root, 12)
    assert node is not None
    assert node.value == "Processed_12"

    node = tree.search(root, 99)
    assert node is None