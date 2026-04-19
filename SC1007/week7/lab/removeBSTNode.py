class BTNode:
    def __init__(self, item, left=None, right=None):
        self.item = item  # Store the item (integer)
        self.left = left  # Reference to the left child node
        self.right = right  # Reference to the right child node

def insertBSTNode(root, value):
    """ Recursive approach to insert a node into a BST. """
    if root is None:
        return BTNode(value)
    
    if value < root.item:
        root.left = insertBSTNode(root.left, value)
    elif value > root.item:
        root.right = insertBSTNode(root.right, value)
    return root  # Ensure the modified node is returned

def findMin(node):
    """ Find the node with the smallest value in a subtree. """
    while node.left is not None:
        node = node.left
    return node

def removeBSTNode(root, value):
    """
    Returns the updated root node and a result code (0 for success, -1 for failure).
    """
    if root is None:
        return None, -1
    
    # Search for the node to remove
    if value < root.item:
        new_left, result = removeBSTNode(root.left, value)
        root.left = new_left
        return root, result
    elif value > root.item:
        new_right, result = removeBSTNode(root.right, value)
        root.right = new_right
        return root, result
    
    # Node found, handle the three cases
    
    # Case 1: Leaf node (no children)
    if root.left is None and root.right is None:
        return None, 0
    
    # Case 2: Node with only one child
    if root.left is None:
        return root.right, 0
    if root.right is None:
        return root.left, 0
    
    # Case 3: Node with two children
    # Find the inorder successor (smallest node in right subtree)
    successor = findMin(root.right)
    root.item = successor.item
    
    # Remove the successor
    root.right, _ = removeBSTNode(root.right, successor.item)
    
    return root, 0

def printBSTInOrder(node):
    """ Print BST items in sorted order using in-order traversal. """
    if node:
        printBSTInOrder(node.left)
        print(node.item, end=" ")
        printBSTInOrder(node.right)

def printTree(node, level=0, prefix="Root: "):
    """ Pretty prints the tree structure for better visualization """
    if node is not None:
        print(" " * level + prefix + str(node.item))
        if node.left or node.right:
            if node.left:
                printTree(node.left, level + 4, "L--- ")
            if node.right:
                printTree(node.right, level + 4, "R--- ")

if __name__ == "__main__":
    root = None
    print("Binary Search Tree Node Removal Program")
    print("=====================================")
    
    print("\nFirst, let's build the BST:")
    while True:
        try:
            value = input("\nEnter a value to insert (-1 to quit): ")
            if not value:
                continue  # Ignore empty inputs
                
            i = int(value)
            if i == -1:
                break
                
            root = insertBSTNode(root, i)
            print("\nCurrent BST structure:")
            printTree(root)
            print("\nIn-order traversal: ", end="")
            printBSTInOrder(root)
            print()
            
        except ValueError:
            print("Invalid input! Please enter an integer.")

    print("\nNow let's remove nodes:")
    while True:
        try:
            value = input("\nEnter a value to remove (-1 to quit): ")
            if not value:
                continue  # Ignore empty inputs
                
            i = int(value)
            if i == -1:
                break
                
            root, result = removeBSTNode(root, i)
            if result == 0:
                print("\nBST structure after removal:")
                printTree(root)
                print("\nIn-order traversal: ", end="")
                printBSTInOrder(root)
                print()
            else:  # result == -1
                print("Value not found in the tree!")
            
        except ValueError:
            print("Invalid input! Please enter an integer.")