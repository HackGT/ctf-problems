import socketserver
import time
import random

FLAG = "hackgt{}\n"

INTRO_STR = """Hello user,
welcome to a game of chance and skill.
To truly be 1337, you need to have 1337 ^ 13 coins
"""

MAGIC = (1337 ** 13) * 1.0

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(INTRO_STR.encode())
        total_coins = 5.0

        while True:
            if total_coins <= 0.0:
                self.request.sendall(b"You LOSE...\n")
                return
            if not total_coins < MAGIC:
                self.request.sendall(FLAG.encode())
            y = random.randint(1, 1000) * 1.0
            self.request.sendall("How much do you want to bet that the random int is > {}\n".format(y).encode())
            bet = None
            try:
                bet = float(self.request.recv(2048).strip())
            except:
                self.request.sendall(b"THATS NOT A FLOAT... TRY AGAIN\n")
                return

            if bet <= 0.0:
                self.request.sendall(b"Haha nice try...\n")
                return
            self.request.sendall(b"""Generating Random int....
            Seriously it is actually random. Please don't try and
            waste your time trying to crack the randomness. It's not
            the solution. It would be in crypto if it was.
                    """)
            x = random.randint(1, 1000) * 1.0

            if x > y:
                total_coins += bet
                self.request.sendall(b"NICE YOU GOT IT!!!!\n")
            else:
                total_coins -= bet
                self.request.sendall(b"RIP I'm SORRY\n")
            self.request.sendall("You now have {} coins!\n".format(total_coins).encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 6789

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
