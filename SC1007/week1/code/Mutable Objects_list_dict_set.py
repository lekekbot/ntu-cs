# List demonstration
print("LIST DEMONSTRATION")
print("-" * 20)
list1 = [1, 2, 3]
list2 = list1  # Both point to same list

print(f"Initially:")
print(f"list1 = {list1}, id(list1) = {id(list1)}")
print(f"list2 = {list2}, id(list2) = {id(list2)}")

list1.append(4)  # Modifies the same list
print(f"\nAfter list1.append(4):")
print(f"list1 = {list1}, id(list1) = {id(list1)}")
print(f"list2 = {list2}, id(list2) = {id(list2)}")

print("\n" + "=" * 40 + "\n")

# Dictionary demonstration
print("DICTIONARY DEMONSTRATION")
print("-" * 20)
dict1 = {'a': 1, 'b': 2}
dict2 = dict1  # Both point to same dictionary

print(f"Initially:")
print(f"dict1 = {dict1}, id(dict1) = {id(dict1)}")
print(f"dict2 = {dict2}, id(dict2) = {id(dict2)}")

dict1['c'] = 3  # Modifies the same dictionary
print(f"\nAfter dict1['c'] = 3:")
print(f"dict1 = {dict1}, id(dict1) = {id(dict1)}")
print(f"dict2 = {dict2}, id(dict2) = {id(dict2)}")

print("\n" + "=" * 40 + "\n")

# Set demonstration
print("SET DEMONSTRATION")
print("-" * 20)
set1 = {1, 2, 3}
set2 = set1  # Both point to same set

print(f"Initially:")
print(f"set1 = {set1}, id(set1) = {id(set1)}")
print(f"set2 = {set2}, id(set2) = {id(set2)}")

set1.add(4)  # Modifies the same set
print(f"\nAfter set1.add(4):")
print(f"set1 = {set1}, id(set1) = {id(set1)}")
print(f"set2 = {set2}, id(set2) = {id(set2)}")