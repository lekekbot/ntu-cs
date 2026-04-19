class Node:
   def __init__(self, data):
       self.data = data
       self.next = None

class LinkedList:
   def __init__(self):
       self.head = None
 
# Standalone function taking head as parameter      
def display(head):
   current = head
   while current:
        print(current.data, end=" -> ")
        current = current.next
   print("None")


if __name__ == "__main__":
   
   # Initialize empty linked list object
   linked_list = LinkedList()
   
   # Create nodes
   node1 = Node(10)
   node2 = Node(20)
   node3 = Node(30)
   
   # Link nodes
   linked_list.head = node1
   node1.next = node2
   node2.next = node3
   
   # Print the linked list 
   # Passes linked_list.head as argument
   display(linked_list.head)