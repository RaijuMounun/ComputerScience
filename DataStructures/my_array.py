"""A low-level array implementation in Python using ctypes.

This module provides a dynamic array implementation that mimics the behavior
of low-level arrays while providing dynamic resizing capabilities. The array
automatically grows when needed and provides efficient O(1) access to elements.

Features:
- Dynamic resizing
- O(1) random access
- O(1) append operation (amortized)
- O(n) insert/delete operations
- Type safety with type hints
- Comprehensive error handling

Example:
    >>> arr = MyArray()
    >>> arr.append(1)
    >>> arr.append(2)
    >>> print(arr[0])  # Output: 1
    >>> arr.insert(1, 3)
    >>> print(arr)  # Output: [1, 3, 2]
"""

from typing import Iterator, TypeVar, Generic
import ctypes
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class ArrayError(Exception):
    """Base exception class for array operations."""
    message: str

class IndexOutOfBoundsError(ArrayError):
    """Raised when an index is out of bounds."""
    pass

class EmptyArrayError(ArrayError):
    """Raised when trying to perform operations on an empty array."""
    pass

class MyArray(Generic[T]):
    """A low-level array implementation using ctypes.
    
    This class provides a dynamic array implementation that automatically
    resizes when needed. It uses ctypes for low-level memory management
    and provides type-safe operations.
    
    Attributes:
        capacity: The current capacity of the array
        length: The current number of elements in the array
        data: The underlying ctypes array
    
    Type Parameters:
        T: The type of elements stored in the array
    """
    
    def __init__(self, capacity: int = 2) -> None:
        """Initialize an empty array with the given capacity.
        
        Args:
            capacity: Initial capacity of the array (default: 2)
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.length = 0
        self.data = self._make_array(capacity)
    
    def _make_array(self, size: int) -> ctypes.Array:
        """Create a new ctypes array of the given size.
        
        Args:
            size: The size of the array to create
            
        Returns:
            A new ctypes array of the specified size
        """
        return (size * ctypes.py_object)()
    
    def __len__(self) -> int:
        """Return the number of elements in the array.
        
        Returns:
            The current length of the array
        """
        return self.length
    
    def __getitem__(self, index: int) -> T:
        """Get the element at the specified index.
        
        Args:
            index: The index of the element to get
            
        Returns:
            The element at the specified index
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
        """
        if not 0 <= index < self.length:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self.length})")
        return self.data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set the element at the specified index.
        
        Args:
            index: The index of the element to set
            value: The value to set at the specified index
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
        """
        if not 0 <= index < self.length:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self.length})")
        self.data[index] = value
    
    def append(self, value: T) -> None:
        """Append an element to the end of the array.
        
        If the array is full, it will be resized to double its current capacity.
        
        Args:
            value: The value to append
            
        Time Complexity:
            O(1) amortized
        """
        if self.length == self.capacity:
            self._resize()
        self.data[self.length] = value
        self.length += 1
    
    def _resize(self) -> None:
        """Double the capacity of the array and copy existing elements.
        
        Time Complexity:
            O(n) where n is the current length
        """
        new_capacity = self.capacity * 2
        new_data = self._make_array(new_capacity)
        for i in range(self.length):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity
    
    def insert(self, index: int, value: T) -> None:
        """Insert an element at the specified index.
        
        Args:
            index: The index at which to insert the value
            value: The value to insert
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
            
        Time Complexity:
            O(n) where n is the current length
        """
        if not 0 <= index <= self.length:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self.length}]")
        
        if self.length == self.capacity:
            self._resize()
        
        # Shift elements to make space
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i - 1]
        
        self.data[index] = value
        self.length += 1
    
    def delete(self, index: int) -> None:
        """Delete the element at the specified index.
        
        Args:
            index: The index of the element to delete
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
            
        Time Complexity:
            O(n) where n is the current length
        """
        if not 0 <= index < self.length:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self.length})")
        
        # Shift elements to fill the gap
        for i in range(index, self.length - 1):
            self.data[i] = self.data[i + 1]
        
        self.data[self.length - 1] = None
        self.length -= 1
    
    def pop(self) -> T:
        """Remove and return the last element of the array.
        
        Returns:
            The last element of the array
            
        Raises:
            EmptyArrayError: If the array is empty
            
        Time Complexity:
            O(1)
        """
        if self.length == 0:
            raise EmptyArrayError("Cannot pop from empty array")
        
        value = self.data[self.length - 1]
        self.data[self.length - 1] = None
        self.length -= 1
        return value
    
    def find(self, value: T) -> int:
        """Find the index of the first occurrence of a value.
        
        Args:
            value: The value to find
            
        Returns:
            The index of the first occurrence, or -1 if not found
            
        Time Complexity:
            O(n) where n is the current length
        """
        for i in range(self.length):
            if self.data[i] == value:
                return i
        return -1
    
    def clear(self) -> None:
        """Remove all elements from the array.
        
        Time Complexity:
            O(1)
        """
        self.data = self._make_array(self.capacity)
        self.length = 0
    
    def contains(self, value: T) -> bool:
        """Check if the array contains a value.
        
        Args:
            value: The value to check for
            
        Returns:
            True if the value is found, False otherwise
            
        Time Complexity:
            O(n) where n is the current length
        """
        return self.find(value) != -1
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the array.
        
        Returns:
            An iterator yielding each element in the array
        """
        for i in range(self.length):
            yield self.data[i]
    
    def __repr__(self) -> str:
        """Return a string representation of the array.
        
        Returns:
            A string showing the array's contents
        """
        return f"MyArray([{', '.join(repr(self.data[i]) for i in range(self.length))}])"
    
    def __str__(self) -> str:
        """Return a string representation of the array.
        
        Returns:
            A string showing the array's contents
        """
        return "[" + ", ".join(str(self.data[i]) for i in range(self.length)) + "]"


if __name__ == "__main__":
    def test_array():
        """Test the array implementation with various operations."""
        # Create an array
        arr = MyArray[int](5)
        print("Created array with capacity 5")
        
        # Test append
        print("\nTesting append:")
        for i in range(1, 6):
            arr.append(i)
            print(f"Appended {i}: {arr}")
        
        # Test insert
        print("\nTesting insert:")
        arr.insert(2, 10)
        print(f"Inserted 10 at index 2: {arr}")
        
        # Test delete
        print("\nTesting delete:")
        arr.delete(3)
        print(f"Deleted element at index 3: {arr}")
        
        # Test pop
        print("\nTesting pop:")
        value = arr.pop()
        print(f"Popped {value}: {arr}")
        
        # Test find and contains
        print("\nTesting find and contains:")
        print(f"Index of 10: {arr.find(10)}")
        print(f"Contains 3: {arr.contains(3)}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements:", end=" ")
        for x in arr:
            print(x, end=" ")
        print()
        
        # Test error handling
        print("\nTesting error handling:")
        try:
            arr[10]  # Index out of bounds
        except IndexOutOfBoundsError as e:
            print(f"Expected error: {e}")
        
        try:
            arr.insert(10, 5)  # Index out of bounds
        except IndexOutOfBoundsError as e:
            print(f"Expected error: {e}")
        
        try:
            empty = MyArray[int]()
            empty.pop()  # Empty array
        except EmptyArrayError as e:
            print(f"Expected error: {e}")
        
        # Test clear
        print("\nTesting clear:")
        arr.clear()
        print(f"Cleared array: {arr}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            arr.append("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_array()
