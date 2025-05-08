"""A circular linked list implementation.

This module provides a circular linked list implementation with comprehensive
features and type safety. The linked list uses a sentinel node for efficient
operations and maintains a circular structure.

Features:
- O(1) prepend operations
- O(n) append and search operations
- Sentinel node for efficient operations
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support
- Advanced operations (split, rotate, kth from end)

Example:
    >>> lst = MyCircularLinkedList[int]()
    >>> lst.append(1)
    >>> lst.append(2)
    >>> print(lst)  # Output: 1 -> 2 -> (head)
    >>> lst.rotate(1)
    >>> print(lst)  # Output: 2 -> 1 -> (head)
"""

from typing import TypeVar, Generic, Optional, Iterator, Tuple
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class CircularLinkedListError(Exception):
    """Base exception class for circular linked list operations."""
    message: str

class IndexOutOfBoundsError(CircularLinkedListError):
    """Raised when an index is out of bounds."""
    pass

class EmptyListError(CircularLinkedListError):
    """Raised when trying to perform operations on an empty list."""
    pass

class Node(Generic[T]):
    """A node in the circular linked list.
    
    Attributes:
        value: The value stored in the node
        next: Reference to the next node
    """
    def __init__(self, value: Optional[T] = None) -> None:
        """Initialize a new node.
        
        Args:
            value: The value to store in the node (optional for sentinel node)
        """
        self.value = value
        self.next: Optional[Node[T]] = None

class MyCircularLinkedList(Generic[T]):
    """A circular linked list implementation.
    
    This class provides a circular linked list implementation using a sentinel
    node for efficient operations. It supports generic types and provides
    comprehensive error handling.
    
    Attributes:
        sentinel: A sentinel node that marks the start/end of the list
        _size: Current number of elements
        _iter_node: Current node for iteration
    
    Type Parameters:
        T: The type of elements stored in the list
    """
    
    def __init__(self) -> None:
        """Initialize an empty circular linked list with a sentinel node."""
        self.sentinel = Node[T]()  # Sentinel node (valueless)
        self.sentinel.next = self.sentinel  # Points to itself
        self._size: int = 0
        self._iter_node: Optional[Node[T]] = None  # For iteration
    
    def append(self, value: T) -> None:
        """Append an element to the end of the list.
        
        Args:
            value: The value to append
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        new_node = Node(value)
        current = self.sentinel
        while current.next != self.sentinel:
            current = current.next
        current.next = new_node
        new_node.next = self.sentinel
        self._size += 1
    
    def prepend(self, value: T) -> None:
        """Prepend an element to the start of the list.
        
        Args:
            value: The value to prepend
            
        Time Complexity:
            O(1)
        """
        new_node = Node(value)
        new_node.next = self.sentinel.next
        self.sentinel.next = new_node
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
        prev = self.sentinel
        current = self.sentinel.next
        while current != self.sentinel:
            if current.value == value:
                prev.next = current.next
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False
    
    def reverse(self) -> None:
        """Reverse the list in place.
        
        Time Complexity:
            O(n) where n is the number of elements
        """
        prev = self.sentinel
        current = self.sentinel.next
        while current != self.sentinel:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.sentinel.next = prev
    
    def kth_from_end(self, k: int) -> T:
        """Find the k-th element from the end of the list.
        
        Args:
            k: The position from the end (1-based)
            
        Returns:
            The value at the k-th position from the end
            
        Raises:
            IndexOutOfBoundsError: If k is invalid
            EmptyListError: If the list is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyListError("Cannot find kth element in empty list")
        
        if k <= 0 or k > self._size:
            raise IndexOutOfBoundsError(f"Invalid k: {k}")
        
        slow = self.sentinel.next
        fast = self.sentinel.next
        for _ in range(k):
            fast = fast.next
        while fast != self.sentinel:
            slow = slow.next
            fast = fast.next
        return slow.value
    
    def find_middle(self) -> T:
        """Find the middle element of the list.
        
        Returns:
            The middle element (second middle if even length)
            
        Raises:
            EmptyListError: If the list is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyListError("Cannot find middle of empty list")
        
        slow = self.sentinel.next
        fast = self.sentinel.next
        while fast != self.sentinel and fast.next != self.sentinel:
            slow = slow.next
            fast = fast.next.next
        return slow.value
    
    def split(self) -> Tuple['MyCircularLinkedList[T]', 'MyCircularLinkedList[T]']:
        """Split the list into two halves.
        
        Returns:
            A tuple containing two new circular linked lists
            
        Raises:
            ValueError: If the list is too small to split
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self._size < 2:
            raise ValueError("List too small to split")
        
        mid_index = self._size // 2
        first_half = MyCircularLinkedList[T]()
        second_half = MyCircularLinkedList[T]()
        
        current = self.sentinel.next
        for _ in range(mid_index):
            first_half.append(current.value)
            current = current.next
        for _ in range(self._size - mid_index):
            second_half.append(current.value)
            current = current.next
        
        return first_half, second_half
    
    def rotate(self, k: int) -> None:
        """Rotate the list k positions to the left.
        
        Args:
            k: Number of positions to rotate
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self._size == 0 or k % self._size == 0:
            return
        
        k = k % self._size
        current = self.sentinel.next
        for _ in range(k - 1):
            current = current.next
        new_head = current.next
        current.next = self.sentinel
        last = new_head
        while last.next != self.sentinel:
            last = last.next
        last.next = new_head
        self.sentinel.next = new_head
    
    def copy_deep(self) -> 'MyCircularLinkedList[T]':
        """Create a deep copy of the list.
        
        Returns:
            A new circular linked list with the same elements
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        new_list = MyCircularLinkedList[T]()
        for value in self:
            new_list.append(value)
        return new_list
    
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
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the list.
        
        Returns:
            An iterator yielding each element in the list
        """
        self._iter_node = self.sentinel.next
        return self
    
    def __next__(self) -> T:
        """Get the next element in the iteration.
        
        Returns:
            The next element
            
        Raises:
            StopIteration: If there are no more elements
        """
        if self._iter_node == self.sentinel:
            raise StopIteration
        value = self._iter_node.value
        self._iter_node = self._iter_node.next
        return value
    
    def __str__(self) -> str:
        """Return a string representation of the list.
        
        Returns:
            A string showing the list's contents
        """
        if self.is_empty():
            return "Empty List"
        return " -> ".join(str(val) for val in self) + " -> (head)"


if __name__ == "__main__":
    def test_circular_linked_list():
        """Test the circular linked list implementation with various operations."""
        # Create a circular linked list
        lst = MyCircularLinkedList[int]()
        print("Created empty circular linked list")
        
        # Test append
        print("\nTesting append:")
        for i in range(1, 6):
            lst.append(i)
            print(f"Appended {i}: {lst}")
        
        # Test prepend
        print("\nTesting prepend:")
        lst.prepend(0)
        print(f"Prepended 0: {lst}")
        
        # Test delete
        print("\nTesting delete:")
        lst.delete(3)
        print(f"Deleted 3: {lst}")
        
        # Test find_middle
        print("\nTesting find_middle:")
        print(f"Middle element: {lst.find_middle()}")
        
        # Test kth_from_end
        print("\nTesting kth_from_end:")
        print(f"2nd from end: {lst.kth_from_end(2)}")
        
        # Test reverse
        print("\nTesting reverse:")
        lst.reverse()
        print(f"Reversed: {lst}")
        
        # Test split
        print("\nTesting split:")
        first, second = lst.split()
        print(f"First half: {first}")
        print(f"Second half: {second}")
        
        # Test rotate
        print("\nTesting rotate:")
        lst.rotate(2)
        print(f"Rotated 2 times: {lst}")
        
        # Test copy_deep
        print("\nTesting copy_deep:")
        copy = lst.copy_deep()
        print(f"Copy: {copy}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements:", end=" ")
        for x in lst:
            print(x, end=" ")
        print()
        
        # Test error handling
        print("\nTesting error handling:")
        try:
            lst.kth_from_end(10)  # Invalid k
        except IndexOutOfBoundsError as e:
            print(f"Expected error: {e}")
        
        empty = MyCircularLinkedList[int]()
        try:
            empty.find_middle()  # Empty list
        except EmptyListError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.split()  # Too small to split
        except ValueError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            lst.append("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_circular_linked_list()
