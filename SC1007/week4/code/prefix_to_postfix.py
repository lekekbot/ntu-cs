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
        if self.is_empty():
            return None
        else:
            return self.top.data
   
    def is_empty(self):
        return self.size == 0

def prefix_to_postfix(expression):
    """Convert prefix expression to postfix - reading from right to left"""
    stack = Stack()
    
    # Process the input from right to left for prefix conversion
    for char in reversed(expression):
        if char.isspace():
            continue
            
        if char not in PRECEDENCE:  # If char is an operand
            stack.push(char)
        else:  # If char is an operator
            if stack.size < 2:
                raise ValueError("Invalid prefix expression: not enough operands")
           
            op1 = stack.pop()
            op2 = stack.pop()
           
            # Create postfix expression and push to stack
            postfix_expr = f"{op1}{op2}{char}"
            stack.push(postfix_expr)
   
    if stack.size != 1:
        raise ValueError("Invalid prefix expression: too many operands")
   
    return stack.pop()

if __name__ == "__main__":
    exp = input("Enter prefix expression: ")
    try:
        postfix = prefix_to_postfix(exp)
        print(f"Postfix expression: {postfix}")
    except ValueError as e:
        print(f"Error: {e}")