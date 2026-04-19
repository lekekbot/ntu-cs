# Memory Pooling Example
print("Integer Memory Pooling:")
# Python reuses integers between -5 and 256
a = 100
b = 100
print(f"a = {a}, b = {b}")
print(f"Are a and b same object? {a is b}")  # True - same object reused
print(f"Memory location of a: {id(a)}")
print(f"Memory location of b: {id(b)}")  # Same as a's location

print("\nString Memory Pooling (String Interning):")
# Python interns (reuses) short strings
str1 = "hello"
str2 = "hello"
print(f"str1 = {str1}, str2 = {str2}")
print(f"Are str1 and str2 same object? {str1 is str2}")  # True - same string reused
print(f"Memory location of str1: {id(str1)}")
print(f"Memory location of str2: {id(str2)}")  # Same as str1's location

# Counter examples (no pooling)
print("\nNo Pooling Examples:")
# Large integers aren't pooled
x = 257
y = 257
print(f"x = {y}, y = {y}")
print(f"Are large integers (257) pooled? {x is y}")  # False - separate objects

# Long or complex strings aren't automatically pooled
str3 = "hello world!"
str4 = "hello world!"
print(f"str3 = {str3}, str4 = {str4}")
print(f"Are longer strings pooled? {str3 is str4}")  # False - separate objects