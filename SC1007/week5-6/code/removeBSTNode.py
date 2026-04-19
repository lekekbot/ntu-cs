class Node:
   def __init__(self, data):
       self.data = data
       self.left = None
       self.right = None

def insert(data, current_node):
   if data < current_node.data:
       if current_node.left is None:
           current_node.left = Node(data)
       else:
           insert(data, current_node.left)
   else:
       if current_node.right is None:
           current_node.right = Node(data)
       else:
           insert(data, current_node.right)

def findMin(node):
   while node.left is not None:
       node = node.left
   return node

def removeBSTNode(node, value):
   if node is None:
       return node, -1
   
   if value < node.data:
       if node.left is None:
           return node, -1
       new_left, result = removeBSTNode(node.left, value)
       node.left = new_left
       return node, result
   elif value > node.data:
       if node.right is None:
           return node, -1
       new_right, result = removeBSTNode(node.right, value)
       node.right = new_right
       return node, result
   else:
       if node.left is None:
           return node.right, 0
       elif node.right is None:
           return node.left, 0
       
       temp = findMin(node.right)
       node.data = temp.data
       new_right, _ = removeBSTNode(node.right, temp.data)
       node.right = new_right
       return node, 0

def printTree(node, level=0, prefix="Root: "):
   if node is not None:
       print(" " * level + prefix + str(node.data))
       if node.left or node.right:
           if node.left:
               printTree(node.left, level + 4, "L--- ")
           if node.right:
               printTree(node.right, level + 4, "R--- ")

def inorder_traversal(node):
   if node:
       inorder_traversal(node.left)
       print(node.data, end=" ")
       inorder_traversal(node.right)

if __name__ == "__main__":
   root = Node(10)
   
   insert(5, root)
   insert(15, root)
   insert(2, root)
   insert(7, root)
   insert(12, root)
   insert(18, root)
   
   print("Original Tree:")
   printTree(root)
   print("\nIn-Order Traversal of original BST:")
   inorder_traversal(root)
   
   print("\n\nRemoving node with two children (5):")
   root, result = removeBSTNode(root, 5)
   print(f"Remove result: {'Success' if result == 0 else 'Failed'}")
   printTree(root)
   
   print("\nRemoving node with one child (15):")
   root, result = removeBSTNode(root, 15)
   print(f"Remove result: {'Success' if result == 0 else 'Failed'}")
   printTree(root)
   
   print("\nRemoving leaf node (2):")
   root, result = removeBSTNode(root, 2)
   print(f"Remove result: {'Success' if result == 0 else 'Failed'}")
   printTree(root)
   
   print("\nFinal In-order traversal:")
   inorder_traversal(root)