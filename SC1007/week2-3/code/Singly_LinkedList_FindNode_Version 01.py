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

if __name__ == "__main__":
    linked_list = LinkedList()

    # Create nodes
    node1 = Node(10)
    node2 = Node(20)
    node3 = Node(30)
    
    # Link nodes and update size
    linked_list.head = node1
    node1.next = node2
    node2.next = node3
    linked_list.size = 3  # Update size after adding 3 nodes
    
    # Find node at index 2
    found_node = linked_list.findNode(2)
    if found_node:
        print(f"Node at index 2: {found_node.data}")
    else:
        print("Index not found")