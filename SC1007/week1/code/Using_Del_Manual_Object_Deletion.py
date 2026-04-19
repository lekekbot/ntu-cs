# Example of manual object deletion using 'del'

# Create variables and show initial state
x = 42
y = x  # y references same integer as x
print(f"Initial value of x: {x}")
print(f"x and y reference same object: {x is y}")
print(f"Memory location of x: {id(x)}")
print(f"Memory location of y: {id(y)}")

list1 = [1, 2, 3, 4, 5]
list2 = list1  # list2 references same list as list1
print(f"\nInitial list1: {list1}")
print(f"list1 and list2 reference same object: {list1 is list2}")
print(f"Memory location of list1: {id(list1)}")
print(f"Memory location of list2: {id(list2)}")

# Delete integer references
print("\nDeleting integer references...")
del x, y  # Removes references to integer 42
# print(x)  # Would raise NameError: x is not defined

# Delete list references
print("Deleting list references...")
del list1, list2  # Removes references to list
# print(list1)  # Would raise NameError: list1 is not defined

print("\nAll objects are now eligible for garbage collection")
# Note: Objects will be collected when Python's garbage collector runs
# We can't access these objects anymore as all references are deleted