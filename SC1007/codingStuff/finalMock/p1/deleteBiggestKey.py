class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

class HashTable:
    def __init__(self, hSize=0):
        self.hSize = hSize #the number of hash slots
        self.nSize = 0 #the number of keys
        self.table = [None] * self.hSize

def hash_func(key, hSize):
    return key % hSize

def hash_search(ht, key):
    if ht.hSize == 0:
        return None
    index = hash_func(key, ht.hSize)
    curr = ht.table[index]
    while curr:
        if curr.key == key:
            return curr
        curr = curr.next
    return None

def hash_print(ht):
    for i in range(ht.hSize):
        print(f"{i}:", end=" ")
        curr = ht.table[i]
        while curr:
            print(f"{curr.key} ->", end=" ")
            curr = curr.next
        print()
        
def hash_insert(ht, key):
    i = hash_func(key, ht.hSize)
    n = Node(key)
    curr = ht.table[i]

    while curr:
        if curr.key == key:
            return 0
        curr = curr.next
    
    n.next = ht.table[i]
    ht.table[i] = n

    ht.nSize += 1

    return 1
    
    
def hash_delete_biggest(ht):
    #add you implementations
    if ht.nSize == 0:
        return 0
    current_max = 0
    target_node = None
    prev_node = None
    target_i = None
    size = ht.hSize

    for i in range(size):
        prev = None
        curr = ht.table[i]

        while curr:
            if curr.key > current_max:
                current_max = curr.key
                target_node = curr
                prev_node = prev
                target_i = i
            prev = curr
            curr = curr.next
    if current_max:
        if prev_node is None:
            ht.table[target_i] = target_node.next
        else:
            prev_node.next = target_node.next
        
        ht.nSize -=1
        return 1
    
    return 0

def main():
    ht = None

    import sys
    input = sys.stdin.read
    data = list(map(int, input().split()))
    i = 0

    print("============= Hash Table ============")
    print("|1. Create a hash table                   |")
    print("|2. Insert a key to the hash table        |")
    print("|3. Search a key in the hash table        |")
    print("|4. Delete biggest key in the hash table  |")
    print("|5. Print the hash table                  |")
    print("|6. Quit                                  |")
    print("=====================================")

    print("Enter Selection: ", end="")
    while i < len(data):
        opt = data[i]
        i += 1

        if opt == 1:
            print("Enter the size of hash table:")
            size = data[i]
            i+=1
            ht = HashTable(size)
            print("HashTable is created.")

        elif opt == 2:
            if ht is None:
                print("HashTable not created yet.")
                continue
            print("Enter a key to be inserted:")
            key = data[i]
            i+=1
            if hash_insert(ht, key):
                print(f"{key} is inserted.")
            else:
                print(f"{key} is a duplicate. No key is inserted.")
        elif opt == 3:
            if ht is None:
                print("HashTable not created yet.")
                continue
            print("Enter a key for searching in the HashTable:")
            key = data[i]
            i+=1
            if hash_search(ht, key):
                print(f"{key} is found.")
            else:
                print(f"{key} is not found.")
        elif opt == 4:
            if ht is None:
                print("HashTable not created yet.")
                continue
            if hash_delete_biggest(ht):
                print("Biggest key is deleted.")
            else:
                print("Biggest key is not existing.")
        elif opt == 5:
            if ht is None:
                print("HashTable not created yet.")
                continue
            hash_print(ht)
        elif opt == 6:
            print("Exiting.")
            break
        else:
            print("Invalid option.")
        print("Enter Selection: ", end="")

if __name__ == "__main__":
    main()