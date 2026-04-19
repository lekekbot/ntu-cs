# Create two empty lists
list1 = []                     # Create first empty list
list2 = []                     # Create second empty list

# Create circular reference
list1.append(list2)           # list1 now contains list2 as its element
list2.append(list1)           # list2 now contains list1 as its element

print("After creating circular reference:")
print(f"list1 = {list1}")     # Shows list1 containing list2
print(f"list2 = {list2}")     # Shows list2 containing list1

# Memory leak situation
del list1                     # Delete first reference but object still exists
del list2                     # Delete second reference but object still exists

# At this point:
# - Both lists still exist in memory
# - Each list contains a reference to the other
# - No external references exist to access these lists
# - Only garbage collector can free this memory
# - This is why reference counting alone isn't enough