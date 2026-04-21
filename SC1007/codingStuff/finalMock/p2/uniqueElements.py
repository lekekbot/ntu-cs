class HashTableNode:
    def __init__(self, key=None):
        self.key = key
        self.deleted = False


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash(self, key, i):
        return (key + i) % self.size

    def hash_delete(self, key):
        i = 0
        index = self._hash(key, i)

        while self.table[index] is not None:
            if self.table[index].key == key and not self.table[index].deleted:
                self.table[index].deleted = True
                return True
            i += 1
            if i >= self.size:
                return False
            index = self._hash(key, i)

        return False

    def hash_search(self, key):
        i = 0
        index = self._hash(key, i)

        while self.table[index] is not None:
            if self.table[index].key == key and not self.table[index].deleted:
                return True
            i += 1
            if i >= self.size:
                return False
            index = self._hash(key, i)

        return False
        
        
    def hash_insert(self, key):
        c = 0
        while c < self.size:
            i = self._hash(key, c)
            if self.table[i] is None:
                self.table[i] = HashTableNode(key)
                return True
            elif self.table[i].deleted:
                self.table[i] = HashTableNode(key)
                self.table[i].deleted = False
                return True
            
            if self.table[i].key == key:
                return False
            c += 1
        return False


def count_unique(nums):
    ht = HashTable(max(2 * len(nums), 1))
    count = 0
    for i in nums:
        j = ht.hash_insert(i)
        if j is not False:
            count += 1
    return count
    #add your codes


nums = list(map(int, input().split()))
result = count_unique(nums)
print(result)