class Node:     
   def __init__(self, data):         
       self.data = data
       self.next = None

class Stack:     
   def __init__(self):         
       self.top = None
       self.size = 0
   
   def peek(self):
       if self.is_empty():
           raise IndexError("Peek: Empty stack")
       return self.top.data
   
   def push(self, data):
       new_node = Node(data)
       new_node.next = self.top
       self.top = new_node
       self.size += 1
   
   def pop(self):
       if self.is_empty():
           raise IndexError("Pop: Empty stack")
       popped_node = self.top
       self.top = self.top.next
       self.size -= 1
       return popped_node.data
   
   def is_empty(self):
       return self.top is None
   
   def get_size(self):
       return self.size

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
           raise IndexError("Peek from empty queue")
       return self.front.data

   def getSize(self):
       return self.size

   # Added print method to display queue
   def printQueue(self):
       if self.isEmpty():
           print("Queue is empty")
           return
       current = self.front
       while current:
           print(current.data, end=" ")
           current = current.next
       print()  # New line

def reverse_queue(queue):
   stack = Stack()
   
   # Push all elements from queue to stack
   while not queue.isEmpty():
       stack.push(queue.dequeue())
       
   # Pop from stack and enqueue back to queue
   while not stack.is_empty():
       queue.enqueue(stack.pop())
   
   return queue

if __name__ == "__main__":
   queue = Queue()
   
   # Enqueue three values
   queue.enqueue(10)
   queue.enqueue(20)
   queue.enqueue(30)
   
   # Print original queue
   print("Original Queue:", end=" ")
   queue.printQueue()    # Will print: 10 20 30
   
   # Reverse the queue
   queue = reverse_queue(queue)
   
   # Print reversed queue
   print("Reversed Queue:", end=" ")
   queue.printQueue()    # Will print: 30 20 10