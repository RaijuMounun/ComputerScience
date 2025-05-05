""" This module implements a binary tree with various methods for insertion, searching, and traversal.
    It includes methods to check if the tree is balanced, full, or perfect, and to count nodes and leaves. """

class TreeNode:
    """ A class representing a node in a binary tree. Each node has a value, a left child, and a right child. """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class MyBinaryTree:
    """ A class representing a binary tree. It supports insertion, searching, and various traversal methods. """
    def __init__(self):
        self.root = None

    def insert(self, value):
        """ Inserts a value into the binary tree. """
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left:
                self._insert_recursive(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert_recursive(node.right, value)
            else:
                node.right = TreeNode(value)

    def contains(self, value):
        """ Checks if the binary tree contains a value and returns true if found, false otherwise. """
        return self._contains_recursive(self.root, value)

    def _contains_recursive(self, node, value):
        if not node:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._contains_recursive(node.left, value)
        return self._contains_recursive(node.right, value)

    def traverse_inorder(self):
        """ Returns a list of values in the binary tree in inorder traversal. """
        return list(self._inorder(self.root))

    def traverse_preorder(self):
        """ Returns a list of values in the binary tree in preorder traversal. """
        return list(self._preorder(self.root))

    def traverse_postorder(self):
        """ Returns a list of values in the binary tree in postorder traversal. """
        return list(self._postorder(self.root))

    def _inorder(self, node):
        if node:
            yield from self._inorder(node.left)
            yield node.value
            yield from self._inorder(node.right)

    def _preorder(self, node):
        if node:
            yield node.value
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)

    def _postorder(self, node):
        if node:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.value

    def height(self):
        """ Returns the height of the binary tree. """
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def is_balanced(self):
        """ Checks if the binary tree is balanced.
            A balanced tree is defined as
            one where the height of the two subtrees of any node never differs by more than one. """
        def check(node):
            if not node:
                return True, -1
            left_bal, left_height = check(node.left)
            right_bal, right_height = check(node.right)
            balanced = left_bal and right_bal and abs(left_height - right_height) <= 1
            return balanced, 1 + max(left_height, right_height)
        return check(self.root)[0]

    def is_full(self):
        """ Checks if the binary tree is full.
            A full binary tree is defined as one where every node other than the leaves has two children. """
        def full(node):
            if not node:
                return True
            if (node.left and not node.right) or (not node.left and node.right):
                return False
            return full(node.left) and full(node.right)
        return full(self.root)

    def is_perfect(self):
        """ Checks if the binary tree is perfect.
            A perfect binary tree is defined as one where all
            internal nodes have two children and all leaves are at the same level. """
        def depth(node):
            d = 0
            while node:
                d += 1
                node = node.left
            return d

        def check(node, level=0, d=0):
            if not node:
                return True
            if not node.left and not node.right:
                return d == level + 1
            if not node.left or not node.right:
                return False
            return check(node.left, level + 1, d) and check(node.right, level + 1, d)

        d = depth(self.root)
        return check(self.root, 0, d)

    def count_nodes(self):
        """ Returns the number of nodes in the binary tree. """
        def count(node):
            if not node:
                return 0
            return 1 + count(node.left) + count(node.right)
        return count(self.root)

    def count_leaves(self):
        """ Returns the number of leaves in the binary tree. """
        def count(node):
            if not node:
                return 0
            if not node.left and not node.right:
                return 1
            return count(node.left) + count(node.right)
        return count(self.root)

    def find_min(self):
        """ Returns the minimum value in the binary tree. """
        current = self.root
        if not current:
            raise ValueError("Tree is empty")
        while current.left:
            current = current.left
        return current.value

    def find_max(self):
        """ Returns the maximum value in the binary tree. """
        current = self.root
        if not current:
            raise ValueError("Tree is empty")
        while current.right:
            current = current.right
        return current.value

    def mirror(self):
        """ Returns a new binary tree that is a mirror image of the original tree. """
        def reverse(node):
            if node:
                node.left, node.right = node.right, node.left
                reverse(node.left)
                reverse(node.right)
        mirror_copy = self.copy_deep()
        reverse(mirror_copy.root)
        return mirror_copy

    def copy_deep(self):
        """ Returns a deep copy of the binary tree. """
        def copy_node(node):
            if not node:
                return None
            new_node = TreeNode(node.value)
            new_node.left = copy_node(node.left)
            new_node.right = copy_node(node.right)
            return new_node
        tree_copy = MyBinaryTree()
        tree_copy.root = copy_node(self.root)
        return tree_copy

    def equals(self, other_tree):
        """ Checks if two binary trees are equal. """
        def compare(n1, n2):
            if not n1 and not n2:
                return True
            if n1 and n2 and n1.value == n2.value:
                return compare(n1.left, n2.left) and compare(n1.right, n2.right)
            return False
        return compare(self.root, other_tree.root)


if __name__ == "__main__":
    my_binary_tree = MyBinaryTree()
    for val in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        my_binary_tree.insert(val)

    print("Inorder:", my_binary_tree.traverse_inorder())
    print("Preorder:", my_binary_tree.traverse_preorder())
    print("Postorder:", my_binary_tree.traverse_postorder())
    print("Height:", my_binary_tree.height())
    print("Balanced?", my_binary_tree.is_balanced())
    print("Full?", my_binary_tree.is_full())
    print("Perfect?", my_binary_tree.is_perfect())
    print("Total Nodes:", my_binary_tree.count_nodes())
    print("Leaf Nodes:", my_binary_tree.count_leaves())
    print("Min:", my_binary_tree.find_min())
    print("Max:", my_binary_tree.find_max())

    mirrored = my_binary_tree.mirror()
    print("Mirrored inorder:", mirrored.traverse_inorder())
