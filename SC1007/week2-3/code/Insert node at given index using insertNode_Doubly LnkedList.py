class Node:
   def __init__(self, data):
       self.data = data
       self.next = None
       self.prev = None

class DoublyLinkedList:
   def __init__(self):
       self.head = None
       self.size = 0

   def insert_at(self, index, data):
       # If index is invalid
       if index < 0 or index > self.size:
           print("Invalid position")
           return False
          
       # Create new node
       new_node = Node(data)
      
       # If inserting at beginning
       if index == 0:
           new_node.next = self.head
           if self.head:
               self.head.prev = new_node
           self.head = new_node
          
       # Inserting at middle or end    
       else:
           current = self.head
           # Traverse to position
           for i in range(index-1):
               current = current.next
              
           # Link new node    
           new_node.prev = current
           new_node.next = current.next
           if current.next:
               current.next.prev = new_node
           current.next = new_node
      
       self.size += 1
       return True

   def display(self):
       current = self.head
       while current:
           print(current.data, end=" <-> ")
           current = current.next
       print("None")

if __name__ == "__main__":
   dll = DoublyLinkedList()
   
   # Test insertions
   dll.insert_at(0, 10)
   dll.insert_at(1, 20) 
   dll.insert_at(2, 30)
   
   print("Original list:")
   dll.display()
   print("Size:", dll.size)
   
   dll.insert_at(1, 25)
   print("\nAfter inserting 25 at index 1:")
   dll.display()
   print("Size:", dll.size)