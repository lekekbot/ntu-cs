class PriorityNode:
   def __init__(self, data, priority):
       self.data = data
       self.priority = priority
       self.next = None

class PriorityQueue:
   def __init__(self):
       self.head = None
       self.size = 0
   
   def peek(self):
       if self.isEmpty():
           raise IndexError("Queue is empty")
       return self.head.data
   
   def enqueue(self, data, priority):
       new_node = PriorityNode(data, priority)
       if self.isEmpty() or priority < self.head.priority:
           new_node.next = self.head
           self.head = new_node
       else:
           current = self.head
           while current.next and current.next.priority <= priority:
               current = current.next
           new_node.next = current.next
           current.next = new_node
       self.size += 1
   
   def dequeue(self):
       if self.isEmpty():
           raise IndexError("Queue is empty")
       removed_data = self.head.data
       self.head = self.head.next
       self.size -= 1
       return removed_data
   
   def isEmpty(self):
       return self.head is None
   
   def getSize(self):
       return self.size
   
   def display(self):
       if self.isEmpty():
           print("Queue is empty")
           return
       current = self.head
       while current:
           print(f"Data: {current.data}, Priority: {current.priority}")
           current = current.next

if __name__ == "__main__":
   pq = PriorityQueue()
   pq.enqueue('Task A', 3)
   pq.enqueue('Task B', 1)
   pq.enqueue('Task C', 2)
   print("Priority Queue Contents:")
   pq.display()
   print("\nPeek at highest priority:", pq.peek())
   print("Dequeued item:", pq.dequeue())
   print("\nPriority Queue After Dequeue:")
   pq.display()
   print("\nIs the queue empty?", pq.isEmpty())
   print("Current size of the queue:", pq.getSize())