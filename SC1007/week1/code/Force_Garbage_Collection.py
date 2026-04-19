# Import garbage collector module for manual collection
import gc

print("Initial garbage count:", gc.get_count())  
# Shows (gen0, gen1, gen2) counts before creating lists

# Create two lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
print("\nAfter creating lists garbage count:", gc.get_count())
# Count increases as new objects created

# Create circular reference
list1.append(list2)    # list1 now contains [1, 2, 3, [4, 5, 6]]
list2.append(list1)    # list2 now contains [4, 5, 6, [1, 2, 3, [...]]]
print("\nAfter circular reference garbage count:", gc.get_count())
print("list1:", list1)
print("list2:", list2)

# Remove direct references
del list1  # Deleting reference but objects still exist
del list2  # Due to circular reference
print("\nAfter deletion garbage count:", gc.get_count())
# Objects still in memory due to circular reference

# Force garbage collection
collected = gc.collect()  # Returns number of objects collected
print("\nGarbage collector collected", collected, "objects.")
print("Final garbage count:", gc.get_count())
# Final count explanation:
# - 41 (or other numver) objects in gen0 are Python's internal objects
#   These include:
#   - Frame objects for function calls
#   - Temporary objects from print statements
#   - Internal references for Python's runtime
#   - System-level temporary objects
# - 0 in gen1 means all middle-aged objects collected
# - 0 in gen2 means all old objects and circular references collected