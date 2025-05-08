# Computer Science Implementations

This repository contains implementations of various computer science concepts and data structures in Python. The implementations are designed to be educational, well-documented, and type-safe.

## Data Structures

The `DataStructures` directory contains implementations of fundamental data structures with the following features:

- Type safety using Python's type hints
- Comprehensive error handling
- Detailed documentation
- Time complexity analysis
- Unit tests
- Example usage

### Implemented Data Structures

1. **Hash Table** (`my_hash_table.py`)
   - Linear probing collision resolution
   - Dynamic resizing
   - O(1) average case operations
   - Generic type support
   - Iterator implementation

2. **Heap** (`my_heap.py`)
   - Min heap implementation
   - Generic type support
   - O(log n) operations
   - Iterator implementation

3. **Array** (`my_array.py`)
   - Dynamic array implementation
   - Generic type support
   - O(1) random access
   - Iterator implementation

4. **Linked List** (`my_linked_list.py`)
   - Singly linked list implementation
   - Generic type support
   - O(1) insertions and deletions at head
   - O(n) search operations
   - Iterator implementation

5. **Stack** (`my_stack.py`)
   - LIFO (Last In, First Out) implementation
   - Generic type support
   - O(1) push and pop operations
   - Dynamic resizing
   - Iterator implementation

6. **Queue** (`my_queue.py`)
   - FIFO (First In, First Out) implementation
   - Generic type support
   - O(1) enqueue and dequeue operations
   - Dynamic resizing
   - Iterator implementation

7. **Circular Linked List** (`my_circular_linked_list.py`)
   - Circular singly linked list implementation
   - Generic type support
   - O(1) insertions and deletions
   - Circular traversal support
   - Iterator implementation

8. **Doubly Linked List** (`my_doubly_linked_list.py`)
   - Doubly linked list implementation
   - Generic type support
   - O(1) insertions and deletions
   - Bidirectional traversal
   - Iterator implementation

### Tree Implementations

1. **Binary Tree** (`Trees/my_binary_tree.py`)
   - Generic binary tree implementation
   - Multiple traversal methods
   - Height and depth calculations
   - Node operations

2. **Binary Search Tree** (`Trees/binary_search_tree.py`)
   - Self-balancing BST implementation
   - O(log n) search operations
   - In-order traversal
   - Node deletion and insertion

3. **Balanced Tree** (`Trees/balanced_tree.py`)
   - AVL tree implementation
   - Automatic balancing
   - O(log n) operations
   - Height balancing

4. **Complete Binary Tree** (`Trees/complete_binary_tree.py`)
   - Complete binary tree implementation
   - Level-order traversal
   - Array-based representation
   - Heap-like structure

5. **Full Binary Tree** (`Trees/full_binary_tree.py`)
   - Full binary tree implementation
   - Node validation
   - Tree properties checking
   - Traversal methods

### Graph Implementations

1. **Adjacency List** (`Graphs/AdjacencyList.py`)
   - Space-efficient graph representation
   - O(V + E) space complexity
   - Fast edge lookups
   - Vertex and edge operations

2. **Adjacency Matrix** (`Graphs/AdjacencyMatrix.py`)
   - Dense graph representation
   - O(V²) space complexity
   - O(1) edge lookups
   - Matrix operations

3. **Directed Graph** (`Graphs/DirectedGraph.py`)
   - Directed graph implementation
   - Edge direction support
   - Path finding algorithms
   - Cycle detection

4. **Undirected Graph** (`Graphs/UndirectedGraph.py`)
   - Undirected graph implementation
   - Symmetric edge representation
   - Connected components
   - Graph traversal

5. **Spanning Tree** (`Graphs/SpanningTree.py`)
   - Minimum spanning tree algorithms
   - Kruskal's algorithm
   - Prim's algorithm
   - Tree validation

## Requirements

- Python 3.8+
- NumPy (for matrix operations in graph implementations)
- No other external dependencies required

## Usage

Each data structure implementation includes:
- Comprehensive docstrings
- Type hints
- Example usage in the `if __name__ == "__main__":` block
- Unit tests

Example usage of the Hash Table:

```python
from DataStructures.my_hash_table import HashTable

# Create a hash table with string keys and integer values
table = HashTable[str, int]()

# Insert key-value pairs
table.put("one", 1)
table.put("two", 2)

# Retrieve values
value = table.get("one")  # Returns 1

# Remove entries
table.remove("two")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
