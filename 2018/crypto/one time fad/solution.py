from pwn import *

def deserialize_from_char_to_bin(bytes):
    binStr = ''
    for byte in bytes:
        binByte = bin(byte)[2:]
        binStr += binPad(binByte, 8)
    return binStr

def generate_final_xor_key(bytesLength):
    xfkey = ''
    for x in range(bytesLength * 8):
        if x % 2 == 0:
            xfkey += '1'
        else:
            xfkey += '0'
    return int(xfkey, 2)

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

cF = open('flag.enc', 'rb')
c = cF.read()
cF.close()

bin_dict = [0] * len(c) * 8
for x in range(500):
    print(x)
    try:
        s = remote("127.0.0.1", 3000)
        s.recv(100)
        s.send(c)
        a = bytearray(s.recv(len(c)))
        s.close()
        d = deserialize_from_char_to_bin(a)
        for bin_char_ind in range(len(d)):
            if d[bin_char_ind] == '0':
                bin_dict[bin_char_ind] -= 1
            else:
                bin_dict[bin_char_ind] += 1
    except:
        pass

print(bin_dict)

bin_final = ''
for v in bin_dict:
    if v > 0:
        bin_final += '1'
    elif v < 0:
        bin_final += '0'
    else:
        raise ValueError('Even distribution of 0 and 1, try running again or raise sample size')

flag_value = int(bin_final, 2) ^ generate_final_xor_key(len(c))

print(str(serialize_to_bytes_from_value(flag_value, len(c))))
