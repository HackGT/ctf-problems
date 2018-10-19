import sys
import random

box_of_tricks = '¯\(ツ)/¯'

def deserialize_to_value_from_bytes(bytes):
    hexStr = ''
    for char in bytes:
        hexPair = hex(char)[2:]
        if len(hexPair) == 1:
            hexPair = '0' + hexPair
        hexStr += hexPair
    return int(hexStr, 16)

def binPad(binStr, size):
    paddedBinStr = binStr
    while len(paddedBinStr) < size:
        paddedBinStr = '0' + paddedBinStr
    return paddedBinStr

def serialize_to_bytes_from_value(value, numBytes):
    vBin = bin(value)[2:]
    vBin = binPad(vBin, 8 * numBytes)
    bytesStr = bytearray()
    for x in range(len(vBin) // 8):
        bytesStr.append(int(vBin[8 * x : 8 * x + 8], 2))
    return bytes(bytesStr)

def broken_decrypt(keyBinStr, value):
    key = int(keyBinStr, 2)
    mystery = int(''.join([bin(ord(random.choice(box_of_tricks)))[-3:-1] for x in range(len(keyBinStr) // 2)]), 2)
    return value ^ key ^ mystery

def pipe(keyBinStr, reader, writer):
    writer.write(b"Send me " + str(len(keyBinStr) // 8).encode() + b" bytes!\n")
    writer.flush()
    c = reader.read(len(keyBinStr) // 8)
    outVal = broken_decrypt(keyBinStr, deserialize_to_value_from_bytes(c))
    outBytes = serialize_to_bytes_from_value(outVal, len(keyBinStr) // 8)
    writer.write(outBytes)
    writer.flush()

def main():
    k = open('key', 'rb')
    keyBinStr = k.read()
    k.close()
    pipe(keyBinStr, sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
  sys.exit(main())