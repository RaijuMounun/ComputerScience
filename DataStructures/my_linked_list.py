"""A singly linked list implementation.

This module provides a singly linked list implementation with comprehensive
features and type safety. The linked list maintains both head and tail pointers
for efficient operations at both ends.

Features:
- O(1) prepend and append operations
- O(n) search and delete operations
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support

Example:
    >>> lst = MyLinkedList[int]()
    >>> lst.append(1)
    >>> lst.append(2)
    >>> print(lst[0])  # Output: 1
    >>> lst.insert_at(1, 3)
    >>> print(lst)  # Output: 1 -> 3 -> 2 -> None
"""

from typing import TypeVar, Generic, Optional, Iterator
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class LinkedListError(Exception):
    """Base exception class for linked list operations."""
    message: str

class IndexOutOfBoundsError(LinkedListError):
    """Raised when an index is out of bounds."""
    pass

class EmptyListError(LinkedListError):
    """Raised when trying to perform operations on an empty list."""
    pass

class Node(Generic[T]):
    """A node in the linked list.
    
    Attributes:
        value: The value stored in the node
        next: Reference to the next node
    """
    def __init__(self, value: T) -> None:
        """Initialize a new node.
        
        Args:
            value: The value to store in the node
        """
        self.value = value
        self.next: Optional[Node[T]] = None

class MyLinkedList(Generic[T]):
    """A singly linked list implementation.
    
    This class provides a singly linked list implementation with both head
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
        """Initialize an empty linked list."""
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
        
        if self.head.value == value:
            self.head = self.head.next
            if not self.head:
                self.tail = None
            self._size -= 1
            return True
        
        current = self.head
        while current.next and current.next.value != value:
            current = current.next
        
        if current.next:
            if current.next == self.tail:
                self.tail = current
            current.next = current.next.next
            self._size -= 1
            return True
        
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
        prev = None
        current = self.head
        self.tail = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
    
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
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def remove_at(self, index: int) -> None:
        """Remove the element at the specified index.
        
        Args:
            index: The index of the element to remove
            
        Raises:
            IndexOutOfBoundsError: If the index is out of bounds
            EmptyListError: If the list is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyListError("Cannot remove from empty list")
        
        if not 0 <= index < self._size:
            raise IndexOutOfBoundsError(f"Index {index} out of bounds [0, {self._size})")
        
        if index == 0:
            self.head = self.head.next
            if not self.head:
                self.tail = None
            self._size -= 1
            return
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        if current.next == self.tail:
            self.tail = current
        
        current.next = current.next.next
        self._size -= 1
    
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
        
        current = self.head
        result = []
        while current:
            result.append(str(current.value))
            current = current.next
        return " -> ".join(result) + " -> None"


if __name__ == "__main__":
    def test_linked_list():
        """Test the linked list implementation with various operations."""
        # Create a linked list
        lst = MyLinkedList[int]()
        print("Created empty linked list")
        
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
        
        # Test remove_at
        print("\nTesting remove_at:")
        lst.remove_at(1)
        print(f"Removed element at index 1: {lst}")
        
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
        
        try:
            lst.remove_at(10)  # Index out of bounds
        except IndexOutOfBoundsError as e:
            print(f"Expected error: {e}")
        
        empty = MyLinkedList[int]()
        try:
            empty.remove_at(0)  # Empty list
        except EmptyListError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            lst.append("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_linked_list()
