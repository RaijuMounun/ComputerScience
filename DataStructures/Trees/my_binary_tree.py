"""A comprehensive binary tree implementation.

This module provides a robust implementation of binary trees with various features:
- Node insertion and deletion
- Multiple traversal methods (inorder, preorder, postorder, level-order)
- Tree property checks (balanced, full, perfect)
- Node counting and tree statistics
- Tree comparison and copying
- Error handling and validation

Example:
    >>> tree = MyBinaryTree()
    >>> tree.insert(1)
    >>> tree.insert(2)
    >>> tree.insert(3)
    >>> print(tree.traverse_inorder())
    [2, 1, 3]
    >>> print(tree.is_balanced())
    True
"""

from typing import Optional, Any, List, Deque, Tuple
from collections import deque


class TreeError(Exception):
    """Base exception class for tree-related errors."""
    pass


class EmptyTreeError(TreeError):
    """Raised when attempting to perform an operation on an empty tree."""
    pass


class TreeNode:
    """A node in a binary tree.
    
    This class represents a node in a binary tree, containing a value and
    references to its left and right children.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    
    def __init__(self, value: Any) -> None:
        """Initialize a tree node with a value.
        
        Args:
            value: The value to store in the node
        """
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
    
    def __str__(self) -> str:
        """Return a string representation of the node.
        
        Returns:
            A string showing the node's value and its children
        """
        return f"TreeNode(value={self.value}, left={self.left.value if self.left else None}, right={self.right.value if self.right else None})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the node.
        
        Returns:
            A string showing the node's value and its children
        """
        return self.__str__()


class MyBinaryTree:
    """A comprehensive binary tree implementation.
    
    This class provides a complete implementation of a binary tree with various
    features for tree manipulation, traversal, and analysis.
    
    The tree provides:
    - Basic operations (insert, delete, search)
    - Multiple traversal methods
    - Tree property checks
    - Node counting and statistics
    - Tree comparison and copying
    - Error handling and validation
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        self.root: Optional[TreeNode] = None
    
    def insert(self, value: Any) -> None:
        """Insert a value into the tree.
        
        This method inserts a value into the tree at the first available position
        in level-order traversal.
        
        Args:
            value: The value to insert
            
        Raises:
            ValueError: If the value is None
        """
        if value is None:
            raise ValueError("Cannot insert None value into tree")
        
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_level_order(value)
    
    def _insert_level_order(self, value: Any) -> None:
        """Insert a value using level-order traversal.
        
        Args:
            value: The value to insert
        """
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            if not node.left:
                node.left = TreeNode(value)
                return
            
            if not node.right:
                node.right = TreeNode(value)
                return
            
            queue.append(node.left)
            queue.append(node.right)
    
    def delete(self, value: Any) -> None:
        """Delete a value from the tree.
        
        This method deletes a value from the tree and replaces it with the
        last node in level-order traversal to maintain tree structure.
        
        Args:
            value: The value to delete
            
        Raises:
            EmptyTreeError: If the tree is empty
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        # Find the node to delete and the last node
        node_to_delete = None
        last_node = None
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            if node.value == value:
                node_to_delete = node
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            
            last_node = node
        
        if not node_to_delete:
            return
        
        # Replace the value of the node to delete with the last node's value
        node_to_delete.value = last_node.value
        
        # Delete the last node
        self._delete_last()
    
    def _delete_last(self) -> None:
        """Delete the last node in level-order traversal."""
        if not self.root:
            return
        
        if not self.root.left and not self.root.right:
            self.root = None
            return
        
        queue: Deque[TreeNode] = deque([self.root])
        last_parent = None
        last_node = None
        
        while queue:
            node = queue.popleft()
            
            if node.left:
                last_parent = node
                last_node = node.left
                queue.append(node.left)
            
            if node.right:
                last_parent = node
                last_node = node.right
                queue.append(node.right)
        
        if last_node:
            if last_parent.right == last_node:
                last_parent.right = None
            else:
                last_parent.left = None
    
    def contains(self, value: Any) -> bool:
        """Check if a value exists in the tree.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value exists, False otherwise
        """
        if not self.root:
            return False
        
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            if node.value == value:
                return True
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return False
    
    def traverse_inorder(self) -> List[Any]:
        """Return a list of values in inorder traversal.
        
        Returns:
            A list of values in inorder traversal
        """
        def inorder(node: Optional[TreeNode]) -> List[Any]:
            if not node:
                return []
            return inorder(node.left) + [node.value] + inorder(node.right)
        
        return inorder(self.root)
    
    def traverse_preorder(self) -> List[Any]:
        """Return a list of values in preorder traversal.
        
        Returns:
            A list of values in preorder traversal
        """
        def preorder(node: Optional[TreeNode]) -> List[Any]:
            if not node:
                return []
            return [node.value] + preorder(node.left) + preorder(node.right)
        
        return preorder(self.root)
    
    def traverse_postorder(self) -> List[Any]:
        """Return a list of values in postorder traversal.
        
        Returns:
            A list of values in postorder traversal
        """
        def postorder(node: Optional[TreeNode]) -> List[Any]:
            if not node:
                return []
            return postorder(node.left) + postorder(node.right) + [node.value]
        
        return postorder(self.root)
    
    def traverse_level_order(self) -> List[Any]:
        """Return a list of values in level-order traversal.
        
        Returns:
            A list of values in level-order traversal
        """
        if not self.root:
            return []
        
        result: List[Any] = []
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def height(self) -> int:
        """Return the height of the tree.
        
        Returns:
            The height of the tree (number of edges in the longest path)
        """
        def get_height(node: Optional[TreeNode]) -> int:
            if not node:
                return -1
            return 1 + max(get_height(node.left), get_height(node.right))
        
        return get_height(self.root)
    
    def is_balanced(self) -> bool:
        """Check if the tree is balanced.
        
        A tree is balanced if the heights of the left and right subtrees
        of every node differ by at most 1.
        
        Returns:
            True if the tree is balanced, False otherwise
        """
        def check_balance(node: Optional[TreeNode]) -> Tuple[bool, int]:
            if not node:
                return True, -1
            
            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)
            
            is_balanced = (left_balanced and right_balanced and
                         abs(left_height - right_height) <= 1)
            height = 1 + max(left_height, right_height)
            
            return is_balanced, height
        
        return check_balance(self.root)[0]
    
    def is_full(self) -> bool:
        """Check if the tree is a full binary tree.
        
        A full binary tree is a tree in which every node has either 0 or 2 children.
        
        Returns:
            True if the tree is full, False otherwise
        """
        def check_full(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            
            if not node.left and not node.right:
                return True
            
            if node.left and node.right:
                return check_full(node.left) and check_full(node.right)
            
            return False
        
        return check_full(self.root)
    
    def is_perfect(self) -> bool:
        """Check if the tree is a perfect binary tree.
        
        A perfect binary tree is a tree in which all internal nodes have
        exactly two children and all leaf nodes are at the same level.
        
        Returns:
            True if the tree is perfect, False otherwise
        """
        def check_perfect(node: Optional[TreeNode], depth: int, level: int) -> bool:
            if not node:
                return True
            
            if not node.left and not node.right:
                return depth == level
            
            if not node.left or not node.right:
                return False
            
            return (check_perfect(node.left, depth, level + 1) and
                   check_perfect(node.right, depth, level + 1))
        
        depth = self.height()
        return check_perfect(self.root, depth, 0)
    
    def count_nodes(self) -> int:
        """Return the total number of nodes in the tree.
        
        Returns:
            The total number of nodes
        """
        def count(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + count(node.left) + count(node.right)
        
        return count(self.root)
    
    def count_leaves(self) -> int:
        """Return the number of leaf nodes in the tree.
        
        Returns:
            The number of leaf nodes
        """
        def count(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            
            if not node.left and not node.right:
                return 1
            
            return count(node.left) + count(node.right)
        
        return count(self.root)
    
    def find_min(self) -> Optional[Any]:
        """Find the minimum value in the tree.
        
        Returns:
            The minimum value, or None if the tree is empty
        """
        if not self.root:
            return None
        
        min_value = self.root.value
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            min_value = min(min_value, node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return min_value
    
    def find_max(self) -> Optional[Any]:
        """Find the maximum value in the tree.
        
        Returns:
            The maximum value, or None if the tree is empty
        """
        if not self.root:
            return None
        
        max_value = self.root.value
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            max_value = max(max_value, node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return max_value
    
    def mirror(self) -> None:
        """Create a mirror image of the tree.
        
        This method swaps the left and right children of every node in the tree.
        """
        def mirror_node(node: Optional[TreeNode]) -> None:
            if not node:
                return
            
            node.left, node.right = node.right, node.left
            mirror_node(node.left)
            mirror_node(node.right)
        
        mirror_node(self.root)
    
    def copy_deep(self) -> 'MyBinaryTree':
        """Create a deep copy of the tree.
        
        Returns:
            A new tree that is a deep copy of the current tree
        """
        def copy_node(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if not node:
                return None
            
            new_node = TreeNode(node.value)
            new_node.left = copy_node(node.left)
            new_node.right = copy_node(node.right)
            return new_node
        
        new_tree = MyBinaryTree()
        new_tree.root = copy_node(self.root)
        return new_tree
    
    def equals(self, other: 'MyBinaryTree') -> bool:
        """Check if this tree is equal to another tree.
        
        Two trees are equal if they have the same structure and values.
        
        Args:
            other: The tree to compare with
            
        Returns:
            True if the trees are equal, False otherwise
        """
        def check_equals(node1: Optional[TreeNode], node2: Optional[TreeNode]) -> bool:
            if not node1 and not node2:
                return True
            
            if not node1 or not node2:
                return False
            
            return (node1.value == node2.value and
                   check_equals(node1.left, node2.left) and
                   check_equals(node1.right, node2.right))
        
        return check_equals(self.root, other.root)
    
    def __str__(self) -> str:
        """Return a string representation of the tree.
        
        Returns:
            A string showing the tree's structure
        """
        if not self.root:
            return "Empty Tree"
        
        def get_tree_lines(node: Optional[TreeNode], prefix: str = "", is_left: bool = True) -> List[str]:
            if not node:
                return []
            
            lines = []
            lines.append(f"{prefix}{'└── ' if is_left else '┌── '}{node.value}")
            
            if node.left:
                lines.extend(get_tree_lines(node.left, prefix + ("    " if is_left else "│   "), True))
            if node.right:
                lines.extend(get_tree_lines(node.right, prefix + ("    " if is_left else "│   "), False))
            
            return lines
        
        return "\n".join(get_tree_lines(self.root))
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the tree.
        
        Returns:
            A string showing the tree's structure and properties
        """
        return (f"MyBinaryTree(height={self.height()}, "
                f"nodes={self.count_nodes()}, "
                f"leaves={self.count_leaves()}, "
                f"balanced={self.is_balanced()}, "
                f"full={self.is_full()}, "
                f"perfect={self.is_perfect()})")


if __name__ == "__main__":
    # Test the binary tree
    tree = MyBinaryTree()
    
    # Test insertion
    print("Testing insertion:")
    test_values = [1, 2, 3, 4, 5, 6, 7]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Tree structure:")
        print(tree)
        print("Inorder:", tree.traverse_inorder())
        print("Preorder:", tree.traverse_preorder())
        print("Postorder:", tree.traverse_postorder())
        print("Level order:", tree.traverse_level_order())
    
    # Test tree properties
    print("\nTesting tree properties:")
    print("Height:", tree.height())
    print("Is balanced?", tree.is_balanced())
    print("Is full?", tree.is_full())
    print("Is perfect?", tree.is_perfect())
    print("Total nodes:", tree.count_nodes())
    print("Leaf nodes:", tree.count_leaves())
    print("Min value:", tree.find_min())
    print("Max value:", tree.find_max())
    
    # Test deletion
    print("\nTesting deletion:")
    values_to_delete = [2, 3]
    for val in values_to_delete:
        tree.delete(val)
        print(f"\nAfter deleting {val}:")
        print("Tree structure:")
        print(tree)
        print("Inorder:", tree.traverse_inorder())
    
    # Test error handling
    print("\nTesting error handling:")
    empty_tree = MyBinaryTree()
    try:
        empty_tree.delete(5)
    except EmptyTreeError as e:
        print("Caught EmptyTreeError:", e)
    
    try:
        tree.insert(None)
    except ValueError as e:
        print("Caught ValueError:", e)
    
    # Test tree operations
    print("\nTesting tree operations:")
    print("Original tree:")
    print(tree)
    
    # Test mirroring
    tree.mirror()
    print("\nAfter mirroring:")
    print(tree)
    
    # Test copying
    tree_copy = tree.copy_deep()
    print("\nTree copy:")
    print(tree_copy)
    print("Trees are equal?", tree.equals(tree_copy))
    
    # Test with a large number of values
    print("\nTesting with a large number of values:")
    large_tree = MyBinaryTree()
    for i in range(15):  # Using a smaller number to keep the tree manageable
        large_tree.insert(i)
    
    print("Tree structure:")
    print(large_tree)
    print("Height:", large_tree.height())
    print("Is balanced?", large_tree.is_balanced())
    print("Is full?", large_tree.is_full())
    print("Is perfect?", large_tree.is_perfect())
    print("Total nodes:", large_tree.count_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
