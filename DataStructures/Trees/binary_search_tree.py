"""A binary search tree implementation with search optimization.

This module implements a binary search tree (BST) that maintains the following properties:
- For any node, all values in its left subtree are less than the node's value
- For any node, all values in its right subtree are greater than the node's value
- No duplicate values are allowed
- O(log n) average case time complexity for search operations

Example:
    >>> tree = BinarySearchTree()
    >>> tree.insert(5)
    >>> tree.insert(3)
    >>> tree.insert(7)
    >>> print(tree.traverse_inorder())
    [3, 5, 7]
    >>> print(tree.search(3))
    True
    >>> print(tree.search(4))
    False
"""

from typing import Optional, Any, List
from my_binary_tree import MyBinaryTree, TreeNode, TreeError, EmptyTreeError


class DuplicateValueError(TreeError):
    """Raised when attempting to insert a duplicate value into the tree."""
    pass


class BinarySearchTree(MyBinaryTree):
    """A binary search tree implementation with optimized search operations.
    
    This class extends MyBinaryTree to provide a binary search tree implementation
    that maintains the BST property: for any node, all values in its left subtree
    are less than the node's value, and all values in its right subtree are
    greater than the node's value.
    
    The tree provides:
    - O(log n) average case time complexity for search operations
    - Efficient insertion and deletion while maintaining BST properties
    - No duplicate values allowed
    - Inorder traversal yields sorted values
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty binary search tree."""
        super().__init__()
    
    def insert(self, value: Any) -> None:
        """Insert a value into the binary search tree.
        
        This method overrides the base class's insert method to ensure
        the BST property is maintained and no duplicates are allowed.
        
        Args:
            value: The value to insert
            
        Raises:
            ValueError: If the value is None
            DuplicateValueError: If the value already exists in the tree
        """
        if value is None:
            raise ValueError("Cannot insert None value into tree")
        
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """Recursively insert a value while maintaining BST properties.
        
        Args:
            node: The current node being processed
            value: The value to insert
            
        Raises:
            DuplicateValueError: If the value already exists in the tree
        """
        if value == node.value:
            raise DuplicateValueError(f"Value {value} already exists in the tree")
        
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
    
    def search(self, value: Any) -> bool:
        """Search for a value in the tree.
        
        This method provides an optimized search operation that takes
        advantage of the BST property to achieve O(log n) average case
        time complexity.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value is found, False otherwise
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> bool:
        """Recursively search for a value in the tree.
        
        Args:
            node: The current node being processed
            value: The value to search for
            
        Returns:
            True if the value is found, False otherwise
        """
        if not node:
            return False
        
        if value == node.value:
            return True
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def delete(self, value: Any) -> None:
        """Delete a value from the tree while maintaining BST properties.
        
        This method overrides the base class's delete method to ensure
        the BST property is maintained after deletion.
        
        Args:
            value: The value to delete
            
        Raises:
            EmptyTreeError: If the tree is empty
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """Recursively delete a value while maintaining BST properties.
        
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
    
    def get_sorted_values(self) -> List[Any]:
        """Return a list of all values in the tree in sorted order.
        
        This method takes advantage of the BST property that inorder
        traversal yields sorted values.
        
        Returns:
            A list of all values in the tree, sorted in ascending order
        """
        return self.traverse_inorder()


if __name__ == "__main__":
    # Test the binary search tree
    tree = BinarySearchTree()
    
    # Test insertion
    print("Testing insertion:")
    test_values = [10, 20, 30, 40, 50, 25]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Height:", tree.height())
        print("Is balanced?", tree.is_balanced())
    
    # Test search
    print("\nTesting search:")
    search_values = [20, 25, 35]
    for val in search_values:
        print(f"Searching for {val}:", tree.search(val))
    
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
    empty_tree = BinarySearchTree()
    try:
        empty_tree.delete(5)
    except EmptyTreeError as e:
        print("Caught EmptyTreeError:", e)
    
    try:
        tree.insert(None)
    except ValueError as e:
        print("Caught ValueError:", e)
    
    try:
        tree.insert(10)  # Try to insert a duplicate value
    except DuplicateValueError as e:
        print("Caught DuplicateValueError:", e)
    
    # Test with a large number of values
    print("\nTesting with a large number of values:")
    large_tree = BinarySearchTree()
    for i in range(100):
        large_tree.insert(i)
    
    print("Height:", large_tree.height())
    print("Is balanced?", large_tree.is_balanced())
    print("Total nodes:", large_tree.count_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
    
    # Test sorted values
    print("\nTesting sorted values:")
    print("Sorted values:", large_tree.get_sorted_values())
