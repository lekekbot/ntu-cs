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

if __name__ == "__main__":
    linked_list = LinkedList()

    # Insert nodes using insert method
    linked_list.insert(10, 0)  # First node
    linked_list.insert(20, 1)  # Second node
    linked_list.insert(30, 2)  # Third node
    
    # Find node at index 2
    found_node = linked_list.findNode(2)
    if found_node:
        print(f"Node at index 2: {found_node.data}")
    else:
        print("Index not found")