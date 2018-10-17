import struct
import sys


with open(sys.argv[1], 'rb') as fh:
    contents = fh.read()


# for i in range(20):
#     print(struct.unpack('<Q', contents[i*4+2:(i+1)*4+2])[0])

ph_addr = struct.unpack('<Q', contents[32:40])[0]
ph_size = struct.unpack('<H', contents[54:56])[0]
ph_num = struct.unpack('<H', contents[56:58])[0]

target = ph_addr + ph_size * 3 + 4
assert struct.unpack('<I', contents[target:target+4])[0] == 5
contents = contents[0:target] + b'\x07' + contents[target+1:]

with open(sys.argv[1], 'wb') as fh:
    fh.write(contents)
