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

## Requirements

- Python 3.8+
- No external dependencies required

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

## License

This project is licensed under the MIT License - see the LICENSE file for details. 