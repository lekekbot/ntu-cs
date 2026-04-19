class ListNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, item, index):
        new_node = ListNode(item)

        # Handle insertion at beginning
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True
    
        # Find node before insertion point
        current = self.head
        count = 0
        while current and count < index - 1:
            current = current.next
            count += 1
    
        # Check if position is valid
        if not current:
            print("Index out of range")
            return False
        
        # Insert the new node
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True
    
    def printList(self):
        if self.head is not None:
            cur = self.head
            print(f"Current List has {self.size} elements: ", end="")
            while cur is not None:
                print(cur.item, end=" ")
                cur = cur.next
            print()

    def remove(self, index):
        if self.head is None:
            print("List is empty")
            return False
            
        # Handle removing first node
        if index == 0:
            cur = self.head
            self.head = cur.next
            del cur
            self.size -= 1
            return True
            
        # Find node before removal point
        current = self.head
        count = 0
        while current and count < index - 1:
            current = current.next
            count += 1
            
        # Check if position is valid
        if not current or not current.next:
            print("Index out of range")
            return False
            
        # Remove the node
        temp = current.next
        current.next = temp.next
        del temp
        self.size -= 1
        return True

# The standalone function as specified in the question
def removeNode(ll, index):
    """
    Remove a node at the specified index from the linked list.
    
    Args:
        ll: LinkedList object
        index: Index of the node to be removed
    
    Returns:
        True if removal was successful, False otherwise
    """
    if ll.head is None:
        print("List is empty")
        return False
        
    # Handle removing first node (index 0)
    if index == 0:
        cur = ll.head
        ll.head = cur.next
        del cur
        ll.size -= 1
        return True
        
    # Find node before removal point
    current = ll.head
    count = 0
    while current and count < index - 1:
        current = current.next
        count += 1
        
    # Check if position is valid
    if not current or not current.next:
        print("Index out of range")
        return False
        
    # Remove the node
    temp = current.next
    current.next = temp.next
    del temp
    ll.size -= 1
    return True

if __name__ == "__main__":
    ll = LinkedList()
    print("Enter one number per line (press Enter after each number).")
    print("Enter any non-digit character to finish input:")
    try:
        while True:
            item = int(input())
            if not ll.insert(item, ll.size):
                break
    except ValueError:
        pass
    ll.printList()
    
    while True:
        try:
            index = int(input("Enter the index of the node to be removed: "))
            if not removeNode(ll, index):
                print("The node cannot be removed.")
                break
            print("After the removal operation:")
            ll.printList()
        except ValueError:
            break
    ll.printList()