class Node:
    """Represents a node in the Binary Search Tree."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def search(data, current_node):
    """Function to recursively search for a value in BST."""
    if current_node is None:
        return False
    elif data == current_node.data:
        return True
    elif data < current_node.data:
        return search(data, current_node.left)
    else:
        return search(data, current_node.right)

def printTree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * level + prefix + str(node.data))
        if node.left or node.right:
            if node.left:
                printTree(node.left, level + 4, "L--- ")
            if node.right:
                printTree(node.right, level + 4, "R--- ")

# Example Usage
if __name__ == "__main__":
    # Create a sample BST
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(2)
    root.left.right = Node(7)
    root.right.left = Node(12)
    root.right.right = Node(18)
    
    # Print the tree structure
    print("BST structure:")
    printTree(root)
      
    # Test searching for various values
    print("\n\nSearch Results:")
    print("Searching for 7:", search(7, root))    # Should return True
    print("Searching for 15:", search(15, root))  # Should return True
    print("Searching for 9:", search(9, root))    # Should return False