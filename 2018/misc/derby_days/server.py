import time
import random
import threading
import socket
import sys

FLAG = "hackgt{NaNaNaNa_NaNaNaNa_hey_hey_hey____g0odby3}\n"

INTRO_STR = """Hello user,
welcome to a game of chance and skill.
To truly be 1337, you need to have 1337 ^ 13 coins
"""

MAGIC = (1337 ** 13) * 1.0
def handle(conn, addr):
    conn.sendall(INTRO_STR.encode())
    total_coins = 5.0

    while True:
        if total_coins <= 0.0:
            conn.sendall(b"You LOSE...\n")
            break
        if not total_coins < MAGIC:
            conn.sendall(FLAG.encode())
        y = random.randint(1, 1000) * 1.0
        conn.sendall("How much do you want to bet that the random int is > {}\n".format(y).encode())
        bet = None
        try:
            bet = float(conn.recv(2048).strip())
        except:
            conn.sendall(b"THATS NOT A FLOAT... TRY AGAIN\n")
            break

        if bet <= 0.0:
            conn.sendall(b"Haha nice try...\n")
            break
        elif bet >= total_coins:
            conn.sendall(b"Haha nice try...\n")
            break
        conn.sendall(b"""Generating Random int....
        Seriously it is actually random. Please don't try and
        waste your time trying to crack the randomness. It's not
        the solution. It would be in crypto if it was.
                """)
        x = random.randint(1, 1000) * 1.0

        if x > y:
            total_coins += bet
            conn.sendall(b"NICE YOU GOT IT!!!!\n")
        else:
            total_coins -= bet
            conn.sendall(b"RIP I'm SORRY\n")
        conn.sendall("You now have {} coins!\n".format(total_coins).encode())
    conn.close()

if __name__ == "__main__":
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8989 # Arbitrary non-privileged port

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
