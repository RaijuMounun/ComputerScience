"""A heap implementation using a dynamic array.

This module provides both min and max heap implementations with comprehensive
features and type safety. The heaps are implemented using a dynamic array for
efficient operations.

Features:
- O(log n) insert and extract operations
- O(1) peek operation
- Dynamic resizing
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support
- Both min and max heap variants

Example:
    >>> min_heap = MyMinHeap[int]()
    >>> min_heap.insert(1)
    >>> min_heap.insert(2)
    >>> print(min_heap.peek())  # Output: 1
    >>> print(min_heap.extract_min())  # Output: 1
"""

from typing import TypeVar, Generic, Iterator
from dataclasses import dataclass
from DataStructures.my_array import MyArray

T = TypeVar('T', bound='Comparable')

class Comparable:
    """Protocol for comparable types."""
    def __lt__(self, other: 'Comparable') -> bool: ...
    def __gt__(self, other: 'Comparable') -> bool: ...

@dataclass
class HeapError(Exception):
    """Base exception class for heap operations."""
    message: str

class EmptyHeapError(HeapError):
    """Raised when trying to perform operations on an empty heap."""
    pass

class MyHeap(Generic[T]):
    """Base heap class implementing common heap operations.
    
    This class provides the base implementation for both min and max heaps.
    It uses a dynamic array for efficient operations.
    
    Attributes:
        data: The underlying dynamic array storing heap elements
    
    Type Parameters:
        T: The type of elements stored in the heap (must be comparable)
    """
    
    def __init__(self) -> None:
        """Initialize an empty heap."""
        self.data = MyArray[T]()
    
    def _parent(self, index: int) -> int:
        """Get the parent index of a given index.
        
        Args:
            index: The index to find the parent of
            
        Returns:
            The parent index
        """
        return (index - 1) // 2
    
    def _left(self, index: int) -> int:
        """Get the left child index of a given index.
        
        Args:
            index: The index to find the left child of
            
        Returns:
            The left child index
        """
        return 2 * index + 1
    
    def _right(self, index: int) -> int:
        """Get the right child index of a given index.
        
        Args:
            index: The index to find the right child of
            
        Returns:
            The right child index
        """
        return 2 * index + 2
    
    def insert(self, value: T) -> None:
        """Insert a new value into the heap.
        
        Args:
            value: The value to insert
            
        Time Complexity:
            O(log n) where n is the number of elements
        """
        self.data.append(value)
        self._heapify_up(self.data.length - 1)
    
    def _heapify_up(self, index: int) -> None:
        """Maintain heap property by bubbling up an element.
        
        Args:
            index: The index of the element to bubble up
            
        Time Complexity:
            O(log n) where n is the number of elements
        """
        pass  # To be implemented in subclasses
    
    def _heapify_down(self, index: int) -> None:
        """Maintain heap property by bubbling down an element.
        
        Args:
            index: The index of the element to bubble down
            
        Time Complexity:
            O(log n) where n is the number of elements
        """
        pass  # To be implemented in subclasses
    
    def peek(self) -> T:
        """Get the root element without removing it.
        
        Returns:
            The root element
            
        Raises:
            EmptyHeapError: If the heap is empty
            
        Time Complexity:
            O(1)
        """
        if self.data.length == 0:
            raise EmptyHeapError("Cannot peek from empty heap")
        return self.data[0]
    
    def is_empty(self) -> bool:
        """Check if the heap is empty.
        
        Returns:
            True if the heap is empty, False otherwise
            
        Time Complexity:
            O(1)
        """
        return self.data.length == 0
    
    def size(self) -> int:
        """Get the number of elements in the heap.
        
        Returns:
            The current size of the heap
            
        Time Complexity:
            O(1)
        """
        return self.data.length
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the heap.
        
        Returns:
            An iterator yielding each element in the heap
        """
        for i in range(self.data.length):
            yield self.data[i]
    
    def __str__(self) -> str:
        """Return a string representation of the heap.
        
        Returns:
            A string showing the heap's contents
        """
        if self.is_empty():
            return "Empty Heap"
        return "Heap: [" + ", ".join(str(self.data[i]) for i in range(self.data.length)) + "]"


class MyMinHeap(MyHeap[T]):
    """A binary min heap implementation.
    
    This class implements a min heap where the smallest element is always at the root.
    All elements must be comparable.
    """
    
    def _heapify_up(self, index: int) -> None:
        """Maintain min heap property by bubbling up an element.
        
        Args:
            index: The index of the element to bubble up
        """
        while index > 0 and self.data[index] < self.data[self._parent(index)]:
            self.data[index], self.data[self._parent(index)] = (
                self.data[self._parent(index)],
                self.data[index]
            )
            index = self._parent(index)
    
    def extract_min(self) -> T:
        """Remove and return the smallest element in the heap.
        
        Returns:
            The smallest element
            
        Raises:
            EmptyHeapError: If the heap is empty
            
        Time Complexity:
            O(log n) where n is the number of elements
        """
        if self.data.length == 0:
            raise EmptyHeapError("Cannot extract from empty heap")
        
        root = self.data[0]
        last = self.data.pop()
        
        if self.data.length > 0:
            self.data[0] = last
            self._heapify_down(0)
        
        return root
    
    def _heapify_down(self, index: int) -> None:
        """Maintain min heap property by bubbling down an element.
        
        Args:
            index: The index of the element to bubble down
        """
        smallest = index
        left = self._left(index)
        right = self._right(index)
        
        if left < self.data.length and self.data[left] < self.data[smallest]:
            smallest = left
        if right < self.data.length and self.data[right] < self.data[smallest]:
            smallest = right
        
        if smallest != index:
            self.data[smallest], self.data[index] = self.data[index], self.data[smallest]
            self._heapify_down(smallest)


class MyMaxHeap(MyHeap[T]):
    """A binary max heap implementation.
    
    This class implements a max heap where the largest element is always at the root.
    All elements must be comparable.
    """
    
    def _heapify_up(self, index: int) -> None:
        """Maintain max heap property by bubbling up an element.
        
        Args:
            index: The index of the element to bubble up
        """
        while index > 0 and self.data[index] > self.data[self._parent(index)]:
            self.data[index], self.data[self._parent(index)] = (
                self.data[self._parent(index)],
                self.data[index]
            )
            index = self._parent(index)
    
    def extract_max(self) -> T:
        """Remove and return the largest element in the heap.
        
        Returns:
            The largest element
            
        Raises:
            EmptyHeapError: If the heap is empty
            
        Time Complexity:
            O(log n) where n is the number of elements
        """
        if self.data.length == 0:
            raise EmptyHeapError("Cannot extract from empty heap")
        
        root = self.data[0]
        last = self.data.pop()
        
        if self.data.length > 0:
            self.data[0] = last
            self._heapify_down(0)
        
        return root
    
    def _heapify_down(self, index: int) -> None:
        """Maintain max heap property by bubbling down an element.
        
        Args:
            index: The index of the element to bubble down
        """
        largest = index
        left = self._left(index)
        right = self._right(index)
        
        if left < self.data.length and self.data[left] > self.data[largest]:
            largest = left
        if right < self.data.length and self.data[right] > self.data[largest]:
            largest = right
        
        if largest != index:
            self.data[largest], self.data[index] = self.data[index], self.data[largest]
            self._heapify_down(largest)


if __name__ == "__main__":
    def test_heap():
        """Test the heap implementations with various operations."""
        # Test MinHeap
        print("=== Testing MinHeap ===")
        min_heap = MyMinHeap[int]()
        print("Created empty min heap")
        
        # Test insert
        print("\nTesting insert:")
        for i in [10, 4, 15, 2]:
            min_heap.insert(i)
            print(f"Inserted {i}: {min_heap}")
        
        # Test peek
        print("\nTesting peek:")
        print(f"Min element: {min_heap.peek()}")
        
        # Test extract_min
        print("\nTesting extract_min:")
        print(f"Extracted min: {min_heap.extract_min()}")
        print(f"After extract: {min_heap}")
        
        # Test size and is_empty
        print("\nTesting size and is_empty:")
        print(f"Size: {min_heap.size()}")
        print(f"Is empty: {min_heap.is_empty()}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements:", end=" ")
        for x in min_heap:
            print(x, end=" ")
        print()
        
        # Test MaxHeap
        print("\n=== Testing MaxHeap ===")
        max_heap = MyMaxHeap[int]()
        print("Created empty max heap")
        
        # Test insert
        print("\nTesting insert:")
        for i in [10, 4, 15, 2]:
            max_heap.insert(i)
            print(f"Inserted {i}: {max_heap}")
        
        # Test peek
        print("\nTesting peek:")
        print(f"Max element: {max_heap.peek()}")
        
        # Test extract_max
        print("\nTesting extract_max:")
        print(f"Extracted max: {max_heap.extract_max()}")
        print(f"After extract: {max_heap}")
        
        # Test error handling
        print("\nTesting error handling:")
        empty = MyMinHeap[int]()
        try:
            empty.peek()  # Empty heap
        except EmptyHeapError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.extract_min()  # Empty heap
        except EmptyHeapError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            min_heap.insert("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_heap()
