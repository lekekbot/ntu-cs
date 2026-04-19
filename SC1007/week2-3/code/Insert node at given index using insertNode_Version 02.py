class Node:
    def __init__(self, data):
        self.data = data    # Store node value
        self.next = None    # Initialize next pointer as None

class LinkedList:
    def __init__(self):
        self.head = None    # Initialize head of empty list

    def insert(self, data, index):
        """
        Insert node with given data at specified index.
        Returns True if successful, False if index is invalid.
        """
        new_node = Node(data)   # Create new node
        
        # Handle empty list or insertion at beginning
        if self.head is None or index == 0:  
            new_node.next = self.head
            self.head = new_node
            return True
            
        # Traverse to node before insertion point    
        current = self.head  
        count = 0
        while current and count < index - 1:
            current = current.next
            count += 1
            
        # Check if index was valid    
        if not current:
            print("Index out of range")
            return False
            
        # Insert node by updating pointers    
        new_node.next = current.next
        current.next = new_node
        return True

    def display(self):
        """Print the contents of the list"""
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

    # Link nodes to form the initial list
    # linked_list.head = node1
    # node1.next = node2
    # node2.next = node3
    
    print("Original list:")
    linked_list.display()
    
    # Insert 25 at index 1
    linked_list.insert(25, 1)
    print("After inserting 25 at index 1:")
    linked_list.display()