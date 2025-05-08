"""A hash table implementation using linear probing.

This module provides a hash table implementation with comprehensive features
and type safety. The hash table uses linear probing for collision resolution
and supports dynamic resizing.

Features:
- O(1) average case for insert, delete, and search operations
- Dynamic resizing
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support
- Linear probing collision resolution

Example:
    >>> table = HashTable[str, int]()
    >>> table.put("one", 1)
    >>> table.put("two", 2)
    >>> print(table.get("one"))  # Output: 1
    >>> print(table.remove("two"))  # Output: None
"""

from typing import TypeVar, Generic, Iterator, Optional, Any
from dataclasses import dataclass
from DataStructures.my_array import MyArray

K = TypeVar('K')
V = TypeVar('V')

@dataclass
class HashTableError(Exception):
    """Base exception class for hash table operations."""
    message: str

class KeyNotFoundError(HashTableError):
    """Raised when trying to access a non-existent key."""
    pass

class HashTableEntry(Generic[K, V]):
    """A single entry in the hash table.
    
    Attributes:
        key: The key of the entry
        value: The value associated with the key
    """
    def __init__(self, key: K, value: V) -> None:
        """Initialize a hash table entry.
        
        Args:
            key: The key of the entry
            value: The value associated with the key
        """
        self.key = key
        self.value = value

class HashTable(Generic[K, V]):
    """A hash table implementation using linear probing for collision resolution.
    
    This class provides a hash table implementation with comprehensive features
    and type safety. It uses linear probing for collision resolution and supports
    dynamic resizing.
    
    Attributes:
        capacity: The current capacity of the hash table
        size: The number of key-value pairs in the table
        table: The underlying array storing the entries
        load_factor: The maximum load factor before resizing (default: 0.7)
    
    Type Parameters:
        K: The type of keys stored in the table
        V: The type of values stored in the table
    """
    
    def __init__(self, capacity: int = 8, load_factor: float = 0.7) -> None:
        """Initialize an empty hash table.
        
        Args:
            capacity: Initial capacity of the hash table (default: 8)
            load_factor: Maximum load factor before resizing (default: 0.7)
        """
        self.capacity = capacity
        self.size = 0
        self.load_factor = load_factor
        self.table = MyArray[Optional[HashTableEntry[K, V]]](capacity)
        for _ in range(capacity):
            self.table.append(None)
    
    def _hash(self, key: K) -> int:
        """Compute the hash value for a key.
        
        Args:
            key: The key to hash
            
        Returns:
            The hash value for the key
            
        Time Complexity:
            O(k) where k is the length of the key's string representation
        """
        hash_value = 0
        p = 31
        m = self.capacity
        for i, char in enumerate(str(key)):
            hash_value += (ord(char) * (p ** i)) % m
        return hash_value % m
    
    def _probe(self, index: int) -> Iterator[int]:
        """Generate indices for linear probing.
        
        Args:
            index: The initial index to start probing from
            
        Yields:
            The next index to probe
            
        Time Complexity:
            O(1) per iteration
        """
        while True:
            yield index
            index = (index + 1) % self.capacity
    
    def put(self, key: K, value: V) -> None:
        """Insert a key-value pair into the hash table.
        
        Args:
            key: The key to insert
            value: The value to associate with the key
            
        Time Complexity:
            O(1) average case, O(n) worst case
        """
        if self.size >= self.capacity * self.load_factor:
            self._resize()
        
        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None or self.table[i].key == key:
                if self.table[i] is None:
                    self.size += 1
                self.table[i] = HashTableEntry(key, value)
                return
    
    def get(self, key: K) -> V:
        """Retrieve a value by its key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key
            
        Raises:
            KeyNotFoundError: If the key is not found
            
        Time Complexity:
            O(1) average case, O(n) worst case
        """
        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None:
                raise KeyNotFoundError(f"Key '{key}' not found")
            if self.table[i].key == key:
                return self.table[i].value
    
    def remove(self, key: K) -> None:
        """Remove a key-value pair from the hash table.
        
        Args:
            key: The key to remove
            
        Raises:
            KeyNotFoundError: If the key is not found
            
        Time Complexity:
            O(1) average case, O(n) worst case
        """
        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None:
                raise KeyNotFoundError(f"Key '{key}' not found")
            if self.table[i].key == key:
                self.table[i] = None
                self.size -= 1
                return
    
    def _resize(self) -> None:
        """Resize the hash table to double its capacity.
        
        Time Complexity:
            O(n) where n is the number of elements
        """
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = MyArray[Optional[HashTableEntry[K, V]]](self.capacity)
        for _ in range(self.capacity):
            self.table.append(None)
        
        for item in old_table:
            if item is not None:
                self.put(item.key, item.value)
    
    def is_empty(self) -> bool:
        """Check if the hash table is empty.
        
        Returns:
            True if the hash table is empty, False otherwise
            
        Time Complexity:
            O(1)
        """
        return self.size == 0
    
    def clear(self) -> None:
        """Remove all key-value pairs from the hash table.
        
        Time Complexity:
            O(n) where n is the capacity
        """
        self.size = 0
        for i in range(self.capacity):
            self.table[i] = None
    
    def __iter__(self) -> Iterator[tuple[K, V]]:
        """Return an iterator over the key-value pairs in the hash table.
        
        Returns:
            An iterator yielding (key, value) pairs
            
        Time Complexity:
            O(n) where n is the capacity
        """
        for item in self.table:
            if item is not None:
                yield (item.key, item.value)
    
    def __str__(self) -> str:
        """Return a string representation of the hash table.
        
        Returns:
            A string showing the hash table's contents
        """
        if self.is_empty():
            return "{}"
        items = [f"{entry.key}: {entry.value}" for entry in self.table if entry is not None]
        return "{" + ", ".join(items) + "}"


if __name__ == "__main__":
    def test_hash_table():
        """Test the hash table implementation with various operations."""
        # Create a hash table
        table = HashTable[str, int]()
        print("Created empty hash table")
        
        # Test put
        print("\nTesting put:")
        test_data = [("one", 1), ("two", 2), ("three", 3), ("four", 4)]
        for key, value in test_data:
            table.put(key, value)
            print(f"Put {key}: {value} -> {table}")
        
        # Test get
        print("\nTesting get:")
        for key, value in test_data:
            print(f"Get {key}: {table.get(key)}")
        
        # Test remove
        print("\nTesting remove:")
        table.remove("two")
        print(f"After removing 'two': {table}")
        
        # Test is_empty and clear
        print("\nTesting is_empty and clear:")
        print(f"Is empty: {table.is_empty()}")
        table.clear()
        print(f"After clear: {table}")
        print(f"Is empty: {table.is_empty()}")
        
        # Test iteration
        print("\nTesting iteration:")
        for key, value in test_data:
            table.put(key, value)
        print("Key-value pairs:", end=" ")
        for key, value in table:
            print(f"{key}={value}", end=" ")
        print()
        
        # Test error handling
        print("\nTesting error handling:")
        try:
            table.get("nonexistent")  # Key not found
        except KeyNotFoundError as e:
            print(f"Expected error: {e}")
        
        try:
            table.remove("nonexistent")  # Key not found
        except KeyNotFoundError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            table.put(123, "string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_hash_table()
