"""A queue implementation using a dynamic array.

This module provides a queue implementation with comprehensive features
and type safety. The queue is implemented using a dynamic array for
efficient operations.

Features:
- O(1) enqueue and dequeue operations
- O(1) peek operation
- Dynamic resizing
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support
- Advanced operations (reverse, min, max)

Example:
    >>> queue = MyQueue[int]()
    >>> queue.enqueue(1)
    >>> queue.enqueue(2)
    >>> print(queue.peek())  # Output: 1
    >>> print(queue.dequeue())  # Output: 1
"""

from typing import TypeVar, Generic, Iterator
from dataclasses import dataclass
from DataStructures.my_array import MyArray

T = TypeVar('T')

@dataclass
class QueueError(Exception):
    """Base exception class for queue operations."""
    message: str

class EmptyQueueError(QueueError):
    """Raised when trying to perform operations on an empty queue."""
    pass

class MyQueue(Generic[T]):
    """A queue implementation using a dynamic array.
    
    This class provides a queue implementation with comprehensive features
    and type safety. It uses a dynamic array for efficient operations.
    
    Attributes:
        queue_array: The underlying dynamic array
        front_index: Index of the front element
        _capacity: Initial capacity of the queue
    
    Type Parameters:
        T: The type of elements stored in the queue
    """
    
    def __init__(self, capacity: int = 4) -> None:
        """Initialize an empty queue.
        
        Args:
            capacity: Initial capacity of the queue (default: 4)
        """
        self.queue_array = MyArray[T](capacity)
        self.front_index = 0
    
    def enqueue(self, value: T) -> None:
        """Add an element to the end of the queue.
        
        Args:
            value: The value to enqueue
            
        Time Complexity:
            O(1) amortized
        """
        self.queue_array.append(value)
    
    def dequeue(self) -> T:
        """Remove and return the front element from the queue.
        
        Returns:
            The front element
            
        Raises:
            EmptyQueueError: If the queue is empty
            
        Time Complexity:
            O(1) amortized
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot dequeue from empty queue")
        value = self.queue_array[self.front_index]
        self.front_index += 1
        return value
    
    def peek(self) -> T:
        """Get the front element without removing it.
        
        Returns:
            The front element
            
        Raises:
            EmptyQueueError: If the queue is empty
            
        Time Complexity:
            O(1)
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot peek from empty queue")
        return self.queue_array[self.front_index]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty.
        
        Returns:
            True if the queue is empty, False otherwise
            
        Time Complexity:
            O(1)
        """
        return self.front_index >= self.queue_array.length
    
    def size(self) -> int:
        """Get the number of elements in the queue.
        
        Returns:
            The current size of the queue
            
        Time Complexity:
            O(1)
        """
        return self.queue_array.length - self.front_index
    
    def reverse(self) -> None:
        """Reverse the queue in place.
        
        Time Complexity:
            O(n) where n is the number of elements
        """
        left = self.front_index
        right = self.queue_array.length - 1
        while left < right:
            self.queue_array[left], self.queue_array[right] = (
                self.queue_array[right],
                self.queue_array[left],
            )
            left += 1
            right -= 1
    
    def max(self) -> T:
        """Get the maximum value in the queue.
        
        Returns:
            The maximum value
            
        Raises:
            EmptyQueueError: If the queue is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot get max from empty queue")
        return max(self.queue_array[i] for i in range(self.front_index, self.queue_array.length))
    
    def min(self) -> T:
        """Get the minimum value in the queue.
        
        Returns:
            The minimum value
            
        Raises:
            EmptyQueueError: If the queue is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot get min from empty queue")
        return min(self.queue_array[i] for i in range(self.front_index, self.queue_array.length))
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the queue.
        
        Returns:
            An iterator yielding each element in the queue (front to back)
        """
        for i in range(self.front_index, self.queue_array.length):
            yield self.queue_array[i]
    
    def __str__(self) -> str:
        """Return a string representation of the queue.
        
        Returns:
            A string showing the queue's contents (front to back)
        """
        if self.is_empty():
            return "Empty Queue"
        return "Queue(front -> back): [" + ", ".join(
            str(self.queue_array[i]) for i in range(self.front_index, self.queue_array.length)) + "]"


if __name__ == "__main__":
    def test_queue():
        """Test the queue implementation with various operations."""
        # Create a queue
        queue = MyQueue[int]()
        print("Created empty queue")
        
        # Test enqueue
        print("\nTesting enqueue:")
        for i in [4, 1, 9, 2]:
            queue.enqueue(i)
            print(f"Enqueued {i}: {queue}")
        
        # Test peek
        print("\nTesting peek:")
        print(f"Front element: {queue.peek()}")
        
        # Test dequeue
        print("\nTesting dequeue:")
        print(f"Dequeued: {queue.dequeue()}")
        print(f"After dequeue: {queue}")
        
        # Test max and min
        print("\nTesting max and min:")
        print(f"Max: {queue.max()}")
        print(f"Min: {queue.min()}")
        
        # Test reverse
        print("\nTesting reverse:")
        queue.reverse()
        print(f"After reverse: {queue}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements (front to back):", end=" ")
        for x in queue:
            print(x, end=" ")
        print()
        
        # Test size and is_empty
        print("\nTesting size and is_empty:")
        print(f"Size: {queue.size()}")
        print(f"Is empty: {queue.is_empty()}")
        
        # Test error handling
        print("\nTesting error handling:")
        empty = MyQueue[int]()
        try:
            empty.dequeue()  # Empty queue
        except EmptyQueueError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.peek()  # Empty queue
        except EmptyQueueError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.max()  # Empty queue
        except EmptyQueueError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            queue.enqueue("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_queue()
