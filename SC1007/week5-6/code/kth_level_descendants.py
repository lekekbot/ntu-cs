class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    
    def kth_level_descendants(self, node, k):
        if node is None:
            return []
        
        if k == 0:
            return [node.data]

        left_descendants = self.kth_level_descendants(node.left, k - 1)
        right_descendants = self.kth_level_descendants(node.right, k - 1)

        return left_descendants + right_descendants


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

    k = 2
    print(f"\nNodes at level {k}: {root.kth_level_descendants(root, k)}")
