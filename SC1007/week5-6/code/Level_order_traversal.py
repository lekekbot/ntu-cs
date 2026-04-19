class BTNode:
    """Binary Tree Node"""
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None


class QueueNode:
    """Queue Node for Linked List-based Queue"""
    def __init__(self, data):
        self.data = data
        self.nextPtr = None

class Queue:
    """Queue implementation using a linked list"""
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.tail:
            self.tail.nextPtr = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        dequeued_data = self.head.data
        self.head = self.head.nextPtr
        if self.head is None:
            self.tail = None
        return dequeued_data


def level_order_traversal(root):
    if not root:
        return

    queue = Queue()
    queue.enqueue(root)

    while not queue.is_empty():
        current = queue.dequeue()
        print(current.item, end=" ")
        if current.left:
            queue.enqueue(current.left)
        if current.right:
            queue.enqueue(current.right)


if __name__ == "__main__":
    # Creating a sample Binary Tree:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5

    root = BTNode(1)
    root.left = BTNode(2)
    root.right = BTNode(3)
    root.left.left = BTNode(4)
    root.left.right = BTNode(5)

    print("Level-Order Traversal:")
    level_order_traversal(root)