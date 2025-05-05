"""
This module defines a base binary tree structure with common tree operations.
"""

class TreeNode:
    """
    Represents a node in a binary tree.

    Attributes:
        value (any): The data value of the node.
        left (TreeNode): The left child node.
        right (TreeNode): The right child node.
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BaseBinaryTree:
    """
    A basic binary tree with traversal and utility methods.
    """

    def __init__(self):
        """
        Initializes an empty binary tree.
        """
        self.root = None

    def insert(self, value):
        """
        Inserts a value into the binary tree in a basic left-to-right fashion.

        Args:
            value (any): Value to insert.
        """
        new_node = TreeNode(value)
        if not self.root:
            self.root = new_node
            return
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if not current.left:
                current.left = new_node
                return
            else:
                queue.append(current.left)
            if not current.right:
                current.right = new_node
                return
            else:
                queue.append(current.right)

    def inorder(self, node=None):
        """
        Returns the inorder traversal of the tree.

        Args:
            node (TreeNode): Node to start traversal from. Defaults to root.

        Returns:
            list: Inorder traversal values.
        """
        if node is None:
            node = self.root
        if node is None:
            return []
        return self.inorder(node.left) + [node.value] + self.inorder(node.right)

    def preorder(self, node=None):
        """
        Returns the preorder traversal of the tree.

        Args:
            node (TreeNode): Node to start traversal from. Defaults to root.

        Returns:
            list: Preorder traversal values.
        """
        if node is None:
            node = self.root
        if node is None:
            return []
        return [node.value] + self.preorder(node.left) + self.preorder(node.right)

    def postorder(self, node=None):
        """
        Returns the postorder traversal of the tree.

        Args:
            node (TreeNode): Node to start traversal from. Defaults to root.

        Returns:
            list: Postorder traversal values.
        """
        if node is None:
            node = self.root
        if node is None:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.value]

    def level_order(self):
        """
        Returns the level-order (breadth-first) traversal of the tree.

        Returns:
            list: Level-order traversal values.
        """
        result = []
        if not self.root:
            return result
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            result.append(current.value)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result
