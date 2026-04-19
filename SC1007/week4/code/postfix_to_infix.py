# Define operator precedence globally
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
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

def postfix_to_infix(expression):
    """Convert postfix expression to infix - character by character processing"""
    stack = Stack()
    
    # Process the input character by character
    for char in expression:
        if char.isspace():
            continue
            
        if char not in PRECEDENCE:  # If char is an operand
            stack.push(char)
        else:  # If char is an operator
            if stack.size < 2:
                raise ValueError("Invalid postfix expression: not enough operands")
           
            op2 = stack.pop()
            op1 = stack.pop()
           
            # Create infix expression with parentheses and push to stack
            infix_expr = f"({op1} {char} {op2})"
            stack.push(infix_expr)
   
    if stack.size != 1:
        raise ValueError("Invalid postfix expression: too many operands")
   
    return stack.pop()

if __name__ == "__main__":
    exp = input("Enter postfix expression: ")
    try:
        infix = postfix_to_infix(exp)
        print(f"Infix expression: {infix}")
    except ValueError as e:
        print(f"Error: {e}")