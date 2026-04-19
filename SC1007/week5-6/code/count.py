class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def pre_order_traversal(self, node):
        if node:
            print(node.data, end=" ")
            self.pre_order_traversal(node.left)
            self.pre_order_traversal(node.right)

    def in_order_traversal(self, node):
        if node:
            self.in_order_traversal(node.left)
            print(node.data, end=" ")
            self.in_order_traversal(node.right)

    def post_order_traversal(self, node):
        if node:
            self.post_order_traversal(node.left)
            self.post_order_traversal(node.right)
            print(node.data, end=" ")

    def count_nodes(self, node):
        if not node:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)


if __name__ == "__main__":
    # Creating a sample tree:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    
    
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    print("Pre-Order Traversal:")
    root.pre_order_traversal(root)

    print("\nIn-Order Traversal:")
    root.in_order_traversal(root)
    
    print("\nPost-Order Traversal:")
    root.post_order_traversal(root)

    print("\nTotal number of nodes in the tree:", root.count_nodes(root))
