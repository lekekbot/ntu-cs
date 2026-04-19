pi = 3.14159  # Global variable with value shown in heap

# STACK SEGMENT
x = 42        # Local variable pointing to 42 in heap
text = "hello"
list1 = [1, 2, 3]  # Local variable pointing to list in heap

print(f"x at memory location: {id(x)}")  # Will show something like 0x1234
print(f"list1 at memory location: {id(list1)}")  # Will show something like 0x5678
print(f"pi at memory location: {id(pi)}")  # Will show something like 0x9999