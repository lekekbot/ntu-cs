class ListNode:
   def __init__(self, data):    
       self.data = data         
       self.next = None

class LinkedList:
   def __init__(self):
       self.size = 0
       self.head = None
       self.tail = None

   def find_node(self, index):
       if index < 0 or index >= self.size:
           return None
       temp = self.head
       for _ in range(index):
           temp = temp.next
       return temp

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

class Stack:
   def __init__(self):
       self.ll = LinkedList()

   def push(self, data):    
       self.ll.insert_node(0, data)

   def pop(self):
       if self.isEmpty():
           return None
       data = self.ll.head.data    
       self.ll.remove_node(0)
       return data

   def peek(self):
       if self.isEmpty():
           return None
       return self.ll.head.data    

   def isEmpty(self):
       return self.ll.size == 0
   
   def get_size(self):
       return self.ll.size

class Queue:
   def __init__(self):
       self.ll = LinkedList()

   def enqueue(self, data):    
       self.ll.insert_node(self.ll.size, data)

   def dequeue(self):
       if self.isEmpty():
           return None
       data = self.ll.head.data    
       self.ll.remove_node(0)
       return data

   def getFront(self):
       if self.isEmpty():
           raise IndexError("Peek from empty queue")
       return self.ll.head.data    

   def getSize(self):           
       return self.ll.size

   def isEmpty(self):
       return self.ll.size == 0
  
   def printQueue(self):
       if self.isEmpty():
           print("Queue is empty")
           return
       current = self.ll.head
       while current:
           print(current.data, end=" ")    
           current = current.next
       print()

def reverse_queue(queue):
   stack = Stack()
   
   while not queue.isEmpty():
       stack.push(queue.dequeue())
       
   while not stack.isEmpty():
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