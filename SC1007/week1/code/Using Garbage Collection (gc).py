# Import garbage collector module
import gc

# Disable automatic garbage collection
gc.disable()
print("Automatic garbage collection disabled.")

# Create objects with circular references
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list1.append(list2)  # list1 references list2
list2.append(list1)  # list2 references list1

# Remove references
del list1  # Reference count doesn't reach 0
del list2  # Due to circular reference

# Manually trigger garbage collection
gc.collect()  # Cleans up circular references
print("Garbage collection manually triggered and circular references cleaned up.")

# Re-enable automatic garbage collection
gc.enable()
print("Automatic garbage collection re-enabled.")