# Define operator precedence globally
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

class Node:
    def __init__(self, data):
        # Initialize a node with data and null next pointer
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        # Initialize an empty stack with no elements
        self.top = None
        self.size = 0
    
    def push(self, data):
        # Add a new element to the top of the stack
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        # Remove and return the top element of the stack
        if self.is_empty():
            return None
        popped = self.top.data
        self.top = self.top.next
        self.size -= 1
        return popped
    
    def peek(self):
        # Return the top element without removing it
        return None if self.is_empty() else self.top.data
    
    def is_empty(self):
        # Check if the stack has no elements
        return self.size == 0

def is_operand(char):
    # Check if a character is a letter or digit
    return char.isalnum()

def has_higher_precedence(op1, op2, precedence=PRECEDENCE):
    # Compare precedence of two operators using the global precedence
    return precedence.get(op1, 0) >= precedence.get(op2, 0)

def infix_to_postfix(expression):
    output = ""
    operator_stack = Stack()
    
    i = 0
    while i < len(expression):
        char = expression[i]
        
        # Handle multi-digit numbers
        if char.isdigit():
            number = ""
            while i < len(expression) and expression[i].isdigit():
                number += expression[i]
                i += 1
            output += number + " " 
            i -= 1  
        elif char == '(':
            operator_stack.push(char)
        elif char == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                output += operator_stack.pop() + " "
            
            if not operator_stack.is_empty() and operator_stack.peek() == '(':
                operator_stack.pop()
        elif char in PRECEDENCE:  # Check if character is an operator
            while (not operator_stack.is_empty() and 
                   operator_stack.peek() != '(' and
                   has_higher_precedence(operator_stack.peek(), char)):
                output += operator_stack.pop() + " "
            
            operator_stack.push(char)
        
        i += 1
    
    while not operator_stack.is_empty():
        output += operator_stack.pop() + " "
    
    return output.strip()

def evaluate_postfix(postfix):
    stack = Stack()
    tokens = postfix.split()
    
    for token in tokens:
        if token.isdigit():
            stack.push(int(token))
        else:
            val2 = stack.pop()
            val1 = stack.pop()
            if token == '+':
                stack.push(val1 + val2)
            elif token == '-':
                stack.push(val1 - val2)
            elif token == '*':
                stack.push(val1 * val2)
            elif token == '/':
                stack.push(val1 / val2)
            elif token == '^':
                stack.push(val1 ** val2)
    
    return stack.pop()

if __name__ == "__main__":
    # Main program entry point for user interaction
    exp = input("Enter infix expression: ")
    postfix = infix_to_postfix(exp)
    print(f"Postfix expression: {postfix}")
    try:
        result = evaluate_postfix(postfix)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        print("Make sure the expression contains valid numbers and operators.")