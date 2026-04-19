# Import sys module to access system-specific functions
import sys                   

x = [1, 2, 3]   

# Print current reference count minus 1 (to account for getrefcount's temporary reference)
print(f"After creating x: {sys.getrefcount(x) - 1} reference(s)")  

y = x                       # Create second reference 'y' pointing to same list object
print(f"After creating y: {sys.getrefcount(x) - 1} reference(s)")  # Print updated reference count with two references

z = x                       # Create third reference 'z' pointing to same list object  
print(f"After creating z: {sys.getrefcount(x) - 1} reference(s)")  # Print reference count now showing three references

del x                       # Delete first reference 'x', reducing reference count by 1
print(f"After deleting x: {sys.getrefcount(y) - 1} reference(s)")  # Print reference count showing two remaining references

del y                       # Delete second reference 'y', reducing count further
print(f"After deleting y: {sys.getrefcount(z) - 1} reference(s)")  # Print reference count showing one final reference

del z                       # Delete final reference 'z', object now has no references

# Cannot print count here as no references exist to check   # Object now eligible for garbage collection since reference count is 0
# Cannot print reference count here because:
# 1. After del z, we have no variable name to reference the object
# 2. sys.getrefcount() needs a reference to an object to check its count
# 3. The object [1, 2, 3] is now eligible for garbage collection since no references exist
# print(sys.getrefcount(z)) would raise a NameError: name 'z' is not defined