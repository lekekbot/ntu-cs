class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def isEmpty(self):
        return self.front is None
    
    def enqueue(self, data):
        new_node = Node(data)
        if self.isEmpty():
            self.front = new_node
        else:
            self.rear.next = new_node
        self.rear = new_node
        self.size += 1
    
    def dequeue(self):
        if self.isEmpty():
            raise IndexError("Dequeue from empty queue")
        dequeued_node = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return dequeued_node.data
    
    def getFront(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.front.data
    
    def getSize(self):
        return self.size
    
    def displayQueue(self):
        current = self.front
        while current:
            print(current.data)
            current = current.next

if __name__ == "__main__":
    queue = Queue()
    
    queue.enqueue("Customer 1")
    queue.enqueue("Customer 2")
    queue.enqueue("Customer 3")
    print("\nInitial queue:")
    queue.displayQueue()
    
    queue.dequeue()
    print("\nAfter dequeue:")
    queue.displayQueue()
    
    queue.enqueue("Customer 4")
    print("\nAfter adding Customer 4:")
    queue.displayQueue()
    
    print("\nFront of queue:", queue.getFront())