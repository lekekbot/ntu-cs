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
            # Changed to index-1 in range
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

    def delete(self, data):
        if self.head is None:
            raise ValueError("List is empty")
       
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                self.size -= 1
                return True
            current = current.next
       
        return False

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
    
    # Delete node at index 3 (value 30)
    dll.delete(30)
    print("\nAfter deleting node with value 30:")
    dll.display()
    print("Size:", dll.size)