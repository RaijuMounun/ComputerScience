"""A complete binary tree implementation.

This module implements a complete binary tree that maintains the following properties:
- All levels are completely filled except possibly the last level
- The last level is filled from left to right
- Efficient array-based representation
- O(log n) time complexity for most operations

Example:
    >>> tree = CompleteBinaryTree()
    >>> tree.insert(1)
    >>> tree.insert(2)
    >>> tree.insert(3)
    >>> print(tree.traverse_level_order())
    [1, 2, 3]
    >>> print(tree.is_complete())
    True
"""

from typing import Optional, Any, List, Deque
from collections import deque
from my_binary_tree import MyBinaryTree, TreeNode, TreeError, EmptyTreeError


class CompleteBinaryTree(MyBinaryTree):
    """A complete binary tree implementation.
    
    This class extends MyBinaryTree to provide a complete binary tree implementation
    that maintains the complete binary tree property: all levels are completely filled
    except possibly the last level, which is filled from left to right.
    
    The tree provides:
    - O(log n) time complexity for most operations
    - Efficient array-based representation
    - Level-order traversal for easy visualization
    - Automatic maintenance of complete property
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty complete binary tree."""
        super().__init__()
    
    def insert(self, value: Any) -> None:
        """Insert a value into the tree while maintaining complete property.
        
        This method overrides the base class's insert method to ensure
        the complete binary tree property is maintained.
        
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
        """Insert a value using level-order traversal to maintain complete property.
        
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
    
    def delete_last(self) -> Any:
        """Delete the last node in level-order traversal.
        
        This method is used to maintain the complete property when deleting nodes.
        
        Returns:
            The value of the deleted node
            
        Raises:
            EmptyTreeError: If the tree is empty
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        if not self.root.left and not self.root.right:
            value = self.root.value
            self.root = None
            return value
        
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
            value = last_node.value
            if last_parent.right == last_node:
                last_parent.right = None
            else:
                last_parent.left = None
            return value
        
        return None
    
    def delete(self, value: Any) -> None:
        """Delete a value from the tree while maintaining complete property.
        
        This method overrides the base class's delete method to ensure
        the complete binary tree property is maintained after deletion.
        
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
        self.delete_last()
    
    def is_complete(self) -> bool:
        """Check if the tree is a complete binary tree.
        
        Returns:
            True if the tree is complete, False otherwise
        """
        if not self.root:
            return True
        
        queue: Deque[TreeNode] = deque([self.root])
        flag = False  # Flag to indicate if we've seen a non-full node
        
        while queue:
            node = queue.popleft()
            
            if node.left:
                if flag:  # If we've seen a non-full node before
                    return False
                queue.append(node.left)
            else:
                flag = True
            
            if node.right:
                if flag:  # If we've seen a non-full node before
                    return False
                queue.append(node.right)
            else:
                flag = True
        
        return True
    
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


if __name__ == "__main__":
    # Test the complete binary tree
    tree = CompleteBinaryTree()
    
    # Test insertion
    print("Testing insertion:")
    test_values = [1, 2, 3, 4, 5, 6]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Level order:", tree.traverse_level_order())
        print("Is complete?", tree.is_complete())
    
    # Test deletion
    print("\nTesting deletion:")
    values_to_delete = [2, 3]
    for val in values_to_delete:
        tree.delete(val)
        print(f"\nAfter deleting {val}:")
        print("Level order:", tree.traverse_level_order())
        print("Is complete?", tree.is_complete())
    
    # Test error handling
    print("\nTesting error handling:")
    empty_tree = CompleteBinaryTree()
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
    large_tree = CompleteBinaryTree()
    for i in range(100):
        large_tree.insert(i)
    
    print("Height:", large_tree.height())
    print("Is complete?", large_tree.is_complete())
    print("Total nodes:", large_tree.count_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
    
    # Test level order traversal
    print("\nTesting level order traversal:")
    print("Level order:", large_tree.traverse_level_order())
