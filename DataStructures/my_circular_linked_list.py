""" This is a simple implementation of a circular linked list in Python. """

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class MyCircularLinkedList:
    """ Circular Linked List class.
        Implements a circular linked list with basic operations. """
    def __init__(self):
        self.sentinel = Node()  # Sentinel node (valueless)
        self.sentinel.next = self.sentinel  # Points to itself
        self._size = 0
        self._iter_node = None  # For iteration

    def append(self, value):
        """ Appends an item to the end of the circular linked list. """
        new_node = Node(value)
        current = self.sentinel
        while current.next != self.sentinel:
            current = current.next
        current.next = new_node
        new_node.next = self.sentinel
        self._size += 1

    def prepend(self, value):
        """ Prepends an item to the start of the circular linked list.
            If the list is empty, it sets the head and tail to the new node. """
        new_node = Node(value)
        new_node.next = self.sentinel.next
        self.sentinel.next = new_node
        self._size += 1

    def delete(self, value):
        """ Deletes the first occurrence of an item from the circular linked list. """
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

    def reverse(self):
        """ Reverses the circular linked list. """
        prev = self.sentinel
        current = self.sentinel.next
        while current != self.sentinel:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.sentinel.next = prev

    def kth_from_end(self, k):
        """ Returns the k-th element from the end of the circular linked list. """
        if k <= 0 or k > self._size:
            raise IndexError("Invalid k")

        slow = self.sentinel.next
        fast = self.sentinel.next
        for _ in range(k):
            fast = fast.next
        while fast != self.sentinel:
            slow = slow.next
            fast = fast.next
        return slow.value

    def find_middle(self):
        """ Returns the middle element of the circular linked list.
            If the list has an even number of elements, returns the second middle element. """
        slow = self.sentinel.next
        fast = self.sentinel.next
        while fast != self.sentinel and fast.next != self.sentinel:
            slow = slow.next
            fast = fast.next.next
        return slow.value

    def split(self):
        """ Splits the circular linked list into two halves.
            Returns two new circular linked lists. """
        if self._size < 2:
            raise ValueError("Liste bölünecek kadar büyük değil.")

        mid_index = self._size // 2
        first_half = MyCircularLinkedList()
        second_half = MyCircularLinkedList()

        current = self.sentinel.next
        for _ in range(mid_index):
            first_half.append(current.value)
            current = current.next
        for _ in range(self._size - mid_index):
            second_half.append(current.value)
            current = current.next

        return first_half, second_half

    def rotate(self, k):
        """Listeyi k adım sola döndürür (başlangıç düğümünü değiştirir)."""
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

    def copy_deep(self):
        """ Creates a deep copy of the circular linked list.
            Returns a new circular linked list with the same elements. """
        new_list = MyCircularLinkedList()
        for value in self:
            new_list.append(value)
        return new_list


    def __iter__(self):
        """ Iterator for the circular linked list """
        self._iter_node = self.sentinel.next
        return self

    def __next__(self):
        if self._iter_node == self.sentinel:
            raise StopIteration
        value = self._iter_node.value
        self._iter_node = self._iter_node.next
        return value

    def __len__(self):
        return self._size

    def __str__(self):
        return " -> ".join(str(val) for val in self) + " -> (head)"


# Example usage
my_circular_linked_list = MyCircularLinkedList()
for val in [10, 20, 30, 40, 50]:
    my_circular_linked_list.append(val)

print("Original:", my_circular_linked_list)
print("Middle:", my_circular_linked_list.find_middle())  # 30
print("2nd element from the end :", my_circular_linked_list.kth_from_end(2))  # 40

my_circular_linked_list.reverse()
print("Reverted:", my_circular_linked_list)

first, second = my_circular_linked_list.split()
print("First half:", first)
print("Second half:", second)

my_circular_linked_list.rotate(2)
print("Rotated 2 times:", my_circular_linked_list)

copy = my_circular_linked_list.copy_deep()
print("Copy:", copy)
