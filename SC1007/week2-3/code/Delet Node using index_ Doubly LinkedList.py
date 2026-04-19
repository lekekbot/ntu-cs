class Node:
   def __init__(self, data):
       self.data = data
       self.next = None
       self.prev = None

class DoublyLinkedList:
   def __init__(self):
       self.head = None
       self.size = 0

   def insert(self, data, index):
       if index < 0 or index > self.size:
           print("Index out of range")
           return False

       new_node = Node(data)

       # Case 1: Insert at beginning (index 0)
       if index == 0:
           new_node.next = self.head
           if self.head:
               self.head.prev = new_node
           self.head = new_node

       # Case 2: Insert at middle or end
       else:
           current = self.head
           for i in range(index-1):
               current = current.next
           
           # Update pointers
           new_node.next = current.next
           new_node.prev = current
           if current.next:
               current.next.prev = new_node
           current.next = new_node

       self.size += 1
       return True

   def remove_at(self, index):
       # Case 1: Check if the list is empty
       if self.head is None:
           print("List is empty")
           return False
       # Case 2: Validate index
       if index < 0 or index >= self.size:
           print("Invalid index")
           return False
       # Case 3: Remove the first node (index 0)
       if index == 0:
           self.head = self.head.next
           if self.head:  # If the list is not empty after removal
               self.head.prev = None
           self.size -= 1
           return True
       # Case 4: Remove from the middle or end
       current = self.head
       for i in range(index):   # Traverse to the node at the given index
           current = current.next
       # Update pointers to remove the node
       current.prev.next = current.next
       if current.next:  # If it's not the last node
           current.next.prev = current.prev
       self.size -= 1
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
   dll.insert(10, 0)
   dll.insert(20, 1) 
   dll.insert(25, 2)
   dll.insert(30, 3)
   
   print("Original list:")
   dll.display()
   print("Size:", dll.size)
   
   # Remove node at index 3
   dll.remove_at(3)
   print("\nAfter removing node at index 3:")
   dll.display()
   print("Size:", dll.size)