""" This module implements a simple queue using a dynamic array."""
from DataStructures.my_array import MyArray

class MyQueue:
    """ A queue data structure implemented using a dynamic array. """
    def __init__(self, capacity=4):
        self.queue_array = MyArray(capacity)
        self.front_index = 0

    def enqueue(self, value):
        """Adds an item to the end of the queue."""
        self.queue_array.append(value)

    def dequeue(self):
        """Removes the front item from the queue and returns it."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        value = self.queue_array[self.front_index]
        self.front_index += 1
        return value

    def peek(self):
        """Returns the front item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.queue_array[self.front_index]

    def is_empty(self):
        """ Checks if the queue is empty.
            Returns True if the queue is empty, otherwise False. """
        return self.front_index >= self.queue_array.length

    def size(self):
        """ Returns the number of items in the queue. """
        return self.queue_array.length - self.front_index

    def reverse(self):
        """ Reverses the queue in place. """
        left = self.front_index
        right = self.queue_array.length - 1
        while left < right:
            self.queue_array[left], self.queue_array[right] = (
                self.queue_array[right],
                self.queue_array[left],
            )
            left += 1
            right -= 1

    def max(self):
        """ Returns the maximum value in the queue. """
        if self.is_empty():
            raise ValueError("Max from empty queue")
        return max(self.queue_array[i] for i in range(self.front_index, self.queue_array.length))

    def min(self):
        """ Returns the minimum value in the queue. """
        if self.is_empty():
            raise ValueError("Min from empty queue")
        return min(self.queue_array[i] for i in range(self.front_index, self.queue_array.length))

    def __iter__(self):
        for i in range(self.front_index, self.queue_array.length):
            yield self.queue_array[i]


    def __str__(self):
        return "Queue(front -> back): [" + ", ".join(
            str(self.queue_array[i]) for i in range(self.front_index, self.queue_array.length)) + "]"


queue = MyQueue()
queue.enqueue(4)
queue.enqueue(1)
queue.enqueue(9)
queue.enqueue(2)

print(queue)  # Output (front -> back): [4, 1, 9, 2]
print("Peek:", queue.peek())  # 4
print("Max:", queue.max())    # 9
print("Min:", queue.min())    # 1

queue.reverse()
print("Reversed:", queue)  # Queue(front -> back): [2, 9, 1, 4]

print("For loop:")
for item in queue:
    print(item, end=" ")  # 2 9 1 4
