""" Low-level array implementation in Python using ctypes."""
import ctypes

class MyArray:
    """ A low-level array implementation using ctypes."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.length = 0
        self.data = self._make_array(capacity)

    def _make_array(self, size):
        return (size * ctypes.py_object)()          # int *array = malloc(sizeof(int) * capacity); in C

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if 0 <= index < self.length:
            return self.data[index]
        raise IndexError("Index out of bounds")

    def __setitem__(self, index, value):
        if 0 <= index < self.length:
            self.data[index] = value
        else:
            raise IndexError("Index out of bounds")

    def append(self, value):
        """ Append an item to the end of the array.
            If the array is full, double its size. """
        if self.length == self.capacity:
            self._resize()
        self.data[self.length] = value
        self.length += 1

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = self._make_array(new_capacity)
        for i in range(self.length):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def __str__(self):
        return "[" + ", ".join(str(self.data[i]) for i in range(self.length)) + "]"



# Example usage:
my_array = MyArray(2)
my_array.append(23)
my_array.append(19)
print(my_array)            # Outputs [23, 19]
my_array.append(99)
print(my_array[2])         # Outputs 99
my_array[1] = 30
print(my_array)            # Outputs [23, 30, 99]
