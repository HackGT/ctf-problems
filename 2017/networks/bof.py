'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
import random

class ASM(object):
    def __init__(self, size):
        self.queue = []        
        self.memory = []
        self.size = size
        for i in range(size):
            self.memory.append(None)

    def write_memory(address, data):
        counter = 0
        for byt in bytearray(data):
            self.memory[address + counter] = byt
            counter += 1

    def read_memory(address)
        return self.memory[address]

    def read_queue():
        self.queue = 

def clientthread(conn):
    #Sending message to connected client
    isWinner = True 
    #infinite loop so that function do not terminate and thread do not end.
    for i in range(0, 500):
        data = conn.recv(1024)
        try:
            data = data.strip()
            ints = data.split(" ")
            for i in range(0, len(ints)):
                ints[i] = int(ints[i])
            if len(ints) != 2:
                raise Exception
        except:
            conn.send("ERROR PARSING INPUT\n")
            isWinner = False
            break
        if ints[0] == userBBST.targetRow and ints[1] == userBBST.targetCol:
            userBBST = Maze()
            conn.send(userBBST.dispMaze())
        else:
            conn.send("WRONG\n")
            isWinner = False
            break
    if isWinner:
        conn.send("Congrats my friend! You have escaped the maze. \n")
        conn.send("The flag is... hackgt{use_this_as_your_hack} \n") 
    conn.close()
    
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 9002 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client
try: 
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        start_new_thread(clientthread, (conn,))
except KeyboardInterrupt:
    s.close()	
