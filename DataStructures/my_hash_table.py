""" This module implements a hash table using linear probing.
    Linear probing is a collision resolution technique in open addressing.
    It is used to resolve collisions in hash tables by finding the next available slot. """
from DataStructures.my_array import MyArray

class HashTableEntry:
    """ Class representing a single entry in the hash table. """
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    """ A hash table implementation using linear probing for collision resolution. """
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.table = MyArray(capacity)
        for _ in range(capacity):
            self.table.append(None)

    def _hash(self, key):
        """Custom hash function for strings (Polynomial rolling hash)."""
        hash_value = 0
        p = 31
        m = self.capacity
        for i, char in enumerate(str(key)):
            hash_value += (ord(char) * (p ** i)) % m
        return hash_value % m

    def _probe(self, index):
        """Linear probing generator."""
        while True:
            yield index
            index = (index + 1) % self.capacity

    def put(self, key, value):
        """ Insert a key-value pair into the hash table. """
        if self.size >= self.capacity * 0.7:
            self._resize()

        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None or self.table[i].key == key:
                if self.table[i] is None:
                    self.size += 1
                self.table[i] = HashTableEntry(key, value)
                return

    def get(self, key):
        """ Retrieve a value by its key. """
        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None:
                raise KeyError(f"Key '{key}' not found.")
            if self.table[i].key == key:
                return self.table[i].value

    def remove(self, key):
        """ Remove a key-value pair from the hash table. """
        index = self._hash(key)
        for i in self._probe(index):
            if self.table[i] is None:
                raise KeyError(f"Key '{key}' not found.")
            if self.table[i].key == key:
                self.table[i] = None
                self.size -= 1
                return

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = MyArray(self.capacity)
        for _ in range(self.capacity):
            self.table.append(None)
        for item in old_table:
            if item is not None:
                self.put(item.key, item.value)

    def __str__(self):
        items = [f"{entry.key}: {entry.value}" for entry in self.table if entry is not None]
        return "{" + ", ".join(items) + "}"
