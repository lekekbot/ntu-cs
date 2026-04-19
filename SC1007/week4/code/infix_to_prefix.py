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

def is_operand(char):
    return char.isalnum()

def has_higher_precedence(op1, op2, precedence=PRECEDENCE):
    return precedence.get(op1, 0) >= precedence.get(op2, 0)

def infix_to_prefix(expression):
    # Reverse the expression (with special handling for parentheses)
    reversed_exp = ""
    for char in reversed(expression):
        if char == '(':
            reversed_exp += ')'
        elif char == ')':
            reversed_exp += '('
        else:
            reversed_exp += char
    
    # Apply the modified infix to postfix algorithm
    output = ""
    operator_stack = Stack()
    
    i = 0
    while i < len(reversed_exp):
        char = reversed_exp[i]
        
        if char.isspace():
            i += 1
            continue
            
        if char.isalnum():
            if char.isalpha():
                output += char
            else:
                number = ""
                while i < len(reversed_exp) and reversed_exp[i].isdigit():
                    number += reversed_exp[i]
                    i += 1
                output += number
                i -= 1
        elif char == '(':
            operator_stack.push(char)
        elif char == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                output += operator_stack.pop()
            
            if not operator_stack.is_empty() and operator_stack.peek() == '(':
                operator_stack.pop()
        elif char in PRECEDENCE:
            while (not operator_stack.is_empty() and 
                   operator_stack.peek() != '(' and
                   has_higher_precedence(operator_stack.peek(), char)):
                output += operator_stack.pop()
            
            operator_stack.push(char)
        
        i += 1
    
    while not operator_stack.is_empty():
        output += operator_stack.pop()
    
    # Reverse the output to get the prefix expression
    prefix = output[::-1]
    return prefix

if __name__ == "__main__":
    exp = input("Enter infix expression: ")
    prefix = infix_to_prefix(exp)
    print(f"Prefix expression: {prefix}")