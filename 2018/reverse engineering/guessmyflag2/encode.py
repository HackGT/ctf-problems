i = input()
i = bytearray(i, 'utf-8')
b = bytearray()

for ind, x in enumerate(i):
    if ind % 2 == 0:
        b.append(i[ind] ^ ind)
    else:
        b.append(i[ind] ^ i[ind - 1])

l = []
for z in b:
    l.append(z)
print(l)