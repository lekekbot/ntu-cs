import weakref
import sys  # To check the reference count

def my_function():
    return "Hello"

# Check the reference count before creating a weak reference
print(f"Reference count Before: {sys.getrefcount(my_function) - 1}")

# Create a weak reference to the function
weak_ref = weakref.ref(my_function)

# Check the reference count after creating a weak reference
print(f"Reference count after: {sys.getrefcount(my_function) - 1}")

# Access the function through the weak reference and call it
print(f"Accessing function through weak reference: {weak_ref()()}")  # Prints: Hello

# Delete the original reference to the function
del my_function

# Check the weak reference after the original function is deleted
print(f"Weak reference after deletion: {weak_ref()}")  # Prints: None
