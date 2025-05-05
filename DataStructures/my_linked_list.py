""" Linked List Module """

class Node:
    """ Node class for Linked List """
    def __init__(self, value):
        self.value = value
        self.next = None


class MyLinkedList:
    """ Linked List class
        Implements a singly linked list with basic operations """
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, value):
        """ Appends an item to the end of the linked list.
            If the list is empty, it sets the head and tail to the new node.
            Otherwise, it adds the new node to the end and updates the tail. """
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, value):
        """ Prepends an item to the start of the linked list.
            If the list is empty, it sets the head and tail to the new node."""
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def delete(self, value):
        """ Deletes the first occurrence of an item from the linked list.
            If the item is found, it updates the head or tail accordingly. """
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
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

    def find(self, value):
        """ Finds the first occurrence of an item in the linked list.
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
        """ Returns the number of items in the linked list. """
        return self._size

    def is_empty(self):
        """ Checks if the linked list is empty.
            Returns True if the list is empty, otherwise False. """
        return self._size == 0

    def reverse(self):
        """ Reverses the linked list in place. """
        prev = None
        current = self.head
        self.tail = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def insert_at(self, index, value):
        """ Inserts an item at a specific index in the linked list.
            If the index is out of bounds, it does nothing. """
        if index < 0 or index > self._size:
            return
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

    def remove_at(self, index):
        """ Removes an item at a specific index from the linked list.
            If the index is out of bounds, it does nothing. """
        if index < 0 or index >= self._size:
            return
        if index == 0:
            self.delete(self.head.value)
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next
        current.next = current.next.next
        if current.next is None:
            self.tail = current
        self._size -= 1

    def __str__(self):
        """ Returns a string representation of the linked list. """
        current = self.head
        result = []
        while current:
            result.append(str(current.value))
            current = current.next
        return " -> ".join(result) + " -> None"


my_linked_list = MyLinkedList()
my_linked_list.append(1)
my_linked_list.append(2)
my_linked_list.append(3)
print("List:", my_linked_list)  # 1 -> 2 -> 3 -> None
my_linked_list.prepend(0)
print("After prepend:", my_linked_list)  # 0 -> 1 -> 2 -> 3 -> None
my_linked_list.delete(2)
print("2 is deleted:", my_linked_list)  # 0 -> 1 -> 3 -> None
print("Where is 3?:", my_linked_list.find(3))  # 2
print("Size:", my_linked_list.size())  # 3
my_linked_list.reverse()
print("Reverted:", my_linked_list)  # 3 -> 1 -> 0 -> None
