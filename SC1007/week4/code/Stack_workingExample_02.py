class ListNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def find_node(self, index):
        if index < 0 or index >= self.size:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

    def remove_node(self, index):
        if index < 0 or index >= self.size:
            return -1
        if index == 0:
            self.head = self.head.next
            if self.size == 1:
                self.tail = None
        else:
            prev = self.find_node(index - 1)
            prev.next = prev.next.next
            if index == self.size - 1:
                self.tail = prev
        self.size -= 1
        return 0

    def insert_node(self, index, value):
        if index < 0 or index > self.size:
            return -1
        new_node = ListNode(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        elif index == self.size:
            self.tail.next = new_node
            self.tail = new_node
        else:
            prev = self.find_node(index - 1)
            new_node.next = prev.next
            prev.next = new_node
        self.size += 1
        return 0

class Stack:
    def __init__(self):
        self.ll = LinkedList()

    def push(self, item):
        self.ll.insert_node(0, item)

    def pop(self):
        if self.isEmpty():
            return None
        item = self.ll.head.item
        self.ll.remove_node(0)
        return item

    def peek(self):
        if self.isEmpty():
            return None
        return self.ll.head.item

    def isEmpty(self):
        return self.ll.size == 0
    
    def get_size(self):
        return self.ll.size

if __name__ == "__main__":
    s = Stack()  # Create a new stack
    
    s.push(10)   # Push some elements: 10, 20, and 30
    s.push(20)
    s.push(30)
    
    print("Size:", s.get_size())      # Print the size. Should print 3
    
    print("Top element:", s.peek())   # Print top element. Should print 30
    
    print("Popped:", s.pop())         # Should print 30
    print("Popped:", s.pop())         # Should print 20
    
    print("New size:", s.get_size())  # Print new size. Should print 1
    
    print("New top element:", s.peek()) # Print new top element. Should print 10
    
    print("Is stack empty?", s.isEmpty()) # Check if empty. Should print False
    
    print("Popped:", s.pop())         # Pop last element. Should print 10
    
    print("Is stack empty now?", s.isEmpty()) # Check if empty again. Should print True