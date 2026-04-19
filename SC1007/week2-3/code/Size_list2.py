class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def findNode(self, index):
        # Check if list is empty or index is invalid
        if self.head is None or index < 0 or index >= self.size:
            return None
        
        # Start traversing from head
        cur = self.head
        while index > 0:
            cur = cur.next
            index -= 1
        return cur
    
    def insert(self, data, index):
        # Check if index is valid
        if index < 0 or index > self.size:
            print("Index out of range")
            return False
            
        new_node = Node(data)
        
        # Insert at beginning
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True
        
        # Use findNode to get previous node
        prev_node = self.findNode(index - 1)
        if prev_node is not None:
            new_node.next = prev_node.next
            prev_node.next = new_node
            self.size += 1
            return True
        
        return False
    
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

if __name__ == "__main__":
    # Create and initialize the linked list
    linked_list = LinkedList()
    linked_list.insert(10, 0)
    linked_list.insert(20, 1)
    linked_list.insert(30, 2)
    
    # Display the original list
    print("Current list:")
    linked_list.display()
    
    # Display initial size
    print(f"Size of the list: {linked_list.size}")  
    
    # Insert 25 at index 1
    linked_list.insert(25, 1)
    print("\nAfter inserting 25 at index 1:")
    linked_list.display()
    
    # Display updated size
    print(f"Size of list: {linked_list.size}")  