"""An AVL tree implementation that maintains balance after each operation.

This module implements a self-balancing binary search tree (AVL tree) with the following features:
- Automatic balancing after insertions and deletions
- O(log n) time complexity for all operations
- Height-balanced property maintenance
- All features of the base binary tree

Example:
    >>> tree = BalancedTree()
    >>> tree.insert(5)
    >>> tree.insert(3)
    >>> tree.insert(7)
    >>> print(tree.traverse_inorder())
    [3, 5, 7]
    >>> print(tree.is_balanced())
    True
"""

from typing import Optional, Any, Tuple
from my_binary_tree import MyBinaryTree, TreeNode, TreeError, EmptyTreeError


class BalancedTree(MyBinaryTree):
    """A self-balancing binary search tree (AVL tree) implementation.
    
    This class extends MyBinaryTree to provide automatic balancing after
    insertions and deletions, ensuring O(log n) time complexity for all operations.
    
    The tree maintains the following properties:
    - For any node, the heights of its left and right subtrees differ by at most 1
    - All operations (insert, delete, search) maintain this balance property
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty balanced tree."""
        super().__init__()
    
    def _get_balance_factor(self, node: Optional[TreeNode]) -> int:
        """Calculate the balance factor of a node.
        
        The balance factor is defined as: height(left subtree) - height(right subtree)
        
        Args:
            node: The node to calculate balance factor for
            
        Returns:
            The balance factor of the node (0 for None)
        """
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _rotate_right(self, y: TreeNode) -> TreeNode:
        """Perform a right rotation around a node.
        
        This rotation is used to balance the tree when the left subtree
        is too tall (balance factor > 1).
        
        Args:
            y: The node to rotate around
            
        Returns:
            The new root of the rotated subtree
        """
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        return x
    
    def _rotate_left(self, x: TreeNode) -> TreeNode:
        """Perform a left rotation around a node.
        
        This rotation is used to balance the tree when the right subtree
        is too tall (balance factor < -1).
        
        Args:
            x: The node to rotate around
            
        Returns:
            The new root of the rotated subtree
        """
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        return y
    
    def insert(self, value: Any) -> None:
        """Insert a value into the balanced tree and maintain balance.
        
        This method overrides the base class's insert method to ensure
        the tree remains balanced after insertion.
        
        Args:
            value: The value to insert
            
        Raises:
            ValueError: If the value is None
        """
        if value is None:
            raise ValueError("Cannot insert None value into tree")
        
        self.root = self._insert_recursive_balanced(self.root, value)
    
    def _insert_recursive_balanced(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        """Recursively insert a value and maintain balance.
        
        Args:
            node: The current node being processed
            value: The value to insert
            
        Returns:
            The root of the balanced subtree
        """
        # Standard BST insertion
        if not node:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive_balanced(node.left, value)
        else:
            node.right = self._insert_recursive_balanced(node.right, value)
        
        # Get balance factor
        balance = self._get_balance_factor(node)
        
        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def delete(self, value: Any) -> None:
        """Delete a value from the balanced tree and maintain balance.
        
        This method overrides the base class's delete method to ensure
        the tree remains balanced after deletion.
        
        Args:
            value: The value to delete
            
        Raises:
            EmptyTreeError: If the tree is empty
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        self.root = self._delete_recursive_balanced(self.root, value)
    
    def _delete_recursive_balanced(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """Recursively delete a value and maintain balance.
        
        Args:
            node: The current node being processed
            value: The value to delete
            
        Returns:
            The root of the balanced subtree
        """
        if not node:
            return node
        
        # Standard BST deletion
        if value < node.value:
            node.left = self._delete_recursive_balanced(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive_balanced(node.right, value)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children: Get the inorder successor (smallest in right subtree)
            temp = node.right
            while temp.left:
                temp = temp.left
            
            # Copy the inorder successor's content to this node
            node.value = temp.value
            
            # Delete the inorder successor
            node.right = self._delete_recursive_balanced(node.right, temp.value)
        
        # If the tree had only one node then return
        if not node:
            return node
        
        # Get balance factor
        balance = self._get_balance_factor(node)
        
        # Left Left Case
        if balance > 1 and self._get_balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        # Left Right Case
        if balance > 1 and self._get_balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and self._get_balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        # Right Left Case
        if balance < -1 and self._get_balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node


if __name__ == "__main__":
    # Test the balanced tree
    tree = BalancedTree()
    
    # Test insertion and balancing
    print("Testing insertion and balancing:")
    test_values = [10, 20, 30, 40, 50, 25]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Height:", tree.height())
        print("Is balanced?", tree.is_balanced())
        print("Balance factor of root:", tree._get_balance_factor(tree.root))
    
    # Test deletion and balancing
    print("\nTesting deletion and balancing:")
    values_to_delete = [20, 30]
    for val in values_to_delete:
        tree.delete(val)
        print(f"\nAfter deleting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Height:", tree.height())
        print("Is balanced?", tree.is_balanced())
        print("Balance factor of root:", tree._get_balance_factor(tree.root))
    
    # Test error handling
    print("\nTesting error handling:")
    empty_tree = BalancedTree()
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
    large_tree = BalancedTree()
    for i in range(100):
        large_tree.insert(i)
    
    print("Height:", large_tree.height())
    print("Is balanced?", large_tree.is_balanced())
    print("Total nodes:", large_tree.count_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
