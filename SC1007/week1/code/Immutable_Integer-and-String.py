# Integer immutability
x = 42 
y = x
print(f"Before: x = {x}, y = {y}")
print(f"Before: id(x) = {id(x)}, id(y) = {id(y)}")

x += 1  # x becomes 43, y stays 42
print(f"\nAfter: x = {x}, y = {y}")
print(f"After: id(x) = {id(x)}, id(y) = {id(y)}")

# String immutability
print("\n" + "-" * 20 + "\n")

s1 = "hello"
s2 = "hello"
print(f"Initially both strings same: id(s1) = {id(s1)}, id(s2) = {id(s2)}")

s1 = "hello!"  # Creates new string
print(f"After change: id(s1) = {id(s1)}, id(s2) = {id(s2)}")