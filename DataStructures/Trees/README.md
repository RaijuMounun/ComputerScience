# Tree Data Structures

This directory contains various tree data structure implementations in Python.

## Implementations

### Base Tree
- `my_binary_tree.py`: Base binary tree implementation with basic operations
  - Insertion and deletion
  - Various traversal methods (inorder, preorder, postorder)
  - Tree property checks (balanced, full, perfect)
  - Node counting and leaf counting
  - Tree comparison and mirroring

### Specialized Trees
- `balanced_tree.py`: AVL tree implementation that maintains balance
- `unbalanced_tree.py`: Basic binary tree without balancing operations
- `binary_search_tree.py`: Binary search tree implementation
- `complete_binary_tree.py`: Complete binary tree implementation
- `full_binary_tree.py`: Full binary tree implementation

## Usage Examples

### Basic Binary Tree
```python
from Trees import MyBinaryTree

tree = MyBinaryTree()
tree.insert(5)
tree.insert(3)
tree.insert(7)

print(tree.traverse_inorder())  # [3, 5, 7]
print(tree.is_balanced())       # True
```

### Balanced Tree (AVL)
```python
from Trees import BalancedTree

tree = BalancedTree()
tree.insert(5)
tree.insert(3)
tree.insert(7)

print(tree.traverse_inorder())  # [3, 5, 7]
print(tree.is_balanced())       # True
```

## Features

- Type hints for better code understanding
- Comprehensive error handling
- Detailed documentation
- Test cases for each implementation
- Performance optimizations where applicable

## Testing

Each implementation includes test cases in its `__main__` block. To run tests:

```bash
python -m Trees.my_binary_tree
python -m Trees.balanced_tree
# etc.
```

## Performance Characteristics

- Basic operations (insert, delete, search): O(log n) for balanced trees, O(n) for unbalanced trees
- Traversal operations: O(n) for all tree types
- Space complexity: O(n) for all tree types 