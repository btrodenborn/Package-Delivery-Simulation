#Citing source: C950 - Webinar-1 - Let’s Go Hashing

#the data structure for the program
class ChainingHashTable:
    def __init__(self, initial_capacity=10):

        self.table = []
        for i in range(initial_capacity):
            self.table.append([])


#insert a value into the hash table
    def insert(self, key, item):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

#search for a value in the hash table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

#remove a value in the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

