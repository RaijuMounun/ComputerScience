""" This module implements a doubly linked list with basic operations. """

class DoublyNode:
    """ Node class for Doubly Linked List """
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class MyDoublyLinkedList:
    """ Doubly Linked List class.
        Implements a doubly linked list with basic operations """
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, value):
        """ Appends an item to the end of the doubly linked list."""
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def prepend(self, value):
        """ Prepends an item to the start of the doubly linked list.
            If the list is empty, it sets the head and tail to the new node."""
        new_node = DoublyNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def delete(self, value):
        """ Deletes the first occurrence of an item from the doubly linked list."""
        current = self.head
        while current:
            if current.value == value:
                if current.prev:  # Orta ya da son
                    current.prev.next = current.next
                else:  # Head
                    self.head = current.next
                if current.next:  # Orta ya da baş
                    current.next.prev = current.prev
                else:  # Tail
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def reverse(self):
        """ Reverses the doubly linked list in place."""
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

    def to_list_forward(self):
        """ Converts the doubly linked list to a Python list in forward order."""
        current = self.head
        result = []
        while current:
            result.append(current.value)
            current = current.next
        return result

    def to_list_backward(self):
        """ Converts the doubly linked list to a Python list in backward order."""
        current = self.tail
        result = []
        while current:
            result.append(current.value)
            current = current.prev
        return result

    def insert_at(self, index, value):
        """ Inserts an item at a specific index in the doubly linked list."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        new_node = DoublyNode(value)
        if index == 0:
            self.prepend(value)
        elif index == self._size:
            self.append(value)
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node
            self._size += 1

    def find(self, value):
        """ Finds the first occurrence of an item in the doubly linked list.
            Returns the index of the item if found, otherwise -1. """
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def size(self):
        """ Returns the number of items in the doubly linked list. """
        return self._size

    def is_empty(self):
        """ Checks if the doubly linked list is empty.
            Returns True if the list is empty, otherwise False. """
        return self._size == 0

    def __iter__(self):
        """ Returns an iterator for the doubly linked list."""
        current = self.head
        while current:
            yield current.value
            current = current.next


    def __str__(self):
        return " <-> ".join(str(v) for v in self.to_list_forward()) + " <-> None"


# Example usage
my_doubly_linked_list = MyDoublyLinkedList()
my_doubly_linked_list.append(10)
my_doubly_linked_list.append(20)
my_doubly_linked_list.append(30)
print("Forward:", my_doubly_linked_list)  # 10 <-> 20 <-> 30 <-> None
print("Backward:", my_doubly_linked_list.to_list_backward())  # [30, 20, 10]
my_doubly_linked_list.prepend(5)
print("Prepend:", my_doubly_linked_list)  # 5 <-> 10 <-> 20 <-> 30 <-> None
my_doubly_linked_list.delete(20)
print("20 is deleted:", my_doubly_linked_list)  # 5 <-> 10 <-> 30 <-> None
my_doubly_linked_list.reverse()
print("Reverted:", my_doubly_linked_list)  # 30 <-> 10 <-> 5 <-> None
