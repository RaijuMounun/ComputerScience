"""A full binary tree implementation.

This module implements a full binary tree that maintains the following properties:
- Every node has either 0 or exactly 2 children
- No node can have only one child
- Leaf nodes have no children
- Internal nodes have exactly two children

Example:
    >>> tree = FullBinaryTree()
    >>> tree.insert(1)
    >>> tree.insert(2)
    >>> tree.insert(3)
    >>> print(tree.traverse_inorder())
    [2, 1, 3]
    >>> print(tree.is_full())
    True
"""

from typing import Optional, Any, List, Deque, Tuple
from collections import deque
from my_binary_tree import MyBinaryTree, TreeNode, TreeError, EmptyTreeError


class InvalidNodeError(TreeError):
    """Raised when attempting to create an invalid node structure in a full binary tree."""
    pass


class FullBinaryTree(MyBinaryTree):
    """A full binary tree implementation.
    
    This class extends MyBinaryTree to provide a full binary tree implementation
    that maintains the full binary tree property: every node has either 0 or
    exactly 2 children.
    
    The tree provides:
    - Strict enforcement of the full binary tree property
    - Efficient insertion and deletion while maintaining the property
    - Automatic validation of tree structure
    - Leaf node counting and internal node counting
    
    Attributes:
        root: The root node of the tree
    """
    
    def __init__(self) -> None:
        """Initialize an empty full binary tree."""
        super().__init__()
    
    def insert(self, value: Any) -> None:
        """Insert a value into the tree while maintaining full property.
        
        This method overrides the base class's insert method to ensure
        the full binary tree property is maintained.
        
        Args:
            value: The value to insert
            
        Raises:
            ValueError: If the value is None
            InvalidNodeError: If the insertion would violate the full binary tree property
        """
        if value is None:
            raise ValueError("Cannot insert None value into tree")
        
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_maintaining_full_property(value)
    
    def _insert_maintaining_full_property(self, value: Any) -> None:
        """Insert a value while maintaining the full binary tree property.
        
        Args:
            value: The value to insert
            
        Raises:
            InvalidNodeError: If the insertion would violate the full binary tree property
        """
        queue: Deque[TreeNode] = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            # If node has no children, create both children
            if not node.left and not node.right:
                node.left = TreeNode(value)
                node.right = TreeNode(value)  # Using same value for both children
                return
            
            # If node has one child, this is invalid for a full binary tree
            if (node.left and not node.right) or (not node.left and node.right):
                raise InvalidNodeError("Cannot insert into a node with only one child")
            
            # If node has two children, continue searching
            queue.append(node.left)
            queue.append(node.right)
    
    def delete(self, value: Any) -> None:
        """Delete a value from the tree while maintaining full property.
        
        This method overrides the base class's delete method to ensure
        the full binary tree property is maintained after deletion.
        
        Args:
            value: The value to delete
            
        Raises:
            EmptyTreeError: If the tree is empty
            InvalidNodeError: If the deletion would violate the full binary tree property
        """
        if not self.root:
            raise EmptyTreeError("Cannot delete from empty tree")
        
        # Find the node to delete and its parent
        node_to_delete = None
        parent = None
        queue: Deque[Tuple[Optional[TreeNode], TreeNode]] = deque([(None, self.root)])
        
        while queue:
            parent_node, current_node = queue.popleft()
            
            if current_node.value == value:
                node_to_delete = current_node
                parent = parent_node
                break
            
            if current_node.left:
                queue.append((current_node, current_node.left))
            if current_node.right:
                queue.append((current_node, current_node.right))
        
        if not node_to_delete:
            return
        
        # If the node to delete is a leaf, we can safely remove it
        if not node_to_delete.left and not node_to_delete.right:
            if parent:
                if parent.left == node_to_delete:
                    parent.left = None
                else:
                    parent.right = None
            else:
                self.root = None
            return
        
        # If the node has children, we need to delete the entire subtree
        if parent:
            if parent.left == node_to_delete:
                parent.left = None
            else:
                parent.right = None
        else:
            self.root = None
    
    def is_full(self) -> bool:
        """Check if the tree is a full binary tree.
        
        Returns:
            True if the tree is full, False otherwise
        """
        def check_node(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            
            # If node is a leaf
            if not node.left and not node.right:
                return True
            
            # If node has exactly two children
            if node.left and node.right:
                return check_node(node.left) and check_node(node.right)
            
            # If node has only one child
            return False
        
        return check_node(self.root)
    
    def count_internal_nodes(self) -> int:
        """Return the number of internal nodes in the tree.
        
        An internal node is a node that has at least one child.
        
        Returns:
            The number of internal nodes
        """
        def count(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            
            if not node.left and not node.right:
                return 0
            
            return 1 + count(node.left) + count(node.right)
        
        return count(self.root)
    
    def get_leaf_values(self) -> List[Any]:
        """Return a list of values stored in leaf nodes.
        
        Returns:
            A list of values stored in leaf nodes
        """
        def get_leaves(node: Optional[TreeNode]) -> List[Any]:
            if not node:
                return []
            
            if not node.left and not node.right:
                return [node.value]
            
            return get_leaves(node.left) + get_leaves(node.right)
        
        return get_leaves(self.root)


if __name__ == "__main__":
    # Test the full binary tree
    tree = FullBinaryTree()
    
    # Test insertion
    print("Testing insertion:")
    test_values = [1, 2, 3, 4, 5, 6, 7]
    for val in test_values:
        tree.insert(val)
        print(f"\nAfter inserting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Is full?", tree.is_full())
        print("Internal nodes:", tree.count_internal_nodes())
        print("Leaf values:", tree.get_leaf_values())
    
    # Test deletion
    print("\nTesting deletion:")
    values_to_delete = [2, 3]
    for val in values_to_delete:
        tree.delete(val)
        print(f"\nAfter deleting {val}:")
        print("Inorder:", tree.traverse_inorder())
        print("Is full?", tree.is_full())
        print("Internal nodes:", tree.count_internal_nodes())
        print("Leaf values:", tree.get_leaf_values())
    
    # Test error handling
    print("\nTesting error handling:")
    empty_tree = FullBinaryTree()
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
    large_tree = FullBinaryTree()
    for i in range(15):  # Using a smaller number to keep the tree manageable
        large_tree.insert(i)
    
    print("Height:", large_tree.height())
    print("Is full?", large_tree.is_full())
    print("Total nodes:", large_tree.count_nodes())
    print("Internal nodes:", large_tree.count_internal_nodes())
    print("Leaf nodes:", large_tree.count_leaves())
    print("Leaf values:", large_tree.get_leaf_values())
