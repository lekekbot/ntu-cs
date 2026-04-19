class Node:
   def __init__(self, data):
       self.data = data
       self.next = None

class LinkedList:
   def __init__(self):
       self.head = None
       
  # Made display a method of LinkedList
   def display(self):
       current = self.head
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
   
   # Call display method to print: 
   # 10 -> 20 -> 30 -> None   
   linked_list.display()