"""
Implementação de uma Árvore AVL Estritamente Balanceada.
Utilizada para buscas em tempo O(log n) de documentos processados.
"""
from typing import Any, Optional

class AVLNode:
    def __init__(self, key: int, value: Any):
        self.key: int = key
        self.value: Any = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1

class AVLTree:
    def get_height(self, node: Optional[AVLNode]) -> int:
        """Retorna a altura do nó."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Optional[AVLNode]) -> int:
        """Calcula o fator de balanceamento do nó."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: AVLNode) -> AVLNode:
        """Realiza uma rotação simples à direita."""
        x = y.left
        T2 = x.right

        # Rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        """Realiza uma rotação simples à esquerda."""
        y = x.right
        T2 = y.left

        # Rotação
        y.left = x
        x.right = T2

        # Atualiza as alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root: Optional[AVLNode], key: int, value: Any) -> AVLNode:
        """
        Insere um novo nó e rebalanceia a árvore subindo pela recursão.
        """

        if not root:
            return AVLNode(key, value)
        
        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            root.value = value
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        #  Verifica os 4 casos de desbalanceamento

        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        """
        Busca O(log n) clássica de uma BST.
        """
        if root is None or root.key == key:
            return root
        
        if root.key < key:
            return self.search(root.right, key)
        
        return self.search(root.left, key)