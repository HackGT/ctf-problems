'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
import random
 
class Maze():
    def __init__(self):
        self.targetRow = 0
        self.targetCol = 0
        self.targetString = "FLAGLOL"
        self.maze = []
        self.size = 10
        self.populate()
        self.insertTarget()
    
    def insertTarget(self):
        posList = []
        while posList == []:
            self.targetRow = int(random.random() * self.size)
            self.targetCol = int(random.random() * self.size)
            posList = self.getPossiblePlacements(self.targetRow, self.targetCol)
        posList[int(random.random() * (len(posList)-1))]()
    
    def getPossiblePlacements(self, row, col):
        posList = []
        length = len(self.targetString)
        canDown = (row + length <= self.size)
        canUp = (row - length >= 0)
        canRight = (col + length <= self.size)
        canLeft = (col - length >= 0)
        
        if canDown:
            posList.append(self.insertD)
            if canRight:
                posList.append(self.insertDR)
            if canLeft:
                posList.append(self.insertDL)
        if canUp:
            posList.append(self.insertU)
            if canRight:
                posList.append(self.insertUR)
            if canLeft:
                posList.append(self.insertUL)
        if canLeft:
            posList.append(self.insertL)
        if canRight:
            posList.append(self.insertR)
        return posList
    
    def insertD(self):
        for i in range(0, len(self.targetString)):
            self.maze[i + self.targetRow][self.targetCol] = self.targetString[i]
    
    def insertU(self):
        for i in range(0, len(self.targetString)):
            self.maze[self.targetRow - i][self.targetCol] = self.targetString[i]
    
    def insertL(self):
        for i in range(0, len(self.targetString)):
            self.maze[self.targetRow][self.targetCol - i] = self.targetString[i]

    def insertR(self):
        for i in range(0, len(self.targetString)):
            self.maze[self.targetRow][self.targetCol + i] = self.targetString[i]
    
    def insertDR(self):
        for i in range(0, len(self.targetString)):
            self.maze[i + self.targetRow][self.targetCol + i] = self.targetString[i]
    
    def insertDL(self):
        for i in range(0, len(self.targetString)):
            self.maze[i + self.targetRow][self.targetCol - i] = self.targetString[i]
    
    def insertUR(self):
        for i in range(0, len(self.targetString)):
            self.maze[self.targetRow - i][self.targetCol + i] = self.targetString[i]
    
    def insertUL(self):
        for i in range(0, len(self.targetString)):
            self.maze[self.targetRow - i][self.targetCol - i] = self.targetString[i]
    def getLetter(self):
        return chr(int(random.random() * 100 % 26) + 65)
    
    def populate(self):
        for i in range(0, self.size):
            tempList = []
            for j in range(0, self.size):
                tempList.append(self.getLetter())
            self.maze.append(tempList)

    def dispMaze(self):
        toRet = ['',]
        for i in range(0, self.size):
            for j in range(0, self.size):
                toRet.append(self.maze[i][j])
            toRet.append("\n")
        return " ".join(toRet)
        
def clientthread(conn):
    #Sending message to connected client
    userBBST = Maze()
    conn.send(userBBST.dispMaze())
    isWinner = True 
    #infinite loop so that function do not terminate and thread do not end.
    for i in range(0, 100):
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
