class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)  # Add to the end

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # Remove from the front
        return None

    def is_empty(self):
        return len(self.items) == 0

class TrieNode:
    def __init__(self, char=None):
        self.char = char
        self.is_end_of_word = False
        self.first_child = None
        self.next_sibling = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _insert_child(self, node, char):
        prev = None
        curr = node.first_child
        while curr and curr.char < char:
            prev = curr
            curr = curr.next_sibling

        if curr and curr.char == char:
            return curr

        new_node = TrieNode(char)
        new_node.next_sibling = curr
        if prev:
            prev.next_sibling = new_node
        else:
            node.first_child = new_node
        return new_node

    def insert(self, word):
        current = self.root
        for char in word:
            current = self._insert_child(current, char)
        current.is_end_of_word = True
    
    def _find_child(self, node, char):
        curr = node.first_child
        while curr:
            if curr.char == char:
                return curr
            curr = curr.next_sibling
        return None

    def search(self, word):
        curr = self.root
        for char in word:
            curr = self._find_child(curr, char)
            if not curr:
                return False
        return curr.is_end_of_word

def count_words_with_length(trie, target_length):
#add your implementations
    if not trie.root:
         return 0
        #  use queue  as (root, depth)
    q = Queue()
    q.enqueue((trie.root,0))
    count = 0

    while not q.is_empty():
        # find target depth
        node, depth = q.dequeue()

        if depth == target_length:
            if node.is_end_of_word:
                count += 1
            continue

        if depth < target_length:
            child = node.first_child
            while child:
                q.enqueue((child, depth + 1))
                child = child.next_sibling
    return count

# Main program
n_l = input().split()
n = int(n_l[0])
L = int(n_l[1])

trie = Trie()
for _ in range(n):
    word = input().strip()
    trie.insert(word)

print(count_words_with_length(trie,L))
    