""" This module implements a Complete Binary Tree data structure.
    It provides methods for inserting nodes and checking if the tree is complete."""

from collections import deque

class CompleteBinaryTree:
    """Represents a Complete Binary Tree where all levels are fully filled except possibly the last one."""

    class Node:
        """A node in the complete binary tree."""
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty complete binary tree."""
        self.root = None

    def insert(self, value):
        """
        Inserts a node into the tree while preserving the complete binary tree property.
        Uses level-order insertion.
        """
        new_node = self.Node(value)
        if not self.root:
            self.root = new_node
            return

        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            if not current.left:
                current.left = new_node
                return
            elif not current.right:
                current.right = new_node
                return
            else:
                queue.append(current.left)
                queue.append(current.right)

    def is_complete(self):
        """
        Checks whether the tree is complete using level order traversal.
        After the first None child, all following nodes must be leaves.
        """
        if not self.root:
            return True

        queue = deque([self.root])
        found_null = False

        while queue:
            node = queue.popleft()
            if node.left:
                if found_null:
                    return False
                queue.append(node.left)
            else:
                found_null = True

            if node.right:
                if found_null:
                    return False
                queue.append(node.right)
            else:
                found_null = True

        return True


# Example usage
cbt = CompleteBinaryTree()
for i in range(1, 8):
    cbt.insert(i)

print("Is complete binary tree?", cbt.is_complete())  # Output: True
