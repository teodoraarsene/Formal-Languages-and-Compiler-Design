from HashTable import HashTable

if __name__ == '__main__':
    ht = HashTable(11)

    print(ht.contains("abracadabra"))

    ht.insert("abracadabra")

    ht.insert(1234)

    ht.insert("1234")

    ht.insert("b")

    ht.insert(2)
    print(ht)


