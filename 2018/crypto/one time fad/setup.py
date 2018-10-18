import random
import os
import binascii

key = bytearray()
if 'flag' not in os.environ:
    raise ValueError('You must set the \'flag\' environment variable before setting up the problem!')
plainText = bytearray(os.environ['flag'], 'utf-8')
size = len(plainText)

for x in range(8 * len(plainText)):
    key.append(random.choice([ord('0'), ord('1')]))

k = open('key', 'wb')
k.write(bytes(key))
k.close()

plainTextHex = binascii.hexlify(plainText)

plainTextVal = int(plainTextHex, 16)
keyVal = int(key, 2)
cipherTextBin = bin(plainTextVal ^ keyVal)[2:]
while len(cipherTextBin) < 8 * size:
    cipherTextBin = '0' + cipherTextBin

cipherText = bytearray()
for x in range(len(cipherTextBin) // 8):
    cipherText.append(int(cipherTextBin[8 * x : 8 * x + 8], 2))

c = open('flag.enc', 'wb')
c.write(cipherText)
c.close()