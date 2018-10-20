import socket
import time
import random
import threading

FLAG = "This is a test of your decription skills: hackgt{se3d_reap_repeat}"

def kinda_xor(string, key):
    to_return = ""
    for i in range(len(string)):
        to_return += chr(ord(string[i]) ^ ord(key[i % len(key)]))
    return to_return

def gen_key_str(rand_dec, length):
    to_return = ""
    tenner = rand_dec * 10
    for _ in range(length):
        tenner_int = int(tenner)
        to_return += str(tenner_int)
        tenner *= 10
    return to_return

def handle(conn, addr):
    # self.request is the TCP socket connected to the client
    t = int(time.time())
    random.seed(t)
    key = random.random()

    key_str = gen_key_str(key, len(FLAG))
    xored = kinda_xor(FLAG, key_str)
    to_send = "Sending test message (definitely not the flag)\n"
    to_send += xored
    to_send += "\n"
    to_send += "What do you want to encrypt?\n"
    conn.sendall(to_send.encode())
    data = conn.recv(1024).strip().decode("utf-8")

    key_str2 = gen_key_str(key, len(data))
    xored2 = kinda_xor(data, key_str2)

    print(key_str)
    print(key_str2)
    print(key_str == key_str2)
    print(xored == xored2)
    conn.sendall(xored2.encode())
    conn.sendall(b"\n\n")
    conn.close()

if __name__ == "__main__":
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 9090 # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        sys.exit()

    #Start listening on socket
    s.listen(10)

    #now keep talking with the client
    try:
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            t = threading.Thread(target=handle, args=(conn, addr))
            t.start()
    except KeyboardInterrupt:
        s.close()
