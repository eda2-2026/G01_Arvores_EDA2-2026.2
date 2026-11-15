import pytest
from src.structures.red_black_tree import RedBlackTree

def test_rb_tree_root_is_always_black():
    tree = RedBlackTree()
    tree.insert(10, "Worker_A")
    assert tree.root.color == "BLACK"
    
    tree.insert(20, "Worker_B")
    tree.insert(30, "Worker_C")
    assert tree.root.color == "BLACK"

def test_rb_tree_no_adjacent_red_nodes():
    tree = RedBlackTree()
    keys = [10, 20, 30, 15, 25, 5]
    for key in keys:
        tree.insert(key, f"Worker_{key}")
    
    # Função auxiliar para checar a regra dos nós vermelhos
    def check_red_rule(node):
        if node == tree.TNULL:
            return True
        if node.color == "RED":
            assert node.left.color == "BLACK", f"Nó {node.key} e filho esquerdo são vermelhos!"
            assert node.right.color == "BLACK", f"Nó {node.key} e filho direito são vermelhos!"
        return check_red_rule(node.left) and check_red_rule(node.right)
    
    check_red_rule(tree.root)

def test_rb_tree_search():
    tree = RedBlackTree()
    tree.insert(10, "Worker_10")
    tree.insert(20, "Worker_20")
    
    node = tree.search(20)
    assert node.key == 20
    assert node.value == "Worker_20"
    
    node_not_found = tree.search(99)
    assert node_not_found == tree.TNULL