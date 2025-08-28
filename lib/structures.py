# lib/structures.py
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add(self, data):
        node = Node(data)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
    
    def move_to_end(self, node):
        if node == self.tail:
            return
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node
    
    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return current
            current = current.next
        return None
    
    def sort(self):
        # Simple bubble sort for demonstration
        current = self.head
        while current:
            next_node = current.next
            while next_node:
                if current.data > next_node.data:
                    current.data, next_node.data = next_node.data, current.data
                next_node = next_node.next
            current = current.next

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class GrammarTree:
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
            return
        current = self.root
        while True:
            if data < current.data:
                if current.left:
                    current = current.left
                else:
                    current.left = TreeNode(data)
                    break
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = TreeNode(data)
                    break
    
    def traverse_in_order(self, node):
        if node:
            self.traverse_in_order(node.left)
            print(node.data)
            self.traverse_in_order(node.right)