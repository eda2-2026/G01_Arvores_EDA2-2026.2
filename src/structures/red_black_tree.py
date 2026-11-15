"""
Implementação da Árvore Red-Black.
Utilizada para gerenciar o pool de Workers devido à sua alta eficiência em inserções e remoções.
"""
from typing import Any

class Node:
    def __init__(self, key: int, value: Any):
        self.key: int = key
        self.value: Any = value
        self.parent: 'Node' = None
        self.left: 'Node' = None
        self.right: 'Node' = None
        self.color: str = "RED"  # Novos nós sempre nascem vermelhos

class RedBlackTree:
    def __init__(self):
        # Nó sentinela (TNULL) representa as folhas nulas, sempre pretas.
        self.TNULL = Node(0, None)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def search(self, key: int) -> Node:
        """Busca um Worker pelo ID (key)."""
        return self._search_tree(self.root, key)

    def _search_tree(self, node: Node, key: int) -> Node:
        if node == self.TNULL or key == node.key:
            return node
        if key < node.key:
            return self._search_tree(node.left, key)
        return self._search_tree(node.right, key)

    def _left_rotate(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node) -> None:
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key: int, value: Any) -> None:
        """Insere um novo Worker ativo e corrige as violações de cor/balanceamento."""
        new_node = Node(key, value)
        new_node.parent = None
        new_node.key = key
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        new_node.color = "RED"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right

        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node

        if new_node.parent is None:
            new_node.color = "BLACK"
            return

        if new_node.parent.parent is None:
            return

        self._fix_insert(new_node)

    def _fix_insert(self, k: Node) -> None:
        """Resolve conflitos de vermelho-vermelho após a inserção."""
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # Tio
                if u.color == "RED":
                    # Caso 1: Tio é vermelho -> Recolore pai, tio e avô
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Caso 2: Tio é preto e nó é filho esquerdo -> Rotação dupla (Dir-Esq)
                        k = k.parent
                        self._right_rotate(k)
                    # Caso 3: Tio é preto e nó é filho direito -> Rotação simples (Esq)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  
                if u.color == "RED":
                    # Caso 1 simétrico
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Caso 2 simétrico -> Rotação dupla (Esq-Dir)
                        k = k.parent
                        self._left_rotate(k)
                    # Caso 3 simétrico -> Rotação simples (Dir)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self._right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"