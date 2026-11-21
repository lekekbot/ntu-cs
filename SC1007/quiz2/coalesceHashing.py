TABLESIZE = 37
PRIME = 13
EMPTY = 0
USED = 1

class HashSlot:
    def __init__(self):
        self.key = 0
        self.indicator = EMPTY
        self.next = -1

def hash_func(key):
    return key % TABLESIZE

def hash_insert(key, hash_table):
    # 1. Calculate the initial home address
    home_index = key % TABLESIZE
    
    # 2. Duplicate Check
    if hash_find(key, hash_table) != -1:
        return -1
    
    # 3. If the home slot is EMPTY, insert it directly
    if hash_table[home_index].indicator == EMPTY:
        hash_table[home_index].key = key
        hash_table[home_index].indicator = USED
        hash_table[home_index].next = -1
        return home_index
    
    # 4. Collision: Find the next available slot using Linear Probing
    # We check (home_index + 1), (home_index + 2), etc.
    target_idx = -1
    for i in range(1, TABLESIZE):
        probe_idx = (home_index + i) % TABLESIZE
        if hash_table[probe_idx].indicator == EMPTY:
            target_idx = probe_idx
            break
            
    if target_idx == -1:
        return TABLESIZE + 1 # Table is full
        
    # 5. Link the new slot to the end of the existing chain
    # We must start at the home_index and follow 'next' until the end
    curr = home_index
    while hash_table[curr].next != -1:
        curr = hash_table[curr].next
        
    # Place the key in the empty slot found and update the chain pointer
    hash_table[target_idx].key = key
    hash_table[target_idx].indicator = USED
    hash_table[target_idx].next = -1
    hash_table[curr].next = target_idx
    
    return target_idx

def hash_find(key, hash_table):
    home_index = key % TABLESIZE
    
    # If the home slot is empty, the key definitely isn't in the table
    if hash_table[home_index].indicator == EMPTY:
        return -1
        
    # Follow the chain starting from the home index
    curr = home_index
    while curr != -1:
        if hash_table[curr].indicator == USED and hash_table[curr].key == key:
            return curr
        curr = hash_table[curr].next
        
    return -1 # Key not found in the chain


def print_menu():
    print("============= Hash Table ============")
    print("|1. Insert a key to the hash table  |")
    print("|2. Search a key in the hash table  |")
    print("|3. Print the hash table            |")
    print("|4. Quit                            |")
    print("=====================================")
    print("Enter selection: ", end="")


def main():
    import sys
    input = sys.stdin.read
    data = list(map(int, input().split()))

    hash_table = [HashSlot() for _ in range(TABLESIZE)]
    for slot in hash_table:
        slot.key = 0
        slot.indicator = EMPTY
        slot.next = -1

    i = 0
    print_menu()
    while i < len(data):

        opt = data[i]
        i += 1

        if opt == 1:  # Insert
            print("Enter a key to be inserted:")
            if i >= len(data):
                break
            key = data[i]
            i += 1
            index = hash_insert(key, hash_table)
            if index < 0:
                print("Duplicate key")
            elif index < TABLESIZE:
                print(f"Insert {key} at index {index}")
            else:
                print("Table is full.")
            print("Enter selection: ", end="")
        elif opt == 2:  # Search
            print("Enter a key for searching in the HashTable:")
            if i >= len(data):
                break
            key = data[i]
            i += 1
            index = hash_find(key, hash_table)
            if index != -1:
                print(f"{key} is found at index {index}.")
            else:
                print(f"{key} is not found.")
            print("Enter selection: ", end="")
        elif opt == 3:  # Print table
            print("index:\t key \t next")
            for j in range(TABLESIZE):
                print(f"{j}\t{hash_table[j].key}\t{hash_table[j].next}")
            print("Enter selection: ", end="")
        elif opt == 4:
            break
        else:
            print("Enter selection: ", end="")
            continue


if __name__ == "__main__":
    main()