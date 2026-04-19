class ListNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def print_list(self):
        temp = self.head
        while temp:
            print(temp.item, end=" ")
            temp = temp.next
        print()

    def find_node(self, index):
        if index < 0 or index >= self.size:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

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

class Stack:
    def __init__(self):
        self.ll = LinkedList()

    def push(self, item):
        self.ll.insert_node(0, item)

    def pop(self):
        if self.is_empty():
            return None
        item = self.ll.head.item
        self.ll.remove_node(0)
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.ll.head.item

    def is_empty(self):
        return self.ll.size == 0

class Queue:
    def __init__(self):
        self.ll = LinkedList()

    def enqueue(self, item):
        self.ll.insert_node(self.ll.size, item)

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.ll.head.item
        self.ll.remove_node(0)
        return item

    def is_empty(self):
        return self.ll.size == 0

def palindrome(word):
    stack = Stack()
    queue = Queue()

    word = word.upper()
    for char in word:
        if char.isalnum():
            stack.push(char)
            queue.enqueue(char)

    while stack.ll.size > queue.ll.size:
        stack.pop()

    while not stack.is_empty():
        if stack.pop() != queue.dequeue():
            print("The string is not a palindrome")
            return False

    print("The string is a palindrome")
    return True

if __name__ == "__main__":
    print("Sample String : A man a plan a canal Panama")
    palindrome("A man a plan a canal Panama")
    print("Sample String : Superman in the sky")
    palindrome("Superman in the sky")