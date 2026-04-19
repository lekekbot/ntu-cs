class Node:
   def __init__(self, data):
       self.data = data
       self.next = None

class LinkedList:
   def __init__(self):
       self.head = None
      
   def display(self):
       current = self.head
       while current:
           print(current.data, end=" -> ")
           current = current.next
       print("None")
  
   def sizeList(self):
       count = 0
       current = self.head  
       while current is not None:
           count += 1
           current = current.next
       return count

   def insert(self, data, index):
       new_node = Node(data)
       if self.head is None or index == 0:
           new_node.next = self.head
           self.head = new_node
           return True
      
       current = self.head
       count = 0
      
       while current and count < index - 1:
           current = current.next
           count += 1
      
       if not current:
           print("Index out of range")
           return False
          
       new_node.next = current.next
       current.next = new_node
       return True

if __name__ == "__main__":
   linked_list = LinkedList()
   linked_list.insert(10, 0)
   linked_list.insert(20, 1)
   linked_list.insert(30, 2)
  
   print("Current list:")
   linked_list.display()
  
   print(f"Size of the list: {linked_list.sizeList()}")
  
   linked_list.insert(25, 1)
   print("\nAfter inserting 25 at index 1:")
   linked_list.display()
  
   print(f"Size of list: {linked_list.sizeList()}")