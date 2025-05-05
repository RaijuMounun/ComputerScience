""" Low-level array implementation in Python using ctypes."""
import ctypes

class MyArray:
    """ A low-level array implementation using ctypes."""
    def __init__(self, capacity=2):
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
        """ Appends an item to the end of the array.
            If the array is full, doubles its size. """
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

    def insert(self, index, value):
        """ Inserts an item at a specific index."""
        if not 0 <= index <= self.length:
            raise IndexError("Index out of bounds")
        if self.length == self.capacity:
            self._resize()
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.length += 1

    def delete(self, index):
        """ Deletes an item at a specific index."""
        if not 0 <= index < self.length:
            raise IndexError("Index out of bounds")
        for i in range(index, self.length - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.length - 1] = None
        self.length -= 1

    def pop(self):
        """ Removes and returns the last item of the array."""
        if self.length == 0:
            raise IndexError("Pop from empty array")
        value = self.data[self.length - 1]
        self.data[self.length - 1] = None
        self.length -= 1
        return value

    def find(self, value):
        """ Finds and returns the index of the first occurrence of a value."""
        for i in range(self.length):
            if self.data[i] == value:
                return i
        return -1

    def clear(self):
        """ Clears the array. """
        self.data = self._make_array(self.capacity)
        self.length = 0

    def contains(self, value):
        """ Checks if the array contains a value.
            Returns True if the value is found, otherwise False. """
        return self.find(value) != -1

    def __iter__(self):
        for i in range(self.length):
            yield self.data[i]

    def __repr__(self):
        return f"LowLevelArray([{', '.join(str(self.data[i]) for i in range(self.length))}])"


    def __str__(self):
        return "[" + ", ".join(str(self.data[i]) for i in range(self.length)) + "]"


# Example usage:
if __name__ == "__main__":
    my_array = MyArray(5)
    my_array.append(1)
    my_array.append(2)
    my_array.append(3)
    my_array.append(4)
    my_array.append(5)
    print(my_array)  # Output: [1, 2, 3, 4, 5]
    my_array.insert(2, 10)
    print(my_array)  # Output: [1, 2, 10, 3, 4, 5]
    my_array.delete(3)
    print(my_array)  # Output: [1, 2, 10, 4, 5]
    print(my_array.pop())  # Output: 5
    print(my_array)  # Output: [1, 2, 10, 4]
    print(my_array.find(10))  # Output: 2
    print(my_array.contains(3))  # Output: False
    my_array.clear()
    print(my_array)  # Output: []
