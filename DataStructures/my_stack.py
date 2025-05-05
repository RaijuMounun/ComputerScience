""" This module implements a stack data structure using a dynamic array. """
from DataStructures.my_array import MyArray


class MyStack:
    """ A stack data structure implemented using a dynamic array. """

    def __init__(self, capacity=4):
        self.stack_array = MyArray(capacity)

    def push(self, value):
        """ Pushes an item onto the stack. """
        self.stack_array.append(value)

    def pop(self):
        """ Pops the top item off the stack and returns it. """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.stack_array.pop()

    def peek(self):
        """ Returns the top item of the stack without removing it. """
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.stack_array[self.stack_array.length - 1]

    def is_empty(self):
        """ Checks if the stack is empty.
            Returns True if the stack is empty, otherwise False. """
        return self.stack_array.length == 0

    def size(self):
        """ Returns the number of items in the stack. """
        return self.stack_array.length

    def reverse(self):
        """Reverses the stack in place."""
        n = self.stack_array.length
        for i in range(n // 2):
            self.stack_array[i], self.stack_array[n - i - 1] = (
                self.stack_array[n - i - 1],
                self.stack_array[i],
            )

    def max(self):
        """Returns the maximum value in the stack."""
        if self.is_empty():
            raise ValueError("Max from empty stack")
        return max(self.stack_array[i] for i in range(self.stack_array.length))

    def min(self):
        """Returns the minimum value in the stack."""
        if self.is_empty():
            raise ValueError("Min from empty stack")
        return min(self.stack_array[i] for i in range(self.stack_array.length))

    def __iter__(self):
        for i in reversed(range(self.stack_array.length)):
            yield self.stack_array[i]

    def __str__(self):
        return "Stack(top -> bottom): [" + ", ".join(
            str(self.stack_array[i]) for i in reversed(range(self.stack_array.length))) + "]"



# Example usage:
stack = MyStack()
stack.push(5)
stack.push(10)
stack.push(3)
stack.push(7)
print(stack)  # Stack(top -> bottom): [7, 3, 10, 5]
print("Peek:", stack.peek())  # 7
print("Pop:", stack.pop())  # 7
print("After Pop:", stack)  # Stack(top -> bottom): [3, 10, 5]
print("Max:", stack.max())  # 10
print("Min:", stack.min())  # 3
stack.reverse()
print("After Reverse:", stack)  # Stack(top -> bottom): [5, 10, 3]
print("For Loop:")
for item in stack:
    print(item, end=" ")  # 5 10 3
print("\nStack Size:", stack.size())      # 3
print("Is Empty:", stack.is_empty())      # False
stack.pop()
stack.pop()
stack.pop()
print("Empty After All Pops:", stack.is_empty())  # True
