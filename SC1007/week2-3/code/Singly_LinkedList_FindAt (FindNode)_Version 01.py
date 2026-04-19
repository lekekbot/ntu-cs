class Node:
   def __init__(self, data):
       self.data = data
       self.next = None

class LinkedList:
   def __init__(self):
       self.head = None
       
# Independent function that takes head and index
def findAt(head, index):
    current = head
    if not current:
        return None
    while index > 0:
        current = current.next
        if not current:
            return None
        index -= 1
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
   found_node = findAt(linked_list.head, 2)
   if found_node:
       print(f"Node at index 2: {found_node.data}")  
   else:
       print("Index not found")