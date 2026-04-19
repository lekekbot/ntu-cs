TABLESIZE = 37
PRIME = 13
EMPTY = 0
USED = 1
DELETED = 2

class HashSlot:
    def __init__(self):
        self.key = 0
        self.indicator = EMPTY

def hash1(key):
    return key % TABLESIZE

def hash2(key):
    return (key % PRIME) + 1

def hash_insert(key, hash_table):
    index = hash1(key)
    step = hash2(key)
    comparisons = 0
    first_deleted_index = -1

    for i in range(TABLESIZE):
        target_idx = (index + i * step) % TABLESIZE
        slot = hash_table[target_idx]

        if slot.indicator == EMPTY:
            insert_pos= ( first_deleted_index if first_deleted_index != -1 else target_idx)
            hash_table[insert_pos].key = key
            hash_table[insert_pos].indicator = USED
            return comparisons
        
        if slot.indicator == USED:
            comparisons += 1
            if slot.key == key:
                return -1
        elif slot.indicator == DELETED:
            if first_deleted_index == -1:
                first_deleted_index = target_idx
    if first_deleted_index != -1:
        hash_table[first_deleted_index].key = key
        hash_table[first_deleted_index].indicator = USED
        return comparisons
    return comparisons

def hash_delete(key, hash_table):
    index = hash1(key)
    step = hash2(key)
    comparisons = 0

    for i in range(TABLESIZE):
        target_idx = (index + i * step) % TABLESIZE
        slot = hash_table[target_idx]

        if slot.indicator == EMPTY:
            return -1 
        if slot.indicator == USED:
            comparisons += 1
            if slot.key == key:
                slot.indicator = DELETED
                return comparisons
        continue
    return -1


def print_menu():
    print("============= Hash Table ============")
    print("|1. Insert a key to the hash table  |")
    print("|2. Delete a key from the hash table|")
    print("|3. Print the hash table            |")
    print("|4. Quit                            |")
    print("=====================================")
    print("Enter selection: ", end="")
    
def main():
    import sys
    input = sys.stdin.read
    data = list(map(int, input().split()))

    hash_table = [HashSlot() for _ in range(TABLESIZE)]
    i = 0
    print_menu()
    while i < len(data):
        opt = data[i]
        i += 1

        if opt == 1:
            print("Enter a key to be inserted:")
            if i >= len(data):
                break
            key = data[i]
            i += 1
            comparison = hash_insert(key, hash_table)
            if comparison < 0:
                print("Duplicate key")
            elif comparison < TABLESIZE:
                print(f"Insert: {key} Key Comparisons: {comparison}")
            else:
                print(f"Key Comparisons: {comparison}. Table is full.")
            print("Enter selection: ", end="")
        elif opt == 2:
            print("Enter a key to be deleted:")
            if i >= len(data):
                break
            key = data[i]
            i += 1
            comparison = hash_delete(key, hash_table)
            if comparison < 0:
                print(f"{key} does not exist.")
            elif comparison <= TABLESIZE:
                print(f"Delete: {key} Key Comparisons: {comparison}")
            else:
                print("Error")
            print("Enter selection: ", end="")
        elif opt == 3:
            for j in range(TABLESIZE):
                marker = '*' if hash_table[j].indicator == DELETED else ' '
                print(f"{j}: {hash_table[j].key} {marker}")
            print("Enter selection: ", end="")
        elif opt == 4:
            break
        else:
            continue

if __name__ == "__main__":
    main()     # Writing output to STDOUT