class Node:
   def __init__(self, data):
       self.data = data
       self.next = None

class LinkedList:
   def __init__(self):
       self.head = None
       
   def findAt(self, index):
       current = self.head
       if not current:
           return None
       while index>0:
           current = current.next
           if not current:
               return None
           index-=1
       return current

if __name__ == "__main__":
   linked_list = LinkedList()
   node1 = Node(10)
   node2 = Node(20) 
   node3 = Node(30)
   
   linked_list.head = node1
   node1.next = node2
   node2.next = node3
   
   # Find node at index 2
   found_node = linked_list.findAt(2)
   if found_node:
       print(f"Node at index 2: {found_node.data}")  # Output: 30
   else:
       print("Index not found")


'''Automatic instance passing: When you call linked_list.findAt(2),Python automatically passes the LinkedList instance (linked_list) 
as the first parameter (self) to the findAt method. This is a fundamental feature of object-oriented programming in Python.

Accessing instance attributes: Through self, the method gains access to all instance attributes, including the head pointer (self.head). 
This allows the method to work with the list's structure without needing external access to these attributes.

Initializing traversal: The line current = self.head sets the starting point for traversal. 
It creates a local variable current that initially points to the first node in the list, using the head pointer accessed through self.

Encapsulation: This design encapsulates the list's internal structure within the class, 
promoting good object-oriented practices by not requiring external access to the head pointer.'''