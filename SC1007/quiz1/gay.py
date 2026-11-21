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

    def printList(self):
        cur = self.head
        if cur is None:
            print("Empty")
            return
        while cur is not None:
            print(cur.data, end=" ")
            cur = cur.next
        print(" ")


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
        self.ll.printList()


def reverseQueueSegment(queue, m, n):
    if m < 0 or n >= queue.getSize() or m > n:
        return  # Safety check

    s = Stack()
    size = queue.getSize()

    # Step 1: Move the first m elements to the back of the queue
    for _ in range(m):
        queue.enqueue(queue.dequeue())

    # Step 2: Dequeue elements from m to n and push them onto a Stack
    count_to_reverse = n - m + 1
    for _ in range(count_to_reverse):
        s.push(queue.dequeue())

    # Step 3: Pop from Stack and enqueue back to the Queue (this reverses them)
    while not s.isEmpty():
        queue.enqueue(s.pop())

    # Step 4: Move the remaining elements (those after n) to the back
    # The number of remaining elements is: total_size - (n + 1)
    remaining = size - (n + 1)
    for _ in range(remaining):
        queue.enqueue(queue.dequeue())
    # temp1 = 0
    # temp2 = 0
    # tempQueue = Queue()

    # for i, data in enumerate(range(queue.getSize())):
    #     if(i == m):
    #         temp1 = queue.getFront()
    #     elif(i==n):
    #         temp2 = queue.getFront()
    #     else:
    #         queue.dequeue()


if __name__ == "__main__":
    queue = Queue()

    print("Enter a list of numbers, terminated by any non-digit character: ", end="")
    input_string = input()
    numbers = input_string.split()

    for num in numbers:
        try:
            queue.enqueue(int(num))
        except ValueError:
            break

    m, n = map(int, input("Enter indices m and n separated by space: ").split())

    print("Original Queue:", end=" ")
    queue.printQueue()

    # Validate input indices before calling the function
    if m < 0 or n >= queue.getSize() or m > n:
        print("Invalid indices")
    else:
        reverseQueueSegment(queue, m, n)
        print("Modified Queue:", end=" ")
        queue.printQueue()
