class ListNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def print_list(self):
        temp = self.head
        while temp:
            print(temp.item, end=" ")
            temp = temp.next
        print()

    def find_node(self, index):
        if index < 0 or index >= self.size:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

    def insert_node(self, index, value):
        if index < 0 or index > self.size:
            return -1
            
        new_node = ListNode(value)
        
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        elif index == self.size:
            self.tail.next = new_node
            self.tail = new_node
        else:
            prev = self.find_node(index - 1)
            new_node.next = prev.next
            prev.next = new_node
            
        self.size += 1
        return 0

    def remove_node(self, index):
        if index < 0 or index >= self.size:
            return -1
            
        if index == 0:
            self.head = self.head.next
            if self.size == 1:
                self.tail = None
        else:
            prev = self.find_node(index - 1)
            prev.next = prev.next.next
            if index == self.size - 1:
                self.tail = prev
                
        self.size -= 1
        return 0

class Queue:
    def __init__(self):
        self.ll = LinkedList()

    def enqueue(self, item):
        self.ll.insert_node(self.ll.size, item)

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.ll.head.item
        self.ll.remove_node(0)
        return item

    def is_empty(self):
        return self.ll.size == 0

def recursive_reverse(queue):
    # add your code here #
    if queue.is_empty():
        return []
    item = queue.dequeue()
    recursive_reverse(queue)
    queue.enqueue(item)
    return queue

if __name__ == "__main__":
    queue = Queue()
    for i in range(10):
        queue.enqueue(i)
    
    print("Original Queue:")
    queue.ll.print_list()
    recursive_reverse(queue)
    print("Queue after recursive_reverse:")
    queue.ll.print_list()