'''
Binary Search Tree (BST) implementation with common operations like insert, delete,
search, and traversal. Extends a TreeNode structure.
'''

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


class BinarySearchTree:
    """
    Binary Search Tree class that supports insert, delete, search, traversals,
    find_min, find_max, and other utility functions.
    """

    def __init__(self):
        """Initialize an empty BST."""
        self.root = None

    def insert(self, value):
        """Insert value into the BST."""
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if not node:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value):
        """Search for a value in the BST."""
        return self._search(self.root, value)

    def _search(self, node, value):
        if not node or node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def delete(self, value):
        """Delete a value from the BST."""
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            min_larger_node = self._find_min(node.right)
            node.value = min_larger_node.value
            node.right = self._delete(node.right, min_larger_node.value)
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _find_max(self, node):
        while node.right:
            node = node.right
        return node

    def inorder(self):
        """Return inorder traversal of the BST."""
        return self._inorder(self.root)

    def _inorder(self, node):
        if not node:
            return []
        return self._inorder(node.left) + [node.value] + self._inorder(node.right)

    def preorder(self):
        """Return preorder traversal of the BST."""
        return self._preorder(self.root)

    def _preorder(self, node):
        if not node:
            return []
        return [node.value] + self._preorder(node.left) + self._preorder(node.right)

    def postorder(self):
        """Return postorder traversal of the BST."""
        return self._postorder(self.root)

    def _postorder(self, node):
        if not node:
            return []
        return self._postorder(node.left) + self._postorder(node.right) + [node.value]

    def find_min(self):
        """Return the minimum value in the BST."""
        if not self.root:
            raise ValueError("Tree is empty")
        return self._find_min(self.root).value

    def find_max(self):
        """Return the maximum value in the BST."""
        if not self.root:
            raise ValueError("Tree is empty")
        return self._find_max(self.root).value


# Example usage
if __name__ == "__main__":
    my_binary_search_tree = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        my_binary_search_tree.insert(val)

    print("Inorder:", my_binary_search_tree.inorder())
    print("Preorder:", my_binary_search_tree.preorder())
    print("Postorder:", my_binary_search_tree.postorder())
    print("Min:", my_binary_search_tree.find_min())
    print("Max:", my_binary_search_tree.find_max())

    my_binary_search_tree.delete(70)
    print("Inorder after deleting 70:", my_binary_search_tree.inorder())
