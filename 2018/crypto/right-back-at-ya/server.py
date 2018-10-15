import socketserver
import time
import random

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

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
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
        self.request.sendall(to_send.encode())
        self.data = self.request.recv(1024).strip().decode("utf-8")

        key_str2 = gen_key_str(key, len(self.data))
        xored2 = kinda_xor(self.data, key_str2)

        print(key_str)
        print(key_str2)
        print(key_str == key_str2)
        print(xored == xored2)
        self.request.sendall(xored2.encode())
        self.request.sendall(b"\n\n")

if __name__ == "__main__":
    HOST, PORT = "localhost", 9876

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
