i = [103, 14, 111, 2, 97, 24, 105, 28, 122, 28, 102, 7, 107, 27, 98, 17]
k = bytearray(i)

for ind, x in enumerate(i):
    if ind % 2 == 0:
        k[ind] ^= ind
    else:
        k[ind] ^= i[ind - 1]
print(k)
