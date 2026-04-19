# Define operator precedence globally
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

class Node:
    """Defines a node for a linked list-based stack"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    """Implements a stack using a linked list"""
    def __init__(self):
        self.top = None
        self.size = 0
       
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
       
    def pop(self):
        if self.is_empty():
            return None
        popped = self.top.data
        self.top = self.top.next
        self.size -= 1
        return popped
       
    def peek(self):
        return None if self.is_empty() else self.top.data
       
    def is_empty(self):
        return self.size == 0

def is_operator(char):
    """Check if the character is an operator"""
    return char in PRECEDENCE

def prefix_to_infix(expression):
    """Convert prefix expression to infix"""
    stack = Stack()
    
    # Iterate through the expression in reverse order
    for char in reversed(expression.strip()):
        if char.isspace():
            continue
        
        if not is_operator(char):
            stack.push(char)
        else:
            if stack.size < 2:
                raise ValueError("Invalid prefix expression")
            
            operand1 = stack.pop()
            operand2 = stack.pop()
            
            # Create infix expression and push to stack
            infix = f"({operand1} {char} {operand2})"
            stack.push(infix)
    
    if stack.size != 1:
        raise ValueError("Invalid prefix expression")
    
    return stack.pop()

# Test the function
if __name__ == "__main__":
    prefix_exp = input("Enter a prefix expression: ")
    try:
        infix_exp = prefix_to_infix(prefix_exp)
        print(f"Infix expression: {infix_exp}")
    except ValueError as e:
        print(f"Error: {e}")