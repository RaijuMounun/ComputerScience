""" This module implements a MinHeap using a dynamic array.
    Heap is a binary tree used to implement a priority queue. """
from DataStructures.my_array import MyArray


class MyHeap:
    """ Base heap class. """

    def __init__(self):
        self.data = MyArray()

    def _parent(self, index):
        return (index - 1) // 2

    def _left(self, index):
        return 2 * index + 1

    def _right(self, index):
        return 2 * index + 2

    def insert(self, value):
        """Insert a new value into the heap."""
        self.data.append(value)
        self._heapify_up(self.data.length - 1)

    def _heapify_up(self, index):
        pass  # To be implemented in subclasses

    def _heapify_down(self, index):
        pass  # To be implemented in subclasses

    def peek(self):
        """Return the smallest element without removing it."""
        if self.data.length == 0:
            raise IndexError("peek from empty heap")
        return self.data[0]

    def __str__(self):
        return "Heap: [" + ", ".join(str(self.data[i]) for i in range(self.data.length)) + "]"


class MyMinHeap(MyHeap):
    """A binary min heap data structure implemented using an array."""

    def _heapify_up(self, index):
        while index > 0 and self.data[index] < self.data[self._parent(index)]:
            self.data[index], self.data[self._parent(
                index)] = self.data[self._parent(index)], self.data[index]
            index = self._parent(index)

    def extract_min(self):
        """Remove and return the smallest element in the heap."""
        if self.data.length == 0:
            raise IndexError("extract_min from empty heap")
        root = self.data[0]
        last = self.data.pop()
        if self.data.length > 0:
            self.data[0] = last
            self._heapify_down(0)
        return root

    def _heapify_down(self, index):
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


class MyMaxHeap(MyHeap):
    """A binary max heap data structure implemented using an array."""

    def _heapify_up(self, index):
        while index > 0 and self.data[index] > self.data[self._parent(index)]:
            self.data[index], self.data[self._parent(
                index)] = self.data[self._parent(index)], self.data[index]
            index = self._parent(index)

    def extract_max(self):
        """Remove and return the largest element in the heap."""
        if self.data.length == 0:
            raise IndexError("extract_max from empty heap")
        root = self.data[0]
        last = self.data.pop()
        if self.data.length > 0:
            self.data[0] = last
            self._heapify_down(0)
        return root

    def _heapify_down(self, index):
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


print("=== MinHeap Test ===")
min_heap = MyMinHeap()
min_heap.insert(10)
min_heap.insert(4)
min_heap.insert(15)
min_heap.insert(2)
print(min_heap)                # Heap: [2, 4, 15, 10]
print("Peek:", min_heap.peek())  # 2
print("Extract Min:", min_heap.extract_min())  # 2
print(min_heap)                # Heap: [4, 10, 15]

print("\n=== MaxHeap Test ===")
max_heap = MyMaxHeap()
max_heap.insert(10)
max_heap.insert(4)
max_heap.insert(15)
max_heap.insert(2)
print(max_heap)                # Heap: [15, 10, 4, 2]
print("Peek:", max_heap.peek())  # 15
print("Extract Max:", max_heap.extract_max())  # 15
print(max_heap)                # Heap: [10, 2, 4]
