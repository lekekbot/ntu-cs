class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

class TrieNode:
    def __init__(self, char=None):
        self.char = char
        self.first_child = None
        self.next_sibling = None
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _find_child(self, node, char):
        prev = None
        curr = node.first_child
        while curr and curr.char < char:
            prev = curr
            curr = curr.next_sibling
        if curr and curr.char == char:
            return curr
        return None

    def _insert_child(self, node, char):
        prev = None
        curr = node.first_child
        while curr and curr.char < char:
            prev = curr
            curr = curr.next_sibling

        if curr and curr.char == char:
            return curr  # already exists

        new_node = TrieNode(char)
        new_node.next_sibling = curr
        if prev:
            prev.next_sibling = new_node
        else:
            node.first_child = new_node
        return new_node

    def search(self, word):
        node = self.root
        for char in word:
            node = self._find_child(node, char)
            if not node:
                return False  # Character path not found
        return node.is_end_of_word
    
    def insert(self, word):
        current = self.root
        for char in word:
            child = self._insert_child(current, char)
            current = child
        current.is_end_of_word = True
        
def count_in_range(trie, L, R):
    total_count = 0  # Store how many words fall inside the range.

    def dfs(node, current_word):
        nonlocal total_count  # Reuse the counter from the outer function.

        if not node:  # Stop if there is no trie node to visit.
            return

        # Build the current word represented by this node.
        if node.char is not None:
            this_word = current_word + node.char
        else:
            this_word = current_word

        # Count this word if it is complete and lies in [L, R].
        if node.is_end_of_word:
            if L <= this_word <= R:
                total_count += 1

        # Visit every child node in lexicographic order.
        child = node.first_child
        while child:
            potential_prefix = this_word + child.char  # Prefix if we continue down this child.

            # If this prefix is already beyond R, later siblings will also be too large.
            if potential_prefix > R and not R.startswith(potential_prefix):
                break

            dfs(child, this_word)  # Recurse into the child subtree.

            child = child.next_sibling  # Move to the next sibling.

    dfs(trie.root, "")  # Start from the trie root with an empty prefix.
    return total_count  # Return the final count.

n, q = map(int, input().split())
trie = Trie()

# Insert words
for _ in range(n):
    word = input().strip()
    trie.insert(word)

# Process queries
for _ in range(q):
    L, R = input().strip().split()
    print(count_in_range(trie, L, R))