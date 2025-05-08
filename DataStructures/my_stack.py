"""A stack implementation using a dynamic array.

This module provides a stack implementation with comprehensive features
and type safety. The stack is implemented using a dynamic array for
efficient operations.

Features:
- O(1) push and pop operations
- O(1) peek operation
- Dynamic resizing
- Type safety with type hints
- Comprehensive error handling
- Efficient memory usage
- Iterator support
- Advanced operations (reverse, min, max)

Example:
    >>> stack = MyStack[int]()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> print(stack.peek())  # Output: 2
    >>> print(stack.pop())   # Output: 2
"""

from typing import TypeVar, Generic, Iterator, Optional
from dataclasses import dataclass
from DataStructures.my_array import MyArray

T = TypeVar('T')

@dataclass
class StackError(Exception):
    """Base exception class for stack operations."""
    message: str

class EmptyStackError(StackError):
    """Raised when trying to perform operations on an empty stack."""
    pass

class MyStack(Generic[T]):
    """A stack implementation using a dynamic array.
    
    This class provides a stack implementation with comprehensive features
    and type safety. It uses a dynamic array for efficient operations.
    
    Attributes:
        stack_array: The underlying dynamic array
        _capacity: Initial capacity of the stack
    
    Type Parameters:
        T: The type of elements stored in the stack
    """
    
    def __init__(self, capacity: int = 4) -> None:
        """Initialize an empty stack.
        
        Args:
            capacity: Initial capacity of the stack (default: 4)
        """
        self.stack_array = MyArray[T](capacity)
    
    def push(self, value: T) -> None:
        """Push an element onto the stack.
        
        Args:
            value: The value to push
            
        Time Complexity:
            O(1) amortized
        """
        self.stack_array.append(value)
    
    def pop(self) -> T:
        """Pop the top element from the stack.
        
        Returns:
            The top element
            
        Raises:
            EmptyStackError: If the stack is empty
            
        Time Complexity:
            O(1) amortized
        """
        if self.is_empty():
            raise EmptyStackError("Cannot pop from empty stack")
        return self.stack_array.pop()
    
    def peek(self) -> T:
        """Get the top element without removing it.
        
        Returns:
            The top element
            
        Raises:
            EmptyStackError: If the stack is empty
            
        Time Complexity:
            O(1)
        """
        if self.is_empty():
            raise EmptyStackError("Cannot peek from empty stack")
        return self.stack_array[self.stack_array.length - 1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty.
        
        Returns:
            True if the stack is empty, False otherwise
            
        Time Complexity:
            O(1)
        """
        return self.stack_array.length == 0
    
    def size(self) -> int:
        """Get the number of elements in the stack.
        
        Returns:
            The current size of the stack
            
        Time Complexity:
            O(1)
        """
        return self.stack_array.length
    
    def reverse(self) -> None:
        """Reverse the stack in place.
        
        Time Complexity:
            O(n) where n is the number of elements
        """
        n = self.stack_array.length
        for i in range(n // 2):
            self.stack_array[i], self.stack_array[n - i - 1] = (
                self.stack_array[n - i - 1],
                self.stack_array[i],
            )
    
    def max(self) -> T:
        """Get the maximum value in the stack.
        
        Returns:
            The maximum value
            
        Raises:
            EmptyStackError: If the stack is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyStackError("Cannot get max from empty stack")
        return max(self.stack_array[i] for i in range(self.stack_array.length))
    
    def min(self) -> T:
        """Get the minimum value in the stack.
        
        Returns:
            The minimum value
            
        Raises:
            EmptyStackError: If the stack is empty
            
        Time Complexity:
            O(n) where n is the number of elements
        """
        if self.is_empty():
            raise EmptyStackError("Cannot get min from empty stack")
        return min(self.stack_array[i] for i in range(self.stack_array.length))
    
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the elements of the stack.
        
        Returns:
            An iterator yielding each element in the stack (top to bottom)
        """
        for i in reversed(range(self.stack_array.length)):
            yield self.stack_array[i]
    
    def __str__(self) -> str:
        """Return a string representation of the stack.
        
        Returns:
            A string showing the stack's contents (top to bottom)
        """
        if self.is_empty():
            return "Empty Stack"
        return "Stack(top -> bottom): [" + ", ".join(
            str(self.stack_array[i]) for i in reversed(range(self.stack_array.length))) + "]"


if __name__ == "__main__":
    def test_stack():
        """Test the stack implementation with various operations."""
        # Create a stack
        stack = MyStack[int]()
        print("Created empty stack")
        
        # Test push
        print("\nTesting push:")
        for i in [5, 10, 3, 7]:
            stack.push(i)
            print(f"Pushed {i}: {stack}")
        
        # Test peek
        print("\nTesting peek:")
        print(f"Top element: {stack.peek()}")
        
        # Test pop
        print("\nTesting pop:")
        print(f"Popped: {stack.pop()}")
        print(f"After pop: {stack}")
        
        # Test max and min
        print("\nTesting max and min:")
        print(f"Max: {stack.max()}")
        print(f"Min: {stack.min()}")
        
        # Test reverse
        print("\nTesting reverse:")
        stack.reverse()
        print(f"After reverse: {stack}")
        
        # Test iteration
        print("\nTesting iteration:")
        print("Elements (top to bottom):", end=" ")
        for x in stack:
            print(x, end=" ")
        print()
        
        # Test size and is_empty
        print("\nTesting size and is_empty:")
        print(f"Size: {stack.size()}")
        print(f"Is empty: {stack.is_empty()}")
        
        # Test error handling
        print("\nTesting error handling:")
        empty = MyStack[int]()
        try:
            empty.pop()  # Empty stack
        except EmptyStackError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.peek()  # Empty stack
        except EmptyStackError as e:
            print(f"Expected error: {e}")
        
        try:
            empty.max()  # Empty stack
        except EmptyStackError as e:
            print(f"Expected error: {e}")
        
        # Test type safety
        print("\nTesting type safety:")
        try:
            stack.push("string")  # Type error
        except TypeError as e:
            print(f"Expected error: {e}")
    
    test_stack()
