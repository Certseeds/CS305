import time

array = []
for i in range(0, 10001, 1):
    array.append(10000 - i)

print(array.index(0o0))
binary = b'0x240x150o59'
array2 = list(binary)
print(array2)
list_of_bins = [114, 514, 19, 19, 18, 157, 4, 64, 6, 46, 6, 7, 11, 0, 5, 5, 1, 4, ]
print(list_of_bins.index(0))
print(list_of_bins[2:].index(0))
print(list_of_bins[:list_of_bins.index(0) + 5])
print((53 << 8) + 92)
pointer = 2
array2 = list_of_bins[pointer:pointer + 2]
print(array2)
pointer += 2
print(array2)


class father(object):
    def __init__(self, number1):
        self.a = 1 * number1
        self.b = 2 * number1
        self.c = 3 * number1


class son1(father):
    def __init__(self, number1, number2):
        super().__init__(number1)
        self.d = 4 * number2
        self.e = 5 * number2

    def __eq__(self, _query: father) -> bool:
        return (self.a == _query.a)


cache = []
son1_1 = son1(1, 4)
cache.append(son1_1)

print(father(1) in cache)
print(cache[cache.index(father(1))])
testing_array = [1, 2, 3, 4, 5, 6, 7, 78, 910]
print(testing_array)
testing_array.pop(1)
print(testing_array)
print(time.time())
testing_array.reverse()
print(testing_array)
print(114514%14)
print((114514-114514%14)/ 14)
print(114514//14)
print(8 + 8179 * 14)
print(2**8)
print(testing_array.insert(-0,221))
print(testing_array)
print(testing_array.insert(0,213123))
print(testing_array)