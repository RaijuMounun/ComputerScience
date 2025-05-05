"""A basic unbalanced binary tree implementation.

This module implements a simple binary tree that does not maintain balance after operations.
It inherits from MyBinaryTree and provides a straightforward implementation without
balancing mechanisms, which can lead to O(n) worst-case time complexity.

Example:
    >>> tree = UnbalancedTree()
    >>> tree.insert(5)
    >>> tree.insert(3)
    >>> tree.insert(7)
    >>> print(tree.traverse_inorder())
    [3, 5, 7]
    >>> print(tree.is_balanced())
    False  # May be unbalanced depending on insertion order
"""

from typing import Optional, Any
from my_binary_tree import MyBinaryTree, TreeNode, EmptyTreeError


class UnbalancedTree(MyBinaryTree):
    """A basic binary tree implementation without balancing mechanisms.
    
    This class extends MyBinaryTree to provide a simple binary tree implementation
    that does not maintain balance after operations. This can lead to:
    - O(n) worst-case time complexity for operations
    - Potentially skewed tree structure
    - No automatic rebalancing
    
    The tree is useful for:
    - Simple binary tree operations
    - Cases where balance is not critical
    - Educational purposes to understand basic tree operations
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty unbalanced tree."""
        super().__init__()
    
    def insert(self, value: Any) -> None:
        """Insert a value into the tree without balancing.
        
        This method overrides the base class's insert method to provide
        a simple insertion without any balancing mechanisms.
        
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
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """Recursively insert a value without balancing.
        
        Args:
            node: The current node being processed
            value: The value to insert
        """
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
    
    def delete(self, value: Any) -> None:
        """Delete a value from the tree without balancing.
        
        This method overrides the base class's delete method to provide
        a simple deletion without any balancing mechanisms.
        
        Args:
            value: The value to delete
            
        Raises:
            EmptyTreeError: If the tree is empty
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """Recursively delete a value without balancing.
        
        Args:
            node: The current node being processed
            value: The value to delete
            
        Returns:
            The root of the subtree after deletion
        """
        if not node:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children: Get the inorder successor
            temp = node.right
            while temp.left:
                temp = temp.left
            
            # Copy the inorder successor's content to this node
            node.value = temp.value
            
            # Delete the inorder successor
            node.right = self._delete_recursive(node.right, temp.value)
        
        return node


if __name__ == "__main__":
    # Test the unbalanced tree
    tree = UnbalancedTree()
    
    # Test insertion
    print("Testing insertion:")
    test_values = [10, 20, 30, 40, 50, 25]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Height:", tree.height())
        print("Is balanced?", tree.is_balanced())
    
    # Test deletion
    print("\nTesting deletion:")
    values_to_delete = [20, 30]
    for val in values_to_delete:
        tree.delete(val)
        print(f"\nAfter deleting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Height:", tree.height())
        print("Is balanced?", tree.is_balanced())
    
    # Test error handling
    print("\nTesting error handling:")
    empty_tree = UnbalancedTree()
    try:
        empty_tree.delete(5)
    except EmptyTreeError as e:
        print("Caught EmptyTreeError:", e)
    
    try:
        tree.insert(None)
    except ValueError as e:
        print("Caught ValueError:", e)
    
    # Test with a large number of values
    print("\nTesting with a large number of values:")
    large_tree = UnbalancedTree()
    for i in range(100):
        large_tree.insert(i)
    
    print("Height:", large_tree.height())
    print("Is balanced?", large_tree.is_balanced())
    print("Total nodes:", large_tree.count_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
    
    # Demonstrate potential imbalance
    print("\nDemonstrating potential imbalance:")
    skewed_tree = UnbalancedTree()
    for i in range(10):
        skewed_tree.insert(i)  # This will create a right-skewed tree
    
    print("Height:", skewed_tree.height())
    print("Is balanced?", skewed_tree.is_balanced())
    print("Total nodes:", skewed_tree.count_nodes())
    print("Leaf nodes:", skewed_tree.count_leaves())
