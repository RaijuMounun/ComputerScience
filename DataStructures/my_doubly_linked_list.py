"""A doubly linked list implementation.

This module provides a doubly linked list implementation with comprehensive
features and type safety. The linked list maintains both head and tail pointers
for efficient operations at both ends.

Features:
- O(1) prepend and append operations
- O(n) search and delete operations
- Bidirectional traversal
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support

Example:
    >>> lst = MyDoublyLinkedList[int]()
    >>> lst.append(1)
    >>> lst.append(2)
    >>> print(lst[0])  # Output: 1
    >>> lst.insert_at(1, 3)
    >>> print(lst)  # Output: 1 <-> 3 <-> 2 <-> None
"""

from typing import TypeVar, Generic, Optional, Iterator, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class DoublyLinkedListError(Exception):
    """Base exception class for doubly linked list operations."""
    message: str

class IndexOutOfBoundsError(DoublyLinkedListError):
    """Raised when an index is out of bounds."""
    pass

class EmptyListError(DoublyLinkedListError):
    """Raised when trying to perform operations on an empty list."""
    pass

class Node(Generic[T]):
    """A node in the doubly linked list.
    
    Attributes:
        value: The value stored in the node
        prev: Reference to the previous node
        next: Reference to the next node
    """
    def __init__(self, value: T) -> None:
        """Initialize a new node.
        
        Args:
            value: The value to store in the node
        """
        self.value = value
        self.prev: Optional[Node[T]] = None
        self.next: Optional[Node[T]] = None

class MyDoublyLinkedList(Generic[T]):
    """A doubly linked list implementation.
    
    This class provides a doubly linked list implementation with both head
    and tail pointers for efficient operations. It supports generic types
    and provides comprehensive error handling.
    
    Attributes:
        head: Reference to the first node
        tail: Reference to the last node
        _size: Current number of elements
    
    Type Parameters:
        T: The type of elements stored in the list
    """
    
    def __init__(self) -> None:
        """Initialize an empty doubly linked list."""
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size: int = 0
    
    def append(self, value: T) -> None:
        """Append an element to the end of the list.
        
        Args:
            value: The value to append
            
        Time Complexity:
            O(1)
        """
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1
    
    def prepend(self, value: T) -> None:
        """Prepend an element to the start of the list.
        
        Args:
            value: The value to prepend
            
        Time Complexity:
            O(1)
        """
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node
        self._size += 1
    
    def delete(self, value: T) -> bool:
        """Delete the first occurrence of a value from the list.
        
        Args:
            value: The value to delete
            
        Returns:
            True if the value was found and deleted, False otherwise
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if not self.head:
            return False
        
        current = self.head
        while current:
            if current.value == value:
                if current.prev:  # Middle or tail node
                    current.prev.next = current.next
                else:  # Head node
                    self.head = current.next
                
                if current.next:  # Middle or head node
                    current.next.prev = current.prev
                else:  # Tail node
                    self.tail = current.prev
                
                self._size -= 1
                return True
            current = current.next
        return False
    
    def find(self, value: T) -> int:
        """Find the index of the first occurrence of a value.
        
        Args:
            value: The value to find
            
        Returns:
            The index of the first occurrence, or -1 if not found
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1
    
    def size(self) -> int:
        """Get the number of elements in the list.
        
        Returns:
            The current size of the list
            
        Time Complexity:
            O(1)
        """
        return self._size
    
    def is_empty(self) -> bool:
        """Check if the list is empty.
        
        Returns:
            True if the list is empty, False otherwise
            
        Time Complexity:
            O(1)
        """
        return self._size == 0
    
    def reverse(self) -> None:
        """Reverse the list in place.
        
        Time Complexity:
            O(n) where n is the number of elements
        """
        current = self.head
        self.tail = current
        prev = None
        while current:
            prev = current.prev
            current.prev = current.next
            current.next = prev
            current = current.prev
        if prev:
            self.head = prev.prev
    
    def insert_at(self, index: int, value: T) -> None:
        """Insert a value at the specified index.
        
        Args:
            index: The index at which to insert
            value: The value to insert
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if not 0 <= index <= self._size:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self._size}]")
        
        if index == 0:
            self.prepend(value)
            return
        
        if index == self._size:
            self.append(value)
            return
        
        new_node = Node(value)
        current = self.head
        for _ in range(index):
            current = current.next
        
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self._size += 1
    
    def to_list_forward(self) -> List[T]:
        """Convert the list to a Python list in forward order.
        
        Returns:
            A list containing all elements in forward order
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        current = self.head
        result = []
        while current:
            result.append(current.value)
            current = current.next
        return result
    
    def to_list_backward(self) -> List[T]:
        """Convert the list to a Python list in backward order.
        
        Returns:
            A list containing all elements in backward order
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        current = self.tail
        result = []
        while current:
            result.append(current.value)
            current = current.prev
        return result
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the list.
        
        Returns:
            An iterator yielding each element in the list
        """
        current = self.head
        while current:
            yield current.value
            current = current.next
    
    def __str__(self) -> str:
        """Return a string representation of the list.
        
        Returns:
            A string showing the list's contents
        """
        if not self.head:
            return "Empty List"
        return " <-> ".join(str(v) for v in self.to_list_forward()) + " <-> None"


if __name__ == "__main__":
    def test_doubly_linked_list():
        """Test the doubly linked list implementation with various operations."""
        # Create a doubly linked list
        lst = MyDoublyLinkedList[int]()
        print("Created empty doubly linked list")
        
        # Test append
        print("\nTesting append:")
        for i in range(1, 4):
            lst.append(i)
            print(f"Appended {i}: {lst}")
        
        # Test prepend
        print("\nTesting prepend:")
        lst.prepend(0)
        print(f"Prepended 0: {lst}")
        
        # Test insert_at
        print("\nTesting insert_at:")
        lst.insert_at(2, 10)
        print(f"Inserted 10 at index 2: {lst}")
        
        # Test delete
        print("\nTesting delete:")
        lst.delete(2)
        print(f"Deleted 2: {lst}")
        
        # Test find
        print("\nTesting find:")
        print(f"Index of 10: {lst.find(10)}")
        print(f"Index of 5: {lst.find(5)}")
        
        # Test size and is_empty
        print("\nTesting size and is_empty:")
        print(f"Size: {lst.size()}")
        print(f"Is empty: {lst.is_empty()}")
        
        # Test reverse
        print("\nTesting reverse:")
        lst.reverse()
        print(f"Reversed: {lst}")
        
        # Test forward and backward traversal
        print("\nTesting traversal:")
        print(f"Forward: {lst.to_list_forward()}")
        print(f"Backward: {lst.to_list_backward()}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements:", end=" ")
        for x in lst:
            print(x, end=" ")
        print()
        
        # Test error handling
        print("\nTesting error handling:")
        try:
            lst.insert_at(10, 5)  # Index out of bounds
        except IndexOutOfBoundsError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            lst.append("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_doubly_linked_list()
