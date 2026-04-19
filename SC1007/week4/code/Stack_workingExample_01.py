class Node:     
    def __init__(self, data):         
        self.data = data
        self.next = None

class Stack:     
    def __init__(self):         
        self.top = None
        self.size = 0
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek: Empty stack")
        return self.top.data
    
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop: Empty stack")
        popped_node = self.top
        self.top = self.top.next
        self.size -= 1
        return popped_node.data
    
    def is_empty(self):
        return self.top is None
    
    def get_size(self):
        return self.size

if __name__ == "__main__":
    s = Stack() # Create a new stack
    
    s.push(10) # Push some elements: 10, 20, and 30
    s.push(20)
    s.push(30)
    
    print("Size:", s.get_size())    # Print the size. Should print 3
    
    print("Top element:", s.peek())  # Print top element. Should print 30
    
    print("Popped:", s.pop())       # Should print 30
    print("Popped:", s.pop())       # Should print 20
    
    print("New size:", s.get_size()) # Print new size. Should print 1
    
    print("New top element:", s.peek()) # Print new top element. Should print 10
    
    print("Is stack empty?", s.is_empty()) # Check if empty. Should print False
    
    print("Popped:", s.pop())       # Pop last element. Should print 10
    
    print("Is stack empty now?", s.is_empty()) # Check if empty again. Should print True