""" Full Binary Tree implementation built on top of BinaryTreeNode """

class FullBinaryTree:
    """Represents a Full Binary Tree where every node has 0 or 2 children."""

    class Node:
        """A node in the full binary tree."""
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self, root_value):
        """Initializes the tree with a root node."""
        self.root = self.Node(root_value)

    def is_full(self, node=None):
        """
        Checks if the tree is a full binary tree.
        Every node must have 0 or 2 children.
        """
        if node is None:
            node = self.root
        if node is None:
            return True
        if (node.left is None) and (node.right is None):
            return True
        if (node.left is not None) and (node.right is not None):
            return self.is_full(node.left) and self.is_full(node.right)
        return False


# Example usage
fbt = FullBinaryTree(1)
fbt.root.left = FullBinaryTree.Node(2)
fbt.root.right = FullBinaryTree.Node(3)
fbt.root.left.left = FullBinaryTree.Node(4)
fbt.root.left.right = FullBinaryTree.Node(5)

print("Is full binary tree?", fbt.is_full())  # Output: True
