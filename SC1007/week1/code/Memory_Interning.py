# Memory Interning Example
import sys

# Demonstrate automatic vs manual string interning
print("Without Manual Interning:")
# Longer strings - Python doesn't automatically intern them
c = "hello world!"
d = "hello world!"

print(f"Memory location of c: {id(c)}")  # First memory location
print(f"Memory location of d: {id(d)}")  # Different memory location
print(f"Are c and d the same object? {c is d}")  # False - different objects
print(f"Do c and d have same value? {c == d}")   # True - same value, different objects

print("\nWith Manual Interning using sys.intern():")
# Manually intern longer strings to force memory sharing
e = sys.intern("hello world!")
f = sys.intern("hello world!")

print(f"Memory location of e: {id(e)}")  # First memory location
print(f"Memory location of f: {id(f)}")  # Same memory location as e
print(f"Are e and f the same object? {e is f}")  # True - same object due to interning
print(f"Do e and f have same value? {e == f}")   # True - same value