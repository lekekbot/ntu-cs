class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

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

    def printList(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()

    def findNode(self, index):
        if self.head is None or index < 0:
            return None
        current = self.head
        while index > 0:
            current = current.next
            if current is None:
                return None
            index -= 1
        return current

    def deleteList(self):
        current = self.head
        while current:
            temp = current.next
            current.next = None
            current = temp
        self.head = None

def duplicateReverse(ll):
    # Add your code here
    

if __name__ == "__main__":
    # Create main linked list
    linked_list = LinkedList()
    index = 0
    
    print("Enter a list of numbers, terminated by any non-digit character:")
    try:
        while True:
            item = int(input())
            if linked_list.insert(item, index):
                print(f"Successfully inserted {item} at index {index}")
                index += 1
            else:
                print(f"Failed to insert {item}")
    except ValueError:
        pass

    print("\nBefore duplicateReverse() is called:")
    print("The original list:", end=" ")
    linked_list.printList()
    
    # Create reversed duplicate list
    reversed_list = duplicateReverse(linked_list)
    
    print("\nAfter duplicateReverse() was called:")
    print("The original list:", end=" ")
    linked_list.printList()
    print("The duplicated reverse list:", end=" ")
    reversed_list.printList()
    
    # Clean up both lists
    linked_list.deleteList()
    reversed_list.deleteList()